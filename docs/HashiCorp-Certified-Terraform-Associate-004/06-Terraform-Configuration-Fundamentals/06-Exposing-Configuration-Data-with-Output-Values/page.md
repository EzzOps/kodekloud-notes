# Exposing Configuration Data with Output Values

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Configuration-Fundamentals/Exposing-Configuration-Data-with-Output-Values/page

How Terraform output blocks expose and manage configuration values like IPs, DNS names, IDs and secrets, including examples, commands, sensitivity handling, and best practices.

Welcome to this lesson on the Terraform `output` block. Outputs let you expose important data produced by your Terraform runs—such as IP addresses, DNS names, resource IDs, and connection strings—so people, scripts, and other modules can consume them without digging through cloud consoles or re-running queries.

## Why use outputs?

* Capture useful attributes created by Terraform (VM IPs, DB connection strings, DNS names, etc.).
* Display important values immediately after `terraform apply` for quick testing.
* Persist outputs in state so they can be retrieved later with `terraform output`.
* Pass values between modules to enable composable infrastructure.
* Make CI/CD automation and scripts more reliable using `terraform output -json`.

## Example: Azure resources

These resource blocks create an Azure Resource Group and a Virtual Network. After creation, surface values such as the resource group name, VNet ID, or subnet IDs with outputs so other systems or modules can use them.

```hcl theme={null}
