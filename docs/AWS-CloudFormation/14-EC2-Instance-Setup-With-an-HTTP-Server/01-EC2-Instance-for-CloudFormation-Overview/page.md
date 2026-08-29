# EC2 Instance for CloudFormation Overview

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/EC2-Instance-Setup-With-an-HTTP-Server/EC2-Instance-for-CloudFormation-Overview/page

Guides provisioning EC2 instances with AWS CloudFormation covering template properties, stack lifecycle, updates and replacements, UserData, IAM, volumes, AMI selection, and best practices

This lesson explains how to provision an Amazon EC2 instance using AWS CloudFormation and describes how the pieces fit together. You'll see the end-to-end flow, the key EC2 properties you typically declare in a template, a minimal example template, and notes on stack lifecycle, updates, and best practices.

High-level flow

* Author an AWS CloudFormation template that declares an AWS::EC2::Instance resource and any supporting resources (Security Groups, EBS Volumes, IAM Roles/InstanceProfiles, etc.).
* Deploy the template to AWS CloudFormation by creating a stack.
* CloudFormation provisions the declared resources and launches the EC2 instance as part of the stack.
* Update or delete the stack to change or remove the instance and its related resources; CloudFormation manages dependencies and lifecycle transitions.

CloudFormation resources are declared in the template using resource types and properties. For EC2 instances, the most common properties you will set include the instance type, AMI, key pair, security groups, volumes, user data, tags, and IAM instance profile.

Common EC2 properties in CloudFormation

| Property                          | Purpose                                                  | Example / Notes                                    |
| --------------------------------- | -------------------------------------------------------- | -------------------------------------------------- |
| InstanceType                      | VM size (CPU/Memory)                                     | `t3.micro`                                         |
| ImageId                           | AMI ID (region-specific)                                 | `ami-0abcdef1234567890`                            |
| KeyName                           | EC2 key pair for SSH access                              | `my-keypair`                                       |
| SecurityGroupIds / SecurityGroups | Network access controls. Use SecurityGroupIds with VPCs. | `!Ref InstanceSecurityGroup`                       |
| BlockDeviceMappings               | Root or additional EBS volumes                           | Configure size, volume type, delete-on-termination |
| UserData                          | Bootstrapping scripts (base64-encoded)                   | Use `!Base64` or Fn::Base64                        |
| Tags                              | Metadata for identification                              | Key/Value tags for cost center, env, etc.          |
| IamInstanceProfile                | IAM role attached to the instance                        | Attach for instance permissions                    |

Minimal EC2 resource example (YAML)

Place resources under the Resources section of your CloudFormation template. Use `!Base64` (Fn::Base64) for UserData so CloudFormation encodes it correctly:

```yaml theme={null}
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-0abcdef1234567890
      KeyName: my-keypair
      SecurityGroupIds:
        - !Ref InstanceSecurityGroup
      UserData: !Base64 |
        #!/bin/bash
        yum update -y
        yum install -y httpd
        systemctl enable httpd
        systemctl start httpd
```

CloudFormation stack lifecycle (create/update/delete)

When you create a stack from the template:

1. CloudFormation validates the template format and parameters.
2. It creates the stack and provisions resources in dependency order.
3. CloudFormation reports status updates (for example, CREATE\_IN\_PROGRESS, CREATE\_COMPLETE, CREATE\_FAILED).
4. If creation fails, CloudFormation typically rolls back the stack to the previous stable state (or deletes it if it was the initial create), unless rollbacks were disabled.

Common stack status values

| Status                 | Meaning                                           |
| ---------------------- | ------------------------------------------------- |
| CREATE\_IN\_PROGRESS   | Stack creation is underway                        |
| CREATE\_COMPLETE       | Stack created successfully                        |
| CREATE\_FAILED         | Creation failed (may trigger rollback)            |
| UPDATE\_IN\_PROGRESS   | An update is being applied                        |
| UPDATE\_COMPLETE       | Update finished successfully                      |
| ROLLBACK\_IN\_PROGRESS | CloudFormation is undoing changes after a failure |

Updating stacks and instance replacement behavior

* You can update a stack by submitting a modified template and/or changing parameters.
* CloudFormation attempts to update resources in place when possible, but some property changes force replacement (delete + create).
* For EC2 instances, many changes—such as altering ImageId, certain network properties, or instance type in some contexts—may trigger instance replacement.
* Plan for replacement: persist important data externally (EBS snapshots, separate EBS volumes mounted with DeleteOnTermination=false, or S3) and prepare for downtime or use Auto Scaling Groups for more controlled rolling replacement.

> **lightbulb** Choose the AMI (ImageId) that matches your region and instance architecture. AMI IDs are region-specific; avoid hard-coding an AMI from another region unless you implement mapping logic (for example, Parameterized mappings or SSM ParameterStore lookups).

> **warning** Some EC2 property changes in CloudFormation will replace the instance. Plan for downtime and persist critical data outside the instance (EBS snapshots, separate EBS volumes, or [Amazon S3](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)) to avoid data loss.

Practical tips and best practices

* Use `Fn::Base64` / `!Base64` for UserData to ensure proper encoding.
* Use CloudFormation metadata plus cfn-init and cfn-signal for structured bootstrapping and to support CreationPolicy/WaitCondition semantics.
* Provide CloudFormation with sufficient IAM permissions. Use a CloudFormation service role for cross-account or fine-grained provisioning control, or run operations with a user/role that has the necessary permissions.
* Separate mutable artifacts (application code, configuration) from the AMI/instance lifecycle. Consider baking AMIs with Packer or use Auto Scaling Groups and configuration management tools for immutability.
* Use CloudFormation mappings or SSM Parameter Store to resolve region-specific AMIs rather than hard-coding AMI IDs.
* For production, tag resources consistently for cost tracking and operational clarity.

Links and references

* [AWS CloudFormation documentation](https://docs.aws.amazon.com/cloudformation/index.html)
* [Amazon EC2 documentation](https://docs.aws.amazon.com/ec2/index.html)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/index.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (conceptual reference)
* Relevant course resources:
  * [Amazon Elastic Compute Cloud (EC2)](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
  * [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)
  * [Amazon Simple Storage Service (Amazon S3)](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)

Summary

Define an AWS::EC2::Instance in your CloudFormation template alongside its Security Groups, IAM InstanceProfile, volumes, and UserData. Deploy the template to create a stack; CloudFormation will manage resource creation, updates, replacements, and deletion according to the template and stack operations. Follow best practices for AMI management, bootstrapping, permissions, and data persistence to avoid surprises during updates.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/e8be47ac-5e51-4463-8b8c-dc5552940b10/lesson/e301e0b7-527e-4b3d-9d81-1449f64c87a0)
