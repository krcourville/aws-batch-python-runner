terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  required_version = ">= 1.1.5"
}

provider "aws" {
  profile = "default"
  region  = local.region
}

locals {
  region = "us-east-1"
}
