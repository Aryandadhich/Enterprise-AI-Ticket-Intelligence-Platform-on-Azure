variable "application_insights_name" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "workspace_id" {
  description = "Log Analytics Workspace ID to link Application Insights"
  type        = string
}