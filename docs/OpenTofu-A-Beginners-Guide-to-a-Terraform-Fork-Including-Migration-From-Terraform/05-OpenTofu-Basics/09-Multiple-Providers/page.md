# aws_key_pair.alpha:
resource "aws_key_pair" "alpha" {
  arn         = "arn:aws:ec2:us-east-1::key-pair/alpha"
  fingerprint = "d7:ff:a6:63:18:64:9c:57:a1:ee:ca:a4:ad:c2:81:62"
  id          = "alpha"
  key_name    = "alpha"
  public_key  = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC3...Ov"
  tags_all    = {}
}

# aws_key_pair.beta:
resource "aws_key_pair" "beta" {
  arn         = "arn:aws:ec2:ca-central-1::key-pair/beta"
  fingerprint = "d7:ff:a6:63:18:64:9c:57:a1:ee:ca:a4:ad:c2:81:62"
  id          = "beta"
  key_name    = "beta"
  public_key  = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC3...Ov"
  tags_all    = {}
}
```

Here, `alpha` appears in **us-east-1** (default) and `beta` in **ca-central-1** (aliased).

## 6. Resource–Provider Mapping

| Resource             | Provider Block      | Region       |
| -------------------- | ------------------- | ------------ |
| aws\_key\_pair.alpha | aws (default)       | us-east-1    |
| aws\_key\_pair.beta  | aws.central (alias) | ca-central-1 |

<Callout icon="triangle-alert">
  Make sure your AWS credentials have permissions for each region or profile you target. Missing credentials can cause resource creation failures.
</Callout>

## Links and References

* [OpenTofu Provider Aliases](https://docs.opentofu.io/configuration/providers/#provider-aliases)
* [AWS Regions and Availability Zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)
* [Terraform Providers Documentation](https://www.terraform.io/docs/language/providers/configuration.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/8c04d4c3-0f65-454a-95b3-b95dcdc21e6a" />
</CardGroup>


# Multiple Providers

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Multiple-Providers/page

This guide explains how to use multiple Providers in a single OpenTofu configuration for provisioning resources across different platforms.

In this guide, we’ll show you how to use multiple Providers in a single OpenTofu (a Terraform-compatible tool) configuration. By combining Providers, you can provision resources across different platforms—local files, random data generators, AWS, and more—all within one `main.tf`.

## Prerequisites

* OpenTofu CLI installed (see [OpenTofu Installation](https://opentofu.org/docs/installation)).
* A working directory with an existing `main.tf` and an initialized backend.

## Defining Multiple Resources

Extend your `main.tf` by adding a `random_pet` resource alongside the existing `local_file`:

```hcl theme={null}
resource "local_file" "pet" {
  filename = "/root/pets.txt"
  content  = "We love pets!"
}

resource "random_pet" "my-pet" {
  prefix    = "Mrs"
  separator = "."
  length    = 1
}
```

<Callout icon="lightbulb">
  Whenever you introduce a new Provider (e.g., the `random` provider here), you must reinitialize your configuration so OpenTofu can download or reuse the required plugin.
</Callout>

## Initializing Providers

Run:

```bash theme={null}
tofu init
```

Sample output:

```plaintext theme={null}
Initializing the backend...

Initializing provider plugins...
- Reusing hashicorp/local from .terraform.lock.hcl
- Finding latest version of hashicorp/random...
- Installing hashicorp/random v3.6.0...
- Installed hashicorp/random v3.6.0

OpenTofu has been successfully initialized!
```

<Callout icon="triangle-alert">
  Review changes in your `.terraform.lock.hcl` after `tofu init`. Commit updates only if they match your intended dependency versions.
</Callout>

## Planning and Applying Changes

First, generate and inspect the execution plan:

```bash theme={null}
tofu plan
```

Then apply the proposed changes:

```bash theme={null}
tofu apply
```

Table: Common OpenTofu Commands

| Command    | Purpose                              | Example                 |
| ---------- | ------------------------------------ | ----------------------- |
| tofu init  | Initialize backend & providers       | `tofu init`             |
| tofu plan  | Preview changes without applying     | `tofu plan -out=tfplan` |
| tofu apply | Apply changes to reach desired state | `tofu apply tfplan`     |

## Example Execution Output

```plaintext theme={null}
local_file.pet: Refreshing state... [id=...]
random_pet.my-pet: Creating...
random_pet.my-pet: Creation complete after 0s [id=Mrs.hen]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

The `random_pet` resource simply generates a random name, exposed as its `id` attribute—no real infrastructure is provisioned.

## Chaining Resources Across Providers

You can reference one resource’s attribute in another, even if they come from different Providers. For example, generate a random string to tag an AWS EC2 instance:

```hcl theme={null}
resource "random_string" "server-suffix" {
  length  = 6
  upper   = false
  special = false
}

resource "aws_instance" "web" {
  ami           = "ami-06178cf087598769c"
  instance_type = "m5.large"
  tags = {
    Name = "web-${random_string.server-suffix.id}"
  }
}
```

When you run `tofu apply`, OpenTofu will:

1. Create the random string.
2. Launch an EC2 instance tagged with `web-<generated-suffix>`.

Linking resources in this way lets you orchestrate complex, multi-provider deployments from a single `.tf` file.

## References

* [OpenTofu Documentation](https://opentofu.org/docs/)
* [Provider Signing](https://opentofu.org/docs/cli/plugins/signing/)
* [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
* [HashiCorp Random Provider](https://registry.terraform.io/providers/hashicorp/random/latest)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/60de153e-0f0d-4bd5-b14d-83dbd1d45729" />
</CardGroup>
