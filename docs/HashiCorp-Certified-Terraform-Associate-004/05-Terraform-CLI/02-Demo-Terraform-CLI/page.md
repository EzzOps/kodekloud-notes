# Demo Terraform CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Terraform-CLI/Demo-Terraform-CLI/page

Walks through an end-to-end Terraform CLI workflow using the random provider, covering create, format, init, plan, apply, inspect state and destroy resources.

This lesson walks through common Terraform CLI commands using a minimal configuration and the `random` provider. You’ll learn the typical Terraform local workflow: create a configuration, format it, initialize providers, plan changes, apply them, inspect state, and destroy resources. These same CLI steps apply when working with real cloud providers, though provider-specific behavior and execution times will differ.

Setup: open an empty directory in [VS Code](https://code.visualstudio.com/) and create a file named `main.tf`.

## 1) Check Terraform version

Confirm the installed Terraform version before you begin.

```bash theme={null}
$ terraform version
Terraform v1.10.5
on darwin_arm64
```

## 2) Create a minimal configuration

Add the [random provider](https://registry.terraform.io/providers/hashicorp/random/latest), a `random_pet` resource, and an output to `main.tf`. The `random` provider generates values locally and does not call external APIs.

main.tf:

```hcl theme={null}
provider "random" {}

resource "random_pet" "name" {
  length = 2
}

output "random_pet_name" {
  value = random_pet.name.id
}
```

## 3) Format the configuration

Use `terraform fmt` to format all HCL files in the working directory.

```bash theme={null}
$ terraform fmt
```

## 4) Initialize the working directory

`terraform init` initializes the working directory, downloads provider plugins, and configures the backend (if one is configured).

```bash theme={null}
$ terraform init
Initializing the backend...
Initializing provider plugins...
- Finding latest version of hashicorp/random...
- Installing hashicorp/random v3.6.3...
Terraform has been successfully initialized!
```

After `init`, Terraform creates a `.terraform` directory with installed provider plugins. The binary layout may vary by Terraform version and OS.

<Frame>
  <img alt="The image shows a Visual Studio Code window with a file named &#x22;terraform-provider-random_v3.6.3_x5&#x22; highlighted in the Explorer. A warning indicates the file is not displayed due to unsupported text encoding, and the terminal below contains Terraform-related instructions." />
</Frame>

<Callout icon="lightbulb">
  The `.terraform` directory and provider plugin binaries are local artifacts for this working directory. They are safe to ignore in version control (add them to `.gitignore`).
</Callout>

## 5) Validate the configuration

`terraform validate` checks HCL syntax and basic semantics.

Valid example:

```bash theme={null}
$ terraform validate
Success! The configuration is valid.
```

Common validation error — undeclared reference:

```hcl theme={null}
