# Enterprise AI Ticket Intelligence Platform

## Azure Account
- **Account:** `santoshdadhich84@gmail.com` (Azure for Students / Free Trial)
- **Subscription ID:** `7d8e5aef-155c-408d-b300-ef7e2b2dfaa2`
- **Tenant ID:** `752909f2-c8de-4b2d-ac63-1a22ac3891cd`
- **Migrated from:** IBM account (`Aryan.Dadheech@ibm.com`) — old state backed up as `terraform.tfstate.old-ibm`

## Project Goal
Build a production-grade AI-powered enterprise ticket intelligence platform on Azure.

## ✅ Infrastructure Completed
- [x] Resource Group (`rg-ai-ticket-dev`)
- [x] Storage Account (`aiticketstorage99`) with `documents` blob container
- [x] Key Vault (`kv-aiticket99`)
- [x] Azure OpenAI resource (`aoai-arya001`) — GPT-4o + text-embedding-3-small deployed
- [x] Application Insights (`appi-aiticket-dev`)
- [x] Log Analytics Workspace (`law-aiticket-dev`)
- [x] Azure AI Search (`aisearch-aiticket-v2`, Standard SKU, SystemAssigned identity, RBAC on Storage)
- [x] AI Search destroyed to save cost — rebuilds in 5 min via `terraform apply`

## ✅ AI Foundry + Model Deployment Completed
- [x] Azure AI Foundry project created (connected to Azure OpenAI resource)
- [x] GPT-4o deployed (`gpt-4o`)
- [x] text-embedding-3-small deployed (for semantic/vector search)

## ✅ Knowledge Pipeline Completed
- [x] Knowledge documents created (`Knowledge/*.md`) — runbooks, incident reports, priority guide
  - `logic-app-authentication-runbook.md`
  - `database-connection-runbook.md`
  - `api-integration-troubleshooting.md`
  - `incident-priority-guide.md`
  - `previous-incident-logic-app-401.md`
- [x] Ingestion script (`scripts/ingest_documents.py`) — uploads docs to Blob Storage via DefaultAzureCredential
- [x] GitHub Actions OIDC pipeline (`.github/workflows/ingest-knowledge.yml`) — triggers on push to `Knowledge/`, no secrets stored
- [x] Pipeline ran successfully (green ✅, 27s)

## ✅ AI Search RAG Configuration Completed
- [x] `scripts/setup_ai_search.py` — creates datasource, index, indexer via REST API
- [x] `.github/workflows/setup-ai-search.yml` — GitHub Actions pipeline (manual trigger)
- [x] Pipeline ran successfully (green ✅, 1m 9s)
- [x] Datasource: `blob-documents` (points to storage container)
- [x] Index: `knowledge-index` (id, content, metadata fields)
- [x] Indexer: `blob-indexer` (schedule: PT5M, triggered immediately)
- [x] AI Search destroyed after setup to save cost (₹18,000/month!)

## ✅ RAG API (FastAPI) Completed
- [x] `app/config.py` — Azure OpenAI settings, MOCK_MODE flag
- [x] `app/models.py` — Pydantic request/response validation
- [x] `app/rag.py` — Full RAG pipeline (load docs → keyword match → GPT-4o)
- [x] `app/main.py` — FastAPI app with 3 endpoints
- [x] `app/requirements.txt` — Python dependencies
- [x] API running locally on `http://localhost:8000`
- [x] Swagger docs at `http://localhost:8000/docs`
- [x] `/analyze-ticket` returning 200 OK with correct sources ✅
- [x] MOCK_MODE=true (works without Azure credits)

## ⏳ Pending (Nice to Have)
- [ ] Docker — containerize the app (solves version issues)
- [ ] Application Insights — wire monitoring into FastAPI
- [ ] Real GPT test — needs Azure credits (MOCK_MODE=false)
- [ ] Re-enable AI Search + semantic search upgrade
- [ ] Deploy to Azure (App Service or Container Apps)

## 🎯 Interview Prep
- [ ] Architecture diagram
- [ ] README update
- [ ] Practice explanation

## Current Cost Status
- AI Search: DESTROYED ✅ (was ₹18,000/month)
- Azure OpenAI: Pay per use (₹0 when not calling)
- Storage + Key Vault: <₹1/month
- App Insights: Free tier

## Skills Learned
- Terraform (Infrastructure as Code)
- Azure Architecture
- Azure OpenAI + AI Foundry
- RAG (Retrieval-Augmented Generation)
- Keyword + Semantic Search
- Prompt Engineering
- FastAPI + Pydantic
- GitHub Actions + OIDC (Workload Identity Federation)
- API Development
- Production Security (no hardcoded secrets)
- Azure RBAC (Role-Based Access Control)
