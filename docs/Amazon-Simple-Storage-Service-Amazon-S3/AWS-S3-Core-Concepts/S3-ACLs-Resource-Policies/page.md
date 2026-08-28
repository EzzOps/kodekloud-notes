# → An error occurred (AccessDenied)
```

Back in **Blue**, append:

```json theme={null}
{
  "Sid": "AllowAccount2UserAdmin",
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::<SECOND_ACCOUNT_ID>:user/admin"
  },
  "Action": [
    "s3:ListBucket",
    "s3:GetObject"
  ],
  "Resource": [
    "arn:aws:s3:::kk-resource-policies",
    "arn:aws:s3:::kk-resource-policies/logs/*"
  ]
}
```

Save and retry in **Yellow**:

```bash theme={null}
aws s3 ls s3://kk-resource-policies
aws s3 rm s3://kk-resource-policies/file1.txt
aws s3 rm s3://kk-resource-policies/logs/log1
# delete: s3://kk-resource-policies/logs/log1
```

***

## Summary

You’ve now configured a private S3 bucket and applied these resource policy patterns:

| Scenario                  | Principal                       | Actions                           | Resource                        |
| ------------------------- | ------------------------------- | --------------------------------- | ------------------------------- |
| Read-only for User 2      | `arn:aws:iam::Acct1:user/user2` | `s3:GetObject`                    | `kk-resource-policies/logs/*`   |
| Delete for User 2         | `arn:aws:iam::Acct1:user/user2` | `s3:DeleteObject`                 | `kk-resource-policies/traces/*` |
| Combined read & delete    | Same as above                   | `s3:GetObject`, `s3:DeleteObject` | `kk-resource-policies/logs/*`   |
| Public read on media/     | `*`                             | `s3:GetObject`                    | `kk-resource-policies/media/*`  |
| Cross-account list & read | `arn:aws:iam::Acct2:user/admin` | `s3:ListBucket`, `s3:GetObject`   | Bucket & `logs/*`               |

With these techniques—granular read, delete, public, and cross-account—you can enforce precise access control over your S3 data.

***

## Links and References

* [AWS S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-iam-policies.html)
* [AWS IAM JSON Policy Elements](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html)
* [AWS Security Best Practices for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/eec05698-c022-44e4-9421-cf157eb32097/lesson/1048de03-7dc7-4beb-8248-f0a6bd8113d2" />
</CardGroup>


# S3 ACLs Resource Policies

Source: https://notes.kodekloud.com/docs/Amazon-Simple-Storage-Service-Amazon-S3/AWS-S3-Core-Concepts/S3-ACLs-Resource-Policies/page

This article explains Amazon S3 access control using ACLs and resource policies for managing permissions effectively.

In this article, we’ll clarify how Amazon S3 secures your buckets by default, then dive deep into **resource policies** (bucket policies) and **ACLs**. You’ll learn how to grant, restrict, and block access—step by step.

## Understanding Default S3 Bucket Permissions

When you create a new S3 bucket:

* Only the **bucket creator** (and the AWS root user) has access.
* No other IAM users—even in your own account—can access it.
* Public or anonymous users are explicitly denied until you grant permission.

<Frame>
  ![The image illustrates S3 access permissions for different types of AWS users, showing that the creator and root user have access, while other AWS users, users from another AWS account, and anonymous/public users do not.](https://kodekloud.com/kk-media/image/upload/v1752869315/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-ACLs-Resource-Policies/s3-access-permissions-aws-users-illustration.jpg)
</Frame>

## Resource Policies (Bucket Policies)

A **resource policy** is a JSON document attached directly to an AWS resource. For S3, this is called a **bucket policy**. It specifies:

* **Principals**: Who can access
* **Effect**: Allow or Deny
* **Actions**: S3 operations
* **Resources**: Which buckets or objects
* **Conditions** (optional): Additional restrictions

<Frame>
  ![The image explains the difference between a Resource Policy and an S3 Bucket Policy, highlighting their roles in determining access and operations for S3 resources.](https://kodekloud.com/kk-media/image/upload/v1752869316/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-ACLs-Resource-Policies/resource-policy-vs-s3-bucket-policy.jpg)
</Frame>

### Anatomy of a Bucket Policy

Below is a minimal bucket policy. Use this as a template:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRule",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:user/JohnDoe"
      },
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::DOC-EXAMPLE-BUCKET/*"]
    }
  ]
}
```

| Field     | Description                                                                                 |
| --------- | ------------------------------------------------------------------------------------------- |
| Version   | Policy language version (use `2012-10-17` unless updated by AWS).                           |
| Sid       | Statement identifier (optional).                                                            |
| Principal | AWS account, user, role, or `*` (everyone).                                                 |
| Effect    | `Allow` or `Deny`.                                                                          |
| Action    | S3 operations, e.g., `s3:GetObject`, `s3:ListBucket`, or `s3:*`.                            |
| Resource  | ARN of bucket or objects, e.g., `arn:aws:s3:::bucket-name` or `arn:aws:s3:::bucket-name/*`. |

<Callout icon="lightbulb">
  Always specify the least-privilege permissions. Start by allowing only the actions and resources that are strictly required.
</Callout>

## Multiple Statements

You can combine statements in one policy. For example, allow everyone to read objects but deny one user:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAll",
      "Principal": "*",
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::DOC-EXAMPLE-BUCKET/*"]
    },
    {
      "Sid": "DenyDaisy",
      "Principal": {
        "AWS": "arn:aws:iam::666438:user/DaisyM"
      },
      "Effect": "Deny",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::DOC-EXAMPLE-BUCKET/*"]
    }
  ]
}
```

* A principal of `*` covers all AWS users and anonymous/public users.
* You may add as many statements as needed.

## Restricting by Prefix

To limit access to a specific “folder” (prefix):

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowDaisyMedia",
      "Principal": {
        "AWS": "arn:aws:iam::666438:user/DaisyM"
      },
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::DOC-EXAMPLE-BUCKET/media/*"]
    }
  ]
}
```

## Adding Conditions

You can enforce network or request constraints:

```json theme={null}
{
  "Id": "PolicyId2",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowFromIP",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::DOC-EXAMPLE-BUCKET",
        "arn:aws:s3:::DOC-EXAMPLE-BUCKET/*"
      ],
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": ["192.0.2.0/24"]
        }
      }
    }
  ]
}
```

## Granting Access to Multiple Folders

Use `StringEquals` on `s3:prefix` and `s3:delimiter`:

```json theme={null}
{
  "Id": "PolicyId3",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAudioVideo",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::DOC-EXAMPLE-BUCKET",
        "arn:aws:s3:::DOC-EXAMPLE-BUCKET/*"
      ],
      "Condition": {
        "StringEquals": {
          "s3:prefix": ["audio/", "video/"],
          "s3:delimiter": ["/"]
        }
      }
    }
  ]
}
```

## Block Public Access Settings

Even if a bucket policy uses `Principal: "*"`, AWS provides **Block Public Access** as a safety net. With these settings enabled, public policies are overridden until you disable them.

```json theme={null}
{
  "Sid": "AllowAll",
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": ["arn:aws:s3:::DOC-EXAMPLE-BUCKET1/*"]
}
```

<Frame>
  ![The image shows a list of options for blocking public access to AWS S3 buckets, alongside a diagram illustrating a secured bucket in "Account 2" with restricted access to anonymous or public users.](https://kodekloud.com/kk-media/image/upload/v1752869317/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-ACLs-Resource-Policies/aws-s3-bucket-access-blocking-diagram.jpg)
</Frame>

<Callout icon="triangle-alert">
  Disabling **Block Public Access** can expose your data to the internet. Confirm your policies and audit logs before making public.
</Callout>

## IAM Policies vs. Resource Policies

| Policy Type     | Attached To              | Scope                               | Can Include Public |
| --------------- | ------------------------ | ----------------------------------- | ------------------ |
| IAM Policy      | IAM user, group, or role | Authenticated AWS principals        | No                 |
| Resource Policy | S3 bucket (or other)     | Any principal (including anonymous) | Yes                |

Both must allow an action for access to succeed. A deny in either one blocks access.

<Frame>
  ![The image compares IAM Policy and Resource Policy, highlighting that IAM Policy is for authenticated AWS users, while Resource Policy can include rules for anonymous or public users.](https://kodekloud.com/kk-media/image/upload/v1752869318/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-ACLs-Resource-Policies/iam-policy-vs-resource-policy-comparison.jpg)
</Frame>

## ACLs (Legacy)

S3 ACLs predate IAM and offer only five permission sets:

| ACL Permission | Description                    |
| -------------- | ------------------------------ |
| READ           | Read objects                   |
| WRITE          | Write objects                  |
| READ\_ACP      | Read bucket ACL                |
| WRITE\_ACP     | Write bucket ACL               |
| FULL\_CONTROL  | Full control (all permissions) |

<Callout icon="lightbulb">
  AWS recommends using IAM policies and bucket policies instead of ACLs for fine-grained access control.
</Callout>

<Frame>
  ![The image is an informational graphic about S3 ACLs, describing them as a legacy access control mechanism with limited flexibility and a table detailing ACL permissions for buckets and objects.](https://kodekloud.com/kk-media/image/upload/v1752869319/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-ACLs-Resource-Policies/s3-acls-legacy-access-control-graphic.jpg)
</Frame>

***

By combining **IAM policies**, **bucket policies**, and **block public access** settings, you can lock down your S3 buckets and grant exactly the permissions your applications need.

## Links and References

* [Amazon S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
* [Amazon S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
* [AWS IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/eec05698-c022-44e4-9421-cf157eb32097/lesson/52028a56-456d-4c8f-acf0-222b8425e48c" />
</CardGroup>
