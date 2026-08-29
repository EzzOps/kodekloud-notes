# What are lifecycle meta arguments

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Lifecycle-Meta-Arguments/What-are-lifecycle-meta-arguments/page

Explains Terraform lifecycle meta-arguments create_before_destroy prevent_destroy and ignore_changes to control resource management during changes.

Lifecycle meta-arguments in Terraform let you control how Terraform manages resources when changes occur. This lesson introduces lifecycle settings and shows how they modify Terraform's default execution behavior during create, update, replace, and delete operations.

Conceptually, lifecycle behavior sits between Terraform and the provider-managed resource: when a resource changes (from your configuration or externally), Terraform normally computes a plan and reconciles the resource. Lifecycle rules let you override parts of that default plan to change replacement strategy, block deletion, or ignore specific attribute changes. Note that lifecycle controls affect Terraform's management behavior — they do not change the resource's runtime behavior in the provider.

Terraform provides three primary lifecycle meta-arguments:

* `create_before_destroy`
* `prevent_destroy`
* `ignore_changes`

<Callout icon="lightbulb">
  Lifecycle settings change how Terraform performs create/replace/delete operations; use them to control replacement order, protect resources, or ignore drift on attributes you don't want Terraform to manage.
</Callout>

## Quick comparison

| Meta-argument           | Purpose                                                                    | Typical use cases                                                            |
| ----------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `create_before_destroy` | Prefer creating the new resource before destroying the old one             | Reduce downtime for replaceable resources (e.g., VMs, load balancer targets) |
| `prevent_destroy`       | Block accidental deletions by failing plans that would remove the resource | Safeguard production DBs, critical S3 buckets, or stateful infrastructure    |
| `ignore_changes`        | Instruct Terraform to ignore changes to specified attributes               | Ignore external controllers, autoscaling changes, or provider-managed fields |

## How lifecycle affects Terraform behavior

Lifecycle rules change how Terraform plans and applies operations, but they do not change the underlying provider resource behavior (for example, how an AWS or GCP service itself behaves at runtime). Some providers or resource types may not support creating new and keeping old resources simultaneously; Terraform will only honor the lifecycle semantics when feasible.

## create\_before\_destroy

By default, Terraform may destroy the old resource before creating the replacement. Setting `create_before_destroy = true` tells Terraform to attempt creating the new resource first, then destroy the old resource only after the new one is successfully created (if the provider supports that workflow).

Example:

```hcl theme={null}
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true
  }
}
```

When to use:

* When you need to minimize downtime during replacement.
* When your provider and resource support multiple concurrent resources (e.g., distinct names or IDs).

Caveats:

* Some resources cannot be created in parallel due to naming constraints or provider limitations; Terraform will only apply `create_before_destroy` when feasible.
* For resources that must be unique (by name or IP), `create_before_destroy` may not be possible.

## prevent\_destroy

`prevent_destroy = true` protects a resource from being removed. If a plan would delete a resource with `prevent_destroy` enabled, Terraform will error instead of performing the deletion.

Example:

```hcl theme={null}
resource "aws_s3_bucket" "important" {
  bucket = "my-important-bucket"

  lifecycle {
    prevent_destroy = true
  }
}
```

<Callout icon="warning">
  `prevent_destroy = true` is a strong safeguard. To remove a protected resource you must explicitly change the configuration (for example, remove the lifecycle block or set `prevent_destroy = false`) and apply the change, or carefully manipulate the state. Avoid manipulating state unless you understand the risks.
</Callout>

When to use:

* Protect production resources such as databases, primary storage buckets, or critical networking resources.
* Prevent accidental deletion during refactoring or automation mistakes.

Notes:

* `prevent_destroy` affects Terraform's plan/apply flow, not the provider's inherent delete safeguards.

## ignore\_changes

`ignore_changes` tells Terraform to ignore changes to one or more resource attributes when planning. This is useful when those attributes are managed outside Terraform (for example, by external controllers, autoscalers, or manual edits) and you do not want Terraform to continually try to revert them.

Example — ignore simple attributes:

```hcl theme={null}
resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"

  tags = {
    Environment = "prod"
  }

  lifecycle {
    ignore_changes = [
      "tags",
      "user_data",
    ]
  }
}
```

Example — ignore nested or list-based attributes (use attribute path strings):

```hcl theme={null}
resource "some_provider_resource" "example" {
  # resource arguments...
  lifecycle {
    ignore_changes = [
      "metadata.0.annotations",  # list-indexed nested attribute
      "spec.0.some_nested_field",
    ]
  }
}
```

Notes:

* Use attribute names or attribute-path strings in the list. For nested/list attributes, specify the path as a string (for example, `"metadata.0.annotations"`).
* Ignored attributes are skipped during diff calculations and Terraform will not plan changes to them; other non-ignored attributes continue to be reconciled normally.

When to NOT use:

* Do not use `ignore_changes` as a substitute for proper resource ownership. If Terraform should be the authoritative manager of a field, do not ignore it.
* Overusing `ignore_changes` can hide configuration drift and complicate troubleshooting.

## Examples and patterns

* Minimal downtime replacement:
  Use `create_before_destroy = true` on resources that can exist concurrently (e.g., some compute instances, DNS records if using a separate name).
* Protecting stateful services:
  Add `prevent_destroy = true` to databases, storage buckets, or identity resources where accidental deletion would be catastrophic.
* Handling external controllers:
  Use `ignore_changes` for fields managed by external systems (service mesh injections, autoscaling group sizes managed by an autoscaler, etc.).

## Summary

* Lifecycle meta-arguments change how Terraform manages resources during create/replace/delete operations.
* They affect Terraform's management and planning behavior, not the provider's runtime behavior.
* Use `create_before_destroy` to prefer new-before-old replacement, `prevent_destroy` to block accidental deletions, and `ignore_changes` to avoid reconciling attributes managed externally.
* Apply lifecycle rules thoughtfully — they can prevent outages, but misusing them can hide drift or block legitimate changes.

References:

* [Terraform: lifecycle meta-argument documentation](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-on-azure/module/82cd6352-f026-4f6f-b739-634e56558de4/lesson/c2e6ac7f-71ed-4339-bb30-1cf2117f1e09" />
</CardGroup>
