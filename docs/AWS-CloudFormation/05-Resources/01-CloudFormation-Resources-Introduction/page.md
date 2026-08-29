# CloudFormation Resources Introduction

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Resources/CloudFormation-Resources-Introduction/page

Explains AWS CloudFormation resources, structure, intrinsic functions, dependency handling, lifecycle controls and best practices for defining and managing resources in templates.

Hi everyone — welcome to the next lesson, focused on CloudFormation resources.

CloudFormation resources are the central elements of a CloudFormation template. They declare the AWS services and objects that CloudFormation will create and manage — for example, Amazon EC2 instances, Amazon S3 buckets, AWS RDS databases, and Amazon DynamoDB tables.

At a high level, each resource definition specifies:

* a logical ID (the template-local name you reference),
* a resource Type (for example, AWS::S3::Bucket or AWS::EC2::Instance),
* and optional Properties that configure how CloudFormation should create the resource.

When you submit a template, CloudFormation analyzes resource references and dependencies, determines a safe create/update/delete order (honoring explicit DependsOn or implicit references), and provisions resources accordingly.

> **lightbulb** A CloudFormation resource block generally contains:

  * A logical ID (the template identifier you use with intrinsic functions),
  * Type (the AWS resource type),
  * Properties (resource-specific configuration),
  * Optional fields like DependsOn, Metadata, DeletionPolicy, UpdatePolicy, and Condition.

## Resource anatomy (YAML example)

This concise example shows an S3 bucket and a bucket policy that depends on the bucket. It demonstrates logical IDs, the Type field, Properties, intrinsic functions (!Ref and !Sub), and an explicit DependsOn to control creation order.

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-example-bucket

  MyBucketPolicy:
    Type: AWS::S3::BucketPolicy
    DependsOn: MyS3Bucket
    Properties:
      Bucket: !Ref MyS3Bucket
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Sid: PublicReadGetObject
            Effect: Allow
            Principal: "*"
            Action: "s3:GetObject"
            Resource: !Sub "arn:aws:s3:::${MyS3Bucket}/*"
```

Key takeaways from the example:

* MyS3Bucket is the logical ID used elsewhere in the template (for example, with !Ref or !GetAtt).
* Type identifies the AWS resource type (here AWS::S3::Bucket and AWS::S3::BucketPolicy).
* Properties contains the resource-specific configuration.
* DependsOn ensures CloudFormation creates MyS3Bucket before MyBucketPolicy.
* !Ref returns the referenced resource value (often the resource name or ID). !Sub composes ARNs or other strings with variables.

## Creation order, dependencies, and references

CloudFormation automatically orders operations when it can detect implicit references (e.g., when one resource property references another). Use DependsOn for explicit ordering when:

* implicit references are not detected, or
* you need strict control over resource creation order.

Common intrinsic functions and how they connect resources:

| Intrinsic Function   | Use Case                                             | Example                                         |
| -------------------- | ---------------------------------------------------- | ----------------------------------------------- |
| !Ref                 | Returns a resource’s reference value (name or ID)    | `Bucket: !Ref MyS3Bucket`                       |
| !GetAtt (Fn::GetAtt) | Retrieves a specific attribute (ARN, endpoint, etc.) | `Endpoint: !GetAtt MyLoadBalancer.DNSName`      |
| !Sub                 | Substitutes variables into strings (useful for ARNs) | `Resource: !Sub "arn:aws:s3:::${MyS3Bucket}/*"` |

Use these functions to wire resources together so CloudFormation understands dependencies and ordering.

## Optional resource fields worth noting

These fields help control lifecycle behavior, attach metadata, or gate resource creation. Use them to fine-tune how CloudFormation manages resources.

| Field          | Purpose                                            | Common Values / Notes                         |
| -------------- | -------------------------------------------------- | --------------------------------------------- |
| DependsOn      | Explicit creation order                            | Name or list of logical IDs                   |
| Metadata       | Arbitrary structured data attached to the resource | Useful for tooling or configuration data      |
| DeletionPolicy | Control behavior on stack deletion                 | `Delete`, `Retain`, `Snapshot` (for RDS/EBS)  |
| UpdatePolicy   | Rolling update / replacement behavior              | Used with AutoScaling/EC2/ELB updates         |
| Condition      | Create resource only if condition is true          | References Conditions defined at template top |

> **warning** Be cautious when renaming a resource’s logical ID. CloudFormation treats a renamed logical ID as a new resource and will create a replacement and delete the original (unless a DeletionPolicy prevents deletion), which can result in data loss or downtime.

## Best practices and tips

* Always use meaningful logical IDs — they’re referenced by other resources and appear in change sets.
* Favor intrinsic functions over hard-coded values to keep templates reusable.
* Use Conditions to create environment-specific resources (dev vs prod).
* Apply DeletionPolicy for stateful resources (S3, RDS) to avoid accidental data loss.
* Test changes using Change Sets to preview resource replacements and deletions.

## Summary

* Resources are the core building blocks of a CloudFormation template.
* Each resource requires a logical ID, a Type, and typically a Properties block.
* Connect resources with intrinsic functions (!Ref, !GetAtt, !Sub) so CloudFormation can determine dependency order.
* Use DependsOn for explicit ordering, and DeletionPolicy/UpdatePolicy/Metadata/Condition to manage lifecycle and behavior.

## Links and references

* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
* [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/index.html)
* [AWS RDS Documentation](https://docs.aws.amazon.com/rds/index.html)
* [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)

This lesson introduced CloudFormation resources, their structure, and how to connect and manage them inside templates. Subsequent material covers common resource types and practical multi-resource templates.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/c6a9b9c1-84c5-4d3e-957e-38673838de64/lesson/e801c737-432e-47b6-a4b6-56d032c2f434)
