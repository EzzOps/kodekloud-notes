# Rollback trigger example (within a RollbackConfiguration)
RollbackConfiguration:
  MonitoringTimeInMinutes: 10
  RollbackTriggers:
    - Arn: arn:aws:cloudwatch:us-east-1:123456789012:alarm:CloudWatchAlarm1
      Type: AWS::CloudWatch::Alarm
```

Now update the CloudFormation stack and attach the CloudWatch alarm as a rollback trigger:

1. In the CloudFormation console select the stack → Update stack.
2. Choose “Use existing template” (or the appropriate template option) → Next.
3. Use the default parameter values (or modify if needed) and continue to Configure stack options.
4. In the Configure stack options page, scroll to Rollback configuration and add the rollback trigger: set the monitoring time (minutes) and paste the alarm ARN (copy the ARN from the CloudWatch alarm details).
5. Review the changes and submit the update.

<Frame>
  <img alt="A screenshot of the AWS CloudFormation console on the &#x22;Update stack&#x22; page showing the &#x22;Prerequisite - Prepare template&#x22; step with three template options (the &#x22;Use existing template&#x22; option selected). The left sidebar shows the update workflow steps (Update stack, Specify stack details, Configure stack options, Review DemoStack)." />
</Frame>

Important behavior and troubleshooting

> **warning** If any specified CloudWatch alarm is in ALARM during the configured MonitoringTimeInMinutes window, CloudFormation treats the operation as failed and rolls back. If an alarm is already in ALARM when you start the update, the update may fail immediately depending on the monitoring window. Choose monitoring windows carefully to allow resources to stabilize and metrics to be collected.

In this demo the alarm was already in ALARM when the update began, so the stack update failed and CloudFormation reported "Update rollback complete (failed)". Always verify alarm states (OK) before initiating critical updates if you want the rollout to proceed.

Clean up resources when finished:

* Delete the CloudFormation stack (CloudFormation console → select stack → Delete).
* Delete the CloudWatch alarm: in CloudWatch go to Alarms, select the alarm, open Actions → Delete, and confirm.

<Frame>
  <img alt="A screenshot of the AWS CloudWatch Alarms console showing one alarm (CWAlarm1) selected and in state &#x22;In alarm,&#x22; with the Actions menu open and the &#x22;Delete&#x22; option highlighted. The sidebar navigation and top controls like &#x22;Create alarm&#x22; and &#x22;Create composite alarm&#x22; are also visible." />
</Frame>

Best practices and quick reference

| Topic                     | Recommendation                                      | Why it matters                                   |
| ------------------------- | --------------------------------------------------- | ------------------------------------------------ |
| Alarm state before update | Ensure alarms are in OK state                       | Prevents immediate rollback on start             |
| MonitoringTimeInMinutes   | Long enough for stabilization (e.g., 5–15 minutes)  | Allows metrics to converge; avoid false failures |
| Tagging resources         | Tag EC2 instances (Name, Environment)               | Makes selecting per-instance metrics easier      |
| Testing                   | Validate alarm behavior in lower environments first | Ensures rollback logic works as expected         |

> **lightbulb** * Ensure alarms used as rollback triggers are in an OK state before starting critical stack operations.
  * Use tags to help find per-instance metrics quickly when creating alarms.
  * Set the monitoring time long enough for resources and metrics to stabilize, but short enough to avoid excessive delays.

Links and references

* [CloudFormation Rollback Triggers documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-rollback-triggers.html)
* [CloudWatch Alarms documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)

This workflow helps you protect deployments by tying CloudFormation operations to CloudWatch alarm states so that metric-driven failures automatically prevent or roll back unsafe changes.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/68ab5c12-a35c-46b7-aef2-2e274c10989c/lesson/7b077bc4-ae18-4599-a801-a03fa9e9bb99)


# Evaluating Stack Creation Failures

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Deployment-Modes/Evaluating-Stack-Creation-Failures/page

Guidance for diagnosing and recovering AWS CloudFormation stack creation failures, especially ROLLBACK_COMPLETE, using events, resource logs, permission checks, then deleting and recreating the stack.

Welcome — this lesson explains how to diagnose and recover from AWS CloudFormation stack creation failures, with a focus on the ROLLBACK\_COMPLETE state. When you create a stack (provide a template, parameters, and click Create), CloudFormation attempts to provision all resources. If a creation error occurs, CloudFormation will usually roll back any partially created resources and place the stack into a terminal failed state named ROLLBACK\_COMPLETE.

What ROLLBACK\_COMPLETE means:

* The stack creation failed.
* CloudFormation attempted to delete any partially created resources.
* The stack is in a terminal state and cannot be updated or repaired in place.
* You must delete the failed stack and recreate it after fixing the root cause.

<Frame>
  <img alt="A presentation slide titled &#x22;Evaluating Stack Creation Failures&#x22; showing a ROLLBACK_COMPLETE state with icons for creation failed, partial resources cleaned up, and stack creation unsuccessful. It notes that failed stacks can't be updated or fixed and must be deleted and recreated." />
</Frame>

Recommended troubleshooting and recovery steps

1. Inspect the stack Events tab
   * The Events timeline shows the sequence of create/delete actions and any error messages returned by resource providers. Identify the first resource that reported an error — that is usually the root cause.
2. Check resource-specific logs and consoles
   * For Lambda: CloudWatch Logs.
   * For EC2: EC2 console and instance system logs (or CloudWatch if configured).
   * For S3 or API access errors: check S3 console, bucket policies, and IAM policies.
3. Verify permissions and configuration
   * Confirm IAM roles/policies referenced by resources exist and have required permissions.
   * Validate template parameters, resource names, ARNs, VPC/subnet IDs, and other environment-specific values.
4. Fix the underlying issue in the template, parameter set, or account configuration.
5. Delete the failed stack (required for ROLLBACK\_COMPLETE) and recreate the stack after applying the fix.

Troubleshooting checklist (summary)

| Step                      | Action                                               | Why it helps                                                 |
| ------------------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| Inspect Events            | Open the CloudFormation Events tab                   | Shows which resource failed and the provider error message   |
| Check resource logs       | CloudWatch Logs, EC2 console, S3 console             | Provides detailed error information from the resource        |
| Validate IAM & parameters | Confirm roles, policies, input values                | Prevents permission and configuration failures               |
| Delete & recreate         | Remove the ROLLBACK\_COMPLETE stack and create again | ROLLBACK\_COMPLETE stacks are terminal and cannot be updated |

Helpful AWS CLI commands

* Delete a failed stack:

```bash theme={null}
aws cloudformation delete-stack --stack-name my-stack
```

* View recent stack events (helps identify the failing resource):

```bash theme={null}
aws cloudformation describe-stack-events --stack-name my-stack
```

* Check current stack status:

```bash theme={null}
aws cloudformation describe-stacks --stack-name my-stack --query 'Stacks[0].StackStatus' --output text
```

> **lightbulb** A stack in ROLLBACK\_COMPLETE represents a terminal create failure. You cannot update it in place — you must delete it and create a new stack once the cause of the failure is resolved.

Keep in mind

* CloudFormation’s default create-time behavior is “all-or-nothing”: it attempts to leave no partial infrastructure by rolling back on failures.
* Use the Events tab plus resource logs to pinpoint the first failing resource, correct the root cause, then delete and recreate the stack.
* When iterating on templates, test changes in smaller or isolated stacks to reduce rebuild time and risk.

Links and references

* [CloudFormation course](https://learn.kodekloud.com/user/courses/aws-cloud-formation) — learn.kodekloud
* [CloudWatch Logs](https://learn.kodekloud.com/user/courses/aws-cloudwatch)
* [Lambda course](https://learn.kodekloud.com/user/courses/aws-lambda)
* [EC2 course](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* [S3 course](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [IAM course](https://learn.kodekloud.com/user/courses/aws-iam)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/68ab5c12-a35c-46b7-aef2-2e274c10989c/lesson/e76302b1-9425-4ad2-a88a-ae784787b824)
