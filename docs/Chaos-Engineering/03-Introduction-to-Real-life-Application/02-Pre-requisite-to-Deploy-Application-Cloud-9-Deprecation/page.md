# Pre requisite to Deploy Application Cloud 9 Deprecation

Source: https://notes.kodekloud.com/docs/Chaos-Engineering/Introduction-to-Real-life-Application/Pre-requisite-to-Deploy-Application-Cloud-9-Deprecation/page

Provisioning an EC2-based development environment to deploy a pet adoption website using AWS CDK while addressing Cloud9 deprecation.

In this lesson, you’ll provision an EC2-based development environment with all the tools required to deploy our pet adoption website using the AWS Cloud Development Kit (CDK). We’ll cover:

1. Manual setup of an EC2 instance
2. Automating that setup with a CloudFormation template
3. Alternatives to the deprecated AWS Cloud9 environment

![The image outlines the prerequisites for setting up architecture and deploying an application, including choosing your environment, deploying an EC2 instance, and deploying the application with CDK.](https://kodekloud.com/kk-media/image/upload/v1752871953/notes-assets/images/Chaos-Engineering-Pre-requisite-to-Deploy-Application-Cloud-9-Deprecation/prerequisites-architecture-deploying-application.jpg)

## 1. Create the IAM Role

First, create an IAM role named **FIS-workshop-admin** with the following managed policies:

| Policy Name                  | Purpose                                     |
| ---------------------------- | ------------------------------------------- |
| AmazonEC2FullAccess          | Full control of EC2 resources               |
| AmazonSSMManagedInstanceCore | Systems Manager Session Manager permissions |

> **triangle-alert** The role name **must** be exactly `FIS-workshop-admin`. All subsequent CDK and CloudFormation scripts expect this exact name.

## 2. Launch and Configure the EC2 Instance

When launching your EC2 instance:

1. Attach the **FIS-workshop-admin** IAM role
2. Choose an instance type (e.g., `t3.medium`)
3. Select your VPC and subnets
4. Enable SSH access **or** plan to use AWS Systems Manager Session Manager

## 3. Connect & Prepare Your Environment

Once your instance is up:

```bash theme={null}
