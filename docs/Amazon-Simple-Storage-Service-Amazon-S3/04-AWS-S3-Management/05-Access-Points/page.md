# Create an S3 bucket in us-east-1
aws s3api create-bucket \
  --bucket my-unique-bucket-name \
  --region us-east-1
```

![The image shows a green bucket icon with shapes on it, equated to a yellow folder icon, suggesting a comparison or analogy between a bucket and a folder.](https://kodekloud.com/kk-media/image/upload/v1752869359/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/green-bucket-yellow-folder-comparison.jpg)

### Objects

An **object** is any file stored in S3. Each object includes:

* **Key**: the unique object name (e.g., `photos/vacation.jpg`)
* **Value**: the actual file data
* **Metadata**: custom or system attributes (e.g., `Content-Type`)
* **Version ID**: if versioning is enabled

```bash theme={null}
# Upload a file to S3
aws s3 cp ./vacation.jpg s3://my-unique-bucket-name/photos/vacation.jpg
```

![The image explains that objects are files uploaded to S3, consisting of a key (file name), value (file data), and additional metadata. It uses PDF and MP3 file icons to illustrate these concepts.](https://kodekloud.com/kk-media/image/upload/v1752869360/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/s3-objects-files-key-value-metadata.jpg)

### Flat Namespace and “Folders”

Under the hood, S3 is a flat key-value store. The console mimics directories by treating prefixes (text before a `/`) as folders.

```text theme={null}
music/song1.mp3
music/song2.mp3
music/song3.mp3
```

* These keys appear under a `music/` folder in the console but are stored flat in S3.

![The image illustrates the flat file structure of S3 buckets, showing files and folders with examples like "File1.txt" and a "music/" directory containing songs.](https://kodekloud.com/kk-media/image/upload/v1752869360/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/s3-bucket-flat-file-structure.jpg)

## Durability and Availability

When you upload to S3, AWS replicates your data across multiple servers and Availability Zones (AZs) within a region, ensuring high durability and availability—even if an AZ fails.

![The image illustrates an AWS architecture with three availability zones in the us-east-1 region, each containing compute resources and PNG files, and a central S3 bucket.](https://kodekloud.com/kk-media/image/upload/v1752869362/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/aws-architecture-three-availability-zones.jpg)

## Bucket Naming and Global Uniqueness

Each bucket name must be unique across all AWS accounts and regions. The bucket name appears in the URL:

```text theme={null}
https://my-unique-bucket-name.s3.amazonaws.com/
```

> **triangle-alert** Choose bucket names carefully. Renaming or deleting buckets can disrupt applications that rely on them.

![The image is about S3 bucket names, highlighting that they must be unique globally across all AWS accounts. It includes a URL example and a graphic of a person.](https://kodekloud.com/kk-media/image/upload/v1752869363/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/s3-bucket-names-global-uniqueness.jpg)

## Limits and Restrictions

| Resource            | Limit                               |
| ------------------- | ----------------------------------- |
| Number of buckets   | 100 per account (increase to 1,000) |
| Maximum object size | 5 TB                                |
| Objects per bucket  | Unlimited                           |

![The image outlines AWS S3 restrictions, stating it can handle unlimited objects, a single file can be up to 5TB, and an account supports 100 buckets by default, expandable to 1,000.](https://kodekloud.com/kk-media/image/upload/v1752869364/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-What-is-AWS-S3/aws-s3-restrictions-objects-buckets.jpg)

> **lightbulb** You can request a service quota increase for more buckets or higher throughput in the AWS Console under [Service Quotas](https://console.aws.amazon.com/servicequotas/).

***

In this lesson, we covered AWS S3’s fundamental concepts, common use cases, and architectural design. Next up: a hands-on demo to create and configure your first S3 bucket.

## References

* [Amazon S3 Developer Guide](https://docs.aws.amazon.com/s3/index.html)
* [AWS CLI Command Reference – S3](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html)
* [Understanding Data Consistency in Amazon S3](https://aws.amazon.com/s3/faqs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/eec05698-c022-44e4-9421-cf157eb32097/lesson/193ac9c9-a85d-4ea4-bb58-75b0f750ee48)


# Access Points

Source: https://notes.kodekloud.com/docs/Amazon-Simple-Storage-Service-Amazon-S3/AWS-S3-Management/Access-Points/page

Access Points streamline and secure Amazon S3 bucket access for multiple teams, applications, and workloads with dedicated ARNs and resource policies.

Access Points streamline and secure Amazon S3 bucket access for multiple teams, applications, and workloads. Instead of a single, complex bucket policy, you can create dedicated Access Points—each with its own ARN and resource policy—to manage permissions at scale.

> **lightbulb** Access Points work with existing S3 features, including bucket ACLs, public access settings, and server-side encryption.

## The Challenge of Complex Bucket Policies

When you have diverse stakeholders sharing one bucket, the policy can balloon:

| Team           | Required Permissions              | Use Case                                |
| -------------- | --------------------------------- | --------------------------------------- |
| Developers     | `s3:PutObject`, `s3:DeleteObject` | Upload and manage application assets    |
| Infrastructure | `s3:*`                            | Full lifecycle, encryption, and logging |
| Legal          | `s3:GetObject`, `s3:ListBucket`   | Compliance audits and data retrieval    |

Every change to a team’s access means editing the monolithic bucket policy, which increases the risk of errors and makes audits difficult.

## Introducing Access Points

With S3 Access Points, you assign each team or application its own “window” to the bucket. Each Access Point:

* Has a unique ARN (`arn:aws:s3:<region>:<account-id>:accesspoint/<name>`)
* Behaves like an independent bucket
* Carries a tailored resource policy

![The image illustrates access points for different roles (Developers, Admin, Infra, Legal) connecting to a central bucket, likely representing a data storage or resource access system.](https://kodekloud.com/kk-media/image/upload/v1752869365/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Access-Points/access-points-roles-data-storage.jpg)

Clients reference the Access Point ARN instead of the bucket ARN, and permissions live closer to the consumer. For example, developers use the `developer-ap` Access Point ARN with write/delete privileges, while the legal team uses `legal-ap` with read-only permissions.

## Restricting Access by VPC

You can tie an Access Point to a specific VPC Endpoint to enforce network-level boundaries. Bind the Access Point so only resources in your VPC can connect:

![The image illustrates a concept of access point restriction for Virtual Private Clouds (VPCs), showing one VPC with access to a resource (indicated by a check mark) and another without access (indicated by a cross mark).](https://kodekloud.com/kk-media/image/upload/v1752869366/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Access-Points/vpc-access-point-restriction-diagram.jpg)

For instance:

* **VPC A**: EC2 instances can access via `ap-vpc-a`.
* **All other VPCs**: Traffic is blocked by the endpoint policy.

> **triangle-alert** Ensure your VPC Endpoint policy explicitly grants `s3:*` actions for the Access Point ARN; otherwise, requests will be denied.

## Simplifying Policy Management

Instead of embedding every role’s permissions in the bucket policy, you delegate authority to Access Points with a single bucket policy statement:

![The image illustrates an "Access Point Policy" with diagrams showing the process of copying policies to a bucket policy and delegating policies to an access point.](https://kodekloud.com/kk-media/image/upload/v1752869367/notes-assets/images/Amazon-Simple-Storage-Service-Amazon-S3-Access-Points/access-point-policy-diagram-bucket-delegation.jpg)

1. **Delegate in the bucket policy** to allow S3 actions for any Access Point.
2. **Define fine-grained permissions** within each Access Point resource policy.

Example: Delegate List and Get operations for all Access Points in the bucket policy:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DelegateAccessPointActions",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": "arn:aws:s3:us-west-2:123456789012:accesspoint/*"
        }
      }
    }
  ]
}
```

Then, move user- or group-specific permissions into each Access Point policy. Example for a developer Access Point:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/Developer"
      },
      "Action": [
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:us-west-2:123456789012:accesspoint/developer-ap/object/*"
    }
  ]
}
```

With this approach, you only update the bucket policy once. All subsequent permission changes happen at the Access Point level, making management and compliance audits far simpler.

## Links and References

* [Amazon S3 Access Points Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html)
* [VPC Endpoints for Amazon S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
* [Managing S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-access-control.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3/module/985e08bc-a007-4d29-9e60-fe90b52410ae/lesson/2d9a3401-efd2-45b1-8957-bc024a82497a)
