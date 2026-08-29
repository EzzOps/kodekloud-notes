# Demo Creating a custom permission policy Update a stack Part 1

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Access-Control/Demo-Creating-a-custom-permission-policy-Update-a-stack-Part-1/page

Guide to create a minimal IAM policy granting a limited user permissions to list and describe CloudFormation stacks, with steps to test and later extend for updates.

In this lesson you'll create a minimal custom IAM policy that lets a limited user view CloudFormation stacks and later be extended to update them. Workflows covered:

* Create a limited IAM user for testing.
* Sign in as that limited user (use an incognito window) to confirm initial lack of permissions.
* Create a simple CloudFormation stack with an administrator account.
* Build and attach a minimal custom IAM policy to allow listing and describing stacks.

Prerequisites:

* Administrator access to the AWS account (in this lesson: Arno Pretorius).
* A second browser (or an incognito window) to sign in as the limited user for side-by-side verification.

## 1 — Create the limited IAM user

Sign in as the administrator (Arno Pretorius) and create a test user called `limited-user-cfn`. Grant AWS Management Console access and set a password; do not attach any permissions yet — we’ll attach a custom policy later.

<Frame>
  <img alt="A screenshot of the AWS IAM &#x22;Create user&#x22; console showing the &#x22;Specify user details&#x22; step. The &#x22;User name&#x22; field is active with &#x22;limite&#x22; entered and options for console or programmatic access are visible." />
</Frame>

When creating the user, make sure “AWS Management Console access” is selected and choose a password option. For this lesson, skip attaching any policies at creation time.

<Frame>
  <img alt="A screenshot of the AWS IAM &#x22;Create user&#x22; workflow showing the &#x22;Set permissions&#x22; step. It displays permission options like &#x22;Add user to group,&#x22; &#x22;Copy permissions,&#x22; and &#x22;Attach policies directly.&#x22;" />
</Frame>

## 2 — Sign in as the limited user (verify no permissions)

Open an incognito/private browser window and sign in as `limited-user-cfn` using your account alias or account ID. From the IAM dashboard you can confirm the account details (account ID, alias, sign-in URL).

<Frame>
  <img alt="A screenshot of the AWS IAM Dashboard showing security recommendations (MFA status and prompts) on the left and AWS account details (account ID, account alias, and sign-in URL) on the right." />
</Frame>

Choose the region used for this lesson — for example, US East (Ohio) / us-east-2.

<Frame>
  <img alt="A screenshot of the AWS Management Console Home showing the &#x22;Recently visited&#x22; panel (no recent services) and a region selector dropdown open listing regions like N. Virginia, Ohio, Mumbai, and Tokyo. The browser window and taskbar are also visible." />
</Frame>

Tip: Keep the admin session (Arno Pretorius) in one window and the limited-user session in another browser or split-screen so you can compare behavior side-by-side while testing.

## 3 — Create a simple CloudFormation stack (as admin)

Back in the administrator session, create a simple stack that the limited user will later try to view. From the CloudFormation console choose “Create stack → With new resources (standard)” and upload a small template. Example (S3 bucket):

```yaml theme={null}
Mappings:
  DevMap:
    Arno:
      Field: Quality assurance
      Env: Testing/development
    Alice:
      Field: Backend developer
      Env: Production

Parameters:
  InputBucketName:
    Type: String
    Description: Name for the S3 bucket (must be DNS-compliant and globally unique)

Resources:
  DemoBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref InputBucketName
```

Select the template and continue to the stack details.

<Frame>
  <img alt="A split-screen screenshot of the AWS Management Console: the left shows the CloudFormation &#x22;Create stack&#x22; template selection panel, and the right shows the Console Home page with &#x22;No recently visited services.&#x22;" />
</Frame>

Provide a stack name (for example `demo-stack`) and fill the `InputBucketName` parameter with a globally unique value (for example `arno-pretorius-kodekloud-kljk-pkt`) before creating the stack.

<Frame>
  <img alt="A split-screen screenshot of the AWS Management Console: the left side shows the CloudFormation &#x22;Create stack&#x22; page with an uploaded template file named &#x22;s3-bucket.yaml,&#x22; and the right side shows the Console Home with no recently visited services." />
</Frame>

While the stack is creating, switch to the limited-user session and open the CloudFormation console. Because the limited user has no permissions yet, the console will fail to list stacks.

<Frame>
  <img alt="A split-screen screenshot of the AWS Management Console: the left side shows the IAM Policies page listing policies, and the right side shows the CloudFormation Stacks page with a red &#x22;Failed to load stacks&#x22; error banner." />
</Frame>

## 4 — Build a minimal custom policy to view stacks

Next, create a minimal IAM policy that grants permissions to list and describe CloudFormation stacks. In the administrator session go to IAM → Policies → Create policy → JSON editor and enter:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListAndDescribeCloudFormation",
      "Effect": "Allow",
      "Action": [
        "cloudformation:ListStacks",
        "cloudformation:DescribeStacks"
      ],
      "Resource": "*"
    }
  ]
}
```

What these actions do:

* cloudformation:ListStacks — list stacks in the account (required for the console stacks table).
* cloudformation:DescribeStacks — read details for a specific stack (status, outputs, parameters).
* Resource: "\*" — CloudFormation list/describe operations are account/stack-level and typically require account-wide resource access.

| Action                                | Use case                                | Notes                                             |
| ------------------------------------- | --------------------------------------- | ------------------------------------------------- |
| cloudformation:ListStacks             | Show the list of stacks in the console  | Required to populate the stacks table             |
| cloudformation:DescribeStacks         | View a stack's details, status, outputs | Required to view stack details in the console     |
| cloudformation:UpdateStack (optional) | Update a stack                          | Add later when you want the user to modify stacks |
| cloudformation:DeleteStack (optional) | Delete a stack                          | Add later if deletion must be allowed             |

<Callout icon="lightbulb">
  Note: Some CloudFormation actions require Resource: "\*" (account-level access). When later granting update or delete permissions, add actions such as `cloudformation:UpdateStack`, `cloudformation:DeleteStack`, and change-set actions. Scope permissions to specific stacks or use IAM conditions where possible to follow least privilege.
</Callout>

<Callout icon="warning">
  Warning: S3 bucket names must be globally unique. Never publish real credentials or sensitive data in templates. Keep your administrator session secure and avoid leaving admin-level access open in long-lived browser windows during testing.
</Callout>

## 5 — Attach the policy and verify access

Attach the newly created policy to `limited-user-cfn` (IAM → Users → limited-user-cfn → Add permissions → Attach policies). Then sign in as the limited user (or refresh the session). The CloudFormation console should now load the stacks list and allow viewing stack details.

From here you can:

* Extend the policy to allow updates (e.g., `cloudformation:UpdateStack`, `cloudformation:CreateChangeSet`, `cloudformation:ExecuteChangeSet`) and scope it to specific stack ARNs.
* Use IAM conditions (such as `aws:ResourceTag`) to restrict which stacks a user can modify.
* Test changes in the limited-user session to verify least-privilege behavior.

## Links and references

* [AWS CloudFormation Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
* [IAM User Guide — Policies and Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
* [IAM JSON Policy Elements: Principal, Action, Resource, Condition](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html)

This completes Part 1: creating a minimal policy that allows viewing CloudFormation stacks. In the next part you'll extend the policy to permit safe, scoped stack updates.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/913fb901-ca2a-4ed9-8d12-2abd519c1393/lesson/9eba3f9b-84f3-4e09-ab0f-9972a71ea1ca" />
</CardGroup>
