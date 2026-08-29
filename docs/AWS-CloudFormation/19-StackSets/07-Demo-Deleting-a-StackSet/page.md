# Demo Deleting a StackSet

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/StackSets/Demo-Deleting-a-StackSet/page

Guide for safely deleting an AWS CloudFormation StackSet by removing stack instances, verifying resource cleanup, monitoring operations, and handling common failures and permissions issues.

This guide shows the recommended, safe procedure to delete an AWS CloudFormation StackSet and its stack instances. You cannot delete a StackSet while it still has stack instances — you must remove the instances first, then delete the StackSet itself. Follow the sequence below to avoid failures and orphaned resources.

Quick checklist

* Delete all stack instances from the StackSet (across target accounts and regions).
* Verify all stack resources were removed (S3 buckets, IAM roles, etc.).
* Delete the StackSet itself once instances are gone.

Overview of steps

1. Remove stack instances from the StackSet (specify target account(s) and region(s)).
2. Monitor the StackSet operations until the delete operation completes for each instance.
3. Confirm external resources (for example, S3 buckets) were deleted or handled.
4. Delete the StackSet record from the CloudFormation console.

Step-by-step

1. Open the StackSet in the CloudFormation console, select the StackSet you want to remove, open the Actions menu, and choose "Delete stacks from stack set". Provide the target account number(s) and select the region(s) that contain the stack instances you want to delete (for example, eu-west-1 and us-east-1). Confirm and submit the deletion.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation StackSets console showing one stack set named &#x22;DemoStackSet&#x22; (SELF_MANAGED) with the Actions menu open listing options like Add stacks, Edit details, Override parameters, Detect drift, and Delete." />
</Frame>

2. After submitting the delete request, monitor operations for progress. The delete operation appears under the Operations tab and shows statuses such as RUNNING while in progress, then SUCCEEDED or FAILED once complete.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation StackSets console on the &#x22;DemoStackSet&#x22; Operations tab showing a DELETE operation with status &#x22;RUNNING,&#x22; its operation ID, and created time. The UI also displays tabs for StackSet info, Stack instances, Parameters, Template, and an Actions button." />
</Frame>

3. Watch the Stack instances tab to follow progress for each instance. Instances may show PENDING or IN\_PROGRESS while being removed. When deletion finishes successfully, instance entries will disappear from the list.

4. Verify external resources created by the stacks were removed in the regions you targeted. For example, CloudFormation cannot delete S3 buckets that still contain objects — if a bucket is not empty, the stack delete for that resource will fail. You will need to empty or delete the bucket manually, or design your stack to remove bucket contents during deletion. In this demo, the stacks created buckets in eu-west-1 and us-east-1; after deleting the stack instances those buckets were removed because they were empty.

5. Once all stack instances are removed, the StackSet remains in the console until you explicitly delete it. To finish, select the StackSet, open Actions, choose "Delete stack set", and confirm. After this, the StackSet will no longer appear in your StackSets list.

Troubleshooting and common causes of failure

| Symptom                                       | Likely cause                                                    | Recommended action                                                                                                                   |
| --------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Stack instance deletion fails                 | Resource-level delete error (for example, non-empty S3 buckets) | Check stack Events for error details; empty S3 buckets or remove problematic resources manually and retry.                           |
| Operation shows FAILED or times out           | Insufficient IAM permissions to delete resources                | Ensure the executing principal has the required CloudFormation and resource permissions in target accounts/regions.                  |
| StackSet still shows instances after deletion | Operation still in progress or rollback occurred                | Wait for operations to complete; inspect Events and the Operations tab for failure reasons and re-run delete after resolving issues. |
| Stacks retained unexpectedly                  | Retain-stacks option was enabled                                | Re-run delete without retaining stacks or manually remove retained resources.                                                        |

Best practices

* Always delete stack instances before deleting the StackSet record.
* Review stack templates for resources that require manual cleanup (S3, EBS snapshots, RDS snapshots).
* Use the Operations and Stack instances tabs to monitor progress and retrieve error details.
* For automation, you can script StackSet deletes via the AWS CLI or SDKs, but ensure you handle non-deletable resources and permissions in advance.

Links and references

* [AWS CloudFormation StackSets concepts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html)
* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/index.html)
* [CloudFormation course on KodeKloud](/user/courses/aws-cloud-formation)
* [Amazon S3 course on KodeKloud](/user/courses/amazon-simple-storage-service-amazon-s3)

> **lightbulb** Always delete stack instances before attempting to delete a StackSet. Deleting instances first ensures that the resources created by those stacks are removed cleanly and avoids operation failures.

Remember: delete your stack instances first, then delete the StackSet.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/13ed2c0a-3a8a-45b0-870a-6c267c392190/lesson/70250eef-93e6-4809-96c6-4447c5d1976d)
