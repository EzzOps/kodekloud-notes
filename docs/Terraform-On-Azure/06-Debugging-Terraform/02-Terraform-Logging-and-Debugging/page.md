# Terraform Logging and Debugging

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Debugging-Terraform/Terraform-Logging-and-Debugging/page

Guides Terraform logging setup and usage including TF_LOG and TF_LOG_PATH, interpreting logs, troubleshooting providers and APIs, and securely centralizing log collection

This guide explains how Terraform logging works, how to enable and collect logs, and how to use logs to troubleshoot provider and API issues. It focuses on the two environment variables Terraform uses for logging (`TF_LOG` and `TF_LOG_PATH`), how to interpret common log entries, and best practices for secure log handling and centralized ingestion.

## Key environment variables

Terraform logging is configured with environment variables:

* `TF_LOG` — sets the logging verbosity level Terraform will emit.
* `TF_LOG_PATH` — when set, Terraform writes logs to the specified file instead of streaming verbose logs to the console.

Example — enable the most verbose logging and persist it to a file:

```bash theme={null}
