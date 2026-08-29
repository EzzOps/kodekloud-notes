# Create the following files inside the payroll-app directory:
#   app_server.tf, dynamodb_table.tf, s3_bucket.tf, variables.tf
```

## EC2 Instance Configuration (`app_server.tf`)

```hcl theme={null}
resource "aws_instance" "app_server" {
  ami           = var.ami
  instance_type = "t2.medium"
  tags = {
    Name = "${var.app_region}-app-server"
  }
  depends_on = [
    aws_dynamodb_table.payroll_db,
    aws_s3_bucket.payroll_data
  ]
}
```

## S3 Bucket Configuration (`s3_bucket.tf`)

```hcl theme={null}
resource "aws_s3_bucket" "payroll_data" {
  bucket = "${var.app_region}-${var.bucket}"
}
```

## DynamoDB Table Configuration (`dynamodb_table.tf`)

```hcl theme={null}
resource "aws_dynamodb_table" "payroll_db" {
  name         = "user_data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "EmployeeID"

  attribute {
    name = "EmployeeID"
    type = "N"
  }
}
```

## Variable Declarations (`variables.tf`)

The module uses the following variables to allow flexibility in deployment:

```hcl theme={null}
variable "app_region" {
  type = string
}

variable "bucket" {
  default = "flexit-payroll-alpha-22001c"
}

variable "ami" {
  type = string
}
```

## Deploying the Application Stack

### Deployment in the US East 1 Region

To deploy the stack in the US East 1 region, create a new directory (for example, `/root/terraform-projects/us-payroll-app`) to serve as the root module. Inside this directory, add the following `main.tf` file:

```bash theme={null}
$ mkdir -p /root/terraform-projects/us-payroll-app
```

```hcl theme={null}
module "us_payroll" {
  source     = "../modules/payroll-app"
  app_region = "us-east-1"
  ami        = "ami-24e140119877avm"
}
```

This configuration specifies that the AWS provider should operate in the US East 1 region using the provided custom AMI. While the module hardcodes values such as the instance type and DynamoDB table parameters for consistency, it still enables regional customizations for the bucket name and AMI.

Initialize, plan, and apply the configuration with the following commands:

```bash theme={null}
$ terraform init
$ terraform plan
$ terraform apply
```

A sample output from `terraform apply` might look like:

```Terraform theme={null}
Terraform will perform the following actions:
# module.us_payroll.aws_dynamodb_table.payroll_db will be created
+ resource "aws_dynamodb_table" "payroll_db" {
    arn          = (known after apply)
    billing_mode = "PAY_PER_REQUEST"
    hash_key     = "EmployeeID"
    name         = "user_data"
  }
# module.us_payroll.aws_instance.app_server will be created
+ resource "aws_instance" "app_server" {
    ami           = "ami-24e140119877avm"
    instance_type = "t2.medium"
  }
# module.us_payroll.aws_s3_bucket.payroll_data will be created
+ resource "aws_s3_bucket" "payroll_data" {
    bucket = "us-east-1-flexit-payroll-alpha-22001c"
  }

Enter a value: yes
module.us_payroll.aws_dynamodb_table.payroll_db: Creating...
```

### Deployment in the UK (London) Region

To deploy the same stack in the UK region, create another directory (for example, `/root/terraform-projects/uk-payroll-app`) for the root module. Since both the `app_region` and the AMI vary by region, your `main.tf` should include the following configuration:

```bash theme={null}
$ mkdir -p /root/terraform-projects/uk-payroll-app
```

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

When you run `terraform apply` in this directory, Terraform will deploy the identical stack in the London region. Note that the S3 bucket name is automatically prefixed with the region code:

```Terraform theme={null}
Terraform will perform the following actions:
# module.uk_payroll.aws_dynamodb_table.payroll_db will be created
+ resource "aws_dynamodb_table" "payroll_db" {
    arn          = (known after apply)
    billing_mode = "PAY_PER_REQUEST"
    hash_key     = "EmployeeID"
    name         = "user_data"
  }
# module.uk_payroll.aws_instance.app_server will be created
+ resource "aws_instance" "app_server" {
    ami           = "ami-35e140119877avm"
    instance_type = "t2.medium"
  }
# module.uk_payroll.aws_s3_bucket.payroll_data will be created
+ resource "aws_s3_bucket" "payroll_data" {
    bucket = "eu-west-2-flexit-payroll-alpha-22001c"
  }

Enter a value: yes
module.uk_payroll.aws_dynamodb_table.payroll_db: Creating...
module.uk_payroll.aws_s3_bucket.payroll_data: Creating...
module.uk_payroll.aws_dynamodb_table.payroll_db: Creation complete after 1s [id=user_data]
```

> **lightbulb** Ensure you have the appropriate AWS credentials configured for each target region before running Terraform commands.

## Module Resource Addressing

When using modules, each resource is addressed with the syntax that concatenates the module name, the resource type, and the resource name. For example, the DynamoDB table in the `us_payroll` module is referenced as:

```Terraform theme={null}
module.us_payroll.aws_dynamodb_table.payroll_db
```

This addressing convention keeps module resources organized and makes it easier to manage configurations when deploying identical stacks in multiple regions.

## Summary

In this tutorial, we have built a Terraform module to deploy a payroll application across multiple AWS regions. By encapsulating resource definitions into a reusable module, you ensure consistency in critical parameters such as the instance type, DynamoDB table name, and primary key while allowing flexibility in regional configurations like the AMI and S3 bucket naming.

Leveraging modules in Terraform simplifies infrastructure management, minimizes configuration redundancy, and reduces the risk of misconfigured resources. In our next guide, we will explore how to utilize modules available in the [Public Terraform Registry](https://registry.terraform.io/).

For further reading and additional resources, consider checking out:

* [Terraform Documentation](https://www.terraform.io/docs)
* [AWS Provider for Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/terraform-basics-training-course/module/e6838c6b-3208-4396-a744-34b0ed2cd292/lesson/4badb52f-7640-4260-805d-afd9931a2d9b)


# What are modules

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-Modules/What-are-modules/page

This guide explores Terraform modules and demonstrates how to use them to simplify and modularize Terraform configurations.

In this guide, we'll explore what Terraform modules are and demonstrate how to leverage them to simplify and modularize your Terraform configurations.

Terraform configuration files can grow lengthy and complex. Initially, you might start with simple resources such as a local file or a random pet, but as you begin deploying more advanced resources on AWS—like IAM roles, policies, S3 buckets, DynamoDB tables, and EC2 instances—the configurations often become repetitive and difficult to manage.

For example, consider a configuration that defines two EC2 instances, a key pair, a security group, and a DynamoDB table. In this case, the EC2 instance configurations are nearly identical, leading to unnecessary duplication of code.

While Terraform supports having hundreds of resources within a single file (with no strict resource limit), coupling all resources together can result in files containing thousands of lines. An alternative approach is to divide the configuration into multiple files within the same directory. Terraform automatically processes every file with a `.tf` extension in the configuration directory, regardless of the file organization.

Below is an example of how you might structure your Terraform files across multiple files:

```hcl theme={null}
