terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  # Uses AWS CLI configuration (aws configure)
}

provider "aws" {
  alias  = "eu-central-1"
  region = "eu-central-1"
}