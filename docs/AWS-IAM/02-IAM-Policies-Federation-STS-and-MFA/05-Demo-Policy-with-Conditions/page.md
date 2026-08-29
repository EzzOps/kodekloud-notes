# Demo Policy with Conditions

Source: https://notes.kodekloud.com/docs/AWS-IAM/IAM-Policies-Federation-STS-and-MFA/Demo-Policy-with-Conditions/page

This tutorial explains how to create an AWS IAM policy with IP and time-based restrictions for administrative actions.

## Demo Policy with IP and Time-Based Conditions

In this tutorial, you’ll learn how to create an AWS IAM policy that restricts administrative actions to:

* Two specific source IP address ranges
* A strict time window between 09:00 – 17:00 UTC

This approach is ideal for junior administrators or use cases requiring both network- and time-based controls.

***

### Prerequisites

* An AWS account with **IAM** permissions to create policies
* Familiarity with JSON policy syntax

***

## Step 1: Open the IAM Console

1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/).
2. Navigate to **IAM** → **Policies** → **Create policy**.
3. Select the **JSON** tab.

***

## Step 2: Define the Policy JSON

Paste the following JSON into the editor. This policy uses a single `Deny` statement with three conditions:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": [
            "200.200.200.0/24",
            "200.200.201.0/24"
          ]
        },
        "DateLessThan": {
          "aws:CurrentTime": "2023-10-08T09:00:00Z"
        },
        "DateGreaterThan": {
          "aws:CurrentTime": "2023-10-08T17:00:00Z"
        }
      }
    }
  ]
}
```

<Callout icon="lightbulb">
  Modify the `aws:CurrentTime` ISO 8601 values to reflect your desired UTC time window.
</Callout>

***

## Common IAM Condition Keys

| Condition Key   | Purpose                                               | Example Value                              |
| --------------- | ----------------------------------------------------- | ------------------------------------------ |
| NotIpAddress    | Deny if source IP is **outside** allowed CIDRs        | `["200.200.200.0/24", "200.200.201.0/24"]` |
| DateLessThan    | Deny if current time is **before** this UTC timestamp | `"2023-10-08T09:00:00Z"`                   |
| DateGreaterThan | Deny if current time is **after** this UTC timestamp  | `"2023-10-08T17:00:00Z"`                   |

***

## Step 3: Review and Create

1. Click **Next**.
2. Provide a **Name** (e.g., `JuniorAdminsPolicy`) and an optional **Description**.
3. Review the settings, then choose **Create policy**.

Search for your newly created policy by name in the IAM console to confirm that your IP and time-based restrictions are in place.

***

## Links and References

* [IAM JSON Policy Elements: Condition](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html)
* [AWS Security Best Practices](https://aws.amazon.com/architecture/security-best-practices/)
* [ISO 8601 Date and Time Format](https://en.wikipedia.org/wiki/ISO_8601)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-iam/module/8ffebc04-c194-403a-ac2e-2a2f0a6221ce/lesson/2b03ba3b-786b-46e0-ad6a-61d75a7f06f5" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/aws-iam/module/8ffebc04-c194-403a-ac2e-2a2f0a6221ce/lesson/9a97bc33-ae09-467f-9d44-0f16315d80aa" />
</CardGroup>
