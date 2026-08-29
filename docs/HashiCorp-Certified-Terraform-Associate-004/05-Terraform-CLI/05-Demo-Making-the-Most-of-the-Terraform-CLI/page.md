# Example terraform plan output
-/+ google_sql_database_instance.prd_db_2
  - resource will be destroyed
```

That would delete production data — which you must avoid. The goal is to make Terraform "forget" the resource (remove it from state) while leaving the actual database intact. The `removed` block provides a safer, declarative way to do this.

What the `removed` block does

* Removes the specified resource address from Terraform state so Terraform stops managing it.
* Leaves the actual infrastructure running and untouched.
* Is useful for handing resources off to other teams, transitioning to manual management, or splitting a monolithic configuration.

Core pieces to know

* `from` — specifies the resource address to remove from state. Use the resource address exactly as it appears in configuration (for example, `google_sql_database_instance.prd_db_2`).
* `removed` blocks only need the `from` argument. They instruct Terraform to remove the matching resource from state without destroying the underlying infrastructure.
* Always validate behavior in your Terraform version and provider. See HashiCorp's refactoring docs for details: [https://developer.hashicorp.com/terraform/language/state/refactoring](https://developer.hashicorp.com/terraform/language/state/refactoring)

Example `removed` blocks for the two databases:

```hcl theme={null}
removed {
  from = google_sql_database_instance.prd_db_1
}

removed {
  from = google_sql_database_instance.prd_db_2
}
```

> **lightbulb** When using a `removed` block, the resource definition must be absent (or commented out) from your configuration first. Terraform will refuse to remove a resource from state if that resource still exists in code.

Important ordering and workflow
The sequence of steps matters. If you keep the resource block in code while also declaring a `removed` block for it, Terraform will be unable to reconcile them. Follow this workflow:

1. Delete or comment out the resource blocks you want Terraform to stop managing.
2. Add a `removed` block for each resource to be forgotten.
3. Run `terraform plan` to inspect the proposed state change.
4. Run `terraform apply` to update the state file and remove the resource from Terraform state.
5. After the state is updated, delete the temporary `removed` blocks from your configuration (they are not required after apply but can be kept for documentation).

Example commands:

```bash theme={null}
# Inspect changes (safe)
terraform plan

# Apply the state-only changes
terraform apply
```

The typical refactoring lifecycle is:
Delete (resource block) → Write (`removed`/`moved` block) → Plan → Apply → Delete (temporary scaffolding).

<Frame>
  <img alt="The image illustrates a refactoring workflow consisting of five steps: Write, Delete, Plan, Apply, and Delete, each with corresponding actions related to Terraform configuration." />
</Frame>

`removed` vs `moved` — quick guidance

* Use `moved` when refactoring addresses within Terraform (renaming resources, moving to modules, etc.). `moved` updates state to reflect a change in resource address while leaving infrastructure intact.
* Use `removed` when you want Terraform to stop managing a resource entirely (hand-off to another team, manual management, or transferring to another state/workspace). `removed` deletes the resource from state without deleting the actual infrastructure.

Comparison table

| Action                                                  | Use case                                          | Terraform block             | Result                                                                          |
| ------------------------------------------------------- | ------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------- |
| Rename or re-address resource                           | Refactoring code, moving resources into modules   | `moved`                     | State updated to new addresses; infrastructure unchanged                        |
| Stop Terraform management / hand off resource           | Transferring ownership; manual management         | `removed`                   | Resource removed from state; infrastructure unchanged                           |
| Remove resource from configuration without state change | Temporary removal from config while still managed | None (use careful planning) | Terraform will propose to delete resource unless you remove it from state first |

<Frame>
  <img alt="The image compares the differences between a &#x22;moved block&#x22; and a &#x22;removed block&#x22; in the context of code management, highlighting the implications of each action." />
</Frame>

Real-world use cases

* Hand off resources to another team: remove them from your state so another team can import them into theirs.
* Migration from another IaC tool: import resources into Terraform and `removed` or `moved` as part of a staged migration.
* Split monolithic configurations or separate environments: remove resources from one state and import them into another workspace or project.

Decision guidance diagram

* If you are renaming or reorganizing within Terraform → use `moved`.
* If you are transferring ownership or stopping Terraform management → use `removed`.
* Migration scenarios often combine `import` with `removed`/`moved` actions depending on the direction of transfer.

<Frame>
  <img alt="The image is a decision tree on a purple background, detailing how to select the appropriate block for Terraform tasks such as renaming resources or handing off to another team." />
</Frame>

Warnings and best practices

> **warning** Do not leave a resource block in your configuration while also declaring a `removed` block for the same address. Terraform will not be able to reconcile them and the operation will fail. Always test `removed` workflows in non-production environments first.

Final notes and references

* The `removed` block is a powerful, but intentionally infrequent, tool. Use it when you need Terraform to forget a resource while keeping the physical resource intact.
* Practice this workflow in a safe environment and double-check behavior for your Terraform version and provider.

Useful links

* Terraform state refactoring: [https://developer.hashicorp.com/terraform/language/state/refactoring](https://developer.hashicorp.com/terraform/language/state/refactoring)
* Terraform state commands overview: [https://developer.hashicorp.com/terraform/cli/commands/state](https://developer.hashicorp.com/terraform/cli/commands/state)

That wraps up this lesson on the `removed` block. Use it when you need Terraform to stop tracking a resource without deleting the actual infrastructure.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/42da48a6-09fe-43c7-997f-255cdb3e0c80/lesson/a0235061-b411-492a-98d9-5e9202ac8e23)


# Demo Making the Most of the Terraform CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-CLI/Demo-Making-the-Most-of-the-Terraform-CLI/page

Practical guide to Terraform CLI features, plan customization flags, and using environment variables for input variables and provider authentication.

This concise guide walks through practical Terraform CLI features: built-in help, command-specific help, plan customization flags, and using environment variables both to set Terraform variables and to provide provider credentials. Keep this as a quick reference while working with Terraform locally or in CI.

Minimal Terraform example (we'll use this throughout)

```hcl theme={null}
provider "random" {}

variable "num_of_pets" {
  type        = number
  description = "How many pets do we want?"
}

resource "random_pet" "name" {
  length = var.num_of_pets
}

output "random_pet_name" {
  value = random_pet.name.id
}
```

## Getting CLI help

Open a terminal in your working directory and request top-level help to see global usage and available subcommands:

```bash theme={null}
$ terraform --help
Usage: terraform [global options] `<subcommand>` [args]

The available commands for execution are listed below.
The primary workflow commands are given first, followed by
less common or more advanced commands.

Main commands:
  init            Prepare your working directory for other commands
  validate        Check whether the configuration is valid
  plan            Show changes required by the current configuration
  apply           Create or update infrastructure
  destroy         Destroy previously-created infrastructure
```

Common and advanced commands (excerpt)

|     Command | Use Case                                                     |
| ----------: | ------------------------------------------------------------ |
|      `init` | Initialize a working directory and download provider plugins |
|  `validate` | Check HCL syntax and basic configuration consistency         |
|      `plan` | Produce an execution plan without changing infrastructure    |
|     `apply` | Create or update resources described by the configuration    |
|   `destroy` | Remove resources managed by Terraform                        |
|     `state` | Advanced state inspection and manipulation                   |
| `workspace` | Manage named workspaces for different state instances        |

Further down in the full help output you’ll also find less-common and deprecated commands (for example, `taint` and `untaint` were deprecated in favor of flags such as `-replace`).

Global options (use these before the subcommand)

```plaintext theme={null}
-chdir=DIR     Switch to a different working directory before executing the given subcommand.
-help          Show this help output, or the help for a specified subcommand.
-version       An alias for the "version" subcommand.
```

Request help for any specific subcommand:

```bash theme={null}
$ terraform validate --help
```

This prints what the subcommand does and all supported flags (for example, `validate` documents JSON output and color control flags).

Callout: subcommand help

> **lightbulb** You can get help for any subcommand (for example, `terraform plan --help`) to see detailed options, examples, and usage notes.

## Deep dive: terraform plan

`terraform plan` generates a speculative execution plan showing what Terraform would do to bring infrastructure in line with the configuration. It does not perform any changes unless you later pass a saved plan file to `apply`.

Example help excerpt:

```bash theme={null}
$ terraform plan --help
Usage:  terraform [global options] plan [options]

Generates a speculative execution plan, showing what actions Terraform
would take to apply the current configuration. This command will not
actually perform the planned actions.

You can optionally save the plan to a file, which you can then pass to
the "apply" command to perform exactly the actions described in the plan.

Plan Customization Options:
  -destroy
  -refresh=true|false
  -replace=resource_address
  -target=resource_address
  -var 'foo=bar'
  -var-file=filename
  -out=path
  -parallelism=n
  -state=statefile
  -no-color
  -input=true|false
```

Plan customization flags — quick reference

| Flag                        | Purpose                                             | Example                                    |
| --------------------------- | --------------------------------------------------- | ------------------------------------------ |
| `-replace=resource_address` | Force resource replacement (replacement of `taint`) | `terraform plan -replace=aws_instance.web` |
| `-target=resource_address`  | Plan only specific resource(s)                      | `terraform plan -target=module.db`         |
| `-var`                      | Set a variable from the CLI                         | `terraform plan -var 'num_of_pets=3'`      |
| `-var-file`                 | Load variables from a file                          | `terraform plan -var-file=prod.tfvars`     |
| `-out`                      | Save a plan to a path for later `apply`             | `terraform plan -out=tfplan`               |
| `-parallelism`              | Limit concurrent operations                         | `terraform plan -parallelism=4`            |

Notes:

* Use `-out` if you want to guarantee that `apply` performs the same actions as planned.
* Prefer `-var-file` or environment variables in CI to avoid leaking secrets in shell history.

## Passing Terraform variables via environment

Terraform supports setting input variables from the environment using the `TF_VAR_<variable_name>` pattern. For the example above, set `TF_VAR_num_of_pets` to provide `num_of_pets` from the environment.

If you run `terraform plan` without supplying `num_of_pets`, Terraform will prompt:

```plaintext theme={null}
$ terraform plan
var.num_of_pets
  How many pets do we want?

Enter a value:
```

Set the variable in a POSIX shell (macOS / Linux):

```bash theme={null}
export TF_VAR_num_of_pets=3
```

Rerunning `terraform plan` will now use that value without prompting:

```plaintext theme={null}
$ terraform plan
Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + random_pet_name = (known after apply)

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
```

If you change `TF_VAR_num_of_pets` to another number (for example `6`), resources depending on `var.num_of_pets` will reflect the new value on the next plan or apply.

Callout: using `TF_VAR_` environment variables

> **lightbulb** Use `TF_VAR_<variable_name>` to inject Terraform variable values from the environment. Example: `export TF_VAR_num_of_pets=3`. This is useful in CI/CD pipelines and local scripts.

## Environment variables for provider authentication

Provider SDKs typically read standard environment variables for authentication. These are provider-specific and are not Terraform-level variables.

Common provider authentication environment variables:

| Provider | Common env vars                                                              | Notes / docs                                                                                                                          |
| -------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| AWS      | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`           | See AWS provider docs: [https://registry.terraform.io/providers/hashicorp/aws](https://registry.terraform.io/providers/hashicorp/aws) |
| GCP      | `GOOGLE_CREDENTIALS`, `GOOGLE_PROJECT`, `GOOGLE_REGION`                      | Accepts service account JSON via `GOOGLE_CREDENTIALS`                                                                                 |
| Azure    | `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID` | AzureRM provider reads these                                                                                                          |
| Vault    | `VAULT_ADDR`, `VAULT_TOKEN`                                                  | Use `VAULT_TOKEN` or approles for auth                                                                                                |

AWS example (POSIX shell):

```bash theme={null}
export AWS_ACCESS_KEY_ID=AKIAEXAMPLEKEY
export AWS_SECRET_ACCESS_KEY=exampleSecretKeyHere
export AWS_DEFAULT_REGION=us-east-1
```

And an AWS provider block in HCL:

```hcl theme={null}
provider "aws" {
  region = "us-east-1"
}
```

Terraform will use the environment variables above to authenticate with AWS during `plan` or `apply`.

Callout: protect credentials

> **warning** Never commit credentials, tokens, or secret keys to version control. Use secure secrets management, environment injection in CI/CD, or a secrets backend (e.g., HashiCorp Vault) instead of hardcoding secrets in files.

## Summary and quick checklist

* Use `terraform --help` and `terraform <subcommand> --help` to discover commands, flags, and usage examples.
* `terraform plan` supports many customization flags (`-replace`, `-target`, `-var`, `-var-file`, `-out`); use `-out` when you need a reproducible apply step.
* Supply Terraform input variables via the environment using `TF_VAR_<variable_name>` for automation-friendly workflows.
* Provider authentication commonly relies on provider-specific environment variables (for example, AWS and Vault); consult provider docs for exact variable names.
* Never store secrets in source control—use secure vaults or platform-managed secret injection.

Further reading and references

* Terraform CLI documentation: [https://www.terraform.io/docs/cli](https://www.terraform.io/docs/cli)
* Terraform Providers: [https://registry.terraform.io/browse/providers](https://registry.terraform.io/browse/providers)
* AWS provider docs: [https://registry.terraform.io/providers/hashicorp/aws/latest/docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* HashiCorp Vault: [https://www.vaultproject.io/docs](https://www.vaultproject.io/docs)

That's it — a compact, practical walkthrough of helpful Terraform CLI commands, plan options, and environment-based variable and credential patterns.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/35cbc795-57ed-4af7-88c8-c9323af9294d/lesson/2fd8a53f-9925-44e9-beb6-c36f3efadc56)
