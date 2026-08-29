# Demo Working with resource imports

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/CFN-init-and-Resource-Imports/Demo-Working-with-resource-imports/page

How to import an existing S3 bucket into an AWS CloudFormation stack and retain it using DeletionPolicy while mapping resources and verifying account, region, and ownership

In this lesson you’ll learn how to import an existing AWS resource (an Amazon S3 bucket) into an AWS CloudFormation stack. Importing is useful when a resource was created outside CloudFormation but you want to start managing it from a stack going forward.

Key scenario: import an existing S3 bucket into CloudFormation so its lifecycle and metadata are tracked by a stack while keeping the bucket and its objects intact.

Step 1 — Create the S3 bucket

* In the AWS console create a new S3 bucket. Ensure the bucket name is globally unique.
* Example bucket used in this demo: `eden-kodekloud-cvvb-bkt`.

Step 2 — Add a CloudFormation template that references the existing bucket
Open your project and add a file named `imports.yaml`. The file should contain a minimal resource definition for the bucket you want to import.

<Frame>
  <img alt="A Visual Studio Code window showing the Explorer for a workspace named &#x22;CF-PROJECT&#x22;, listing several YAML files (cfn-init.yaml, cli.yaml, ec2-instance.yaml, etc.). The file list has an input field with &#x22;import&#x22; typed in." />
</Frame>

Example `imports.yaml`:

```yaml theme={null}
Resources:
  MyImportedBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: eden-kodekloud-cvvb-bkt
```

Important template notes:

* Logical ID: `MyImportedBucket` can be any valid CloudFormation logical name. Use a meaningful name for clarity.
* `BucketName` must exactly match the existing S3 bucket’s name.
* `DeletionPolicy: Retain` prevents CloudFormation from deleting the bucket when the stack is deleted — CloudFormation requires resources being imported to be protected from accidental deletion.

<Callout icon="lightbulb">
  When importing existing resources, CloudFormation requires you to protect them from accidental deletion. Use `DeletionPolicy: Retain` (and optionally `UpdateReplacePolicy: Retain`) to ensure the resource is retained if the stack is deleted or replaced.
</Callout>

<Callout icon="warning">
  Before starting the import, verify:

  * The bucket exists in the same AWS account and region you’ll use for the stack.
  * The bucket is not already managed by another CloudFormation stack.
  * You map the template logical ID to the correct physical resource during the import workflow.
</Callout>

Step 3 — Import the resource using the CloudFormation console

1. Open the CloudFormation console and choose Create stack → Import resources (Import existing resources).
2. Upload the `imports.yaml` template file.
3. During the import workflow map the template logical ID (`MyImportedBucket`) to the existing S3 bucket's physical name (`eden-kodekloud-cvvb-bkt`).
4. Enter a stack name (for example, `DemoStack`) and proceed through the import steps.
5. Confirm and run the import. Wait for the import operation to complete.

When the import completes successfully the stack status will be `IMPORT_COMPLETE`.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing one stack named &#x22;DemoStack&#x22; with status &#x22;IMPORT_COMPLETE&#x22; and a created time of 2025-07-14 12:57:44 UTC+0400. The page also shows filter and stack action buttons at the top." />
</Frame>

Step 4 — Verify DeletionPolicy behavior
To demonstrate the effect of `DeletionPolicy: Retain`, delete the CloudFormation stack. The stack and CloudFormation metadata are removed, but the S3 bucket remains in your account because CloudFormation retained it.

<Frame>
  <img alt="A screenshot of the Amazon S3 console open to a bucket's Objects tab, showing toolbar buttons (Copy S3 URI/URL, Download, Open, Delete, Create folder, Upload) and a message indicating it's loading objects." />
</Frame>

If you want the bucket removed after deleting the stack, delete the bucket manually in the S3 console.

Quick checklist before importing an S3 bucket

| Requirement                  | Why it matters                          | Example/Action                           |
| ---------------------------- | --------------------------------------- | ---------------------------------------- |
| Exact bucket name            | CloudFormation matches by physical name | `BucketName: eden-kodekloud-cvvb-bkt`    |
| Same AWS account & region    | Imports are account/region-scoped       | Confirm console region matches bucket    |
| Not managed by another stack | Avoid resource ownership conflicts      | Check for existing stack associations    |
| Deletion protection          | Required to prevent accidental removal  | Add `DeletionPolicy: Retain` to template |

Links and references

* AWS CloudFormation Import Resources: [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import.html)
* AWS CloudFormation resource type: AWS::S3::Bucket: [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html)
* Amazon S3 documentation: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html)

That’s the basic workflow for importing an existing S3 bucket into a CloudFormation stack and ensuring it’s retained if the stack is removed.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/026ceaf9-07b6-4964-b49d-7190c136ea2b/lesson/cb055d17-5efa-43c7-a608-92cf84400d5c" />
</CardGroup>
