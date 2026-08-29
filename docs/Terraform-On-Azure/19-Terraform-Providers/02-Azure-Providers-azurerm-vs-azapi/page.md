# Resource Group in West Europe, explicitly using the "weu" provider alias
resource "azurerm_resource_group" "rg_weu" {
  name     = "rg-hub-weu"
  location = "West Europe"
  provider = azurerm.weu
}

# Resource Group in Qatar Central, explicitly using the "qc" provider alias
resource "azurerm_resource_group" "rg_qc" {
  name     = "rg-hub-qc"
  location = "Qatar Central"
  provider = azurerm.qc
}
```

Note the explicit bindings: `provider = azurerm.weu` and `provider = azurerm.qc`. Without these, Terraform uses the default (non-aliased) `azurerm` provider block, which could result in resources being deployed to the wrong subscription or region.

Authentication reminder: setting `subscription_id` selects the target subscription, but Terraform still needs authentication credentials. Provide credentials via environment variables, a service principal, managed identity, or other supported authentication mechanisms.

<Callout icon="lightbulb">
  Always bind resources explicitly to an aliased provider when working with multiple provider configurations. Explicit bindings prevent accidental deployments to the default provider or the wrong subscription.
</Callout>

Best practices and considerations

| Topic             | Recommendation                                                                                                           | Example / Notes                                                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Default provider  | If you want a fallback, configure a non-aliased `azurerm` provider block.                                                | `provider "azurerm" { features {} }`                                                                                             |
| Credentials       | Avoid hard-coding secrets. Use environment variables, service principals, or managed identities.                         | See [Azure authentication for Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli) |
| Modules           | Pass providers into modules using the `providers` argument if module resources must target a specific provider instance. | `module "x" { source = "./module" providers = { azurerm = azurerm.weu } }`                                                       |
| Naming            | Use concise alias names that indicate region or purpose (e.g., `weu`, `qc`, `prod`, `stg`).                              | Clear aliases reduce configuration confusion.                                                                                    |
| Secret management | Store subscription IDs and sensitive variables in secure storage (Key Vault, secrets manager, or CI secret stores).      | Avoid committing secrets to VCS.                                                                                                 |

When using modules that need to operate against multiple providers, pass the aliased provider into the module explicitly. Example:

```hcl theme={null}
module "hub" {
  source = "./modules/hub"
  # Pass the aliased provider instance into the module
  providers = {
    azurerm = azurerm.weu
  }
}
```

This ensures the module's resources are created in the intended subscription/region.

<Callout icon="warning">
  If resources are not bound to the correct provider alias, Terraform may create resources in the wrong subscription or region. Always verify provider bindings (and authentication) before running `terraform apply`.
</Callout>

Summary

Provider aliases enable safe, maintainable multi-region and multi-subscription deployments in a single Terraform project. Use clear alias naming, explicit resource bindings, secure authentication methods, and provider-passing into modules to minimize risk and keep your infrastructure code predictable.

Further reading and references

* [Terraform Providers — Multiple Provider Configurations](https://www.terraform.io/docs/language/providers/configuration.html)
* [AzureRM Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* [Azure authentication options for Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/eeac3f53-157e-493c-a726-7e5d9190c4c3/lesson/d9f29a5c-d620-4796-98b5-2a3fbf90c981" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/eeac3f53-157e-493c-a726-7e5d9190c4c3/lesson/7d5b7814-9314-49e1-afba-b83bcf29ed56" />
</CardGroup>


# Azure Providers azurerm vs azapi

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Providers/Azure-Providers-azurerm-vs-azapi/page

Comparison of Terraform Azure providers azurerm and azapi, outlining differences in abstraction, validation, use cases, and guidance to combine them for stable and preview features

In this lesson we’ll focus on how Terraform interacts with Microsoft Azure and the two primary providers you’ll encounter: AzureRM and AzAPI. Terraform communicates with Azure through providers—these act as an abstraction layer between Terraform and the Azure platform. For Azure, you can use either or both providers in a single project. Each provider differs in abstraction level, validation, and flexibility, so choosing the right one for each use case is important.

* AzureRM: a high-level, opinionated provider that enforces schemas, performs input validation, and provides strongly typed resources. It’s jointly maintained by HashiCorp and Microsoft and is the most commonly used provider for Azure infrastructure.
* AzAPI: a lower-level provider exposing direct access to Azure Resource Manager (ARM) APIs. It’s maintained by Microsoft and supports any ARM resource type and API version with minimal abstraction—ideal for preview or newly released features not yet available in AzureRM.

A key point: these providers are complementary and can be used together in the same Terraform project.

## Quick provider summaries

| Provider  |                Abstraction level | Best for                                                                 | Example usage                                                          |
| --------- | -------------------------------: | ------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| `azurerm` |       High-level, strongly typed | Stable, common Azure services (VMs, networks, storage, managed services) | Use when you want schema validation and predictable lifecycle behavior |
| `azapi`   | Low-level, direct ARM API access | New/preview features, niche or advanced configurations                   | Use when AzureRM doesn’t yet support a resource or API version         |

<Callout icon="lightbulb">
  You can combine AzureRM and AzAPI in the same Terraform project: use AzureRM for stable, validated resource types and AzAPI for features that are not yet supported by AzureRM.
</Callout>

## AzureRM (high-level) — what you get

* Official provider for public Azure cloud.
* Maintains resource lifecycle via ARM APIs.
* Strongly typed resources with schema validation and built-in lifecycle handling.
* Best choice for stable, well-supported Azure services.
* Limitation: may lag behind Azure for preview or newly released features.

## AzAPI (low-level) — characteristics & benefits

<Frame>
  <img alt="The image is a presentation slide explaining the existence of the &#x22;azapi&#x22; provider, which allows Terraform to directly interact with ARM APIs. It highlights characteristics like no predefined resource schemas, support for any ARM resource or API version, and enabling preview and newly released features." />
</Frame>

* No predefined resource schemas: you specify the ARM resource type and API version directly.
* Support for any ARM resource or API version: use new or preview APIs immediately.
* Enables preview and newly released features without waiting for AzureRM provider schema updates.

<Callout icon="warning">
  AzAPI provides flexibility but no compile-time schema validation. Mistakes in API version or property names will only surface at `terraform apply`. Use AzAPI for targeted gaps, not as a default for everything.
</Callout>

## AzAPI use cases and trade-offs

* When a feature is not yet supported in AzureRM (new or preview capabilities).
* Advanced or edge-case configurations and platform experimentation.
* Trade-offs: you must choose API versions manually, deal with runtime errors, and perform more detailed ARM knowledge checks during development.

## Practical examples

### 1) AzureRM-only provider (typical setup)

provider configuration:

```hcl theme={null}
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.55.0, != 4.59.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "1b228746-75fd-46ed-a6b-6a9066d6d3a"
}
```

Initialize the working directory:

```bash theme={null}
terraform init --upgrade
```

Example CLI confirmation:

```json theme={null}
{
  "message": "Terraform has been successfully initialized!"
}
```

You can confirm your Azure subscription with Azure CLI:

```bash theme={null}
az account show
```

Example output (representative):

```json theme={null}
{
  "environmentName": "AzureCloud",
  "id": "1b228746-75fd-46ed-a6b-6a9066d6d3a",
  "name": "PenTest Lab 2",
  "isDefault": true,
  "tenantId": "1e0fa212-37dc-45f5-bb0f-b60687cac64b",
  "user": {
    "name": "rithinskaria@kodekloud.lab.onmicrosoft.com",
    "type": "user"
  }
}
```

### 2) Adding AzAPI alongside AzureRM

Declare both providers under `required_providers` and configure each provider block. Terraform loads all `.tf` files in the working directory.

```hcl theme={null}
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.55.0, != 4.59.0"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "2.8.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "1b228746-75fd-46ed-a6b-6a9066d6d3a"
}

provider "azapi" {
  subscription_id = "1b228746-75fd-46ed-a6b-6a9066d6d3a"
}
```

Notes on provider file naming:

* Terraform loads all `.tf` files in a directory. Many teams use `providers.tf` (or `provider.tf`) for clarity, especially when multiple providers are present.

## Creating the same resource: AzureRM vs AzAPI

AzureRM resource group (strongly typed and validated):

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = "kodekloud-tf-rg"
  location = "eastus"
  tags = {
    environment = "testing"
  }
}
```

AzAPI equivalent (direct ARM type + API version):

```hcl theme={null}
resource "azapi_resource" "rg" {
  name     = "kodekloud-tf-rg-azapi"
  type     = "Microsoft.Resources/resourceGroups@2021-04-01"
  location = "eastus"
  tags = {
    environment = "testing"
  }
}
```

Notes on the AzAPI example:

* `type` uses the format `<namespace>/<resourceType>@<apiVersion>`.
* For complex resources you can pass a full ARM JSON body (use `jsonencode()`), or set specific properties as required.
* Because AzAPI lacks a typed schema, verify the API version and property names against ARM documentation—errors will appear at apply time if mismatched.

## When to use which provider

* Use AzureRM when you want:
  * Schema validation
  * Predictable lifecycle behavior
  * Coverage for the majority of common Azure resources
* Use AzAPI when you need:
  * Immediate access to new or preview ARM features
  * Niche property control or resource types not exposed by AzureRM
* Common approach: use AzureRM for most resources and AzAPI selectively to fill gaps.

## Real-world scenario

If Microsoft releases a new capability for Azure Database for PostgreSQL that’s not yet available in AzureRM, you can target the correct ARM resource type and API version with AzAPI to enable that capability immediately while keeping the rest of your infrastructure managed by AzureRM.

## Wrap-up

AzureRM and AzAPI are complementary:

* AzureRM = stability, validation, conventional provider behaviors.
* AzAPI = agility, immediate ARM access, and coverage for preview/new features.

Use AzureRM as your default provider and introduce AzAPI selectively to bridge feature gaps or enable early adoption of Azure capabilities. This hybrid approach helps keep Terraform configurations maintainable while staying current with Azure’s evolving platform.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/eeac3f53-157e-493c-a726-7e5d9190c4c3/lesson/9e1ac059-a826-4466-a9e4-da67a85b1bc4" />
</CardGroup>
