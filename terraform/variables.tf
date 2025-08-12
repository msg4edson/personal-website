variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket for hosting the website"
  type        = string
  default     = "edson-personal-website"
}

variable "domain_name" {
  description = "Domain name for the website (leave empty to use CloudFront domain)"
  type        = string
  default     = ""
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "Personal Website"
    Owner       = "Edson da Silva"
    Environment = "production"
  }
}
