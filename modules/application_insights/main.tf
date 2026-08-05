resource "azurerm_application_insight" "this" {
    name = var.application_insights_name
    location = var.location
    resource_group_name = var.resource_group_name
    application_type = "web"

}