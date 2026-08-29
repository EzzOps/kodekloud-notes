# Create Bucket using AWS CLI

Source: https://notes.kodekloud.com/docs/Amazon-Simple-Storage-Service-Amazon-S3/AWS-S3-Core-Concepts/Create-Bucket-using-AWS-CLI/page

This guide covers essential Amazon S3 operations using AWS CLI for managing buckets and automating workflows.

In this guide, we'll explore essential Amazon S3 operations—listing, creating, deleting buckets, and managing objects—using the AWS CLI. Automate your workflows and integrate these commands into scripts for seamless infrastructure management.

## Prerequisites

* AWS CLI installed and configured (`aws configure`)
* IAM permissions to list, create, and delete S3 buckets and objects
* Unique bucket names (globally unique across AWS)

<Callout icon="lightbulb">
  Before creating a bucket, verify the name’s availability. Bucket names must be globally unique and compliant with DNS naming conventions.
</Callout>

## Quick Reference: Common S3 CLI Commands

| Operation        | Command                                       | Description                                  |
| ---------------- | --------------------------------------------- | -------------------------------------------- |
| List Buckets     | `aws s3 ls`                                   | Display all S3 buckets in the account        |
| Create Bucket    | `aws s3 mb s3://<bucket-name> --region ...`   | Make a new bucket in a specified region      |
| Delete Bucket    | `aws s3 rb s3://<bucket-name> [--force]`      | Remove an empty bucket or delete recursively |
| List Objects     | `aws s3 ls s3://<bucket>`                     | Show top-level objects and prefixes          |
| Copy Files/Dirs  | `aws s3 cp <src> <dest> [--recursive]`        | Copy files between local and S3              |
| Move Files/Dirs  | `aws s3 mv <src> <dest> [--recursive]`        | Move files between local and S3              |
| Sync Directories | `aws s3 sync <local> s3://<bucket>`           | Sync only new or changed files               |
| Delete Objects   | `aws s3 rm s3://<bucket>/<key> [--recursive]` | Remove objects or entire prefixes            |

***

## 1. Listing S3 Buckets

Retrieve all buckets in your AWS account:

```bash theme={null}
$ aws s3 ls
2023-03-29 00:51:27 bucket1
2023-03-28 02:22:48 bucket2
2023-03-28 02:20:43 bucket3
```

***

## 2. Creating a New Bucket

Use the **make bucket** command and specify a region:

```bash theme={null}
$ aws s3 mb s3://newbucket --region us-east-1
make_bucket: newbucket
```

***

## 3. Deleting a Bucket

Remove an **empty** bucket:

```bash theme={null}
$ aws s3 rb s3://newbucket
remove_bucket: newbucket
```

To delete a bucket and all its contents, add `--force`:

```bash theme={null}
$ aws s3 rb s3://newbucket --force
remove_bucket: newbucket
```

<Callout icon="triangle-alert">
  Using `--force` is irreversible. All objects in the bucket will be permanently deleted.
</Callout>

***

## 4. Listing Objects Inside a Bucket

### 4.1 Top-Level Listing

List prefixes (folders) and files at the root of the bucket:

```bash theme={null}
$ aws s3 ls s3://newbucket
                           PRE logs/
                           PRE media/
2023-03-29 01:38:08          0 file1.txt
2023-03-29 01:38:09          0 file2.txt
```

### 4.2 Recursive Listing

Show every object under the bucket:

```bash theme={null}
$ aws s3 ls s3://newbucket --recursive
2023-03-29 01:38:08          0 file1.txt
2023-03-29 01:38:09          0 file2.txt
2023-03-29 01:38:09          0 logs/log1
2023-03-29 01:38:09          0 logs/log2
2023-03-29 01:38:10      24599 media/images/image1.png
2023-03-29 01:38:10      21420 media/images/image2.png
```

***

## 5. Copying Files

### 5.1 Local → S3

Upload a file without deleting the source:

```bash theme={null}
$ aws s3 cp file1.txt s3://newbucket
upload: ./file1.txt to s3://newbucket/file1.txt
```

### 5.2 S3 → Local

Download an object to a local directory:

```bash theme={null}
$ aws s3 cp s3://newbucket/file1.txt /tmp/
download: s3://newbucket/file1.txt to ./tmp/file1.txt
```

### 5.3 S3 → S3

Copy between two buckets:

```bash theme={null}
$ aws s3 cp s3://bucket1/file1.txt s3://bucket2/
copy: s3://bucket1/file1.txt to s3://bucket2/file1.txt
```

***

## 6. Deleting Objects

### 6.1 Single Object

```bash theme={null}
$ aws s3 rm s3://bucket/404.html
delete: s3://bucket/404.html
```

### 6.2 Multiple Objects (Recursive)

```bash theme={null}
$ aws s3 rm s3://bucket/logs/ --recursive
delete: s3://bucket/logs/log1
delete: s3://bucket/logs/log2
```

***

## 7. Directory Operations

Most S3 CLI commands support `--recursive` to process all files under a directory or prefix.

### 7.1 Copy an Entire Directory

```bash theme={null}
$ aws s3 cp media/ s3://newbucket --recursive
```

### 7.2 Move Files and Directories

Use `mv` to transfer and remove the source:

```bash theme={null}
