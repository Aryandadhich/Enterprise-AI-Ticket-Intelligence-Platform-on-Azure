resource "azurerm_storage_account" "this" {

  name                     = var.storage_account_name

  resource_group_name      = var.resource_group_name

  location                 = var.location

  account_tier             = "Standard"

  account_replication_type = "LRS"

}

# Grant the AI Search service's managed identity read access to blobs in this storage account.
# scope       = WHERE the permission applies (this storage account's resource ID)
# role        = WHAT it can do (Storage Blob Data Reader = read blobs, nothing else)
# principal   = WHO gets the permission (the Search service's Azure AD identity)
# This is the zero-secret approach: no connection strings, no account keys stored anywhere.
resource "azurerm_role_assignment" "search_blob_reader" {
  scope                = azurerm_storage_account.this.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = var.search_principal_id
}