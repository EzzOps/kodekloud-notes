# Restrict key permissions so SSH accepts the key
chmod 400 ec2-demo.pem

# Replace PUBLIC_IP with the instance public IPv4 or use the public DNS
ssh -i ec2-demo.pem ubuntu@PUBLIC_IP
```

On first connection SSH will ask to confirm the host key — type `yes`. A successful login will show a prompt such as:

```text theme={null}
ubuntu@ip-172-31-90-1:~$
```

Simple commands to run after connecting:

```bash theme={null}
# List files in home
ls -la

# Check disk space
df -h

# Update package lists (Ubuntu)
sudo apt update
```

> **lightbulb** If SSH fails, check:

  * Security group inbound rules (SSH allowed from your IP).
  * The username matches the AMI (e.g., `ubuntu`, `ec2-user`).
  * The private key file has restrictive permissions (`chmod 400 ec2-demo.pem`).

## 8. Stop, reboot, or terminate

When finished, manage instance lifecycle via the Actions menu:

* Stop: Graceful shutdown; you can start it later.
* Reboot: Restart the instance.
* Terminate: Permanently delete the instance and (usually) its attached root EBS volume, depending on the DeleteOnTermination setting.

Terminate or stop unused instances to avoid unexpected charges.

## Links and references

* [Amazon EC2 overview](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2)
* [EC2 key pairs documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
* [EC2 AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
* [EBS volumes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)
* [AWS CloudWatch](https://learn.kodekloud.com/user/courses/aws-cloudwatch)

Follow these steps to quickly launch and access an EC2 instance; for production environments apply hardened security group rules, use IAM roles, and enable monitoring and backups.

- [Watch Video](https://learn.kodekloud.com/user/courses/crash-course-aws-basics/module/76d6cbfc-c16d-4f87-a93c-31cfa5f795f7/lesson/f899c186-e429-421b-bbe4-2cd3d1fa2e80)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/crash-course-aws-basics/module/76d6cbfc-c16d-4f87-a93c-31cfa5f795f7/lesson/c38f7fe0-bcbd-4f92-80b1-5bb1097d2369)


# Amazon S3 Simple Storage Service Part 1

Source: https://notes.kodekloud.com/docs/Crash-Course-AWS-Basics/AWS-Services/Amazon-S3-Simple-Storage-Service-Part-1/page

Step-by-step guide to creating and managing an Amazon S3 bucket, configuring properties and permissions, and uploading objects.

In this guide you'll create your first Amazon S3 bucket, explore the main console screens, and upload an object. The steps below preserve the console workflows and screenshots so you can follow along in the same sequence.

## 1. Open S3 in the AWS Console

Sign in to the AWS Management Console and search for **S3**. If you have no buckets yet, the S3 dashboard shows a prompt to create one. If you already have buckets, you will see a list and the same "Create bucket" action.

<Frame>
  <img alt="A screenshot of the Amazon S3 web console showing an Account snapshot (storage, object count, average size) and the Buckets panel. The Buckets list is empty and there's a prominent &#x22;Create bucket&#x22; button." />
</Frame>

Important: the region selector at the top of the console controls the default region view, but S3 displays a global list of your buckets. When you create a bucket you explicitly choose the region in which that individual bucket will reside.

## 2. Create a bucket (name and region)

Click **Create bucket** and enter a globally unique name for your bucket. Bucket names must be unique across all AWS accounts and regions, so pick a name that is unlikely to be taken (for example, include your initials, project name, or a timestamp).

> **lightbulb** S3 bucket names are globally unique across all AWS accounts and regions. Use a descriptive, unique name (for example `yourname-project-2026`) to avoid naming conflicts.

Example of the Create bucket page showing a chosen name and region:

<Frame>
  <img alt="A screenshot of the AWS S3 &#x22;Create bucket&#x22; configuration page showing the bucket name &#x22;kk-demo-123&#x22;, region set to US East (N. Virginia), and Object Ownership settings with ACLs disabled selected. The lower part of the page shows Block Public Access settings." />
</Frame>

For full naming requirements, see the S3 documentation:

* [Bucket naming rules — AWS S3 Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html)

<Frame>
  <img alt="A screenshot of the Amazon S3 User Guide showing the &#x22;Bucket naming rules&#x22; page, with a list of bullet-point rules for naming S3 buckets and a navigation menu on the left. The page includes notes about character limits, allowed characters, and suffix/prefix restrictions." />
</Frame>

## 3. Key Create bucket settings (overview)

On the Create bucket page you’ll configure several important options. Below is a concise summary of the common settings and their purpose:

| Setting                                    | Purpose                                                           | Typical choice for beginners                         |
| ------------------------------------------ | ----------------------------------------------------------------- | ---------------------------------------------------- |
| Object ownership                           | Controls ownership for objects uploaded by different AWS accounts | `Bucket owner preferred` (or leave default)          |
| Block Public Access                        | Prevents public access unless explicitly allowed                  | **Enabled** (recommended)                            |
| Versioning                                 | Retain prior versions of objects                                  | Disabled (enable if you need object version history) |
| Default encryption                         | Automatically encrypt objects at rest                             | Disabled (or enable SSE-S3 / SSE-KMS for production) |
| Advanced options (Object Lock, MFA Delete) | Regulatory retention and protection features                      | Leave disabled unless required                       |

For this lesson we leave defaults (bucket locked down, no versioning or default encryption) and click **Create bucket**. After creation the new bucket appears in the list with its region and creation time — click the bucket name to open its detail view.

## 4. Bucket Properties

The Properties tab displays high-level metadata and status flags:

* Bucket ARN (the canonical identifier)
* Region and creation date
* Status of features (versioning, default encryption, MFA delete)
* Links to configure server access logging, CloudTrail data events, event notifications, transfer acceleration, object lock, requester pays, and static website hosting

<Frame>
  <img alt="A screenshot of an AWS S3 bucket Properties page for &#x22;kk-demo-123,&#x22; showing the bucket overview (region US East. N. Virginia, ARN, creation date) and that versioning and MFA delete are disabled. It also shows there are no tags or default encryption configured." />
</Frame>

Some property panes show sources of additional visibility and control:

<Frame>
  <img alt="Screenshot of an AWS S3 console showing the &#x22;AWS CloudTrail data events&#x22; and &#x22;Event notifications&#x22; sections. Both sections show no entries (&#x22;No data events&#x22; and &#x22;No event notifications&#x22;) with buttons to configure CloudTrail or create an event notification." />
</Frame>

## 5. Permissions tab — access control

The Permissions tab centralizes who can access the bucket and its objects. By default:

* Block Public Access is turned on and prevents public access
* Only the creating AWS account has full access
* You can add bucket policies, IAM policies, or ACLs to grant other principals access

<Frame>
  <img alt="A screenshot of an AWS S3 bucket settings page showing &#x22;Block all public access&#x22; turned on and the Bucket policy section reporting &#x22;Public access is blocked&#x22; with &#x22;No policy to display.&#x22; The panel also includes an Edit button and links to learn more about Amazon S3 Block Public Access." />
</Frame>

> **warning** Be careful when disabling Block Public Access or making objects public. Misconfigured public buckets can expose sensitive data to the internet.

## 6. Metrics and Management

* Metrics (CloudWatch) show storage size, object count, and request rates.
* Management contains lifecycle policies, replication rules, inventory, analytics, and access points — use these to control costs, durability, and access over time.

<Frame>
  <img alt="A screenshot of an Amazon S3 bucket settings page showing the &#x22;Replication rules&#x22; and &#x22;Inventory configurations&#x22; sections. Both sections are empty and display buttons to create a replication rule or create an inventory configuration." />
</Frame>

## 7. Upload an object

Open the **Objects** tab and click **Upload** (or drag-and-drop files/folders). During upload you can:

* Add single files or a folder
* Set the destination path (key prefix)
* Choose a storage class (Standard, Intelligent‑Tiering, Standard‑IA, One Zone‑IA, Glacier, etc.)
* Set metadata and permissions (defaults inherit bucket settings)

<Frame>
  <img alt="A screenshot of the AWS S3 &#x22;Upload&#x22; page showing one file (pexels-julio-nery-1687147.jpg, 2.7 MB) queued for upload. The destination bucket is s3://kk-demo-123 and there's an orange &#x22;Upload&#x22; button at the bottom." />
</Frame>

S3 storage classes trade off cost and availability. For most general-purpose objects choose `Standard`. You can change the class per object or add lifecycle rules later to move objects to cheaper tiers.

<Frame>
  <img alt="A screenshot of the Amazon S3 console showing a bucket's Permissions and Properties sections, with a Storage class table listing options like Standard, Intelligent‑Tiering, Standard‑IA, One Zone‑IA, and Glacier. The Standard storage class is selected." />
</Frame>

Click **Upload** to start the transfer. When complete the object appears in the bucket’s object list showing name, size, and last modified timestamp.

<Frame>
  <img alt="Screenshot of an Amazon S3 bucket named &#x22;kk-demo-123&#x22; showing the Objects tab with one file (pexels-julio-nery-1687147.jpg) listed, size 2.7 MB and last modified April 4, 2023." />
</Frame>

## Next steps and references

Now that you’ve created a bucket and uploaded an object, consider these follow-up topics:

* Enable versioning and practice restoring older object versions
* Configure lifecycle policies to move or expire objects automatically
* Turn on default encryption (SSE-S3 or SSE-KMS) for data-at-rest protection
* Set up replication rules if you need cross-region redundancy
* Create fine-grained access using bucket policies and IAM policies

References:

* Amazon S3 documentation: [https://docs.aws.amazon.com/s3/](https://docs.aws.amazon.com/s3/)
* S3 bucket naming rules: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html)

This completes the basics: creating an S3 bucket, inspecting its properties and permissions, and uploading your first object. Future lessons will dive deeper into versioning, lifecycle rules, encryption, replication, and advanced access patterns.

- [Watch Video](https://learn.kodekloud.com/user/courses/crash-course-aws-basics/module/76d6cbfc-c16d-4f87-a93c-31cfa5f795f7/lesson/aac28cb1-a3a9-46a5-bd68-18d22e3825a0)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/crash-course-aws-basics/module/76d6cbfc-c16d-4f87-a93c-31cfa5f795f7/lesson/e13894c8-f3f2-471b-93dc-6b173612dcbb)
