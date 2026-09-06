# Enterprise AI Ticket Intelligence Platform

## Azure Account
- **Account:** `santoshdadhich84@gmail.com` (Azure for Students / Free Trial)
- **Subscription ID:** `7d8e5aef-155c-408d-b300-ef7e2b2dfaa2`
- **Tenant ID:** `752909f2-c8de-4b2d-ac63-1a22ac3891cd`
- **Migrated from:** IBM account (`Aryan.Dadheech@ibm.com`) — old state backed up as `terraform.tfstate.old-ibm`

## Project Goal
Build a production-grade AI-powered enterprise ticket intelligence platform on Azure.

## Infrastructure Completed
- [x] Resource Group
- [x] Storage Account (`aiticketstorage99`) with `documents` blob container
- [x] Key Vault (`kv-aiticket99`)
- [x] Azure OpenAI resource
- [x] Application Insights
- [x] Log Analytics Workspace
- [x] Azure AI Search (`aisearch-aiticket-v2`, Standard SKU, SystemAssigned identity, RBAC on Storage)

## AI Foundry + Model Deployment Completed
- [x] Azure AI Foundry project created (connected to Azure OpenAI resource)
- [x] GPT model deployed inside Foundry
- [x] Initial agent configuration done in Foundry
- [ ] RAG integration with AI Search — pending

## Knowledge Pipeline Completed
- [x] Knowledge documents created (`Knowledge/*.md`) — runbooks, incident reports, priority guide
- [x] Ingestion script (`scripts/ingest_documents.py`) — uploads docs to Blob Storage via DefaultAzureCredential
- [x] GitHub Actions OIDC pipeline (`.github/workflows/ingest-knowledge.yml`) — triggers on push to `Knowledge/`, no secrets stored
- [x] `scripts/requirements.txt`

## Pending One-Time Azure Setup
- [ ] Create App Registration with Federated Credential (OIDC) for GitHub Actions
- [ ] Add GitHub Variables: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID
- [ ] Add GitHub Secret: AZURE_STORAGE_ACCOUNT

## Current Phase
GitHub ↔ Azure OIDC connection + AI Search RAG configuration

## Next Steps
- [ ] Build GitHub ↔ Azure OIDC connection and test pipeline end-to-end
- [ ] Configure AI Search datasource → index → indexer (pointing at blob container)
- [ ] RAG integration — connect AI Search + Azure OpenAI inside Foundry
- [ ] Build ticket ingestion API
- [ ] Build AI ticket analysis
- [ ] Add monitoring and tracing
- [ ] Add Agentic AI capabilities
- [ ] Build production-style API
- [ ] Deploy application
- [ ] Prepare architecture + interview explanation

## Skills We Are Learning
- Terraform
- Azure Architecture
- Azure OpenAI
- AI Foundry
- RAG
- Vector Search
- Prompt Engineering
- AI Agents / Agentic AI
- API Development
- Monitoring
- Security
- Production AI Architecture