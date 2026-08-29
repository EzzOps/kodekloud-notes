# Environment Variables

Source: https://notes.kodekloud.com/docs/Spacelift-Elevate-Your-Infrastructure-Deployment/Spacelift-Basics/Environment-Variables/page

Learn to configure AWS credentials in Spacelift for demo deployment and manage environment variables securely.

In this lesson, you'll learn how to configure AWS credentials in Spacelift for a demo deployment. While several authentication methods are available, we begin with the simplest approach. If the AWS provider is not configured correctly, you may encounter an error similar to the following:

```plain theme={null}
Planning failed. Terraform encountered an error while generating this plan.

  Error: configuring Terraform AWS Provider: no valid credential sources for Terraform AWS Provider found.

  Please see https://registry.terraform.io/providers/hashicorp/aws
  for more information about providing credentials.

  AWS Error: failed to refresh cached credentials: no EC2 IMDS role found, operation error ec2: DescribeInstances,
  request canceled, context deadline exceeded

  with provider["registry.terraform.io/hashicorp/aws"],
 on main.tf line 11, in provider "aws":
  11: provider "aws" {}

[1821G4J8XYZ43R5R3KGH3C] Unexpected exit code when planning changes: 1
```

> **lightbulb** The same methods for configuring the AWS provider in Spacelift also apply when working on your local machine or within any containerized environment.

## Sample Terraform Configuration

Below is an example Terraform configuration that sets up the AWS provider and creates a Virtual Private Cloud (VPC). In your environment, you can pass your AWS Access Key ID and AWS Secret Access Key as environment variables:

```hcl theme={null}
