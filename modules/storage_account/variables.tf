variable "storage_account_name" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

# The Azure AD principal_id of the AI Search service's managed identity.
# Used to create the RBAC role assignment that allows Search to read blobs.
variable "search_principal_id" {
  description = "Principal ID of the AI Search managed identity, granted Storage Blob Data Reader."
  type        = string
}