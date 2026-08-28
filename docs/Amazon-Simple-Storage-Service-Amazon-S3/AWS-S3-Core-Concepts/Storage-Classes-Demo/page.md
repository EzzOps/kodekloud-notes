# Storage Classes Demo

Source: https://notes.kodekloud.com/docs/Amazon-Simple-Storage-Service-Amazon-S3/AWS-S3-Core-Concepts/Storage-Classes-Demo/page

Learn to specify and change the storage class of objects in Amazon S3 using the AWS Management Console.

Learn how to specify and change the storage class of objects in Amazon S3 using the AWS Management Console. This guide covers uploading files with a custom storage class and modifying it afterward.

## Prerequisites

* An AWS account with S3 access.
* IAM user permissions: `s3:CreateBucket`, `s3:PutObject`, `s3:PutObjectStorageClass`.
* Familiarity with the [Amazon S3 console](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html).

<Callout icon="lightbulb">
  Choosing the right storage class balances cost, durability, and retrieval time. Review [S3 pricing](https://aws.amazon.com/s3/pricing/) before proceeding.
</Callout>

## 1. Create a New S3 Bucket

1. Open the [Amazon S3 console](https://console.aws.amazon.com/s3/).
2. Click **Create bucket**.
3. Enter **Bucket name**: `kk-sc-demo`.
4. Leave default settings and click **Create bucket**.

## 2. Upload an Object with a Custom Storage Class

1. In the **kk-sc-demo** bucket, click **Upload**.
2. Choose **Add files** and select your file.
3. Under **Properties**, expand **Storage class** and select **One Zone-IA** (default is Standard).

<Frame>
  ![The image shows an Amazon S3 Management Console screen displaying different storage class options, including Standard, Intelligent-Tiering, and Glacier, with details about their availability zones and minimum storage duration.](https://kodekloud.com/kk-media/image/upload/v1752869343/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Storage-Classes-Demo/amazon-s3-management-console-storage-classes.jpg)
</Frame>

4. Click **Upload**. The object now appears with the specified storage class.

## Storage Class Comparison

| Storage Class              | Use Case                             | Min. Storage Duration | Durability & Availability                   |
| -------------------------- | ------------------------------------ | --------------------- | ------------------------------------------- |
| Standard                   | Frequent access                      | None                  | 99.999999999% durability, 99.99% avail.     |
| One Zone-IA                | Infrequent access, lower cost        | 30 days               | 99.999999999% durability, single AZ         |
| Intelligent-Tiering        | Unknown/variable access patterns     | 30 days               | Auto-optimizes cost                         |
| Glacier Flexible Retrieval | Long-term archive, infrequent access | 90 days               | 99.999999999% durability, minutes retrieval |
| Glacier Deep Archive       | Archival with minimal retrieval      | 180 days              | Lowest-cost archival storage                |

<Callout icon="triangle-alert">
  Archival classes (Glacier) incur retrieval fees and can take from minutes to hours.
</Callout>

## 3. Change the Storage Class of an Existing Object

1. In the **kk-sc-demo** bucket, select the object (e.g., `beach1.jpg`).
2. Choose **Actions** → **Change storage class**.
3. Select **Standard** (or another class) and click **Save**.

<Frame>
  ![The image shows an Amazon S3 console with a bucket named "kk-sc-demo" containing a single file, "beach1.jpg," which is 1.3 MB in size.](https://kodekloud.com/kk-media/image/upload/v1752869344/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Storage-Classes-Demo/amazon-s3-console-kk-sc-demo.jpg)
</Frame>

***

## Links and References

* [Amazon S3 Storage Classes Overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)
* [Managing S3 Object Lifecycles](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
* [AWS S3 Pricing](https://aws.amazon.com/s3/pricing/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/eec05698-c022-44e4-9421-cf157eb32097/lesson/e1f856d3-369c-4186-85b3-55041b57955e" />
</CardGroup>
