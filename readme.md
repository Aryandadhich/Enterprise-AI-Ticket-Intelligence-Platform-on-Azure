# Enterprise AI Ticket Intelligence Platform on Azure

> A production-grade GenAI platform for enterprise incident and ticket intelligence, built on Microsoft Azure.

## Overview

Enterprise support teams receive a large number of incidents and service tickets every day. Understanding an incident often requires engineers to search through previous incidents, knowledge-base articles, runbooks, application logs, and monitoring data before deciding what to do next.

This platform is being built to assist engineers throughout that investigation process — grounding AI responses in real enterprise knowledge rather than relying on a general-purpose LLM alone.

Instead of simply summarizing a ticket, the platform progressively evolves toward:

- Understanding and classifying incidents
- Identifying severity and affected services
- Finding similar historical incidents
- Retrieving relevant enterprise knowledge (runbooks, playbooks, past incidents)
- Generating evidence-based root-cause hypotheses
- Recommending troubleshooting and remediation steps
- Using AI agents and tools for deeper automated investigation
- Keeping humans in control of high-impact actions
- Providing production-grade monitoring, security, and observability

---

## Project Goals

1. Reduce the time engineers spend investigating incidents.
2. Ground AI responses in enterprise knowledge instead of relying only on LLM knowledge.
3. Combine ticket information with historical incidents and operational telemetry.
4. Provide evidence and reasoning behind AI-generated recommendations.
5. Introduce Agentic AI for multi-step investigation and tool usage.
6. Maintain human approval for potentially impactful actions.
7. Build all infrastructure using Infrastructure as Code (Terraform).
8. Apply production-oriented security, observability, reliability, and deployment practices.

---

## High-Level Architecture

```
                         Enterprise Ticket
                                │
                                ▼
                       Ticket Ingestion API
                                │
                                ▼
                    ┌────────────────────────┐
                    │   AI Processing Layer  │
                    │                        │
                    │ Azure OpenAI / Foundry │
                    └───────────┬────────────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
          Ticket Analysis   Knowledge Base   Telemetry
                 │              │              │
                 │              ▼              ▼
                 │       Azure AI Search   App Insights
                 │              │          / Log Analytics
                 │              │              │
                 └──────────────┼──────────────┘
                                ▼
                         RAG / Grounding
                                │
                                ▼
                       Incident Intelligence
                                │
                                ▼
                       AI Investigation Agent
                                │
                     ┌──────────┴──────────┐
                     │                     │
                     ▼                     ▼
              Recommendation        Human Approval
                                           │
                                           ▼
                                  Controlled Automation
```

---

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── ingest-knowledge.yml      # CI/CD: auto-uploads Knowledge docs to Azure Blob
│
├── Knowledge/                        # Enterprise knowledge base (markdown documents)
│   ├── api-integration-troubleshooting.md
│   ├── database-connection-runbook.md
│   ├── incident-priority-guide.md
│   ├── logic-app-authentication-runbook.md
│   └── previous-incident-logic-app-401.md
│
├── modules/                          # Terraform modules (one per Azure resource)
│   ├── ai_search/                    # Azure AI Search (Standard SKU, managed identity)
│   ├── application_insights/         # Application Insights (linked to Log Analytics)
│   ├── Azure_openai/                 # Azure OpenAI Service
│   ├── key_vault/                    # Azure Key Vault
│   ├── log_analytics_workspace/      # Log Analytics Workspace
│   ├── resource_group/               # Azure Resource Group
│   └── storage_account/             # Storage Account + documents blob container
│
├── scripts/
│   ├── ingest_documents.py           # Ingestion script: uploads Knowledge/*.md to blob
│   └── requirements.txt              # Python dependencies
│
├── main.tf                           # Root Terraform: wires all modules together
├── variables.tf                      # Input variable declarations
├── terraform.tfvars                  # Variable values (non-sensitive)
├── output.tf                         # Output values after terraform apply
├── provider.tf                       # Azure provider configuration
└── version.tf                        # Terraform and provider version constraints
```

---

## What Is Built So Far

### Phase 1 — Azure Infrastructure (Terraform) ✅

All infrastructure is defined as code using Terraform modules. Running `terraform apply` provisions everything from scratch.

| Resource | Purpose |
|---|---|
| Resource Group | Logical container for all platform resources |
| Storage Account | Blob storage for raw knowledge documents (`documents/` container) |
| Key Vault | Secure storage for secrets and credentials |
| Azure OpenAI | Azure OpenAI Service resource (S0 SKU) |
| Log Analytics Workspace | Centralised log collection and querying |
| Application Insights | Application performance monitoring and telemetry |
| Azure AI Search | Full-text and vector search over enterprise knowledge documents |

Notable infrastructure decisions:
- AI Search uses a **SystemAssigned Managed Identity** — no credentials stored
- RBAC role assignment grants AI Search **Storage Blob Data Reader** on the Storage Account — indexer can read documents without keys

### Phase 2 — AI Foundry + Model Deployment ✅

Azure AI Foundry project created and a GPT model deployed and configured as an initial agent.

- Azure AI Foundry project connected to the Azure OpenAI resource
- GPT model deployed (available for RAG integration)
- Initial agent configuration done inside Foundry
- RAG integration with AI Search is the next step

### Phase 3 — Knowledge Ingestion Pipeline ✅

A production-grade pipeline that automatically uploads enterprise knowledge documents to Azure Blob Storage whenever files change in the repository.

**Document types in `Knowledge/`:**
- Runbooks (step-by-step investigation and remediation guides)
- Previous incident reports (historical context for AI grounding)
- Priority guides (business impact classification)

**How the pipeline works:**

```
Engineer adds/updates a .md file in Knowledge/
             ↓
Git push to main branch
             ↓
GitHub Actions triggers automatically (ingest-knowledge.yml)
             ↓
Authenticates to Azure using OIDC — no secrets stored
             ↓
ingest_documents.py uploads Knowledge/*.md to Azure Blob Storage
             ↓
Azure AI Search Indexer picks up changes (next phase)
             ↓
Search Index updated with latest knowledge
```

**Authentication — GitHub Actions OIDC (Workload Identity Federation):**

No Azure credentials are stored in GitHub. Instead:
1. GitHub requests a short-lived token (~10 min) from Azure AD at runtime
2. Azure AD verifies the request is genuinely from this repository and branch
3. A scoped token is issued and used to authenticate the upload
4. Token expires automatically — nothing to rotate or leak

---

## Getting Started

### Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.5
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- Python 3.11+
- An Azure subscription
- A GitHub repository with OIDC federated credentials configured (see below)

### 1. Provision Infrastructure

```bash
az login
terraform init
terraform apply
```

### 2. Configure GitHub Actions OIDC (one-time manual setup)

This step is always done manually — it is a security policy decision that a human must consciously approve.

**In Azure Portal:**
1. Go to **Azure Active Directory → App Registrations → New Registration**
2. Name it (e.g. `sp-ai-ticket-github`)
3. Go to **Certificates & secrets → Federated credentials → Add credential**
4. Select **GitHub Actions** → enter your repo name and `main` branch

**In GitHub (Settings → Variables → Actions):**
```
AZURE_CLIENT_ID       = <app registration client ID>
AZURE_TENANT_ID       = <your Azure AD tenant ID>
AZURE_SUBSCRIPTION_ID = <your Azure subscription ID>
```

**In GitHub (Settings → Secrets → Actions):**
```
AZURE_STORAGE_ACCOUNT = aiticketstorage12
```

**Grant the App Registration access to Storage:**
```bash
az role assignment create \
  --assignee <client-id> \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/rg-ai-ticket-dev/providers/Microsoft.Storage/storageAccounts/aiticketstorage12
```

### 3. Run Ingestion Locally

```bash
pip install -r scripts/requirements.txt
az login
python scripts/ingest_documents.py
```

---

## What Is Coming Next

- [x] Azure Infrastructure (Terraform) — all resources provisioned
- [x] Azure AI Foundry project setup
- [x] GPT model deployment and initial agent configuration
- [x] Knowledge ingestion pipeline (GitHub Actions OIDC → Blob Storage)
- [ ] GitHub ↔ Azure OIDC connection setup (one-time manual step)
- [ ] Azure AI Search — datasource, index, and indexer configuration
- [ ] RAG integration — connect AI Search + Azure OpenAI inside Foundry
- [ ] Ticket ingestion API
- [ ] AI ticket analysis (classification, severity, similar incidents)
- [ ] Agentic AI — multi-step investigation with tools
- [ ] Monitoring and tracing (Application Insights integration)
- [ ] Production API with authentication
- [ ] Full deployment pipeline

---

## Technologies Used

| Category | Technology |
|---|---|
| Cloud | Microsoft Azure |
| Infrastructure as Code | Terraform |
| AI / LLM | Azure OpenAI (GPT-4o) |
| Knowledge Search | Azure AI Search |
| Document Store | Azure Blob Storage |
| Secret Management | Azure Key Vault |
| Monitoring | Application Insights, Log Analytics |
| CI/CD | GitHub Actions |
| Auth (CI/CD) | OIDC Workload Identity Federation |
| Language | Python 3.11 |

---

## Skills Being Developed

Terraform · Azure Architecture · Azure OpenAI · AI Foundry · RAG · Vector Search · Prompt Engineering · AI Agents · API Development · Monitoring · Security · Production AI Architecture · GitHub Actions · OIDC Authentication
