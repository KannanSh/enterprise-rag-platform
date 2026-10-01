terraform {
  required_version = ">= 1.6"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
provider "aws" { region = var.region }
variable "region" { default = "eu-central-1" }
# Foundation only: production should add VPC, private subnets, RDS/pgvector strategy,
# IAM roles, secrets, logging, WAF and EKS/ECS according to enterprise standards.
resource "aws_s3_bucket" "documents" { bucket_prefix = "enterprise-rag-docs-" }
output "document_bucket" { value = aws_s3_bucket.documents.id }
