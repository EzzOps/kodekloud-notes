# AWS VPC lookup by tag
data "aws_vpc" "prd" {
  filter {
    name   = "tag:Name"
    values = ["prd-vpc"]
  }
}

# Azure resource group lookup
data "azurerm_resource_group" "dev" {
  name = "dev-resource-group"
}

# Kubernetes namespace lookup
data "kubernetes_namespace" "app" {
  metadata {
    name = "customer-app"
  }
}
```

Referencing attributes when creating resources:

```hcl theme={null}
# Use VPC ID to create an AWS subnet
resource "aws_subnet" "pub" {
  vpc_id     = data.aws_vpc.prd.id
  cidr_block = "10.0.6.0/24"
}
```

Best practices and tips

* Use filters or explicit names in data sources to reduce accidental matches.
* Prefer data sources in modules when the module must integrate with already existing infrastructure.
* Be mindful of provider API rate limits: data sources are called during plan and apply.
* If attributes change outside Terraform, re-running `terraform plan` will reflect the new values (depending on provider behavior).

Summary

* Data sources are read-only constructs that let you query existing infrastructure and expose attributes to your Terraform configuration.
* Use data sources to avoid hard-coded IDs and to resolve dependencies on existing resources.
* Each provider documents supported arguments and returned attributes in the Terraform Registry — check it for the exact schema.

Links and references

* Terraform Registry: [https://registry.terraform.io/](https://registry.terraform.io/)
* AWS Provider documentation: [https://registry.terraform.io/providers/hashicorp/aws/latest/docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* AzureRM Provider documentation: [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* Kubernetes Provider documentation: [https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs)

You'll practice using data sources in hands-on exercises to gain practical experience working with real-world Terraform configurations.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/e58a8612-ffdb-41a2-87ab-3055990d7c3b)


# Using Multiple Providers in Your Configuration

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Configuration-Fundamentals/Using-Multiple-Providers-in-Your-Configuration/page

Explains using multiple Terraform provider blocks and aliases to manage resources across different accounts or regions and select specific provider configurations per resource.

In this lesson we'll cover the Terraform `provider` meta-argument and how to configure multiple provider instances within a single configuration. For reference, see the official provider meta-argument docs: [https://developer.hashicorp.com/terraform/language/meta-arguments/provider](https://developer.hashicorp.com/terraform/language/meta-arguments/provider).

A provider block tells Terraform how to authenticate and interact with a target platform (for example, AWS, Azure, GitHub, Vault). When managing resources across different accounts, regions, or platform settings, you can declare more than one provider block of the same provider type. Add an `alias` to additional provider blocks to create named configurations, and then select the desired configuration inside a resource using the `provider` meta-argument.

Why this matters:

* Provides precise control over where each resource is created.
* Enables multi-account and multi-region deployments from a single Terraform configuration.
* Facilitates using different credentials, roles, or regions for specific resources.

## How it works — step by step

1. Define one or more `provider` blocks. Any provider block without an `alias` is the default configuration and is used by resources that do not explicitly set a provider.
2. Add `alias = "<name>"` to create additional named configurations.
3. In a resource block, set `provider = <provider_name>.<alias>` to target a specific provider configuration.

Example rules:

* If at least one provider block has no `alias`, it becomes the default. Resources without an explicit `provider` will use that default.
* If all provider blocks are aliased (no default), every resource must explicitly set the `provider` meta-argument.

## Quick example

* The first provider block below is the default AWS provider (used by resources that do not specify a provider).
* The second provider block is an aliased configuration named `prod` for a different region (or different credentials).

```hcl theme={null}
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "prod"
  region = "us-west-1"
}

resource "aws_s3_bucket" "dev_bucket" {
  bucket = "my-dev-bucket"
}

resource "aws_s3_bucket" "prod_bucket" {
  provider = aws.prod
  bucket   = "my-prod-bucket"
}
```

Explanation:

* `provider "aws" { region = "us-east-1" }` — default provider configuration. `aws_s3_bucket.dev_bucket` will be created using this configuration.
* `provider "aws" { alias = "prod" region = "us-west-1" }` — named provider configuration `aws.prod`, which can point to a different region or use different credentials/role.
* `resource "aws_s3_bucket" "prod_bucket" { provider = aws.prod ... }` — creates `prod_bucket` using the aliased `aws.prod` provider (so it will be created in `us-west-1`).

## Common scenarios and examples

| Scenario                            | Use case                                                      | Example                                                                                                |
| ----------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Separate accounts                   | Deploy dev vs production into different AWS accounts          | Use different credentials for `provider "aws"` blocks and alias the production provider                |
| Multiple regions                    | Create resources in `us-east-1` and `us-west-1`               | `provider "aws" { region = "us-east-1" }` and `provider "aws" { alias = "west" region = "us-west-1" }` |
| Assume role / different credentials | Use different IAM roles or API tokens for different resources | Configure `assume_role` or credentials per provider block and reference via alias                      |
| Cross-region replication            | Source S3 bucket in one region and destination in another     | Create two `aws_s3_bucket` resources each using the appropriate provider configuration                 |

## Best practices

* Keep provider configuration and credentials secure (environment variables, shared credentials file, or Terraform Cloud variables).
* Use clear alias names (for example, `prod`, `staging`, `europe`) to make intent obvious.
* Minimize mixing too many provider instances in a single file; group related resources into modules when appropriate.
* When all provider blocks are aliased, the configuration requires explicit `provider` assignments for every resource — consider adding a sensible default to reduce repetition.

> **lightbulb** If you define only aliased provider blocks (i.e., every provider block has an `alias`), then no default provider exists and every resource must explicitly set the `provider` meta-argument. Conversely, if you leave at least one provider block without an alias, that block becomes the default and resources without an explicit `provider` will use it.

> **warning** Be careful with credentials and roles: each provider block can have its own authentication settings. Ensure the credentials or role configured for an alias have the required permissions for the resources you intend to create in that account/region.

## Use cases (expanded)

* Cross-region replication: create a source [S3 bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) in one region and a destination bucket in another, then configure replication.
* Multi-account deployments: assign different credentials to each provider block (via environment variables, credentials blocks, or `assume_role`) and use aliases to deploy resources into the intended account.
* Mixed environments: deploy some resources to a default/dev account and others to production without splitting into multiple Terraform configurations—use aliases and the `provider` meta-argument to control placement.

## Links and references

* [Terraform: Provider meta-argument](https://developer.hashicorp.com/terraform/language/meta-arguments/provider)
* [Terraform Docs](https://developer.hashicorp.com/terraform)
* [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* [S3 Bucket Resource (AWS)](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)

That's the core idea behind the provider meta-argument: it allows precise selection of which provider configuration Terraform uses per resource, enabling flexible multi-account, multi-region, and multi-cloud workflows.

Let's proceed to a quick demo.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/d67e8dc8-0136-4296-966d-229a1d9f46bc/lesson/13270bea-4051-436b-be54-73ac08a0ebc0)
