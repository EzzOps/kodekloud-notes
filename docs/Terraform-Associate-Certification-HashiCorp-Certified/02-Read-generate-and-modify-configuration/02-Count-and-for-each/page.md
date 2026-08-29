# Count and for each

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Read-generate-and-modify-configuration/Count-and-for-each/page

This guide explores using Terraform's `count` and `for_each` meta-arguments to create multiple resource instances efficiently.

In this guide, we'll explore how to use Terraform's meta-arguments—`count` and `for_each`—to efficiently create multiple instances of a resource using the same configuration block. Understanding these options will help you manage resource deployments more dynamically and reliably.

## Using Count

The `count` meta-argument allows you to create multiple copies of a resource. In the example below, we launch three EC2 instances by setting `count` to 3:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  count         = 3
}

variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}
```

After running `terraform apply`, Terraform records these instances in the state file as a list. This means that each resource is identified by its index, for example:

* `aws_instance.web[0]`
* `aws_instance.web[1]`
* `aws_instance.web[2]`

### Dynamically Setting Count Using a List Variable

To streamline your configuration, you can use a list variable instead of a hardcoded count. The following configuration uses the `length` function to determine the number of instances based on the number of elements in the `webservers` list:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  count         = length(var.webservers)
  tags = {
    Name = var.webservers[count.index]
  }
}

variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}

variable "webservers" {
  type    = list(string)
  default = ["web1", "web2", "web3"]
}
```

In this configuration, Terraform creates as many instances as there are elements in the `webservers` list, with each instance tagged according to its corresponding name.

> **lightbulb** Using a dynamic list makes your Terraform configuration more flexible and easier to maintain when scaling resources.

### Potential Drawback of Using Count

One important limitation of the `count` meta-argument is that it organizes resources based on list indices. If the order of the elements changes or an element is removed, Terraform may update the wrong resource or destroy the unintended instance.

For example, consider the updated configuration when `"web1"` is removed from the list:

```hcl theme={null}
