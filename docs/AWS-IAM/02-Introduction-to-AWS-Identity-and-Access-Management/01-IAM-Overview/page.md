# fatal error: An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
```

***

## Step 3: Define the Session Policy

Create a JSON policy that allows listing, reading, and uploading:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject"
    ],
    "Resource": [
      "arn:aws:s3:::company1-hr",
      "arn:aws:s3:::company1-hr/*"
    ]
  }]
}
```

| Action        | Description                      |
| ------------- | -------------------------------- |
| s3:ListBucket | List the bucket’s objects        |
| s3:GetObject  | Download or read bucket objects  |
| s3:PutObject  | Upload new objects to the bucket |

> **lightbulb** Save this policy as `SessionPolicy-UploadFile.json` and upload it as a **customer-managed policy** named **SessionPolicy-UploadFile**.

***

## Step 4: Create and Configure the IAM Role

1. In the IAM console or via AWS CLI, create a role **JohnUploadRole**.
2. Attach the `SessionPolicy-UploadFile` policy to this role.

Update the role’s trust policy so that **John** can assume it:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "AWS": "arn:aws:iam::629470240201:user/john"
    },
    "Action": "sts:AssumeRole"
  }]
}
```

> **triangle-alert** Ensure the trust relationship is properly updated—otherwise, John will not be able to assume the role.

***

## Step 5: Assume the Role and Export Temporary Credentials

Have John run the following to get short-lived credentials:

```bash theme={null}
aws sts assume-role \
  --role-arn arn:aws:iam::629470240201:role/JohnUploadRole \
  --role-session-name JohnUploadSession
```

Sample response:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "ASIAFD2ZUTS3J3PIX55",
    "SecretAccessKey": "iqhGcv6Lp3Y4wUgmIiRiRHhS4KinLURta92SW5V",
    "SessionToken": "IQoJb3JpZ2luX2VjE/////////WwECAa...",
    "Expiration": "2023-10-08T21:53:20Z"
  }
}
```

Export these values to the environment:

```bash theme={null}
export AWS_ACCESS_KEY_ID="ASIAFD2ZUTS3J3PIX55"
export AWS_SECRET_ACCESS_KEY="iqhGcv6Lp3Y4wUgmIiRiRHhS4KinLURta92SW5V"
export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjE/////////WwECAa..."
```

***

## Step 6: Verify Upload Succeeds

With the new session credentials, repeat the list and upload:

```bash theme={null}
aws s3 ls s3://company1-hr
aws s3 cp new-file.txt s3://company1-hr
aws s3 ls s3://company1-hr
# 2023-10-08 17:45:42      7 Test.txt
# 2023-10-08 20:55:38      3 new-file.txt
```

The file `new-file.txt` is now uploaded. These permissions automatically expire when the session token’s `Expiration` time is reached.

***

## Links and References

* [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
* [AWS STS AssumeRole API](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
* [S3 Permissions Reference](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-with-s3-actions.html)
* [IAM Trust Policy Examples](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_iam-roles.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-iam/module/84a65700-7455-4ad8-aeb5-27dfaf07b8cc/lesson/3ad23a8c-1591-4d58-a9dd-537b91ed7adb)


# IAM Overview

Source: https://notes.kodekloud.com/docs/AWS-IAM/Introduction-to-AWS-Identity-and-Access-Management/IAM-Overview/page

Overview of AWS Identity and Access Management for managing permissions and access control in the AWS Cloud.

AWS Identity and Access Management (IAM) is the cornerstone of security and access control in the AWS Cloud. With IAM, you can centrally manage permissions, enforce the principle of least privilege, and govern how your users and applications authenticate and authorize with AWS services.

## What You’ll Learn

* **IAM Users**: Create dedicated accounts for individuals to access AWS via Management Console, CLI, or SDKs.
* **AWS CLI & SDKs**: Automate IAM operations and integrate AWS services into your applications.
* **IAM Groups**: Simplify permission management by grouping users and attaching policies.
* **IAM Roles**: Grant short-term permissions to AWS resources without storing long-term credentials.
* **Identity Policies**: Define JSON-based permissions and attach them to users, groups, or roles.
* **Resource-Based Policies**: Attach permissions directly to AWS resources (e.g., S3 buckets, SQS queues).
* **Session Policies**: Scope down permissions for a single session to enforce tighter control.
* **Permission Boundaries**: Limit the maximum permissions an IAM entity can acquire, enforcing least-privilege.

![The image is a slide titled "IAM Overview" with a list of topics related to Identity and Access Management, including IAM Users, AWS CLI and SDK, IAM Groups, IAM Roles, Identity Policy, Resource Based Policy, Session Policy, and Permission Boundary.](https://kodekloud.com/kk-media/image/upload/v1752863050/notes-assets/images/AWS-IAM-IAM-Overview/iam-overview-identity-access-management.jpg)

## Key IAM Components

| Component             | Description                                                         | Common Use Case                                          |
| --------------------- | ------------------------------------------------------------------- | -------------------------------------------------------- |
| IAM Users             | Long-term credentials for individual identity                       | Team members accessing the AWS Console or CLI            |
| IAM Groups            | Collections of users for bulk permission management                 | Granting developers access to specific AWS services      |
| IAM Roles             | Temporary credentials assumed by AWS services or federated users    | EC2 instances needing S3 read/write access               |
| Identity Policies     | JSON documents specifying “Allow” or “Deny” actions                 | Attaching S3-read policy to a developer group            |
| Resource Policies     | Permissions attached directly to AWS resources (bucket, queue, etc) | S3 bucket policy to allow CloudFront distribution        |
| Session Policies      | Inline policies passed in a role or user session                    | Limiting an API call to only a particular DynamoDB table |
| Permission Boundaries | Maximum permissions an IAM entity can obtain                        | Ensuring contractors cannot escalate privileges          |

> **lightbulb** Use permission boundaries to enforce least-privilege at scale. They act as an upper-limit guardrail, even if an identity has broader permissions via attached policies.

## Meet Sara: A Real-World Example

To illustrate how IAM works in practice, follow Sara, an AWS Solutions Architect, as she:

* Creates and manages AWS accounts
* Defines IAM users, groups, and roles
* Configures fine-grained access control
* Implements authentication and authorization flows
* Applies the principle of least privilege in every step
* Audits and monitors user access and policy changes

![The image outlines Sara's responsibilities, including managing AWS accounts, creating users and groups, access control management, authentication and authorization, and following the principle of least privilege.](https://kodekloud.com/kk-media/image/upload/v1752863051/notes-assets/images/AWS-IAM-IAM-Overview/sara-responsibilities-aws-access-control.jpg)

## Next Steps: AWS Account Setup

Now that you understand the IAM landscape, proceed with:

1. Configuring your AWS root user for MFA
2. Creating your first IAM user and group
3. Attaching managed policies to your group
4. Verifying permissions via AWS CLI

For detailed instructions, see [Managing IAM Users and Groups](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) and [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

***

## References

* [AWS Identity and Access Management Documentation](https://docs.aws.amazon.com/iam/)
* [AWS Security Best Practices](https://docs.aws.amazon.com/whitepapers/latest/security-best-practices/welcome.html)
* [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-iam/module/84a65700-7455-4ad8-aeb5-27dfaf07b8cc/lesson/c8cb14b8-947e-46e8-9301-1573e4170525)
