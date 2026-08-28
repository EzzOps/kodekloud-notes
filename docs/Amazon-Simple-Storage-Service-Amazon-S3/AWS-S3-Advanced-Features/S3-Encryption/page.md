# Example usage
url = create_presigned_get_url(
    bucket_name='my-video-bucket',
    object_key='videos/movie.mp4',
    expiration=600
)
print(url)
```

## Use Case: Direct Client Uploads

By default, clients upload files through your backend (EC2), which consumes bandwidth and CPU:

<Frame>
  ![The image illustrates a process involving pre-signed URLs in AWS Cloud, showing a user interacting with cloud services and storage. A note mentions that all files must traverse through back-end servers.](https://kodekloud.com/kk-media/image/upload/v1752869221/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Presigned-URLs/aws-cloud-presigned-urls-process-diagram.jpg)
</Frame>

With a pre-signed PUT URL, clients upload directly to S3:

```python theme={null}
import boto3
from botocore.exceptions import ClientError

def create_presigned_put_url(bucket_name, object_key, expiration=3600):
    s3 = boto3.client('s3')
    try:
        return s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
    except ClientError as e:
        print(f"Error generating PUT URL: {e}")
        return None

# Example usage
url = create_presigned_put_url(
    bucket_name='my-bucket',
    object_key='uploads/profile-pic.png',
    expiration=300
)
print(url)
```

<Callout icon="lightbulb">
  Bypassing your backend for large file uploads reduces latency and operational costs.
</Callout>

## Expiration and Permissions

Every pre-signed URL requires an expiration time. For IAM user credentials, the maximum is 7 days (604,800 seconds). Always choose the shortest practical duration.

<Frame>
  ![The image provides information about pre-signed URLs, noting that an expiration date is required, with a maximum duration of 7 days using an IAM user, and that a pre-signed URL can be generated even if an IAM user lacks access to an S3 bucket.](https://kodekloud.com/kk-media/image/upload/v1752869222/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Presigned-URLs/presigned-urls-expiration-iam-s3.jpg)
</Frame>

| Operation   | Required Permission | Max Expiration |
| ----------- | ------------------- | -------------- |
| get\_object | s3:GetObject        | 7 days         |
| put\_object | s3:PutObject        | 7 days         |

Even if an IAM user lacks direct access to the bucket, they can still generate a pre-signed URL. S3 will enforce the embedded permissions:

<Frame>
  ![The image illustrates the concept of pre-signed URLs, showing how an IAM user without direct access to an S3 bucket can use a pre-signed URL to gain temporary access.](https://kodekloud.com/kk-media/image/upload/v1752869223/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Presigned-URLs/pre-signed-urls-iam-user-access.jpg)
</Frame>

<Callout icon="triangle-alert">
  A pre-signed URL grants the specified action to anyone holding it. Never expose URLs in public repos or client-side code that can be easily inspected.
</Callout>

## References

* [Amazon S3 Pre-Signed URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)
* [Boto3 S3 Client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
* [AWS Security Best Practices](https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/90fd6d76-d0d4-481c-b267-b9247a005a6e/lesson/60e19d1d-0788-4a36-ac63-21ee0f7a2f70" />
</CardGroup>


# S3 Encryption

Source: https://notes.kodekloud.com/docs/Amazon-Simple-Storage-Service-Amazon-S3/AWS-S3-Advanced-Features/S3-Encryption/page

This article explores how Amazon S3 encrypts data, covering encryption types, methods, and practical code examples.

In this lesson we’ll explore how Amazon S3 encrypts your data. We’ll cover:

1. What is Encryption in S3?
2. Client-Side vs. Server-Side Encryption
3. Server-Side Encryption Methods (SSE-S3, SSE-KMS, SSE-C)
4. Per-Object Encryption and Bucket Defaults
5. Practical Code Examples for Each SSE Method

***

## What Is Encryption?

Encryption transforms readable data (plaintext) into unreadable ciphertext using cryptographic keys. Only holders of the correct key can decrypt the data. In Amazon S3, encryption happens at two layers:

* **In transit**: Secured by SSL/TLS between your client and S3.
* **At rest**: Data stored on AWS servers is encrypted on disk.

<Frame>
  ![The image illustrates two types of encryption: "In Transit" using SSL/TLS and "Encryption at Rest" related to S3, with icons representing a user, a storage bucket, and a server.](https://kodekloud.com/kk-media/image/upload/v1752869224/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-Encryption/encryption-in-transit-at-rest-diagram.jpg)
</Frame>

* **In transit**: Automatic over HTTPS (SSL/TLS).
* **At rest**: Must be enabled so S3 stores your objects encrypted on disk.

***

## Client-Side vs. Server-Side Encryption

* **Client-Side Encryption**: You generate, manage, and store keys. You encrypt data locally, then upload only ciphertext to S3.
* **Server-Side Encryption**: You send plaintext over HTTPS; AWS encrypts it at rest using the method you choose.

<Frame>
  ![The image illustrates the differences between client-side and server-side encryption, showing data flow from a user to a server with encryption occurring either before or after data reaches the server.](https://kodekloud.com/kk-media/image/upload/v1752869226/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-Encryption/client-server-encryption-data-flow-diagram.jpg)
</Frame>

S3 supports three server-side methods:

<Frame>
  ![The image lists three server-side encryption methods: Amazon S3-Managed Keys (SSE-S3), Customer-Provided Keys (SSE-C), and Key Management Service Keys (SSE-KMS).](https://kodekloud.com/kk-media/image/upload/v1752869227/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-Encryption/server-side-encryption-methods-sse-s3-sse-c-sse-kms.jpg)
</Frame>

***

## Per-Object Encryption and Bucket Defaults

* Encryption is configured **per object**.
* You can set a **default encryption** on the bucket so that any upload without explicit encryption uses the bucket’s setting.
* You can still override the default on a per-object basis.

<Frame>
  ![The image is a note about encryption, explaining that it occurs on a per-object basis and a default encryption method can be configured on a bucket.](https://kodekloud.com/kk-media/image/upload/v1752869228/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-Encryption/encryption-per-object-bucket-configure.jpg)
</Frame>

<Callout icon="lightbulb">
  When you enable default encryption on a bucket, uploads without specified encryption inherit the bucket’s default settings.
</Callout>

***

## SSE-S3 (Server-Side Encryption with Amazon S3-Managed Keys)

With SSE-S3, AWS handles all key management using AES-256:

* Key generation & management: AWS
* Encryption algorithm: AES-256
* Responsibilities: AWS S3

**Encryption Flow**

1. AWS maintains a master root key (opaque to you).
2. For each object, S3 generates a unique data key.
3. The object is encrypted with the data key (AES-256).
4. The data key is encrypted with the root key.
5. Both encrypted object and encrypted data key are stored.

<Frame>
  ![The image illustrates SSE-S3 encryption in AWS, showing the use of a root key and AES-256 algorithm for encrypting objects uniquely per item in a storage bucket.](https://kodekloud.com/kk-media/image/upload/v1752869229/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-Encryption/sse-s3-encryption-aws-aes256.jpg)
</Frame>

**Decryption Flow**

1. S3 decrypts the data key using the root key.
2. S3 decrypts your object with the data key.
3. Plaintext is returned to you.

<Frame>
  ![The image illustrates the process of SSE-S3 decryption in AWS, showing a flow from a user to an S3 bucket and then to a server, with a focus on the use of a root key for decryption.](https://kodekloud.com/kk-media/image/upload/v1752869230/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-Encryption/sse-s3-decryption-aws-flow-diagram.jpg)
</Frame>

**AWS CLI Example**

```bash theme={null}
aws s3 cp file.txt s3://my-bucket/ --sse AES256
```

***

## SSE-KMS (Server-Side Encryption with AWS KMS Keys)

SSE-KMS integrates AWS Key Management Service for advanced control:

* Key management: AWS KMS
* Encryption/decryption: AWS KMS invoked by S3
* Features: Key policies, automatic rotation, CMK metadata

The flow is similar to SSE-S3 but uses a KMS Customer Master Key (CMK):

<Frame>
  ![The image illustrates the SSE-KMS process in AWS, showing a user interacting with an S3 bucket and a server, with a KMS key used for encryption.](https://kodekloud.com/kk-media/image/upload/v1752869231/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-S3-Encryption/sse-kms-aws-s3-encryption-diagram.jpg)
</Frame>

**AWS CLI Examples**

```bash theme={null}
