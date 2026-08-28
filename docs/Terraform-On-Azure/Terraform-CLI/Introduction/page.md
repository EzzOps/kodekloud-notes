# Verify Azure CLI
az --version

# Verify Terraform CLI
terraform version

# Verify VS Code (if installed)
code --version
```

If any command fails, follow the corresponding installation guide linked above and re-run the verification commands.

## Authenticate to Azure

After installing the Azure CLI, authenticate so Terraform can operate against your Azure subscription. Common authentication methods include:

* Interactive login (local development):

```bash theme={null}
az login
```

* Service principal (recommended for automation / CI pipelines):

```bash theme={null}
az ad sp create-for-rbac --name "tf-sp-automation" --role Contributor --scopes /subscriptions/<SUBSCRIPTION_ID>
# This command prints the appId, password, tenant - store these securely as pipeline secrets
```

* Managed identity (when Terraform runs from Azure-hosted compute)

<Callout icon="lightbulb">
  Common authentication options include interactive `az login` for local development, a service principal for automated pipelines, and managed identities when running from Azure-hosted compute.
</Callout>

Choose the method that matches your workflow and security requirements. For CI/CD, use a service principal with least-privilege role assignments and store credentials in your pipeline secret store.

## Quick Terraform workflow

Once tools are installed and authentication is configured, the typical Terraform workflow for Azure is:

1. Write HCL configuration files (.tf)
2. Initialize the working directory:

```bash theme={null}
terraform init
```

3. Preview changes:

```bash theme={null}
terraform plan -out=tfplan
```

4. Apply changes:

```bash theme={null}
terraform apply "tfplan"
```

Use `terraform validate` and `terraform fmt` to ensure code quality before planning and applying.

## Next steps

With your environment configured and authentication in place, proceed to create a simple Terraform configuration that provisions a resource group and a storage account. Refer to the official Terraform Azure Provider documentation for resource examples and provider configuration:

* [Terraform Azure Provider docs](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])
* [Azure CLI documentation](https://learn.microsoft.com/cli/azure/)

This prepares you for the hands-on modules where we’ll initialize a Terraform project, configure the AzureRM provider, and deploy basic infrastructure.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/db2adc19-fa48-4b03-9d9a-8ef71c4c28db/lesson/869116c0-840a-47cd-88cd-e91431d2016e" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-CLI/Introduction/page

Guide to commonly used Terraform CLI commands for validating, formatting, planning, inspecting state, visualizing dependencies, managing providers, and importing existing resources into state.

Terraform CLI is the primary operational interface for Terraform—every lifecycle action (validate, plan, apply, inspect, and manage state) is executed through CLI commands. This guide covers additional, commonly used Terraform CLI commands beyond the basics, organized to match a typical workflow:

1. Validation and formatting
2. Reviewing deployed resources and exported values
3. Inspecting provider usage and visualizing resource dependencies
4. Inspecting and reconciling state
5. Importing existing resources into your Terraform state

We’ll follow this sequence and show the purpose, typical usage, and helpful flags for each command.

For the canonical Terraform documentation and version-specific details, see the official Terraform docs: [https://www.terraform.io/docs](https://www.terraform.io/docs)

## Quick reference table

| Task                    | Command / Example                                             | Purpose                                                        |
| ----------------------- | ------------------------------------------------------------- | -------------------------------------------------------------- |
| Validate configuration  | `terraform validate`                                          | Check syntactic and semantic correctness of your configuration |
| Format files            | `terraform fmt -recursive`                                    | Reformat files to a canonical style                            |
| Create & inspect plan   | `terraform plan -out=plan.out`<br />`terraform show plan.out` | Save a plan to file and inspect it                             |
| Show state              | `terraform show`                                              | Print current state in human-readable form                     |
| List outputs            | `terraform output`                                            | Print values defined by `output` blocks                        |
| List providers          | `terraform providers`                                         | Show providers referenced by configuration                     |
| Create dependency graph | `terraform graph`                                             | Produce DOT-format graph for resource relationships            |
| List state resources    | `terraform state list`                                        | Enumerate resources tracked in state                           |
| Show state resource     | `terraform state show <ADDRESS>`                              | Display attributes for one resource in state                   |
| Pull remote state       | `terraform state pull`                                        | Retrieve raw state file from remote backend                    |
| Refresh state (preview) | `terraform plan -refresh-only`                                | Reconcile state with real-world resources and preview changes  |
| Import resource         | `terraform import <ADDRESS> <ID>`                             | Add an existing resource into Terraform state                  |

## 1. Validation and formatting

Before creating a plan or applying changes, validate your configuration to catch errors early and format files to a consistent style.

* Validate configuration correctness:

```bash theme={null}
terraform validate
```

* Format files recursively to the standard style:

```bash theme={null}
terraform fmt -recursive
```

Run `terraform fmt` and `terraform validate` in CI pipelines and pre-commit hooks to ensure consistent formatting and to detect configuration issues before they reach shared environments.

<Callout icon="lightbulb">
  Run `terraform fmt` and `terraform validate` from the root of your configuration directory so they operate across the entire workspace. Integrating these commands into CI or a pre-commit hook reduces diff noise and catches mistakes early.
</Callout>

## 2. Reviewing deployed resources and exported values

After you create a plan or have state, use `terraform show` to inspect it and `terraform output` to read exported values.

* Create a plan and save it to a file for later inspection:

```bash theme={null}
terraform plan -out=plan.out
```

* Show a saved plan:

```bash theme={null}
terraform show plan.out
```

* Show the current state in a human-friendly format:

```bash theme={null}
terraform show
```

* Read outputs:
  * List all outputs:
  ```bash theme={null}
  terraform output
  ```
  * Get a single output value:
  ```bash theme={null}
  terraform output <NAME>
  ```
  * Get outputs in JSON (machine-readable) form:
  ```bash theme={null}
  terraform output -json
  ```

Use `terraform show` when you need to inspect the contents of a saved plan or the in-memory plan after `terraform plan`. Use `terraform output` to expose configured `output` blocks to external systems (CI scripts, other tooling) and prefer `-json` for automation.

## 3. Providers and graph

Discover which providers your configuration references and visualize resource dependency relationships.

* List providers referenced by the configuration:

```bash theme={null}
terraform providers
```

This command helps you locate provider addresses (for example `registry.terraform.io/hashicorp/aws`) and see which modules consume them.

* Generate a dependency graph (Graphviz required to render the output):

```bash theme={null}
terraform graph | dot -Tpng -o graph.png
```

`terraform graph` outputs DOT format describing relationships between resources and modules. Piping to `dot` (part of Graphviz) produces a visual diagram you can inspect to understand resource dependencies and module boundaries.

Tip: Large graphs can be noisy—filter or focus on modules to make diagrams actionable.

## 4. State and refresh

Terraform’s state commands let you inspect and manage the state file. Because state is authoritative for Terraform-managed resources, operate on it carefully and always back up before making destructive changes.

* List resources tracked in the state:

```bash theme={null}
terraform state list
```

* Show a specific state resource’s attributes:

```bash theme={null}
terraform state show <ADDRESS>
```

* Pull the remote state contents (raw JSON):

```bash theme={null}
terraform state pull
```

* Refresh the state by reconciling Terraform state with real-world infrastructure and preview differences:

```bash theme={null}
terraform plan -refresh-only
```

Note: Older Terraform versions included a `terraform refresh` command to update state in place; current workflows commonly prefer `terraform plan -refresh-only` to preview changes before applying them.

When changing state directly (for example using `terraform state mv`, `terraform state rm`, or manual edits), always make a backup of the state file or rely on backend versioning.

<Callout icon="warning">
  Be cautious when manipulating state directly. Always back up your state (or enable backend versioning) before performing state modifications such as `terraform state rm` or `terraform state mv`. Mistakes in state can lead to resource drift or accidental destruction.
</Callout>

## 5. Importing existing resources

If you have existing infrastructure created outside Terraform, import it into a Terraform state and then author the matching configuration blocks.

* Basic import syntax:

```bash theme={null}
terraform import <ADDRESS> <ID>
```

* Example (import an AWS EC2 instance):

```bash theme={null}
terraform import aws_instance.example i-1234567890abcdef0
```

After running `terraform import`, Terraform adds the resource and its attributes to the state, but you must create a corresponding `resource` block in your `.tf` files that matches the imported resource. Run `terraform plan` afterwards to identify any attribute or configuration gaps, then update your configuration to align with the imported state.

Tips for importing:

* Write the resource block first (with the same resource type and name) so the import has a clear address.
* For complex resources, consider importing smaller logical pieces first (for example, security groups or IAM roles) and then grouping them.
* Use `terraform state show <ADDRESS>` to inspect attributes after import.

***

This lesson outlined additional Terraform CLI commands used to validate and standardize configurations, inspect and export values, explore providers and dependency graphs, manage and reconcile state, and import existing resources. Incorporate these commands into a disciplined workflow—local checks, CI validation, and careful state management—to keep your infrastructure-as-code reliable and maintainable.

Links and references:

* Terraform documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* Terraform CLI reference: [https://www.terraform.io/cli](https://www.terraform.io/cli)
* Graphviz: [https://graphviz.org/](https://graphviz.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/a87fc0ec-6ef6-409e-91cb-709bdcebb9eb/lesson/24376e48-7a91-47fe-84d6-f47a33552ae5" />
</CardGroup>
