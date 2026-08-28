# Demo Resource cleanup

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Infrastructure-Composer/Demo-Resource-cleanup/page

Instructions to empty a demo S3 bucket, remove object versions if needed, and delete its CloudFormation stack to properly clean up demo AWS resources and avoid deletion failures.

In this lesson we remove resources created during previous demos so the next lesson begins with a clean environment. The primary objective is to empty and remove the demo S3 bucket, then delete the CloudFormation stack that created it. This ensures no orphaned resources remain and that stack state is consistent.

## Overview — why this matters

* AWS CloudFormation cannot delete S3 buckets that contain objects.
* If a stack-managed bucket is non-empty, stack deletion will fail and leave resources in an inconsistent state.
* Cleaning up via CloudFormation (when possible) preserves the stack lifecycle and avoids manual drift.

## Step 1 — Empty the demo S3 bucket

1. Open the Amazon Simple Storage Service (Amazon S3) console and find the bucket created by the demo stack. (Ignore any CloudFormation template buckets; focus on the demo bucket you used.)
2. Select the bucket.
3. Click the "Empty" action to remove all objects.
4. Confirm by typing `permanently delete` when prompted.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the &#x22;General purpose buckets&#x22; list with three buckets (one selected: eden-kodekloud-bncv-bkt) and action buttons like Copy ARN, Empty, Delete, and Create bucket. The table shows bucket names, region (US East Ohio), IAM Access Analyzer links, and creation dates." />
</Frame>

<Callout icon="warning">
  If the bucket has versioning enabled, simply emptying the bucket may not remove prior object versions. You must remove all versions (or suspend versioning and delete versions) before CloudFormation can delete the bucket. Attempting to delete a stack with a versioned, non-empty bucket will fail.
</Callout>

After emptying the bucket you should see a success notification showing how many objects were removed.

<Frame>
  <img alt="A screenshot of the AWS S3 console showing the &#x22;Empty bucket: status&#x22; page with a green notification saying the bucket &#x22;eden-kodekloud-bncv-bkt&#x22; was successfully emptied. The summary shows 1 object (26.2 KB) deleted and 0 failures." />
</Frame>

## Step 2 — Delete the CloudFormation stack

With the S3 bucket empty, remove the CloudFormation stack that created the demo resources:

* Open the AWS CloudFormation console.
* Select the stack you want to delete (for example, DemoStack).
* Click "Delete" to initiate the deletion process.
* Confirm the deletion in the modal.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console showing a &#x22;Delete stack?&#x22; confirmation dialog for a stack named &#x22;DemoStack,&#x22; warning that the deletion is permanent and will remove all stack resources. The modal shows options to cancel or proceed with deletion." />
</Frame>

Click "Delete" to start stack teardown. The deletion may take a short while—refresh the CloudFormation console to monitor progress. Once deletion completes, verify the demo S3 bucket no longer appears in the S3 console.

<Callout icon="lightbulb">
  Tip: You can delete an empty bucket directly from the S3 console, but preferring CloudFormation-driven deletion for stack-managed resources keeps the stack status accurate and reduces manual cleanup steps.
</Callout>

## Quick checklist

| Resource                | Action                                             | Expected result                                           |
| ----------------------- | -------------------------------------------------- | --------------------------------------------------------- |
| Demo S3 bucket          | Empty all objects (and delete versions if enabled) | Bucket becomes empty and displays success notification    |
| CloudFormation stack    | Delete stack from console                          | Stack transitions to DELETE\_IN\_PROGRESS then is removed |
| S3 console verification | Confirm bucket absence                             | Demo bucket is no longer listed                           |

## Troubleshooting

* If stack deletion fails due to the S3 bucket, confirm there are no remaining objects or versions in the bucket.
* For cross-account or permission issues, ensure your IAM user/role has S3 and CloudFormation delete permissions.
* For automated cleanup, consider scripting removal with the AWS CLI (aws s3 rm --recursive and aws cloudformation delete-stack).

## References

* [Amazon Simple Storage Service (Amazon S3)](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [AWS CloudFormation](https://learn.kodekloud.com/user/courses/aws-cloud-formation)

That's it — demo resources are cleaned up and you're ready for the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/563043d1-772f-4d1f-a812-f0a96dafa94f/lesson/a30d3939-5f6d-4ece-a7cd-39c418aeb4a5" />
</CardGroup>
