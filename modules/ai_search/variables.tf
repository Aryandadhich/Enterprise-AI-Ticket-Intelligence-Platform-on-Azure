variable "search_service_name" {
  description = "The name of the Azure AI Search service."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group in which to create the search service."
  type        = string
}

variable "location" {
  description = "The Azure region where the search service will be created."
  type        = string
}

variable "sku" {
  description = "The SKU of the Azure AI Search service (e.g. free, basic, standard)."
  type        = string
  # "basic" does NOT support vector search (HNSW indexes).
  # "standard" is the minimum SKU required for vector/semantic RAG retrieval.
  default     = "standard"
}
