output "search_service_name" {
  value = azurerm_search_service.this.name
}

output "search_service_id" {
  value = azurerm_search_service.this.id
}

# Exposes the Azure AD object ID of the Search service's managed identity.
# Root main.tf uses this to create the RBAC role assignment on the Storage Account.
output "search_principal_id" {
  value = azurerm_search_service.this.identity[0].principal_id
}