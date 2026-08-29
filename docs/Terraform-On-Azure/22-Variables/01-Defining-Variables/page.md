# shows: default, dev, * prod
terraform apply -var="environment=prod"
```

Each workspace maintains an isolated state. The configuration and resources may have the same names, but the state is tracked separately.

## How workspace state is stored in Azure Storage

When using the AzureRM backend, Terraform stores separate state blobs per workspace. For example, if your configured key is `workspace.tfstate`, the backend will typically create blobs such as:

* `workspace.tfstate`
* `workspace.tfstate?env=dev` (backend implementation may vary; common naming patterns include workspace suffixes)
* `workspace.tfstate?env=prod`

Open your storage container to verify the actual blob names. Example screenshot:

<Frame>
  <img alt="The image shows a Microsoft Azure storage container interface listing three blob items with their names, modification dates, access tiers, blob types, sizes, and lease states." />
</Frame>

Workspaces behavior is similar for other backends (S3, local files, etc.) — each workspace gets its own state file object.

## Deleting a workspace — safety checks

Terraform prevents accidental loss of tracked remote objects. You cannot delete a workspace that contains tracked resources unless you first remove those resources from Terraform (destroy them) or you force Terraform to forget them.

Example error when attempting to delete a non-empty workspace:

```bash theme={null}
terraform workspace delete dev

Error: Workspace is not empty

Workspace "dev" is currently tracking the following resource instances:
  - azurerm_resource_group.rg

Deleting this workspace would cause Terraform to lose track of any associated remote objects, which would then require you to delete them manually outside of Terraform. You should destroy these objects with Terraform before deleting the workspace.
```

If you want to permanently delete the workspace and make Terraform forget about its resources (use with extreme caution), use the `-force` flag:

```bash theme={null}
terraform workspace delete -force dev
```

<Callout icon="warning">
  Deleting a workspace that contains resources can leave real infrastructure orphaned and unmanaged. Always run `terraform destroy` in the workspace first if you intend to remove the actual cloud resources. Use `-force` only when you understand the consequences.
</Callout>

## Summary & best practices

* Use workspaces to isolate state (e.g., dev/prod) while reusing the same Terraform code.
* Do not attempt to reference variables inside the backend block for `terraform init`.
* Name resources or use `terraform.workspace` to generate workspace-specific names.
* Verify remote state objects (storage container, S3 bucket) to understand how workspaces map to backend state files.
* Always destroy resources before deleting a workspace to avoid orphaned infrastructure.

References:

* [Terraform Workspaces](https://www.terraform.io/docs/cli/concepts/workspaces.html)
* [AzureRM Backend](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/state)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/0eb3275a-a37d-45a5-86b5-4920e2e44e7c/lesson/6ec19685-743e-4758-a830-969e3dedb58b" />
</CardGroup>


# Defining Variables

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Variables/Defining-Variables/page

Explains declaring and using Terraform input variables to avoid hardcoding, enable reusable environment-agnostic configurations, and manage values securely through defaults, environment variables, tfvars, or CLI flags

This lesson explains how to define and use input variables in Terraform to make your configurations reusable and environment-agnostic.

Defining variables means declaring named inputs that Terraform configuration can reference instead of hardcoded values. Variables act as parameters, enabling the same Terraform code to be reused across environments (dev, staging, prod) by changing only the input values.

Hardcoded resource example
Below is an Azure Storage Account resource where key configuration values are hardcoded directly in the resource block. This will deploy successfully, but it tightly couples the resource to a single name, region, and resource group. Any change (for example, deploying to a different region) requires editing the Terraform code.

```hcl theme={null}
resource "azurerm_storage_account" "storage" {
  name                     = "satfworshop46536"
  location                 = "East US"
  resource_group_name      = "my-workshop-eus-rg"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

Why this is brittle

* Hardcoded values prevent easy reuse across environments.
* Editing multiple resource blocks for a simple change is error-prone.
* Sharing or versioning configurations becomes harder.

Use variables to decouple values from resource blocks and centralize configuration.

Declaring and using variables
Create input variables in a `variables.tf` file and reference them using `var.<name>` from your resource files (`main.tf`, etc.).

Variables declaration (`variables.tf`):

```hcl theme={null}
