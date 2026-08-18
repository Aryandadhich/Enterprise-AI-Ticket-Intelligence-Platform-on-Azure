module "resource_group" {
  source              = "./modules/resource_group"
  resource_group_name = var.resource_group_name
  location            = var.location
}

module "storage_account" {
  source               = "./modules/storage_account"
  storage_account_name = var.storage_account_name
  resource_group_name  = module.resource_group.resource_group_name
  location             = var.location
}

module "key_vault" {
  source              = "./modules/key_vault"
  key_vault_name      = var.key_vault_name
  resource_group_name = module.resource_group.resource_group_name
  location            = var.location
}

module "Azure_openai" {
  source              = "./modules/Azure_openai"
  resource_group_name = module.resource_group.resource_group_name
  openai_account_name = var.openai_account_name
  location            = var.openai_location
}

module "log_analytics_workspace" {
  source              = "./modules/log_analytics_workspace"
  workspace_name      = var.workspace_name
  resource_group_name = module.resource_group.resource_group_name
  location            = var.location
}

module "application_insights" {
  source                    = "./modules/application_insights"
  application_insights_name = var.application_insights_name
  resource_group_name       = module.resource_group.resource_group_name
  location                  = var.location
  workspace_id              = module.log_analytics_workspace.workspace_id
}

module "ai_search" {
  source              = "./modules/ai_search"
  search_service_name = var.search_service_name
  resource_group_name = module.resource_group.resource_group_name
  location            = var.location
}

# RBAC grant: Allow the AI Search managed identity to read blobs from the Storage Account.
# Placed at root level (not inside a module) so Terraform can correctly defer this resource
# until AFTER both the Search service (for principal_id) and Storage Account (for scope/id)
# have been created. Inside a child module, computed values from sibling modules are not
# available at plan time and cause "required argument missing" errors.
# scope       = WHERE: the storage account resource ID
# role        = WHAT:  Storage Blob Data Reader (read-only on blobs — exactly what the indexer needs)
# principal   = WHO:   the Search service's Azure AD managed identity
resource "azurerm_role_assignment" "search_blob_reader" {
  scope                = module.storage_account.storage_account_id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = module.ai_search.search_principal_id
}

