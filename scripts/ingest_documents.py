"""
ingest_documents.py
-------------------
Production ingestion script for the Enterprise AI Ticket Intelligence Platform.

Purpose:
    Reads all markdown (.md) files from the Knowledge/ directory and uploads
    them to the Azure Blob Storage 'documents' container.

Authentication:
    Uses DefaultAzureCredential — no passwords or keys in code.

    Locally:   uses your 'az login' session.

    In CI/CD:  uses GitHub Actions OIDC (Workload Identity Federation).
               GitHub requests a short-lived token from Azure AD at runtime.
               No secret is ever stored — the token expires in ~10 minutes.
               Required env vars (injected by the workflow, not secrets):
                 AZURE_CLIENT_ID      - App registration client ID
                 AZURE_TENANT_ID      - Azure AD tenant ID
                 AZURE_FEDERATED_TOKEN_FILE - auto-set by azure/login OIDC action

Usage:
    python scripts/ingest_documents.py

Environment variables:
    AZURE_STORAGE_ACCOUNT   - Name of the Azure Storage Account (GitHub Secret)
    AZURE_CLIENT_ID         - App registration client ID   (GitHub Variable)
    AZURE_TENANT_ID         - Azure AD tenant ID           (GitHub Variable)
"""

import os
import sys
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# ---------------------------------------------------------------------------
# Configuration — read from environment variables (no hardcoded values)
# ---------------------------------------------------------------------------
STORAGE_ACCOUNT_NAME = os.environ.get("AZURE_STORAGE_ACCOUNT", "aiticketstorage12")
CONTAINER_NAME = "documents"

# Knowledge folder is always relative to the repo root, regardless of where
# the script is run from.
REPO_ROOT = Path(__file__).parent.parent
KNOWLEDGE_DIR = REPO_ROOT / "Knowledge"


def get_blob_service_client() -> BlobServiceClient:
    """
    Build a BlobServiceClient using DefaultAzureCredential.

    DefaultAzureCredential tries these in order:
      1. Environment variables (AZURE_CLIENT_ID / TENANT_ID / CLIENT_SECRET)
         → used by GitHub Actions service principal
      2. Workload Identity (AKS)
      3. Managed Identity (Azure-hosted compute)
      4. Azure CLI session (local development with 'az login')
      5. Visual Studio Code / Azure PowerShell session

    This means the SAME script works locally AND in CI/CD with zero changes.
    """
    credential = DefaultAzureCredential()
    account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    return BlobServiceClient(account_url=account_url, credential=credential)


def upload_documents(client: BlobServiceClient) -> tuple[int, int]:
    """
    Upload all .md files from Knowledge/ to the blob container.

    Returns:
        (uploaded_count, skipped_count)
    """
    container_client = client.get_container_client(CONTAINER_NAME)

    uploaded = 0
    skipped = 0

    md_files = sorted(KNOWLEDGE_DIR.glob("*.md"))

    if not md_files:
        print(f"[WARN] No .md files found in {KNOWLEDGE_DIR}")
        return 0, 0

    print(f"[INFO] Found {len(md_files)} document(s) in {KNOWLEDGE_DIR}")
    print(f"[INFO] Target: {STORAGE_ACCOUNT_NAME}/{CONTAINER_NAME}\n")

    for file_path in md_files:
        blob_name = file_path.name  # e.g. "logic-app-authentication-runbook.md"

        try:
            with open(file_path, "rb") as data:
                container_client.upload_blob(
                    name=blob_name,
                    data=data,
                    overwrite=True,  # idempotent — safe to re-run anytime
                    content_settings=None,
                )
            print(f"  [OK] Uploaded: {blob_name}")
            uploaded += 1

        except Exception as exc:  # noqa: BLE001
            print(f"  [FAIL] {blob_name}: {exc}", file=sys.stderr)
            skipped += 1

    return uploaded, skipped


def main() -> None:
    print("=" * 60)
    print("  Enterprise AI Ticket Platform — Document Ingestion")
    print("=" * 60)

    if not KNOWLEDGE_DIR.exists():
        print(f"[ERROR] Knowledge directory not found: {KNOWLEDGE_DIR}", file=sys.stderr)
        sys.exit(1)

    try:
        client = get_blob_service_client()
        uploaded, skipped = upload_documents(client)
    except Exception as exc:  # noqa: BLE001
        print(f"\n[ERROR] Ingestion failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\n[DONE] Uploaded: {uploaded} | Failed: {skipped}")

    if skipped > 0:
        sys.exit(1)  # non-zero exit → CI/CD pipeline will mark the run as failed


if __name__ == "__main__":
    main()
