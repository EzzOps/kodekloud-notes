# AWS IAM with Terraform

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-with-AWS/AWS-IAM-with-Terraform/page

Learn to provision AWS IAM resources using Terraform for efficient and secure infrastructure management.

In this guide, you'll learn how to provision AWS IAM resources using Terraform. Previously, we explored using the AWS Management Console and AWS CLI for IAM tasks. Now, we'll streamline the process by leveraging Terraform to create an IAM user resource. For further details, refer to the [AWS Provider documentation on the Terraform Registry](https://registry.terraform.io/providers/hashicorp/aws/latest/docs).

## Creating an IAM User Resource

Terraform resource blocks follow a naming convention where the resource type is prefixed by the provider name. In our example, we will define an AWS IAM user resource block named "admin-user". The block requires a mandatory argument called "name" (the IAM user's name) and can also include optional arguments such as tags.

Below is an example configuration:

```hcl theme={null}
resource "aws_iam_user" "admin-user" {
  name = "Lucy"
  tags = {
    Description = "Technical Team Leader"
  }
}
```

In this configuration, an IAM user named Lucy is created with a tag that describes the user as a "Technical Team Leader."

## Initializing Terraform and Running the Plan

Before applying the configuration, initialize Terraform to download the AWS provider plugin by running:

```bash theme={null}
terraform init
```

After initialization, if you run:

```bash theme={null}
terraform plan
```

you might encounter two common issues:

1. Terraform may prompt for an AWS region. Although IAM resources are global, Terraform requires a region because most AWS resources are region-specific.
2. Terraform might not find valid AWS credentials to connect to your AWS account.

## Configuring the AWS Provider

To address these issues, add a provider block to your configuration. The provider block specifies both the default region and the credentials needed to interact with your AWS account. The following combined configuration includes both the provider block and the IAM user resource block:

```hcl theme={null}
provider "aws" {
  region     = "us-west-2"
  access_key = "[AWS_ACCESS_KEY_ID]"
  secret_key = "je7MtGbClwBF/2tk/h3yCo8n..."
}

resource "aws_iam_user" "admin-user" {
  name = "Lucy"
  tags = {
    Description = "Technical Team Leader"
  }
}
```

In this setup, the default region is set to US West 2. The access key and secret access key ensure Terraform can authenticate and make changes to your AWS account.

## Executing the Terraform Plan and Apply

With the provider configuration in place, proceed by running:

```bash theme={null}
terraform plan
```

You'll see an execution plan similar to this:

```bash theme={null}
$ terraform plan
...
+ create

Terraform will perform the following actions:
