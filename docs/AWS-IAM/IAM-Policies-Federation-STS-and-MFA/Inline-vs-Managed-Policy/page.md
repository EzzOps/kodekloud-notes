# Inline vs Managed Policy

Source: https://notes.kodekloud.com/docs/AWS-IAM/IAM-Policies-Federation-STS-and-MFA/Inline-vs-Managed-Policy/page

This guide explores differences between AWS managed policies, customer managed policies, and inline policies, including when to use each type and a demo for granting temporary S3 access.

AWS Identity and Access Management (IAM) offers flexible controls to secure resources. In this guide, we explore the differences between AWS managed policies, customer managed policies, and inline policies. You'll learn when to use each type and see a hands-on demo for granting temporary S3 access.

## Scenario: Organizing Roles and Permissions

Sarah must implement access controls across multiple departments. Her workflow includes:

1. Mapping each **department** and listing team members’ responsibilities (e.g., John in HR handles onboarding).
2. Identifying required **AWS resources** and permission levels for every user.
3. Crafting **IAM policies**—collections of permissions tied to resources.
4. Creating **IAM groups** for teams with similar roles and attaching the appropriate policies.
5. Attaching **inline policies** to users, groups, or roles for unique scenarios.
6. Applying **resource-based policies** (e.g., for S3 buckets) where needed.

<Frame>
  ![The image shows "Sara's Task List," which includes six tasks related to employee management and policy creation, such as documenting responsibilities, creating access lists, and configuring resources.](https://kodekloud.com/kk-media/image/upload/v1752862989/notes-assets/images/AWS-IAM-Inline-vs-Managed-Policy/saras-task-list-employee-management.jpg)
</Frame>

Her manager has also requested a consolidated access control plan spanning Finance, Marketing, and IT:

<Frame>
  ![The image illustrates a manager's request for Sara to configure access control for all employees across three departments: Finance, Marketing, and IT. It shows icons representing employees in each department.](https://kodekloud.com/kk-media/image/upload/v1752862991/notes-assets/images/AWS-IAM-Inline-vs-Managed-Policy/manager-request-access-control-departments.jpg)
</Frame>

## Types of Identity-Based Policies

AWS IAM supports three identity-based policy types:

* **AWS Managed Policies**: Predefined and maintained by AWS.
* **Customer Managed Policies**: Custom, reusable policies you create and maintain.
* **Inline Policies**: Embedded within a single user, group, or role; not reusable.

<Frame>
  ![The image describes three types of identity policies: AWS Managed policies, Customer Managed policies, and Inline policies, highlighting their pros and cons.](https://kodekloud.com/kk-media/image/upload/v1752862993/notes-assets/images/AWS-IAM-Inline-vs-Managed-Policy/identity-policies-aws-managed-customer-inline.jpg)
</Frame>

### Policy Comparison Table

| Policy Type             | Maintenance         | Reuse  | Best For                                             |
| ----------------------- | ------------------- | ------ | ---------------------------------------------------- |
| AWS Managed Policy      | AWS-maintained      | High   | Common permissions across multiple accounts          |
| Customer Managed Policy | Customer-maintained | Medium | Tailored permissions shared across teams or projects |
| Inline Policy           | Entity-specific     | None   | One-off exceptions and tightly scoped use cases      |

<Callout icon="lightbulb">
  AWS managed policies simplify administration, but they may not cover every custom scenario. Use customer managed policies for greater control, and reserve inline policies for exceptional cases.
</Callout>

## Inline vs Managed: Key Differences

* **Inline Policies** attach directly to a single IAM entity (user, group, or role).
* **AWS Managed Policies** exist as separate objects and can be attached to multiple entities, even across AWS accounts, reducing duplication.

<Frame>
  ![The image illustrates AWS Managed Policies, showing how a single policy can be applied to users, groups, and roles across multiple AWS accounts. It highlights the ease of managing and updating policies at scale.](https://kodekloud.com/kk-media/image/upload/v1752862994/notes-assets/images/AWS-IAM-Inline-vs-Managed-Policy/aws-managed-policies-users-groups-roles.jpg)
</Frame>

## Demo: Granting Temporary S3 Access

In this example, we give the DevOps engineer, Alice, limited S3 access until year-end using a customer managed policy with a date-based condition.

Create the JSON policy document `temporary_s3_access_policy.json`:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "TemporaryS3Access",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::example-bucket",
        "arn:aws:s3:::example-bucket/*"
      ],
      "Condition": {
        "DateLessThanEquals": {
          "aws:CurrentTime": "2023-12-31T23:59:59Z"
        }
      }
    }
  ]
}
```

Then use the AWS CLI to create and attach the policy:

```bash theme={null}
aws iam create-policy \
  --policy-name TemporaryS3AccessPolicy \
  --policy-document file://temporary_s3_access_policy.json

aws iam attach-user-policy \
  --user-name Alice \
  --policy-arn arn:aws:iam::123456789012:policy/TemporaryS3AccessPolicy
```

<Callout icon="triangle-alert">
  Replace `123456789012` with your actual AWS account ID before running these commands.
</Callout>

## Next Steps

* Explore **multi-factor authentication (MFA)** to add an extra layer of security.
* Learn about **identity federation** and **STS** for single sign-on.
* Configure **AWS Resource Access Manager** to share resources across accounts.
* Set up **VPC endpoints** to control network traffic to AWS services.

## Links and References

* [IAM Policies and Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
* [Managed Policies vs. Inline Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html)
* [AWS CLI IAM Reference](https://docs.aws.amazon.com/cli/latest/reference/iam/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-iam/module/8ffebc04-c194-403a-ac2e-2a2f0a6221ce/lesson/c851c12c-edcf-44bc-832f-8e33848b1175" />
</CardGroup>
