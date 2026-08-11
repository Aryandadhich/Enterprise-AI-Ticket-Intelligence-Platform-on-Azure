output "resource_group_name" {
  value = module.resource_group.resource_group_name
}

output "storage_account_name" {
  value = module.storage_account.storage_account_name
}

output "key_vault_name" {
  value = module.key_vault.key_vault_name
}

output "openai_account_name" {
  value = module.Azure_openai.openai_account_name
}

output "log_analytics_workspace_name" {
  value = module.log_analytics_workspace.workspace_name
}

output "application_insights_name" {
  value = module.application_insights.application_insights_name
}
