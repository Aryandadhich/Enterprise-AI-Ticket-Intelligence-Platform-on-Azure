#Define what values are needed

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
}

variable "location" {
  description = "Azure Region where resources will be deployed"
  type        = string
}

variable "storage_account_name"{
  type = string
}