# Demo of Lab 5

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Managing-Remote-State-with-Terragrunt/Demo-of-Lab-5/page

This lab teaches configuring a remote state backend and AWS provider using Terragrunt to manage infrastructure in AWS.

In this lab, you’ll learn how to configure a remote state backend and set up the AWS provider using Terragrunt. We’ll generate Terraform configuration files automatically and initialize your stack to manage infrastructure in AWS.

Before you begin, ensure you have AWS credentials configured:

```bash theme={null}
show-creds
```

You can run commands in VS Code’s integrated terminal via your browser for easy copy & paste.

***

## 1. Verify Your Terraform Version

First, confirm the Terraform CLI version installed on your system:

```bash theme={null}
terraform version
```

You should see output similar to:

```bash theme={null}
Terraform v1.8.3
```

***

## 2. Auto-Generate AWS Provider Files with Terragrunt

All Terragrunt configuration lives under your Terraform stack directory (`terraform-stack/terragrunt.hcl`). We’ll generate three files:

| Filename       | Purpose                                    | Key Settings              |
| -------------- | ------------------------------------------ | ------------------------- |
| `providers.tf` | Declares the AWS provider and region       | `region = "us-east-1"`    |
| `versions.tf`  | Pins the AWS provider version              | `version = "~> 5.0"`      |
| `backend.tf`   | Configures remote state with an S3 backend | bucket, key, region, lock |

### 2.1 Generate `providers.tf`

Add this block to `terragrunt.hcl` to configure AWS in `us-east-1`:

```hcl theme={null}
generate "provider" {
  path      = "providers.tf"
  if_exists = "overwrite"
  contents  = <<EOF
provider "aws" {
  region = "us-east-1"
}
EOF
}
```

### 2.2 Generate `versions.tf`

Next, pin to the latest major AWS provider release:

```hcl theme={null}
generate "provider_version" {
  path      = "versions.tf"
  if_exists = "overwrite"
  contents  = <<EOF
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
EOF
}
```

> **lightbulb** Ensure your `terragrunt.hcl` includes these `generate` blocks before initializing.

***

## 3. Initialize Terragrunt

Switch into your Terraform stack directory and run initialization:

```bash theme={null}
cd terraform-stack
terragrunt init
```

On success, you should see `providers.tf` and `versions.tf` created automatically.

***

## 4. Configure Remote State in S3

An S3 bucket named `kk-infra-state-<random>` already exists for your Terraform state. Discover its exact name:

```bash theme={null}
aws s3 ls | grep kk-infra-state
```

Copy the bucket name and update your root `terragrunt.hcl` with this block to generate `backend.tf`:

```hcl theme={null}
generate "remote_state" {
  path      = "backend.tf"
  if_exists = "overwrite"
  contents  = <<EOF
remote_state {
  backend = "s3"
  config = {
    encrypt        = true
    bucket         = "kk-infra-state-<random>"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform box"
  }
}
EOF
}
```

> **triangle-alert** Never commit your AWS access keys or state files to version control.

***

## 5. Reinitialize & Apply Your Stack

Apply the new backend settings and spin up resources:

```bash theme={null}
terragrunt init
