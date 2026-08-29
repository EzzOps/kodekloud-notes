# Section Intro Terraform State

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Understading-and-Managing-Terraform-State/Section-Intro-Terraform-State/page

Overview of Terraform state including what it stores, how Terraform uses state during plan and apply, collaboration risks, and best practices for secure shared backends

Welcome to this lesson on Terraform state.

You may already have heard of the Terraform "desired state" concept. In this lesson we make that idea concrete and cover the core concepts you need to manage Terraform state safely and effectively.

What you'll learn in this lesson:

* What the Terraform state file is and why Terraform requires it.
* The kinds of information state stores and how Terraform uses that data during `plan` and `apply`.
* Why state matters for collaboration, incremental updates, and predictable infrastructure changes.

<Callout icon="lightbulb">
  This lesson focuses on the basics. Advanced topics—remote backends, state locking, `terraform import`, and state migration—are important but beyond the scope of this lesson.
</Callout>

Think of the Terraform state file as Terraform’s memory: the single source of truth that records what Terraform has created, the attributes and IDs of resources, and the dependency relationships between them. Terraform uses that data to:

* Compare your declared configuration with the actual infrastructure.
* Generate precise plans that show what will change.
* Perform targeted updates instead of recreating everything.

Because the state contains resource identifiers and metadata required to manage resources across runs, the state file is critical to safe and predictable infrastructure management and is an integral part of a healthy Terraform workflow.

## What the state file actually contains

The state file contains structured data that represents the current view of your managed infrastructure. Typical contents include:

| Item                              | Purpose                                                              | Examples                                                         |
| --------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Resource metadata                 | Identifiers and attributes Terraform needs to manage resources       | `id`, provider-specific attributes, resource type                |
| Resource dependencies             | Dependency graph Terraform uses to order operations                  | implicit/explicit dependencies between resources                 |
| Outputs                           | Values exported from modules for consumption by other code or humans | `output "db_endpoint" { value = aws_db_instance.main.endpoint }` |
| Provider configuration references | Which provider instances were used to create resources               | provider names, versions, and configuration references           |
| Module structure                  | How resources are grouped inside modules                             | module paths and their resources                                 |
| Internal metadata                 | Terraform's internal bookkeeping                                     | module addresses, serial, lineage                                |

## Example: Viewing state locally

Common commands for inspecting or retrieving state:

* Initialize a working directory:

```bash theme={null}
terraform init
```

* Generate a plan (state is used to compute diffs):

```bash theme={null}
terraform plan
```

* Show a specific resource or the whole state:

```bash theme={null}
terraform state list
terraform state show aws_instance.example
```

* Pull the current remote state (if using a remote backend):

```bash theme={null}
terraform state pull
```

You can also export state in machine-readable JSON for automation:

```bash theme={null}
terraform show -json > state.json
```

Example snippet from `terraform show -json` (abridged):

```json theme={null}
{
  "format_version": "0.1",
  "values": {
    "root_module": {
      "resources": [
        {
          "address": "aws_instance.example",
          "type": "aws_instance",
          "name": "example",
          "values": {
            "id": "i-0123456789abcdef0",
            "ami": "ami-0abcdef1234567890",
            "instance_type": "t2.micro"
          }
        }
      ]
    }
  }
}
```

## How Terraform uses state during plan and apply

1. Terraform reads the state file to understand what exists.
2. It compares the state + real-world resource attributes (via the provider) to the desired configuration.
3. Terraform builds a dependency graph to compute the optimal order for creating, updating, or destroying resources.
4. The plan shows precise create/update/delete operations; applying that plan updates both real resources and the state file.

This process allows Terraform to:

* Avoid unnecessary changes,
* Target updates efficiently,
* Preserve resource identity across runs.

## Why state matters for collaboration

When multiple team members or automation systems run Terraform against the same infrastructure, consistent and protected state is essential. Remote backends (S3, GCS, Terraform Cloud, etc.) centralize state and often provide locking to prevent concurrent modifications.

Key collaboration considerations:

* Use a remote backend to share state.
* Enable state locking where supported to prevent concurrent changes.
* Control access to the state file because it can contain sensitive values.

<Callout icon="warning">
  Terraform state can contain sensitive data (for example, resource IDs, IPs, or secrets). Always secure access to any backend or storage holding state and avoid committing state files (like `terraform.tfstate`) to source control.
</Callout>

## Best practices (brief)

* Use a remote backend for team-based workflows.
* Enable state locking when available.
* Store only non-sensitive configuration in code; protect secrets via provider-specific secret management or state encryption.
* Use `terraform import` to reconcile existing resources into state rather than recreating them.
* Regularly back up your remote state or use a backend that snapshots state history.

## Links and references

* [Terraform State Documentation](https://www.terraform.io/language/state)
* [Terraform Remote Backends](https://www.terraform.io/language/settings/backends)
* [Terraform Commands: state, show, plan, apply](https://www.terraform.io/cli)

Next, we'll examine what a real state file looks like on disk and how to migrate or lock state safely when collaborating across a team.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/2470872e-2566-4903-992b-b9fedc8c5739/lesson/93c54e54-0b9c-499e-bc61-a6d3d199231c" />
</CardGroup>
