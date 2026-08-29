# terraform plan (example)
azurerm_storage_account.example: Refreshing state...
  ~ resource "azurerm_storage_account" "example" {
      ~ tags = {
          - "environment" = "policy-applied" -> null
          + "Added from"  = "Terraform"
        }
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

2. With `ignore_changes` for `tags`

Add a `lifecycle` block that instructs Terraform to ignore changes to the `tags` attribute:

```hcl theme={null}
resource "azurerm_storage_account" "example" {
  name                     = var.storage_account_name
  location                 = "East US"
  resource_group_name      = "rg-workshop-riskaria"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  public_network_access_enabled = true

  tags = {
    "Added from" = "Terraform"
  }

  lifecycle {
    ignore_changes = [
      tags,
    ]
  }
}
```

After adding this lifecycle block, Terraform will still refresh and detect the external tags, but it will not plan any changes to reconcile them.

Example outputs

Terraform apply reporting no changes:

```bash theme={null}
$ terraform apply -var "storage_account_name=saqeworkshop0689" -auto-approve
Acquiring state lock. This may take a few moments...
azurerm_storage_account.example: Refreshing state...
[id=/subscriptions/25d172e2-1262-4980-8164-1d2c95eae1ff/resourceGroups/rg-qe-workshop-riskaria/providers/Microsoft.[AWS_SECRET_ACCESS_KEY]]
No changes. Your infrastructure matches the configuration.
Releasing state lock. This may take a few moments...
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

Querying the storage account tags with Azure CLI shows tags are controlled externally and not overwritten by Terraform:

```bash theme={null}
$ az storage account show -g rg-qe-workshop-riskaria -n saqeworkshop0689 --query tags
{}
```

Working in your editor / VS Code

* Reuse an existing storage account if convenient.
* Confirm the account exists using `az storage account list -o table`.
* If Terraform initially plans to change `tags`, add the `lifecycle { ignore_changes = [tags] }` block and re-run `terraform plan`. After adding `ignore_changes`, Terraform should no longer propose updates for that attribute.

Concise HCL example:

```hcl theme={null}
resource "azurerm_resource_group" "rg" {
  name     = "lifecycle-resources"
  location = "West Europe"
}

resource "azurerm_storage_account" "storage" {
  name                     = "lifecyclestorage75636"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "lifecycle"
  }

  lifecycle {
    ignore_changes = [
      tags,
    ]
  }
}
```

Typical `terraform plan` outputs you may observe

* Before adding `ignore_changes`:

```bash theme={null}
# terraform plan (before ignore_changes)
azurerm_storage_account.storage: Refreshing state...
  ~ resource "azurerm_storage_account" "storage" {
      ~ tags = {
          - "environment" = "policy-managed" -> null
          + "environment" = "lifecycle"
        }
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

* After adding `ignore_changes`:

```bash theme={null}
# terraform plan (after ignore_changes)
azurerm_storage_account.storage: Refreshing state...

No changes. Your infrastructure matches the configuration.
```

Best practices and caveats

<Callout icon="lightbulb">
  Use `ignore_changes` sparingly and only for attributes that are legitimately owned by an external system (for example, tags applied by Azure Policy). Limit its scope to the minimal set of attributes you need to ignore to avoid hiding unexpected drift.
</Callout>

<Callout icon="warning">
  Do not overuse `ignore_changes` to mask configuration problems. Ignoring attributes makes Terraform blind to changes in those attributes and can make debugging and auditing more difficult. Always prefer centralizing ownership (for example using a policy-first tagging approach) where practical.
</Callout>

Quick comparison of lifecycle meta-arguments

| Meta-argument           | Purpose                                                                | Typical use case                                                         |
| ----------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `ignore_changes`        | Instruct Terraform to not act on differences for specified attributes  | Let platform or external tooling manage tags or properties               |
| `prevent_destroy`       | Prevent a resource from being destroyed by Terraform                   | Protect critical resources from accidental deletion                      |
| `create_before_destroy` | Ensure replacement resource is created before the old one is destroyed | Perform in-place replacements that require no downtime (where supported) |

Summary

* `ignore_changes` is useful to avoid reconciliation for attributes managed outside Terraform (e.g., tags applied by Azure Policy).
* Apply it narrowly — to the minimal set of attributes you explicitly want Terraform to ignore.
* Terraform will continue to detect differences but will not include the ignored attributes in the plan, preventing constant update churn.

Links and references

* [Terraform lifecycle meta-arguments — ignore\_changes](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#ignore_changes)
* [Azure Policy documentation](https://learn.microsoft.com/azure/governance/policy/)
* [Azure CLI: storage account list](https://learn.microsoft.com/cli/azure/storage/account?view=azure-cli-latest#az_storage_account_list)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/82cd6352-f026-4f6f-b739-634e56558de4/lesson/956f5453-cd68-4b1e-953d-8b4080929dc2" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/82cd6352-f026-4f6f-b739-634e56558de4/lesson/cec76ae3-cbb9-4f33-8c55-c65cc5e0adfc" />
</CardGroup>


# prevent destroy

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Lifecycle-Meta-Arguments/prevent-destroy/page

Explains Terraform lifecycle prevent_destroy to protect critical Azure resources, how it blocks planned deletions, and methods to intentionally replace or remove protected resources.

In this lesson we cover the Terraform `prevent_destroy` lifecycle meta-argument: what it does, when to use it, and how to handle cases where a protected resource must be intentionally removed or replaced. This is especially useful for protecting critical Azure resources such as production storage accounts, databases, and Key Vaults.

Two core behaviors of `prevent_destroy`:

* It prevents accidental deletion of critical resources. If a planned change would cause a resource to be destroyed, Terraform refuses to perform that destruction.
* Terraform surfaces an explicit error during the plan phase if destruction is detected. This ensures `terraform apply` cannot silently delete the resource — it forces an intentional decision.

<Frame>
  <img alt="The image explains two functions: preventing accidental deletion of critical resources and causing Terraform to throw an error if a resource is planned for destruction." />
</Frame>

Use case overview

* Protect production-grade resources from accidental or automatic removal during refactoring or configuration changes.
* Add an extra safety layer in your IaC pipeline beyond cloud provider delete locks (e.g., Azure Delete Lock), implemented at the Terraform level.

<Callout icon="lightbulb">
  `prevent_destroy` causes plan-time failures when a resource would be destroyed. Always run `terraform plan` and review the output before applying in production to prevent unexpected interruptions.
</Callout>

Example: Protect an Azure Storage Account with `prevent_destroy`

```hcl theme={null}
provider "azurerm" {
  features {}
  subscription_id = "1b228746-75fd-46ed-8a6b-6a9066d6d3a3"
}

resource "azurerm_resource_group" "rg" {
  name     = "lifecycle-resources"
  location = "West Europe"
}

resource "azurerm_storage_account" "storage" {
  name                     = "lifestorage75636"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  lifecycle {
    prevent_destroy = true
  }
}
```

What happens with the configuration above

* Creation: Running `terraform apply` creates the resource normally.
* Replacement: If later you change a property that requires replacement (for example changing `account_replication_type` from `LRS` to `ZRS`), the plan will attempt to destroy the existing storage account and create a new one. Because `prevent_destroy = true` is set, Terraform aborts the plan and reports an error.

Typical commands and sample outputs

Initialization:

```bash theme={null}
terraform init
```

Sample init output (truncated):

```text theme={null}
- Reusing previous version of hashicorp/azurerm from the dependency lock file
- Using previously-installed hashicorp/azurerm v4.59.0

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see any changes that are required for your infrastructure.
```

Create resources:

```bash theme={null}
terraform apply --auto-approve
```

Sample apply output (truncated):

```text theme={null}
azurerm_resource_group.rg: Creating...
azurerm_storage_account.storage: Creating...
azurerm_resource_group.rg: Creation complete after 1s [id=/subscriptions/.../resourceGroups/lifecycle-resources]
azurerm_storage_account.storage: Still creating... [10s elapsed]
azurerm_storage_account.storage: Creation complete after 1m20s [id=/subscriptions/.../resourceGroups/lifecycle-resources/providers/Microsoft.[AWS_SECRET_ACCESS_KEY]]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

Planned replacement blocked by `prevent_destroy`:

If you change a property that requires replacing the storage account and then run `terraform plan` or `terraform apply`, you will see an error similar to this:

```bash theme={null}
terraform apply --auto-approve
```

Sample plan error:

```text theme={null}
Error: Instance cannot be destroyed:

  on main.tf line 11:
  resource "azurerm_storage_account" "storage" {

Resource "azurerm_storage_account.storage" has lifecycle.prevent_destroy set, but the plan calls for this resource to be destroyed. To avoid this error and continue with the plan, either disable lifecycle.prevent_destroy or reduce the scope of the plan using the -target flag.
```

When to use `prevent_destroy` (summary table)

| Scenario                       | Why use `prevent_destroy`?                                          | Example                                            |
| ------------------------------ | ------------------------------------------------------------------- | -------------------------------------------------- |
| Protect critical data          | Prevent accidental deletion of storage accounts, databases, secrets | `Key Vault`, production `Storage Account`          |
| Safe refactoring               | Avoid accidental destructive changes during refactors               | Team members changing resource names or properties |
| Not needed for ephemeral infra | Adds friction for resources intended to be regularly recreated      | Test or dev environments                           |

How to intentionally remove or replace a protected resource

* Update the lifecycle block: set `prevent_destroy = false` (or remove the block), run `terraform plan` and then `terraform apply` again. This is the safest, most explicit path.
* Targeted plans: use `-target` to reduce the scope of evaluation. Note: `-target` does not bypass `prevent_destroy` for resources that are planned to be destroyed — it simply limits what Terraform evaluates.
* Remove from state as a last resort: run `terraform state rm <resource>` and then delete the resource outside of Terraform. This makes Terraform forget the resource and is potentially dangerous for production-managed resources — use with care and approvals.

<Callout icon="warning">
  `prevent_destroy` is a safety mechanism. Do not circumvent it lightly for production resources. If destruction is truly required, make the removal explicit (for example, by modifying the lifecycle block) and ensure appropriate approvals are in place.
</Callout>

Comparing `prevent_destroy` to Azure Delete Lock

* `prevent_destroy` is implemented at the Terraform/IaC layer and prevents Terraform from planning a destroy.
* Azure Delete Locks are enforced by the Azure control plane and block deletion operations regardless of tool.
  Using both provides defense in depth: the lock protects resources from accidental deletion through any client, while `prevent_destroy` prevents accidental deletion as a result of Terraform workflows.

Links and references

* Terraform lifecycle meta-arguments: [https://www.terraform.io/docs/language/meta-arguments/lifecycle.html](https://www.terraform.io/docs/language/meta-arguments/lifecycle.html)
* Azure Resource Manager locks: [https://learn.microsoft.com/azure/role-based-access-control/locking-resources](https://learn.microsoft.com/azure/role-based-access-control/locking-resources)
* Terraform Azure Provider (azurerm): [https://registry.terraform.io/providers/hashicorp/azurerm/latest](https://registry.terraform.io/providers/hashicorp/azurerm/latest)

Further reading

* Best practices for protecting production infrastructure in GitOps/IaC pipelines
* Strategies for data migration and in-place upgrades to avoid destructive replacements

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/82cd6352-f026-4f6f-b739-634e56558de4/lesson/f996ed9f-6e8d-4f63-98ab-4a32d1ab6600" />
</CardGroup>
