resource "azurerm_search_service" "this" {
  name                = var.search_service_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku

  # SystemAssigned identity gives this Search service its own Azure AD identity.
  # The Search Indexer uses this identity to authenticate to Blob Storage — no secrets needed.
  identity {
    type = "SystemAssigned"
  }
}