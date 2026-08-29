# S3 with Terraform

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-with-AWS/S3-with-Terraform/page

This guide explains how to create and manage an S3 bucket using Terraform, including uploading files and attaching bucket policies.

In this guide, you will learn how to create and manage an S3 bucket using Terraform. We will cover the steps to:

* Create an S3 bucket,
* Upload a file to the bucket, and
* Attach a bucket policy that grants access to an existing IAM entity.

Follow along to understand how Terraform integrates with AWS for managing S3 resources.

## Creating an S3 Bucket

To create an S3 bucket, we use the AWS S3 bucket resource in Terraform. For more details on the available resource arguments, please refer to the [Terraform AWS documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs).

Below is an example configuration where we define an S3 bucket with a unique name and attach a descriptive tag.

```hcl theme={null}
resource "aws_s3_bucket" "finance" {
  bucket = "finance-21092020"
  tags = {
    Description = "Finance and Payroll"
  }
}
```

When you run the following command, Terraform will plan and proceed to create the bucket:

```bash theme={null}
$ terraform apply
Terraform will perform the following actions:
