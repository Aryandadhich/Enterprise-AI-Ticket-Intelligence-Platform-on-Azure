output "storage_account_name" {
  value = azurerm_storage_account.this.name
}

output "storage_account_id" {
  value = azurerm_storage_account.this.id
}

# Expose container name so root module and future indexer config can reference it.
output "documents_container_name" {
  value = azurerm_storage_container.documents.name
}