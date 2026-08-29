# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-Context-for-Terraform/Introduction/page

Guidance on using Terraform with Azure, covering tenants, subscriptions, resource groups, provider configuration, state management, environment separation strategies, and best practices

Azure context required for Terraform

Before writing Terraform code for Azure, it's important to understand the Azure context in which Terraform operates. Terraform declares and plans resources, but Azure enforces scope, boundaries, and permissions. Designing Terraform configurations with Azure's tenants, subscriptions, and resource groups in mind produces more secure, predictable, and maintainable infrastructure.

In this lesson we will:

* Identify core Azure concepts Terraform interacts with: tenants, subscriptions, and resource groups.
* Explain how Terraform maps configuration and state to Azure subscriptions and resource groups so resources are created in the intended scope.
* Describe common approaches for environment separation in Azure (for example: `dev`, `test`, `production`) when using Terraform.
* Provide guidance on choosing an appropriate environment separation strategy based on scale, access control, and governance requirements.

This foundation helps you design Terraform configurations that align with Azure governance and organizational needs.

<Callout icon="lightbulb">
  Every Terraform action against Azure is scoped and controlled by Azure. Terraform orchestrates resources, but Azure determines the boundaries and permissions that apply.
</Callout>

## Key Azure concepts Terraform interacts with

Understanding these Azure constructs is essential when authoring Terraform:

| Azure construct |                                                     What it represents | How Terraform uses it                                                                                                              |
| --------------- | ---------------------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------------- |
| Tenant          | The Azure Active Directory (AAD) identity boundary for an organization | The identity realm used for authentication (service principals, managed identities). Terraform authenticates against a tenant.     |
| Subscription    |                                    Billing and resource quota boundary | Terraform targets a subscription to create and manage resources. Use the subscription ID in provider configuration or credentials. |
| Resource group  |                                Logical container for related resources | Terraform creates resources inside resource groups; they define lifecycle and organizational grouping.                             |

## Example: Provider configuration

A minimal Terraform provider configuration declares the target subscription and tenant (using a service principal or managed identity). Place this in a dedicated provider file (for example `provider.tf`):

```hcl theme={null}
provider "azurerm" {
  features = {}

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id

  # Recommended: authenticate with a service principal, environment variables,
  # or managed identity rather than hard-coding credentials.
}
```

Use variables (e.g. `var.subscription_id`) or environment-based authentication to keep credentials out of code and configuration files.

## How Terraform maps configuration and state to Azure

* Provider scope: The AzureRM provider determines the tenant and subscription used for resource operations. You can set `subscription_id` and `tenant_id` in the provider or rely on the environment/credentials.
* Resource group mapping: Terraform resources that require a resource group (for example, `azurerm_virtual_network`, `azurerm_storage_account`) include a `resource_group_name` argument to place them in the intended group.
* State file considerations:
  * A single state file can manage many resources across multiple resource groups in one subscription.
  * Use workspaces or separate state backends to separate environments or teams.
  * Store Terraform state remotely (for example, in an Azure Storage Account with blob locking via Azure Blob Storage + `azurerm` backend) to enable collaboration and locking.

## Common approaches for environment separation

Selecting an environment separation strategy depends on scale, team autonomy, security, and governance. Here are common patterns:

| Strategy                                                           | Description                                                                                                          | Typical use cases                                                                        |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Single subscription, multiple resource groups                      | Use resource groups per environment (e.g., `rg-app-dev`, `rg-app-prod`) within one subscription                      | Small teams, minimal billing separation, simpler networking                              |
| Multiple subscriptions per environment                             | Separate subscriptions for `dev`, `test`, `prod` for quotas and billing isolation                                    | Medium to large organizations with distinct billing and quota needs                      |
| Management / Shared services subscription + workload subscriptions | Dedicated subscriptions for shared services (management, logging, identity) and separate subscriptions for workloads | Enterprises requiring strong isolation, central governance, and shared-platform services |
| Hybrid: tenant-level policies + subscription separation            | Use Azure Policy and RBAC at tenant or management group level while splitting workloads across subscriptions         | Organizations needing consistent governance across many subscriptions                    |

## Implementation patterns and examples

* Small scale / low risk: Use a single Azure subscription; create resource groups per environment. Use Terraform workspaces or separate state files per environment.
* Medium scale: Use one subscription per environment. Configure provider per environment or use different backend states and variable sets.
* Enterprise scale: Use management groups to organize subscriptions, centralize shared services in dedicated subscriptions, and enforce Azure Policy and RBAC. Use separate Terraform state backends and Service Principals or Managed Identities with least privilege per subscription.

### Example folder layout for multiple environments

* `live/`
  * `dev/`
    * `network/`
    * `app/`
  * `prod/`
    * `network/`
    * `app/`

This layout maps logically to separate state files and backends, enabling independent lifecycle and access control per environment.

## Choosing the right strategy

Ask these questions to decide:

* Do you need billing and quota isolation per environment?
* Do different teams require separate ownership and RBAC?
* Is governance (Azure Policy, security baselines) required consistently across all workloads?
* How many subscriptions and management groups will you manage at scale?

Guidelines:

* If you need simple separation with limited overhead, use resource groups inside one subscription.
* If billing, quota, and isolation are important, use separate subscriptions per environment.
* For enterprise governance and scale, combine management groups, subscription separation, and centralized shared services.

## Best practices

* Authenticate Terraform using service principals, managed identities, or secure CI/CD credentials—avoid hard-coded secrets.
* Store Terraform state remotely with locking (Azure Storage Account backend) and enable versioning.
* Use modules to encapsulate environment-agnostic components and reduce duplication.
* Apply Azure Policy and RBAC at the appropriate scope: management group, subscription, or resource group.
* Test changes in a non-production subscription or resource group before applying to production.

## Links and references

* [Azure Provider for Terraform (azurerm)](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
* [Azure management groups and subscriptions documentation](https://learn.microsoft.com/azure/governance/management-groups/)
* [Azure Resource Manager (ARM) overview](https://learn.microsoft.com/azure/azure-resource-manager/management/overview)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/7fc76e5f-e1e7-4c53-8940-57761020744e/lesson/28067714-12e1-4d90-9802-bf39ed6b5370" />
</CardGroup>
