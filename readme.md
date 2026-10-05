# Enterprise AI Ticket Intelligence Platform

> A production-grade AI-powered platform that automatically analyzes IT support tickets using RAG (Retrieval-Augmented Generation) — combining Azure OpenAI GPT-4o with a curated enterprise knowledge base.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEVELOPER WORKFLOW                           │
│                                                                 │
│  Add Knowledge Doc → git push → GitHub Actions (OIDC)          │
│                                       ↓                        │
│                              Azure Blob Storage                 │
│                              (documents container)              │
│                                       ↓                        │
│                              AI Search Indexer                  │
│                              (every 5 min)                      │
│                                       ↓                        │
│                              knowledge-index                    │
└───────────────────────────────────────┬─────────────────────────┘
                                        │
┌───────────────────────────────────────▼─────────────────────────┐
│                    RAG API (FastAPI)                            │
│                                                                 │
│  POST /analyze-ticket                                           │
│         ↓                                                       │
│  1. Load Knowledge docs (local .md files)                       │
│  2. Find relevant docs (keyword / semantic search)              │
│  3. Build prompt: ticket + relevant docs                        │
│  4. Call Azure OpenAI GPT-4o                                    │
│  5. Return: answer + sources + model_used                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
├── app/                          # FastAPI RAG application
│   ├── main.py                   # API endpoints (/, /health, /analyze-ticket)
│   ├── rag.py                    # RAG pipeline (load → search → GPT)
│   ├── models.py                 # Pydantic request/response schemas
│   ├── config.py                 # Settings + environment variables
│   └── requirements.txt          # Python dependencies
│
├── Knowledge/                    # Enterprise knowledge base
│   ├── logic-app-authentication-runbook.md
│   ├── database-connection-runbook.md
│   ├── api-integration-troubleshooting.md
│   ├── incident-priority-guide.md
│   └── previous-incident-logic-app-401.md
│
├── scripts/                      # Automation scripts
│   ├── ingest_documents.py       # Uploads Knowledge/ docs to Blob Storage
│   ├── setup_ai_search.py        # Configures AI Search (datasource+index+indexer)
│   └── requirements.txt          # Script dependencies
│
├── .github/workflows/            # CI/CD pipelines
│   ├── ingest-knowledge.yml      # Auto-uploads docs on push to Knowledge/
│   └── setup-ai-search.yml       # One-time AI Search setup (manual trigger)
│
├── modules/                      # Terraform modules
│   ├── resource_group/
│   ├── storage_account/
│   ├── key_vault/
│   ├── Azure_openai/
│   ├── ai_search/
│   ├── log_analytics_workspace/
│   └── application_insights/
│
├── main.tf                       # Terraform root — wires all modules
├── variables.tf                  # Input variable declarations
├── terraform.tfvars              # Actual variable values
└── output.tf                     # Output values after apply
```

---

## Azure Infrastructure

| Resource | Name | Purpose |
|---|---|---|
| Resource Group | `rg-ai-ticket-dev` | Container for all resources |
| Storage Account | `aiticketstorage99` | Holds knowledge base documents |
| Key Vault | `kv-aiticket99` | Secrets management |
| Azure OpenAI | `aoai-arya001` | GPT-4o + text-embedding-3-small |
| AI Search | `aisearch-aiticket-v2` | Vector + semantic search index |
| App Insights | `appi-aiticket-dev` | Monitoring + tracing |
| Log Analytics | `law-aiticket-dev` | Centralized logs |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check — returns `{"status": "ok"}` |
| `POST` | `/analyze-ticket` | Analyze ticket using RAG |
| `GET` | `/docs` | Interactive Swagger UI |

### Example Request
```bash
POST /analyze-ticket
Content-Type: application/json

{
  "ticket": "Logic App is giving 401 unauthorized error in production"
}
```

### Example Response
```json
{
  "answer": "Based on logic-app-authentication-runbook.md, the 401 error is caused by an expired managed identity token. Steps to resolve: 1. Check the managed identity assignment...",
  "sources": [
    "logic-app-authentication-runbook.md",
    "previous-incident-logic-app-401.md"
  ],
  "model_used": "gpt-4o"
}
```

---

## How RAG Works Here

```
User ticket: "Logic App 401 error"
       ↓
1. LOAD    — Read all 5 .md files from Knowledge/
       ↓
2. SEARCH  — Find docs with 2+ keyword matches
             "logic" → logic-app-authentication-runbook.md ✅
             "401"   → previous-incident-logic-app-401.md  ✅
       ↓
3. PROMPT  — Build GPT prompt:
             System: "You are an IT support expert..."
             User:   ticket + relevant doc contents
       ↓
4. ANSWER  — GPT-4o returns grounded answer
             based ONLY on provided documents
       ↓
5. RETURN  — answer + source filenames (citations)
```

---

## Running Locally

```bash
# 1. Install dependencies
pip install -r app/requirements.txt

# 2. Create app/.env
echo "AZURE_OPENAI_KEY=your_key_here" > app/.env
echo "MOCK_MODE=true" >> app/.env   # false = real GPT calls

# 3. Start the server
python -m uvicorn app.main:app --reload

# 4. Open browser
# http://localhost:8000/docs
```

---

## Security Design

- **No secrets in code** — all keys via environment variables
- **OIDC authentication** — GitHub Actions uses short-lived tokens (no stored secrets)
- **Managed Identity** — AI Search reads Blob Storage without keys
- **RBAC** — least privilege role assignments on every resource
- **Key Vault** — centralized secret storage for production

---

## CI/CD Pipelines

| Pipeline | Trigger | What it does |
|---|---|---|
| `ingest-knowledge.yml` | Push to `Knowledge/` | Uploads .md files to Blob Storage |
| `setup-ai-search.yml` | Manual | Creates AI Search datasource + index + indexer |

Both use **OIDC Workload Identity Federation** — zero secrets stored in GitHub.

---

## Skills Demonstrated

`Terraform` `Azure OpenAI` `RAG` `FastAPI` `Pydantic` `Azure AI Search`
`GitHub Actions` `OIDC` `Managed Identity` `RBAC` `Prompt Engineering`
`Vector Search` `Python` `REST APIs` `Infrastructure as Code` `CI/CD`
