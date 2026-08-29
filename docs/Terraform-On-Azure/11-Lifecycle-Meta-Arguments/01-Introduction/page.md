# Introduction

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Lifecycle-Meta-Arguments/Introduction/page

Summarizes Terraform lifecycle meta-arguments and usage to reduce downtime, prevent accidental deletion, and ignore external attribute changes for controlled resource lifecycle behavior.

In this article we move beyond basic resource definitions to focus on how Terraform controls resource lifecycle behavior during create, update, and destroy operations. Understanding lifecycle meta-arguments helps you enforce safety, reduce downtime, and align Terraform's behavior with operational requirements.

Learning objectives:

* Understand what lifecycle meta-arguments are and how they modify Terraform's default behavior.
* Learn how `create_before_destroy` changes the replacement strategy to reduce downtime.
* Learn how `prevent_destroy` acts as a safety mechanism to block accidental deletions.
* Learn how `ignore_changes` lets Terraform ignore specified attribute changes during plans and applies.

By the end of this article you will be able to use lifecycle meta-arguments to shape resource lifecycle semantics to match production requirements.

## What are lifecycle meta-arguments?

Lifecycle meta-arguments are specified in a `lifecycle` block inside a resource. They change Terraform’s default replacement and update behavior on a per-resource basis, enabling fine-grained control over create/update/destroy semantics.

Common lifecycle meta-arguments:

| Meta-argument           |                                                                               What it does | Typical use case                                                                     |
| ----------------------- | -----------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------ |
| `create_before_destroy` |                       Create the replacement resource first, then destroy the old resource | Reduce downtime for resources that can coexist temporarily                           |
| `prevent_destroy`       |                                      Treat any planned destroy of the resource as an error | Protect critical resources (databases, production S3 buckets, IAM roles)             |
| `ignore_changes`        | Tell Terraform to ignore specified attributes when comparing configuration to actual state | Ignore provider- or automation-managed fields (e.g., tags updated outside Terraform) |

Example `lifecycle` block structure:

```hcl theme={null}
resource "aws_example" "foo" {
  # resource arguments ...

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
    ignore_changes        = ["tags"]
  }
}
```

For more details, see the Terraform documentation on lifecycle meta-arguments: [https://www.terraform.io/docs/language/meta-arguments/lifecycle](https://www.terraform.io/docs/language/meta-arguments/lifecycle)

## create\_before\_destroy

Default replacement strategy: when a resource requires replacement, Terraform typically destroys the existing resource first and then creates the new one. For resources that cannot be recreated with the same identifiers (name, IP, etc.), this destroy-first behavior can cause downtime.

Setting `create_before_destroy = true` flips the replacement order so Terraform attempts to create the new resource before destroying the old one. This reduces downtime for many resources that can coexist temporarily.

Example:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.micro"
  tags = {
    Name = "web-server"
  }

  lifecycle {
    create_before_destroy = true
  }
}
```

Notes and caveats:

* Provider constraints: Not all resources can live side-by-side. If a provider or resource type requires a unique identifier (for example, a unique DNS name), a create-before-destroy replacement may not be possible and the provider will fall back to destroying first.
* Stateful services: `create_before_destroy` can be useful for stateful services when brief overlap is acceptable, but you must evaluate application-level consistency (for example, database replication or cluster reconfiguration).
* Plan visibility: Terraform will show a replacement plan that includes a create action followed by a destroy action. Review the plan carefully before applying.

## prevent\_destroy

`prevent_destroy = true` makes any planned destroy of the resource fail the plan/apply with an error. This is a defensive setting to protect critical resources from accidental deletion.

Example:

```hcl theme={null}
resource "aws_s3_bucket" "important" {
  bucket = "my-critical-bucket"

  lifecycle {
    prevent_destroy = true
  }
}
```

> **warning** `prevent_destroy` will block any planned destroy, including `terraform destroy` for that resource. To remove such a resource you must first remove or change the `prevent_destroy` setting and then run `terraform apply`. Do not rely on it as the only form of protection — combine with IAM and organizational safeguards.

## ignore\_changes

`ignore_changes` tells Terraform to treat specified attributes as if they had not changed when diffing configuration vs. real-world infrastructure. This is helpful when attributes are managed outside Terraform, by provider automation, or by separate tooling.

Example:

```hcl theme={null}
resource "aws_instance" "app" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.medium"
  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }

  lifecycle {
    ignore_changes = [
      "tags",         # ignore any changes to the whole tags map
      "user_data",    # ignore changes in user_data
    ]
  }
}
```

Important notes:

* Attribute paths: `ignore_changes` accepts a list of attribute paths. Use dot notation for nested attributes (for example, `"metadata.0.name"` for certain resources), and quoted strings inside the list for each path.
* Granularity: Avoid ignoring entire maps unless necessary. Overusing `ignore_changes` can hide drift and lead to unmanaged differences between configuration and actual resources. If you only need to ignore specific map keys (e.g., one tag), prefer provider tag management features or targeted attribute paths if supported.
* Workflow: When a resource has `ignore_changes`, Terraform will still read the real state but will suppress diffs for the specified attributes, so no update will be planned for those attributes even if they differ.

> **lightbulb** Best practice: Use lifecycle meta-arguments sparingly and document their intent. They are powerful tools to align Terraform behavior with operational realities but can also mask drift or create surprising behavior if used without care.

## Combining lifecycle arguments

Multiple lifecycle settings can be combined in the same resource. Be aware they can interact or conflict.

Example:

```hcl theme={null}
resource "aws_db_instance" "db" {
  identifier     = "prod-db"
  instance_class = "db.t3.medium"
  # other arguments...

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = ["tags"]
  }
}
```

Important interaction notes:

* Conflicts: `create_before_destroy` aims to create a replacement before destroying the existing resource. If `prevent_destroy = true` is also set, the subsequent destroy step will be blocked, preventing the replacement from completing. Test such combinations in non-production environments.
* Provider behavior: Always validate provider-specific constraints. Some providers may ignore `create_before_destroy` for certain resource types or require additional configuration to allow parallel resources.

## Quick reference

| Lifecycle setting       | Default | Effect when enabled                                     |
| ----------------------- | ------: | ------------------------------------------------------- |
| `create_before_destroy` | `false` | Tries to create replacement first, then destroy old one |
| `prevent_destroy`       | `false` | Blocks any destroy of the resource                      |
| `ignore_changes`        |    `[]` | Suppresses diffs for listed attributes                  |

## Summary

Lifecycle meta-arguments let you:

* Reduce downtime with `create_before_destroy`.
* Protect critical resources with `prevent_destroy`.
* Avoid noisy diffs for provider- or externally-managed attributes with `ignore_changes`.

Use these options carefully, test in lower environments, and document why each lifecycle setting is present so your team understands the operational reasoning behind them.

## Links and References

* Terraform lifecycle meta-arguments: [https://www.terraform.io/docs/language/meta-arguments/lifecycle](https://www.terraform.io/docs/language/meta-arguments/lifecycle)
* Terraform documentation: [https://www.terraform.io/docs/](https://www.terraform.io/docs/)
* Best practices and provider docs (example — AWS): [https://registry.terraform.io/providers/hashicorp/aws/latest/docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-on-azure/module/82cd6352-f026-4f6f-b739-634e56558de4/lesson/7c6f8401-272d-4b89-8fd4-abab580d7cf4)
