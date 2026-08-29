# Enable the most detailed logs
export TF_LOG=TRACE
terraform plan
```

PowerShell (Windows)

```powershell theme={null}
# Enable the most detailed logs
$env:TF_LOG = "TRACE"
terraform plan
```

Targeting Core vs. Providers

To narrow down whether an issue stems from Terraform Core or a provider plugin, set the Core and Provider variables separately:

Bash

```bash theme={null}
export TF_LOG_CORE=TRACE
export TF_LOG_PROVIDER=TRACE
terraform plan
```

PowerShell

```powershell theme={null}
$env:TF_LOG_CORE = "TRACE"
$env:TF_LOG_PROVIDER = "TRACE"
terraform plan
```

Capturing logs to a file
By default Terraform writes logs to `STDERR`. To save logs to a file, set `TF_LOG_PATH` in addition to a logging level:

Bash

```bash theme={null}
export TF_LOG=TRACE
export TF_LOG_PATH=terraform.log
terraform plan
```

PowerShell

```powershell theme={null}
$env:TF_LOG = "TRACE"
$env:TF_LOG_PATH = "terraform.log"
terraform plan
```

Important details and best practices

* `TF_LOG_PATH` does nothing by itself — you must set `TF_LOG`, `TF_LOG_CORE`, or `TF_LOG_PROVIDER`.
* Logs are appended to the file; rotate or remove the file between runs if you want fresh logs per session.
* Terraform will create the file automatically if it does not exist.
* Log files can become very large at `TRACE` level; prefer targeted runs or rotate logs frequently.
* When troubleshooting, prefer `DEBUG` or `TRACE` only for the shortest time necessary to reduce noise and exposure.

> **warning** Terraform logs (especially `TRACE`-level) can contain sensitive information such as credentials, tokens, or resource attributes. Be careful when saving, sharing, or uploading logs. Redact or sanitize logs before sharing externally.

Structured logs and machine parsing
Some Terraform versions and environments support structured logging or options to emit logs in machine-readable formats (JSON) or provide ways to post-process trace output. Check the official Terraform environment variables and CLI docs for version-specific guidance:

* HashiCorp Terraform environment variables: [https://developer.hashicorp.com/terraform/cli/config/environment-variables](https://developer.hashicorp.com/terraform/cli/config/environment-variables)

Quick exam & quick-reference summary

> **lightbulb** Remember these essentials for studying and troubleshooting:

  * Key variables: `TF_LOG`, `TF_LOG_CORE`, `TF_LOG_PROVIDER`, `TF_LOG_PATH`.
  * Log level order (most → least verbose): `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`.
  * `TF_LOG_PATH` only works when a TF\_LOG variable is set.
  * Logs default to `STDERR`; use `TF_LOG_PATH` to write to a file.

References and further reading

* Terraform CLI environment variables — [https://developer.hashicorp.com/terraform/cli/config/environment-variables](https://developer.hashicorp.com/terraform/cli/config/environment-variables)
* Terraform documentation and provider docs for vendor-specific debugging guidance

That covers the essentials of Terraform logging. When a problem proves difficult to reproduce or diagnose, enabling the appropriate log level and capturing the output to a file will often reveal the cause.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/5a3363d1-83cc-4a39-997d-82fa687251ac/lesson/2c0e788a-1c6b-43e5-b3e2-417dbc64b0d8)


# Demo Debugging Terraform

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Troubleshooting/Demo-Debugging-Terraform/page

How to enable and use Terraform logging for detailed TRACE debugging, including configuration, log setup, interpreting traces, and redacting sensitive data

This lesson shows how to enable Terraform's logging to get detailed debugging information when troubleshooting configuration or provider issues. Detailed logs can reveal internal graph transforms, provider attachment, HCL source locations, and diff analysis that help diagnose misconfigurations, provider matching problems, or communication errors.

## Minimal demo configuration

Below is the minimal Terraform configuration used for the demo:

```hcl theme={null}
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.31.0"
    }
  }

  required_version = ">= 1.2.2"
}

provider "aws" {
  region = "us-east-2"
}
```

Running a normal plan typically produces a concise summary:

```bash theme={null}
$ terraform plan
Plan: 3 to add, 0 to change, 0 to destroy.

Note: You didn't use the --out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
```

## When to enable logging

Enable Terraform logging when you need more visibility into what Terraform Core and providers are doing — for example, when:

* Providers fail to match or load.
* Resources unexpectedly change or are omitted from the graph.
* API calls to providers return errors and you need the request/response context.

The most verbose output level is `TRACE`.

## TF\_LOG levels

| Level   | Description                                                                            |
| ------- | -------------------------------------------------------------------------------------- |
| `ERROR` | Only error messages                                                                    |
| `WARN`  | Warnings and errors                                                                    |
| `INFO`  | High-level informational messages                                                      |
| `DEBUG` | Detailed debugging messages from Terraform and providers                               |
| `TRACE` | Most verbose; internal operations, graph transforms, HCL ranges, provider interactions |

See the official environment variables reference for Terraform logging: [Terraform CLI — Environment variables](https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_log).

## Enable verbose logging

* On macOS / Linux (bash/zsh):

```bash theme={null}
export TF_LOG=TRACE
