# What is Remote State

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Remote-State/What-is-Remote-State/page

Explains using remote Terraform state with Azure Storage to centralize state, enable locking, secure sensitive data, and avoid storing state in Git.

Remote state is how teams share a single authoritative view of Terraform-managed infrastructure. When multiple people run Terraform against the same environment, using local state files quickly leads to inconsistencies, merge conflicts, and even data exposure.

Consider a common scenario:

* John has a local Terraform configuration and a `terraform.tfstate` file on his machine.
* Jack has a separate local configuration and a different `terraform.tfstate`.\
  Both believe they manage the same infrastructure, yet each holds a different, potentially stale snapshot of the environment.

Why storing state in Git is a bad idea:

* Terraform state files change frequently and are not source code; treating them like code produces noisy commits.
* State often contains sensitive values (secrets, resource IDs, connection strings) that should not be in a code repository.
* Git is optimized for textual merges, not for reconciling concurrent binary-like state updates, so merge conflicts and corruption are common.
* Git provides no automatic concurrency control for Terraform operations; two simultaneous applies can overwrite each other’s state.

What Terraform needs instead is a remote backend that provides:

* A single, authoritative state location so every operation starts from the latest state and writes updates back centrally.
* Concurrency control (state locking) so only one operation can modify state at a time.
* Access controls and encryption to protect sensitive data.

<Frame>
  <img alt="The image illustrates a workflow involving two users, John and Jack, managing Terraform state files, with steps for loading, state locking, and security. It shows interactions with a version control system and encapsulated processes." />
</Frame>

For Azure-based teams, the recommended approach is to use Azure Storage (Azure Blob Storage) as the Terraform backend via the `azurerm` backend. Azure Storage provides encryption at rest, RBAC integration, and state locking implemented with blob leases to prevent concurrent writes that would corrupt state.

Example `azurerm` backend block (HCL):

```hcl theme={null}
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "tfstateacct"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

Backend configuration notes:

* The Storage account and container must exist before running `terraform init`, unless you create them out-of-band (for example, with a separate Terraform run or via Azure CLI).
* Ensure the identity used by Terraform (service principal, managed identity, or your user account) has read/write access to the storage container.
* State locking is implemented using blob leases, preventing simultaneous writes.

Common backend configuration options

| Option                 | Purpose                                                                        | Example                  |
| ---------------------- | ------------------------------------------------------------------------------ | ------------------------ |
| `resource_group_name`  | The Resource Group containing the Storage Account                              | `rg-terraform-state`     |
| `storage_account_name` | The Storage Account used to store the state                                    | `tfstateacct`            |
| `container_name`       | The Blob container within the Storage Account                                  | `tfstate`                |
| `key`                  | Path/name of the state file (acts like a unique identifier for this workspace) | `prod.terraform.tfstate` |

Initialize the backend after creating your storage resources and adding the backend block:

```bash theme={null}
terraform init
```

If you want to supply backend settings dynamically (for CI/CD or automation), pass them as `-backend-config` flags:

```bash theme={null}
terraform init \
  -backend-config="resource_group_name=rg-terraform-state" \
  -backend-config="storage_account_name=tfstateacct" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=prod.terraform.tfstate"
```

<Callout icon="lightbulb">
  Confirm the storage account and container exist and that the executing identity has the required permissions before running `terraform init`. If they don't, backend initialization will fail.
</Callout>

<Callout icon="warning">
  Do not store Terraform state files in Git. This can expose sensitive data, create frequent merge conflicts, and lead to state corruption.
</Callout>

How to migrate existing local state

* If you already have a `terraform.tfstate` locally, `terraform init` will detect the configured remote backend and prompt to migrate local state to the remote backend. You can automate migration using `terraform init -migrate-state`.
* Alternatively, you can use `terraform state push` to upload a local state, or follow a two-step process: create the backend resources out-of-band, then run `terraform init` and allow it to move state.

Key takeaways

* Local state does not scale for teams — it leads to inconsistent views and possible corruption.
* Source control is not a safe place for Terraform state due to sensitivity and concurrency concerns.
* Use a remote backend (for Azure: Azure Storage with the `azurerm` backend) to centralize state, enable locking, and secure sensitive data.

Links and references

* [Terraform Backends Documentation](https://www.terraform.io/docs/backends/index.html)
* [Azure Storage documentation](https://docs.microsoft.com/azure/storage/)
* [Terraform azurerm Backend Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/terraform_backend)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/4693ec96-f075-4e4f-922b-1f1e27202120/lesson/dd3e2db7-ff0b-4ded-be2f-211a2459c1bb" />
</CardGroup>
