# Local Provisioners

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Provisioners/Local-Provisioners/page

Explains Terraform local-exec provisioner for running commands on the Terraform host to orchestrate tasks like saving outputs, triggering CI/CD, and sending notifications, not configuring resources.

In this lesson we move from remote provisioners to local provisioners in Terraform and show how to use the `local-exec` provisioner to run commands on the machine executing Terraform (your laptop, a jump host, or a CI/CD agent).

Unlike remote provisioners, which log into and configure created resources (via SSH, WinRM, etc.), the `local-exec` provisioner executes a command locally after Terraform completes the resource creation lifecycle event. It does not connect to or modify the created resource; it’s intended for orchestration and automation side-effects.

<Frame>
  <img alt="The image is an illustration explaining local provisioners with a computer screen icon and text pointing out that it happens after the resource is created and doesn't connect to the resource." />
</Frame>

Key characteristics

* Runs on the Terraform host (not on the provisioned resource).
* Executes after the resource creation or before destruction depending on configuration.
* Useful for orchestration tasks (writing local files, triggering pipelines, sending notifications).
* Not suitable for resource configuration or long-running configuration management.

Use cases

Local provisioners are commonly used for lightweight automation tasks such as:

* Writing resource outputs to a local file (for example, capturing a public IP address or a connection string).
* Triggering shell scripts or CI/CD tasks (invoking additional deployment stages, notifying systems, or kicking off pipelines).
* Sending alerts or webhooks (Slack notifications, integrations with monitoring/operational tooling).

These are orchestration or automation side effects, not infrastructure configuration tasks.

<Frame>
  <img alt="The image lists three use cases: writing outputs to a file, triggering shell scripts or CI/CD tasks, and sending Slack/webhook alerts." />
</Frame>

Use cases at a glance

| Use case                 | Typical goal                                 | Example                                              |
| ------------------------ | -------------------------------------------- | ---------------------------------------------------- |
| Persist outputs locally  | Capture provider values for downstream tools | Write a connection string to `connection_string.txt` |
| Trigger CI/CD or scripts | Orchestrate further automation steps         | Run a shell script after apply                       |
| Send notifications       | Inform teams or systems about changes        | Post a webhook to Slack or a monitoring system       |

Example: save a storage account connection string locally

The following compact example creates an Azure resource group and a storage account, then uses a `local-exec` provisioner to write the storage account's primary connection string to a local file named `connection_string.txt`.

Notes applied:

* Use `provider "azurerm" { features {} }` (required by recent `azurerm` provider versions).
* Wrap provider-marked sensitive values with `nonsensitive()` when you intentionally need to emit them.
* Wrap the connection string in single quotes in the shell `echo` to avoid shell interpretation of semicolons.

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
    command = "echo '${nonsensitive(self.primary_connection_string)}' > connection_string.txt"
  }
}
```

Why this works

* In a provisioner, `self` refers to the current resource instance (here, the storage account).
* `primary_connection_string` is the attribute exposed by the storage account resource that contains the connection string.
* `nonsensitive()` unwraps values marked sensitive by the provider so Terraform can emit them. Use this only when you intentionally want the value exposed.
* Single quotes around the interpolated value prevent semicolons in the connection string from being interpreted by the shell.

Initialize and apply

1. Initialize the working directory (downloads providers and sets up the environment):

```bash theme={null}
terraform init
```

Example initialization output (trimmed):

```plaintext theme={null}
Installed hashicorp/azurerm v4.60.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!
```

2. Apply the configuration (use `--auto-approve` to skip the confirmation prompt):

```bash theme={null}
terraform apply --auto-approve
```

Example apply output (truncated):

```plaintext theme={null}
azurerm_resource_group.rg: Creating...
azurerm_resource_group.rg: Creation complete after 28s [id=/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-local-provisioner]
azurerm_storage_account.sa: Creating...
azurerm_storage_account.sa: Creation complete after 1m3s [id=/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-local-provisioner/providers/Microsoft.Storage/storageAccounts/salocalprov2026]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

After apply, the `local-exec` provisioner runs on the Terraform host and writes the file. Verify it:

```bash theme={null}
cat connection_string.txt
```

Example output:

```plaintext theme={null}
DefaultEndpointsProtocol=https;AccountName=salocalprov2026;AccountKey=ABCDEFGHIJK...;EndpointSuffix=core.windows.net
```

This demonstrates capturing a provider attribute and storing it locally using a local provisioner.

<Callout icon="lightbulb">
  Local provisioners are best for orchestration or integration steps (e.g., saving outputs locally, invoking CI/CD pipelines, or sending notifications). They are not a substitute for configuration management on created resources.
</Callout>

<Callout icon="warning">
  Avoid using provisioners for critical configuration or secrets handling. Sensitive values written locally may be stored in plaintext unless handled carefully; using `nonsensitive()` forces Terraform to expose values that would otherwise be masked—use with caution.
</Callout>

Considerations before using provisioners

* Execution environment: Provisioners run on the machine executing Terraform; ensure that host has required permissions, network access, and installed tooling.
* Idempotence: Provisioner commands may have side effects and can make `terraform apply` non-idempotent if not written carefully.
* Lifecycle coupling: Provisioners are tied to the resource lifecycle (they run during create/destroy as configured). Plan for how retries and re-creates affect side effects.
* Prefer native solutions: When possible, use built-in provider features or established configuration management/orchestration tools such as Ansible or cloud-init. Use provisioners only when no native alternative exists.

Further reading and references

* [Terraform Provisioners Documentation](https://developer.hashicorp.[SECRET_REDACTED])
* [Azure RM Provider Docs](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY])
* [Learn Ansible Basics - Beginners Course](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course)
* [cloud-init](https://cloud-init.io/)

That's how the `local-exec` provisioner works and how you can use it to capture and persist resource outputs on the Terraform host.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/cb34375e-505a-4794-a260-d12aeba6440e/lesson/f340efec-310e-4ba6-8fd7-009f973460d4" />
</CardGroup>
