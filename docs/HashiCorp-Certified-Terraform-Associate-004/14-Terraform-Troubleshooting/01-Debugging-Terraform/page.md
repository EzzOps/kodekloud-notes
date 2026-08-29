# module.vpc.aws_vpc.vpc will be created
resource "aws_vpc" "vpc" {
  + arn                        = (known after apply)
  + cidr_block                 = "10.0.0.0/16"
  + default_network_acl_id     = (known after apply)
  + default_route_table_id     = (known after apply)
  + default_security_group_id  = (known after apply)
  ...
}
```

<Frame>
  <img alt="The image shows a Visual Studio Code window with a Terraform configuration file open, displaying code related to module configuration and variables for a cloud infrastructure setup. The left sidebar lists project files, while the main section includes code with autocompletion suggestions." />
</Frame>

***

## Notes and best practices

<Callout icon="lightbulb">
  Use module outputs to pass information between modules (for example: `module.vpc.vpc_id` -> `module.subnet_module.vpc_id`). Keep modules small, well-documented, and parameterized so they can be reused across environments.
</Callout>

<Callout icon="warning">
  Running `terraform apply` will create resources in your cloud account and may incur charges. Always review the plan before applying and destroy resources when they are no longer needed.
</Callout>

* Use descriptive variable names and include `description` in each `variables.tf`.
* Prefer explicit module inputs over relying on implicit defaults in a parent configuration.
* You can call a module multiple times with different arguments, or use `for_each` to create multiple instances of a module.
* Split responsibilities logically (networking, compute, database) to simplify testing and reuse.
* Consider versioning modules if you extract them to a shared registry.

Recommended links:

* [Terraform Documentation](https://www.terraform.io/docs)
* [AWS Provider for Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

***

## Summary

* You created a local module structure (`vpc`, `subnet`, `ec2`), implemented resources along with variables and outputs, and wired module outputs into parent module inputs.
* This modular approach reduces duplication and makes it easy to create multiple similar environments by calling the same module with different inputs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/7a9b9328-bd7d-4cb0-99f2-2ac166f272a7/lesson/d75b966e-68c8-44e4-9ba3-b79efa99bbb2" />
</CardGroup>


# Debugging Terraform

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Troubleshooting/Debugging-Terraform/page

Guide for enabling and capturing Terraform internal logs, using TF_LOG variables and TF_LOG_PATH, choosing log levels, targeting Core or providers, and best practices for secure debugging

In this guide you’ll learn how to enable and capture Terraform’s internal logs for troubleshooting, auditing, or when preparing bug reports. These environment variables and workflows are commonly expected knowledge for the Terraform Associate Certification and practical debugging tasks.

Why logging matters

* Reproduce unexpected behavior (resources not created, unexpected diffs, confusing errors).
* Provide detailed trace-level logs when filing bug reports with HashiCorp or provider maintainers.
* Audit API calls, provider interactions, and Terraform Core decisions during planning and apply phases.

By default Terraform emits only user-facing messages (summaries and errors). Enabling logging reveals internal operations and API traffic — invaluable for debugging but often very verbose.

When to enable detailed logs

* You're investigating non-deterministic or unexplained Terraform behavior.
* A provider or the Terraform binary returns unclear errors.
* You need trace-level evidence to open a bug/issue with maintainers.
* You want to learn how Terraform orchestrates provider calls and state transitions.

Environment variables and log levels

| Environment Variable | Purpose                                                                            | Example                            |
| -------------------- | ---------------------------------------------------------------------------------- | ---------------------------------- |
| `TF_LOG`             | Enable logging for both Core and providers (global).                               | `export TF_LOG=TRACE`              |
| `TF_LOG_CORE`        | Target logging specifically to Terraform Core (dependency graph, state, planning). | `export TF_LOG_CORE=DEBUG`         |
| `TF_LOG_PROVIDER`    | Target logging specifically to provider plugins (AWS, Azure, Kubernetes, etc.).    | `export TF_LOG_PROVIDER=TRACE`     |
| `TF_LOG_PATH`        | File path to append logs. Only works when a TF\_LOG\*/TF\_LOG variable is set.     | `export TF_LOG_PATH=terraform.log` |

Log levels (most → least verbose)

* `TRACE` — most detailed; recommended for bug reports.
* `DEBUG` — developer-level detail; slightly less noisy than TRACE.
* `INFO` — high-level informational messages.
* `WARN` — potential issues worth attention.
* `ERROR` — only actual error messages.

Enabling logging (examples)

Bash (Linux / macOS)

```bash theme={null}
