# module.us_payroll.aws_dynamodb_table.payroll_db will be created
+ resource "aws_dynamodb_table" "payroll_db" {
    + arn          = (known after apply)
    + billing_mode = "PAY_PER_REQUEST"
    + hash_key     = "EmployeeID"
    + name         = "user_data"
}
...
# module.us_payroll.aws_instance.app_server will be created
+ resource "aws_instance" "app_server" {
    + ami           = "ami-24e140119877avm"
    + instance_type = "t2.medium"
}
...
+ resource "aws_s3_bucket" "payroll_data" {
    + acceleration_status = (known after apply)
    + acl                 = "private"
    + arn                 = (known after apply)
    + bucket              = "us-east-1-flexit-payroll-alpha-22001c"
}
Enter a value: yes
```

The EC2 instance, S3 bucket, and DynamoDB table are created based on the configuration defined in the module and the values provided in the root module.

***

### UK Deployment

To deploy the same stack in the UK region, create a directory for the UK payroll application:

```bash theme={null}
$ mkdir /root/terraform-projects/uk-payroll-app
```

Inside this directory, create a `main.tf` file with the following content:

```hcl theme={null}
module "uk_payroll" {
  source     = "../modules/payroll-app"
  app_region = "eu-west-2"
  ami        = "ami-35e140119877avm"
}

provider "aws" {
  region = "eu-west-2"
}
```

In this configuration, the `app_region` is set to `eu-west-2` (London region) and the AMI ID is appropriate for that region. When you run `terraform apply`, Terraform will create the resources with names prefixed by `eu-west-2` to reflect the region-specific deployment.

The module output ensures clear resource addressing. For instance, you can reference the DynamoDB table as:

```text theme={null}
module.uk_payroll.aws_dynamodb_table.payroll_db
```

And the EC2 instance as:

```text theme={null}
module.uk_payroll.aws_instance.app_server
```

***

## Benefits of Using Terraform Modules

Using reusable modules in Terraform provides several advantages:

| Benefit                     | Description                                                                                                    |
| --------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Simplified Configuration    | Organize your infrastructure into modular components rather than maintaining a large monolithic configuration. |
| Reduced Risk of Human Error | Use a preconfigured and validated module for consistent deployments across various environments.               |
| Improved Reusability        | Deploy the same infrastructure in multiple regions while keeping core configurations consistent.               |

By adopting a module-based approach, you ensure that key configuration aspects such as the EC2 instance type and DynamoDB settings remain constant, while still being able to adjust region-specific variables like the AMI ID and bucket naming.

> **lightbulb** For further learning on Terraform modules, refer to the [Terraform Documentation](https://www.terraform.io/docs/modules/index.html).

***

That’s it for this guide on creating and deploying a Terraform module for multiple environments. Happy deploying!

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/7b1fdaed-c4dd-45b8-be74-8068def45ce7/lesson/29347ea5-f039-4996-a0c6-9ab7d94659d9)


# Terraform Modules

Source: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Terraform-Modules/Terraform-Modules/page

This article explains Terraform modules, their structure, usage, and benefits for organizing infrastructure as code.

Terraform modules are a powerful way to organize your infrastructure as code. In Terraform, any directory containing configuration files is considered a module. Each Terraform configuration must have one root module, which is the directory where you run your Terraform commands. In this guide, we'll review how modules work and demonstrate how to use both local and registry modules.

## Understanding the Root Module

Consider a configuration directory named "aws-instance" located under your Terraform projects directory. This folder contains the configuration files needed to deploy a simple EC2 instance on AWS. Since Terraform commands are executed inside this folder, "aws-instance" serves as the root module for that configuration.

For example, listing the contents of the "aws-instance" directory:

```bash theme={null}
$ ls /root/terraform-projects/aws-instance
main.tf  variables.tf
```

The `main.tf` file might include the following configuration:

```hcl theme={null}
resource "aws_instance" "webserver" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = var.key
}
```

And the `variables.tf` file could define variables like this:

```hcl theme={null}
variable "ami" {
  type        = string
  default     = "ami-0edab43b6fa892279"
  description = "Ubuntu AMI ID in the ca-central-1 region"
}
```

## Reusing Modules with Child Modules

Terraform modules can also reference other modules, enabling you to package and reuse resource configurations efficiently. Suppose you wish to create a new development web server instance using the existing "aws-instance" module. Instead of duplicating the configuration, you can simply call the module from a new directory called "development."

First, create the new directory:

```bash theme={null}
$ mkdir /root/terraform-projects/development
```

Inside the "development" directory, create a configuration file with the following module block that references the local AWS instance module:

```hcl theme={null}
module "dev-webserver" {
  source = "../aws-instance"
}
```

Since Terraform commands are executed from the "development" directory, it becomes the root module and the AWS instance directory works as a child module. The "module" keyword is followed by a logical name (in this example, "dev-webserver") and a required `source` parameter that provides the path to the module. You can also specify an absolute path:

```hcl theme={null}
module "dev-webserver" {
  source = "/root/terraform-projects/aws-instance"
}
```

> **lightbulb** Using absolute paths can be effective in some scenarios, but it is generally recommended to use relative paths for portability.

## Leveraging the Terraform Registry

One of the key benefits of using modules is code reusability. In addition to local modules, you can also utilize modules hosted on the [Terraform Registry](https://registry.terraform.io), which is a robust repository for both provider plugins and community or official modules. For example, instead of writing a security group configuration from scratch, you might search for a suitable module in the Registry.

Below is an example search result:

![The image shows a search result for "security-group" in the Terraform Registry, listing various modules for AWS and Azure security groups.](https://kodekloud.com/kk-media/image/upload/v1752884150/notes-assets/images/Terraform-Associate-Certification-HashiCorp-Certified-Terraform-Modules/frame_190.jpg)

Modules found in the Registry typically include publisher details, version information, and usage instructions with examples. They might also offer sub-modules for common configurations like SSH, HTTP, or HTTPS security rules.

### Example: Using an AWS Security Group Module

To use a module for creating a security group in your configuration, include a module block with the appropriate source and version specifications. For instance:

```hcl theme={null}
module "security-group" {
  source  = "terraform-aws-modules/security-group"
  version = "3.16.0"
  # Insert the required variables here
}
```

If you need a sub-module specifically for SSH access, requiring additional arguments like a security group name, VPC ID, and ingress CIDR blocks, your configuration might look like this:

```hcl theme={null}
module "security-group_ssh" {
  source              = "terraform-aws-modules/security-group/aws/modules/ssh"
  version             = "3.16.0"
  vpc_id              = "vpc-7d8d215"
  ingress_cidr_blocks = ["10.10.0.0/16"]
  name                = "ssh-access"
}
```

After defining your configuration, follow the standard Terraform workflow:

1. **Initialize Terraform:**\
   Download necessary provider plugins and modules by running:

   ```bash theme={null}
   $ terraform init
   Downloading terraform-aws-modules/security-group/aws 3.16.0 for security-group_ssh...
   - security-group_ssh in .terraform/modules/security-group_ssh/modules/ssh
   ```

2. **Plan and Apply:**\
   Validate the configuration with `terraform plan` and create the resources using `terraform apply`.

> **lightbulb** Remember that running `terraform init`, `terraform plan`, and `terraform apply` in the directory where your root module is located is crucial for successful deployment.

## Benefits of Using Modules

Modules in Terraform offer numerous advantages:

| Benefit                     | Description                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| Reusability                 | Encapsulate resources in self-contained units that can be reused across multiple projects. |
| Simplified Configuration    | Reduce configuration complexity by abstracting detailed setups into modules.               |
| Improved Readability        | Maintain shorter and more understandable root modules.                                     |
| Reduced Risk of Human Error | Use tested and validated modules to minimize errors.                                       |
| Configuration Locking       | Restrict specific variables in the root module to enforce standard parameters.             |

These benefits emphasize why modules are a vital tool for creating consistent and standardized cloud environments.

## Next Steps

In the next lesson, we will dive deeper into advanced module usage, exploring techniques for module parameterization and dependency management. For further learning, consider visiting the [Terraform Documentation](https://www.terraform.io/docs) or exploring additional modules on the [Terraform Registry](https://registry.terraform.io).

Happy coding with Terraform!

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-associate-certification-hashicorp-certified/module/7b1fdaed-c4dd-45b8-be74-8068def45ce7/lesson/b83ef4fa-afa8-4ada-b72e-425153d4b38e)
