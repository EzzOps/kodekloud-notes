# aws_vpc.sbx_vpc will be created
+ resource "aws_vpc" "sbx_vpc" {
    + arn = (known after apply)
    + id  = (known after apply)
    ...
}

# aws_vpc.vpc will be destroyed
- resource "aws_vpc" "vpc" {
    - id  = "vpc-0123456789abcdef0" -> null
    ...
}

Plan: 1 to add, 0 to change, 1 to destroy.
```

That plan indicates Terraform intends to destroy the existing VPC and create a new one under the new address — not what you want if the resource was only renamed.

<Frame>
  <img alt="The image is a diagram titled &#x22;Another Scenario&#x22; showcasing a Terraform configuration with various components like firewall, database, load balancer, and virtual machines organized in blocks." />
</Frame>

Another common refactor: moving resources out of a monolithic `main.tf` into logical child modules (for example `network`, `security`, `compute`, `database`). From Terraform’s perspective the addresses differ: `aws_instance.web_server` is not the same as `module.compute.aws_instance.web_server`. Without telling Terraform about the move, it will attempt to recreate the resources under the new module addresses.

<Frame>
  <img alt="The image is a diagram displaying components of a network infrastructure, including security, database, network, DNS, load balancing, apps, and compute sections with various labeled elements like firewall, virtual machines, and DNS entries." />
</Frame>

What the moved block does

* The `moved` block maps an old resource address to a new one so Terraform updates its state without performing provider API calls.
* Terraform updates only its internal state file; no infrastructure is destroyed or recreated.
* Use it to rename resources or to move resources into/out of modules safely.

<Frame>
  <img alt="The image shows a description of the &#x22;Moved Block&#x22; in Terraform, explaining its purpose in updating resource addresses without impacting infrastructure. On the left, there is a photo of a purple arrow painted on concrete." />
</Frame>

When to use `moved`

| Use case                              | Description                                                                   |
| ------------------------------------- | ----------------------------------------------------------------------------- |
| Rename a resource                     | Change `aws_vpc.vpc` → `aws_vpc.sbx_vpc` without recreating the VPC.          |
| Move into a module                    | Change `aws_s3_bucket.data` → `module.storage.aws_s3_bucket.data`.            |
| Move between modules / rename modules | Change `module.old_app.aws_instance.app` → `module.new_app.aws_instance.app`. |

moved block syntax

* The block is declarative and simple: provide `from` and `to`, both as string resource addresses.

Examples:

```hcl theme={null}
moved {
  from = "aws_instance.server"
  to   = "aws_instance.web_server"
}

moved {
  from = "aws_s3_bucket.data"
  to   = "module.storage.aws_s3_bucket.data"
}

moved {
  from = "module.old_app.aws_instance.app"
  to   = "module.new_app.aws_instance.app"
}
```

These examples tell Terraform to reassign the tracked state for the specified addresses; no provider API calls are made.

Refactoring workflow using `moved` blocks

1. Add the destination resources to your configuration first.
   * If moving into a module, create the module definition and include the resource blocks.
2. Add one or more `moved` blocks mapping old addresses to new addresses.
   * You can put these mappings in a dedicated file such as `moved.tf` for clarity.
3. Run `terraform plan` to validate. Expect state move operations — not create/destroy of cloud resources.
4. Run `terraform apply` to update the state file. This is fast because it updates only Terraform’s state.
5. After successful apply you can remove the `moved` blocks (or keep them as documentation).

Typical command sequence:

```bash theme={null}
$ terraform plan
$ terraform apply
# apply the state updates (no provider-side resource changes)
```

> **lightbulb** The `moved` blocks are temporary state-migration scaffolding. Once applied they are no longer required for Terraform to track the resources at their new addresses, though many teams keep them in `moved.tf` for auditability.

Additional references

* Terraform docs — State: Move resources: [https://www.terraform.io/docs/cli/commands/state/move.html](https://www.terraform.io/docs/cli/commands/state/move.html)
* Terraform docs — Configuration language: resource addresses: [https://www.terraform.io/docs/language/state/resource-addressing.html](https://www.terraform.io/docs/language/state/resource-addressing.html)

Summary

* Use the `moved` block to refactor resource addresses without changing infrastructure.
* Always add destination resources first, then declare `moved` mappings, then `plan` and `apply`.
* This approach keeps your refactor safe, auditable, and fast — no downtime and no manual state edits.

<Frame>
  <img alt="The image outlines a refactoring workflow for Terraform, including stages: write, plan, apply, and delete, with specific actions for each step. Each stage is represented by an icon and a brief description of the task involved." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/42da48a6-09fe-43c7-997f-255cdb3e0c80/lesson/d2de55ad-7b05-4bdd-83e5-5a055fe553f9)


# Refactoring Terraform State

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Refactoring-Terraform-State/Refactoring-Terraform-State/page

Explains configuration-driven Terraform state refactoring using moved, removed, and import blocks for safe, auditable renames, moves, and imports.

In this lesson we cover how to refactor Terraform state in a controlled, auditable way — that is, changing how Terraform tracks your infrastructure without modifying the real-world resources themselves.

Why this matters

* Avoid accidental destroy/recreate cycles when you rename or move resources in code.
* Keep state operations visible in version control and code review.
* Validate refactors using `terraform plan` before applying them.

Common scenarios that require state refactoring:

* You renamed a resource (for example, `aws_instance.web` → `aws_instance.webserver`).
* You reorganized code (moved resources between files or into modules).
* You want Terraform to adopt existing infrastructure created outside Terraform.
* You want Terraform to stop managing a resource while leaving it running in the cloud (e.g., handing it off to another team).

Historically, teams relied on CLI tools such as `terraform state mv`, `terraform state rm`, and `terraform import`. Those work, but they are procedural and happen outside of configuration — making them harder to review, test, and reproduce. HashiCorp introduced a configuration-driven approach: declare `moved`, `removed`, and `import` blocks in Terraform configuration. Because these refactoring declarations are code, they are version-controlled, reviewable in PRs, and validated by `terraform plan` before being applied.

<Frame>
  <img alt="The image compares &#x22;The Old Way&#x22; and &#x22;The New Way&#x22; of using Terraform. The old method involves using separate CLI commands that are risky and not version-controlled, while the new method uses configuration blocks that are version-controlled, reviewable in pull requests, and can be tested before application." />
</Frame>

Key refactoring blocks

* moved — Map an old Terraform address to a new one so state is updated without destroying the underlying resource.
* removed — Remove a resource from Terraform state while leaving the resource running in-cloud.
* import — Adopt an existing resource into Terraform state by providing the target address and the provider-specific ID.

Quick reference table

| Refactor block |                                                      When to use | Minimal example                                                                      |
| -------------- | ---------------------------------------------------------------: | ------------------------------------------------------------------------------------ |
| `moved`        | You only changed the resource address (renamed or moved in code) | `hcl\nmoved { from = aws_instance.web to = aws_instance.webserver }\n`               |
| `removed`      | Tell Terraform to stop managing a resource without destroying it | `hcl\nremoved { from = aws_instance.production_db }\n`                               |
| `import`       |                Adopt an existing resource into Terraform control | `hcl\nimport { to = aws_s3_bucket.terraform_state id = "terraform_state_bucket" }\n` |

Example: all three blocks together

```hcl theme={null}
moved {
  from = azurerm_subnet.subnet1
  to   = azurerm_subnet.prod_private
}

removed {
  from = aws_instance.production_db
}

import {
  to = aws_s3_bucket.terraform_state
  id = "terraform_state_bucket"
}
```

Best practices and notes

moved

* Use `moved` only when the real resource hasn't changed — only its address in your configuration has.
* `from` and `to` are Terraform addresses (for example, `aws_instance.web`, or `module.db.aws_db_instance.main`).
* Add the `moved` block to your configuration and run `terraform plan` to validate the mapping before `terraform apply`.

removed

* A `removed` block instructs Terraform to drop the resource from state. Terraform will not try to destroy the actual resource as part of this refactor.
* If you are concerned that other code changes might try to destroy the resource accidentally, add a `lifecycle` block with `prevent_destroy = true` to the resource configuration before you remove it from state. Example:

```hcl theme={null}
resource "aws_instance" "production_db" {
  # ... other resource configuration ...

  lifecycle {
    prevent_destroy = true
  }
}
```

* After you validate with `terraform plan` and are confident the resource is safe, add the `removed` block and run `terraform apply` to drop it from state.

> **warning** If you use `prevent_destroy = true`, remember to remove or update that lifecycle rule when you want normal destroy behavior again. Leaving `prevent_destroy` in place can block legitimate destroy operations in future runs.

import

* Use `import` when a resource already exists (created manually, by another tool, or in a different workspace) and you want Terraform to manage it.
* `to` is the Terraform address you will declare in your configuration. `id` is the provider-specific identifier (for example, an S3 bucket name or an EC2 instance ID).
* After adding the `import` block and validating with `terraform plan`, run `terraform apply` to create the state entry. You still must declare the corresponding resource in your configuration with matching arguments where applicable.

Safe workflow for configuration-driven refactoring

1. Add the refactoring block(s) to your Terraform files (under the same root that has your state).
2. Run `terraform plan` to preview how state will change and to validate that the mapping or import works as expected.
3. If the plan looks correct, run `terraform apply` to update the state. The actual infrastructure will remain unchanged unless you also make other configuration changes.

Command examples

```bash theme={null}
terraform plan
terraform apply
```

<Frame>
  <img alt="The image outlines &#x22;The Refactoring Workflow,&#x22; consisting of three steps: Write (adding blocks to Terraform config), Plan (validating changes with terraform plan), and Apply (updating state with terraform apply)." />
</Frame>

Wrapping up
Using configuration-driven refactoring blocks (`moved`, `removed`, `import`) is the recommended, modern workflow. It makes state changes auditable, reviewable, and safer by integrating refactors into the standard plan/apply lifecycle. These techniques are practical for day-to-day Terraform management and are relevant study topics for the [HashiCorp Certified: Terraform Associate 004](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004) exam.

Further reading and references

* [Terraform State Move Command](https://www.terraform.io/cli/commands/state/mv)
* [Terraform State Remove Command](https://www.terraform.io/cli/commands/state/rm)
* [Terraform Import Command](https://www.terraform.io/cli/commands/import)
* [Terraform: Moved and Removed Blocks (HashiCorp)](https://www.terraform.io/docs/configuration/refactoring/state.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/42da48a6-09fe-43c7-997f-255cdb3e0c80/lesson/9ba261ee-30be-4570-abfc-a07af4c8abb7)
