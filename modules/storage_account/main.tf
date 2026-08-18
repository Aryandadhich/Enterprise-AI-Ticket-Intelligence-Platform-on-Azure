resource "azurerm_storage_account" "this" {

  name                     = var.storage_account_name

  resource_group_name      = var.resource_group_name

  location                 = var.location

  account_tier             = "Standard"

  account_replication_type = "LRS"

}

# A container is like a folder inside the storage account.
# All RAG knowledge documents (runbooks, playbooks) go inside here.
# "private" = only authenticated identities can read blobs.
# AI Search already has Storage Blob Data Reader via RBAC, so it can read these.
resource "azurerm_storage_container" "documents" {
  name                  = "documents"
  storage_account_id    = azurerm_storage_account.this.id
  container_access_type = "private"
}