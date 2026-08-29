# Architecture Real Time Stream Processing IoT

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Data-Engineering-Architecture-and-Landscape/Architecture-Real-Time-Stream-Processing-IoT/page

Production-ready architecture for real-time IoT telemetry ingestion, stream processing, storage, analytics, and presentation on Google Cloud Platform using Pub/Sub, Dataflow, BigQuery, Bigtable, and Firestore.

Welcome back. This lesson describes a production-ready architecture for real-time IoT stream processing on Google Cloud Platform (GCP). The example company, Smart Home Analytics, manufactures smart lights, speakers, thermostats, and cameras that continuously emit telemetry (temperature, energy usage, user interactions, and error/status events). The architecture below shows how to ingest, process, store, and analyze that telemetry with minimal latency and high reliability.

Below we walk through the end-to-end architecture block by block, focusing on design choices, recommended services, and operational considerations.

## Devices and Gateways

* Devices fall into two broad categories:
  * Constrained devices: low-power, resource-limited devices (BLE sensors, microcontrollers). These typically rely on a local gateway to aggregate telemetry and perform protocol translation.
  * Standard devices: more capable devices (smart hubs, cameras) that can communicate directly to the cloud using MQTT, HTTP, or HTTPS.
* Gateway responsibilities:
  * Local aggregation and buffering to handle intermittent connectivity.
  * Device authentication and authorization.
  * Protocol translation (CoAP, BLE, custom protocols → MQTT/HTTP).
  * Reliable forwarding to cloud ingestion with retry/backoff and ordering guarantees as required.

## Ingestion

* Cloud Pub/Sub is the primary messaging layer for high-throughput, durable ingestion. Pub/Sub supports topics and subscriptions, push/pull delivery, and at-least-once delivery semantics, so downstream consumers must be designed for idempotency or deduplication.
* Use Cloud Monitoring and Cloud Logging to capture operational metrics and logs across gateways, ingestion, and processing layers for alerting and incident investigation.

Best practices:

* Partition topics by logical device groups or geographic region to scale consumers independently.
* Set message retention and dead-letter topics for problematic messages.
* Use batching and compression for cost efficiency when forwarding from gateways.

## Processing (Stream Pipeline)

* Use Cloud Dataflow (Apache Beam) for real-time stream processing:
  * Support for windowing (fixed, sliding, session windows) and triggers to handle late-arriving data.
  * Aggregations (e.g., rolling averages, percentiles).
  * Enrichment by joining with device metadata or configuration stores.
  * Stateful processing and timers for complex event detection (e.g., multi-sensor correlation, anomaly windows).
* Typical real-time tasks:
  * Filtering and transformation into analytics-friendly formats.
  * Anomaly detection and alert generation.
  * Sessionization (per-device activity windows).
  * Generating materialized views or pre-aggregated results for downstream queries.

Operational notes:

* Tune autoscaling and worker disk/CPU based on event size and state requirements.
* Use job monitoring, metrics, and backlog alerts to detect processing lag early.

## Storage

Choose storage based on access patterns (point reads, time-series queries, analytical scans, or cold archival):

| Storage type                | Use case                                                              | Example                                               |
| --------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------- |
| Object storage              | Raw event dumps, archival, and replay                                 | [Cloud Storage](https://cloud.google.com/storage)     |
| NoSQL transactional         | Device metadata, configuration, low-latency reads/writes              | [Cloud Firestore](https://cloud.google.com/firestore) |
| High-throughput time-series | Massive time-series sensor readings with fast point and range queries | [Cloud Bigtable](https://cloud.google.com/bigtable)   |
| Analytics warehouse         | Large-scale ad hoc SQL analytics and BI                               | [BigQuery](https://cloud.google.com/bigquery)         |

Streaming vs batch ingestion into BigQuery:

* Use streaming inserts for low-latency analytics (costly at scale).
* Use micro-batch loads from Cloud Storage for cost-effective bulk ingestion and replay.

## Analytics and Batch Processing

* BigQuery is the primary engine for large-scale historical analysis and ad hoc queries.
* Dataproc provides managed Spark/Hadoop clusters for custom ETL, heavy transformations, or model training.
* Interactive exploration and model development can be performed with Vertex AI Workbench (managed notebooks).

## Presentation and Applications

Processed and aggregated results feed user-facing services and dashboards:

* App hosting: App Engine for PaaS or GKE for containerized microservices; use Compute Engine for specialized workloads.
* Dashboards and BI: Looker or Looker Studio for visualization and embedded analytics.
* APIs: Expose aggregated data and alerts to mobile/web clients or partner systems.

## End-to-end flow summary

1. Devices (constrained or standard) → local Gateway (optional) → Ingestion with Cloud Pub/Sub.
2. Monitoring and logging collect operational telemetry with Cloud Monitoring and Cloud Logging.
3. Stream processing (Cloud Dataflow / Apache Beam) performs windowing, aggregation, enrichment, and anomaly detection.
4. Processed data is persisted to the appropriate stores: Cloud Storage, Cloud Bigtable, Cloud Firestore, and/or BigQuery.
5. Analytics engines (BigQuery, Dataproc) and notebooks are used for exploration, BI, and model training.
6. Results power applications hosted on App Engine, GKE, or Compute Engine and dashboards (Looker / Looker Studio).

<Frame>
  <img alt="A Google Cloud Platform architecture diagram for real-time IoT stream processing, showing constrained and standard devices sending data through a gateway into ingest services (Cloud Pub/Sub, monitoring, logging) and pipelines (Cloud Dataflow). The data flows into storage and analytics components (Cloud Storage, Datastore, Bigtable, BigQuery, Dataproc, Datalab) and then to application/presentation layers (App Engine, Kubernetes Engine, Compute Engine)." />
</Frame>

<Callout icon="lightbulb">
  When designing for real-time IoT streams, ensure idempotency or deduplication in downstream consumers because Pub/Sub provides at-least-once delivery. Also pick the storage option according to access patterns: Bigtable for high-throughput time-series access, BigQuery for analytical queries, and Cloud Storage for raw archival.
</Callout>

## Links and references

* [Cloud Pub/Sub](https://cloud.google.com/pubsub) — scalable messaging for ingestion
* [Cloud Dataflow](https://cloud.google.com/dataflow) & [Apache Beam](https://beam.apache.org) — stream processing model and managed runner
* [Cloud Storage](https://cloud.google.com/storage) — object storage for raw and archival data
* [Cloud Bigtable](https://cloud.google.com/bigtable) — high-throughput time-series store
* [Cloud Firestore](https://cloud.google.com/firestore) — low-latency metadata store
* [BigQuery](https://cloud.google.com/bigquery) — analytics data warehouse
* [Cloud Monitoring](https://cloud.google.com/monitoring) and [Cloud Logging](https://cloud.google.com/logging) — operational visibility
* [Dataproc](https://cloud.google.com/dataproc) — managed Spark/Hadoop clusters
* [Vertex AI Workbench](https://cloud.google.com/vertex-ai/docs/workbench) — managed notebooks for ML and exploration
* [App Engine](https://cloud.google.com/appengine), [GKE](https://cloud.google.com/kubernetes-engine), [Compute Engine](https://cloud.google.com/compute) — hosting options

That is it for this lesson. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/1330181a-1f1c-4747-9f22-fdae21dfdf2e/lesson/1aa0c4b6-e742-4c47-acd1-e4f97b1fbfc9" />
</CardGroup>
