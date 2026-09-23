"""
config.py
---------
Central configuration for the RAG API.

All sensitive values (API keys) are read from environment variables.
Non-sensitive values (endpoints, model names) are hardcoded here since
they are not secrets — just configuration.

Locally:
    Create app/.env file with:
        AZURE_OPENAI_KEY=your_key_here
    Then run: uvicorn app.main:app --reload

In Production:
    Set AZURE_OPENAI_KEY as an environment variable (Key Vault / App Service config)
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file if it exists (local development only)
# In production, environment variables are set directly — no .env file needed
load_dotenv(Path(__file__).parent / ".env")

# ---------------------------------------------------------------------------
# Azure OpenAI settings
# ---------------------------------------------------------------------------

# The endpoint for our Azure OpenAI resource
AZURE_OPENAI_ENDPOINT = "https://aoai-arya001-517ec.openai.azure.com/"

# API key — read from environment variable, never hardcoded
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY", "")

# The deployment name we created in Azure AI Foundry
GPT_DEPLOYMENT_NAME = "gpt-4o"

# API version for Azure OpenAI REST API
AZURE_OPENAI_API_VERSION = "2024-02-01"

# ---------------------------------------------------------------------------
# Knowledge base settings
# ---------------------------------------------------------------------------

# Path to the Knowledge/ folder (relative to repo root)
# This is used for local RAG when AI Search is not available
KNOWLEDGE_DIR = Path(__file__).parent.parent / "Knowledge"

# ---------------------------------------------------------------------------
# AI Search settings (used when AI Search is enabled)
# ---------------------------------------------------------------------------

AZURE_SEARCH_SERVICE  = os.environ.get("AZURE_SEARCH_SERVICE", "aisearch-aiticket-v2")
AZURE_SEARCH_KEY      = os.environ.get("AZURE_SEARCH_KEY", "")
AZURE_SEARCH_INDEX    = "knowledge-index"
