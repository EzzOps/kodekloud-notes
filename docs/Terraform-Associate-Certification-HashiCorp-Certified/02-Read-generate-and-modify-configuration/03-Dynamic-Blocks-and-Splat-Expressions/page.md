# main.tf
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  count         = length(var.webservers)
  tags = {
    Name = var.webservers[count.index]
  }
}

# variables.tf
variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}

variable "webservers" {
  type    = list(string)
  default = ["web2", "web3"]
}
```

Running `terraform plan` may generate an execution plan like this:

```bash theme={null}
$ terraform plan
...
Terraform will perform the following actions:

# aws_instance.web[0] will be updated in-place
~ resource "aws_instance" "web" {
    ami = "ami-06178cf087598769c"
    ...
    tags = {
        ~ "Name" = "web1" -> "web2"
    }
}

# aws_instance.web[1] will be updated in-place
~ resource "aws_instance" "web" {
    ami = "ami-06178cf087598769c"
    ...
    tags = {
        ~ "Name" = "web2" -> "web3"
    }
}

# aws_instance.web[2] will be destroyed
- resource "aws_instance" "web" {
    ...
}

Plan: 0 to add, 2 to change, 1 to destroy.
```

> **triangle-alert** Since resources are managed as a list when using `count`, removing or reordering items can lead to unintended updates or inadvertent deletion of resources. Always verify your plan before applying such changes.

## Using For\_Each

The `for_each` meta-argument offers an alternative approach by creating a resource for each element in a set or map. Unlike `count`, `for_each` stores resources in a map keyed by each element’s value, eliminating issues caused by index reordering.

Consider the following configuration that uses `for_each` to loop through the `webservers` variable:

```hcl theme={null}
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  for_each      = var.webservers
  tags = {
    Name = each.value
  }
}

variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}

variable "webservers" {
  type    = set(string)
  default = ["web1", "web2", "web3"]
}
```

Key advantages of using `for_each`:

* The `webservers` variable is defined as a set (or map) to ensure unique keys.
* Each resource is identified by its key, such as `aws_instance.web["web1"]`.
* Removing an element (like `"web1"`) only destroys that specific resource without affecting the others.

After applying this configuration, running `terraform state list` displays resources as:

```bash theme={null}
$ terraform state list
aws_instance.web["web1"]
aws_instance.web["web2"]
aws_instance.web["web3"]
```

This predictable mapping means that modifying the set—such as removing `"web1"`—only affects the corresponding resource.

## Conclusion

In this article, we explored two strategies for provisioning multiple instances in Terraform: using `count` and using `for_each`. While `count` is straightforward, it can introduce complications when handling dynamic lists due to index-based identification. In contrast, `for_each` facilitates more predictable resource management by leveraging set or map keys.

By understanding these distinctions, you can choose the most appropriate approach for your Terraform configurations and avoid unintended resource modifications. Stay tuned for our next article, where we'll dive deeper into advanced Terraform concepts and best practices.

For more detailed Terraform documentation and best practices, visit the [Terraform Registry](https://registry.terraform.io/) or [HashiCorp's documentation](https://www.terraform.io/docs).

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/c59e52ed-8a8c-4a6c-8ad0-8dcc38c1598e/lesson/c74b55ae-d1b0-4b56-a865-08d69121bf97)


# Dynamic Blocks and Splat Expressions

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Read-generate-and-modify-configuration/Dynamic-Blocks-and-Splat-Expressions/page

Learn to streamline Terraform configurations using dynamic blocks and splat expressions for efficient resource creation and cleaner code.

In this article, you'll learn how to streamline your Terraform configurations using dynamic blocks and splat expressions. These techniques are especially useful when you need to create multiple resource instances efficiently and maintain cleaner code.

Previously, we covered how to loop through collections such as lists, sets, or maps using arguments like count and for\_each. This approach is practical for creating multiple instances of similar resource blocks. For instance, consider the following variable definition for backend servers:

```hcl theme={null}
resource "aws_instance" "backend" {
  ami           = var.ami
  instance_type = var.instance_type
  count         = length(var.backend-servers)
  tags = {
    Name = var.backend-servers[count.index]
  }
}

variable "ami" {
  default = "ami-06178cf087598769c"
}

variable "instance_type" {
  default = "m5.large"
}

variable "backend-servers" {
  type    = list
  default = ["server1", "server2"]
}
```

In this example, Terraform creates two EC2 instances (server1 and server2) using the count parameter.

## Building a VPC, Subnet, and Security Group with Dynamic Blocks

Consider a more complex scenario where you need to create a new AWS VPC with a private subnet and configure a security group that permits inbound traffic on specific ports. A Virtual Private Cloud (VPC) is a custom network in AWS where you can deploy resources such as EC2 instances. In this case, the VPC uses a CIDR range of 10.0.0.0/16. Inside the VPC, a private subnet (without public IP addresses or direct internet connectivity) is created, and a security group is set up to allow inbound traffic on ports 22 and 8080.

![The image depicts an Amazon VPC setup with a private subnet containing two servers, server1 and server2, within a security group allowing inbound ports 8080 and 22.](https://kodekloud.com/kk-media/image/upload/v1752884105/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Dynamic-Blocks-and-Splat-Expressions/frame_90.jpg)

Let’s start by defining the resources needed for the VPC, private subnet, and a security group with explicit nested ingress blocks:

```hcl theme={null}
resource "aws_vpc" "backend-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "backend-vpc"
  }
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.backend-vpc.id
  cidr_block = "10.0.2.0/24"
  tags = {
    Name = "private-subnet"
  }
}

resource "aws_security_group" "backend-sg" {
  name   = "backend-sg"
  vpc_id = aws_vpc.backend-vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

Notice the use of a reference expression (aws\_vpc.backend-vpc.id) to link the VPC ID with both the subnet and the security group. Although this static configuration functions correctly, it can quickly become repetitive as you add more ingress rules.

> **lightbulb** To simplify your configuration and enhance flexibility, use dynamic blocks to automatically generate the ingress blocks.

### Refactoring with Dynamic Blocks

Begin by removing the static ingress blocks and introduce a new variable for allowed ports:

```hcl theme={null}
variable "ingress_ports" {
  type    = list
  default = [22, 8080]
}
```

Then, modify the security group resource to employ a dynamic block that iterates over the ingress\_ports variable:

```hcl theme={null}
resource "aws_security_group" "backend-sg" {
  name   = "backend-sg"
  vpc_id = aws_vpc.backend-vpc.id

  dynamic "ingress" {
    for_each = var.ingress_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

In this configuration, the dynamic block automatically creates an ingress rule for every port value present in the ingress\_ports list.

It is also possible to specify a custom iterator name instead of using the default. Using an iterator named port, the dynamic block can be rewritten as follows:

```hcl theme={null}
resource "aws_security_group" "backend-sg" {
  name   = "backend-sg"
  vpc_id = aws_vpc.backend-vpc.id

  dynamic "ingress" {
    iterator = port
    for_each = var.ingress_ports
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}

variable "ingress_ports" {
  type    = list
  default = [22, 8080]
}
```

### Exploring Splat Expressions

Splat expressions in Terraform allow you to extract specific attributes from a list of blocks. For instance, if you want to output all the to\_port values from the dynamically generated ingress rules, you can use the following output variable:

```hcl theme={null}
output "to_ports" {
  value = aws_security_group.backend-sg.ingress[*].to_port
}
```

This splat expression aggregates the to\_port attribute from every ingress rule into a single list.

### Applying the Terraform Configuration

To deploy these resources, run the following command:

```bash theme={null}
$ terraform apply --auto-approve
```

After applying, you should see output similar to this:

```bash theme={null}
aws_vpc.backend-vpc: Creating...
aws_vpc.backend-vpc: Creation complete after 0s [id=vpc-593470c0]
aws_subnet.private-subnet: Creating...
aws_security_group.backend-sg: Creating...
aws_subnet.private-subnet: Creation complete after 1s [id=subnet-fdd6b762]
aws_security_group.backend-sg: Creation complete after 1s [id=sg-a5aa3b711157d4a2b]
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```

> **lightbulb** In this article, we demonstrated how to simplify complex Terraform configurations using dynamic blocks for multiple ingress rules and splat expressions for efficient attribute extraction.

That's it for this guide. To further reinforce your understanding, consider taking the accompanying quiz.

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/c59e52ed-8a8c-4a6c-8ad0-8dcc38c1598e/lesson/630c7612-947c-445e-b67b-cd64a405cca9)
