# Initialize the working directory (downloads providers, sets up backend)
terraform init

# Create and show an execution plan (safe preview of changes)
terraform plan

# Apply the planned changes (prompts for approval by default)
terraform apply

# Tear down managed infrastructure
terraform destroy
```

Workflow details, commands, and best practices

* Use version control (Git) for all Terraform code. Treat `.tf` files as the canonical source of truth.
* Prefer remote state backends (e.g., S3 with DynamoDB locking, Terraform Cloud/Enterprise) for team collaboration and state locking.
* Use `terraform plan -out=plan.tfplan` then `terraform apply "plan.tfplan"` to guarantee the apply exactly matches the reviewed plan.
* Protect secrets: avoid committing plaintext secrets. Use environment variables, secret managers, or encrypted variables in CI/CD.

Step-by-step breakdown

1. Write configuration

* Create `.tf` files to declare providers, resources, variables, outputs, and modules.
* Use modules to encapsulate reusable infrastructure patterns.
* Keep environment-specific values out of code; pass them via variables, variable files (`-var-file`), or a workspace-specific backend.
* Example:

```hcl theme={null}
provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "app_bucket" {
  bucket = var.bucket_name
  acl    = "private"
}
```

2. Initialize the workspace (`terraform init`)

* Downloads provider plugins and modules.
* Configures the backend (local or remote).
* Useful flags:
  * `-backend-config=FILE` to supply backend configuration.
  * `-reconfigure` to ignore existing backend configuration and reinitialize.
* Example:

```bash theme={null}
terraform init -backend-config="bucket=my-terraform-state" -reconfigure
```

3. Plan changes (`terraform plan`)

* Produces an execution plan showing what will be created, changed, or destroyed.
* Common flags:
  * `-out=plan.tfplan` to save the plan for later apply.
  * `-var='key=value'` or `-var-file=prod.tfvars` to inject variables.
  * `-refresh=true|false` to control state refresh.
* Best practice: always run `terraform plan` and review the diff before applying.

4. Apply changes (`terraform apply`)

* Apply can accept a saved plan file or run a fresh plan interactively.
* Typical usage:

```bash theme={null}
# Apply from a previously-saved plan
terraform apply "plan.tfplan"

# or run and apply in one step (prompts for confirmation)
terraform apply

# Non-interactive (CI)
terraform apply -auto-approve
```

* Prefer using saved plan files in automated pipelines to ensure reproducibility.

5. Destroy (`terraform destroy`)

* Safely tear down infrastructure that Terraform manages.
* Use with caution; consider `-target` or manual safeguards if you only want to remove specific resources.

```bash theme={null}
terraform destroy
terraform destroy -target=aws_instance.example
```

State management and locking

* State is critical: it maps your Terraform configuration to real resources.
* Use remote backends for team environments:
  * S3 + DynamoDB (AWS) for state storage + locking
  * Terraform Cloud or Terraform Enterprise for integrated state, locking, runs, and policy
* Encrypt state at rest and limit access.
* Avoid manual edits to state; use `terraform state` subcommands only when necessary.

Workspaces, environments, and branching

* Use separate workspaces (or separate backends/states) per environment (dev, staging, prod).
* Common pattern: separate IaC repos or directories for distinct lifecycles; or use variable files and CI/CD pipelines that target specific backends.
* Prefer distinct state per environment rather than relying on a single workspace to hold multiple unrelated resources.

CI/CD integration

* Create pipelines that:
  1. Run `terraform fmt` and `terraform validate`
  2. Run `terraform plan -out=plan.tfplan` and publish plan output for review
  3. On approval, run `terraform apply plan.tfplan` (non-interactive)
* Store backend secrets and provider credentials in the CI secret store.
* Lock and version provider/plugins by using the `required_providers` block and `terraform lock` file.

Common Commands and Useful Flags

| Command              | Purpose                                                     | Example                                                 |
| -------------------- | ----------------------------------------------------------- | ------------------------------------------------------- |
| `terraform init`     | Initialize directory, download providers, configure backend | `terraform init -backend-config="bucket=team-state"`    |
| `terraform plan`     | Preview changes without applying                            | `terraform plan -out=plan.tfplan -var-file=prod.tfvars` |
| `terraform apply`    | Apply changes to reach desired state                        | `terraform apply "plan.tfplan"`                         |
| `terraform destroy`  | Remove managed infrastructure                               | `terraform destroy -auto-approve`                       |
| `terraform fmt`      | Reformat HCL files                                          | `terraform fmt -recursive`                              |
| `terraform validate` | Validate configuration syntax                               | `terraform validate`                                    |

Security and operations callouts

<Callout icon="warning">
  Sensitive data can end up in Terraform state. Do not store secrets in plaintext variables that are committed to version control. Use secure secret management and encrypted backends.
</Callout>

Links and references

* Terraform CLI docs: [https://www.terraform.io/cli](https://www.terraform.io/cli)
* Terraform State: [https://www.terraform.io/language/state](https://www.terraform.io/language/state)
* Terraform Backends: [https://www.terraform.io/language/settings/backends](https://www.terraform.io/language/settings/backends)
* Terraform Cloud: [https://www.terraform.io/cloud](https://www.terraform.io/cloud)

Next steps

* We'll next walk through an example repository: initialize a backend, write a small module, run a plan, and apply safely in a CI pipeline. You’ll get hands-on practice with state locking, plan-review workflow, and best practices for team collaboration.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5b03b9b7-5f0f-4df6-8506-7de492c4791d/lesson/a55925df-881f-4ad6-863d-46c9356ce36a" />
</CardGroup>


# Terraform Apply

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/The-Core-Terraform-Workflow/Terraform-Apply/page

Describes terraform apply execution, state locking, incremental updates, lack of automatic rollback, operation modes and best practices for safely applying infrastructure changes.

Now that you’ve written your Terraform configs, initialized the working directory, and reviewed the plan, the final step is `terraform apply`.

Apply is the execution phase: Terraform reconciles your configuration with real-world infrastructure by calling provider APIs to create, modify, or destroy resources. Everything up to this point has been preparation and preview; apply is where infrastructure-as-code becomes actual infrastructure.

In this article you'll learn:

* What `terraform apply` does under the hood
* Key operational behaviors to expect during apply
* Common ways to run apply (interactive, saved plan, automation)
* Practical best practices to use apply safely

## What terraform apply actually does

* Runs a planning step that compares the recorded state with the desired configuration and produces a proposed set of changes.
* By default, displays that plan and prompts you to confirm before making changes (you must type `yes` to proceed).
* Executes the proposed changes by calling provider APIs and updates state as resources are created/updated/destroyed.

## Key operational behaviors during apply

* State locking: Terraform attempts to acquire a lock on state before applying changes when the backend supports locking (for example, [Terraform Cloud](https://www.terraform.io/cloud) or AWS S3 with a DynamoDB lock). This prevents concurrent modifications and reduces the risk of state corruption. Note: the local backend has limited locking semantics and some backends do not support locks.
* Incremental state updates: State is written incrementally as each resource operation succeeds rather than only at the end. If an apply fails partway through, the state reflects the resources already processed.
* No automatic rollback: Terraform does not automatically undo resources that were successfully created if a later resource fails. After a failed apply you must fix the cause and re-run apply (Terraform will continue from the current state), or manually destroy partial resources if appropriate.
* Dependency graph: Terraform respects resource dependencies and processes resources in the correct order. Independent resources may be handled in parallel when the provider supports it.

<Frame>
  <img alt="The image provides an overview of Terraform apply operations, explaining state locking, state updates, and the absence of automatic rollback when applying changes to infrastructure." />
</Frame>

## How to run terraform apply

| Mode                         | Command / Workflow                                                              | When to use                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Interactive default          | `terraform apply`                                                               | Manual changes when you want to review the final plan before execution.          |
| Saved plan file              | `terraform plan -out=myplan.tfplan` then `terraform apply myplan.tfplan`        | CI pipelines or when you want to review and store the exact plan to apply later. |
| Non-interactive / automation | `terraform apply -auto-approve` or `terraform apply -input=false -auto-approve` | Automation and CI/CD where human interaction is not possible (use with caution). |

Details and examples:

Default interactive apply

```bash theme={null}
terraform apply
```

This runs an implicit plan (refreshing state as needed), prints the proposed changes, and waits for you to confirm by typing `yes`. It’s the safest manual workflow.

Apply a saved plan file

1. Create and save a plan:

```bash theme={null}
terraform plan -out=myplan.tfplan
```

2. Apply the saved plan:

```bash theme={null}
terraform apply myplan.tfplan
```

Applying a saved plan skips the planning step and applies exactly what was saved. Note: applying a previously saved plan does not refresh real-world state before execution — if the infrastructure changed since the plan was created, the apply may fail.

Non-interactive / automation flags

* Skip the confirmation prompt:

```bash theme={null}
terraform apply -auto-approve
```

* For CI/CD pipelines (disable prompts and auto-approve):

```bash theme={null}
terraform apply -input=false -auto-approve
```

Use these flags only in automated contexts. `-auto-approve` removes the safeguard of human confirmation; `-input=false` prevents Terraform from prompting for input.

<Callout icon="lightbulb">
  When running Terraform in CI, generate and save the plan (`terraform plan -out=myplan.tfplan`) and then apply that exact plan file in the pipeline so the applied changes match what you reviewed.
</Callout>

<Callout icon="warning">
  Avoid `-auto-approve` for manual or production changes. Skipping confirmation increases the risk of unintended destruction or replacement of resources.
</Callout>

## Best practices before and during apply

* Always run and review `terraform plan` separately, especially for production or complex changes. Carefully check for unexpected replacements or deletions.
* Ensure you are in the correct working directory, using the intended backend and workspace before applying.
* Test changes in development or staging environments before applying to production.
* Be patient for long-running resources (databases, complex networking). Terraform waits for provider operations to complete; slow progress typically means the cloud provider is still provisioning.
* After a successful apply, verify resources were created/updated as intended and commit configuration changes to version control with clear messages that reflect the infrastructure changes.
* Use access controls and code review workflows for changes that modify critical infrastructure.

## Summary

`terraform apply` is the execution step that converts configuration into real infrastructure. It uses state locking (when supported), updates state incrementally, honors dependency ordering, and does not automatically roll back failed operations. Prefer interactive planning and careful review for manual changes; in automation use saved plans and non-interactive flags with appropriate safeguards.

## Links and references

* [Terraform documentation — Apply](https://developer.hashicorp.com/terraform/cli/commands/apply)
* [Terraform Cloud](https://www.terraform.io/cloud)
* [AWS S3](https://aws.amazon.com/s3) and [DynamoDB](https://aws.amazon.com/dynamodb) (for S3-backed state locking patterns)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5b03b9b7-5f0f-4df6-8506-7de492c4791d/lesson/8b6f86e5-5803-47e0-a116-981ad0a9b214" />
</CardGroup>
