# Google Cloud Storage GCS Overview and Bucket Setup

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Storage-Options/Google-Cloud-Storage-GCS-Overview-and-Bucket-Setup/page

Guide to Google Cloud Storage and how to create, configure, and manage production ready buckets for data engineering including storage classes, location, access control, versioning, and lifecycle policies.

Hello and welcome back.

In this lesson we’ll cover Google Cloud Storage (GCS): what it is, why it matters for data engineers, and how to create and configure a bucket for production-ready data workflows. GCS is a core Google Cloud service used as a durable object store for everything from small log files to petabyte-scale data lakes. For data engineers, GCS is often the persistent layer where raw data lands, intermediate artifacts are written, and final datasets are staged for analytics and machine learning.

What GCS provides (high level)

* Universal object storage: stores structured, semi-structured, and unstructured data — CSV, JSON, images, video, binary blobs, and more.
* Common use cases: backups and archival, media distribution, analytics, ML training datasets, and data lake storage.
* Pricing model: pay-as-you-go with no upfront commitments — suitable for both experimentation and production workloads.
* Global access and low-latency delivery: objects can be accessed securely from around the world; latency depends on the chosen location.
* Deep integrations: native connectors to BigQuery, Dataflow, Cloud Functions, and Vertex AI streamline end-to-end data pipelines.

In short: GCS is more than “buckets and files.” It’s an integrated, scalable, and secure storage backbone for Google Cloud.

Creating a bucket — important configuration choices
A bucket is the top-level container for objects. Objects are the individual files you store. When you create a bucket, there are several decisions that directly affect cost, performance, durability, and access controls:

1. Bucket name (global and immutable)

   * Rules to follow:
     * 3–63 characters
     * Lowercase letters, numbers, dashes, and dots allowed
     * Must start and end with a letter or number
     * No uppercase letters or underscores
     * Cannot be formatted like an IP address

   <Callout icon="lightbulb">
     Use a predictable naming convention (for example, `project-environment-region-purpose`) so it’s easier to manage and discover buckets across teams.
   </Callout>

   Recommended pattern example:

   * `myproject-prod-us-central1-raw` — indicates project, environment, location, and purpose.

2. Storage class — pick based on access patterns and cost
   * Storage class affects storage pricing and retrieval characteristics. Use the following decision guide.

| Storage class | Best for                          | Typical cost/latency profile                        |
| ------------- | --------------------------------- | --------------------------------------------------- |
| Standard      | Frequent access, active workloads | Higher storage cost, low latency                    |
| Nearline      | Infrequent access (monthly)       | Lower storage cost, retrieval fees apply            |
| Coldline      | Rare access (quarterly)           | Lower storage cost, higher retrieval fees           |
| Archive       | Long-term retention (yearly)      | Lowest storage cost, highest retrieval latency/fees |

3. Location (region, dual-region, multi-region)
   * Choose based on latency, redundancy, and compliance requirements. Examples:
     * Region: `us-central1` — data stored in a single region
     * Dual-region: two specific regions for redundancy
     * Multi-region: wide geographic redundancy for global access
   * Location affects where your data is physically stored and can change cost and performance.

4. Access control
   * Use Cloud IAM (recommended) for fine-grained, auditable permissions.
   * Legacy ACLs still exist but are discouraged; IAM integrates with organization policies and is easier to manage at scale.

5. Optional settings to enforce lifecycle and governance
   * Object versioning: retain previous versions for recovery from accidental deletes or overwrites.
   * Retention policies: lock data for a minimum retention period.
   * Lifecycle rules: automatically transition or delete objects (for example, move objects from Standard to Coldline after 30 days).
   * Customer-Managed Encryption Keys (CMEK): use Cloud KMS when you need to control key rotation and ownership.

Quick example — create a bucket with gcloud

* Replace placeholders with your project, bucket name, and location:

```bash theme={null}
gcloud storage buckets create gs://myproject-prod-us-central1-raw \
  --project=my-gcp-project \
  --location=us-central1 \
  --storage-class=STANDARD \
  --uniform-bucket-level-access
```

Most of these options can also be configured via the Google Cloud Console, the gcloud CLI, or infrastructure-as-code tools like Terraform.

<Frame>
  <img alt="An infographic titled &#x22;Bucket Setup — Setting Up Cloud Storage&#x22; showing a five-step staircase of steps and icons: Create Bucket, Choose Storage Class, Select Location, Configure Access, and Optional Settings. Each step includes a short instruction about naming the bucket, picking storage class and location, setting access controls, and enabling versioning/lifecycle policies." />
</Frame>

Key features that make GCS powerful

* Scalability and durability
  * GCS automatically scales to petabytes with high durability and SLA-backed availability. You don’t provision storage nodes — Google manages the infrastructure.

* Security and encryption
  * Data is encrypted in transit (TLS) and at rest by default.
  * Integrates with Cloud IAM for access control and Cloud KMS for CMEK when you need to manage encryption keys.

* Global access and performance
  * Choose the right location type to balance cost, latency, and redundancy for your application.

* Versioning and data protection
  * Object versioning preserves historical versions for accidental deletion recovery and auditability.

* Storage classes and cost optimization
  * Multiple storage classes let you align cost to access frequency. Combine storage classes with lifecycle rules to automate cost reductions over time.

* Lifecycle management
  * Define lifecycle rules to transition objects across storage classes (Standard → Coldline → Archive) or to delete objects automatically.

* GCP integrations
  * GCS integrates natively with BigQuery, Dataflow, Cloud Functions, Vertex AI, and other services to simplify data pipelines and ML workflows.

GCS is a reliable, secure, and integrated platform for storing and serving data across Google Cloud. For data engineers, it’s often the starting and persistent layer of modern data architecture.

<Frame>
  <img alt="An infographic titled &#x22;Key Features&#x22; showing colorful banner icons and short descriptions. Each banner lists cloud storage capabilities like Scalability, Strong Security, Global Access, Versioning, Storage Classes, Lifecycle Management, and GCP Integration." />
</Frame>

Next steps and references

* If you’re following along, try creating a bucket in the Console or with the gcloud example above, enable versioning, and add a lifecycle rule to transition objects after 30 days.
* Useful docs and references:
  * [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
  * [BigQuery and Cloud Storage integration](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage)
  * [Cloud KMS documentation for CMEK](https://cloud.google.com/kms/docs)
  * [Terraform Google Cloud Storage module](https://registry.terraform.io[AWS_SECRET_ACCESS_KEY]resources/storage_bucket)

This lesson prepares you to set up a GCS bucket and apply the options and settings demonstrated here.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9963c1-ef6f-4c29-94d2-1427ab43c94c/lesson/8b285410-f6a8-40eb-b767-e35b6cbb896e" />
</CardGroup>
