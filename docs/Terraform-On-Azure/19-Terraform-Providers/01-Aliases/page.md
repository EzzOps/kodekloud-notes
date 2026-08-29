# Aliases

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Providers/Aliases/page

Explains Terraform azurerm provider aliases for managing multiple Azure regions, subscriptions, and environments, including explicit provider bindings, module provider passing, and authentication best practices.

In this lesson we cover Terraform provider aliases and how to use them with the Azure provider (`azurerm`). Provider aliases let you define multiple instances of the same provider within a single Terraform configuration. This is essential when you need to manage resources across multiple Azure regions, subscriptions, or isolated environments from the same codebase.

Why use provider aliases? Typical scenarios include:

* Multi-region deployment: Deploy resources to multiple Azure regions from the same Terraform configuration without duplicating code or maintaining separate projects. Use different provider aliases to target specific regions.
* Multi-subscription / credential management: Run a single Terraform plan against multiple subscriptions or with different credentials (service principals, managed identities) — useful for hub-and-spoke and cross-subscription architectures.
* Environment isolation: Keep production, staging, and sandbox resources separated to reduce the risk of accidental deployment into the wrong environment.

<Frame>
  <img alt="The image outlines three concepts: multi-region deployment, credential management, and isolation, each with a brief explanation related to resource distribution, credential usage, and environment separation." />
</Frame>

Each environment, region, or subscription can have its own provider block. When resources are explicitly bound to an aliased provider, Terraform will use that instance for CRUD operations, preventing accidental resource creation in an unintended subscription or region.

Example: two aliased `azurerm` provider instances and resources bound to them

```hcl theme={null}
provider "azurerm" {
  alias           = "weu"
  features        {}
  # WE-HUB (West Europe subscription)
  subscription_id = "00000000-0000-0000-0000-000000000001"
}

provider "azurerm" {
  alias           = "qc"
  features        {}
  # QC-HUB (Qatar Central subscription)
  subscription_id = "00000000-0000-0000-000000000002"
}
