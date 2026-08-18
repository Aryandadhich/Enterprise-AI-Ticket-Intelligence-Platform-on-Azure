output "search_service_name" {
  value = azurerm_search_service.this.name
}

output "search_service_id" {
  value = azurerm_search_service.this.id
}

# The principal_id is the Azure AD object ID of the Search service's managed identity.
# The root module needs this to create the RBAC role assignment on the Storage Account.
# Without this output, the root module cannot see the identity and the grant cannot be made.
output "search_principal_id" {
  value = azurerm_search_service.this.identity[0].principal_id
}