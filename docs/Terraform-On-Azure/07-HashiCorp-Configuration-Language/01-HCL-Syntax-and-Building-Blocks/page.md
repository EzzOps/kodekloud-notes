# Set the logging level (TRACE is the most verbose)
export TF_LOG=TRACE

# Persist logs to a file
export TF_LOG_PATH=/tmp/tf.log
```

<Callout icon="lightbulb">
  If you run Terraform on an Azure VM or build agent, install the Azure Monitor Agent to collect the `TF_LOG` file and send it to a Log Analytics workspace. This enables centralized querying, filtering, and analysis of Terraform logs. See: [https://learn.microsoft.com/azure/azure-monitor/agents/azure-monitor-agent](https://learn.microsoft.com/azure/azure-monitor/agents/azure-monitor-agent)
</Callout>

<Callout icon="warning">
  Terraform logs at `DEBUG` or `TRACE` levels can contain sensitive data such as secrets or API tokens. Treat files created via `TF_LOG_PATH` as sensitive: restrict access, redact before sharing, and rotate credentials if exposed.
</Callout>

## TF\_LOG levels

Terraform supports these logging levels (from least to most verbose). Setting a level will include that level and all higher-severity messages.

| Level   | When to use                           | What it includes                                                                  |
| ------- | ------------------------------------- | --------------------------------------------------------------------------------- |
| `ERROR` | Production or minimal troubleshooting | Only failure messages and errors.                                                 |
| `WARN`  | Non-fatal potential problems          | Warning messages and errors.                                                      |
| `INFO`  | Normal operational visibility         | High-level events such as plan/apply summaries.                                   |
| `DEBUG` | Troubleshooting provider/API behavior | Detailed internal information and provider API calls.                             |
| `TRACE` | Deep debugging                        | Most verbose output including request/response cycles and fine-grained internals. |

Recommendation: use `DEBUG` for typical troubleshooting. Reserve `TRACE` for deep investigations, and avoid those levels for routine CI runs unless necessary.

## Example Terraform configuration

The following compact example is used throughout this guide. It provisions an Azure resource group and a storage account. A `local-exec` provisioner demonstrates how Terrafrom can execute local commands (note: provisioners and writing secrets to disk have security implications).

```hcl theme={null}
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-local-provisioner"
  location = "canadacentral"
}

resource "azurerm_storage_account" "sa" {
  name                     = "salocalprov2026"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  provisioner "local-exec" {
    command = "echo 'CONNECTION_STRING_PLACEHOLDER' > connection_string.txt"
  }
}
```

Note: the `azurerm` provider version and attribute availability can vary. To construct a real connection string, you may need to use provider attributes, data sources, or by retrieving account keys. Avoid writing secrets to disk where possible.

## Running Terraform with logging enabled

Set the environment variables in your terminal or CI agent before running Terraform commands.

Example:

```bash theme={null}
# export environment variables
export TF_LOG=DEBUG
export TF_LOG_PATH=/tmp/tf.log

# run Terraform plan
terraform plan
```

Behavior:

* When `TF_LOG` is set and `TF_LOG_PATH` is unset, verbose logs stream to the console.
* When `TF_LOG_PATH` is set, detailed logs are written to the file and Terraform’s console output remains the normal, succinct Terraform summary (the plan/apply text remains readable).
* For CI systems, prefer writing logs to a file and ingesting that file into your centralized logging.

## Inspecting and filtering the log file

Search and filter the log file to focus on provider API calls or errors. For example, to see provider HTTP GET requests:

```bash theme={null}
# Show provider GET requests in the log
cat /tmp/tf.log | grep GET
```

Representative output:

```plaintext theme={null}
2026-02-13T15:52:17.434Z [DEBUG] provider.terraform-provider-azurerm_v4.60.0_x5: GET https://management.azure.com/subscriptions/1b228746-75d4-46ed-8a6b-6a960d6d3a3/providers?api-version=2022-09-01
2026-02-13T15:52:18.054Z [DEBUG] provider.terraform-provider-azurerm_v4.60.0_x5: GET https://management.azure.com/subscriptions/1b228746-75d4-46ed-8a6b-6a960d6d3a3/resourceGroups/rg-local-provisioner?api-version=2022-09-01
2026-02-13T15:52:14.571Z [DEBUG] provider.terraform-provider-azurerm_v4.60.0_x5: GET https://salocalprov2026.queue.core.windows.net/?comp=properties
```

These entries show provider calls to Azure Resource Manager and storage endpoints. Reviewing these HTTP requests and their timestamps helps diagnose issues like authentication failures, rate limits, incorrect API versions, or missing resources.

## Sample log snippets

A provider plugin error and subsequent plugin exit may appear like this (cleaned and representative):

```plaintext theme={null}
2026-02-13T15:50:44.000+03:00 [DEBUG] plugin: error: code = Unavailable desc = error reading from server: connection reset
2026-02-13T15:50:44.000+03:00 [DEBUG] plugin: process exited: path=/terraform/providers/registry.terraform.io/hashicorp/azurerm/4.60.0/darwin_arm64/terraform-provider-azurerm_v4.60.0_x5
2026-02-13T15:50:44.000+03:00 [INFO] backend/local: plan operation completed!
```

A normal `terraform plan` run (console output remains user-friendly even when `TF_LOG_PATH` is set):

```plaintext theme={null}
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.
```

## Reducing verbosity

If `TRACE` or `DEBUG` is too noisy, reduce the level:

```bash theme={null}
export TF_LOG=INFO   # or WARN or ERROR
unset TF_LOG_PATH    # if you no longer want a persistent file
```

Guidance:

* Use `INFO` or `WARN` for routine runs.
* Use `DEBUG` to investigate provider-specific issues.
* Use `TRACE` only when troubleshooting deep internals or when requested by provider maintainers.

## Best practices for secure logging and centralized analysis

* Treat `TF_LOG_PATH` output as sensitive data. Limit permissions and encryption-at-rest where possible.
* Redact or scrub logs before sharing externally or attaching to tickets.
* Rotate credentials if they may have been exposed in logs.
* In production pipelines, send logs to a centralized logging system (e.g., Azure Log Analytics, Splunk, Elastic) and apply retention, access controls, and alerting.
* For Azure-specific ingestion, use the Azure Monitor Agent to forward log files to a Log Analytics workspace for query and correlation.

## Quick reference

| Topic                    | Command / Note                                              |
| ------------------------ | ----------------------------------------------------------- |
| Enable debug logs        | `export TF_LOG=DEBUG`                                       |
| Persist logs to file     | `export TF_LOG_PATH=/tmp/tf.log`                            |
| View provider HTTP calls | `grep GET /tmp/tf.log`                                      |
| Revoke logs or secrets   | Rotate credentials and remove or secure `TF_LOG_PATH` files |

## Summary

* Control Terraform logging with `TF_LOG` and persist logs with `TF_LOG_PATH`.
* `DEBUG` and `TRACE` reveal provider and API interactions—very useful for troubleshooting, but they can expose secrets.
* Centralize `TF_LOG` outputs with logging agents (Azure Monitor Agent → Log Analytics) for better analysis and retention.
* Inspect provider HTTP calls in logs to understand what Terraform requested and how the cloud provider responded.

## Links and references

* Terraform CLI environment variables: [https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf\_log](https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_log)
* Azure Monitor Agent: [https://learn.microsoft.com/azure/azure-monitor/agents/azure-monitor-agent](https://learn.microsoft.com/azure/azure-monitor/agents/azure-monitor-agent)
* Log Analytics workspace: [https://learn.microsoft.com/azure/azure-monitor/logs/log-analytics-workspace](https://learn.microsoft.com/azure/azure-monitor/logs/log-analytics-workspace)
* azurerm provider docs: [https://registry.terraform.io[AWS_SECRET_ACCESS_KEY]](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/8eb2a0b5-4324-4bba-9e4e-c01dd765911d/lesson/bca84dc3-abf2-4bdc-bbd5-e192250c830e" />
</CardGroup>


# HCL Syntax and Building Blocks

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/HashiCorp-Configuration-Language/HCL-Syntax-and-Building-Blocks/page

Overview of Terraform HCL syntax, resource block structure, provider roles, and examples for authoring cloud infrastructure configurations across Azure AWS and GCP

In this lesson we start authoring Terraform configuration files and examine the core building blocks of HCL (HashiCorp Configuration Language). HCL is a declarative language designed to describe the desired state of your infrastructure rather than a sequence of imperative steps.

Terraform configuration files use the `.tf` extension. Terraform automatically loads and evaluates all `.tf` files in a single directory as one configuration. File names are for organization only and do not control execution order. This lets you split large projects into logical files (for example, `network.tf`, `storage.tf`, `main.tf`) while Terraform evaluates them together.

<Callout icon="lightbulb">
  Terraform treats all `.tf` files in a directory as a single configuration. Use multiple files to organize resources logically (for example, `network.tf`, `storage.tf`, `main.tf`) without affecting evaluation order.
</Callout>

## Resource block: core structure

A Terraform resource block declares an infrastructure object that Terraform will create and manage. The general pattern is:

resource + provider-specific resource type + local name + arguments

Example: creating an Azure Resource Group

```hcl theme={null}
resource "azurerm_resource_group" "example" {
  name     = "my-rg"
  location = "East US"
}
```

Breakdown:

* `resource` — block type that declares a managed infrastructure object.
* `azurerm_resource_group` — provider-specific resource type (here: AzureRM provider).
* `"example"` — local name (local identifier) used within Terraform to reference this resource.
* The block body contains arguments that describe desired state:
  * `name` — the actual resource name in Azure.
  * `location` — the Azure region for the resource.

Every Terraform resource follows this same pattern. Once you understand it, reading and writing Terraform is predictable across providers.

## Example: Azure Storage Account

The resource type and arguments will vary by provider and resource. For example, creating an Azure Storage Account:

```hcl theme={null}
resource "azurerm_storage_account" "storage" {
  name                      = "mystorageacct123"
  resource_group_name       = "my-rg"
  location                  = "East US"
  account_tier              = "Standard"
  account_replication_type  = "LRS"
}
```

Notes on the storage account example:

* `azurerm_storage_account` is provided by the AzureRM provider.
* `account_tier` and `account_replication_type` are service-specific settings.
* `resource_group_name` shows how one resource is placed inside another logical resource (the storage account is created inside the resource group named `my-rg`).

Terraform supports explicit references between resources so it can infer dependencies and determine the correct creation order. Reference and dependency management are covered in more detail in later lessons.

<Callout icon="warning">
  Avoid hardcoding sensitive values (credentials, secrets, or provider tokens) directly in `.tf` files. Use `variables`, `terraform.tfvars`, or secret management solutions (for example, HashiCorp Vault or cloud-native secret stores) to keep secrets out of source control.
</Callout>

## Quick reference: resource block components

|     Component | Purpose                                                        | Example                                   |
| ------------: | -------------------------------------------------------------- | ----------------------------------------- |
|    Block type | Declares object type Terraform should manage                   | `resource`                                |
| Resource type | Provider-specific resource (resource schema)                   | `azurerm_resource_group`, `aws_s3_bucket` |
|    Local name | Local identifier for referencing the resource within Terraform | `"example"`, `"storage"`                  |
|     Arguments | Key/value settings that describe the desired state             | `name`, `location`, `account_tier`        |

## Provider responsibility

Terraform itself is provider-agnostic: it does not contain built-in knowledge about Azure, AWS, GCP, or other systems. Providers implement the platform-specific logic:

* Authenticate with APIs for the target platform.
* Expose supported resource types and their arguments.
* Validate configuration fields.
* Translate HCL into platform API calls.

In our examples, the AzureRM provider translates HCL resource blocks into Azure API calls. Each cloud or platform has its own provider and set of resource types. Examples include:

| Cloud / Platform | Example provider resource types                                                |
| ---------------- | ------------------------------------------------------------------------------ |
| Azure            | `azurerm_resource_group`, `azurerm_storage_account`, `azurerm_virtual_network` |
| AWS              | `aws_instance`, `aws_s3_bucket`, `aws_lambda_function`                         |
| GCP              | `google_compute_instance`, `google_container_cluster`                          |

<Frame>
  <img alt="The image compares cloud resource icons for three providers: Azure, AWS, and Google Cloud, each with distinctive service icons." />
</Frame>

Because providers handle platform-specific details, Terraform provides a consistent authoring workflow across clouds and services. You write HCL resource blocks and provider configurations; the provider translates them to API calls.

## Next steps and references

Now that you understand how a Terraform resource block maps to provider resource types and arguments, the next topics to explore are:

* How to configure and authenticate providers (provider blocks).
* Using `variables` and `outputs`.
* Managing references and implicit/explicit dependencies.
* Organizing large configurations into modules.

Useful references:

* [Terraform Documentation: Configuration Language](https://www.terraform.io/docs/language/index.html)
* [Azure Provider Docs (azurerm)](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])
* [AWS Provider Docs (aws)](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* [Google Cloud Provider Docs (google)](https://registry.terraform.[SECRET_REDACTED])

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/2dc00bf7-fa00-41df-a4e0-bce9fb23c19d/lesson/395f553f-0b72-44c1-a15a-ad90a71e6a93" />
</CardGroup>
