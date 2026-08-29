# Create a single-region bucket with Standard storage class
gsutil mb -p YOUR_PROJECT -l us-central1 -c STANDARD gs://gcs-demo-cloud/
```

To upload an object:

```bash theme={null}
gsutil cp index.html gs://gcs-demo-cloud/index.html
```

To set a lifecycle configuration (example JSON file `lifecycle.json`):

```json theme={null}
[
  {
    "action": { "type": "Delete" },
    "condition": { "age": 30 }
  }
]
```

Apply it:

```bash theme={null}
gsutil lifecycle set lifecycle.json gs://gcs-demo-cloud
```

## Typical GCS use cases

* Static website hosting (public frontend assets)
* Staging/landing zones for ETL and data pipelines
* Intermediate or persistent storage for data lakes
* Storing artifacts (build outputs, backups)

GCS is a flexible, low-maintenance option well-suited to these patterns and integrates tightly with BigQuery, Dataflow, and other GCP services.

## Links and references

* [Google Cloud Storage documentation](https://cloud.google.com/storage/docs)
* [gsutil tool](https://cloud.google.com/storage/docs/gsutil)
* [GCS bucket naming guidelines](https://cloud.google.com/storage/docs/naming-buckets)

That concludes this lesson on creating and configuring a GCS bucket. See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9963c1-ef6f-4c29-94d2-1427ab43c94c/lesson/0112ecf8-e75d-4d0d-b198-d2950c54d023)


# GCS Availability and Failover Strategies

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Storage-Options/GCS-Availability-and-Failover-Strategies/page

Explains GCS durability, location choices, automatic failover, strong consistency, and disaster recovery strategies including versioning and Storage Transfer Service

Hello and welcome back.

We previously explored GCS classes, lifecycle rules, versioning, and retention policies. In this lesson we shift focus to a critical operational concern: availability and failover strategies for Google Cloud Storage (GCS). As a data engineer, you must ensure that stored data remains accessible and durable even when parts of the cloud infrastructure fail. GCS provides features and location models to help you meet those goals. Below we break down the core concepts, trade-offs, and practical recommendations.

## Durability

Google Cloud Storage offers extremely high durability — 99.999999999% (eleven 9s). In practice, this means the probability of permanent object loss due to hardware failures is negligible because GCS automatically replicates data across multiple devices and locations.

> **lightbulb** Exam tip: Remember the "11 nines" durability number (99.999999999%) — it’s a key differentiator for GCS and a useful fact for architecture decisions.

## Storage location options and trade-offs

Choosing the right location type affects latency, availability, redundancy, and cost. Use the table below to compare options and decide which fits your access patterns and recovery objectives.

| Location type | Best for                                                                                                                 | Trade-offs / notes                                                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Single-region | Low-latency access from a specific region; lower storage cost                                                            | No automatic cross-region failover. If the region suffers an outage, data is unavailable until the region recovers.                             |
| Dual-region   | Applications that need higher availability across two regions with lower cross-region latency (e.g., two nearby regions) | Better availability than single-region; reduced cross-region latency for the two chosen regions.                                                |
| Multi-region  | Global read availability and reduced latency for geographically distributed users (e.g., `US`, `EU`, `ASIA`)             | Highest availability and resilience against regional outages; typically higher cost and potential higher write latencies depending on workload. |

Recommended guidance:

* Use single-region for cost-sensitive workloads with locality requirements and acceptable region-level risk.
* Use dual-region when you need higher availability and deterministic low latency between two chosen regions.
* Use multi-region for global services requiring resilient, widely distributed read access.

## Automatic failover and traffic routing

For dual-region and multi-region buckets, GCS maintains replicas across the configured locations. If a replica or one of the selected regions experiences an outage, Google Cloud routes requests to healthy replicas automatically — reads (and many types of writes) continue to work without manual intervention. This behavior provides transparent failover for most operational scenarios.

> **warning** Important: Single-region buckets do not have automatic cross-region failover. If the entire region is impacted, you must rely on manual recovery strategies (e.g., pre-configured transfers or backups) to restore access.

## Consistency guarantees

GCS provides strong consistency for object operations. That means:

* Read-after-write: After a successful upload, subsequent reads see the new object.
* Read-after-update: After an object overwrite, subsequent reads reflect the updated object.
* Immediate visibility simplifies application logic because you don’t need to handle eventual-consistency windows for common operations.

Strong consistency improves correctness for distributed applications and reduces complexity for caching and synchronization.

## Disaster recovery and backups

GCS integrates into DR strategies through built-in features and services:

* Object Versioning: Enable to retain historical versions and recover from accidental deletes or overwrites.
* Storage Transfer Service: Use the Storage Transfer Service to schedule automated, recurring copies between buckets, projects, or from other cloud providers: [https://cloud.google.com/storage-transfer](https://cloud.google.com/storage-transfer)
* Cross-location strategies: Combine dual-region/multi-region buckets with replication or scheduled copies to other regions or projects to meet your Recovery Time Objectives (RTOs) and Recovery Point Objectives (RPOs).
* Lifecycle rules: Use lifecycle policies to transition older data to cheaper storage classes or to automatically delete old versions while maintaining an appropriate retention window.

Example backup approach (conceptual):

* Enable versioning on your critical production bucket.
* Configure a scheduled Storage Transfer job to copy daily snapshots to a bucket in another region or a separate project.
* Apply lifecycle rules on the backup bucket to transition older snapshots to colder storage classes (e.g., Nearline/Coldline/Archive) to control cost.

Mapping DR choices to objectives:

| Goal                                  | Recommended features                                                    |
| ------------------------------------- | ----------------------------------------------------------------------- |
| Minimize data loss (RPO ≈ 0)          | Versioning + frequent Storage Transfer jobs or multi/dual-region design |
| Minimize downtime (low RTO)           | Dual-region or multi-region buckets with automatic failover             |
| Minimize cost for long-term retention | Lifecycle rules to transition older versions to Coldline/Archive        |

## Practical considerations

* Security and access controls travel with the bucket; ensure IAM policies and encryption keys are managed consistently across backup locations.
* Test your DR runbooks periodically (perform an actual failover and restore test).
* Monitor storage usage, transfer costs, and data transfer latency to balance cost vs. availability.
* Consider network egress and transfer costs when designing cross-region backups.

## Summary

Google Cloud Storage is built for resilient, durable storage and supports multiple architectural patterns for availability and failover:

* Durability: 99.999999999% (11 nines).
* Location options: Single-region, Dual-region, Multi-region — choose based on latency, cost, and availability needs.
* Automatic failover: Available for dual-region and multi-region configurations; not available for single-region buckets.
* Consistency: Strong consistency for reads after writes and updates.
* Disaster recovery: Use versioning, Storage Transfer Service, and lifecycle policies to implement backup and recovery strategies that meet your RTO and RPO.

<Frame>
  <img alt="An infographic titled &#x22;Building Resilient Data Infrastructure&#x22; showing five colored arrows merging into a &#x22;Robust Data Storage&#x22; endpoint. Each arrow is labeled with features like High Durability, Storage Location Options, Automatic Failover, Consistency Guarantees, and Disaster Recovery." />
</Frame>

That concludes this lesson on GCS availability and failover strategies. For next steps, review the Google Cloud Storage documentation and Storage Transfer Service guides to design and validate your production DR plan:

* Google Cloud Storage docs: [https://cloud.google.com/storage](https://cloud.google.com/storage)
* Storage Transfer Service docs: [https://cloud.google.com/storage-transfer](https://cloud.google.com/storage-transfer)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/9b9963c1-ef6f-4c29-94d2-1427ab43c94c/lesson/bc613ab1-ec48-470b-97fa-43cdf8f60d96)
