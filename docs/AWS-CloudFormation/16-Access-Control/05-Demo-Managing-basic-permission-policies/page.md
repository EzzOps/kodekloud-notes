# Demo Managing basic permission policies

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Access-Control/Demo-Managing-basic-permission-policies/page

Demonstrates how changing IAM policies affects CloudFormation and S3 access by modifying a user’s permissions and observing console behavior, illustrating least privilege and required service permissions.

In this lesson we demonstrate how IAM permission policies affect access to AWS services using CloudFormation as an example. We'll modify the IAM user arno-cf’s policies from the root account, then observe how those changes immediately affect what the IAM user can do in the console (particularly around CloudFormation template uploads and stack operations).

Overview

* IAM user used in this demo: arno-cf
* Sign in to the AWS root account (in an incognito/private window) to change permissions, and keep a separate browser window signed in as arno-cf to observe the effect.

<Callout icon="warning">
  For safety: avoid using the root account for daily tasks. Use the root account only when necessary (for example, to modify IAM user policies), and ensure MFA is enabled on the root account.
</Callout>

Step 1 — Sign in as root and open a separate session as the IAM user

* Open an incognito/private browser session and sign in with your AWS root credentials.
* In a regular browser session, sign in with the IAM user arno-cf.
* This allows you to change the IAM user’s permissions from the root account and immediately observe the effect from the IAM user's session.

Step 2 — Inspect current permissions for the IAM user

* In this demo the IAM user originally had the AWS managed policy AdministratorAccess attached, allowing all actions.
* From the root account: navigate to IAM → Users → select arno-cf (arn:aws:iam::635573991785:user/arno-cf) → Permissions.
* For the demo, remove the AdministratorAccess policy to simulate a least-privilege configuration and see how service access is affected.

Step 3 — Observe behavior after removing AdministratorAccess

* After removing AdministratorAccess, switch to the IAM user’s session (or reload their AWS Management Console) and try to open CloudFormation and upload a template.
* You will typically see CloudFormation fail to load stacks or produce permission errors when uploading templates.

<Frame>
  <img alt="A dark-themed Windows file-open dialog is shown listing three YAML files (cli, ec2-instance, s3-bucket) inside a &#x22;cf-project&#x22; folder. Behind it, a browser window with the AWS console is partially visible." />
</Frame>

Example IAM error returned when attempting to upload a template (from the IAM user's session):

```text theme={null}
User: arn:aws:iam::635573991785:user/arno-cf is not authorized to perform: cloudformation:CreateUploadBucket because no identity-based policy allows the cloudformation:CreateUploadBucket action
```

What this error means

* CloudFormation needs the cloudformation:CreateUploadBucket permission to prepare a template upload (it often creates a temporary S3 upload bucket).
* In addition to the CloudFormation permission, you may also need S3 permissions (for example, s3:CreateBucket and s3:PutObject) for the bucket used to store the template.

Step 4 — Attach CloudFormation-specific permissions

* From the root account, add the AWS managed policy AWSCloudFormationFullAccess to the arno-cf user.
* AWSCloudFormationFullAccess grants full control over CloudFormation stack operations (create/update/delete). It does not automatically grant permissions for the underlying AWS services that your templates create (for example, EC2 or S3). You must also grant those service permissions separately.

<Frame>
  <img alt="A screenshot of two side-by-side AWS Console pages: the left shows the CloudFormation &#x22;Stacks&#x22; page with no stacks, and the right shows an IAM &#x22;Add permissions&#x22; dialog listing policies with &#x22;AWSCloudFormationFullAccess&#x22; selected. The Windows taskbar is visible at the bottom." />
</Frame>

After attaching AWSCloudFormationFullAccess:

* Reload the IAM user's CloudFormation console. The "Failed to load stacks" error should be resolved and the user can view and manage stacks.
* Uploading a template can still fail if the user lacks S3 permissions to create or write to the upload bucket.

Common console message when S3 permissions are missing:

```text theme={null}
Cannot prepare to upload template. You must be authorized to create an S3 bucket.
```

Step 5 — Attach S3 permissions

* From the root account, attach the managed policy AmazonS3FullAccess to the IAM user, or better: grant narrowly scoped S3 permissions (least-privilege) such as s3:CreateBucket and s3:PutObject limited to a specific bucket ARN or region.
* With CloudFormation and the appropriate S3 permissions, the console should succeed in creating the upload bucket and return a template URL similar to:

```text theme={null}
S3 URL: https://s3.us-east-2.amazonaws.com/cf-templates-vzm2aqs09qyo-us-east-2/2025-07-13T040416.546Z5v9-cli.yaml
```

Key point

* CloudFormation permissions allow you to manage stacks, but resource creation still depends on permissions for each AWS service referenced by the template (e.g., EC2, RDS, Lambda). If the IAM user lacks those resource-level permissions, stack operations will fail during create/update.

<Callout icon="lightbulb">
  Best practice: follow the principle of least privilege. Grant only the actions and specific resources required—e.g., CloudFormation access plus targeted S3 upload permissions, and any resource-specific privileges (EC2, RDS) only when needed.
</Callout>

Step 6 — Restore AdministratorAccess (optional)

* If you need to return arno-cf to its previous elevated state for testing, re-attach the AdministratorAccess managed policy from the root account.
* After re-attaching, reload the IAM user's console session to ensure the new permissions take effect.

<Frame>
  <img alt="A screenshot of a Windows desktop with two browser windows open to the AWS Management Console. The left pane shows CloudFormation Stacks (no stacks), and the right pane shows an IAM user page for &#x22;arno-cf&#x22; with console access enabled (without MFA) and account details." />
</Frame>

Quick reference: common managed policies and their use cases

| Managed Policy              | Purpose / Use Case                                                                                                               |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| AdministratorAccess         | Full administrative access to all AWS resources (not recommended for everyday use).                                              |
| AWSCloudFormationFullAccess | Full CloudFormation stack management (create/update/delete). Does NOT grant permissions to create resources used by templates.   |
| AmazonS3FullAccess          | Full S3 permissions (use with caution). Prefer scoped S3 policies granting s3:CreateBucket and s3:PutObject on specific buckets. |

Troubleshooting checklist

* If CloudFormation shows "Failed to load stacks": confirm cloudformation:\* permissions are present.
* If template upload fails with CreateUploadBucket error: ensure cloudformation:CreateUploadBucket and S3 permissions (s3:CreateBucket, s3:PutObject) exist.
* If stack creation fails while provisioning resources: check permissions for each service referenced by the template (EC2, RDS, IAM, Lambda, etc.).

Summary

* Removing AdministratorAccess prevents many actions for the IAM user; attaching service-specific managed policies (for example, AWSCloudFormationFullAccess and AmazonS3FullAccess) restores the ability to use those services.
* CloudFormation requires both CloudFormation API permissions and permissions for any AWS resources the template creates.
* Always apply least-privilege principles: grant CloudFormation and minimal S3 access for template uploads, and add resource-specific permissions only when template actions require them.

Links and references

* [AWS CloudFormation Concepts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
* [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
* [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/index.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/913fb901-ca2a-4ed9-8d12-2abd519c1393/lesson/89fd794b-ce62-4fb4-aa49-bf6527fdfb63" />
</CardGroup>
