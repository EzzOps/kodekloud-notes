# GCP Data Engineering Landscape

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/GCP-Data-Engineering-Architecture-and-Landscape/GCP-Data-Engineering-Landscape/page

Overview of Google Cloud data engineering landscape, mapping services to ingestion, storage, processing, orchestration, and monitoring with guidance on choosing tools for production data platforms.

Hello and welcome back.

This guide explains the Google Cloud Platform (GCP) data engineering landscape — the common services, how they fit together, and when to choose each. After reading, you should be able to glance at any GCP service and quickly tell whether it belongs to ingestion, storage, transformation, streaming, orchestration, or monitoring.

Let's get started.

## High-level view

A production-grade GCP data platform is typically organized into these layers:

* Ingestion and streaming: capturing data from devices, apps, and logs.
* Storage and databases: short- and long-term storage with different latency and consistency characteristics.
* Transformation and processing: batch and stream analytics, ETL/ELT.
* Orchestration and integration: scheduling, pipelines, and visual ETL.
* Monitoring and operations: observability, security, and developer tooling.

We’ll walk each layer and highlight the GCP services commonly used in production platforms.

## Ingestion and streaming

Use these services to collect events, telemetry, and messages in real time or near-real time:

* Pub/Sub — A globally distributed messaging bus for ingesting events from IoT devices, mobile/web apps, and logs. Ideal for decoupling producers and consumers.
* Cloud Storage — Frequently used as a durable landing zone for batch uploads, logs, and bulk files (CSV, JSON, Parquet).
* Data Transfer Service / Transfer Appliance — For large, periodic data transfers from on-premises systems or third-party sources.

> **lightbulb** For streaming-first architectures, pair Pub/Sub with a stream processor such as Dataflow to apply windowing, enrichment, and exactly-once semantics before loading into BigQuery or other sinks.

## Transformation and processing (analytics)

These services cover interactive SQL analytics, batch and stream compute, and visual data preparation:

* BigQuery — Serverless, highly scalable data warehouse for fast SQL analytics on petabyte-scale datasets.
* Dataflow — Managed Apache Beam runner for unified batch and streaming pipelines (ETL, event processing, windowing).
* Dataproc — Managed Hadoop / Spark clusters for lift-and-shift or custom Spark jobs.
* Dataprep — Visual, no-code/low-code data cleaning and preparation built for analysts and data engineers.
* Data Fusion — Visual, drag-and-drop ETL/ELT for building integration pipelines that can run on-prem or in the cloud.
* Data Catalog — Metadata management and discovery service to catalog datasets, schemas, and lineage.

When selecting a processing engine, consider latency needs (stream vs batch), operational overhead, and the required ecosystem (Beam vs Spark).

## Databases and storage

Choose storage based on access patterns, consistency, and scale. The table below summarizes the primary GCP storage and database options:

| Resource Type      | Use Case                                              | Example                                     |
| ------------------ | ----------------------------------------------------- | ------------------------------------------- |
| Wide-column NoSQL  | Low-latency, high-throughput time-series or telemetry | `Bigtable`                                  |
| Document DB        | Mobile/web apps requiring realtime sync               | `Datastore / Firestore`                     |
| Managed relational | OLTP and transactional workloads                      | `Cloud SQL (MySQL, PostgreSQL, SQL Server)` |
| Global relational  | Strong consistency and horizontal scale               | `Spanner`                                   |
| In-memory cache    | Low-latency lookups, session stores                   | `Memorystore (Redis, Memcached)`            |
| Object storage     | Raw landing zone for files, backups, ETL staging      | `Cloud Storage`                             |

## Orchestration, integration, and workflow

Coordinate and manage pipelines with:

* Cloud Composer — Managed Apache Airflow for complex scheduling and DAG-based workflows.
* Data Fusion — Also used for integration and orchestration in visual ETL scenarios.
* Cloud Build & Cloud Functions — For event-driven transforms, CI/CD of data pipelines, or light-weight orchestration tasks.

Use orchestration tools to enforce ordering, retries, SLA monitoring, and visibility across your data platform.

## Monitoring, security, and developer tooling

Production platforms require observability, security, and the right developer tools:

* Cloud Operations (Monitoring, Logging, Trace) — Centralized metrics, logs, traces; alerting, dashboards, and incident management.
* Cloud Console, Cloud Shell, Cloud SDK — Developer tools and CLI for provisioning, debugging, and automation.
* Cloud IAM — Fine-grained identity and access control to secure resources and data.

> **warning** Security and cost are operational first-class concerns. Use IAM roles, audit logs, and monitoring alerts to detect misuse and control spend — especially for serverless services like BigQuery and Dataflow where costs scale with usage.

## Quick reference mapping

The table below maps each key GCP service to its primary role and typical use case:

|                     Service |         Layer         | Typical Use Case                                            |
| --------------------------: | :-------------------: | ----------------------------------------------------------- |
|                    BigQuery | Analytics / Warehouse | Ad hoc SQL analytics, BI, analytics at scale                |
|                    Dataflow |       Processing      | Stream/batch unified pipelines using Apache Beam            |
|                    Dataproc |       Processing      | Spark/Hadoop jobs, migration of existing clusters           |
|                     Pub/Sub | Ingestion / Streaming | Event bus for real-time data, decoupled producers/consumers |
|                 Data Fusion |   ETL / Integration   | Visual ELT/ETL pipelines and connectors                     |
|                    Dataprep |    Data Preparation   | No-code/low-code data cleaning for analysts                 |
|                Data Catalog |        Metadata       | Data discovery, schema registry, simple lineage             |
|                    Bigtable |        Storage        | High-throughput low-latency time-series data                |
|       Firestore / Datastore |        Storage        | Realtime document DB for apps                               |
|                   Cloud SQL |        Storage        | Managed relational (OLTP) workloads                         |
|                     Spanner |        Storage        | Globally consistent, horizontally scalable RDBMS            |
|                 Memorystore |         Cache         | Caching, session management with Redis/Memcached            |
|               Cloud Storage |      Object Store     | Landing zone, staged files, backups                         |
|              Cloud Composer |     Orchestration     | Airflow-based DAG scheduling and orchestration              |
|            Cloud Operations |       Monitoring      | Metrics, logs, traces, dashboards, alerts                   |
| Cloud SDK / Console / Shell |       Dev Tools       | Resource management, automation, debugging                  |
|                   Cloud IAM |        Security       | Role-based access control and policies                      |

## How to choose services

* Start with requirements: latency, throughput, consistency, global scale, and team skillset.
* For analytics-first workloads with SQL queries: BigQuery is the default choice.
* For stream processing and event-driven pipelines: Pub/Sub + Dataflow provides a robust, scalable pattern.
* If you already have Spark jobs or need custom libraries: Dataproc is the natural migration path.
* For OLTP relational workloads with global consistency: consider Spanner; for managed single-region relational DBs, use Cloud SQL.
* Use Data Catalog and IAM together to secure and make datasets discoverable.

## Next steps and architecture example

With this landscape in mind, a practical next step is studying concrete architectures — for example, a real-time IoT pipeline using Pub/Sub, Dataflow (Beam), BigQuery, and Cloud Monitoring. That will show how ingestion, processing, storage, and observability work together end-to-end.

<Frame>
  <img alt="" />
</Frame>

Further reading and references:

* [GCP Documentation — BigQuery](https://cloud.google.com/bigquery)
* [GCP Documentation — Dataflow](https://cloud.google.com/dataflow)
* [GCP Documentation — Pub/Sub](https://cloud.google.com/pubsub)
* [GCP Documentation — Dataproc](https://cloud.google.com/dataproc)
* [GCP Documentation — Cloud Storage](https://cloud.google.com/storage)
* [GCP Documentation — Cloud Composer (Airflow)](https://cloud.google.com/composer)
* [GCP Documentation — Cloud Operations (Monitoring & Logging)](https://cloud.google.com/products/operations)

With this overview of the GCP data engineering landscape, you should be able to classify services, choose appropriate tools for common patterns, and design more reliable, cost-effective data platforms.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/1330181a-1f1c-4747-9f22-fdae21dfdf2e/lesson/ece2a6b2-c66d-4acd-86b7-d776906bfc1f)
