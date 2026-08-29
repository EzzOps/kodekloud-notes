# Terraform Providers and Graph

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-CLI/Terraform-Providers-and-Graph/page

Explains using terraform providers and terraform graph to inspect provider usage and visualize Terraform's dependency graph for debugging and troubleshooting resource ordering and provider issues.

In this lesson we go beyond basic CLI validation and inspection and explore how Terraform discovers providers and constructs its internal dependency graph (DAG). Understanding these diagnostics helps you debug provider mismatches, orphaned state references, and complex dependency relationships that affect execution order and parallelism.

Key diagnostics covered:

* `terraform providers` — lists provider dependencies discovered from configuration and state.
* `terraform graph` — prints Terraform's internal dependency graph in DOT format (renderable with Graphviz).

Below is a simple example configuration used throughout this article:

```hcl theme={null}
resource "azurerm_storage_account" "example" {
  name                          = var.storage_account_name
  location                      = "East US"
  resource_group_name           = "my-workshop-eus-rg"
  account_tier                  = "Standard"
  account_replication_type      = "LRS"
  public_network_access_enabled = false
}
```

## terraform providers

The `terraform providers` command summarizes provider usage in two places:

* Providers required by configuration — inferred from your `.tf` files and the resource types used.
* Providers required by state — referenced in the current state file (this can include providers removed from the configuration after refactors).

Example output:

```bash theme={null}
$ terraform providers
Providers required by configuration:
└── provider[registry.terraform.io/hashicorp/azurerm]

Providers required by state:
└── provider[registry.terraform.io/hashicorp/azurerm]
```

Why this matters

* The configuration section shows which providers Terraform will attempt to install for your current `.tf` files.
* The state section reveals providers still referenced by state, which helps detect orphaned provider references after refactoring or manual edits.
* Use this command to troubleshoot provider version/source issues (registry vs private mirror), confirm provider sources, and verify policy compliance in enterprise setups.

> **lightbulb** Run `terraform init` before `terraform providers` if you need Terraform to install or upgrade provider plugins. This command is also helpful when you want to confirm the provider set after a module refactor or a provider source change.

Quick reference: commands and purpose

| Command               | Purpose                                              | Example                                    |
| --------------------- | ---------------------------------------------------- | ------------------------------------------ |
| `terraform providers` | List providers referenced by configuration and state | `terraform providers`                      |
| `terraform graph`     | Output the internal dependency graph in DOT format   | `terraform graph \| dot -Tpng > graph.png` |

## terraform graph

Before planning or applying, Terraform builds a directed acyclic graph (DAG) of resources, providers, variables, outputs, and their dependency relationships. The DAG determines create/destroy order and identifies opportunities for parallel execution.

Terraform can output this DAG in DOT format. To render it as an image, pipe the output to Graphviz's `dot` tool:

```bash theme={null}
$ terraform graph | dot -Tpng > sa.png
```

Note: Graphviz must be installed for `dot` to be available.

> **lightbulb** Install Graphviz to render DOT output to PNG or other formats (for example: `brew install graphviz` on macOS or `apt-get install graphviz` on Debian/Ubuntu). See the Graphviz downloads page: [https://graphviz.org/download/](https://graphviz.org/download/)

What the generated graph shows

* Provider nodes (e.g., the AzureRM provider).
* Resource nodes (e.g., `azurerm_storage_account.example`).
* Inputs referenced by resources (e.g., `var.storage_account_name`).
* Outputs that depend on resources.
* Explicit `depends_on` relationships that you declared.

These relationships drive execution sequencing: a resource implicitly depends on its provider and on any inputs it references; outputs depend on resources they read. Explicit `depends_on` entries will appear and enforce ordering where needed.

When to use `terraform graph`

* Debug complex module interactions and implicit dependencies.
* Diagnose circular dependency errors by visualizing connections.
* Optimize parallelism or add explicit dependencies to control ordering.
* Produce architecture diagrams for documentation or review.

## Putting it together

* Use `terraform providers` to confirm the set of providers required by your configuration and the state—especially after refactors or provider upgrades.
* Use `terraform graph` (and Graphviz) to visualize Terraform’s DAG, reason about ordering, and troubleshoot dependency issues.

These tools aren’t required for everyday changes, but they are indispensable when troubleshooting complex infrastructure, unexpected dependency behaviors, or provider-related issues.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/a87fc0ec-6ef6-409e-91cb-709bdcebb9eb/lesson/38e840a4-7cc5-456f-84f3-e2b200457e52)
