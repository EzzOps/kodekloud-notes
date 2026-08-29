# DemoModifying the name of an S3 Bucket

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/From-Template-to-Stack/DemoModifying-the-name-of-an-S3-Bucket/page

Explains how to set a custom Amazon S3 bucket name in AWS CloudFormation templates and covers naming rules, risks of renaming, and best practices like using DeletionPolicy retain.

In this lesson you'll learn how to give an Amazon S3 bucket a custom name when creating it with an AWS CloudFormation template. By default CloudFormation generates a unique name for S3 buckets unless you explicitly set the `BucketName` property in the resource's `Properties` section.

Why this matters:

* A custom bucket name can make resources easier to identify across environments.
* S3 bucket names must be globally unique, so plan names carefully.
* Renaming a bucket in a template often triggers replacement of the resource during stack updates.

Example — set a specific bucket name

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: eden-kodekloud-xcvt-bkt
```

What each part means:

* `Resources`: top-level mapping that contains all resources in the template.
* `MyS3Bucket`: logical name used inside the template.
* `Type`: AWS resource type (`AWS::S3::Bucket`).
* `Properties`: resource-specific configuration.
* `BucketName`: the explicit S3 bucket name you want CloudFormation to create.

| Resource element | Purpose                                                       | Example                          |
| ---------------- | ------------------------------------------------------------- | -------------------------------- |
| Resources        | Container for all resource declarations                       | `Resources:`                     |
| Logical ID       | Template-local name for the resource                          | `MyS3Bucket`                     |
| Type             | AWS resource type identifier                                  | `AWS::S3::Bucket`                |
| Properties       | Settings and options for the resource                         | `Properties:`                    |
| BucketName       | The explicit name for the S3 bucket (must be globally unique) | `BucketName: my-app-bucket-prod` |

<Callout icon="lightbulb">
  S3 bucket names must be globally unique and follow S3 naming rules (3–63 characters, lowercase letters, numbers, and hyphens). If you omit `BucketName`, CloudFormation generates a unique name for you. For more on naming rules see the AWS S3 documentation.
</Callout>

Best practices and considerations

* Use predictable naming conventions scoped by environment (for example, `myapp-prod-bucket`) to make lifecycle operations easier.
* To avoid accidental deletion during stack updates or deletions, consider adding a `DeletionPolicy: Retain` to the bucket resource so CloudFormation will not delete the bucket automatically:

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: eden-kodekloud-xcvt-bkt
    DeletionPolicy: Retain
```

* If you plan to manage bucket contents programmatically, remember CloudFormation does not empty a bucket before attempting deletion. Deleting a non-empty bucket fails and can cause stack updates to roll back.

<Callout icon="warning">
  Changing `BucketName` in a template typically causes CloudFormation to create a new bucket and attempt to delete the old one. If the new name is already owned by another account, the update will fail. Also, CloudFormation will not empty buckets for you — deletion of a bucket containing objects will fail. Plan carefully and use `DeletionPolicy: Retain` or other safeguards when renaming buckets.
</Callout>

Quick checklist before giving an explicit `BucketName`:

* Confirm the desired name is available and follows S3 naming rules.
* Decide whether the bucket should be retained on stack deletion (`DeletionPolicy: Retain`).
* If renaming, ensure downstream references (applications, IAM policies, DNS, etc.) are updated.
* Consider using environment-specific prefixes or account IDs to reduce naming collisions.

Links and references

* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
* [Amazon S3 bucket restrictions and limitations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-buckets.html)
* [CloudFormation resource and property types reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)

That’s all you need to specify a custom S3 bucket name in your CloudFormation template.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/d0ac0bcf-be2c-4c53-a2f7-8f59a760e9de/lesson/24cd1b06-03b1-48a2-a94b-06e369d8d73b" />
</CardGroup>
