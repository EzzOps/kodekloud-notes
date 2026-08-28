# Importing Pulumi S3 bucket

Source: https://notes.kodekloud.com/docs/Pulumi-Essentials/Pulumi-Essentials/Importing-Pulumi-S3-bucket/page

This guide covers the process of defining, deploying, and managing an S3 bucket using Pulumi's Infrastructure as Code approach.

In this lesson, you'll learn how to create and manage an AWS S3 bucket using Pulumi's AWS library with Python. The example below demonstrates the basic structure of a Pulumi program that imports necessary libraries, creates an S3 bucket, and exports its identifier.

<Callout icon="lightbulb">
  This guide covers the process of defining, deploying, and managing an S3 bucket using Pulumi's Infrastructure as Code approach.
</Callout>

## Example: Creating an S3 Bucket with Pulumi

Below is the initial Python code that imports Pulumi alongside the AWS S3 library, creates an S3 bucket (named internally as "my-bucket"), and exports the bucket's ID:

```python theme={null}
"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3
