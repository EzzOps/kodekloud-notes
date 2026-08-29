# Setting Up Azure Credentials for Terraform

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Preparing-Your-Environment/Setting-Up-Azure-Credentials-for-Terraform/page

Explains how to authenticate Terraform with Azure using Azure CLI, environment variables, service principals, or managed identities and run terraform plan and apply.

In this lesson you'll learn how to authenticate Terraform with Azure so you can run `terraform plan` and `terraform apply`. There are multiple authentication options (environment variables, service principals, managed identities, Azure CLI, etc.). For interactive and development workflows the simplest method is to authenticate with the Azure CLI using `az login`. Below is a minimal, reproducible example and the exact steps to get Terraform authorized to manage Azure resources.

Below are the example Terraform files used in this lesson.

main.tf

```hcl theme={null}
resource "azurerm_resource_group" "example" {
  name     = "example"
  location = "East US"
}
```

providers.tf

```hcl theme={null}
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.19.0"
    }
  }
}

provider "azurerm" {
  features {}

  # Using Azure CLI authentication, so no provider-specific auth settings required here.
}
```

Prerequisites

* Terraform installed.
* Azure CLI installed and available on your PATH.
* An Azure account with a subscription you can use.

> **lightbulb** If you are using a development environment such as [Codespaces](https://github.com/features/codespaces), the Azure CLI is often pre-installed.

Quick overview of authentication options

| Authentication method  |                                       Best for | Notes / example                                                                                                                 |
| ---------------------- | ---------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------- |
| Azure CLI (`az login`) |                  Interactive/local development | Simple to use; provider will use the logged-in account.                                                                         |
| Service Principal      |                           CI/CD and automation | Non-interactive; requires creating SP and setting `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID`. |
| Managed Identity       | Azure-hosted automation (VM, App Service, AKS) | Secure, no secrets needed; grant RBAC to the managed identity.                                                                  |

Step-by-step

1. Initialize the working directory

```bash theme={null}
terraform init
```

2. Attempt a plan (before authenticating)

```bash theme={null}
terraform plan
```

If you have not authenticated, the AzureRM provider will report that a `subscription_id` (or other credentials) is required. Example error:

```text theme={null}
Error: `subscription_id` is a required provider property when performing a plan/apply operation

with provider["registry.terraform.io/hashicorp/azurerm"],
on providers.tf line 10, in provider "azurerm":
10: provider "azurerm" {
```

3. Authenticate with the Azure CLI
   Run:

```bash theme={null}
az login
```

This command opens a browser window for interactive sign-in (or prints a device login code for headless environments). After a successful login the CLI lists the subscriptions available to the account.

To confirm the CLI can access your account:

```bash theme={null}
az account show
```

4. Configure which subscription Terraform should use

There are two common ways to make a subscription available to Terraform when authenticating via the Azure CLI:

Option A — Set the `ARM_SUBSCRIPTION_ID` environment variable (session-only)

* macOS / Linux (bash/zsh):
  ```bash theme={null}
  export ARM_SUBSCRIPTION_ID=4c62e312-4b55-4e4d-8c5f-d40d247a5bb
  ```
* Windows PowerShell (session-only):
  ```powershell theme={null}
  $env:ARM_SUBSCRIPTION_ID = "4c62e312-4b55-4e4d-8c5f-d40d247a5bb"
  ```
* Windows Command Prompt (session-only):
  ```cmd theme={null}
  set ARM_SUBSCRIPTION_ID=4c62e312-4b55-4e4d-8c5f-d40d247a5bb
  ```

To persist the variable across sessions on Windows, use `setx` or configure it in System Properties.

Option B — Tell the Azure CLI which subscription to use (affects `az` commands and is honored by CLI auth):

```bash theme={null}
az account set --subscription 4c62e312-4b55-4e4d-8c5f-d40d247a5bb
```

Either of these options ensures the subscription ID is available when the AzureRM provider authenticates via the Azure CLI.

5. Apply the Terraform configuration

```bash theme={null}
terraform apply
```

Terraform will show a plan summary similar to:

```text theme={null}
Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
Terraform will perform the actions described above.
Only 'yes' will be accepted to approve.

Enter a value:
```

Type `yes` to proceed. Terraform will create the resource group and write state to the configured backend (local by default).

Notes and troubleshooting

* If you still see errors about missing credentials:
  * Verify `az login` succeeded and `az account show` returns the expected subscription.
  * Confirm `ARM_SUBSCRIPTION_ID` is set in your session or that `az account show` lists the desired subscription.
* To check CLI-auth usage, run Terraform with detailed logs:
  ```bash theme={null}
  TF_LOG=DEBUG terraform plan
  ```
* For non-interactive automation (CI/CD), use a Service Principal or a managed identity instead of `az login`. See the official docs for best practices and examples.

> **warning** Do not commit secrets or credentials (client secrets, subscription IDs, or other sensitive data) to version control. For automation, prefer Service Principal or Managed Identity with least-privilege RBAC and store credentials in a secure secrets manager.

References and further reading

* Azure CLI documentation: [https://learn.microsoft.com/cli/azure/](https://learn.microsoft.com/cli/azure/)
* AzureRM Provider (Terraform): [https://registry.terraform.io/providers/hashicorp/azurerm/latest](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
* Authenticating with the Azure Provider: [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure\_cli](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli)

That’s it — authenticate with `az login`, set the subscription (via environment variable or `az account set`), then use `terraform plan` and `terraform apply` to manage your Azure resources.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/df5b5815-c1ea-45f5-ba18-7a5c53ded28a/lesson/4151a641-8fd6-42cb-83ae-e06ed7b81cf8)
