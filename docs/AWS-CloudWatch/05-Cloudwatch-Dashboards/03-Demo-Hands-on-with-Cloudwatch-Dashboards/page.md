# Demo Hands on with Cloudwatch Dashboards

Source: https://notes.kodekloud.com/docs/AWS-CloudWatch/Cloudwatch-Dashboards/Demo-Hands-on-with-Cloudwatch-Dashboards/page

This tutorial teaches provisioning infrastructure with CloudFormation, deploying a Python app on EC2, generating load, and building an AWS CloudWatch dashboard.

In this tutorial, you’ll learn how to provision infrastructure with CloudFormation, deploy a Python application on EC2 that writes to DynamoDB, generate load, and build a centralized AWS CloudWatch dashboard with various widget types.

## 1. Provision Base Infrastructure with CloudFormation

First, use a CloudFormation template to create the EC2 instance, IAM role, and instance profile.

### 1.1 CloudFormation Template Overview

This template (`cloudwatch_dashboard_cloudformation.yaml`) provisions:

* A t2.micro EC2 instance (Amazon Linux 2).
* An IAM role with full EC2, DynamoDB, and SSM permissions.
* An instance profile to attach the role to the instance.

| Resource             | Type                      | Details                                            |
| -------------------- | ------------------------- | -------------------------------------------------- |
| EC2 Instance         | AWS::EC2::Instance        | t2.micro, Amazon Linux 2, uses SSM Session Manager |
| IAM Role             | AWS::IAM::Role            | Full access to EC2, DynamoDB, and SSM              |
| IAM Instance Profile | AWS::IAM::InstanceProfile | Binds the IAM role to the EC2 instance             |

```yaml theme={null}
