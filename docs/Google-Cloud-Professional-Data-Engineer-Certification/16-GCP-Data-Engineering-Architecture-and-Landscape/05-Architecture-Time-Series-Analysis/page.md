# Architecture Time Series Analysis

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Data-Engineering-Architecture-and-Landscape/Architecture-Time-Series-Analysis/page

A GCP architecture guide for ingesting, processing, storing, and analyzing time series data using Pub/Sub, Cloud Storage, Dataflow, Bigtable, and BigQuery

Hello and welcome.

This article walks through a time-series analysis architecture on Google Cloud Platform, explaining why each service is chosen and how the pieces fit together. As you read, keep asking: does this design match the use case, scale, latency, and operational constraints?

## Use case and ingestion

* Use case: internal time-series analysis (monitoring, IoT, metrics, financial ticks, etc.).
* Ingestion patterns: both streaming (near real-time) and batch (file-based) data arrive into the system.

For streaming ingestion, Cloud Pub/Sub is a natural fit: it offers durable, distributed messaging with low latency and at-least-once delivery semantics. For file-based batch ingestion, Cloud Storage is typically the initial landing zone for raw time-series files (CSV, Parquet, JSONL).

Recommended reading:

* [Cloud Pub/Sub](https://cloud.google.com/pubsub/docs/overview)
* [Cloud Storage](https://cloud.google.com/storage/docs/overview)

## Storage choice: Cloud Storage vs Cloud Bigtable

Choosing between Cloud Storage and Cloud Bigtable depends on access patterns, latency requirements, and operational goals.

| Characteristic |                                               Cloud Storage |                                                              Cloud Bigtable |
| -------------- | ----------------------------------------------------------: | --------------------------------------------------------------------------: |
| Best for       |            Cost-effective archival and batch file workflows |             High-throughput, low-latency row lookups and point reads/writes |
| Access pattern |                              File-level and bulk processing |             Time-series row or windowed queries with well-designed row keys |
| Latency        |                                    Seconds (batch-oriented) |                                         Sub-millisecond to low milliseconds |
| Integration    |                  Easy with Dataflow, Dataproc, Data Catalog |         Excellent for OLTP-like time-series workloads and real-time lookups |
| When to choose | Start here when ingesting files and running batch pipelines | Move here when you require low-latency, high QPS access to time-series rows |

<Callout icon="lightbulb">
  Start with Cloud Storage for raw/batch files to reduce cost and complexity. Adopt Cloud Bigtable when your workload demands low-latency point reads/writes, sustained high throughput, and you can design efficient row keys for time-window access patterns.
</Callout>

<Callout icon="warning">
  If you choose Cloud Bigtable, plan your row-key carefully. Poor row-key design can lead to hotspotting and degraded performance for time-series workloads.
</Callout>

## Processing layer

This architecture uses Cloud Dataflow (Apache Beam) for unified stream and batch processing. Dataflow is a serverless, managed service providing autoscaling, windowing, session handling, and built-in connectors to Pub/Sub, Cloud Storage, BigQuery, and Bigtable.

When to consider alternatives:

* Use Dataproc (Spark) if you have existing Spark jobs or need specific Spark libraries, notebooks, or custom cluster management.
* Prefer Dataflow when you want a unified programming model for streaming and batch with minimal operational overhead.

Reference:

* [Cloud Dataflow](https://cloud.google.com/dataflow/docs/overview)
* [Apache Beam programming model](https://beam.apache.org/documentation/)

## Outputs and downstream analysis

Processed outputs typically flow to one or more destinations depending on query patterns and downstream consumers:

* Cloud Storage — store raw, windowed, or aggregated files; archive snapshots and large batch outputs.
* Cloud Bigtable — store time-series rows for sub-millisecond lookups and high-throughput point queries.
* BigQuery — store denormalized or aggregated tables for interactive, ad-hoc analytics and reporting.

These stores then feed ML and analytics tools:

* Vertex AI / Cloud AI for model training and serving.
* Dataproc (Spark) for specialized heavy analytics or legacy Spark workloads.
* Notebooks and notebook services for experimentation and exploratory analysis.

Useful links:

* [BigQuery](https://cloud.google.com/bigquery/docs)
* [Vertex AI](https://cloud.google.com/vertex-ai)
* [Dataproc](https://cloud.google.com/dataproc/docs)

<Frame>
  <img alt="A Google Cloud Platform architecture diagram for time series analysis showing batch (Cloud Storage) and streaming (Pub/Sub) inputs feeding a Time Series Processing step (Cloud Dataflow). Processed data flows to storage services (BigQuery, Bigtable, Cloud Storage) and to ML/processing/analysis tools (Cloud ML, Cloud Dataproc, Cloud Datalab)." />
</Frame>

## How to think about service selection

When evaluating components ask:

* Which service minimizes operational burden while meeting functional needs?
* Which service will provide the required features at scale and over time?
* Do we need serverless autoscaling and unified semantics (Dataflow), or specific Spark features (Dataproc)?
* Are low-latency point reads required (Bigtable) or are batch/analytical queries more important (BigQuery/Cloud Storage)?

Quick decision checklist:

1. Start: Ingest files to Cloud Storage, streams to Pub/Sub, process with Dataflow.
2. If you need interactive analytics and SQL, push aggregates to BigQuery.
3. If you need low-latency, high-throughput row access, move processed time-series rows to Bigtable.
4. For specialized Spark work or migration, use Dataproc.

Further reading and certification resources:

* [Google Cloud Professional Data Engineer certification course](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification)
* [Google Cloud product docs](https://cloud.google.com/docs)

That is it for this article.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/1330181a-1f1c-4747-9f22-fdae21dfdf2e/lesson/f0c68e45-ba6e-4e04-9420-b426eeceb782" />
</CardGroup>
