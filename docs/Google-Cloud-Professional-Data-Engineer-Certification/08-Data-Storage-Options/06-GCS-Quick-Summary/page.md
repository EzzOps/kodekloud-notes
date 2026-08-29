# GCS Quick Summary

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Storage-Options/GCS-Quick-Summary/page

Concise guide to Google Cloud Storage fundamentals including objects and buckets, storage classes, locations, lifecycle management, versioning and retention, security controls, and common commands

Welcome back.

Previously we reviewed GCS availability and failover strategies — how Google Cloud Storage keeps data available during regional outages. This lesson is a concise, practical summary of the core Google Cloud Storage (GCS) concepts you’ll encounter in real implementations and on the GCP exam. We cover objects & buckets, storage classes, locations & availability, lifecycle management, versioning & retention, and security controls.

Let’s get started.

## Objects and Buckets

* Objects are the basic data unit in GCS. Each object contains file data plus metadata such as content type, size, creation time, generation, and ACLs/attributes.
* Buckets are top-level containers for objects. Bucket names are globally unique across Google Cloud — two buckets in different projects cannot share the same name.
* Each bucket has two important settings that affect cost, latency, and durability:
  * Location (regional, dual-region, multi-region)
  * Storage class (Standard, Nearline, Coldline, Archive)

> **lightbulb** Bucket names are globally unique. Choose names intentionally (for example, include a project or org prefix) to avoid collisions.

Practical tips:

* Use project or organization prefixes in bucket names to avoid naming collisions and make ownership obvious.
* Keep metadata and meaningful object naming conventions to simplify lifecycle rules and analytics.

## Storage Classes

GCS provides four primary storage classes optimized for different access patterns and cost trade-offs. The table below summarizes use cases, cost characteristics, and minimum storage durations.

| Storage class | Use case                                                             | Cost profile                                                      | Minimum storage duration |
| ------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------ |
| Standard      | Frequently accessed data (web assets, active logs, application data) | Higher storage cost but lowest per-operation cost and latency     | None                     |
| Nearline      | Infrequently accessed (monthly access)                               | Lower storage cost than Standard, higher retrieval/operation cost | 30 days                  |
| Coldline      | Rarely accessed (quarterly access)                                   | Lower storage cost than Nearline, higher retrieval costs          | 90 days                  |
| Archive       | Very rare access (yearly/less)                                       | Lowest storage cost, highest retrieval cost and latency           | 365 days                 |

Exam tip: for datasets accessed \~once per year, Archive is usually the best fit.

## Location and Availability

Choose bucket location according to latency, availability, and compliance requirements:

| Location type | Description                                                                     | Best for                                                               |
| ------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Regional      | Data stored in a single Google Cloud region                                     | Low latency for regional apps; lower egress cost within region         |
| Dual-region   | Data stored in two specified regions (you choose the pair)                      | Higher availability and resilience, regional compliance controls       |
| Multi-region  | Data spread across multiple regions within a continent (or global multi-region) | Maximum availability and durability for globally distributed workloads |

Decision factors:

* Latency: pick the region(s) closest to your consumers.
* Durability/Availability: dual-region or multi-region increases resilience.
* Cost/compliance: regional storage can reduce cost and help satisfy data residency requirements.

## Lifecycle Management

Lifecycle rules automate object transitions (to cheaper storage classes) and deletions based on conditions like object age, storage class, or custom time. Use lifecycle policies to optimize long-term storage cost without manual intervention.

Example lifecycle rule: move objects to Nearline after 30 days

```json theme={null}
{
  "rule": [
    {
      "action": { "type": "SetStorageClass", "storageClass": "NEARLINE" },
      "condition": { "age": 30 }
    }
  ]
}
```

Common lifecycle actions:

* Transition objects to cheaper storage classes (`SetStorageClass`).
* Delete objects automatically after a condition is met (`Delete`).
* Use `matchesStorageClass`, `isLive`, `createdBefore`, `numNewerVersions`, or `customTimeBefore` conditions to target objects precisely.

Commands:

* Apply lifecycle via the Cloud Console, `gsutil` with bucket configuration, or the Storage API.

## Versioning and Retention

* Versioning: Enable object versioning on a bucket to retain older object generations after overwrite or deletion. This protects against accidental deletes or overwrites.
  * Example: enable versioning with gsutil
    ```bash theme={null}
    gsutil versioning set on gs://YOUR_BUCKET_NAME
    ```
* Retention policies: Apply an immutable retention period to a bucket to prevent object deletion or modification for a specified duration.
  * Example: set a 365-day retention policy
    ```bash theme={null}
    gsutil retention set 365d gs://YOUR_BUCKET_NAME
    ```
* Bucket Lock: After you lock a retention policy, it becomes permanent and cannot be shortened — enforcing WORM (write once, read many) behavior for compliance.

Retention policies and versioning together create strong protection and help meet regulatory requirements.

> **warning** Be careful: enabling Bucket Lock to permanently enforce retention policies is irreversible. Confirm retention requirements before locking.

## Security and Access Control

Encryption:

* Data is encrypted in transit and at rest by default.
* Customer-Managed Encryption Keys (CMEK): Use Cloud KMS keys you control to encrypt buckets or objects while Google manages key wrapping.
* Customer-Supplied Encryption Keys (CSEK): You supply encryption keys with each request; GCS does not store them. Use CSEK only if you can securely manage and supply the keys.

Access control:

* IAM (recommended): Use role-based IAM policies to manage bucket and object access at scale.
* Uniform bucket-level access (recommended): Disable object ACLs and rely exclusively on IAM for simpler, auditable access policies.
* Fine-grained ACLs: Still available for legacy scenarios but are more complex and error-prone.

Temporary access:

* Signed URLs and Signed Policy Documents let you grant time-limited access to objects without modifying IAM policies.

Choose between GCP-managed keys, CMEK, or CSEK based on compliance, auditability, and your key-management capabilities.

## Quick Commands and Examples

| Action                | Example                                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| Create a bucket       | `gsutil mb -l us-central1 gs://my-project-bucket`                                                          |
| Enable versioning     | `gsutil versioning set on gs://my-project-bucket`                                                          |
| Set retention         | `gsutil retention set 30d gs://my-project-bucket`                                                          |
| Make bucket uniform   | `gsutil iam ch allUsers:legacyBucketReader gs://my-project-bucket` (use IAM for consistent access control) |
| Generate a signed URL | Use `gsutil signurl` or Storage API for programmatic signed URLs                                           |

Note: Replace `my-project-bucket` and `us-central1` with your actual bucket name and region. Wrap placeholders like `<BUCKET_NAME>` or `<KEY>` in backticks when using them inline.

## Summary

Key takeaways for Google Cloud Storage:

* Objects are the data units; buckets are globally unique containers with configurable location and storage class.
* Choose the right storage class (Standard, Nearline, Coldline, Archive) based on access patterns and cost.
* Select the appropriate location type (regional, dual-region, multi-region) for latency, availability, and compliance.
* Use lifecycle rules to automate storage class transitions and deletions to reduce costs.
* Combine versioning, retention policies, and Bucket Lock to protect data and meet compliance requirements.
* Secure data with encryption (CMEK/CSEK options), IAM-based access controls, uniform bucket-level access, and temporary signed URLs.

GCS is a foundational component for durability, cost optimization, and secure data management in cloud-native architectures.

See you in the next lesson.

## Links and References

* [Google Cloud Storage documentation](https://cloud.google.com/storage/docs)
* [Cloud KMS documentation (CMEK)](https://cloud.google.com/kms/docs)
* [Signed URLs guide](https://cloud.google.com/storage/docs/access-control/signed-urls)
* [Lifecycle management guide](https://cloud.google.com/storage/docs/lifecycle)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9963c1-ef6f-4c29-94d2-1427ab43c94c/lesson/21450887-8657-4809-bb3a-add65216a985)
