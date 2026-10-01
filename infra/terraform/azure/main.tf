terraform {
  required_version = ">= 1.6"
  required_providers { azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" } }
}
provider "azurerm" { features {} }
variable "location" { default = "West Europe" }
resource "azurerm_resource_group" "rag" { name = "rg-enterprise-rag" location = var.location }
output "resource_group" { value = azurerm_resource_group.rag.name }
# Foundation only: production should add VNet, managed PostgreSQL/pgvector,
# managed identity, Key Vault, monitoring and Azure Container Apps/AKS as required.
