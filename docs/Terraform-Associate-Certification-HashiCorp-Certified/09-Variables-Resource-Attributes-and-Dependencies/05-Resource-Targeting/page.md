# aws_key_pair.alpha:
resource "aws_key_pair" "alpha" {
  arn          = "arn:aws:ec2:us-east-1::key-pair/alpha"
  fingerprint  = "d7:ff:a6:63:18:64:9c:57:a1:ee:ca:a4:ad:c2:81:62"
  id           = "alpha"
  key_name     = "alpha"
  public_key   = "ssh-rsa AAAAB3NzaC1yc2EAAAA...alpha@a-server"
  tags_all     = {}
}
```

This output reveals exported attributes such as ARN, fingerprint, ID, key name, public key, and tags. For more detailed explanations of these attributes, refer to the [Terraform Documentation](https://www.terraform.io/docs) for each resource.

<Callout icon="lightbulb">
  Remember: Utilizing exported attributes allows you to build dependencies between resources, enabling dynamic infrastructure provisioning.
</Callout>

## Referencing Resource Attributes

Exported resource attributes are often used as inputs for configuring other resources. Consider a scenario where you need to configure an EC2 instance using the AWS key pair resource. You can reference the key pair's attributes in your EC2 instance configuration as follows:

```hcl theme={null}
resource "aws_key_pair" "alpha" {
  key_name   = "alpha"
  public_key = "ssh-rsa..."
}

resource "aws_instance" "cerberus" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = aws_key_pair.alpha.key_name
}
```

In this configuration, the EC2 instance's key\_name parameter is set using the reference expression:

resourceType.ResourceName.attribute

Here, `aws_key_pair.alpha.key_name` refers to the key\_name attribute of the key pair resource named "alpha". By running `terraform apply`, both the key pair and the EC2 instance are provisioned in the correct order. Terraform automatically ensures that the key pair is created before the EC2 instance, thanks to the inherent resource dependency.

The sample console output from running `terraform apply` is shown below:

```bash theme={null}
$ terraform apply
...
aws_key_pair.alpha: Creating...
aws_key_pair.alpha: Creation complete after 1s [id=alpha]
aws_instance.cerberus: Creating...
aws_instance.cerberus: Still creating... [10s elapsed]
aws_instance.cerberus: Creation complete after 10s [id=i-c791dc46a6639d4a7]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed
```

<Callout icon="lightbulb">
  Terraform automatically manages the creation order by analyzing resource dependencies. During deletion, resources are removed in reverse order, ensuring a safe teardown.
</Callout>

## Managing Explicit Dependencies

Sometimes, two resources might not implicitly depend on each other—for instance, two EC2 instances that do not reference one another. In such cases, you can enforce a creation order using the `depends_on` meta-argument.

Imagine you have two EC2 instances: one for your database server and another for your web server. To ensure that Terraform creates the database instance before the web instance, modify the configuration as follows:

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

With the `depends_on` argument, Terraform provisions the database instance first. When removing resources, it deletes the web instance before the database instance, preserving the dependency order.

<Callout icon="triangle-alert">
  Be cautious with explicit dependencies. Overusing `depends_on` can lead to unnecessarily complex dependency graphs, which might complicate the execution plan.
</Callout>

## Conclusion

This lesson has reviewed how Terraform manages resource attributes and dependencies. By leveraging both implicit and explicit dependencies, you can efficiently control resource creation and deletion order, ensuring a robust infrastructure lifecycle management.

Happy building with Terraform!

## Additional Resources

* [Terraform Documentation](https://www.terraform.io/docs)
* [AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/cca81ade-f05a-42b2-af56-1926cade6582/lesson/c980f12b-3dab-4e34-8d4f-beb7178d78be" />
</CardGroup>


# Resource Targeting

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Variables-Resource-Attributes-and-Dependencies/Resource-Targeting/page

This guide explains how to use resource targeting with Terraform's commands to manage infrastructure changes effectively.

In this guide, you will learn how to employ resource targeting with Terraform's `plan` and `apply` commands. This tutorial uses an example that includes two resource blocks: one for generating a random string and another for provisioning an AWS instance. In this updated example, both resource blocks have been slightly modified for enhanced functionality.

## Enhanced AWS Instance Tagging

The AWS instance resource, named "web," now has a tag with the key `Name` that appends the salt value generated by the random string resource. This is accomplished using Terraform's interpolation syntax by referencing `random_string.server-suffix.id` within `${...}`.

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

## Changing the Random String Length

Suppose you need to update the random string length from 6 to 5. Running `terraform apply` without targeting will lead to the recreation of the random string resource with the new length. Consequently, the AWS instance's tag will be updated due to its dependency on the random string value.

Below is a sample of the console output after applying the change:

```plaintext theme={null}
$ terraform apply
.
Plan: 1 to add, 1 to change, 1 to destroy.

Do you want to perform these actions?
Terraform will perform the actions described above.
Only 'yes' will be accepted to approve.

Enter a value: yes

random_string.server-suffix: Destroying... [id=6r923x]
random_string.server-suffix: Destruction complete after 0s
random_string.server-suffix: Creating...
random_string.server-suffix: Creation complete after 0s [id=nglmop]
aws_instance.web: Modifying... [id=i-67428769e06ae2901]
aws_instance.web: Modifications complete after 0s [id=i-67428769e06ae2901]

Apply complete! Resources: 1 added, 1 changed, 1 destroyed.
```

<Callout icon="triangle-alert">
  Using `terraform apply` without proper targeting will update both the random string and the AWS instance tag. Make sure this is the desired behavior before proceeding.
</Callout>

## Resource Targeting to Isolate Changes

What if you want to update only the random string resource and keep the AWS instance configuration intact? To do this, you should first revert both resources to their original state, where the random string had a 6-character value. Then, use the `-target` flag with `terraform apply` to focus solely on the random string resource.

By specifying the resource address using the syntax `resourceType.resourceName`, the following command targets only the random string resource "server-suffix". Note that Terraform may warn you that the changes could be incomplete.

```bash theme={null}
$ terraform apply -target random_string.server-suffix
.
Terraform will perform the following actions:
