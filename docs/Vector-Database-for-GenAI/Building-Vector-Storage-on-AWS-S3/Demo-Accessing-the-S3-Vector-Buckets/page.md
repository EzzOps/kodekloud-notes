# Demo Accessing the S3 Vector Buckets

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Building-Vector-Storage-on-AWS-S3/Demo-Accessing-the-S3-Vector-Buckets/page

Guide to accessing and managing AWS S3 Vector Buckets with Python Boto3, including creating clients, listing vector buckets and indexes and common s3vectors operations

Welcome back. In this lesson you'll learn how to programmatically access S3 Vector Buckets from a Jupyter notebook using Python and Boto3. This builds on prior work creating an IAM policy and attaching it to a user — those permissions are required to query vector buckets and indexes.

What you'll accomplish

* Create a Boto3 session / client for the `s3vectors` service.
* List available vector buckets.
* List indexes inside a specific vector bucket.

S3 Vector Buckets use a dedicated Boto3 client, typically exposed as `s3vectors`. This client provides methods such as `list_vector_buckets`, `list_indexes`, `get_vectors`, `create_index`, and `create_vector_bucket` (among others).

<Callout icon="lightbulb">
  Do not hardcode production credentials in notebooks. Prefer environment variables, an AWS credentials file, or an IAM role (if running on AWS compute). Never commit secrets to source control.
</Callout>

## Prerequisites

* Python 3.8+ installed
* Boto3 installed in your environment: `pip install boto3`
* A user or role with permissions to call S3 Vector Bucket APIs
* Target vector bucket and index names you want to inspect

Helpful references:

* Boto3 s3vectors API: [https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors.html](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors.html)
* AWS credentials and configuration: [https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

## Step 1 — Import and configure

Import the required libraries and set your credentials and target names. Replace placeholders with your own values or, better, load them from environment variables or a credentials file.

```python theme={null}
import boto3
import json
import os
