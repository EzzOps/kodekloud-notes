# IAM Policies with Terraform

Source: https://notes.kodekloud.com/docs/Terraform-Basics-Training-Course/Terraform-with-AWS/IAM-Policies-with-Terraform/page

Learn to create and attach IAM policies using Terraform, following the principle of least privilege for AWS users.

In this lesson, you will learn how to create IAM policies using Terraform and attach them to an AWS user. We will use the example of an IAM user named Lucy, who initially has no permissions. By following the principle of least privilege, we will incrementally grant her the required permissions.

<Callout icon="lightbulb">
  Always start AWS users with the least privilege and only grant specific permissions as needed.
</Callout>

## Prerequisites

Before you begin, ensure you have an IAM user created. In our example, Lucy has already been created.

## Creating an IAM Policy Document

AWS uses JSON-formatted policy documents to define permissions. Below is an example of an administrator access policy document:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

## Defining Resources in Terraform

To add permissions via Terraform, you will use the `aws_iam_policy` resource. According to the [AWS Terraform Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy), the only mandatory argument for this resource is the policy document in JSON format.

### Step 1: Declare the IAM User and IAM Policy

Below is a Terraform configuration snippet that first defines the IAM user resource, followed by the IAM policy resource:

```hcl theme={null}
resource "aws_iam_user" "admin-user" {
  name = "lucy"
  tags = {
    Description = "Technical Team Leader"
  }
}

resource "aws_iam_policy" "adminUser" {
  name   = "AdminUsers"
  policy = ?
}
```

### Step 2: Incorporate the Policy Document with Heredoc Syntax

One efficient method to include the policy document within your Terraform configuration is to use a heredoc. This allows you to embed multi-line strings without external file references. Here’s how to integrate the JSON document using this syntax:

```hcl theme={null}
resource "aws_iam_user" "admin-user" {
  name = "lucy"
  tags = {
    Description = "Technical Team Leader"
  }
}

resource "aws_iam_policy" "adminUser" {
  name   = "AdminUsers"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
EOF
}
```

### Step 3: Attaching the Policy to the IAM User

Even though the IAM policy is defined, it is not automatically granted to Lucy. To attach the policy, we use the `aws_iam_user_policy_attachment` resource. This resource takes the username and the ARN of the IAM policy as inputs:

```hcl theme={null}
resource "aws_iam_user_policy_attachment" "lucy-admin-access" {
  user       = aws_iam_user.admin-user.name
  policy_arn = aws_iam_policy.adminUser.arn
}
```

### Complete Terraform Configuration

Combining all the resources, the complete Terraform configuration looks as follows:

```hcl theme={null}
resource "aws_iam_user" "admin-user" {
  name = "lucy"
  tags = {
    Description = "Technical Team Leader"
  }
}

resource "aws_iam_policy" "adminUser" {
  name   = "AdminUsers"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_user_policy_attachment" "lucy-admin-access" {
  user       = aws_iam_user.admin-user.name
  policy_arn = aws_iam_policy.adminUser.arn
}
```

## Deploying the Configuration

After finalizing your Terraform configuration, follow these steps to preview and apply your changes:

```bash theme={null}
$ terraform plan
$ terraform apply
```

Below is a sample output from the Terraform apply process:

```bash theme={null}
$ terraform apply
