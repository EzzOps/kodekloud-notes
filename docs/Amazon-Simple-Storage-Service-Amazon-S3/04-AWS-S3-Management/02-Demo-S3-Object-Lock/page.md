# As user2
[cloudshell-user@ip-... ~]$ aws s3 ls s3://kk-accesspoint/
fatal error: An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
[cloudshell-user@ip-... ~]$ aws s3 cp s3://kk-accesspoint/beach.jpg .
fatal error: An error occurred (403) when calling the HeadObject operation: Forbidden

# As user3
[cloudshell-user@ip-... ~]$ aws s3 ls s3://kk-accesspoint/
fatal error: An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
[cloudshell-user@ip-... ~]$ aws s3 cp s3://kk-accesspoint/beach.jpg .
fatal error: An error occurred (403) when calling the HeadObject operation: Forbidden
```

***

## 3. Create Access Points

Navigate to Amazon S3 → **Access points** and create two points:

1. **developers** (for user2)
2. **finance** (for user3)

Select **kk-accesspoint** as the data source, choose **Internet** for Network origin, and keep public access blocking enabled.

![The image shows an AWS S3 console interface for creating an access point, with fields for access point name, bucket selection, and network origin settings.](https://kodekloud.com/kk-media/image/upload/v1752869374/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-s3-access-point-creation-interface.jpg)

![The image shows an AWS S3 Access Point configuration screen, where settings for bucket selection, AWS region, network origin, and public access blocking are being configured.](https://kodekloud.com/kk-media/image/upload/v1752869375/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-s3-access-point-configuration.jpg)

> **triangle-alert** Always keep **Block all public access** enabled on buckets and access points to prevent accidental exposure.

***

## 4. Delegate Bucket Permissions to Access Points

To let your access points list bucket contents, add this bucket policy. Replace `123456789012` with your AWS account ID:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::kk-accesspoint",
      "Condition": {
        "StringEquals": {
          "s3:DataAccessPointAccount": "123456789012"
        }
      }
    }
  ]
}
```

Apply under **Bucket → Permissions → Bucket policy**:

![The image shows an Amazon S3 console screen with the "Permissions" tab open for a bucket named "kk-access-point." It displays settings related to blocking public access and bucket policies.](https://kodekloud.com/kk-media/image/upload/v1752869377/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/amazon-s3-console-permissions-kk-access-point.jpg)

***

## 5. Define Access Point Policies

### 5.1 Developer Access Point Policy

Go to **Access points → developers → Permissions → Edit** and paste:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/user2"
      },
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:us-east-1:123456789012:accesspoint/developers",
        "arn:aws:s3:us-east-1:123456789012:accesspoint/developers/object/*"
      ]
    }
  ]
}
```

![The image shows an AWS management console screen for editing an S3 Access Point policy, indicating that public access is blocked due to current settings. There are options to check and learn more about public access settings.](https://kodekloud.com/kk-media/image/upload/v1752869378/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-s3-access-point-policy-settings.jpg)

### 5.2 Finance Access Point Policy

For **finance**, allow user3:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/user3"
      },
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:us-east-1:123456789012:accesspoint/finance",
        "arn:aws:s3:us-east-1:123456789012:accesspoint/finance/object/*"
      ]
    }
  ]
}
```

After saving, review each access point’s overview:

![The image shows an Amazon S3 Access Point overview page, displaying details such as bucket name, account ID, AWS region, creation date, and network origin.](https://kodekloud.com/kk-media/image/upload/v1752869378/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/amazon-s3-access-point-overview.jpg)

***

### Access Point Summary

| Access Point | Principal                              | Actions                    |
| ------------ | -------------------------------------- | -------------------------- |
| developers   | `arn:aws:iam::123456789012:user/user2` | List, GetObject, PutObject |
| finance      | `arn:aws:iam::123456789012:user/user3` | List, GetObject, PutObject |

***

## 6. Test Access via Access Points

### 6.1 Developer (user2)

In AWS CloudShell as **user2**, list and copy via the developers access point ARN:

```bash theme={null}
# List via developers access point
[cloudshell-user@... ~]$ aws s3 ls s3://arn:aws:s3:us-east-1:123456789012:accesspoint/developers
2023-09-04 07:39:25    2879314 beach.jpg

# Download the object
[cloudshell-user@... ~]$ aws s3 cp s3://arn:aws:s3:us-east-1:123456789012:accesspoint/developers/beach.jpg .
```

### 6.2 Finance (user3)

As **user3**, perform the same steps and upload a new file:

```bash theme={null}
# List via finance access point
[cloudshell-user@... ~]$ aws s3 ls s3://arn:aws:s3:us-east-1:123456789012:accesspoint/finance
2023-09-04 07:39:25    2879314 beach.jpg

# Download the object
[cloudshell-user@... ~]$ aws s3 cp s3://arn:aws:s3:us-east-1:123456789012:accesspoint/finance/beach.jpg .

# Upload a test file
[cloudshell-user@... ~]$ touch test1
[cloudshell-user@... ~]$ aws s3 cp test1 s3://arn:aws:s3:us-east-1:123456789012:accesspoint/finance/test1

# Verify both files
[cloudshell-user@... ~]$ aws s3 ls s3://arn:aws:s3:us-east-1:123456789012:accesspoint/finance
2023-09-04 07:39:25    2879314 beach.jpg
2023-09-04 07:40:10         0 test1
```

***

## 7. Final Permissions Overview

Inspect the finance access point’s permissions tab:

![The image shows an AWS S3 Access Point settings page, specifically the "Permissions" tab for an access point named "finance," with options to block public access enabled.](https://kodekloud.com/kk-media/image/upload/v1752869379/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-s3-access-point-permissions-finance.jpg)

***

## 8. Conclusion

By leveraging S3 Access Points, you can:

* Delegate access control to distinct teams without modifying the main bucket policy.
* Create isolated entry points with tailored permissions.
* Simplify management when multiple user groups share a bucket.

This approach improves security posture and operational efficiency in multi-team environments.

***

## 9. Links and References

* [Amazon S3 Access Points Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html)
* [AWS CloudShell User Guide](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html)
* [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/985e08bc-a007-4d29-9e60-fe90b52410ae/lesson/9c50bd18-eb1f-4ba9-a66a-a04d05ec0ace)


# Demo S3 Object Lock

Source: https://notes.kodekloud.com/docs/Amazon-Simple-Storage-Service-Amazon-S3/AWS-S3-Management/Demo-S3-Object-Lock/page

Learn to enable and enforce Object Lock on Amazon S3 buckets, apply retention modes, and verify access restrictions using IAM policies.

Learn how to enable and enforce Object Lock on Amazon S3 buckets, apply governance and compliance retention modes, and verify access restrictions using IAM policies.

## Table of Contents

1. [What You’ll Learn](#what-youll-learn)
2. [1. Create an S3 Bucket with Object Lock](#1-create-an-s3-bucket-with-object-lock)
3. [2. Upload an Object](#2-upload-an-object)
4. [3. Configure Object Lock Retention](#3-configure-object-lock-retention)
5. [4. Test Deletion with a Restricted IAM User](#4-test-deletion-with-a-restricted-iam-user)
6. [5. Delete with an Admin User](#5-delete-with-an-admin-user)
7. [6. Demonstrate Object Legal Hold](#6-demonstrate-object-legal-hold)
8. [7. Deny Legal Hold Removal](#7-deny-legal-hold-removal)
9. [Summary](#summary)
10. [References](#references)

***

## What You’ll Learn

* How to enable Object Lock on an S3 bucket
* The difference between Governance and Compliance retention modes
* Applying and testing IAM policies that enforce or bypass retention settings
* Using Object Legal Hold for indefinite protection

***

## 1. Create an S3 Bucket with Object Lock

1. In the AWS S3 console, click **Create bucket**.
2. Under **Advanced settings**, check **Enable Object Lock**.

![The image shows an AWS S3 bucket configuration page with options for default encryption and advanced settings, including Object Lock.](https://kodekloud.com/kk-media/image/upload/v1752869380/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-S3-Object-Lock/aws-s3-bucket-configuration-page.jpg)

> **lightbulb** Object Lock requires versioning. When you enable Object Lock, S3 automatically enables versioning for the bucket (the Versioning option is grayed out).

***

## 2. Upload an Object

Upload a test file, for example `file1.txt`, to your new bucket:

1. Click **Upload**.
2. Select `file1.txt`.
3. Confirm and upload.

![The image shows an AWS S3 Management Console screen where a file named "file1.txt" is being prepared for upload to a bucket named "kk-objectclock-demo." The file is 7.0 bytes in size and is of type "text/plain."](https://kodekloud.com/kk-media/image/upload/v1752869381/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-S3-Object-Lock/aws-s3-console-file-upload-kk-objectclock.jpg)

After upload, open the object’s **Properties** to configure Object Lock.

***

## 3. Configure Object Lock Retention

In the object’s **Object Lock** section you can choose:

* **Legal Hold**: Indefinite hold without a retention date.
* **Retention Mode**: Specify Governance or Compliance mode and a retention date.

| Retention Mode  | Bypass Permission Required     | Use Case                          |
| --------------- | ------------------------------ | --------------------------------- |
| Governance Mode | `s3:BypassGovernanceRetention` | Temporary holds with exception    |
| Compliance Mode | Not bypassable                 | Regulatory or compliance mandates |

![The image shows an Amazon S3 interface for editing object lock retention settings, with options for retention mode and a warning about governance mode. A specified object, "file1.txt," is listed below with details.](https://kodekloud.com/kk-media/image/upload/v1752869382/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-S3-Object-Lock/amazon-s3-object-lock-settings-file1.jpg)

1. Select **Governance** mode.
2. Set the retention date (e.g., tomorrow).
3. Click **Save**.

> **triangle-alert** In Compliance mode, objects cannot be deleted or overwritten until the retention period expires.

***

## 4. Test Deletion with a Restricted IAM User

Switch to **User Two**, who has a policy denying `s3:BypassGovernanceRetention`. They have full S3 access but cannot bypass governance locks:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyBypassGovernanceRetention",
      "Effect": "Deny",
      "Action": "s3:BypassGovernanceRetention",
      "Resource": "*"
    }
  ]
}
```

When User Two tries to delete the locked object version, the request fails:

![The image shows an AWS S3 console screen with a "Failed to delete objects" error message, indicating an object could not be deleted due to access denial.](https://kodekloud.com/kk-media/image/upload/v1752869383/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-S3-Object-Lock/aws-s3-failed-delete-objects-error.jpg)

User Two also cannot modify retention settings.

***

## 5. Delete with an Admin User

Switch back to **User One** (Administrator) with full permissions, including `s3:BypassGovernanceRetention`:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

User One can now permanently delete the locked object version.

***

## 6. Demonstrate Object Legal Hold

1. Upload a second file, e.g., `file2.txt`.
2. Open its **Properties** and scroll to **Object Lock**.
3. Enable **Legal Hold**, then **Save**.

![The image shows an Amazon S3 console interface displaying details of an object, including the owner, AWS region, last modified date, size, and object URL.](https://kodekloud.com/kk-media/image/upload/v1752869384/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-S3-Object-Lock/amazon-s3-console-file1-details.jpg)

The object is now held indefinitely under Legal Hold.

***

## 7. Deny Legal Hold Removal

Update **User Two**’s policy to also deny `s3:PutObjectLegalHold`, preventing removal of legal holds:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyLegalHoldAndBypass",
      "Effect": "Deny",
      "Action": [
        "s3:PutObjectLegalHold",
        "s3:BypassGovernanceRetention"
      ],
      "Resource": "*"
    }
  ]
}
```

Now, when User Two tries to disable the legal hold, they see a permission error:

![The image shows an AWS S3 console screen where a user is attempting to edit an Object Lock legal hold but receives a permission error message.](https://kodekloud.com/kk-media/image/upload/v1752869385/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-S3-Object-Lock/aws-s3-console-object-lock-error.jpg)

Only users with the correct permissions (e.g., User One) can remove a legal hold.

***

## Summary

In this lesson, you’ve learned to:

* Enable Object Lock on an S3 bucket
* Apply Governance and Compliance retention modes
* Test deletion restrictions with IAM policies
* Use Object Legal Hold for indefinite protection

***

## References

* [AWS S3 Object Lock Documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html)
* [IAM JSON Policy Reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html)
* [Amazon S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/dev/Versioning.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/985e08bc-a007-4d29-9e60-fe90b52410ae/lesson/cfd3e010-0bcb-4d83-aad1-24c5b426cb78)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/985e08bc-a007-4d29-9e60-fe90b52410ae/lesson/ba19ff43-cdc2-4c39-9fbe-9fcfd739467e)
