# Type "yes" to confirm
```

Verify the new VPC in the AWS Console.

***

## 6. Deploy EC2 Web Module with VPC Dependency

Create `Terraform stack/ec2-web/terragrunt.hcl` and reference the VPC outputs:

<Frame>
  ![The image shows a split-screen view of a coding environment. On the left, there's a task description about setting dependencies for an EC2 web module, and on the right, there's a code editor displaying Terraform configuration files.](https://kodekloud.com/kk-media/image/upload/v1752884301/notes-assets/images/Terragrunt-for-Beginners-Demo-of-Lab-3/ec2-web-module-terraform-coding-view.jpg)
</Frame>

```hcl theme={null}
terraform {
  source = "terraform-aws-modules/ec2-instance/aws//?version=2.0.0"
}

include "root" {
  path   = find_in_parent_folders()
  expose = true
}

dependency "vpc" {
  config_path = "../../vpc"
}

inputs = {
  name          = include.root.locals.project
  ami           = include.root.locals.ami
  instance_type = include.root.locals.instance_type
  subnet_id     = dependency.vpc.outputs.public_subnets[0]
}
```

Initialize and apply:

```bash theme={null}
cd "Terraform stack/ec2-web"
terragrunt init
terragrunt apply
# Type "yes" to confirm
```

***

## 7. Add Database Dependency to the Web Module

If you have a database module under `Terraform stack/ec2-database`, ensure it deploys before the web server:

```hcl theme={null}
dependencies {
  paths = ["../ec2-database"]
}
```

Re-run in `ec2-web`:

```bash theme={null}
terragrunt init
terragrunt apply
```

Terragrunt will sequence: VPC → Database → Web.

***

## 8. Deploy All Modules Simultaneously

From the root of `Terraform stack`, run:

```bash theme={null}
terragrunt run-all apply
```

This command orchestrates every module in dependency order.

***

## 9. Verify Remote State Files in S3

Check that each module has its own state file:

```bash theme={null}
BUCKET=$(aws s3 ls | grep kk-tf-state | awk '{print $3}' | head -n1)
aws s3 ls "s3://$BUCKET" --recursive
```

Expected output:

```bash theme={null}
2024-06-23 09:14:06   180 0/terraform.tfstate
2024-06-23 09:14:06  9575 0/database/terraform.tfstate
2024-06-23 09:14:09 39803 0/web/terraform.tfstate
```

***

## 10. Why Generate at the Root

By generating the backend, provider, and Terraform-version files at the project root, you:

* Centralize configuration for consistency
* Avoid duplication in child modules
* Simplify maintenance as your infrastructure grows

***

Thank you for completing Lab Three! You now have a reusable Terragrunt setup for AWS VPC, EC2, and remote state management. See you in the next lab!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/bab279d4-de1d-4e8d-8376-ea420c71c9e1/lesson/afc1e84c-ca3e-4ad0-a1b0-344073719a34" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/bab279d4-de1d-4e8d-8376-ea420c71c9e1/lesson/22d3770d-f36b-47c7-bd42-f0a0c8e76214" />
</CardGroup>


# Terragrunt Blocks Overview

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Blocks/Terragrunt-Blocks-Overview/page

This article provides an overview of the seven core Terragrunt configuration blocks for enhancing Terraform workflows.

In this lesson, we’ll dive into the seven core Terragrunt configuration blocks that power your Terraform workflows. Whether you’re already familiar with Terraform or new to Terragrunt’s advanced features, you’ll learn how each block streamlines state management, dependency handling, and DRY (Don’t Repeat Yourself) principles for infrastructure as code.

<Callout icon="lightbulb">
  Terragrunt extends Terraform by adding useful wrappers around remote state, dependencies, and configuration generation. If you’re new to Terragrunt, check out the [official Terragrunt documentation](https://terragrunt.gruntwork.io/).
</Callout>

## Summary of Terragrunt Blocks

| Block         | Purpose                                                                | Key Benefit                            |
| ------------- | ---------------------------------------------------------------------- | -------------------------------------- |
| terraform     | Pass extra arguments directly to the Terraform CLI.                    | Fine-tune your Terraform runs.         |
| remote\_state | Configure reading from and writing to remote state backends.           | Centralize and secure state storage.   |
| include       | Import and merge settings from another Terragrunt config file.         | Share common configurations.           |
| locals        | Define reusable values and expressions.                                | Keep code DRY and maintainable.        |
| dependency    | Declare a single dependency on another Terragrunt module.              | Expose outputs from one module.        |
| dependencies  | List multiple module dependencies for orchestration.                   | Orchestrate complex multi-module runs. |
| generate      | Auto-generate additional HCL or JSON files before Terraform execution. | Automate boilerplate file creation.    |

## 1. terraform Block

Use the `terraform` block to pass custom flags and settings to the Terraform CLI:

```hcl theme={null}
terraform {
  extra_arguments "plan_args" {
    commands = ["plan"]
    arguments = ["-var-file=prod.tfvars", "-parallelism=10"]
  }
}
```

## 2. remote\_state Block

Configure your remote backend once in Terragrunt to avoid repeating it in every module:

```hcl theme={null}
remote_state {
  backend = "s3"
  config = {
    bucket         = "my-terraform-states"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

<Callout icon="triangle-alert">
  Always enable state locking (e.g., DynamoDB for S3 backends) to prevent concurrent state modifications.
</Callout>

## 3. include Block

Share common settings by importing another Terragrunt file:

```hcl theme={null}
include {
  path = find_in_parent_folders("terragrunt.hcl")
}
```

## 4. locals Block

Define and reuse variables and expressions:

```hcl theme={null}
locals {
  environment = "production"
  tags = {
    Project = "website"
    Env     = local.environment
  }
}
```

## 5. dependency Block

Declare a single dependency to retrieve outputs from another module:

```hcl theme={null}
dependency "vpc" {
  config_path = "../vpc"
}
