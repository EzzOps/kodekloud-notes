# GCS Storage Class Lifecycle Rules Versioning and Retention

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Storage-Options/GCS-Storage-Class-Lifecycle-Rules-Versioning-and-Retention/page

Overview of Google Cloud Storage features including storage classes, lifecycle rules, object versioning, retention policies and retention lock to optimize costs and protect data.

Welcome back. In this lesson we cover essential Google Cloud Storage (GCS) features that help you optimize costs, automate data lifecycle, and protect objects from accidental or permanent deletion. We'll walk through storage classes, lifecycle rules, versioning, retention policies, and retention lock — with practical examples and operational tips.

## Storage classes: pick the right tier for access patterns and cost

Storage classes define access characteristics, availability, and cost for objects in a bucket. All GCS classes offer the same durability; differences are in access frequency, minimum storage durations, and pricing.

| Storage Class |               Typical access frequency | Minimum storage duration | Typical use cases                                  |
| ------------- | -------------------------------------: | -----------------------: | -------------------------------------------------- |
| Standard      | Frequent (daily or multiple times/day) |                     None | Active datasets, hot data, frequently-read objects |
| Nearline      |                   Infrequent (monthly) |                  30 days | Backups, archive-you-still-access-occasionally     |
| Coldline      |                       Rare (quarterly) |                  90 days | Long-term backup, disaster recovery                |
| Archive       | Very infrequent (yearly or for audits) |                 365 days | Compliance archives, regulatory records            |

As access frequency decreases (Standard → Nearline → Coldline → Archive), storage cost per GB typically decreases while minimum retention commitments increase. Deleting or changing storage class before the minimum storage duration can result in early deletion or reclassification charges equivalent to the remaining minimum period.

> **lightbulb** Durability is the same across all GCS storage classes. Choose a class based on access frequency, availability SLAs, and cost — not durability.

## Lifecycle rules: automate transitions and deletions

Lifecycle rules let GCS automatically move objects between storage classes or delete objects (including noncurrent versions) based on conditions. This helps reduce storage costs and enforce data retention without manual intervention.

Common lifecycle conditions:

* `age`: move/delete objects older than N days
* `createdBefore`: apply to objects created before a date
* `matchesStorageClass`: target objects in a specific storage class
* `isLive` / `numNewerVersions`: distinguish live objects vs. noncurrent versions
* `matchesPrefix` / `matchesSuffix`: filter by object name patterns

Example scenario:

* Application logs are written to `Standard`.
* After 30 days, transition to `Nearline`.
* After 90 days, transition to `Coldline`.
* After 365 days, delete the logs.

Example lifecycle configuration (JSON) to transition objects by age and then delete:

```json theme={null}
{
  "rule": [
    {
      "action": { "type": "SetStorageClass", "storageClass": "NEARLINE" },
      "condition": { "age": 30 }
    },
    {
      "action": { "type": "SetStorageClass", "storageClass": "COLDLINE" },
      "condition": { "age": 90 }
    },
    {
      "action": { "type": "Delete" },
      "condition": { "age": 365 }
    }
  ]
}
```

You can combine multiple conditions (for example, only noncurrent versions older than N days or objects matching a prefix). GCS evaluates lifecycle rules and executes any applicable actions automatically.

## Versioning, retention policies, and retention lock — protecting data

These features protect data from accidental or intentional loss and help meet regulatory requirements.

### Object versioning

* When enabled, GCS retains older generations of an object when it is overwritten or deleted.
* Useful for recovery after accidental overwrite or deletion.
* Increases storage usage and cost because older generations are retained until deleted or managed via lifecycle rules.

Enable versioning with gsutil:

```bash theme={null}
gsutil versioning set on gs://YOUR_BUCKET_NAME
```

### Retention policies

* A bucket-level retention policy enforces a minimum object age: objects cannot be deleted or overwritten until this period elapses.
* Useful for compliance (e.g., financial or audit records).
* You can set or remove a retention policy unless it has been locked.

Set a retention period with gsutil:

```bash theme={null}
gsutil retention set 365d gs://YOUR_BUCKET_NAME
```

### Retention lock (Bucket Lock)

* Locking a retention policy makes it immutable and irreversible.
* Once locked, you cannot shorten or remove the retention period, even with administrative privileges.
* Use retention lock only when you are certain you need an immutable retention policy for legal or regulatory reasons.

> **warning** Retention lock is irreversible. After locking a bucket's retention policy, the policy and its duration cannot be changed or removed. Confirm requirements before applying a lock.

## Operational tips and best practices

* Combine versioning with lifecycle rules to automatically remove noncurrent versions after a retention window or transition them to cheaper storage classes.
* Consider minimum storage durations for Nearline, Coldline, and Archive: changing storage class or deleting objects before the minimum can incur early deletion charges.
* Define lifecycle rules in the Cloud Console, via `gsutil` lifecycle commands, or by uploading a JSON lifecycle configuration.
* For regulatory compliance, prefer bucket retention policies (and retention lock when required) over manual retention practices.
* Test lifecycle and retention settings in a nonproduction bucket first to validate behavior and cost impact.

## Quick summary

* Choose the appropriate storage class based on expected access patterns and retention needs.
* Use lifecycle rules to automate transitions and deletions to lower costs.
* Enable object versioning to protect against accidental overwrite/delete and manage retained versions with lifecycle rules.
* Use retention policies and retention lock to enforce legal or regulatory retention requirements.

## Links and references

* [Google Cloud Storage: Overview](https://cloud.google.com/storage/docs/overview)
* [GCS Lifecycle Management](https://cloud.google.com/storage/docs/lifecycle)
* [GCS Object Versioning](https://cloud.google.com/storage/docs/object-versioning)
* [Bucket Lock (Retention Policy)](https://cloud.google.com/storage/docs/bucket-lock)

That concludes this lesson — see you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9963c1-ef6f-4c29-94d2-1427ab43c94c/lesson/e3069887-9b69-4ea5-ae96-982b51e343d1)
