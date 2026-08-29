# Azure Concepts Terraform Operates On

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Azure-Context-for-Terraform/Azure-Concepts-Terraform-Operates-On/page

Explains how Terraform uses the AzureRM provider to manage Azure resources via ARM APIs, covering subscriptions, resource groups, regions, lifecycle actions, state management, and operational best practices.

This lesson explains what Terraform actually talks to in Azure before you start creating resources. Terraform does not recreate or replace Azure’s resource model — it automates it. When you run Terraform with the AzureRM provider, Terraform translates your desired infrastructure expressed in HCL into the same Azure Resource Manager (ARM) API calls used by the Azure Portal and ARM templates.

Think of Terraform as a translator: you write the desired state in [HCL](https://www.terraform.io/language), and Terraform issues ARM API calls to create, update, or delete resources in your Azure tenant.

At the Azure level, Terraform primarily operates within three core boundaries:

* Subscriptions: Security, access, and billing boundaries. Terraform must be configured to target a subscription (or multiple subscriptions via provider configuration); most resources are scoped to a subscription.
* Resource groups: Logical deployment and lifecycle boundaries used to group related resources for management and deletion.
* Regions: Physical Azure datacenters where resources are deployed. Most resources must have a valid Azure region; some services are global or tenant-scoped.

<Frame>
  <img alt="The image explains three Azure concepts that Terraform operates on: Subscriptions (security, access, and billing boundaries), Resource Groups (deployment and lifecycle boundaries), and Regions (physical locations for resource deployment)." />
</Frame>

Example provider and resource group snippets show how Terraform targets these boundaries. Replace placeholder values with your own subscription, tenant, and names:

```hcl theme={null}
provider "azurerm" {
  features = {}

  subscription_id = "00000000-0000-0000-0000-000000000000"
  tenant_id       = "11111111-1111-1111-1111-111111111111"
}

resource "azurerm_resource_group" "rg" {
  name     = "example-rg"
  location = "eastus"
}
```

Key concepts summarized in a table:

|       Boundary | Role                                  | Example                                                      |
| -------------: | ------------------------------------- | ------------------------------------------------------------ |
|   Subscription | Billing, policy, and access boundary  | `subscription_id = "..."` in provider config                 |
| Resource group | Deployment and lifecycle boundary     | `azurerm_resource_group` groups compute, networking, storage |
|         Region | Physical location where resources run | `location = "eastus"` on resources                           |

When Terraform runs, it performs three core lifecycle actions against Azure:

* Provision: Create new resources by calling ARM APIs when resources do not exist.
* Update: Modify existing resources when configuration or inputs change.
* Delete: Remove resources when they are removed from configuration or explicitly destroyed.

<Frame>
  <img alt="The image illustrates how Terraform interacts with Azure's existing resource model, highlighting operations like provisioning, updating, and deleting resources." />
</Frame>

Table: Terraform lifecycle operations vs Azure

| Operation | Description                                       | Result                              |
| --------: | ------------------------------------------------- | ----------------------------------- |
| Provision | Create resources described in HCL                 | New resources in Azure via ARM APIs |
|    Update | Apply changes detected in plan                    | Resource modifications via ARM APIs |
|    Delete | Remove resources removed from config or destroyed | Resources deleted in Azure          |

Terraform state must reflect what actually exists in Azure. State drift happens when resources are changed outside of Terraform (for example, manual deletions in the Azure Portal). If state is out of sync, `terraform plan` and `terraform apply` may produce unexpected results.

Resource groups are commonly used as lifecycle boundaries. Terraform normally:

* Plans across all resources in scope and produces a single execution plan.
* Applies changes in the correct order using dependency resolution (explicit references or implicit attribute dependencies).
* Destroys resources grouped under a resource group if the group itself is removed in Azure.

Terraform typically creates the resource group before resources that depend on it, ensuring correct deployment ordering. Understanding dependency relationships and resource attributes is essential for predictable deployments.

> **warning** Deleting a resource group in Azure deletes everything it contains—regardless of whether Terraform created those resources. Accidental deletions outside Terraform cause state drift and can break future Terraform operations. Design resource groups and environment separation carefully to avoid unintended data or service loss.

> **lightbulb** Use remote state backends and access controls to keep Terraform state consistent and safe. For Azure, the `azurerm` backend using an Azure Storage Account plus a `container_name` and `key` is a common pattern for team workflows.

Example remote backend configuration (replace placeholders):

```hcl theme={null}
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstatestorage"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

Operational best practices for safe, scalable Terraform on Azure:

* Separate environments (dev/test/prod) using resource groups, subscriptions, or workspaces.
* Use multiple subscriptions when needed for security, billing, or policy isolation.
* Store state remotely (e.g., Azure Storage backend) and enable state locking where supported.
* Use least-privilege authentication (service principals, managed identities, or Azure CLI auth) and follow organizational RBAC policies.
* Review and audit changes with `terraform plan` and CI/CD pipelines before applying to production.

Links and references

* [Azure Resource Manager templates overview](https://learn.microsoft.com/azure/azure-resource-manager/templates/overview)
* [Terraform language docs (HCL)](https://www.terraform.io/language)
* [Azure CLI authentication](https://learn.microsoft.com/cli/azure/authenticate-azure-cli)
* [Terraform backend azurerm](https://www.terraform.io/language/settings/backends/azurerm)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/7fc76e5f-e1e7-4c53-8940-57761020744e/lesson/cebc9f10-30fe-4ce0-bfb2-1324044b1fa9)
