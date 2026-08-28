# aws_key_pair.alpha:
resource "aws_key_pair" "alpha" {
  arn         = "arn:aws:ec2:us-east-1:key-pair/alpha"
  fingerprint = "d7:ff:a6:63:18:64:9c:57:a1:ee:ca:a4:ad:c2:81:62"
  id          = "alpha"
  key_name    = "alpha"
  public_key  = "ssh-rsa AAAAB3NzaC1yc2EAAAAADAQABAAABAQD3F6ty... alpha@a-server"
  tags_all    = {}
}
```

| Attribute   | Description                                      |
| ----------- | ------------------------------------------------ |
| arn         | Amazon Resource Name for the key pair            |
| fingerprint | SHA1 fingerprint of the public key               |
| id          | Unique identifier (same as `key_name`)           |
| key\_name   | Name assigned to the key pair                    |
| public\_key | SSH public key supplied by the user              |
| tags\_all   | Combined map of resource and provider-level tags |

<Callout icon="lightbulb">
  You can target a specific resource by running `tofu show aws_key_pair.alpha`.\
  Learn more in the \[OpenTofu CLI Docs].
</Callout>

## Referencing Exported Attributes

Exported attributes become inputs for other resources. For instance, associate the key pair with an EC2 instance:

```hcl theme={null}
resource "aws_instance" "cerberus" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = aws_key_pair.alpha.key_name
}
```

The reference `aws_key_pair.alpha.key_name` follows the format:

```text theme={null}
resource_type.resource_name.attribute
```

This creates an **implicit dependency**, ensuring `aws_key_pair.alpha` is created before `aws_instance.cerberus`.

## Implicit Dependencies in Action

When you run `tofu apply`, OpenTofu will build the dependency graph and provision resources in the correct order:

```bash theme={null}
$ tofu apply
aws_key_pair.alpha: Creating...
aws_key_pair.alpha: Creation complete after 1s [id=alpha]
aws_instance.cerberus: Creating...
aws_instance.cerberus: Creation complete after 10s [id=i-c791dc46a6639d4a7]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed
```

During `tofu destroy`, the reverse order is applied: the EC2 instance is terminated before the key pair.

<Callout icon="lightbulb">
  Implicit dependencies eliminate race conditions and ensure resources are created or destroyed in the correct sequence.\
  Read more about the \[AWS Provider] for detailed attribute information.
</Callout>

## Explicit Dependencies with `depends_on`

If resources lack direct attribute references but still require ordering, use the `depends_on` meta-argument:

```hcl theme={null}
resource "aws_instance" "db" {
  ami           = var.db_ami
  instance_type = var.db_instance_type
}

resource "aws_instance" "web" {
  ami           = var.web_ami
  instance_type = var.web_instance_type

  depends_on = [
    aws_instance.db
  ]
}
```

Here, `aws_instance.web` will wait for `aws_instance.db` to finish creation first.

<Callout icon="triangle-alert">
  Overusing `depends_on` can complicate your configuration. Prefer implicit references whenever possible.\
  For advanced dependency control, see the \[Infrastructure as Code] best practices.
</Callout>

***

That’s it for this lesson on resource attributes and dependencies in OpenTofu. In the next module, we’ll cover **outputs** and **remote backends** to share state across your team.

## Links and References

* [OpenTofu CLI Docs](https://docs.opentofu.io/cli)
* [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* [Infrastructure as Code](https://en.wikipedia.org/wiki/Infrastructure_as_code)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/19c6f909-165d-43f8-82a8-37bb654d0145" />
</CardGroup>


# Resource Targeting

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Resource-Targeting/page

Learn to use resource targeting with OpenTofu’s commands to update individual resources without affecting the rest of your infrastructure.

In this lesson, you'll learn how to use resource targeting with OpenTofu’s `plan` and `apply` commands to update individual resources without affecting the rest of your infrastructure.

## Example Configuration

Below is a sample HCL configuration that generates a random string and launches an AWS EC2 instance tagged with that string:

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

<Callout icon="lightbulb">
  The `aws_instance.web` resource uses the interpolation `${random_string.server-suffix.id}` to append the generated suffix to the **Name** tag.
</Callout>

## Applying Changes Normally

If you change the random string’s length from `6` to `5` and run:

```bash theme={null}
$ tofu apply
```

OpenTofu will plan and apply updates for both resources because the EC2 tag depends on the random string:

```plaintext theme={null}
Plan: 1 to add, 1 to change, 1 to destroy.

Enter a value: yes
random_string.server-suffix: Destroying... [id=6r923x]
random_string.server-suffix: Creation complete after 0s [id=nglmpo]
aws_instance.web: Modifying... [id=i-67428769e06ae2901]
Apply complete! Resources: 1 added, 1 changed, 1 destroyed.
```

## Targeting a Single Resource

To update only the random string and leave the EC2 instance untouched, use the `-target` flag:

```bash theme={null}
$ tofu apply -target=random_string.server-suffix
```

OpenTofu will generate a plan for just that resource:

```plaintext theme={null}
OpenTofu will perform the following actions:

  # random_string.server-suffix must be replaced
-/+ resource "random_string" "server-suffix" {
    ~ id      = "bl12qd" -> (known after apply)
    ~ length  = 6 -> 5 # forces replacement
}

Plan: 1 to add, 0 to change, 1 to destroy.

Warning: Resource targeting is in effect

Enter a value: yes
random_string.server-suffix: Destroying... [id=6r923x]
random_string.server-suffix: Creation complete after 0s [id=nglmpo]

Warning: Applied changes may be incomplete
Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

<Callout icon="triangle-alert">
  Using resource targeting can leave your state incomplete. Reserve this feature for urgent fixes or small, isolated changes.
</Callout>

## CLI Commands Reference

| Command                                     | Description                                  |
| ------------------------------------------- | -------------------------------------------- |
| `tofu plan`                                 | Preview all changes before applying them     |
| `tofu apply`                                | Apply all planned changes                    |
| `tofu apply -target=<RESOURCE_TYPE>.<NAME>` | Apply changes only to the specified resource |

## Links and References

* [OpenTofu Documentation](https://github.com/opentofu/opentofu)
* [AWS EC2 Overview](https://aws.amazon.com/ec2/)
* [Terraform Random Provider](https://registry.terraform.io/providers/hashicorp/random/latest)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/707a39e7-31dc-43f6-ba9d-40a3df9366be" />
</CardGroup>
