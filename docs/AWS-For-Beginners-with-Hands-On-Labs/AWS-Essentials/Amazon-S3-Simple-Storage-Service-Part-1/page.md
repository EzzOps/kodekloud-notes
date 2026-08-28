# Restrict PEM permissions (required on many systems)
chmod 400 ec2-demo.pem

# SSH to the instance (replace <public-ip> with the instance's public IPv4)
ssh -i ec2-demo.pem ubuntu@<public-ip>
```

* On first connect you may be prompted to accept the host key (type "yes").
* After successful authentication you will see the remote shell prompt, e.g.:

```bash theme={null}
ubuntu@ip-172-31-90-1:~$ ls -la
```

Windows options

* Convert PEM to PPK for PuTTY using PuTTYgen ([https://www.putty.org/](https://www.putty.org/)) or
* Use Windows Subsystem for Linux ([https://learn.microsoft.com/windows/wsl/](https://learn.microsoft.com/windows/wsl/)) or native OpenSSH ([https://www.openssh.com/](https://www.openssh.com/)) to run the same ssh commands as above.

Stop vs Terminate

* Stop: powers off the instance and preserves the EBS root volume. You can later Start it again.
* Terminate: deletes the instance and (by default) its associated root volume; data not backed up will be lost.

References

* AWS EC2 documentation: [https://docs.aws.amazon.com/ec2/](https://docs.aws.amazon.com/ec2/)
* Accessing instances (SSH): [https://docs.aws.amazon.com/AWSEC2/[AWS_SECRET_ACCESS_KEY].html](https://docs.aws.amazon.com/AWSEC2/[AWS_SECRET_ACCESS_KEY].html)
* PuTTY and PuTTYgen: [https://www.putty.org/](https://www.putty.org/)
* Windows Subsystem for Linux: [https://learn.microsoft.com/windows/wsl/](https://learn.microsoft.com/windows/wsl/)

This completes the quick demo: launching an EC2 instance, inspecting its configuration, connecting via SSH, and managing its lifecycle.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/d28d64dd-cbb1-45ed-83c4-e8d4b0b0d08b/lesson/f899c186-e429-421b-bbe4-2cd3d1fa2e80" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/d28d64dd-cbb1-45ed-83c4-e8d4b0b0d08b/lesson/c38f7fe0-bcbd-4f92-80b1-5bb1097d2369" />
</CardGroup>


# Amazon S3 Simple Storage Service Part 1

Source: https://notes.kodekloud.com/docs/AWS-For-Beginners-with-Hands-On-Labs/AWS-Essentials/Amazon-S3-Simple-Storage-Service-Part-1/page

Guide to creating an Amazon S3 bucket via the AWS Console, configuring settings and permissions, and uploading objects with console and CLI examples.

In this guide you'll create your first Amazon S3 bucket through the AWS Management Console, inspect the key bucket pages (Objects, Properties, Permissions, Metrics, Management), and upload a file. The steps below are ordered to follow the console flow and include CLI examples for automation.

Start by opening the AWS Console and searching for the S3 service. If you have no buckets yet, the console invites you to create one. If you already have buckets, you'll see a list and a Create bucket button.

<Frame>
  <img alt="A screenshot of the Amazon S3 webpage showing the headline &#x22;Store and retrieve any amount of data from anywhere,&#x22; a large AWS video thumbnail, and a right-hand sidebar with panels for creating a bucket, pricing, resources, and common tasks." />
</Frame>

If your account has no buckets the console emphasizes creating a bucket with a prominent "Create bucket" action:

<Frame>
  <img alt="A screenshot of the AWS S3 Buckets console showing an account snapshot with storage metrics at the top. The Buckets list is empty and a &#x22;Create bucket&#x22; button is shown." />
</Frame>

Key concept: S3 bucket names are globally unique across all AWS accounts and regions. You do not select a region on the global bucket list — you choose the bucket region at creation time.

<Callout icon="lightbulb">
  S3 bucket names must be globally unique. The console displays all buckets from every region; pick the bucket's region when you create it.
</Callout>

## Create a bucket

Click Create bucket to begin. Provide a globally unique name — common names like "demo" are already used. In this walkthrough we use the example name kk-demo-123.

<Frame>
  <img alt="A screenshot of the AWS S3 &#x22;Create bucket&#x22; console showing the General configuration (bucket name &#x22;kk-demo-123&#x22; and region US East N. Virginia) and Object Ownership settings, with ACLs disabled recommended. The lower part also shows the Block Public Access settings section." />
</Frame>

If you want the full rules for valid bucket names, review the AWS documentation on bucket naming:

<Frame>
  <img alt="A screenshot of the Amazon S3 documentation page titled &#x22;Bucket naming rules,&#x22; showing a list of bullet-point rules for naming S3 buckets. The left side shows the user guide navigation menu." />
</Frame>

When creating a bucket you must also choose the target region and can configure options such as:

* Object ownership (controls whether objects are owned by the bucket owner or the object uploader),
* Block Public Access settings,
* Versioning,
* Default encryption,
* Tags, and more.

Block Public Access is enabled by default to protect you from accidentally exposing data.

<Callout icon="warning">
  Do not disable Block Public Access unless you intentionally want objects to be publicly accessible. Public buckets can expose data to anyone on the internet.
</Callout>

## After creation — bucket overview

After the bucket is created it appears in the list with its region and creation date. Click the bucket name to open its dedicated console page.

On the Objects tab you will find all files (objects) stored in the bucket. A freshly created bucket contains no objects.

<Frame>
  <img alt="A screenshot of the Amazon S3 console for bucket &#x22;kk-demo-123&#x22; showing the Objects tab with no objects listed and an &#x22;Upload&#x22; button." />
</Frame>

Open the Properties tab to view bucket metadata such as the bucket ARN, region, creation date, versioning status, tags, and default encryption settings.

<Frame>
  <img alt="A screenshot of an AWS S3 bucket Properties page for &#x22;kk-demo-123&#x22; in the US East (N. Virginia) region. It shows the bucket ARN and creation date, with versioning disabled and no tags configured." />
</Frame>

The bucket ARN (Amazon Resource Name) uniquely identifies your bucket across AWS. As you enable features such as versioning, server access logging, transfer acceleration, or static website hosting, those statuses are shown in Properties.

Use the Permissions tab to control access. By default the bucket is owned and accessible only by the bucket owner. From Permissions you can attach:

* Bucket policies (recommended for fine-grained access control),
* Access Control Lists (ACLs — not recommended for new accounts),
* Block Public Access settings,
* CORS rules for browser-based access.

<Frame>
  <img alt="A screenshot of an AWS S3 bucket settings page showing the &#x22;Block all public access&#x22; option turned on. The Bucket policy section states public access is blocked and shows &#x22;No policy to display.&#x22;" />
</Frame>

Metrics (CloudWatch) and the Management tab surface additional features:

* Metrics: storage used, object counts, request metrics.
* Management: lifecycle rules (transition/expiration), replication between regions or accounts, inventory, and access points.

## Upload an object

To upload a file return to the Objects tab and click Upload. You can Add files, Add folder, or drag-and-drop. The console shows file size and detected type prior to upload.

<Frame>
  <img alt="A screenshot of the AWS S3 &#x22;Upload&#x22; page showing one JPEG file (pexels-julio-nery-1687147.jpg, 2.7 MB) queued for upload. The destination bucket is s3://kk-demo-123 and there are Cancel and Upload buttons at the bottom." />
</Frame>

During upload you can confirm or change:

* Permissions (uploads inherit bucket defaults unless you override them),
* Versioning behavior for the object (if bucket versioning is enabled),
* Storage class selection.

S3 provides multiple storage classes to balance cost, durability, and availability. Common storage classes include Standard, Intelligent‑Tiering, Standard‑IA, One Zone‑IA, and Glacier. Use the table below to compare typical use cases.

| Storage Class                  | Typical Use Case                             | Notes                                              |
| ------------------------------ | -------------------------------------------- | -------------------------------------------------- |
| Standard                       | Frequently accessed data                     | High durability and availability                   |
| Intelligent‑Tiering            | Unknown or changing access patterns          | Automatic tiering to save costs                    |
| Standard‑IA                    | Infrequently accessed, requires rapid access | Lower storage costs, retrieval fee applies         |
| One Zone‑IA                    | Infrequently accessed, non-critical          | Stored in a single AZ — cheaper but less resilient |
| Glacier / Glacier Deep Archive | Long-term archiving                          | Low cost, retrieval times vary                     |

<Frame>
  <img alt="A screenshot of the AWS S3 console showing a bucket's Permissions banner and Properties section. The visible panel lists Storage class options (Standard, Intelligent‑Tiering, Standard‑IA, One Zone‑IA, Glacier, etc.) for the bucket." />
</Frame>

After the upload completes you will see a green check in the console and the object will appear in the Objects list.

<Frame>
  <img alt="Screenshot of an Amazon S3 bucket page for &#x22;kk-demo-123&#x22;. It shows one object named &#x22;pexels-julio-nery-1687147.jpg&#x22; (2.7 MB) with options to upload, create folders, and manage the bucket." />
</Frame>

## Quick CLI examples (optional)

You can also create buckets and upload files with the AWS CLI. Replace \<region> and \<bucket-name> with your values.

Create a bucket (example for regions other than us-east-1):

```bash theme={null}
aws s3api create-bucket \
  --bucket kk-demo-123 \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2
```

Note: For us-east-1 (N. Virginia) you should omit LocationConstraint:

```bash theme={null}
aws s3api create-bucket \
  --bucket kk-demo-123 \
  --region us-east-1
```

Upload a file using the high-level S3 command:

```bash theme={null}
aws s3 cp ./pexels-julio-nery-1687147.jpg s3://kk-demo-123/
```

For scripted or programmatic interactions consider the AWS SDKs (Python boto3, JavaScript AWS SDK, etc.) and CI/CD integration.

## Next steps and references

This completes the basic flow: creating a bucket and uploading an object. From here you can explore:

* Enabling versioning and restoring previous versions,
* Creating lifecycle rules to transition or expire objects,
* Configuring default encryption (SSE-S3 or SSE-KMS),
* Adding bucket policies for cross-account access,
* Using the AWS CLI and SDKs for automation.

Useful references:

* AWS S3 Documentation: [https://docs.aws.amazon.com/s3/](https://docs.aws.amazon.com/s3/)
* S3 Bucket Naming Rules: [https://docs.aws.amazon.[SECRET_REDACTED].html](https://docs.aws.amazon.[SECRET_REDACTED].html)
* Working with Objects (S3 docs): [https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-objects.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-objects.html)

<Callout icon="lightbulb">
  For production buckets, enable default encryption, enable versioning (if applicable), and use lifecycle policies to manage storage costs.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/d28d64dd-cbb1-45ed-83c4-e8d4b0b0d08b/lesson/aac28cb1-a3a9-46a5-bd68-18d22e3825a0" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-for-beginners-with-hands-on-labs/module/d28d64dd-cbb1-45ed-83c4-e8d4b0b0d08b/lesson/e13894c8-f3f2-471b-93dc-6b173612dcbb" />
</CardGroup>
