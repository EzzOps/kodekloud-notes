# aws_instance.web has changed
~ resource "aws_instance" "web" {
    ~ ebs_optimized = false -> true
    ~ id            = "i-0c4192b0347156b5c"
    ~ instance_type = "t2.small" -> "t3.small"
    ~ tags = {
        "Environment" = "development"
        "Name"        = "web-server"
        + "Team"       = "dev-app-01"
      }
  }
```

Key observations:

* `instance_type` changed from `t2.small` to `t3.small`.
* A new tag `Team = dev-app-01` appears.
* Some attributes (e.g., `ebs_optimized`, CPU/thread counts) can change when switching instance families — these are provider-driven differences.

## Two ways to resolve detected drift

You have two primary options after detecting drift. The best choice depends on whether you want configuration to be the source of truth or whether you want to accept the out-of-band changes.

| Option                                 | Action                                                                                        | Command                         | Outcome                                                                                      |
| -------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------- |
| Revert provider to match configuration | Make real infrastructure match Terraform code (configuration is source of truth)              | `terraform apply`               | Terraform will modify resources to match your configuration (may restart/replace resources). |
| Accept provider changes into state     | Update Terraform state to reflect current provider attributes without changing infrastructure | `terraform apply -refresh-only` | Terraform updates the state file only; no provider-side changes are made.                    |

1. Revert manual changes to match Terraform (enforce code)

* Run a regular apply to make real resources match your configuration:

```bash theme={null}
terraform apply
```

Terraform will show and apply a plan that changes the EC2 instance back to the configured `instance_type` and removes tags not present in your code.

2. Accept manual changes into Terraform state (no infra changes)

* Use the apply refresh-only option to update state to match the provider:

```bash theme={null}
terraform apply -refresh-only
```

Terraform will refresh resource attributes and prompt to update the state. Confirm with `yes` to accept.

<Frame>
  <img alt="The image displays a code editor window with a Terraform project, showing a terminal prompt asking to update the Terraform state to reflect detected changes." />
</Frame>

After accepting the refresh-only apply, Terraform updates the state file without adding/changing/destroying resources:

```plaintext theme={null}
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

Example excerpt from the refreshed state (JSON) showing the updated instance type and tags:

```json theme={null}
{
  "resources": [
    {
      "instances": [
        {
          "id": "i-0c4192b0347156b5c",
          "instance_state": "running",
          "instance_type": "t3.small",
          "tags": {
            "Environment": "development",
            "Name": "web-server",
            "Team": "dev-app-01"
          },
          "tags_all": {
            "Environment": "development",
            "Name": "web-server",
            "Team": "dev-app-01"
          }
        }
      ]
    }
  ]
}
```

## Keep configuration and state in sync

If you accepted the provider-side changes into state and want those changes to persist, update your Terraform configuration accordingly:

* Update the `instance_type` variable default:

```hcl theme={null}
variable "instance_type" {
  description = "The instance type for the EC2 instance"
  type        = string
  default     = "t3.small"
}
```

* Add the new `Team` tag to the resource's `tags` block:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.private.id
  tags = {
    Name        = "web-server"
    Environment = "development"
    Team        = "dev-app-01"
  }
}
```

Then format and apply your updated configuration:

```bash theme={null}
terraform fmt
terraform apply
```

If your configuration, state, and provider are aligned, Terraform reports no changes:

```plaintext theme={null}
No changes. Your infrastructure matches the configuration
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

<Callout icon="lightbulb">
  Use `terraform plan -refresh-only` to detect drift. To accept external changes into state without modifying resources, use `terraform apply -refresh-only`. To make real infrastructure match your code (configuration as source of truth), run a normal `terraform apply`.
</Callout>

## Links and references

* [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)
* [Terraform state guide](https://developer.hashicorp.com/terraform/language/state)
* [AWS EC2 documentation](https://docs.aws.amazon.com/ec2/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/2470872e-2566-4903-992b-b9fedc8c5739/lesson/070b7662-52e9-4ac4-a710-b22b32f02abb" />
</CardGroup>


# Demo Inspecting Terraform State using the CLI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Understading-and-Managing-Terraform-State/Demo-Inspecting-Terraform-State-using-the-CLI/page

Inspect Terraform state from the CLI using state list, state show, and show to view resource IDs, network attributes, tags, and full state dumps

In this lesson you'll learn how to inspect Terraform state from the CLI. This is useful when you need to verify concrete resource IDs, network attributes, tags, or other values that Terraform has recorded after apply. The primary commands demonstrated here are:

* `terraform state list` — enumerate resource addresses stored in the state.
* `terraform state show` — display detailed attributes for a single resource from the state.
* `terraform show` — render the full state (or a saved plan file) in a human-readable format.

<Callout icon="lightbulb">
  Use `terraform state list` to discover resource addresses, then pass one of those addresses to `terraform state show` to inspect that resource in detail.
</Callout>

## Quick command reference

| Command                          | Purpose                                                    | Example                                       |
| -------------------------------- | ---------------------------------------------------------- | --------------------------------------------- |
| `terraform state list`           | List all resource addresses recorded in the state          | `terraform state list`                        |
| `terraform state show <address>` | Show detailed attributes for a single resource             | `terraform state show aws_instance.web`       |
| `terraform show [planfile]`      | Dump the full state or a saved plan in human-readable form | `terraform show` or `terraform show plan.out` |

## 1. List resources in state

Begin by listing every resource Terraform currently manages in your state:

```bash theme={null}
$ terraform state list
aws_instance.web
aws_subnet.private
aws_subnet.public
aws_vpc.main
$
```

This output lists resource addresses you can use as arguments to `terraform state show`. The addresses reflect the resource type and name from your configuration (for example, `aws_instance.web`).

## 2. Inspect the entire state (or a saved plan)

When you want a full dump of state data or want to inspect a saved plan file, use `terraform show`. This prints resource blocks with all recorded attributes:

```bash theme={null}
$ terraform show
