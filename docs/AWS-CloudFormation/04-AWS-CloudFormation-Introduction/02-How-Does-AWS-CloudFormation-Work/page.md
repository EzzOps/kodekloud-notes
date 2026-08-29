# How Does AWS CloudFormation Work

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/AWS-CloudFormation-Introduction/How-Does-AWS-CloudFormation-Work/page

Explains how AWS CloudFormation templates and stacks work, how templates are stored, and how stacks are created, updated, and deleted.

This lesson explains how AWS CloudFormation operates and describes the lifecycle of a CloudFormation template and the stack that instantiates it. You'll learn where templates are stored, how CloudFormation creates and manages resources, and what happens when you update or delete a stack.

## Creating and storing a template

A CloudFormation template is a declarative specification (JSON or YAML) that lists the AWS resources and their configuration. Common resource examples include S3 buckets, EC2 instances, managed databases, and IAM roles.

* Author a template that declares the resources you need (for example: [S3 buckets](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3), [EC2 instances](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2), [databases](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases), [IAM roles](https://learn.kodekloud.com/user/courses/aws-iam)).
* Make the template available to CloudFormation in one of two common ways:
  1. Upload the template file to an [S3 bucket](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) yourself, then provide the S3 URL when creating the stack.
  2. Upload the template directly when creating a stack in the CloudFormation console or via the CLI. CloudFormation can store it in S3 for you or use a URL you provide.
* To change a stack, update the template (create a new version) and then update the stack to point to the new template or replace the template object in S3.

Example minimal YAML template structure:

```yaml theme={null}
AWSTemplateFormatVersion: '2010-09-09'
Description: Minimal example creating an S3 bucket
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-example-bucket-12345
```

<Frame>
  <img alt="A slide titled &#x22;How Does AWS CloudFormation Work?&#x22; that shows: to make changes you create a new version of a template file which is used to update the CloudFormation stack." />
</Frame>

## What is a stack?

A stack is the runtime instantiation of a CloudFormation template — a logical container that CloudFormation creates and manages for the resources defined in the template.

* Each stack has a unique name CloudFormation uses to track and manage its resources.
* Creating a stack causes CloudFormation to provision the resources specified in the template (for example, S3 buckets, EC2 instances, databases).
* Deleting a stack typically deletes the resources it created, unless you explicitly configure specific resources to be retained.

Compare templates and stacks at a glance:

| Resource Type | Purpose                                                           | When to use                                                               |
| ------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Template      | Declarative definition of resources and configuration (YAML/JSON) | Use to define desired architecture and all resource properties            |
| Stack         | Instantiated, managed set of resources created from a template    | Use to launch, update, and delete the environment described by a template |

<Frame>
  <img alt="A diagram explaining an AWS CloudFormation &#x22;stack&#x22; that groups resources. A central container provisions servers, storage buckets and databases, and all those resources are automatically deleted when the stack is deleted." />
</Frame>

> **warning** Deleting a stack will usually delete the resources it created. For stateful resources (databases, EBS volumes, S3 objects with important data), create backups or configure those resources with a DeletionPolicy of Retain before deleting the stack.

> **lightbulb** Tip: Use Change Sets to preview the impact of template updates before executing them. Change Sets show which resources will be created, modified, or removed.

## Logical flow for creating and launching a stack

Follow these steps when you create and launch a CloudFormation stack:

1. Author a CloudFormation template describing required resources and configuration.
2. Upload the template to an [S3 bucket](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3) or provide it directly during the CloudFormation create-stack workflow.
3. Point CloudFormation at the template location (S3 URL or direct upload).
4. CloudFormation reads the template and creates a stack (a named container for the resources).
5. CloudFormation provisions the AWS resources declared in the template. Once the stack creation completes, you can manage and interact with those resources as usual.

<Frame>
  <img alt="A slide showing a five-step flowchart of how AWS CloudFormation works: create a CloudFormation template, upload it to an S3 bucket, point CloudFormation to the template, create the application stack, and then access the AWS resources." />
</Frame>

## Summary

* Templates describe the desired AWS resources and configuration; stacks are the live instantiation of those templates.
* Store templates in S3 or upload them directly during stack creation.
* To change a stack, apply a new template version (or use Change Sets to preview updates).
* Deleting a stack removes its resources unless you set them to be retained.

Links and references:

* [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/index.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (for context on infrastructure-as-code vs container orchestration)
* [KodeKloud AWS Courses](https://learn.kodekloud.com)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/2ec6349c-f14b-48d2-8049-b313938d561e/lesson/026733f1-031b-4cbf-bc2f-aa7933ad2717)
