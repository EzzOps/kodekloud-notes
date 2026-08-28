# Roles for AWS Services

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Identity-and-Access-Management-IAM/Roles-for-AWS-Services/page

This article explains how to assign IAM roles to AWS services for secure and efficient access to resources.

IAM roles in AWS allow applications and services to access other AWS services securely and efficiently. In this lesson, you'll learn how to assign IAM roles to various AWS services, ensuring your resources communicate seamlessly with the necessary permissions.

## Overview

For example:

* An EC2 instance that needs to access an S3 bucket can be assigned a role containing the required permissions.
* An AWS Lambda function that pulls messages from a queue or writes logs to CloudWatch must have an IAM role with the appropriate permissions.

## Assigning Roles to EC2 Instances

To assign an IAM role to an EC2 instance, follow these steps:

1. Navigate to the EC2 management console.
2. Under the "Actions" menu, select "Security" and then "Modify IAM Role."
3. Once the role is assigned, any application running on that EC2 instance automatically inherits the permissions associated with the IAM role.

<Frame>
  ![The image shows an AWS EC2 management console interface with options to manage instances, including launching instances and modifying IAM roles. It highlights a running instance named "mywebapp."](https://kodekloud.com/kk-media/image/upload/v1752858968/notes-assets/images/AWS-Certified-Developer-Associate-Roles-for-AWS-Services/aws-ec2-management-console-mywebapp.jpg)
</Frame>

## Assigning Roles to Lambda Functions

The process for assigning a role to a Lambda function is similar:

* When creating a Lambda function, select a role to grant the permissions required for its operations.
* For instance, if the Lambda function needs to write logs to CloudWatch, choose or create a role with permissions for CloudWatch Logs.

During the Lambda function setup, you'll typically see options such as:

* Creating a new role using an AWS policy template.
* Using an existing role.
* Creating a brand new role if necessary.

<Frame>
  !\[The image is a screenshot of a user interface for setting roles for AWS Lambda functions, showing options to create a new role with basic permissions, use an existing role, or create a new role from AWS policy templates. It includes a note about role creation time and permissions for uploading logs to Amazon CloudWatch Logs.]
</Frame>

<Callout icon="lightbulb">
  Using IAM roles is the best practice for assigning permissions and ensuring secure access between AWS services.
</Callout>

## Exam Preparation Tips

If you encounter exam questions regarding assigning permissions for inter-service communication, remember:

* Use IAM roles to securely assign the necessary permissions between services.
* Always verify that the role has the correct policy permissions for the intended operations.

For further reading on AWS security and IAM roles, consider visiting the [AWS Identity and Access Management documentation](https://aws.amazon.com/iam/).

By following these guidelines, you'll improve security, reduce management overhead, and adhere to AWS best practices for role-based permissions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-certified-developer-associate/module/683c50bc-9bd3-4094-b666-354fcc06941f/lesson/b47b8b73-6288-4f9c-b65a-65716d088c87" />
</CardGroup>
