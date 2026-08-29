# terragrunt.hcl
terraform {
  source = "tfr://<namespace>/<module_name>/<provider>"
}
```

| Element      | Description                                  | Example               |
| ------------ | -------------------------------------------- | --------------------- |
| namespace    | Author or organization publishing the module | terraform-aws-modules |
| module\_name | Identifier for the module                    | vpc                   |
| provider     | Cloud provider name                          | aws                   |

Example:

```hcl theme={null}
terraform {
  source = "tfr://terraform-aws-modules/vpc/aws"
}
```

## 2. Initializing the Configuration

Run the following command to download and prepare the module in your working directory:

```bash theme={null}
terragrunt init
```

This initializes your Terragrunt configuration and fetches the specified module from the Terraform Registry.

## 3. Pinning a Module Version

To guarantee reproducible builds and avoid unintended upgrades, specify a version constraint:

```hcl theme={null}
terraform {
  source  = "tfr://terraform-aws-modules/vpc/aws"
  version = "~> 3.0"
}
```

Modules in the Registry follow semantic versioning. Locking to `~> 3.0` ensures you get all non-breaking updates in the 3.x series.

## 4. Updating to the Latest Matching Version

When you’re ready to pull in the newest matching release (within your version constraint), use:

```bash theme={null}
terragrunt get --update
```

This command refreshes your local copy of the module, incorporating any fixes or enhancements.

## 5. Security and Best Practices

> **triangle-alert** Always verify the module’s publisher and review its source code before applying in production. Prefer modules marked as **Verified** or provided by official vendors to reduce risk.

* Review module inputs, outputs, and provisioners for security compliance.
* Check the [Terraform Registry](https://registry.terraform.io) page for the module’s documentation and changelog.
* Use version pinning to control when features and fixes are introduced.

## Links and References

* [Terraform Registry](https://registry.terraform.io)
* [Terragrunt Documentation](https://terragrunt.gruntwork.io/)
* [Terraform Modules Best Practices](https://www.terraform.io/docs/language/modules/develop/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/terragrunt-for-beginners/module/4d4cda50-7d42-4622-b0d4-fa6e6ce0a16d/lesson/0d9390cd-e0d4-4e5f-af6f-00a2e9bf6d3b)


# Wrapper Module Approach

Source: https://notes.kodekloud.com/docs/Terragrunt-for-Beginners/Terragrunt-Modules/Wrapper-Module-Approach/page

This article discusses the wrapper module approach in Terraform for enforcing organizational standards while reusing community modules.

The **wrapper module pattern** builds on top of existing community modules, enabling you to enforce organizational standards while reusing battle-tested code. This approach reduces maintenance overhead, maintains upstream compatibility, and ensures consistency across environments.

## Why Use Wrapper Modules?

* **Consistency**\
  Enforce company-wide naming conventions, tag policies, and resource configurations through standardized inputs.
* **Scoped Customization**\
  Override only the settings you need, leaving the underlying community module intact for easier upstream upgrades.
* **Maintainability**\
  Minimize drift from official releases by wrapping instead of forking—updating to new versions becomes straightforward.

## Common Use Cases

| Use Case                        | Description                                                                                        |
| ------------------------------- | -------------------------------------------------------------------------------------------------- |
| Standardizing Inputs            | Enforce naming conventions, tagging policies, or sizing guidelines for all deployments.            |
| Adding Defaults                 | Provide default values for certain inputs (e.g., instance types, region) while allowing overrides. |
| Injecting Organization Settings | Preconfigure logging levels, monitoring hooks, or security controls across all modules.            |

## Implementation Example

1. Create your wrapper module directory:\
   `modules/my-wrapper/`

2. In `modules/my-wrapper/main.tf`, call the community module and map your inputs:

```hcl theme={null}
