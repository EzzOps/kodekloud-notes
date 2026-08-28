# Confirm with "yes"
```

After success:

```plaintext theme={null}
local_file.jedi: Creating...
local_file.jedi: Creation complete after 0s [id=...]
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

Verify the file:

```bash theme={null}
cat /root/first-jedi
# phanius
```

***

That’s it for this lab. Thank you for following along!

## Links and References

* [Terraform Variables Documentation](https://developer.hashicorp.com/terraform/language/values/variables)
* [OpenTofu GitHub Repository](https://github.com/OpenTofu)
* [Terraform Local Provider](https://registry.terraform.io/providers/hashicorp/local/latest)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/2fd9cf67-3105-4688-bc49-25da6c99e3f3" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/84672ea0-e48d-476e-b0c2-aea7a86a732a" />
</CardGroup>


# Multiple Providers Part 2Aliases

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Multiple-Providers-Part-2Aliases/page

Learn to configure multiple AWS providers in OpenTofu using aliases for deploying resources across different regions or accounts without repeating configurations.

In this lesson, you’ll learn how to configure multiple AWS providers in a single OpenTofu setup using provider aliases. This lets you deploy resources—such as EC2 key pairs—to different regions (or accounts) without repeating your configuration.

## 1. Declare Your Resources

First, define two AWS EC2 key pairs named `alpha` and `beta`:

```hcl theme={null}
resource "aws_key_pair" "alpha" {
  key_name   = "alpha"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAAADAQABAAABQD3...alpha@a-server"
}

resource "aws_key_pair" "beta" {
  key_name   = "beta"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAAADAQABAAABQD3...beta@b-server"
}
```

By default, both resources will target the same AWS provider.

## 2. Configure the Default Provider

Specify the default AWS provider region:

```hcl theme={null}
provider "aws" {
  region = "us-east-1"
}
```

At this point, both `aws_key_pair.alpha` and `aws_key_pair.beta` will be created in **us-east-1**.

## 3. Add an Aliased Provider

To deploy `beta` in a different region, add a second provider block with an `alias`:

```hcl theme={null}
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "central"
  region = "ca-central-1"
}
```

* The first block remains the **default** (`us-east-1`).
* The second block is identified by `alias = "central"` and targets **ca-central-1**.

## 4. Assign the Aliased Provider to a Resource

Use the `provider` meta-argument within your resource to select the aliased provider:

```hcl theme={null}
resource "aws_key_pair" "beta" {
  provider   = aws.central
  key_name   = "beta"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAAADAQABAAABQD3...beta@b-server"
}
```

* `alpha` continues to use the **default** AWS provider (`us-east-1`).
* `beta` now uses the **aws.central** provider (`ca-central-1`).

<Callout icon="lightbulb">
  Provider aliases are ideal for multi-region or multi-account strategies in a single configuration. You can also combine aliases with workspaces or backends for more complex deployments.
</Callout>

## 5. Verify with `tofu show`

After running `tofu apply`, inspect your deployed resources:

```bash theme={null}
$ tofu show
