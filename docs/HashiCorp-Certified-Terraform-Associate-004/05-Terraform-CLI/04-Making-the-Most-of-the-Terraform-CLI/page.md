# terraform destroy
```

Note: Running `terraform plan` before `terraform apply` is a best practice—it lets you review changes and avoids surprises.

<Callout icon="warning">
  Be careful with `terraform destroy`. It will remove infrastructure managed by Terraform. Confirm that you really intend to destroy resources before typing `yes`.
</Callout>

## Core CLI commands — quick reference

Below are the most commonly used Terraform subcommands with a short description and example usage.

| Command              | Purpose                                                     | Example                                            |
| -------------------- | ----------------------------------------------------------- | -------------------------------------------------- |
| `terraform init`     | Initialize a working directory and download providers.      | `terraform init`                                   |
| `terraform fmt`      | Format configuration files.                                 | `terraform fmt`                                    |
| `terraform validate` | Validate configuration for syntax and internal consistency. | `terraform validate`                               |
| `terraform plan`     | Generate and display an execution plan.                     | `terraform plan -out=planfile`                     |
| `terraform apply`    | Execute changes to reach the desired state.                 | `terraform apply`                                  |
| `terraform destroy`  | Destroy remote resources managed by a configuration.        | `terraform destroy`                                |
| `terraform state`    | Inspect and modify the state file.                          | `terraform state list`                             |
| `terraform show`     | Show state or saved plan details.                           | `terraform show planfile`                          |
| `terraform import`   | Import existing resources into state.                       | `terraform import aws_instance.example i-12345678` |

This list is not exhaustive but covers the commands most teams use daily.

<Frame>
  <img alt="The image lists various Terraform subcommands, with some checked off, such as &#x22;apply,&#x22; &#x22;init,&#x22; &#x22;destroy,&#x22; &#x22;validate,&#x22; and &#x22;version.&#x22; It also notes that this is not an exhaustive list." />
</Frame>

## Additional commonly used subcommands

Beyond the core workflow, Terraform includes powerful subcommands for state management, debugging, and advanced operations:

* `terraform state` — inspect and manually modify state objects (use carefully).
* `terraform show` — display state or plan details in a human-readable format.
* `terraform import` — bring existing external resources under Terraform management.
* `terraform fmt` and `terraform validate` — help enforce configuration quality and consistency.

## Environment variables

Environment variables are a secure, convenient way to provide credentials, configure Terraform behavior, and set input variables without embedding secrets in `.tf` files.

Why use environment variables?

* Avoid committing credentials into version control.
* Provide defaults or overrides for variables in CI/CD pipelines.
* Control logging and runtime behavior for debugging.

Common environment variables:

* `TF_LOG` — set Terraform logging level (`TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`). Useful for troubleshooting.
* `TF_VAR_<name>` — set Terraform input variables from the environment. For example:
  ```bash theme={null}
  export TF_VAR_server_name="prod-db-01"
  ```
  A configuration referencing `var.server_name` will pick up this value.
* Provider-specific variables — many providers support environment-based credentials (for example AWS or Azure environment variables). Terraform checks multiple sources for credentials, including environment variables and credential helpers.

Example combined environment setup:

```bash theme={null}
export TF_LOG=DEBUG
export TF_VAR_server_name="prod-db-01"
export AWS_ACCESS_KEY_ID="EXAMPLEACCESSKEY"
export AWS_SECRET_ACCESS_KEY="EXAMPLESECRETKEY"
```

<Callout icon="lightbulb">
  Use environment variables for credentials and sensitive values instead of hardcoding them into `.tf` files to reduce the risk of accidentally committing secrets.
</Callout>

## Best practices and tips

* Always run `terraform fmt` and `terraform validate` before committing changes.
* Use `terraform plan -out=planfile` and `terraform apply planfile` to ensure the exact planned changes are applied.
* Store state securely (remote backends like S3 with locking via DynamoDB, or HashiCorp Consul, are recommended for team workflows).
* Use workspaces, modules, and variable files to organize environments and reusable components.
* Limit the use of `terraform state` commands; prefer importing and re-creating resources through configuration when possible.

## Links and references

* Terraform documentation: [https://www.terraform.io/docs](https://www.terraform.io/docs)
* Terraform CLI reference: [https://www.terraform.io/cli](https://www.terraform.io/cli)
* State and backends: [https://www.terraform.io/language/state](https://www.terraform.io/language/state)

Wrapping up

You now have a concise, practical overview of the Terraform CLI: its command structure, mapped workflow, useful subcommands, and secure use of environment variables. In later sections you can explore advanced topics like remote state backends, workspaces, custom providers, and automation patterns for CI/CD.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/35cbc795-57ed-4af7-88c8-c9323af9294d/lesson/b6d18b73-a1cc-4a58-b6d7-90cf07a6dd27" />
</CardGroup>


# Making the Most of the Terraform CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-CLI/Making-the-Most-of-the-Terraform-CLI/page

Guide to Terraform CLI productivity features, enabling autocomplete, using built-in help, and formatting configurations with terraform fmt to improve speed, accuracy, and consistent style.

Terraform includes several built-in CLI conveniences—autocomplete, comprehensive help, and automatic formatting—that help you stay productive without leaving your terminal. This guide walks through enabling and using these features so you can discover commands, reduce typos, and keep configuration style consistent.

## Autocomplete: speed up typing and reduce errors

Shell autocomplete lets your shell predict and complete Terraform commands, subcommands, flags, and file paths as you type. If you already have shell completion enabled, this is a quick review. If not, enabling it consolidates useful CLI ergonomics in one place.

<Frame>
  <img alt="The image is a promotional graphic for using auto-complete with the Terraform CLI, explaining that tab completion aids in filling subcommands, flags, and file paths by pressing the Tab key. It features geometric lines and logos on a dark background." />
</Frame>

Install autocomplete for your shell with:

```bash theme={null}
$ terraform -install-autocomplete
```

If your shell configuration file does not exist, create it first (example for bash):

```bash theme={null}
$ touch ~/.bashrc
$ terraform -install-autocomplete
```

<Callout icon="lightbulb">
  After installing autocomplete, reload your shell configuration (for example, `source ~/.bashrc` or `source ~/.zshrc`) or restart the terminal to activate completion.
</Callout>

Usage example: type a partial command then press Tab. Typing `terraform s` and pressing Tab will present matching subcommands:

```bash theme={null}
$ terraform s<TAB>
show    state
```

Autocomplete is especially helpful for remembering long flag names, provider-specific subcommands, and relative file paths.

## Built-in help: discover commands and flags

Terraform ships contextual help at both the global and subcommand levels. Use `--help` to view available commands, flags, and short explanations without leaving your terminal.

Global overview:

```bash theme={null}
$ terraform --help
Usage: terraform [global options] <subcommand> [args]

The available commands for execution are listed below.
The primary workflow commands are given first, followed by
less common or more advanced commands.

Main commands:
  init      Prepare your working directory for other commands
  validate  Check whether the configuration is valid
  plan      Show changes required by the current configuration
  apply     Create or update infrastructure
  destroy   Destroy previously-created infrastructure
  ...
```

Per-command help provides detailed flag descriptions and usage examples. For example:

```bash theme={null}
$ terraform plan --help
Usage: terraform [global options] plan [options]

Generates a speculative execution plan, showing what actions Terraform
would take to apply the current configuration. This command will not
actually perform the planned actions.

You can optionally save the plan to a file, which you can then pass to
the "apply" command to perform exactly the actions described in the plan.

Plan Customization Options:
  -destroy        Select the "destroy" planning mode, which creates a plan
                  to destroy all objects currently managed by this
                  configuration.
  ...
```

Use per-command help whenever you need to confirm a flag name, understand an option’s effect, or find switches for advanced behavior.

<Callout icon="lightbulb">
  For extended guides, examples, and tutorials, see the official Terraform documentation: [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform).
</Callout>

## Formatting with terraform fmt

Consistent formatting improves readability and reduces diffs in commits. `terraform fmt` rewrites Terraform configuration files to the canonical style.

Example of a compact resource before formatting:

```hcl theme={null}
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  tags = { Name = "example" }
}
```

Run `terraform fmt` in the working directory:

```bash theme={null}
$ terraform fmt
```

To format files in subdirectories as well, use the recursive flag:

```bash theme={null}
$ terraform fmt -recursive
```

Notes:

* By default, `terraform fmt` processes files in the current directory only.
* Add `-recursive` to traverse and format nested directories.

## Quick command reference

|                           Command | Purpose                                                | Example                           |
| --------------------------------: | ------------------------------------------------------ | --------------------------------- |
| `terraform -install-autocomplete` | Enable shell autocomplete for Terraform                | `terraform -install-autocomplete` |
|                `terraform --help` | Show global command list and usage                     | `terraform --help`                |
|   `terraform <subcommand> --help` | Show options for a specific subcommand                 | `terraform plan --help`           |
|                   `terraform fmt` | Reformat configuration files in current directory      | `terraform fmt`                   |
|        `terraform fmt -recursive` | Reformat files in current directory and subdirectories | `terraform fmt -recursive`        |

## Summary

* Enable autocomplete with `terraform -install-autocomplete` to speed up typing and reduce errors.
* Use `terraform --help` and `terraform <subcommand> --help` for quick, contextual CLI documentation.
* Keep Terraform code consistent with `terraform fmt`; add `-recursive` to format nested directories.

These built-in tools make it easy to discover commands, confirm flag behavior, and maintain consistent configuration style—all without leaving your terminal.

## Links and references

* Official Terraform documentation: [https://developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/35cbc795-57ed-4af7-88c8-c9323af9294d/lesson/e6fcea39-8d6d-486e-8704-4853d693ad27" />
</CardGroup>
