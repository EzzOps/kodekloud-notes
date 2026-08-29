# This file is maintained automatically by "terraform init".
provider "registry.terraform.io/hashicorp/azurerm" {
  version     = "4.55.0"
  constraints = "4.55.0"
  hashes = [
    "h1:1DbkylsqsoK2K8s1NsMkuR8GtCxxFdXyEshkQM=",
    "zh:3504c212166cb0da721e38b2be8e176f7adb199b599d5c52961e84f3c",
    "zh:49ad233a950c6a6815b014b5c7eb68c251deac5763e519cebadcbad5259",
    "zh:58ad6ecf8ab1eb670555804a3390a25fb2f11b39ea925037bd510faf9b",
  ]
}
```

When a `.terraform.lock.hcl` file exists, subsequent `terraform init` runs will reuse the recorded versions:

```bash theme={null}
$ terraform init
Initializing provider plugins...
- Reusing previous version of registry.terraform.io/hashicorp/azurerm from the dependency lock file
- Using previously-installed registry.terraform.io/hashicorp/azurerm 4.55.0

Terraform has been successfully initialized!
```

Real-world workflow: modular code and provider separation

A common pattern is to keep provider configuration in `provider.tf` and resources in `main.tf` (or split by resource types). This keeps configuration modular and easier to manage in editors like Visual Studio Code.

Example files

provider.tf

```hcl theme={null}
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.55.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "1b228746-75fd-46ed-8a6b-6a9066d6d3a3"
}
```

main.tf

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = "kodekloud-tf-rg"
  location = "eastus"
  tags     = {
    environment = "testing"
  }
}

resource "azurerm_virtual_network" "vnet" {
  name                = "kodekloud-tf-vnet"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  address_space       = ["10.0.0.0/16"]
}
```

With `version = "4.55.0"`, `terraform init` will fetch that exact provider instead of any newer release:

```plaintext theme={null}
$ terraform init
- Finding registry.terraform.io/hashicorp/azurerm version matching "4.55.0"...
- Installing registry.terraform.io/hashicorp/azurerm v4.55.0...
- Installed registry.terraform.io/hashicorp/azurerm v4.55.0 (signed by HashiCorp)
Terraform has been successfully initialized!
```

Refreshing provider selection and updating the lock file

If you change version constraints and want Terraform to re-evaluate available versions and update `.terraform.lock.hcl`, run `terraform init --upgrade`. Example: allow versions greater than `4.55.0` but less than `4.58.0`:

```hcl theme={null}
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "> 4.55.0, < 4.58.0"
    }
  }
}
```

Then run:

```bash theme={null}
$ terraform init --upgrade
Initializing provider plugins...
- Finding registry.terraform.io/hashicorp/azurerm versions matching "> 4.55.0, < 4.58.0"...
- Installing registry.terraform.io/hashicorp/azurerm v4.57.0...
- Installed registry.terraform.io/hashicorp/azurerm v4.57.0 (signed by HashiCorp)
Terraform has been successfully initialized!
```

If you modify constraints but do not use `--upgrade` and the new constraint conflicts with the locked version, Terraform will refuse to proceed and instruct you to run `terraform init --upgrade`. Example error:

```plaintext theme={null}
Error: Failed to query available provider packages

Could not retrieve the list of available versions for provider registry.terraform.io/hashicorp/azurerm: locked provider registry.terraform.io/hashicorp/azurerm 4.59.0 does not match configured version constraint > 4.55.0, != 4.59.0; must use "terraform init --upgrade" to allow selection of new versions
```

Summary and best practices

* Declare version constraints in the `terraform` block under `required_providers` to control which provider versions Terraform can install.
* Use exact pins for maximum stability in production, or ranges/pessimistic constraints for controlled patch updates.
* Combine operators to express ranges and exclusions for known problematic releases.
* Commit `.terraform.lock.hcl` to version control to ensure all users and CI environments use the same provider binaries.
* Use `terraform init --upgrade` intentionally to refresh provider selections and update the lock file.

Links and references

* [Terraform CLI: init](https://www.terraform.io/cli/commands/init)
* [Terraform Provider Version Constraints](https://www.terraform.io/language/providers/requirements)
* [HashiCorp Provider Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/eeac3f53-157e-493c-a726-7e5d9190c4c3/lesson/3f5c5496-f505-4650-8b50-9912ce1ce548)


# When to Use azurerm vs azapi

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Providers/When-to-Use-azurerm-vs-azapi/page

Guide to choosing between Terraform azurerm and azapi providers, recommending azurerm by default and azapi as an escape hatch for unsupported or preview Azure ARM features, with best practices

Now that you understand what the `azurerm` and `azapi` Terraform providers do, the next question is: when should you use each? This guide focuses on practical decision-making to help you choose the right provider for the task—rather than relying on habit or guessing.

Use this guidance to reduce risk, improve maintainability, and keep your Terraform code aligned with Azure features and lifecycle practices.

## Quick decision summary

* Prefer `azurerm` for standard, well-supported Azure resources where stability, validation, and long-term maintainability matter.
* Use `azapi` as an escape hatch when `azurerm` does not yet support a resource or property (including preview APIs), or when you need immediate access to specific ARM features.
* Mix both providers in the same configuration when appropriate: `azurerm` for most resources, `azapi` only where necessary.

## High-level comparison

Below is a concise comparison of the most important criteria to consider when choosing between `azurerm` and `azapi`.

<Frame>
  <img alt="The image is a comparison table between &#x22;azurerm&#x22; and &#x22;azapi&#x22; based on several aspects such as resource schema, validation, feature availability, ease of use, and stability." />
</Frame>

| Aspect               | `azurerm`                                                             | `azapi`                                                                                                 |
| -------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Resource schema      | Strongly typed provider schema with explicit arguments and types      | Effectively schema-less from Terraform’s perspective—passes ARM resource body directly                  |
| Validation           | Provider-side validation detects many errors at `terraform plan` time | Minimal provider validation; many errors surface only when Azure processes the request (often at apply) |
| Feature availability | New Azure features arrive after provider updates and releases         | Immediate access to ARM APIs and API versions (including preview APIs)                                  |
| Ease of use          | High — comprehensive docs, examples, and typed resource blocks        | Moderate — requires knowledge of ARM resource types, API versions, and JSON property shapes             |
| Stability            | High — conservative, production-ready behavior                        | Varies — depends on the underlying ARM API (preview APIs may change)                                    |

## Detailed guidance

Resource schema and validation

* `azurerm` is strongly typed: the provider exposes documented arguments and types for each resource. This enables provider-side validation, clearer error messages, and better editor autocompletion.
* `azapi` treats the ARM resource body as a payload. Terraform (via `azapi`) performs minimal schema validation for ARM properties and forwards the JSON to Azure Resource Manager (ARM). This gives flexibility but removes many safety nets.

Validation behavior:

* `azurerm`: many mistakes are caught in `terraform plan` before modifications reach Azure.
* `azapi`: you are more likely to encounter validation errors at `terraform apply` (or later), so authors must validate ARM properties and API version choices carefully.

Feature availability and release cadence

* `azurerm`: waits for provider maintainers to model new Azure features. There can be a delay between the ARM API release and `azurerm` support.
* `azapi`: can target the ARM API version you need and access new or preview functionality immediately.

Ease of use and author experience

* `azurerm`: better for most teams—well-documented, consistent patterns, and lower cognitive load.
* `azapi`: better for advanced scenarios where direct ARM control is required. Expect to author JSON blocks, choose API versions explicitly, and handle raw ARM property shapes.

Stability and production risk

* `azurerm`: generally the safer choice for production workloads.
* `azapi`: powerful but riskier when used with preview APIs or unstable ARM endpoints. Use with caution and document intent.

## Combining providers (recommended pattern)

You do not need to pick one provider for everything. A pragmatic pattern:

1. Use `azurerm` for the majority of resources—those that are supported, stable, and commonly managed.
2. Introduce `azapi` only for:
   * Resources not yet implemented in `azurerm`.
   * Features only exposed in preview APIs.
   * Cases where you need to set ARM properties that `azurerm` does not expose.

This hybrid approach keeps your configuration readable and safer while still enabling access to the latest Azure capabilities.

## Best practices

* Prefer `azurerm` by default to reduce complexity and operational risk.
* Restrict `azapi` usage to well-justified exceptions. Keep such usages minimal and isolated.
* Document every `azapi` resource with:
  * The exact ARM resource type (e.g., `Microsoft.Service/resourceType`).
  * The targeted ARM API version.
  * The concrete reason `azurerm` couldn’t be used.
* Validate `azapi` configurations against the ARM API reference and test in non-production environments.
* Use version control and code reviews to ensure `azapi` payloads remain maintainable.
* Periodically review `azapi` resources—migrate them to `azurerm` if/when provider support becomes available.

> **lightbulb** Prefer `azurerm` by default. Use `azapi` as an escape hatch for missing or preview features, and document each `azapi` usage with the targeted ARM API version and the reason it was chosen.

## When to choose which provider — short checklist

* Choose `azurerm` when:
  * The resource is supported by the provider.
  * You want provider-side validation and safer `plan` behavior.
  * You need stability and maintainability for production workloads.

* Choose `azapi` when:
  * The resource or property is not yet supported in `azurerm`.
  * You must use a preview or very recent ARM API.
  * You require direct access to ARM properties not surfaced by `azurerm`.

In summary: `azurerm` is the default, stable choice. `azapi` is a powerful tool to access recent or unsupported ARM features, but it requires additional care. Use them together strategically to keep Terraform aligned with Azure’s pace of innovation without sacrificing reliability.

<Frame>
  <img alt="The image is a diagram comparing the usage of &#x22;azurerm&#x22; and &#x22;azapi&#x22; in Terraform, suggesting using &#x22;azurerm&#x22; for standard resources and &#x22;azapi&#x22; only when required, with best practices included." />
</Frame>

## Links and references

* [azurerm provider (Terraform Registry)](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
* [azapi provider (Terraform Registry)](https://registry.terraform.io/providers/azure/azapi/latest)
* [Azure Resource Manager REST API reference](https://learn.microsoft.com/azure/azure-resource-manager/management/rest-api-resources)
* [Terraform documentation](https://www.terraform.io/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/eeac3f53-157e-493c-a726-7e5d9190c4c3/lesson/d459ff12-81e3-423a-8f95-d537ccf715b9)
