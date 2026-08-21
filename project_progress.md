# Enterprise AI Ticket Intelligence Platform

## Project Goal
Build a production-grade AI-powered enterprise ticket intelligence platform on Azure.

## Infrastructure Completed
- [x] Resource Group
- [x] Storage Account (with `documents` blob container)
- [x] Key Vault
- [x] Azure OpenAI resource
- [x] Application Insights
- [x] Log Analytics Workspace
- [x] Azure AI Search (Standard SKU, SystemAssigned identity, RBAC on Storage)

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