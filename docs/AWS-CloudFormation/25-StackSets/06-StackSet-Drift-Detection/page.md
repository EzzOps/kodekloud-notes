# StackSet Drift Detection

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/StackSets/StackSet-Drift-Detection/page

Explains AWS CloudFormation StackSet drift detection, how it identifies and reports configuration drift across accounts and regions, and strategies to remediate or accept changes.

Welcome — in this lesson we'll explore StackSet drift detection in AWS CloudFormation: what it is, how it works, and practical steps to detect and remediate configuration drift across accounts and regions.

StackSet drift detection applies the same principles as standard CloudFormation drift detection but at the StackSet level. When enabled and run, CloudFormation compares each stack instance (the individual stacks deployed from a StackSet into member accounts and regions) against the StackSet template and reports any differences between the deployed resources and the template.

When a stack instance matches the template, CloudFormation reports it as IN\_SYNC. If a manual or out-of-band change has been made to a resource property (for example, an EC2 instance type changed from t3.micro to t3.large in one account/region), the affected stack instance is reported as DRIFTED and CloudFormation will enumerate the specific resource properties that differ.

<Frame>
  <img alt="A diagram showing AWS CloudFormation StackSet deployed to multiple Organizational Units and member accounts with stack instances in different regions. It illustrates checking those deployed stacks against the CloudFormation template to detect drift." />
</Frame>

## How StackSet drift detection works

* Scope: For each stack instance, CloudFormation compares the live resource configuration (the properties CloudFormation manages) with the StackSet template and the recorded stack template for that instance.
* Granularity: Detection is per stack instance. A single manual change in a single account or region marks that instance as DRIFTED while other instances can remain IN\_SYNC.
* Output: CloudFormation reports which resources drifted and which specific properties differ. This lets you choose to update the StackSet (or the affected instance) to restore conformity or accept the divergence.
* Consistency: Detecting drift helps enforce consistent configuration across multiple accounts and regions by flagging manual or out-of-band changes.

Key statuses and recommended actions:

| Status       | Meaning                                                          | Typical action                                                                            |
| ------------ | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| IN\_SYNC     | Deployed resources match the StackSet template for that instance | No action required                                                                        |
| DRIFTED      | One or more resources differ from the template                   | Inspect drift details and either update the StackSet/instance or accept the manual change |
| NOT\_CHECKED | Drift detection has not been run for this instance               | Run drift detection for the StackSet or individual instances                              |

<Frame>
  <img alt="A presentation slide titled &#x22;StackSet Drift Detection&#x22; showing two cards: one about detecting manual changes that can cause configuration inconsistencies, and the other about ensuring consistency across multiple stacks and environments." />
</Frame>

## Practical workflow

1. Enable drift detection for your StackSet (drift detection runs against stack instances).
2. Start drift detection for the StackSet.
3. Monitor the drift detection operation status and review the detected differences by instance and resource.
4. Remediate by updating the StackSet (or the individual stack instance) to match the desired template, or accept the change if appropriate.

Example CLI commands (start detection and check status):

```bash theme={null}
