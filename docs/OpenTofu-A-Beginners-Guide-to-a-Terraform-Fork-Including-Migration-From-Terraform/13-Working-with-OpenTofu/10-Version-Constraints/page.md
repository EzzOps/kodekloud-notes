# Version Constraints

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/Working-with-OpenTofu/Version-Constraints/page

Explains how to pin and constrain OpenTofu provider versions, use the pessimistic operator, and commit lock files to ensure reproducible, stable deployments.

In this lesson we cover provider versions and version constraints in OpenTofu. Providers are published to the public registry and distributed as plugins. By default, running `tofu init` downloads the latest provider versions required by your configuration, but pinning or constraining versions is important to maintain reproducible, stable deployments.

## Example resource

This simple example uses the `local` provider to write to a file:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

## Default behavior of `tofu init`

When you run `tofu init`, OpenTofu locates and installs provider plugins. By default it selects the latest compatible versions and records those selections in a lock file:

```text theme={null}
$ tofu init

Initializing the backend...

Initializing provider plugins...
 - Finding latest version of hashicorp/local...
 - Installing hashicorp/local v2.4.1...
 - Installed hashicorp/local v2.4.1 (signed, key ID 0C0AF313E5FD9F80)

Providers are signed by their developers.

If you'd like to know more about provider signing, you can read about it here:
https://opentofu.org/docs/cli/plugins/signing/

OpenTofu has created a lock file .terraform.lock.hcl to record the provider
selections it made above.

Include this file in your version control repository so that OpenTofu can
guarantee the same selections by default when you run "tofu init" in the future.

OpenTofu has been successfully initialized!
```

> **lightbulb** Include the generated .terraform.lock.hcl in version control to ensure consistent provider selection across runs and machines.

Because provider behavior may change between releases, you should explicitly pin or constrain provider versions to protect your configuration from unexpected changes.

## Pinning an exact provider version

To pin a provider to a single specific version, declare it in the `terraform` block using `required_providers` with `source` and `version`:

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "2.3.0"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

Running `tofu init` with that configuration installs the exact version you requested:

```bash theme={null}
$ tofu init

Initializing the backend...

Initializing provider plugins...
 - Finding latest version of hashicorp/local...
 - Installing hashicorp/local v2.3.0...
 - Installed hashicorp/local v2.3.0 (signed, key ID 0C0AF313E5FD9F80)

OpenTofu has created a lock file .terraform.lock.hcl to record the provider
selections it made above.

OpenTofu has been successfully initialized!
```

## Using version constraints

If you want flexibility while still controlling upgrades, use version constraints. The `version` attribute accepts constraint expressions similar to common package managers.

Examples below show how to express different constraints while using the same `local_file` resource.

1. Not-equal constraint (`!=`)

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "!= 2.4.1"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

This tells OpenTofu to avoid version 2.4.1; it will select the newest available version that does not match the excluded version.

2. Less-than or greater-than constraints

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "< 2.4.1"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

This requires a version strictly less than 2.4.1 (for example 2.4.0 or earlier).

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "> 2.3.0"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

This requires a version strictly greater than 2.3.0 (for example 2.3.1, 2.4.0, etc., when available).

3. Combining constraints (comma-separated)

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "> 2.2.3, < 2.4.1, != 2.4.0"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

This allows versions greater than 2.2.3 and less than 2.4.1 but explicitly excludes 2.4.0. OpenTofu will pick the highest available version that satisfies all constraints (for example, 2.3.0).

## The pessimistic operator (\~>)

The pessimistic operator `~>` is useful when you want to allow non-breaking updates but prevent potentially breaking ones. Its behavior depends on the specificity of the version you supply.

1. `~> 2.2`

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.2"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

`~> 2.2` is equivalent to ">= 2.2.0, \< 3.0.0" — this permits any 2.x version at or above 2.2.0 (2.2.1, 2.3.0, 2.4.1, etc.) but prevents upgrades to 3.x.

2. `~> 2.2.0`

```hcl theme={null}
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.2.0"
    }
  }
}

resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}
```

`~> 2.2.0` is equivalent to ">= 2.2.0, \< 2.3.0" — this allows patch-level updates within the 2.2 series, but not newer minor versions (2.3.x or later).

## Quick reference: constraint operators

| Operator       | Meaning                                         | Example                        |
| -------------- | ----------------------------------------------- | ------------------------------ |
| exact          | Pin to a single version                         | `version = "2.3.0"`            |
| !=             | Exclude a specific version                      | `version = "!= 2.4.1"`         |
| \<, \<=, >, >= | Range comparisons                               | `version = "< 2.4.1"`          |
| , (comma)      | Combine multiple constraints                    | `version = "> 2.2.3, < 2.4.1"` |
| \~>            | Pessimistic operator (allow compatible updates) | `version = "~> 2.2.0"`         |

## Best practices

* Use an exact version when you require strict reproducibility across environments.
* Use range comparisons or the pessimistic operator to permit safe, non-breaking updates while avoiding unintended major upgrades.
* Exclude known-broken versions with `!=` when necessary.
* Always commit `.terraform.lock.hcl` to version control so subsequent runs use the same provider selections.

> **warning** When adjusting provider constraints, test upgrades in a staging environment before applying changes in production. Provider releases can introduce behavior changes even when the API surface looks compatible.

## Links and references

* OpenTofu CLI plugins and provider signing: [https://opentofu.org/docs/cli/plugins/signing/](https://opentofu.org/docs/cli/plugins/signing/)
* OpenTofu documentation: [https://opentofu.org/docs/](https://opentofu.org/docs/)
* Provider registry (examples and discovery): [https://registry.opentofu.org/](https://registry.opentofu.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/69432d48-55d0-4340-a56d-9f9a7819d26c/lesson/12d63e59-cf59-4df8-bfa8-3216cae1d003)
