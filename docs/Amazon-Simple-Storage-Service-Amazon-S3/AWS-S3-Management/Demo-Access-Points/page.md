# Demo Access Points

Source: https://notes.kodekloud.com/docs/Amazon-Simple-Storage-Service-Amazon-S3/AWS-S3-Management/Demo-Access-Points/page

This tutorial explains how to use Amazon S3 Access Points for access control delegation and isolation for different teams.

In this tutorial, you’ll learn how to use Amazon S3 Access Points to delegate and isolate access control for different teams. By the end, you will have configured two access points—one for developers and one for finance—each with its own fine-grained policy.

***

## Table of Contents

1. [Create a Demo Bucket](#1-create-a-demo-bucket)
2. [Verify Default Access for Other Users](#2-verify-default-access-for-other-users)
3. [Create Access Points](#3-create-access-points)
4. [Delegate Bucket Permissions to Access Points](#4-delegate-bucket-permissions-to-access-points)
5. [Define Access Point Policies](#5-define-access-point-policies)
   * [5.1 Developer Access Point Policy](#51-developer-access-point-policy)
   * [5.2 Finance Access Point Policy](#52-finance-access-point-policy)
6. [Test Access via Access Points](#6-test-access-via-access-points)
   * [6.1 Developer (user2)](#61-developer-user2)
   * [6.2 Finance (user3)](#62-finance-user3)
7. [Final Permissions Overview](#7-final-permissions-overview)
8. [Conclusion](#8-conclusion)
9. [Links and References](#9-links-and-references)

***

## 1. Create a Demo Bucket

First, set up a new S3 bucket named `kk-accesspoint` with the default settings. Then upload a sample file (`beach.jpg`) for testing.

<Frame>
  ![The image shows an AWS S3 console screen where a user is configuring settings for a new bucket, including versioning, tags, and default encryption options. The "Create bucket" button is highlighted at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752869367/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-s3-console-create-bucket-settings.jpg)
</Frame>

Upload your test asset:

<Frame>
  ![The image shows an AWS S3 upload interface where a file named "beach.jpg" is being prepared for upload. The file is 2.7 MB in size, and the "Upload" button is highlighted.](https://kodekloud.com/kk-media/image/upload/v1752869368/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-s3-upload-beach-file-interface.jpg)
</Frame>

Once uploaded, as the bucket owner (user1), you can view the object details:

<Frame>
  ![The image shows an Amazon S3 console page displaying details of an object named "beach.jpg," including its properties, S3 URI, and object URL. It also indicates that bucket versioning is disabled.](https://kodekloud.com/kk-media/image/upload/v1752869369/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/amazon-s3-console-beachjpg-properties.jpg)
</Frame>

<Callout icon="lightbulb">
  Consider enabling versioning and default encryption on production buckets to protect against accidental data loss or unauthorized access.
</Callout>

***

## 2. Verify Default Access for Other Users

Assume two IAM users—**user2** and **user3**—each have only CloudShell access. By default, neither can list or retrieve objects from your new bucket.

<Frame>
  ![The image shows the AWS Identity and Access Management (IAM) console, displaying a list of users with details such as last activity, password age, and active key age.](https://kodekloud.com/kk-media/image/upload/v1752869370/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-iam-console-user-details.jpg)
</Frame>

<Frame>
  ![The image shows an AWS Identity and Access Management (IAM) console screen, displaying user permissions with the "AWSCloudShellFullAccess" policy attached. The console access is enabled without MFA, and no permissions boundary is set.](https://kodekloud.com/kk-media/image/upload/v1752869372/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-iam-console-user-permissions-policy.jpg)
</Frame>

In AWS CloudShell, both users attempt to list and copy objects:

<Frame>
  ![The image shows the AWS Management Console with a search for "CloudShell," displaying services, resources, blogs, and documentation related to AWS CloudShell. The interface is dark-themed, and there are multiple tabs open in the browser.](https://kodekloud.com/kk-media/image/upload/v1752869373/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Demo-Access-Points/aws-management-console-cloudshell-search-dark-theme.jpg)
</Frame>

```bash theme={null}
