# List all outputs
$ tofu output
pub_ip = 54.214.145.69

# Fetch a single output value
$ tofu output pub_ip
54.214.145.69
```

***

## Use Cases

* Quickly inspect provisioned resource attributes on-screen.
* Pass output values into other IaC tools, ad-hoc scripts, Ansible playbooks, or testing frameworks.
* Expose dynamic data for remote execution contexts or CI/CD pipelines.

***

## Links and References

* [OpenTofu Documentation](https://opentofu.io/)
* [Terraform Output Variables](https://www.terraform.io/language/values/outputs)
* [AWS Provider for Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/opentofu-a-beginners-guide-to-a-terraform-fork-including-migration-from-terraform/module/c3586b29-e450-4c95-bad9-91bdf332eb24/lesson/b646ce21-3806-4df8-9e7e-8395f67da219" />
</CardGroup>


# Resource Attributes And Dependencies

Source: https://notes.kodekloud.com/docs/OpenTofu-A-Beginners-Guide-to-a-Terraform-Fork-Including-Migration-From-Terraform/OpenTofu-Basics/Resource-Attributes-And-Dependencies/page

This article explores how OpenTofu records resource attributes and manages dependencies during provisioning for reliable Infrastructure as Code.

In this lesson, we’ll explore how OpenTofu records resource attributes and manages dependencies during provisioning. Understanding these concepts is key to writing reliable Infrastructure as Code.

## Exported Attributes

When you define a resource in OpenTofu, several attributes are exported after creation. For example, create an AWS key pair:

```hcl theme={null}
resource "aws_key_pair" "alpha" {
  key_name   = "alpha"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAAADAQABAAABAQD3.....alpha@a-server"
}
```

Here, `public_key` is a required argument. After running `tofu apply`, inspect the exported values using:

```bash theme={null}
tofu show
```

Example output:

```bash theme={null}
