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

##if we didnt diclare this in varibale then terraform throw a eror because the root module is trying to use 
# a variable it doesn't know about