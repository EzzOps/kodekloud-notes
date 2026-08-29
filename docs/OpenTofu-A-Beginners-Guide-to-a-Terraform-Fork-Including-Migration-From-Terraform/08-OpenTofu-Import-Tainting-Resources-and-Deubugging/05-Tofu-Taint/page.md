# Tofu Taint

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Import-Tainting-Resources-and-Deubugging/Tofu-Taint/page

Managing resource replacement in OpenTofu using a taint mechanism to ensure automatic replacement of failed or stale instances.

OpenTofu’s taint mechanism lets you mark resources for destruction and recreation, ensuring failed or stale instances are replaced automatically. While the legacy `tofu taint` command is deprecated, its core logic remains intact under the new `apply-replace` flag.

## What Is a Tainted Resource?

A *tainted* resource in OpenTofu is one you explicitly mark (or is marked automatically) for replacement on the next apply. This is useful when:

* A previous `tofu apply` failed during provisioning.
* You manually modified software or configuration on an existing cloud instance outside of OpenTofu.

## Example: Auto-Taint on Provisioner Failure

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = "ami-0edab43b6fa892279"
  instance_type = "t2.micro"
  key_name      = "ws"

  provisioner "local-exec" {
    # Invalid path causes the provisioner to fail
    command = "echo ${self.public_ip} > invalid/path/to/ip.txt"
  }
}
```

Here, a `local-exec` provisioner tries to write the instance’s public IP to a nonexistent path. When you run:

```bash theme={null}
$ tofu apply
```

the creation fails and OpenTofu marks the resource as **tainted**.

<Callout icon="lightbulb">
  A tainted resource will be destroyed and recreated on the next `tofu apply`. This behavior mirrors `terraform taint` in Terraform CLI.
</Callout>

## 1. Detecting a Tainted Resource

Run `tofu plan` to see any tainted resources in your state:

```bash theme={null}
$ tofu plan
```

You’ll see output similar to:

```plaintext theme={null}
Refreshing state in-memory prior to plan...
aws_instance.webserver: Refreshing state... [id=i-0dba2d5dc22a9a904]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  -/+ destroy and then create replacement

OpenTofu will perform the following actions:
