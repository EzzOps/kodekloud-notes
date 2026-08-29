# Type "yes" to confirm
```

Inspect the generated key:

```bash theme={null}
opentofu show tls_private_key.pvtkey
```

<Callout icon="triangle-alert">
  Storing private keys in plain text can pose a security risk. Never commit sensitive key material to version control.
</Callout>

## Writing the Key to a Local File

Update `key.tf` to include a `local_file` resource:

```hcl theme={null}
resource "tls_private_key" "pvtkey" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "key_details" {
  filename = "/root/key.txt"
  content  = tls_private_key.pvtkey.private_key_pem
}
```

Re-run OpenTofu:

```bash theme={null}
opentofu init
opentofu plan
opentofu apply
# Confirm with "yes"
```

Verify that `/root/key.txt` contains your PEM-encoded private key.

## Cleanup

When you’re done, destroy both resources:

```bash theme={null}
opentofu destroy
# Confirm with "yes"
```

## Explicit Dependency with depends\_on

Create a new directory (e.g., `/root/explicit-dependency`) and add `main.tf`:

```hcl theme={null}
resource "local_file" "krill" {
  filename = "/root/krill.txt"
  content  = "krill"
}

resource "local_file" "whale" {
  filename   = "/root/whale.txt"
  content    = "whale"
  depends_on = [local_file.krill]
}
```

Here, `whale` will only be created after `krill`, illustrating an **explicit dependency** without attribute references.

Apply this configuration:

```bash theme={null}
opentofu init
opentofu plan
opentofu apply
# Enter "yes" to proceed
```

## Links and References

* [OpenTofu CLI Documentation](https://docs.opentofu.org/cli)
* [Terraform TLS Provider](https://registry.terraform.io/providers/hashicorp/tls/latest)
* [OpenTofu GitHub Repository](https://github.com/opentofu/opentofu)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/6e6cebbb-004c-453c-952d-309748451cb4" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/b8e642d8-752e-46a9-9a8e-6c18fe04d3a2" />
</CardGroup>


# Demo Using Variables in OpenTofu

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Demo-Using-Variables-in-OpenTofu/page

Explains how to provide and prioritize input variables in OpenTofu using environment variables, variable files, and command line flags, with examples and troubleshooting

In this lesson you’ll learn how to pass input variables into OpenTofu configurations using environment variables, variable files, and command-line flags. You’ll also see how OpenTofu determines which value to use when multiple sources provide the same variable.

## 1) Using environment variables

To provide an input variable from the environment, export it using the TF\_VAR\_ prefix followed by the variable name. For example, to set a variable named `filename`:

```bash theme={null}
export TF_VAR_filename="/root/baseball.txt"
```

OpenTofu recognizes environment variables that match the `TF_VAR_<name>` pattern and treats them as input values for the root module.

<Callout icon="lightbulb">
  Environment variables set with `TF_VAR_<name>` are convenient for CI or temporary local overrides. They are lower priority than command-line flags, but generally take precedence over variable definition files such as `*.tfvars`.
</Callout>

Use cases for environment variables:

* CI/CD secrets or temporary overrides that you do not want checked into source control.
* Local overrides during development without changing `.tfvars` files.
* Quick testing of alternate inputs.

## 2) Variable definition precedence

When multiple sources supply a value for the same variable, OpenTofu follows a deterministic precedence order. The general precedence (highest to lowest) is:

| Precedence (highest → lowest)         | Source                                                            |
| ------------------------------------- | ----------------------------------------------------------------- |
| 1. Last-specified CLI flags           | `-var` and `-var-file` flags provided on the command line         |
| 2. Environment variables              | `TF_VAR_<name>`                                                   |
| 3. Variable definition files          | `*.tfvars`, `terraform.tfvars`, and `*.auto.tfvars` (auto-loaded) |
| 4. Declared defaults in configuration | `variable "<name>" { default = ... }` in `.tf` files              |

Notes:

* If you pass multiple `-var` or `-var-file` flags, the flag specified last on the command line takes priority among them.
* Auto-loaded `*.auto.tfvars` files are combined; explicit `-var-file` will override values from those files.

## 3) Using a custom variable file with apply

To supply a custom variables file at apply time, use the `-var-file` flag:

```bash theme={null}
tofu apply -var-file=variables.tfvars
```

Because `-var-file` is a CLI flag, its values take precedence over both environment variables and auto-loaded `*.tfvars` files. This is useful when you need an environment-specific or sensitive values file that should override defaults.

## 4) Example project and troubleshooting

Assume the following files exist under `/root/opentofu-projects/variables`:

* `main.tf`
* `variables.tf` (may be missing initially)
* `throw.auto.tfvars`
* `basket.auto.tfvars`
* `terraform.tfvars`

Contents of `main.tf` (a resource that expects a variable `filename`):

```hcl theme={null}
resource "local_file" "games" {
  filename = var.filename
  content  = "football"
}
```

An auto var file `throw.auto.tfvars` might contain:

```hcl theme={null}
filename = "/root/baseball.txt"
```

Troubleshooting: undeclared variable error

If `main.tf` references `var.filename` but the configuration does not declare a `variable "filename" {}` block, running `tofu plan` will warn that a value was found in an auto-loaded file and then error because the input variable is undeclared. Example console output:

```console theme={null}
$ tofu plan
Warning: Value for undeclared variable

The root module does not declare a variable named "filename" but a value was found in file "throw.auto.tfvars". If you meant to use this value, add a "variable" block to the configuration.

Error: Reference to undeclared input variable

on main.tf line 2, in resource "local_file" "games":
  2:   filename = var.filename

An input variable with the name "filename" has not been declared. This variable can be declared with a variable "filename" {} block.
```

Fix: declare the variable in the root module (for example, in `variables.tf`):

```hcl theme={null}
variable "filename" {}
```

You do not need to provide a `default`; declaring the variable allows OpenTofu to accept values from `.tfvars` files, environment variables, or CLI flags. After adding the `variable` block, `tofu plan` will proceed and use the appropriate value according to the precedence rules above.

## 5) Example: command-line `-var` overrides

Passing a value via the CLI `-var` flag overrides values from `.tfvars` files and environment variables:

```bash theme={null}
tofu apply -var 'filename="/root/tennis.txt"'
```

Given these sources:

* `throw.auto.tfvars` contains `filename = "/root/baseball.txt"`
* Environment: `TF_VAR_filename="/root/baseball.txt"`
* Command line: `-var 'filename="/root/tennis.txt"'`

OpenTofu will choose `/root/tennis.txt` because `-var` on the command line has the highest priority.

<Callout icon="warning">
  If you have multiple `.tfvars` files and `*.auto.tfvars` files, remember that auto-loaded files are combined; however explicit `-var-file` or `-var` on the CLI will override those values.
</Callout>

## Summary

* Export variables for quick, ephemeral overrides: `export TF_VAR_<name>=<value>`.
* Always declare variables in the root module with `variable "<name>" {}` to avoid undeclared variable errors.
* Use `tofu apply -var-file=FILE` or `tofu apply -var 'name=value'` to provide or override values at runtime; CLI flags take highest precedence.
* Auto-loaded `*.auto.tfvars` files are convenient for defaults but can be overridden by environment variables and the CLI.

## Links and references

* OpenTofu website: [https://opentofu.org/](https://opentofu.org/)
* OpenTofu documentation: [https://opentofu.org/docs/](https://opentofu.org/docs/)
* Terraform variables documentation (compatible reference for variable behavior): [https://developer.hashicorp.com/terraform/language/values/variables](https://developer.hashicorp.com/terraform/language/values/variables)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/26ad5fda-325b-4fea-9bee-a04aca6b725c" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/69d33f38-4c3a-4d7c-9814-b9565402b14a" />
</CardGroup>
