#Azure calls OpenAI under Azure AI Services (Cognitive Services).

resource "azurerm_cognitive_account" "this" {
    name = var.openai_account_name
    location = var.location
    resource_group_name = var.resource_group_name
    kind = "OpenAI"
    sku_name = "S0"  #just like vm have diffrent size Az openai have pricing tiers (sku) s0 is standard sku commonly used.

}