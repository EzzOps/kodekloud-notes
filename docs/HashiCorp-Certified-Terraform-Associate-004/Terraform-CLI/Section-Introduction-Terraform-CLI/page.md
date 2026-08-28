# Section Introduction Terraform CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-CLI/Section-Introduction-Terraform-CLI/page

Overview of Terraform CLI commands, workflow, and best practices for managing infrastructure as code, state, and safe change application across providers and environments.

Welcome to the Terraform CLI overview.

The Terraform command-line interface (CLI) is the core tool for defining, provisioning, and managing infrastructure as code. It provides a consistent, provider-agnostic set of commands that work with AWS, Azure, GCP, on-premises systems, and many third-party services. Because the CLI workflow is the same across providers and operating systems (Linux, Windows, macOS), teams can adopt Terraform more quickly and reduce operational friction.

This section introduces the essential Terraform commands you will use to create, review, and safely apply infrastructure changes. You’ll learn how these commands interact with one another, when to use each, and how they help you maintain predictable, repeatable infrastructure states.

<Frame>
  <img alt="The image shows a person speaking, with text saying &#x22;Using the Terraform CLI&#x22; on a purple background, suggesting it is a lecture on the topic." />
</Frame>

Core objectives covered in this section:

* Understand the Terraform CLI workflow from initialization to destruction.
* Learn the purpose and typical usage of core commands: `init`, `validate`, `plan`, `apply`, `destroy`, and state management commands.
* Learn best practices for safely reviewing and applying changes, managing remote state, and working with modules and workspaces.

<Callout icon="lightbulb">
  Tip: Treat the CLI as your single source of truth for executing infrastructure changes. Combine careful use of `terraform plan` with remote state locking to avoid race conditions in team environments.
</Callout>

Essential Terraform CLI commands and their primary use cases:

|                       Command | Purpose                                                                                                     | Typical example                                             |
| ----------------------------: | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
|              `terraform init` | Initialize a working directory, download providers and modules, and configure the backend.                  | `terraform init`                                            |
|          `terraform validate` | Validate configuration syntax and internal consistency.                                                     | `terraform validate`                                        |
|               `terraform fmt` | Reformat configuration files to canonical style.                                                            | `terraform fmt`                                             |
|              `terraform plan` | Create an execution plan showing proposed changes without applying them.                                    | `terraform plan -out=plan.tfplan`                           |
|             `terraform apply` | Apply the changes required to reach the desired state. Accepts a saved plan: `terraform apply plan.tfplan`. | `terraform apply`                                           |
|           `terraform destroy` | Destroy all resources defined in the configuration.                                                         | `terraform destroy`                                         |
|             `terraform state` | Inspect and modify the Terraform state. Useful for advanced state corrections.                              | `terraform state list`                                      |
|            `terraform output` | Read outputs from the state.                                                                                | `terraform output -json`                                    |
|            `terraform import` | Import existing resources into state.                                                                       | `terraform import aws_instance.example i-1234567890abcdef0` |
| `terraform taint` / `untaint` | Mark/unmark resources for recreation on next apply (legacy; prefer `terraform apply -replace`).             | `terraform taint aws_instance.example`                      |

<Callout icon="warning">
  Warning: Avoid editing the Terraform state file directly. Use `terraform state` subcommands or remote state features (backends) to prevent corruption and ensure team safety.
</Callout>

Recommended CLI workflow (typical sequence):

1. `terraform init` — set up the directory and backend.
2. `terraform validate` and `terraform fmt` — ensure configuration quality.
3. `terraform plan -out=plan.tfplan` — generate a reviewable plan.
4. Review the plan carefully, then `terraform apply plan.tfplan` — apply changes.
5. Use `terraform output` to retrieve values and `terraform state` to inspect state as needed.
6. When decommissioning resources, use `terraform destroy` with caution.

Further reading and references:

* Terraform Documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* CLI Commands Reference: [https://www.terraform.io/cli](https://www.terraform.io/cli)
* State Management: [https://www.terraform.io/language/state](https://www.terraform.io/language/state)

With this overview, you’re ready to dive into each command in detail. Next, we’ll look at how to initialize projects and configure backends for secure remote state management.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/35cbc795-57ed-4af7-88c8-c9323af9294d/lesson/d404ab90-44cf-430f-9230-694be44070fb" />
</CardGroup>
