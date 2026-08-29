# Setting Variables

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Variables/Setting-Variables/page

Guide to supplying Terraform input variable values at runtime, covering prompts, flags, tfvars files, environment TF_VAR variables, precedence, and best practices for automation and secrets.

Now that you understand what variables are and why they're useful in Terraform, this guide shows how to provide concrete values at runtime. Declaring a variable in Terraform creates a placeholder; a value must be supplied by one of several supported methods. Below we walk through each method—from interactive prompts to production-ready CI/CD approaches—and explain precedence so there’s no confusion when multiple sources supply the same variable.

Quick overview of methods:

* Interactive prompts
* Command-line flags (`-var` / `-var-file`)
* Variable definition files (`.tfvars` / `.auto.tfvars`)
* Environment variables (`TF_VAR_*`)

## 1) Interactive prompts

If a variable is declared without a `default` and no other source provides a value, Terraform prompts you at runtime. This is convenient for demos and learning but unsuitable for automation.

Example declarations:

```hcl theme={null}
