# Sourcing a Module From the Terraform Registry

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Modules/Sourcing-a-Module-From-the-Terraform-Registry/page

Learn to source and manage Terraform modules using Terragrunt for efficient infrastructure as code practices.

Leverage the Terraform Registry to discover, share, and reuse community-maintained modules. When you integrate Terragrunt, you can reference these modules directly using the `tfr://` protocol.

## 1. Referencing a Module in Terragrunt

In your `terragrunt.hcl` file, set the `source` attribute to point at a Registry module:

```hcl theme={null}
