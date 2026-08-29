# Demo Deleting nested stacks

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Nested-Stacks/Demo-Deleting-nested-stacks/page

Guide for safely deleting nested AWS CloudFormation stacks by removing the parent stack, using DeletionPolicy to retain resources when needed, and cleaning up template S3 buckets.

Welcome — this lesson shows the correct, safe way to remove nested AWS CloudFormation stacks and the resources they created. The core principle is simple and important:

* Always delete the parent (top-level) stack. Do not delete nested stacks individually. When you delete the parent, CloudFormation cascades deletion to its nested stacks and their resources unless you explicitly set retention policies.

Why this matters: manually deleting nested stacks can leave orphaned resources, break dependency ordering, and cause stack deletion failures.

Steps to delete nested stacks safely

1. Identify the parent (top-level) stack in the CloudFormation Stacks console — the stack that was created directly, not an AWS::CloudFormation::Stack resource inside another stack.
2. Select the parent stack and choose Delete.
3. Monitor the parent stack’s events. CloudFormation will start deleting nested stacks and the resources they own in the correct order.
4. Refresh related service consoles (S3, EC2, etc.) to confirm resources are being removed.
5. If you used a templates bucket to host nested-stack templates (for example, eden-kodekloud-lkjo-bkt-templates), empty it and then delete the bucket.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation &#x22;Stacks&#x22; console showing three stacks (DemoStack and two nested stacks) listed with status &#x22;UPDATE_COMPLETE&#x22; and creation timestamps. The page header shows the US East (Ohio) region and control buttons like Delete, Update stack, and Create stack." />
</Frame>

Important details about DeletionPolicy and UpdateReplacePolicy

* Nested stacks and their resources are deleted by default when the parent stack is deleted.
* To keep a nested stack or certain resources after deleting the parent, set DeletionPolicy: Retain on the nested-stack resource (or on specific resources).
* UpdateReplacePolicy controls behavior for resource replacement scenarios.

Examples

Minimal parent stack declaring two nested stacks:

```yaml theme={null}
Resources:
  S3Stack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://eden-kodekloud-lkjo-bkt-templates.s3.amazonaws.com/simple-s3.yaml

  EC2Stack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://eden-kodekloud-lkjo-bkt-templates.s3.amazonaws.com/simple-ec2.yaml
```

Make a nested stack retain its resources when the parent is deleted:

```yaml theme={null}
Resources:
  S3Stack:
    Type: AWS::CloudFormation::Stack
    DeletionPolicy: Retain
    Properties:
      TemplateURL: https://eden-kodekloud-lkjo-bkt-templates.s3.amazonaws.com/simple-s3.yaml
```

Quick reference: DeletionPolicy options

| DeletionPolicy value | Effect                                                                    |
| -------------------- | ------------------------------------------------------------------------- |
| Delete (default)     | Resource (or nested stack) is deleted when its stack is deleted.          |
| Retain               | Resource is left intact; CloudFormation stops managing it.                |
| Snapshot             | For supported resources (e.g., RDS), a snapshot is taken before deletion. |

Monitoring and verification

* Watch stack events in the CloudFormation console to see nested stack deletion progress and any errors.
* Check the service-specific consoles (S3, EC2, RDS, IAM, etc.) to confirm resources have been removed or retained according to policy.
* If a nested stack fails to delete, review the nested stack’s events to find the resource causing the failure.

Warning: do not delete nested stacks individually

<Callout icon="warning">
  Avoid deleting nested stacks directly from the console or API. Removing only the child stack may break the parent stack’s state and lead to orphaned resources or failed operations. Always delete the parent stack unless you intentionally used DeletionPolicy: Retain.
</Callout>

Cleaning up the templates bucket (S3)
If you used an S3 bucket to store nested stack templates (for example, eden-kodekloud-lkjo-bkt-templates), remove it after all nested-stack resources are cleaned up.

* To delete a non-empty bucket you must first empty it.
  * In the S3 console, select the bucket and choose Empty.
  * Confirm by typing the required confirmation phrase (for example, "permanently delete") and proceed.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing a confirmation dialog to permanently delete all objects in the bucket &#x22;eden-kodekloud-lkjo-bkt-templates,&#x22; with an input field requiring you to type &#x22;permanently delete&#x22; and buttons to Cancel or Empty. A blue banner above suggests using a lifecycle rule to more efficiently empty large buckets." />
</Frame>

* Once the bucket is empty, delete the bucket itself. The console will prompt you to type the bucket name to confirm deletion.

<Frame>
  <img alt="Screenshot of the AWS S3 console showing a &#x22;Delete bucket&#x22; confirmation for the bucket &#x22;eden-kodekloud-lkjo-bkt-templates,&#x22; asking the user to type the bucket name to confirm deletion. The dialog shows an input field and a disabled &#x22;Delete bucket&#x22; button with a &#x22;Cancel&#x22; link." />
</Frame>

Example S3 bucket resource used in child templates:

```yaml theme={null}
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
        - Key: Developer
          Value: John
```

Best practices and checklist

* Delete the parent stack to remove nested stacks and their resources in the correct order.
* Use DeletionPolicy or UpdateReplacePolicy when you need to preserve resources.
* Verify deletions in both CloudFormation and the individual AWS service consoles.
* Empty and delete any auxiliary S3 templates buckets after cleanup.
* Automate cleanup with scripts or CI/CD steps when possible to avoid manual mistakes.

<Callout icon="lightbulb">
  Best practice: delete the parent stack to remove nested stacks and their resources. Use DeletionPolicy and UpdateReplacePolicy to intentionally retain child stacks or resources during delete/replace operations. For more, see the AWS CloudFormation documentation on nested stacks and deletion policies.
</Callout>

References

* [AWS CloudFormation nested stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html)
* [AWS CloudFormation DeletionPolicy attribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html)
* [Amazon S3 console — empty and delete buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/delete-or-empty-bucket.html)

That completes the cleanup: parent stack deleted, nested stacks removed (or retained if specified), resources terminated or preserved per policy, and the templates bucket emptied and deleted.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/c7bfde08-7ccf-44bc-aa61-9949db5c41f3/lesson/760a5275-2210-4daa-8ab9-430e52dcde29" />
</CardGroup>
