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
  region  = var.region

  default_tags {
    tags = {
    terraform = "true"
    env       = var.app_env
    app       = var.app_name
    }
  }
}

locals {
  region = "us-east-1"
  prefix = "${var.app_name}-${var.app_env}"
}
