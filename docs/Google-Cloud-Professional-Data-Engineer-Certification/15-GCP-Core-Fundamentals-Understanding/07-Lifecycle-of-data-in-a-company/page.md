# Lifecycle of data in a company

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Core-Fundamentals-Understanding/Lifecycle-of-data-in-a-company/page

Overview of the data lifecycle in businesses covering ingestion, storage, processing, governance, monitoring, and delivery for analytics and machine learning with practical best practices.

Hello everyone — welcome back.

This lesson covers a fundamental topic that affects every business: the data lifecycle. Think of it as the circle of life for data — from the moment a customer clicks a "Buy Now" button to when that event becomes a metric on a dashboard or a feature for a machine learning model. Each stage of this lifecycle influences latency, cost, trust, and ultimately the quality of decisions.

We’ll follow the end-to-end flow: how data is ingested, stored, processed, and delivered to business platforms — all under the umbrella of governance, monitoring, and quality.

## Ingesting data

Ingestion is the entry point where raw data enters your systems. Typical sources include web and mobile activity, IoT sensor streams, transactional systems, and third-party feeds.

Two common ingestion patterns:

| Pattern               | Characteristics                                                                                                                                 | When to use                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Streaming (real-time) | Continuous, low-latency delivery. Examples: [Apache Kafka](https://kafka.apache.org/), [Google Cloud Pub/Sub](https://cloud.google.com/pubsub). | Real-time analytics, alerting, personalization, fraud detection.        |
| Batch                 | Collected into discrete jobs run at intervals (e.g., hourly, nightly).                                                                          | Periodic ETL, large-volume historical loads, cost-efficient processing. |

Design trade-offs at this stage affect system complexity, cost, and timeliness of insights. Consider throughput, retention, ordering, and exactly-once vs at-least-once semantics when selecting an ingestion strategy.

## Storing data

After ingestion, persist data in systems designed for durability, discoverability, and appropriate access patterns:

| Storage type                 | Purpose                                       | Examples / Notes                                                                           |
| ---------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Operational databases (OLTP) | Transactional workloads and fast lookups      | Use for user profiles, orders, inventory.                                                  |
| Data warehouses (OLAP)       | Analytical queries, reporting, BI             | e.g., BigQuery, Snowflake — structured, columnar storage for fast aggregations.            |
| Object stores                | Large, unstructured assets and raw event logs | e.g., `Amazon S3`, `Google Cloud Storage` — ideal for landing zones and data lake storage. |

Apply schema design, partitioning, and lifecycle policies (retention, tiering) so downstream consumers can efficiently find and process the data.

## Processing data

Processing transforms raw streams and files into reliable datasets for analytics and ML:

* Cleaning: remove corrupt records, normalize formats, deduplicate.
* Enrichment: join lookup tables (user attributes, product catalogs) and add derived fields.
* Transformation: aggregations, filtering, reshaping (wide → narrow), and feature engineering for ML.
* Validation: schema checks, completeness checks, and anomaly detection to catch issues early.

Quality gates and automated tests here reduce the cost of fixing problems later (garbage-in → garbage-out prevention).

## Connecting data to business platforms

Processed data is consumed by multiple platforms, each with different shape and freshness requirements:

* Data analysis: ad hoc queries for discovery and hypothesis testing.
* Data visualization: dashboards/reports for business users and leadership (e.g., [Looker](https://cloud.google.com/looker), [Tableau](https://www.tableau.com/), [Looker Studio](https://lookerstudio.google.com/)).
* Machine learning: training datasets and serving features for models (recommendation, forecasting, anomaly detection).

Common pipeline pattern: produce multiple layers — raw (immutable), curated (cleaned/enriched), and consumption-ready (denormalized/aggregated). This enables reuse and reduces rework.

## Data governance (the umbrella)

Governance ensures that data is secure, compliant, and trustworthy across the entire lifecycle:

* Access controls and encryption: prevent unauthorized access and data leaks.
* Lineage and metadata: trace data provenance and transformations for auditability.
* Policies: retention, masking, and privacy controls aligned with regulations.
* Monitoring and observability: pipeline health, SLA alerts, and data-quality dashboards.

Governance isn’t a one-time step — it’s applied across ingestion, storage, processing, and consumption so business decisions rely on trusted data.

<Callout icon="lightbulb">
  Apply automated quality checks and monitoring early in the pipeline. It’s far cheaper to detect and fix data issues during processing than to debug problems after they appear in production dashboards or models.
</Callout>

## Best practices (summary)

* Define clear SLAs for freshness and availability per use case.
* Instrument pipelines with metrics: latency, throughput, error rates.
* Use immutable raw stores for reproducibility and replayability.
* Maintain a canonical metadata catalog and record lineage for auditability.
* Tailor storage formats and partitioning to query patterns (e.g., columnar formats for analytics).

## Recap

* Data typically flows: ingestion → storage → processing → consumption (analytics, visualization, ML).
* Governance, monitoring, and automated quality checks should span the entire lifecycle to ensure reliable, compliant insights.
* Choose the right ingestion pattern and storage architecture based on latency, cost, and access requirements.

We’ll also discuss how Google Cloud’s global infrastructure maps to these use cases in upcoming lessons and how its managed services can simplify many lifecycle aspects.

<Frame>
  <img alt="A flowchart titled &#x22;Data Lifecycle in a Business Environment&#x22; showing data moving from &#x22;Ingest Data&#x22; to &#x22;Store Data&#x22; to &#x22;Process Data&#x22; inside a &#x22;Data Governance&#x22; boundary. The processed data then feeds platforms for data analysis, visualization, and machine learning." />
</Frame>

That’s it for this lesson — see you in the next one!

## Links and references

* [Apache Kafka](https://kafka.apache.org/)
* [Google Cloud Pub/Sub](https://cloud.google.com/pubsub)
* [Google Cloud Storage](https://cloud.google.com/storage)
* [Amazon S3](https://aws.amazon.com/s3/)
* [Looker](https://cloud.google.com/looker)
* [Tableau](https://www.tableau.com/)
* [Looker Studio](https://lookerstudio.google.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/54d4f17c-56da-41a4-b998-2a2c63f0ee3f/lesson/c8f3fece-162a-40f0-8d77-04667ac6bc4b" />
</CardGroup>
