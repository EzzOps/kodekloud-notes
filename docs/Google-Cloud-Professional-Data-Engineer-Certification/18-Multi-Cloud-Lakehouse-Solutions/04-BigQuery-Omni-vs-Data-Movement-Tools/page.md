# BigQuery Omni vs Data Movement Tools

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Multi-Cloud-Lakehouse-Solutions/BigQuery-Omni-vs-Data-Movement-Tools/page

Comparison of BigQuery Omni, Storage Transfer Service, and BigQuery Data Transfer Service to help data engineers decide whether to query data in place or move it into Google Cloud

Welcome back.

This article answers a common operational question for data engineers: when should you use BigQuery Omni versus other Google Cloud data-movement options? The right choice depends on where your data resides, how often you need to access it, latency and egress-cost constraints, and whether you prefer to query data in place or centralize it in Google Cloud.

Think like a data engineer: pick the right tool for the right scenario. Below is a concise, practical comparison of three common approaches with guidance to help you decide quickly.

## At-a-glance summary

* BigQuery Omni
  * Best when data must remain outside Google Cloud (for example, in AWS S3 or Azure Blob Storage).
  * Runs BigQuery compute in the same cloud/region as the storage, enabling in-place SQL queries and minimizing large-scale data transfer.
  * Supports cross-cloud joins with external datasets, reducing egress costs and migration time (runtime performance depends on locality and network).
  * Maintains a consistent BigQuery SQL experience; ensure appropriate IAM and governance across clouds.
  * Docs: [https://cloud.google.com/bigquery-omni](https://cloud.google.com/bigquery-omni)

* Storage Transfer Service (STS)
  * Moves data into Google Cloud Storage (GCS).
  * Ideal for one-time migrations, bulk transfers, data-lake consolidation, backups, and discovery.
  * Use STS when you want to centralize storage or modernize by bringing data into GCP for downstream processing.
  * Docs: [https://cloud.google.com/storage-transfer](https://cloud.google.com/storage-transfer)

* BigQuery Data Transfer Service (DTS)
  * Automates and schedules ingestion from managed sources and SaaS applications (Google Ads, YouTube Analytics, many CRMs).
  * Handles recurring loads, incremental updates, and common schema-change patterns.
  * Use DTS for automated, repeatable ingestion into BigQuery.
  * Docs: [https://cloud.google.com/bigquery-transfer](https://cloud.google.com/bigquery-transfer)

<Frame>
  <img alt="A presentation slide titled &#x22;Data Transfer Options&#x22; showing three colored columns for BigQuery Omni, Storage Transfer Service, and BigQuery Data Transfer Service. Each column lists brief use cases or features (e.g., query data in-place, data migration to GCP, SaaS application data)." />
</Frame>

## Decision framework (high level)

Use the short decision flow below to pick the right tool:

* Must run analytics where the data physically resides (AWS or Azure) and cannot/must not move the data → BigQuery Omni.
* One-time bulk migration or consolidation into Google Cloud → Storage Transfer Service (or Transfer Appliance for extremely large physical transfers).
* Continuous, scheduled ingestion from SaaS or managed services into BigQuery → BigQuery Data Transfer Service.

For quick reference, here is a side-by-side comparison.

| Tool                                 | Best for                                                    | Typical pros                                                                 | Typical cons                                                                                       | Docs                                                                                     |
| ------------------------------------ | ----------------------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| BigQuery Omni                        | Cross-cloud analytics on data that must remain in AWS/Azure | Query in-place, avoids large data transfers, consistent BigQuery SQL         | Runtime depends on cloud locality; network/latency considerations; cross-cloud governance required | [https://cloud.google.com/bigquery-omni](https://cloud.google.com/bigquery-omni)         |
| Storage Transfer Service (STS)       | Bulk migration / data-lake consolidation into GCS           | Centralizes data for GCP-native processing, good for one-time or large moves | Data move costs/egress may apply; time to transfer large datasets                                  | [https://cloud.google.com/storage-transfer](https://cloud.google.com/storage-transfer)   |
| BigQuery Data Transfer Service (DTS) | Scheduled ingestion from SaaS/managed sources               | Automates recurring loads and incremental updates                            | Limited to supported sources; may need transformations after load                                  | [https://cloud.google.com/bigquery-transfer](https://cloud.google.com/bigquery-transfer) |

<Frame>
  <img alt="A slide titled &#x22;Decision Framework&#x22; showing two colored boxes that compare when to &#x22;Choose Omni for:&#x22; (cross-cloud analytics, low latency needs, egress cost concerns) versus &#x22;Choose STS/BQ DTS for:&#x22; (data consolidation, migrations, transformations)." />
</Frame>

## Examples — quick Q\&A

* Q: We need to migrate an on-premises data lake (a very large set of files) into Google Cloud. What should we choose?
  * A: Storage Transfer Service (STS). For extremely large physical datasets, consider using Transfer Appliance to move data physically, then STS or GCS to ingest into Google Cloud.

* Q: Our data will remain in AWS S3 or Azure Blob Storage and cannot be moved, but we want to run BigQuery analytics (including joins with datasets in GCP). What should we choose?
  * A: BigQuery Omni. It lets you query the external cloud storage in place. If you later choose to centralize for performance or tighter integration, use STS to migrate.

* Q: We want daily ingestion from a SaaS app (e.g., Google Ads or Salesforce) into BigQuery for reporting. What should we choose?
  * A: BigQuery Data Transfer Service. DTS schedules and automates recurring transfers from many SaaS sources and supports incremental patterns.

## Operational considerations

* Latency and runtime: Omni reduces bulk data movement but can introduce cross-cloud network latency and performance variability. STS/DTS centralization often yields lower-latency queries inside GCP.
* Costs: Evaluate egress fees, storage costs, and compute costs. Omni minimizes transfer costs but may incur cross-cloud compute and network charges.
* Governance and security: Cross-cloud IAM, encryption, and policy enforcement require careful configuration. Centralizing data in GCS simplifies applying uniform GCP policies.
* Operational overhead: DTS is low-maintenance for supported SaaS sources. STS and Omni may require more operational planning for schema management, monitoring, and error handling.

<Callout icon="lightbulb">
  When deciding among Omni, STS, and DTS, weigh latency, egress costs, governance needs, and operational overhead. Omni avoids large data moves but introduces cross-cloud runtime considerations; STS/DTS centralize data into GCP and enable tighter integration with GCP-native analytics and processing.
</Callout>

## Further reading and references

* BigQuery Omni — [https://cloud.google.com/bigquery-omni](https://cloud.google.com/bigquery-omni)
* Storage Transfer Service — [https://cloud.google.com/storage-transfer](https://cloud.google.com/storage-transfer)
* Transfer Appliance — [https://cloud.google.com/transfer-appliance](https://cloud.google.com/transfer-appliance)
* BigQuery Data Transfer Service — [https://cloud.google.com/bigquery-transfer](https://cloud.google.com/bigquery-transfer)
* BigQuery documentation — [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)

I hope this lesson clarified when to use BigQuery Omni versus Storage Transfer Service or BigQuery Data Transfer Service. Thanks for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/c354d782-20e6-4961-a282-071b52a4013d/lesson/87d8859c-8ad9-4772-a2b6-f2901cf794e3" />
</CardGroup>
