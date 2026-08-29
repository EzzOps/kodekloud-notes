# Policies Overview

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CloudFormation-Conditions-and-Policies/Policies-Overview/page

Overview of AWS CloudFormation per resource policies that control deletion, replacement, and creation signals to protect data and manage resource lifecycle during stack operations

Welcome to this lesson on AWS CloudFormation resource policies. This practical overview explains the three per-resource policies CloudFormation provides, how they affect resource lifecycle operations (create, update, delete), and when to apply each policy to protect data and manage infrastructure changes safely.

At a high level, CloudFormation supports three related per-resource policies:

* DeletionPolicy — controls what happens to a resource when its stack is deleted.
* UpdateReplacePolicy — specifies what to do with the old resource when a replacement occurs during a stack update.
* CreationPolicy — requires external confirmation (a "signal") before CloudFormation considers a resource creation successful.

Below you’ll find a quick comparison table, detailed explanations, and concise YAML examples for each policy.

| Policy              | Purpose                                                                     | Typical Use Case                                                     |
| ------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| DeletionPolicy      | Defines action on a resource when its stack is deleted                      | Preserve critical data (Retain) or create snapshots (Snapshot)       |
| UpdateReplacePolicy | Controls the old resource’s fate when a replacement is needed during update | Retain existing data while creating a new resource                   |
| CreationPolicy      | Waits for resource signals before marking creation successful               | Ensure bootstrapping scripts finish on EC2 or Auto Scaling instances |

## DeletionPolicy

The DeletionPolicy attribute tells CloudFormation what to do with a resource when its stack is deleted. Choosing the right deletion behavior helps prevent accidental data loss, or conversely, prevents orphaned resources and unexpected costs.

Common values:

* Delete — CloudFormation deletes the resource (default).
* Retain — CloudFormation leaves the resource in your account. Use this to protect data but be aware retained resources are unmanaged by CloudFormation and may incur charges.
* Snapshot — CloudFormation takes a snapshot before deletion. Supported only for snapshot-capable resources (EBS volumes, RDS DB instances, and similar).

Example: retain an Amazon S3 bucket so it isn't removed when the stack is deleted.

```yaml theme={null}
MyBucket:
  Type: AWS::S3::Bucket
  DeletionPolicy: Retain
  Properties:
    BucketName: my-important-bucket
```

## UpdateReplacePolicy

When an update requires a resource replacement (for example, changing an immutable property), CloudFormation creates the replacement resource and then takes action on the old one. UpdateReplacePolicy accepts the same values as DeletionPolicy (Delete, Retain, Snapshot) and controls the behavior applied to the old resource after the new resource has been created.

Use UpdateReplacePolicy to avoid accidental data loss during updates by retaining the old resource until you’ve validated the replacement.

Example: keep the old S3 bucket when a replacement occurs during stack update.

```yaml theme={null}
MyBucket:
  Type: AWS::S3::Bucket
  UpdateReplacePolicy: Retain
  DeletionPolicy: Retain
  Properties:
    BucketName: my-important-bucket
```

## CreationPolicy

CreationPolicy requires confirmation from the resource (a ResourceSignal) before CloudFormation marks the resource creation as successful. This is commonly used with EC2 instances or Auto Scaling groups whose bootstrapping scripts must complete before the stack creation proceeds.

Key points:

* CreationPolicy waits for a specified number of success signals within a timeout period.
* Signals are typically sent with the CloudFormation helper (cfn-signal) or via API calls.
* If required signals are not received before the timeout, the creation fails and CloudFormation rolls back (unless rollback is disabled).

Example: require one signal from an EC2 instance within 15 minutes.

```yaml theme={null}
MyInstance:
  Type: AWS::EC2::Instance
  Properties:
    ImageId: ami-0123456789abcdef0
    InstanceType: t3.micro
  CreationPolicy:
    ResourceSignal:
      Count: 1
      Timeout: PT15M
```

## Best practices and callouts

> **lightbulb** Use DeletionPolicy: Retain to protect critical data and resources from accidental stack deletions. Always document and tag retained resources so they can be discovered and managed later.

> **warning** Avoid using Retain indiscriminately. Retained resources become unmanaged by CloudFormation and can accumulate costs. Plan lifecycle management, automation, or tagging strategies for retained items.

## Notes and constraints

* DeletionPolicy and UpdateReplacePolicy are set per resource — not at the stack level.
* Snapshot is valid only for resource types that support snapshots (EBS, RDS, etc.).
* CreationPolicy requires that the resource or bootstrapping scripts send a signal (for example, via cfn-signal). Missing signals before timeout cause stack failure/rollback.
* For Auto Scaling groups, CreationPolicy can wait for signals from instances launched by the group — useful for ensuring instances are healthy and bootstrapped before completing stack creation.

## Links and references

* [AWS CloudFormation User Guide — AWS::CloudFormation::Stack Policies and Signals](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties.html)
* [cfn-signal documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-signal.html)
* [Amazon EC2 documentation](https://docs.aws.amazon.com/ec2/)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/)
* [Amazon RDS documentation](https://docs.aws.amazon.com/rds/)

This overview should help you choose the right CloudFormation policy to protect data, control replacements during updates, and ensure resources are properly initialized during stack creation.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/216ef226-4efe-45ed-b547-b3ab7c5dd29b/lesson/b1f4625c-3ce7-446b-bd59-eb7f9cec5b8f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/216ef226-4efe-45ed-b547-b3ab7c5dd29b/lesson/8d3c1177-e3d6-4dbd-adec-fd111974b5b2)
