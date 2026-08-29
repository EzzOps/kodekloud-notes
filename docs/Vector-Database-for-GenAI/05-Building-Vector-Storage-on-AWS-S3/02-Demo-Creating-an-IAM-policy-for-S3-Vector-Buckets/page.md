# Example: prefer environment variables or ~/.aws/credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "REPLACE_ME")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "REPLACE_ME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

BUCKET_NAME = "airline-policy-vectors-YOURNAME"
VECTOR_INDEX_NAME = "airline-policy-index"
```

## Step 2 — Create a Boto3 session and s3vectors client

Create a Boto3 session and then instantiate an `s3vectors` client. You can also call `boto3.client("s3vectors", ...)` directly if you prefer not to use a session.

```python theme={null}
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

client = session.client("s3vectors")
print("Connected to s3vectors in", AWS_REGION)
```

<Callout icon="warning">
  If you receive `AccessDenied` or `Unauthorized` errors, verify the IAM policy attached to your user/role includes the required s3vectors actions and the resource ARNs are in scope for your region and account.
</Callout>

## Step 3 — List vector buckets

Use `list_vector_buckets()` to retrieve the vector buckets accessible to the credentials in use. The API response keys may vary in capitalization across SDK versions, so handle common variants.

```python theme={null}
bucket_response = client.list_vector_buckets()

# Handle variations in response key capitalization
entries = (
    bucket_response.get("VectorBuckets")
    or bucket_response.get("vectorBuckets")
    or []
)

# Derive a list of bucket identifiers (try common fields)
bucket_names = [
    b.get("vectorBucketName") or b.get("name") or b.get("bucketName")
    for b in entries
    if isinstance(b, dict)
]

bucket_visible = BUCKET_NAME in bucket_names
print("Configured bucket visible:", bucket_visible)

if not bucket_visible:
    print("Double-check bucket name, region, and IAM scope.")
```

Common troubleshooting tips

* Ensure the region in your session matches where the vector bucket is located.
* Confirm the IAM policy permits `s3vectors:ListVectorBuckets` (and other needed actions).
* Verify the vector bucket name you configured is exact.

## Step 4 — List indexes within a vector bucket

A single S3 Vector Bucket may contain multiple indexes. Call `list_indexes()` with the target vector bucket name to get its indexes.

```python theme={null}
index_response = client.list_indexes(vectorBucketName=BUCKET_NAME)
index_entries = index_response.get("indexes") or []

# Extract index names (if present)
index_names = [x.get("indexName") for x in index_entries if x.get("indexName")]

print("Indexes found:", len(index_names))
print("Expected index visible:", VECTOR_INDEX_NAME in index_names)

# Show a small preview of the structured responses
preview = {
    "vectorBuckets": entries[:3],
    "indexes": index_entries[:3],
}
print(json.dumps(preview, indent=2, default=str))
```

This prints the number of indexes found for the specified vector bucket and a short preview of the returned objects. Use `get_vectors` and index-level calls once you confirm the index names.

## Common s3vectors operations

| Operation                               | Use case                                                       |
| --------------------------------------- | -------------------------------------------------------------- |
| `list_vector_buckets`                   | Enumerate S3 Vector Buckets visible to the current credentials |
| `list_indexes`                          | List all indexes inside a specific vector bucket               |
| `get_vectors`                           | Retrieve vectors (embedding results) from an index             |
| `create_vector_bucket`                  | Create a new S3 Vector Bucket for storing vectorized objects   |
| `create_index`                          | Build an index from content stored in a vector bucket          |
| `delete_vector_bucket` / `delete_index` | Remove resources when no longer needed                         |

For the full list of methods, parameter shapes, and response structures see the Boto3 s3vectors documentation:
[https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors.html](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors.html)

<Frame>
  <img alt="The image shows a section of the AWS Boto3 documentation page, listing available methods for managing S3 vectors, alongside navigation links on the left sidebar." />
</Frame>

You can also embed text or documents into a vector bucket and create an index from that content — that workflow will be covered in a follow-up tutorial.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/afa51fbf-32d5-4459-a9de-0a764b24682b/lesson/94f5393a-3890-4d8c-be70-da046f8489e1" />
</CardGroup>


# Demo Creating an IAM policy for S3 Vector Buckets

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Building-Vector-Storage-on-AWS-S3/Demo-Creating-an-IAM-policy-for-S3-Vector-Buckets/page

Guides creating and attaching a customer managed IAM policy granting least privilege S3 actions for programmatic access to vector buckets, including tagging, permissions, KMS considerations, and credential handling

Welcome. This lesson assumes you already have an S3 vector bucket. To allow programmatic access to that bucket, create a customer-managed IAM policy scoped to the vector bucket ARN(s) and attach it to the user or role your application uses. This lets you explicitly grant the exact S3 actions required for vector workflows (list, read, write, permission management, and tagging) while following least-privilege principles.

Overview

* Goal: Create a customer-managed IAM policy that permits programmatic listing, reading, writing, permission management, and tagging for S3 vector buckets, then attach it to a user.
* Pre-requisite: You have an existing S3 vector bucket (or buckets) and an IAM user or role to attach the policy to.

Step 1 — Create the customer-managed policy

1. In the AWS Console, search for and open **IAM**.
2. On the left menu, click **Policies**, then click **Create policy**.
3. In the policy editor:
   * If your account or organization provides an `S3 Vectors` policy template, search for `vectors` and select it.
   * If that template is not available, choose the **S3** service and manually select the actions your vector workflows require (examples below).
4. Fine-tune allowed actions depending on your needs:
   * Permit only listing, only read/write, or full control depending on the principle of least privilege.
   * For this demo, enable actions required for listing, reading, writing, permission management, and tagging so the user can list, read, write, and manage S3 vector buckets and objects.
5. Choose the resource scope:
   * Selecting `All` applies the policy to all S3 buckets. For least privilege, scope the policy to specific bucket ARNs such as `arn:aws:s3:::my-vector-bucket` and `arn:aws:s3:::my-vector-bucket/*`.
6. Click **Next**, give the policy a name (for example `S3-vector-bucket-demo`), then **Create policy**.

<Frame>
  <img alt="The image shows an AWS IAM policy creation page where various S3 Vectors actions like List, Read, Write, Permissions management, and Tagging are selected. There is also a notification indicating that some dependent permissions are not selected." />
</Frame>

Recommended S3 actions for vector bucket workflows

| Action group          | Example actions                              | Purpose                                                                                   |
| --------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Listing               | `s3:ListBucket`                              | List objects in a bucket or prefixes (required for enumerating data and shards).          |
| Read                  | `s3:GetObject`, `s3:GetObjectVersion`        | Read object content and versions for embedding or retrieval.                              |
| Write                 | `s3:PutObject`, `s3:PutObjectAcl`            | Upload new objects, store serialized embeddings or metadata, manage ACLs.                 |
| Permission management | `s3:PutBucketPolicy`, `s3:PutBucketAcl`      | Manage bucket-level policies and access controls if your app needs to change permissions. |
| Tagging & metadata    | `s3:PutObjectTagging`, `s3:GetObjectTagging` | Tag objects for lifecycle, labeling, or vector metadata.                                  |

Example minimal customer-managed IAM policy (adjust ARNs and actions for your environment)

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListBucket",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::your-vector-bucket-name"]
    },
    {
      "Sid": "AllowObjectsReadWriteAndTag",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:PutObjectTagging",
        "s3:GetObjectTagging"
      ],
      "Resource": ["arn:aws:s3:::your-vector-bucket-name/*"]
    }
  ]
}
```

Replace `your-vector-bucket-name` with your actual bucket name, or add multiple ARNs to scope to several buckets.

Step 2 — Attach the policy to a user (or role)

1. In IAM, go to **Users** and select the target user (for example `s3-vector`).
2. Click **Add permissions** → **Attach policies directly**.
3. Choose the **Customer managed** filter, search for `vector`, select the policy you created, click **Next**, then **Add permissions**.

<Frame>
  <img alt="The image shows an AWS Identity and Access Management (IAM) console displaying details for a user named &#x22;s3-vector,&#x22; including permissions policies and access keys. The user has AWS managed policies like &#x22;AmazonBedrockFullAccess&#x22; and &#x22;AmazonS3FullAccess&#x22; attached." />
</Frame>

Note about AWS-managed policies
Although this user may already have the AWS-managed `AmazonS3FullAccess` policy attached, creating and attaching a customer-managed policy for S3 vector buckets lets you explicitly grant the precise actions and resource scope required by your vector operations (for example scoping permissions to specific bucket ARNs or enabling tagging and permission-management actions). AWS-managed policies can be broader than necessary for your application.

<Callout icon="lightbulb">
  If you have multiple vector buckets or separate environments (dev/stage/prod), create separate policies per environment and scope ARNs accordingly. This makes auditing and rotation easier.
</Callout>

Dependent permissions and encryption
Depending on how your buckets are configured, you may need additional permissions beyond basic S3 actions:

* If objects are encrypted with a KMS key, include the appropriate KMS key permissions such as `kms:Encrypt`, `kms:Decrypt`, and `kms:GenerateDataKey` for the key used by the bucket or objects.
* Cross-account bucket access, bucket policies, or object lambda integrations may require extra permissions or trust relationships.

Generate and store programmatic credentials
If your application will access the S3 vector buckets from code, create programmatic access keys:

1. In the user’s **Security credentials** tab, generate an **Access key (access key ID and secret access key)**.
2. Store these keys securely — for example:
   * In an AWS Secrets Manager secret.
   * In an encrypted environment variable management solution.
   * In a CI/CD secret store.

<Callout icon="warning">
  Never commit access keys to source control. Store them securely (for example, in a secrets manager or environment variables) and rotate them regularly.
</Callout>

Quick checklist before testing access

* [ ] Policy created and scoped to correct bucket ARNs.
* [ ] Policy attached to the intended user or role.
* [ ] KMS key policy updated if bucket uses SSE-KMS.
* [ ] Access keys generated and stored securely.
* [ ] Application environment configured to use the keys or role.

References and further reading

* [IAM Policies and Permissions (AWS)](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
* [Amazon S3 Actions, Resources, and Condition Keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html)
* [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)

That completes this lesson. Use these credentials to programmatically access the S3 vector bucket, upload and embed data, and query your vector store.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/afa51fbf-32d5-4459-a9de-0a764b24682b/lesson/9191e7a7-9555-44f1-899e-9a15c16efe0e" />
</CardGroup>
