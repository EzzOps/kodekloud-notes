# Demo Integrating metadata and parameters

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/EC2-Instance-Setup-With-an-HTTP-Server/Demo-Integrating-metadata-and-parameters/page

Explains adding Metadata and Parameters to a CloudFormation template to let users choose EC2 instance types via dropdown and document choices for auditing and deployment.

In this lesson we'll add Metadata and Parameters to a CloudFormation template so you can choose the EC2 instance type at deploy time. This pattern is useful when you want to offer a small set of supported instance types (for example, free-tier eligible types) while keeping the template self-documenting for auditors and operators.

## What you’ll learn

* How to add top-level Metadata to a CloudFormation template for documentation.
* How to expose an InstanceType as a Parameter with a dropdown (AllowedValues).
* How to reference the parameter with the intrinsic function `!Ref`.
* How to update a stack in the console and verify the resulting EC2 instance type.

## Metadata

Add a top-level Metadata section near the top of the template. Metadata is for humans and auditing — CloudFormation doesn’t use top-level Metadata to change provisioning behavior, though resource-level Metadata can be used by helper tools (for example, cfn-init).

```yaml theme={null}
Metadata:
  Purpose: Basic EC2 instance with HTTP and SSH access
```

<Callout icon="lightbulb">
  Top-level Metadata is for humans and documentation. CloudFormation itself does not directly use top-level Metadata to change provisioning behavior, although resource-level Metadata can be consumed by helper tools (for example, cfn-init) to influence instance configuration.
</Callout>

## Choosing which instance types to allow (research)

Before defining the parameter, decide which EC2 instance types you’ll expose (for example, free-tier eligible types or sizes that match your workload and cost constraints). You can inspect instance types in the EC2 console.

<Frame>
  <img alt="A screenshot of the AWS EC2 console (United States — Ohio region) showing the Resources dashboard with counts for Instances (running), Security groups, Volumes, and other EC2 resources. The left sidebar shows EC2 navigation items and the top and bottom show the browser tabs and Windows taskbar." />
</Frame>

Open the Launch Instance wizard to view the available instance types and confirm which types are offered in your region and account.

<Frame>
  <img alt="A screenshot of the AWS EC2 &#x22;Launch an instance&#x22; console showing AMI selection with quick-start tiles for Amazon Linux, macOS, Ubuntu, Windows, and Red Hat. A right-hand Summary pane displays the number of instances, selected AMI details, and a &#x22;Launch instance&#x22; button." />
</Frame>

Common examples you might choose to expose:

* t3.micro (often free-tier eligible)
* t3.small

After you decide which instance types to present to users, add a Parameters block to the template.

## Parameters — make InstanceType configurable

Create a parameter named `MyInstanceType` (or another clear name). Add a Description and an AllowedValues list so the CloudFormation console presents a dropdown for selection.

```yaml theme={null}
Parameters:
  MyInstanceType:
    Type: String
    Description: Select your EC2 instance type
    AllowedValues:
      - t3.micro
      - t3.small
    Default: t3.micro
```

Parameters at a glance:

| Field         | Purpose                                             | Example                         |
| ------------- | --------------------------------------------------- | ------------------------------- |
| Type          | Data type for the parameter                         | `String`                        |
| Description   | Short help text shown in the console                | `Select your EC2 instance type` |
| AllowedValues | Limits choices; shows a dropdown in the console     | `t3.micro`, `t3.small`          |
| Default       | Value used if the user doesn’t change the parameter | `t3.micro`                      |

Refer to the parameter using the intrinsic function `!Ref` when setting the EC2 InstanceType property. Below is a minimal complete template that includes Metadata, the Parameter, a Security Group allowing HTTP and SSH, and an EC2 instance that references the parameter.

```yaml theme={null}
AWSTemplateFormatVersion: "2010-09-09"
Description: CloudFormation template to create a basic EC2 instance with HTTP and SSH access.

Metadata:
  Purpose: Basic EC2 instance with HTTP and SSH access

Parameters:
  MyInstanceType:
    Type: String
    Description: Select your EC2 instance type
    AllowedValues:
      - t3.micro
      - t3.small
    Default: t3.micro

Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable HTTP and SSH access
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref MyInstanceType
      ImageId: ami-0eb9d6fc9fab44d24
      SecurityGroupIds:
        - !Ref MySecurityGroup
```

<Callout icon="warning">
  The ImageId shown (ami-0eb9d6fc9fab44d24) is region-specific. Replace it with an AMI ID available in your target region (for example, an Amazon Linux 2 AMI). Also be aware that changing InstanceType may replace the instance (resulting in termination of the previous instance) depending on the property change behavior for EC2 instances.
</Callout>

Useful references:

* [AWS CloudFormation Parameters](https://docs.aws.amazon.[SECRET_REDACTED]-section-structure.html)
* [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)

## Deploying or updating the stack

When creating or updating a stack in the CloudFormation console you can upload your template file or point to an S3 URL.

<Frame>
  <img alt="A browser screenshot of the AWS CloudFormation console showing the &#x22;Update stack&#x22; page where you can choose a template source (Amazon S3 URL or upload a template file). The page includes an input for the S3 URL and &#x22;Cancel&#x22; and &#x22;Next&#x22; buttons." />
</Frame>

During stack creation or update the console displays parameter inputs. The `MyInstanceType` parameter will show your Description and AllowedValues as a dropdown.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Specify stack details&#x22; step while updating a stack named DemoStack. The Parameters box shows MyInstanceType set to &#x22;t3.micro,&#x22; and the cursor is hovering over the orange Next button." />
</Frame>

Select the instance type you want (for example `t3.small`) and continue. CloudFormation will apply the change: it may modify the instance in place or replace it (terminating the previous instance and launching a new one) depending on the resource update behavior.

When the update completes successfully the stack will show an UPDATE\_COMPLETE status.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing one stack named &#x22;DemoStack&#x22; with a timestamp and status &#x22;UPDATE_COMPLETE.&#x22; The filter status is set to &#x22;Active&#x22; and the &#x22;View nested&#x22; toggle is on." />
</Frame>

In the EC2 console you can verify the running instance reflects the selected InstanceType (for example, `t3.small`). You may also see terminated instances from the previous configuration in the console.

<Frame>
  <img alt="A screenshot of the AWS EC2 Instances console showing three instances in the us-east-2 region; one is Running (t3.small) while two are Terminated (t3.micro). The table displays instance IDs, status checks, availability zone, and the &#x22;Launch instances&#x22; action." />
</Frame>

To revert, update the stack again and choose the original allowed value (for example, `t3.micro`) — CloudFormation will apply the update and change the instance accordingly.

## Viewing the template and Metadata

Auditors and operators can view the template and the Metadata you added from the CloudFormation console by selecting the stack and opening the template view.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Stacks&#x22; console. It shows a single stack named &#x22;DemoStack&#x22; with status &#x22;UPDATE_COMPLETE&#x22; and a created timestamp." />
</Frame>

## Summary checklist

* Add a top-level Metadata section for documentation.
* Define a Parameter for InstanceType with Description, AllowedValues, and Default.
* Use `!Ref` to reference the parameter in the EC2 Instance resource.
* Upload the template or provide an S3 URL in the CloudFormation console.
* Select the desired InstanceType during stack creation/update and verify the result in EC2.

Further reading:

* [AWS CloudFormation User Guide](https://docs.aws.amazon.[SECRET_REDACTED].html)
* [Amazon EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/e8be47ac-5e51-4463-8b8c-dc5552940b10/lesson/1bff1f95-d148-4eb5-a988-f56c37f5efaa" />
</CardGroup>
