# What is AWS S3

Source: https://notes.kodekloud.com/docs/Amazon-Simple-Storage-Service-Amazon-S3/AWS-S3-Core-Concepts/What-is-AWS-S3/page

Amazon S3 is a fully managed object storage solution offering scalability, data availability, security, and performance within the AWS ecosystem.

Amazon S3 (Simple Storage Service) is a fully managed object storage solution offering industry-leading scalability, data availability, security, and performance. Think of it as a highly durable, highly available file store—similar to Dropbox or Google Drive—but deeply integrated into the AWS ecosystem.

## Key Features

<Frame>
  ![The image explains the features of Amazon S3 (Simple Storage Service), highlighting scalability, data availability, security, and performance.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869352/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/amazon-s3-features-scalability-security-performance.jpg)
</Frame>

* Virtually unlimited storage capacity
* 99.999999999% (11 9’s) of data durability
* Fine-grained access control with IAM policies and bucket policies
* Multiple interfaces: Console, AWS CLI, AWS SDKs, REST API

## Seamless AWS Integration

Because S3 is an AWS-native service, it integrates seamlessly with services like EC2, Lambda, and IAM. You can manage buckets and objects using:

* AWS Management Console
* AWS CLI
* AWS SDKs (e.g., Boto3 for Python)
* RESTful API calls

<Frame>
  ![The image compares cloud storage services, showing logos for Dropbox, Google Drive, and an S3 bucket, with the question "What is S3?"](../../../../images/kodekloud.com/kk-media/image/upload/v1752869353/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/cloud-storage-comparison-dropbox-google-s3.jpg)
</Frame>

<Frame>
  ![The image is a diagram titled "What Is S3?" showing AWS services, including S3 (represented by a bucket icon), EC2, Lambda, and IAM.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869355/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/what-is-s3-aws-services-diagram.jpg)
</Frame>

## Object Storage vs. File and Block Storage

S3 is **object-based** storage: you upload whole objects (files) rather than individual blocks. It uses a flat namespace rather than a hierarchical filesystem, so you cannot mount an S3 bucket like an EBS volume or NFS share.

| Storage Type | Description                       | Examples                  |
| ------------ | --------------------------------- | ------------------------- |
| Object       | Stores entire files as objects    | Amazon S3                 |
| File         | Shares directories over a network | NFS, Amazon EFS           |
| Block        | Presents raw block devices to OS  | EBS, direct-attached SSDs |

<Frame>
  ![The image explains S3 as object-based storage, contrasting it with file-based storage (NFS and EFS) and block-based storage (Server and EBS), indicating EFS and EBS as correct options.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869356/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/s3-object-storage-vs-file-block.jpg)
</Frame>

## Common Use Cases

* Storing application log files
* Hosting media assets (images, videos, audio)
* Saving CI/CD pipeline artifacts

<Frame>
  ![The image illustrates three S3 use cases: storing log files, media (audio/video/images), and CI/CD artifacts, with corresponding icons for each category.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869356/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/s3-use-cases-log-media-artifacts.jpg)
</Frame>

## Real-World Example: Offloading Media for a Website

In traditional web hosting, your server handles HTML, CSS, JavaScript, and all media. As traffic scales—imagine YouTube or Netflix—storing petabytes of video on web servers becomes costly and unscalable.

With S3:

1. Keep only static assets (HTML/CSS/JS) on your web server
2. Offload large media files to an S3 bucket
3. Reference S3 URLs in your HTML so browsers fetch content directly from S3

<Frame>
  ![The image illustrates an S3 use case, showing a user interacting with a server to access video content, with a comparison to storing content in an S3 bucket.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869358/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/s3-use-case-user-server-video-content.jpg)
</Frame>

## Key Terminology

### Buckets

A **bucket** is a container for objects—think of it as a top-level folder. Names must be globally unique across all AWS accounts.

```bash theme={null}
