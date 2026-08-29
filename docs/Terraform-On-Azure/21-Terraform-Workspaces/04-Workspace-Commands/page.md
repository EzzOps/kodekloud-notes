# list available workspaces
terraform workspace list
```

```bash theme={null}
# create a new workspace called 'dev' and switch to it
terraform workspace new dev
```

```bash theme={null}
# switch to an existing workspace named 'dev'
terraform workspace select dev
```

```bash theme={null}
# show the currently active workspace
terraform workspace show
```

```bash theme={null}
# delete the workspace named 'dev' (cannot be the active workspace)
terraform workspace delete dev
```

Example session

```bash theme={null}
# create and switch to a new workspace called 'dev'
terraform workspace new dev
# verify active workspace
terraform workspace show
# switch back to default
terraform workspace select default
# output: Switched to workspace "default".
```

Notes about backends and remote state

* Remote backends typically store workspace-specific state using distinct keys or namespaces, so workspaces are compatible with many remote backends. Backend implementations (for example, Amazon S3 or Consul) may differ in how they manage workspace-related keys.
* Understand your backend's semantics before relying on local CLI workspaces for production separation. For example, some hosted platforms treat the workspace concept as a first-class entity and map workspaces to repositories or configurations differently.
* Further reading:
  * Amazon S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
  * Consul: [https://www.consul.io/](https://www.consul.io/)
  * Terraform Cloud & Enterprise: [https://www.terraform.io/docs/cloud/](https://www.terraform.io/docs/cloud/)

Key takeaways

* Workspaces isolate state, not configuration. Use them when multiple environments share the same infrastructure design.
* They are ideal for light-weight separation: experiments, feature branches, and temporary environments.
* For long-term divergent environments (different resources or lifecycle requirements), prefer separate configurations or dedicated backends.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/0eb3275a-a37d-45a5-86b5-4920e2e44e7c/lesson/cdb9db53-f3d1-4f45-ad6e-635c10a65634" />
</CardGroup>


# Workspace Commands

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Workspaces/Workspace-Commands/page

Explains Terraform workspaces, their commands and AzureRM backend behavior, how workspaces isolate state, manage multiple environments, and best practices for creating, switching, and deleting workspaces

This section explains Terraform workspaces — the built-in mechanism for managing multiple independent state instances from a single configuration. Workspaces let you isolate state (for example: `dev`, `prod`) while keeping the same Terraform code.

Below is the high-level `terraform workspace` usage and available subcommands:

```bash theme={null}
$ terraform workspace
Usage: terraform [global options] workspace

new, list, show, select and delete Terraform workspaces.

Subcommands:
  delete    Delete a workspace
  list      List Workspaces
  new       Create a new workspace
  select    Select a workspace
  show      Show the name of the current workspace
```

## Workspace subcommands (quick reference)

|  Command | Purpose                                                          | Example                           |
| -------: | ---------------------------------------------------------------- | --------------------------------- |
|   `list` | Show all workspaces for the current configuration/backend        | `terraform workspace list`        |
|   `show` | Print the currently-active workspace name                        | `terraform workspace show`        |
|    `new` | Create a new workspace and switch to it (creates an empty state) | `terraform workspace new dev`     |
| `select` | Switch the active workspace                                      | `terraform workspace select prod` |
| `delete` | Remove a workspace (only if empty, or use `-force`)              | `terraform workspace delete dev`  |

## How workspaces affect state and configuration

* Workspaces isolate state files but reuse the same configuration files.
* The active workspace determines which state Terraform reads from and writes to during `plan` and `apply`.
* Use the built-in expression `terraform.workspace` inside your configuration to adapt resource names or logic by workspace.

<Callout icon="lightbulb">
  Do not expect Terraform to substitute variables into a backend block during `terraform init`. Backend configuration is evaluated before variable values are applied. If you need workspace-specific backends you must configure them explicitly or use automation outside of Terraform init.
</Callout>

***

## Example: AzureRM provider and single-file demo

Below is a compact example used for the demo. In production you should split provider, variables, resources, and backend into separate files.

```hcl theme={null}
provider "azurerm" {
  features {}
  subscription_id = "1b228746-75fd-46ed-8a6b-6a906d6d3a3"
}

variable "environment" {
  type    = string
  default = "dev"
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.environment}-01"
  location = "West US"
}

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-state-refresh-demo"
    storage_account_name = "ststatereshdemo"
    container_name       = "statecontainer"
    key                  = "workspace.tfstate"
  }
}
```

<Frame>
  <img alt="The image shows a Visual Studio Code editor window with a Terraform configuration file open, displaying a directory structure on the left sidebar and a suggestion for &#x22;required-providers&#x22; under the &#x22;provider&#x22; keyword." />
</Frame>

Notes about the example:

* The `environment` variable is used to name the resource group.
* The backend block shown above is static — variables are not expanded at `terraform init` time.
* The `key` value determines the root state object name in the remote backend; Terraform will append workspace identifiers to that key when using workspaces (see below).

## Initialize the backend

After creating your configuration, run:

```bash theme={null}
terraform init
```

Typical simplified output:

```bash theme={null}
Acquiring state lock. This may take a few moments...

Successfully configured the backend "azurerm"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Finding latest version of hashicorp/azurerm...
- Installing hashicorp/azurerm v4.59.0...
```

## Working with workspaces (common workflow)

1. List existing workspaces:

```bash theme={null}
terraform workspace list
```

Output example:

```bash theme={null}
* default
```

2. Create and switch to a new workspace:

```bash theme={null}
terraform workspace new dev
```

Output:

```bash theme={null}
Created and switched to workspace "dev"!
```

You're now on a new, empty workspace. Workspaces isolate their state, so if you run "terraform plan" Terraform will not see any existing state for this configuration.

3. Plan and apply for the workspace (supply variable values as needed):

```bash theme={null}
terraform plan -var="environment=dev"
terraform apply -var="environment=dev"
```

Repeat for a production workspace:

```bash theme={null}
terraform workspace new prod
terraform workspace list
