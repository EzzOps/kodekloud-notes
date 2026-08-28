# Start drift detection for a StackSet
aws cloudformation detect-stack-set-drift --stack-set-name MyStackSet

# Check the status of a drift detection operation (use the returned detection ID)
aws cloudformation describe-stack-set-drift-detection-status --stack-set-name MyStackSet --drift-detection-id <detection-id>
```

For detailed per-instance drift results and remediation steps, consult the CloudFormation console or the API/CLI documentation linked below.

<Callout icon="lightbulb">
  Not all AWS resource types and properties are supported by CloudFormation drift detection. Some runtime attributes or provider-managed values may not be compared. Always review the drift results and consult the CloudFormation documentation for the current list of supported resource types and limitations.
</Callout>

## Remediation strategies

* Update the StackSet template and perform a StackSet operation to push the desired configuration to all affected instances.
* Update a single stack instance if the change should only apply to one account/region.
* If the manual change is intended, document and accept it, or update the StackSet/template to reflect the new desired state.

## Where to learn more

* AWS CloudFormation drift detection: [https://docs.aws.amazon.com/[AWS_SECRET_ACCESS_KEY]-cfn-stack-drift.html](https://docs.aws.amazon.com/[AWS_SECRET_ACCESS_KEY]-cfn-stack-drift.html)
* AWS CloudFormation StackSets: [https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-is-cfnstacksets.html](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-is-cfnstacksets.html)

This extends CloudFormation’s drift model from individual stacks to the distributed footprint created by StackSets, helping you detect and manage manual changes across organizational units, accounts, and regions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/13ed2c0a-3a8a-45b0-870a-6c267c392190/lesson/d015536e-ce40-40f2-9cd9-54fa8b1debf9" />
</CardGroup>


# StackSets Introduction

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/StackSets/StackSets-Introduction/page

Overview of AWS CloudFormation StackSets for centrally deploying, updating, and deleting consistent CloudFormation stacks across multiple AWS accounts and regions using administrator account control

In this lesson we cover AWS CloudFormation StackSets: a feature that lets you deploy and manage identical CloudFormation stacks across multiple AWS accounts and regions from a single central operation.

StackSets are ideal when you need the same infrastructure deployed consistently across environment tiers (development, test, production) or across multiple AWS accounts and regions. Instead of manually recreating a stack in each account/region, you define one StackSet with its template and parameters, then target the accounts and regions where stack instances should be created.

<Frame>
  <img alt="A slide diagram showing an AWS CloudFormation StackSet deploying stack instances across Organizational Units and member accounts in multiple regions. On the right it lists environment tiers (Development, Test, Production) with the caption &#x22;Keep things consistent.&#x22;" />
</Frame>

Why use StackSets?

* Centralized operations: create, update, and delete stacks across many accounts and regions from a single administrator (management) account.
* Consistency: ensure identical templates and parameter values are applied across targets.
* Scale: efficiently deploy infrastructure at organization scale using Organizational Units (OUs) or explicit account lists.

<Callout icon="lightbulb">
  Before deploying StackSets at scale, confirm your deployment permission model: service-managed permissions or self-managed permissions. With self-managed permissions, you must create an administrator IAM role in each target account that the management account can assume.
</Callout>

Terminology and behavior

| Term           | Meaning                                                                                                          | Example / Note                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| StackSet       | The CloudFormation construct that stores the template, parameter values, and target accounts/regions.            | The central definition you manage from the administrator account.           |
| Stack instance | A standard CloudFormation stack created from the StackSet in a specific account and region.                      | Each stack instance appears in the target account’s CloudFormation console. |
| Targets        | Where the StackSet deploys stack instances — can be specific accounts, a list of accounts, or OUs, plus regions. | Use OUs to target all member accounts in an organizational unit.            |

Important behavioral notes:

* Management scope: StackSets are created and controlled from an administrator (management) account, but the resulting stack instances are deployed into target member accounts and regions.
* Visibility: To inspect resources created by a stack instance, open the CloudFormation console in the target account and region where the instance was provisioned.

StackSet operations

* Create — deploys stack instances across the specified accounts and regions based on the StackSet definition.
* Update — modifies the StackSet template or parameters and propagates changes to existing stack instances.
* Delete — removes stack instances and, when no instances remain, allows deletion of the StackSet itself.

<Frame>
  <img alt="A diagram titled &#x22;StackSet Operations&#x22; showing an AWS CloudFormation StackSet at the top deploying stack instances into member accounts grouped under Organizational Units (OUs) across multiple regions. To the right are colored circular icons labeled Create, Update, and Delete representing available operations." />
</Frame>

Important deletion behavior

* A StackSet cannot be deleted while it still has associated stack instances. Remove all stack instances first (either individually or via the StackSet delete-instances operation), then delete the StackSet itself.
* Consider resource dependencies and deletion order across accounts and regions to avoid orphaned or dependent resources being left behind.

<Callout icon="warning">
  When deleting stack instances across accounts and regions, review cross-account and cross-region dependencies. Deleting in the wrong order can leave orphaned resources or cause failures that require manual remediation.
</Callout>

Quick operational checklist

* Choose permission model: service-managed (recommended for AWS Organizations) or self-managed.
* Prepare IAM roles: for self-managed, create administrator roles in target accounts; for service-managed, confirm organization permissions.
* Test in a small set of accounts/regions first before large-scale deployments.
* Monitor stack instance drift, failures, and stack events in each target account/region.

Further reading and references

* [AWS CloudFormation — StackSets (AWS Docs)](https://docs.aws.amazon.com[AWS_SECRET_ACCESS_KEY]-is-cfnstacksets.html)
* [AWS Organizations (overview)](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)
* [AWS IAM documentation](https://docs.aws.amazon.com/iam/latest/UserGuide/introduction.html)
* [CloudFormation course on KodeKloud](https://learn.kodekloud.com/user/courses/aws-cloud-formation)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/13ed2c0a-3a8a-45b0-870a-6c267c392190/lesson/6b6e5492-0397-4e3a-8001-7bd10141911b" />
</CardGroup>
