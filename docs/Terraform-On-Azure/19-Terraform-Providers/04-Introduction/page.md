# Azure Provider
provider "azurerm" {
  features {}
}

# AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Local Provider (used for creating local files)
provider "local" {}
```

Provider publication and trust model

* Providers are typically published to the Terraform Registry and are organized by publisher/namespace.
* Providers fall into three common tiers: Official (HashiCorp-maintained), Verified/Partner (vendor-validated), and Community (third-party).

| Provider Tier      | Description                                                                                   | Examples                                                 |
| ------------------ | --------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Official           | Maintained by HashiCorp; generally recommended for production                                 | `hashicorp/azurerm`, `hashicorp/aws`, `hashicorp/google` |
| Verified / Partner | Vendor-supported and validated by HashiCorp; good balance of support and feature coverage     | `microsoft/azapi` (example partner provider)             |
| Community          | Community-maintained providers; useful for niche use cases but evaluate before production use | Various independent authors                              |

<Frame>
  <img alt="The image categorizes various providers into three groups: Official, Verified, and Community, each containing different cloud and software services." />
</Frame>

What happens during terraform init

1. Initialize the configured backend.
2. Discover required providers referenced in configuration.
3. Query the Registry for provider metadata (namespace, available versions).
4. Download and install provider binaries into the project directory.

Example terraform init output (first run):

```bash theme={null}
$ terraform init
Initializing the backend...
Initializing provider plugins...
- Finding latest version of hashicorp/azurerm...
- Finding latest version of hashicorp/aws...
- Finding latest version of hashicorp/local...
- Installing hashicorp/azurerm v4.28.0...
- Installed hashicorp/azurerm v4.28.0 (signed by HashiCorp)
- Installing hashicorp/aws v5.97.0...
- Installed hashicorp/aws v5.97.0 (signed by HashiCorp)
- Installing hashicorp/local v2.5.2...
- Installed hashicorp/local v2.5.2 (signed by HashiCorp)

Terraform has created a lock file: terraform.lock.hcl to record the provider selections it made above. Include this file in your version control repository so that Terraform can guarantee to make the same selections by default when you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see any changes that are required for your infrastructure.
```

Provider binaries and workspace layout

* Provider plugins are stored inside your project under the `.terraform` directory (they are not installed globally). Example listing:

```bash theme={null}
$ ls -lah .terraform/providers/registry.terraform.io/hashicorp/
total 20K
drwxr-xr-x  5 rithin rithin 4.0K May 12 02:31 .
drwxr-xr-x  3 rithin rithin 4.0K May 12 02:31 ..
drwxr-xr-x  3 rithin rithin 4.0K May 12 02:31 aws
drwxr-xr-x  3 rithin rithin 4.0K May 12 02:31 azurerm
drwxr-xr-x  3 rithin rithin 4.0K May 12 02:31 local
```

* Provider IDs use a namespace/type pattern such as `hashicorp/azurerm`. The provider type (for example `azurerm`, `aws`, `local`) is what you reference when declaring resources (e.g., `azurerm_virtual_network`, `aws_s3_bucket`).

Provider versioning and lock files

* Providers are versioned. By default, Terraform will choose the latest compatible version; however, pinning or constraining provider versions is best practice for stability.
* terraform init creates a `terraform.lock.hcl` that records the exact provider download selections. When this file exists in the project, subsequent `terraform init` runs will prefer those locked versions and reuse already-installed binaries.

Example init output when reusing locked provider versions:

```bash theme={null}
$ terraform init
Initializing the backend...
Initializing provider plugins...
- Reusing previous version of hashicorp/azurerm from the dependency lock file
- Reusing previous version of hashicorp/aws from the dependency lock file
- Reusing previous version of hashicorp/local from the dependency lock file
- Using previously-installed hashicorp/azurerm v4.28.0
- Using previously-installed hashicorp/aws v5.97.0
- Using previously-installed hashicorp/local v2.5.2

Terraform has been successfully initialized!
```

<Callout icon="lightbulb">
  Include `terraform.lock.hcl` in version control. The lock file ensures everyone (local developers and CI) uses the exact same provider versions for reproducible, deterministic runs.
</Callout>

When to re-run terraform init

* Run `terraform init` any time you change provider configuration, add a new provider, or modify provider version constraints.
* CI pipelines should run `terraform init` at the start of each job so the correct backend and provider plugins are installed.

Exploring providers on the Terraform Registry

* The Terraform Registry is the authoritative place to browse providers, view version history, filter by tier (official, verified, community), and inspect usage examples and source links.

<Frame>
  <img alt="The image shows the Terraform Registry website, featuring options to browse providers, modules, policy libraries, and run tasks against a purple background. A section about the Terraform MCP Server is also visible below." />
</Frame>

You can filter providers by tier and category on the Registry. Official providers (HashiCorp) include AWS, Azure, and Google Cloud; partner/verified providers are vendor-maintained and validated; community providers are contributed by independent maintainers.

<Frame>
  <img alt="The image is a screenshot of the Terraform registry, displaying various cloud providers like AWS, Azure, Google Cloud Platform, and more, with filters for tier and category on the left panel." />
</Frame>

Provider pages include version history, release notes, download stats, and usage instructions. For example, the azurerm provider page shows recent releases and how to pin your configuration:

<Frame>
  <img alt="The image shows a webpage from the HashiCorp Terraform Registry, specifically for the &#x22;azurerm&#x22; provider, which manages Microsoft Azure resources. It displays version information and download statistics for the provider." />
</Frame>

Pinning a provider source and version
To ensure Terraform pulls the provider from the intended source and respects a version constraint, add a `terraform` block with `required_providers` and then configure the provider. Example:

```hcl theme={null}
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.58.0"
    }
  }
}

provider "azurerm" {
  # Configuration options
}
```

This pattern guarantees your team and CI use the same provider source and version. In the next lesson we'll cover version constraints and provider upgrade strategies in more depth.

Links and references

* Terraform Registry — [https://registry.terraform.io/](https://registry.terraform.io/)
* Terraform CLI documentation — [https://www.terraform.io/docs/cli/index.html](https://www.terraform.io/docs/cli/index.html)
* Managing providers and modules — [https://www.terraform.io/docs/language/providers/index.html](https://www.terraform.io/docs/language/providers/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/eeac3f53-157e-493c-a726-7e5d9190c4c3/lesson/fc69f181-2bca-4316-bb35-25e8976111d0" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Providers/Introduction/page

Explains Terraform providers, discovery and configuration, versioning best practices, choosing between AzureRM and AzAPI providers, and using provider aliases for multiple Azure subscriptions or tenants

Terraform providers

In this lesson we’ll walk through Terraform providers: what they are, how Terraform discovers and configures them, best practices for versioning, and how to choose between the two primary Azure providers — AzureRM (`azurerm`) and AzAPI (`azapi`). You’ll also learn how to handle multiple Azure subscriptions or tenants using provider aliases.

Here's what we will cover:

* What Terraform providers are and how Terraform uses them to interact with external platforms.
* How to declare `required_providers` and apply safe version constraints.
* A comparison of the AzureRM (`azurerm`) and AzAPI (`azapi`) providers and when to use each.
* How to handle multiple subscriptions/tenants with provider aliases.

<Frame>
  <img alt="The image shows an agenda with two points: understanding Terraform providers and configuring required providers with version constraints. It has a gradient blue background with numbered markers for each agenda point." />
</Frame>

Consistent provider configuration and versioning are critical for predictable behavior in teams and CI pipelines. We’ll start with the fundamentals: what a provider is and how Terraform finds and configures them.

## What is a Terraform provider?

A provider is a plugin that implements resources and data sources for a target platform. Providers translate HCL into API calls (CRUD operations) against cloud platforms, SaaS services, or HTTP APIs.

Common examples:

* `hashicorp/aws` — AWS
* `hashicorp/azurerm` — Azure Resource Manager
* `azure/azapi` — Direct Azure REST API interactions

Key points:

* Providers are downloaded by `terraform init` from the Terraform Registry or other configured sources.
* Each provider exposes resource types and data sources you reference in HCL.
* You declare provider requirements in the `terraform` block (`required_providers`) and configure provider instances with `provider` blocks.

## How Terraform discovers and configures providers

Use the `terraform` block to declare provider sources and version constraints. Example:

```hcl theme={null}
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    azapi = {
      source  = "azure/azapi"
      version = "~> 1.0"
    }
  }
}
```

Notes:

* `source` points to the namespace/provider on the registry (or to a custom hostname).
* `version` constrains which provider versions Terraform will install.

When you run `terraform init`, Terraform resolves and downloads the provider binaries and records checksums and versions in `.terraform.lock.hcl`.

### Version constraints and best practices

Common constraint styles:

* Exact: `= 3.45.0`
* Tilde (pessimistic): `~> 3.0` — allows `>= 3.0.0` and `< 4.0.0`

Best practices:

* Pin provider major versions (e.g., `~> 3.0`) to avoid surprises from breaking changes.
* Commit `.terraform.lock.hcl` to version control to guarantee consistent provider installs across machines and CI.
* Upgrade providers intentionally: update constraints, run `terraform init -upgrade`, and test in non-production environments first.

<Callout icon="lightbulb">
  Always commit `.terraform.lock.hcl` and pin provider versions to ensure reproducible provider installs across developer machines and CI.
</Callout>

## Provider configuration and aliases

Provider instances are configured with `provider` blocks. For `azurerm`, you typically include an (often-empty) `features` block:

```hcl theme={null}
provider "azurerm" {
  features = {}
}
```

To manage multiple subscriptions, tenants, or separate credential sets in one configuration, use provider aliases:

```hcl theme={null}
provider "azurerm" {
  alias           = "prod"
  features        = {}
  subscription_id = "00000000-0000-0000-0000-000000000000"
  tenant_id       = "11111111-1111-1111-1111-111111111111"
}

provider "azurerm" {
  alias           = "dev"
  features        = {}
  subscription_id = "22222222-2222-2222-2222-222222222222"
  tenant_id       = "33333333-3333-3333-3333-333333333333"
}
```

Reference an aliased provider on resources using the `provider` meta-argument:

```hcl theme={null}
resource "azurerm_resource_group" "prod_rg" {
  provider = azurerm.prod
  name     = "rg-prod"
  location = "eastus"
}

resource "azurerm_resource_group" "dev_rg" {
  provider = azurerm.dev
  name     = "rg-dev"
  location = "eastus"
}
```

Passing providers into modules:

```hcl theme={null}
module "network" {
  source = "./modules/network"

  providers = {
    azurerm = azurerm.prod
  }

  # module inputs...
}
```

## AzureRM vs AzAPI: when to use each

Use the table below for a quick comparison and guidance.

| Provider            | Primary purpose                                                  | When to use                                                            | Example strengths                                                       |
| ------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `azurerm` (AzureRM) | Terraform-native provider for Azure Resource Manager             | Stable, GA resources with full Terraform schema                        | Rich resource schema, better ergonomics, cross-resource integrations    |
| `azapi` (AzAPI)     | Low-level Azure REST API access via a generic resource primitive | Preview/new resource types, unsupported ARM types, custom ARM payloads | Direct ARM API access, supports raw JSON/ARM templates and preview APIs |

Examples:

* AzureRM (preferred when resource is supported and stable):
  * Use `azurerm` for most production workloads
  * Better ergonomics and state handling

* AzAPI (use when you need low-level control):
  * Managing preview features or brand-new Azure services not yet modeled in `azurerm`
  * Applying raw ARM templates or specifying `type` + API `version` directly

AzAPI example — creating a VM via raw ARM type and `body`:

```hcl theme={null}
resource "azapi_resource" "vm_example" {
  type     = "Microsoft.Compute/virtualMachines@2021-07-01"
  name     = "vm-example"
  location = "eastus"

  body = jsonencode({
    properties = {
      hardwareProfile = {
        vmSize = "Standard_DS1_v2"
      }
      # other properties...
    }
  })
}
```

Guidelines:

* Prefer `azurerm` for GA resources for better Terraform-native support.
* Use `azapi` when you need immediate access to new API versions, preview features, or raw ARM payloads not yet covered by `azurerm`.
* It’s common to mix both providers in a single configuration — choose the right tool for the resource and be mindful of implicit dependencies (outputs, references, or ordering) between resources managed by different providers.

<Callout icon="warning">
  When mixing `azurerm` and `azapi`, explicitly manage dependencies (e.g., using `depends_on`) if the ordering matters and verify resource state interactions to avoid drift or race conditions.
</Callout>

## Additional operational notes

* `terraform init` resolves providers and records them in `.terraform.lock.hcl`. Commit this lock file to source control.
* Upgrading providers:
  1. Change the version constraint in the `terraform` block.
  2. Run `terraform init -upgrade`.
  3. Run `terraform plan` and test in non-production.
* Use provider aliases to manage multiple subscriptions, tenants, or credentials in a single project.
* Consult official docs and registry pages for provider-specific behaviors:
  * Terraform Providers: [https://www.terraform.io/docs/cli/providers/index.html](https://www.terraform.io/docs/cli/providers/index.html)
  * AzureRM provider registry: [https://registry.terraform.io/providers/hashicorp/azurerm/latest](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
  * AzAPI provider registry: [https://registry.terraform.io/providers/azure/azapi/latest](https://registry.terraform.io/providers/azure/azapi/latest)

## Summary

* Providers connect Terraform to external platforms and are required for managing resources.
* Declare providers via `required_providers` and configure instances with `provider` blocks.
* Pin provider versions and commit `.terraform.lock.hcl` for reproducibility.
* Use `azurerm` for stable, supported Azure resources and `azapi` for new/preview or niche resources that require direct ARM API access.
* Use provider aliases to manage multiple subscriptions, tenants, or credential sets in the same configuration.

Practice these concepts with hands-on examples and incrementally apply provider upgrades in isolated environments to validate changes before production deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/eeac3f53-157e-493c-a726-7e5d9190c4c3/lesson/e75c10ce-2c16-473f-a84a-6f2f642461a6" />
</CardGroup>
