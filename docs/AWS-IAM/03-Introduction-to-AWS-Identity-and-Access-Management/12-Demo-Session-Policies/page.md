# Demo Session Policies

Source: https://notes.kodekloud.com/docs/AWS-IAM/Introduction-to-AWS-Identity-and-Access-Management/Demo-Session-Policies/page

This tutorial explains how to grant temporary S3 upload permissions to an IAM user using AWS STS session policies.

In this tutorial, you’ll grant the IAM user **John** temporary file-upload permissions to the S3 bucket `company1-hr` using an AWS STS session policy and a dedicated IAM role. By the end, John will be able to upload objects for a limited time without altering his long-term permissions.

## Prerequisites

* AWS CLI installed and configured for user **John**
* Bucket `company1-hr` already exists in account `629470240201`
* Basic familiarity with IAM, STS, and S3 permissions

***

## Step 1: Verify Current AWS Identity

Confirm you’re authenticated as **John**:

```bash theme={null}
aws sts get-caller-identity
```

Expected output:

```json theme={null}
{
  "UserId": "AIDAZFDZUTSTSYQ6QFLS",
  "Account": "629470240201",
  "Arn": "arn:aws:iam::629470240201:user/john"
}
```

***

## Step 2: List Bucket Contents and Test Upload

Check existing objects and verify that upload is currently denied:

```bash theme={null}
aws s3 ls s3://company1-hr
aws s3 cp new-file.txt s3://company1-hr
