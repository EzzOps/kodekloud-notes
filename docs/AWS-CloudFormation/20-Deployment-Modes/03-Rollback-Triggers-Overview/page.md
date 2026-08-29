# Rollback Triggers Overview

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Deployment-Modes/Rollback-Triggers-Overview/page

Explains using CloudFormation rollback triggers to monitor CloudWatch alarms during stack create or update and automatically revert deployments when alarms enter ALARM state.

Welcome to the lesson on rollback triggers in AWS CloudFormation. Rollback triggers let CloudFormation monitor one or more CloudWatch alarms during a stack create or update. If any specified alarm transitions into the ALARM state while the stack operation is in progress, CloudFormation automatically rolls back the stack operation. This helps prevent or cancel bad deployments when an integrated CloudWatch alarm detects unhealthy or unexpected conditions.

For example, if you have a CloudWatch alarm tracking high error rates or CPU saturation and that alarm moves to ALARM during a stack update that affects your application, CloudFormation can abort and roll back the update to avoid leaving the system in an unhealthy state.

<Frame>
  <img alt="A diagram titled &#x22;Rollback Triggers&#x22; showing CloudWatch Alarms triggering CloudFormation to roll back a Stack during stack creation/update. It notes this helps avoid bad deployments by cancelling changes." />
</Frame>

How rollback triggers work

* You specify rollback triggers in the stack's RollbackConfiguration. That configuration contains one or more RollbackTriggers, each pointing to a CloudWatch alarm (by ARN) and specifying a Type (for alarms, Type is `AWS::CloudWatch::Alarm`).
* During stack create or update operations, CloudFormation subscribes to the specified alarms. If any alarm transitions to the ALARM state while the stack operation is still in progress, CloudFormation initiates a rollback.
* Rollback triggers are only evaluated during create and update operations; they do not apply to stack deletion.

RollbackConfiguration fields

| Field            | Description                                                                                      | Example                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| RollbackTriggers | Array of objects that identify alarms to watch during the operation.                             | See JSON example below                                    |
| Arn              | The Amazon Resource Name (ARN) of the CloudWatch alarm. Must be in the same region as the stack. | `arn:aws:cloudwatch:us-east-1:123456789012:alarm:MyAlarm` |
| Type             | Resource type of the trigger; for CloudWatch alarms use `AWS::CloudWatch::Alarm`.                | `AWS::CloudWatch::Alarm`                                  |

How to supply rollback triggers

* API / SDK / CLI: Include the `RollbackConfiguration` JSON when calling `create-stack` or `update-stack`. Provide one or more `RollbackTriggers` with the alarm ARN and type.
* Console: When creating or updating a stack, set rollback triggers in the Advanced options section.

> **lightbulb** If the CloudWatch alarm is created in the same stack and the alarm is not yet fully active when CloudFormation starts evaluating rollback triggers, CloudFormation may not observe that alarm. To avoid this, reference existing alarms, create alarms in a separate stack first, or use nested stacks to control resource creation order.

Example: passing rollback triggers using the AWS CLI

```bash theme={null}
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --rollback-configuration '{"RollbackTriggers":[{"Arn":"arn:aws:cloudwatch:us-east-1:123456789012:alarm:MyAlarm","Type":"AWS::CloudWatch::Alarm"}]}'
```

Example JSON structure for the RollbackConfiguration

```json theme={null}
{
  "RollbackTriggers": [
    {
      "Arn": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:MyAlarm",
      "Type": "AWS::CloudWatch::Alarm"
    }
  ]
}
```

Important notes and best practices

* Rollback triggers only fire during stack create and update operations. They do not trigger rollback during stack deletion.
* The CloudWatch alarm must exist and be in the same AWS region as the stack. Cross-region alarm ARNs are not supported for rollback triggers.
* CloudFormation responds when an alarm transitions to the ALARM state. Other alarm states (INSUFFICIENT\_DATA, OK) do not cause rollback.
* If you need guarantees that an alarm is active before stack operations begin, create the alarm in a separate stack and reference it, or sequence resources via nested stacks.

> **warning** Ensure the CloudWatch alarm ARN and Type are correct and that the alarm is accessible in the same region before relying on it for rollback behavior—otherwise the rollback trigger will not function as intended.

Summary
Rollback triggers let you couple CloudFormation stack operations with CloudWatch alarms to abort and undo changes automatically when monitored conditions indicate problems. Use rollback triggers to increase deployment safety, especially in production or for critical resources.

Links and references

* [AWS CloudFormation RollbackConfiguration docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_RollbackConfiguration.html)
* [Amazon CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/68ab5c12-a35c-46b7-aef2-2e274c10989c/lesson/91ab42d3-d7dd-4f3d-b442-f1112683b56c)
