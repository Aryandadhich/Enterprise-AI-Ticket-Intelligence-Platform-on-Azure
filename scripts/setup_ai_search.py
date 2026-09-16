"""
setup_ai_search.py
------------------
Configures Azure AI Search for RAG (Retrieval-Augmented Generation) by
creating three resources against the AI Search service:

  1. Datasource  — points AI Search at the Azure Blob Storage 'documents' container
  2. Index       — defines the searchable schema (id, content, metadata fields)
  3. Indexer     — runs the crawler that reads blobs and populates the index

Run this once after initial infrastructure setup, or any time the index
schema changes. It is fully idempotent — re-running will update existing
resources, not duplicate them.

Authentication:
    Uses DefaultAzureCredential — no passwords or keys in code.

    Locally:   uses your 'az login' session.
    In CI/CD:  uses GitHub Actions OIDC (Workload Identity Federation).

    The AI Search REST API requires a bearer token obtained via the
    Search service's Azure AD endpoint.

Required environment variables:
    AZURE_SEARCH_SERVICE    - AI Search service name  (e.g. aisearch-aiticket-v2)
    AZURE_STORAGE_ACCOUNT   - Storage account name    (e.g. aiticketstorage99)
    AZURE_SUBSCRIPTION_ID   - Azure subscription ID
    AZURE_RESOURCE_GROUP    - Resource group name      (e.g. rg-ai-ticket-dev)

Usage:
    python scripts/setup_ai_search.py
"""

import json
import os
import sys

import requests
from azure.identity import DefaultAzureCredential

# ---------------------------------------------------------------------------
# Configuration — all values read from environment, no hardcoded secrets
# ---------------------------------------------------------------------------
SEARCH_SERVICE    = os.environ.get("AZURE_SEARCH_SERVICE", "aisearch-aiticket-v2")
STORAGE_ACCOUNT   = os.environ.get("AZURE_STORAGE_ACCOUNT", "aiticketstorage99")
SUBSCRIPTION_ID   = os.environ.get("AZURE_SUBSCRIPTION_ID", "")
RESOURCE_GROUP    = os.environ.get("AZURE_RESOURCE_GROUP", "rg-ai-ticket-dev")
CONTAINER_NAME    = "documents"

# Names for the three AI Search resources we will create
DATASOURCE_NAME   = "blob-documents"
INDEX_NAME        = "knowledge-index"
INDEXER_NAME      = "blob-indexer"

# AI Search REST API version — use stable 2023-11-01
API_VERSION       = "2023-11-01"
SEARCH_BASE_URL   = f"https://{SEARCH_SERVICE}.search.windows.net"

# Azure AD scope for AI Search
SEARCH_SCOPE      = "https://search.azure.com/.default"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_token() -> str:
    """Obtain a bearer token for the AI Search REST API via DefaultAzureCredential."""
    credential = DefaultAzureCredential()
    token = credential.get_token(SEARCH_SCOPE)
    return token.token


def search_request(method: str, path: str, token: str, body: dict | None = None) -> dict:
    """
    Send a REST request to the AI Search management API.

    Uses PUT (create-or-update) so the operation is always idempotent.
    Raises on HTTP errors with the full response body for diagnosis.
    """
    url = f"{SEARCH_BASE_URL}{path}?api-version={API_VERSION}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.request(
        method,
        url,
        headers=headers,
        json=body,
        timeout=60,
    )

    if response.status_code not in (200, 201, 204):
        print(f"  [HTTP {response.status_code}] {response.text}", file=sys.stderr)
        response.raise_for_status()

    # 204 No Content has no body
    if response.status_code == 204 or not response.text:
        return {}

    return response.json()


def build_storage_connection_string() -> str:
    """
    Build a managed-identity connection string for the blob datasource.

    Using ResourceId= instead of AccountKey= means AI Search authenticates
    to Blob Storage with its SystemAssigned managed identity — no keys stored.
    The managed identity must have 'Storage Blob Data Reader' on the container.
    """
    resource_id = (
        f"/subscriptions/{SUBSCRIPTION_ID}"
        f"/resourceGroups/{RESOURCE_GROUP}"
        f"/providers/Microsoft.Storage/storageAccounts/{STORAGE_ACCOUNT}"
    )
    return f"ResourceId={resource_id};"


# ---------------------------------------------------------------------------
# Step 1 — Create or update the Datasource
# ---------------------------------------------------------------------------

def create_datasource(token: str) -> None:
    """
    Register the blob container as a datasource.

    AI Search will poll this container for new/updated blobs when the
    indexer runs. Using a managed-identity connection keeps it key-free.
    """
    print("[1/3] Creating datasource ...")

    body = {
        "name": DATASOURCE_NAME,
        "type": "azureblob",
        "credentials": {
            "connectionString": build_storage_connection_string(),
        },
        "container": {
            "name": CONTAINER_NAME,
            # index every blob at the top level; no subfolder filter
        },
        "description": "Blob container holding enterprise knowledge base documents",
    }

    search_request("PUT", f"/datasources/{DATASOURCE_NAME}", token, body)
    print(f"  [OK] Datasource '{DATASOURCE_NAME}' created / updated.")


# ---------------------------------------------------------------------------
# Step 2 — Create or update the Index
# ---------------------------------------------------------------------------

def create_index(token: str) -> None:
    """
    Define the searchable schema.

    Fields:
      id            — unique document key  (blob URL, base64-encoded)
      content       — full text of the blob; used for full-text + semantic search
      metadata_storage_name   — original filename (e.g. logic-app-runbook.md)
      metadata_storage_path   — full blob URL (useful for citations)

    The 'content' field uses the standard analyser for full-text search.
    Semantic ranking is configured so Azure OpenAI can do grounded answers
    against the most relevant chunks.
    """
    print("[2/3] Creating index ...")

    body = {
        "name": INDEX_NAME,
        "fields": [
            {
                "name": "id",
                "type": "Edm.String",
                "key": True,
                "searchable": False,
                "filterable": True,
                "retrievable": True,
            },
            {
                "name": "content",
                "type": "Edm.String",
                "key": False,
                "searchable": True,
                "filterable": False,
                "retrievable": True,
                "analyzer": "standard.lucene",
            },
            {
                "name": "metadata_storage_name",
                "type": "Edm.String",
                "key": False,
                "searchable": True,
                "filterable": True,
                "retrievable": True,
            },
            {
                "name": "metadata_storage_path",
                "type": "Edm.String",
                "key": False,
                "searchable": False,
                "filterable": False,
                "retrievable": True,
            },
        ],
        # Semantic search configuration — enables re-ranking + extractive answers
        "semantic": {
            "configurations": [
                {
                    "name": "semantic-config",
                    "prioritizedFields": {
                        "contentFields": [{"fieldName": "content"}],
                        "keywordsFields": [{"fieldName": "metadata_storage_name"}],
                    },
                }
            ]
        },
    }

    search_request("PUT", f"/indexes/{INDEX_NAME}", token, body)
    print(f"  [OK] Index '{INDEX_NAME}' created / updated.")


# ---------------------------------------------------------------------------
# Step 3 — Create or update the Indexer
# ---------------------------------------------------------------------------

def create_indexer(token: str) -> None:
    """
    Create the indexer that crawls the blob datasource and populates the index.

    The built-in 'extractAndTransformContent' skill is used to extract text
    from .md files automatically — no custom skill set needed for plain text.

    Schedule: runs every 5 minutes so new documents appear in the index
    quickly after being uploaded by the ingestion pipeline.
    """
    print("[3/3] Creating indexer ...")

    body = {
        "name": INDEXER_NAME,
        "dataSourceName": DATASOURCE_NAME,
        "targetIndexName": INDEX_NAME,
        "description": "Indexes knowledge base .md files from blob storage",
        "schedule": {
            # PT5M = ISO 8601 for 5 minutes
            "interval": "PT5M",
        },
        "parameters": {
            "configuration": {
                # Parse each blob as a single document (works well for .md files)
                "parsingMode": "default",
                # Skip blobs that fail to parse rather than halting the entire run
                "failOnUnsupportedContentType": False,
            }
        },
        # Map blob metadata fields → index fields
        "fieldMappings": [
            {
                "sourceFieldName": "metadata_storage_path",
                "targetFieldName": "id",
                "mappingFunction": {"name": "base64Encode"},
            },
            {
                "sourceFieldName": "metadata_storage_name",
                "targetFieldName": "metadata_storage_name",
            },
            {
                "sourceFieldName": "metadata_storage_path",
                "targetFieldName": "metadata_storage_path",
            },
        ],
    }

    search_request("PUT", f"/indexers/{INDEXER_NAME}", token, body)
    print(f"  [OK] Indexer '{INDEXER_NAME}' created / updated.")


# ---------------------------------------------------------------------------
# Step 4 — Trigger an immediate indexer run
# ---------------------------------------------------------------------------

def run_indexer(token: str) -> None:
    """
    Kick off an immediate indexer run so documents are indexed right away
    rather than waiting for the next scheduled interval.
    """
    print("[+]  Triggering immediate indexer run ...")
    search_request("POST", f"/indexers/{INDEXER_NAME}/run", token)
    print("  [OK] Indexer run triggered. Documents will appear in the index within ~1 minute.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Enterprise AI Ticket Platform — AI Search Setup")
    print("=" * 60)

    # Validate required environment variables
    missing = [
        v for v in ("AZURE_SEARCH_SERVICE", "AZURE_STORAGE_ACCOUNT",
                    "AZURE_SUBSCRIPTION_ID", "AZURE_RESOURCE_GROUP")
        if not os.environ.get(v)
    ]
    # Fall back to defaults already set above — only abort if SUBSCRIPTION_ID is missing
    if not SUBSCRIPTION_ID:
        print(
            "[ERROR] AZURE_SUBSCRIPTION_ID is required but not set.\n"
            "        Set it as a GitHub secret or export it locally.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        print("\n[AUTH] Obtaining Azure AD token for AI Search ...")
        token = get_token()
        print("  [OK] Token obtained.\n")

        create_datasource(token)
        create_index(token)
        create_indexer(token)
        run_indexer(token)

    except Exception as exc:  # noqa: BLE001
        print(f"\n[ERROR] Setup failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print("\n[DONE] AI Search configuration complete.")
    print(f"       Index:    {INDEX_NAME}")
    print(f"       Indexer:  {INDEXER_NAME} (runs every 5 min, triggered now)")
    print(f"       RAG is ready — connect '{INDEX_NAME}' in Azure AI Foundry.")


if __name__ == "__main__":
    main()
