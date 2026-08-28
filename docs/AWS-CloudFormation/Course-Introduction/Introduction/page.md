# Introduction

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Course-Introduction/Introduction/page

A KodeKloud course teaching AWS CloudFormation infrastructure as code, covering templates, stacks, parameters, policies, drift detection, automation, and hands-on labs for practical DevOps skills.

Welcome to the AWS CloudFormation course by KodeKloud.

I'm Arno Pretorius, and I'll guide you through Infrastructure as Code (IaC) using AWS CloudFormation. This course is designed for cloud engineers, DevOps practitioners, and anyone expanding their AWS skill set. You’ll gain hands-on experience defining, deploying, and maintaining cloud infrastructure using CloudFormation templates.

Understanding CloudFormation is essential for automating scalable, secure, and repeatable deployments. Organizations such as Netflix and Samsung rely on CloudFormation to manage large-scale, complex infrastructure reliably. In this lesson you’ll learn what CloudFormation is, how it works, and how to start using its documentation, features, and best practices.

<Frame>
  <img alt="A presentation slide titled &#x22;AWS CloudFormation&#x22; showing a diagram that describes CloudFormation as an Infrastructure-as-Code service that defines and manages EC2 instances, S3 buckets, and databases (YAML/JSON). A small circular video of a presenter appears in the bottom-right." />
</Frame>

<Callout icon="lightbulb">
  CloudFormation templates can be authored in JSON or YAML. Throughout this course we’ll use YAML for readability, conciseness, and easier maintenance of complex templates.
</Callout>

What you will learn in this course:

* Core CloudFormation concepts: templates, stacks, change sets, and StackSets.
* How to author resources, metadata, parameters, mappings, conditions, and outputs in YAML templates.
* Policies and drift detection to manage stack lifecycle and configuration integrity.
* Best practices for modular templates (nested stacks), cross-stack references, and multi-account deployments.

Why CloudFormation?

* Declarative IaC: Describe the desired state, and CloudFormation provisions resources.
* Repeatability: Recreate environments consistently across regions and accounts.
* Integration: Works with IAM, AWS Organizations, CI/CD pipelines, and other AWS services.
* Auditable change control: Use change sets and drift detection to track modifications.

Getting started: a minimal resource
Below is a simple CloudFormation resource that creates an S3 bucket. Use this as a base to learn template structure and resource declaration.

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-kodekloud-demo-bucket
```

Practical tips:

* Keep templates modular and use logical names for resources.
* Validate templates with tools like cfn-lint and the CloudFormation validate-template API.
* Use Change Sets before applying updates to production stacks.

<Frame>
  <img alt="A presentation slide titled &#x22;Optional Attributes for Resources&#x22; for AWS CloudFormation listing DeletionPolicy, UpdatePolicy, and Condition with short explanations. A small circular video overlay in the bottom-right shows a presenter." />
</Frame>

Enhancing templates with Metadata, Tags, and Intrinsic Functions
Use Metadata and Tags to make templates informative and to add operational context. Intrinsic functions such as !Ref and !Sub enable dynamic references and string interpolation.

Example S3 bucket with Metadata and Tags:

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: eden-kodekloud-xcvt-bkt
      Tags:
        - Key: Environment
          Value: Production
        - Key: Owner
          Value: JohnDoe
    Metadata:
      Purpose: "Creating an S3 bucket"
      Reviewed: "02-07-2025"
      Owner: "John Doe"
      Contact: "johndoe@mail.com"
```

<Callout icon="warning">
  S3 bucket names must be globally unique across all AWS accounts and regions. Avoid hardcoding names in production templates unless you control the naming scheme. Consider using parameters or generated names instead.
</Callout>

Parameters: reusable and flexible templates
Parameters allow templates to accept inputs at stack creation time, making templates reusable across environments (dev, staging, prod). Parameters support types, defaults, allowed values, and validation rules.

<Frame>
  <img alt="A presentation slide titled &#x22;How Do Parameters Work?&#x22; showing a flowchart of AWS CloudFormation parameter steps (define parameters, choose input type, set defaults, supply values at launch, and use !Ref). A circular video inset of the presenter appears in the bottom-right." />
</Frame>

Example: parameterized bucket name:

```yaml theme={null}
Parameters:
  InputBucketName:
    Type: String
    Description: Enter the name of your S3 bucket
    Default: kodekloud-bkt

Resources:
  MyFirstS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
      Tags:
        - Key: Environment
          Value: Lab
        - Key: Owner
          Value: KodeKloud
    Metadata:
      Purpose: Demo S3 bucket for training
```

Conditions and lifecycle policies
Conditions let you control when resources are created. Policies manage resource lifecycle and update behaviors. These attributes help you craft safe update strategies and protect critical resources during stack changes.

<Frame>
  <img alt="A presentation slide titled &#x22;An Overview of Policies&#x22; listing AWS CloudFormation policies — DeletionPolicy, UpdateReplacePolicy, and CreationPolicy — with brief descriptions of each. A presenter thumbnail (KodeKloud) appears in the lower-right corner." />
</Frame>

Table: Common CloudFormation policy attributes

| Policy Attribute    | Purpose                                               | Example use case                                        |
| ------------------- | ----------------------------------------------------- | ------------------------------------------------------- |
| DeletionPolicy      | Retain or snapshot resource on stack deletion         | Keep S3 buckets or DB snapshots when stacks are deleted |
| UpdateReplacePolicy | Control replacement behavior during updates           | Prevent accidental data loss on resource replacement    |
| CreationPolicy      | Delay stack completion until resource signals success | Wait for EC2 instances to finish bootstrapping          |

Outputs, Exports, and cross-stack communication
Use Outputs to publish values from a stack (ARNs, endpoints, resource names). Outputs can be exported and imported by other stacks, enabling modular, composable infrastructure.

Access control and Drift Detection

* IAM integration: Attach fine-grained IAM policies to CloudFormation execution role for secure deployments.
* Custom IAM policies: Define least-privilege roles to limit stack actions.
* Drift Detection: Use drift detection to identify resources that diverged from the template and remediate drift through updates and change sets.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing a stack named &#x22;DemoStack&#x22; with status CREATE_IN_PROGRESS and the &#x22;Stack actions&#x22; menu open. A small circular video overlay of a presenter appears in the bottom-right." />
</Frame>

Nested stacks and modular templates
Nested stacks let you break large templates into smaller, maintainable components. Compose a root template that references smaller templates for networking, storage, or compute modules.

<Frame>
  <img alt="A slide titled &#x22;Nested Stacks&#x22; showing a diagram of a root Stack A containing Stack B and Stack C, with icons labeled Networking, Storage, and Compute on the right. A small circular webcam inset in the lower-right shows a person." />
</Frame>

StackSets: multi-account and multi-region deployments
StackSets provide a way to deploy and manage identical stacks across multiple AWS accounts and regions. This is essential for enterprise-scale infrastructure and standardized environment deployment.

Tools, validation, and CI/CD integration

* Template validation: Use aws cloudformation validate-template and cfn-lint for syntax and best-practice checks.
* Automation: Integrate CloudFormation with CI/CD pipelines (AWS CodePipeline, GitHub Actions, Jenkins).
* Local testing: Combine SAM for serverless resources and LocalStack for local testing when appropriate.

Recommended tools and links

* AWS CloudFormation User Guide: [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
* Template reference (intrinsic functions): [https://docs.aws.amazon.[SECRET_REDACTED]-function-reference.html](https://docs.aws.amazon.[SECRET_REDACTED]-function-reference.html)
* cfn-lint (linting tool): [https://github.com/aws-cloudformation/cfn-lint](https://github.com/aws-cloudformation/cfn-lint)
* AWS CLI (CloudFormation commands): [https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]index.html](https://docs.aws.amazon.[AWS_SECRET_ACCESS_KEY]index.html)
* StackSets documentation: [https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-is-cfnstacksets.html](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-is-cfnstacksets.html)

Hands-on labs and community
This course includes labs, demos, and real-world scenarios so you can apply concepts and build job-ready skills. Engage with the KodeKloud community to ask questions, share solutions, and collaborate with other learners.

Let's begin the journey and unlock the full potential of AWS CloudFormation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/9c364b08-c54a-4c05-879f-4aaca10b12ff/lesson/7355a92f-cc5d-46e4-a01a-f19517b72e02" />
</CardGroup>
