#Define what values are needed

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
}

variable "location" {
  description = "Azure Region where resources will be deployed"
  type        = string
}

variable "storage_account_name" {
  type = string
}

variable "key_vault_name" {
  type = string
}

variable "openai_account_name" {
  type = string
}

variable "openai_location" {
  type = string
}

variable "workspace_name" {
  description = "Name of the Log Analytics Workspace"
  type        = string
}

variable "application_insights_name" {
  description = "Name of the Application Insights instance"
  type        = string
}

# If a variable is not declared here, Terraform will throw an error because
# the root module won't know about it.