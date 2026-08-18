resource "azurerm_search_service" "this" {
  name                = var.search_service_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku

  # A SystemAssigned identity gives this Search service its own Azure AD identity.
  # This is how the Search Indexer will authenticate to Blob Storage — no secrets, no keys.
  identity {
    type = "SystemAssigned"
  }
}