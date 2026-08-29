# Assigning Variable Values and Understanding Precedence

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-Configuration-Fundamentals/Assigning-Variable-Values-and-Understanding-Precedence/page

Explains Terraform variable assignment methods and layered precedence among defaults, environment variables, tfvars files, and CLI flags with best practices for secure, predictable configurations.

After declaring variables in a Terraform configuration, you can assign values in multiple ways. Terraform resolves variable values using a layered precedence model—each method acts like a layer in an onion, where higher layers override lower ones. Understanding these methods and their order of precedence helps you keep configurations predictable, secure, and suitable for development, CI/CD, and production.

This guide covers four primary methods to set Terraform variables:

* Variable block defaults
* Environment variables (`TF_VAR_` prefix)
* Terraform variable files (`.tfvars`)
* Command-line flags (`-var` / `-var-file`)

Quick summary (for scanning or SEO):

| Method                            | Best for                                  | Example                                   |
| --------------------------------- | ----------------------------------------- | ----------------------------------------- |
| Variable `default`                | Safe baseline values, documentation       | See `variable` block example below        |
| Environment variables (`TF_VAR_`) | Sensitive values from CI/CD/secret stores | `export TF_VAR_db_password="..."`         |
| `.tfvars` files                   | Grouping environment-specific settings    | `terraform plan -var-file="prod.tfvars"`  |
| Command-line flags                | Ad-hoc overrides, testing                 | `terraform apply -var="region=us-west-2"` |

For more detailed official guidance, see the Terraform docs: [Terraform CLI and provider docs](https://www.terraform.io/docs).

## 1) Variable defaults (variable block)

The simplest place to provide a value is inside the `variable` block using `default`. Defaults serve as a fallback when no other input method supplies a value.

Example:

```hcl theme={null}
variable "pub_subnet_ids" {
  type    = set(string)
  default = ["subnet-12345", "subnet-67890"]
}
```

When to use defaults:

* Provide reasonable, non-sensitive baseline values for development or documentation.
* Use defaults to make modules easier to consume without requiring every caller to set every value.

Best practices:

* Never put secrets (API keys, passwords) in `default`.
* Keep defaults minimal and generic.

<Callout icon="warning">
  Do not store sensitive secrets (API keys, credentials, passwords) in variable `default` values. Defaults are part of your configuration and may be committed to version control.
</Callout>

## 2) Environment variables (TF\_VAR\_)

Terraform maps environment variables with the `TF_VAR_` prefix to variables by name. This keeps secrets and environment-specific values out of repository files and integrates seamlessly with CI/CD secret stores.

Examples (bash):

```bash theme={null}
export TF_VAR_vsphere_network="10.0.5.0/24"
export TF_VAR_vm_image="image-x3f83j2sv3"
export TF_VAR_enable_logging=true
```

Examples (PowerShell):

```powershell theme={null}
$env:TF_VAR_enable_logging = "true"
$env:TF_VAR_subscription_id = "abcd-1234-cc"
```

Advantages:

* Keeps sensitive values out of code and `.tfvars` files.
* Works well with CI/CD secrets and ephemeral runners.
* Simple to inject per session or per pipeline run.

Limitations:

* Environment variables are scoped to the session/runner and are not automatically versioned alongside your code.

<Callout icon="lightbulb">
  Use environment variables for sensitive values that should not be checked into version control or for injecting secrets into CI/CD pipelines.
</Callout>

## 3) Terraform variable files (`.tfvars`)

`.tfvars` files are intentionally designed to hold variable assignments. Terraform automatically loads `terraform.tfvars` and any files ending in `.auto.tfvars` or `.auto.tfvars.json` in the working directory. Other `.tfvars` files—such as `dev.tfvars`, `staging.tfvars`, or `prod.tfvars`—must be passed explicitly with `-var-file`.

<Frame>
  <img alt="The image is an informational slide about using a .tfvars file to set variable values in Terraform, stating that Terraform automatically loads these files if they exist." />
</Frame>

Example `dev.tfvars`:

```hcl theme={null}
