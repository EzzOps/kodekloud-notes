# main.tf
resource "local_file" "pet" {
  filename = var.filename
  content  = var.content
}

resource "random_pet" "my-pet" {
  prefix    = var.prefix
  separator = var.separator
  length    = var.length
}
```

The variable definitions remain in `variables.tf` as shown earlier.

When you run `terraform apply`, Terraform processes your configuration and recognizes that variable values do not need to be enclosed in double quotes in concatenated expressions. If you update a variable value (for example, changing the `content` variable or increasing the `length` from 1 to 2), Terraform will detect the change and replace the affected resources accordingly.

Below is an example output after updating variable values:

```plaintext theme={null}
$ terraform apply
Terraform will perform the following actions:

-/+ resource "local_file" "pet" {
    ~ content            = "We love pets!" -> "My favorite pet is Mrs. Whiskers!" # forces replacement
      directory_permission = "0777"
      file_permission      = "0777"
      filename            = "/root/pet.txt"
      ~ id                 = "bc9cabef1d8b0071d3c4ae9959a9c328f35fe697" -> (known after apply)
}

# random_pet.my-pet must be replaced
-/+ resource "random_pet" "my-pet" {
      ~ id      = "Mrs.Hen" -> (known after apply)
      ~ length  = 1 -> 2 # forces replacement
        prefix    = "Mrs"
        separator = "."
}

Plan: 2 to add, 0 to change, 2 to destroy.
random_pet.my-pet: Destroying... [id=Mrs.hen]
random_pet.my-pet: Destruction complete after 0s
local_file.pet: Destroying... [id=bc9cabef1d8b0071d3c4ae9959a9c328f35fe697]
local_file.pet: Destruction complete after 0s
random_pet.my-pet: Creating...
local_file.pet: Creating...
```

<Callout icon="lightbulb">
  Using variables in Terraform not only makes your configurations more readable but also simplifies maintenance when scaling your infrastructure.
</Callout>

***

## AWS Instance Example Using Variables

Consider an example where you create an AWS instance using variables for the AMI and instance type. In the resource definition below, the values for `ami` and `instance_type` are referenced from variables:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = var.ami
  instance_type = var.instance_type
}
```

The variable definitions for this configuration might look like the following:

```hcl theme={null}
variable "ami" {
  default = "ami-0edab43b6fa892279"
}

variable "instance_type" {
  default = "t2.micro"
}
```

While these defaults are set in `variables.tf`, you can override them when applying the configuration. There are a few methods to do so:

1. **Remove the Default Values:**\
   You can remove the defaults in `variables.tf` and provide values explicitly during runtime.

   ```hcl theme={null}
   # main.tf
   resource "aws_instance" "webserver" {
     ami           = var.ami
     instance_type = var.instance_type
   }

   # variables.tf
   variable "ami" {
   }

   variable "instance_type" {
   }
   ```

2. **Pass Values with Command-Line Flags:**\
   Provide variable values using the `-var` flag during execution:

   ```bash theme={null}
   $ terraform apply -var "ami=ami-0edab43b6fa892279" -var "instance_type=t2.micro"
   ```

3. **Use Environment Variables:**\
   Export the variable values before running Terraform:

   ```bash theme={null}
   $ export TF_VAR_instance_type="t2.micro"
   $ terraform apply
   ```

4. **Variable Definition File:**\
   Supply variable values via a variable definition file (ending with `.tfvars` or `.tfvars.json`). By default, Terraform automatically loads files named `terraform.tfvars` or `terraform.tfvars.json`. For custom-named files, use the `-var-file` flag:

   ```hcl theme={null}
   # variables.tfvars
   ami = "ami-0edab43b6fa892279"
   instance_type = "t2.micro"
   ```

   ```bash theme={null}
   $ terraform apply -var-file="variables.tfvars"
   ```

***

## Variable Definition Precedence

Terraform provides multiple methods for assigning variable values. When a variable is defined in more than one way, Terraform follows a specific precedence order:

| Precedence Level              | Description                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------- |
| 1. Environment Variables      | Values set via environment variables (e.g., `export TF_VAR_instance_type="t2.micro"`) |
| 2. terraform.tfvars File      | Values provided in `terraform.tfvars` or `terraform.tfvars.json`                      |
| 3. Auto-loaded Variable Files | Files ending with `.auto.tfvars` or `.auto.tfvars.json` loaded in alphabetical order  |
| 4. Command-Line Flags         | Values passed using the `-var` or `-var-file` flags (highest precedence)              |

For example, if the variable `type` is specified through multiple methods as shown below:

```bash theme={null}
$ export TF_VAR_type="t2.nano"
```

```hcl theme={null}
# In terraform.tfvars:
type = "t3.micro"
```

```hcl theme={null}
# In an auto.tfvars file:
type = "t3.small"
```

```bash theme={null}
$ terraform apply -var "type=t2.medium"
```

Terraform will use `t2.medium` as the final value for `type` since command-line flags have the highest precedence.

<Callout icon="lightbulb">
  Always be aware of the variable precedence in Terraform to avoid unexpected behaviors during deployment. Using dedicated variable files or environment variables can improve consistency across different environments.
</Callout>

***

That concludes our article on variables in Terraform. Understanding how to define, reference, and override variables is essential for creating flexible and reusable Terraform configurations. Happy building!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/cca81ade-f05a-42b2-af56-1926cade6582/lesson/06a9906c-1823-4986-a292-ada617ddd68b" />
</CardGroup>


# Resource Attributes and Dep

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Variables-Resource-Attributes-and-Dependencies/Resource-Attributes-and-Dep/page

This lesson explores how Terraform manages resource attributes and dependencies for dynamic infrastructure provisioning.

In this lesson, we explore how Terraform manages resource attributes and dependencies. When you provision a resource, Terraform stores various details (attributes) related to that resource. These attributes can then be referenced throughout your configuration, enabling you to create dynamic and interconnected infrastructures.

## Understanding Exported Attributes

Earlier, we created an AWS key pair resource that required a user-supplied public key. After its creation, Terraform exported several attributes, which you can inspect using the Terraform show command.

Below is the configuration used to create the AWS key pair resource:

```hcl theme={null}
resource "aws_key_pair" "alpha" {
  key_name   = "alpha"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAADAQABAAABAAQD3......alpha@a-server"
}
```

Run the following command to display the resource details:

```bash theme={null}
$ terraform show
```

The command produces output similar to this:

```plaintext theme={null}
