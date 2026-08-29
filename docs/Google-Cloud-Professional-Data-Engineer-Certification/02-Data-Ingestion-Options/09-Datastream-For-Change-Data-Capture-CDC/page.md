# Datastream For Change Data Capture CDC

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Datastream-For-Change-Data-Capture-CDC/page

Explains Google Cloud Datastream CDC service that captures database change events and streams them to BigQuery, Cloud Storage, or Pub/Sub for near real time analytics and event driven pipelines.

Hello and welcome back.

In this lesson we cover Datastream for Change Data Capture (CDC) on Google Cloud. This builds on Cloud Pub/Sub concepts and continues the data ingestion journey by explaining how Datastream captures and delivers database changes in near real time.

## What is Datastream?

Datastream is a serverless, real-time data replication service on Google Cloud that continuously captures changes from supported source databases and delivers them to configured destinations. It reads database transaction logs (binlog/WAL/redo logs), converts those changes into events, and streams them to targets with minimal impact on the source systems.

Why this matters for data engineers

* Keeps analytics and downstream systems up to date with minimal latency.
* Transfers only changes (inserts, updates, deletes) rather than full database dumps, reducing load, storage, and network costs.
* Enables event-driven architectures, real-time analytics, and near-real-time ETL pipelines.

<Callout icon="lightbulb">
  Exam tip: Datastream supports MySQL, PostgreSQL, and Oracle as source databases. Use it to stream change events to BigQuery, Cloud Storage, or Pub/Sub for downstream processing.
</Callout>

<Frame>
  <img alt="A slide titled &#x22;Data Replication Concepts&#x22; with four colored blocks labeled Destination Format (Avro/JSON/Parquet), CDC (change data capture), Targets (BigQuery, Cloud Storage, Cloud Spanner) and Source Systems (MySQL, PostgreSQL, Oracle). Each block includes an icon and short text explaining how changed data is identified and replicated to downstream targets in different formats." />
</Frame>

## How Datastream works (high level)

1. Application writes data to the source database (inserts/updates/deletes).
2. Datastream monitors database transaction logs (e.g., MySQL binlog, PostgreSQL WAL, Oracle redo logs) to capture changes in order.
3. The CDC engine parses and optionally filters events (by table, schema, column, or operation).
4. Datastream writes change events to the configured destination (BigQuery, Cloud Storage, Pub/Sub, etc.) in the chosen format (commonly Avro or JSON).
5. Downstream consumers process, transform, or analyze those change events in near real time.

## Core components and recommended configurations

| Component           |                                                     Purpose | Example / Notes                                                               |
| ------------------- | ----------------------------------------------------------: | ----------------------------------------------------------------------------- |
| Stream              |             Logical grouping of tables/schemas to replicate | Create one stream per application or workload boundary for easier management  |
| Connection profile  |        Stores connection and network details for the source | Includes credentials, VPC peering or private IP settings                      |
| Stream object       |    Represents an individual table or schema within a stream | Specify schema/table filters to limit scope                                   |
| CDC engine          | Reads transaction logs and converts them into change events | Managed by Datastream — no infrastructure to run                              |
| Destination formats |           Output serialization formats for delivered events | Typically Avro or JSON. Parquet is often produced downstream after conversion |
| Monitoring          |          Metrics, logs, and alerts to observe stream health | Track latency, connector errors, and throughput                               |

## Supported sources and typical targets

| Source databases          | Typical destinations | Use cases                                    |
| ------------------------- | -------------------: | -------------------------------------------- |
| MySQL, PostgreSQL, Oracle |             BigQuery | Near real-time analytics and reporting       |
| MySQL, PostgreSQL, Oracle |        Cloud Storage | Data lake storage (raw change events)        |
| MySQL, PostgreSQL, Oracle |        Cloud Pub/Sub | Event-driven architectures and microservices |

## Lifecycle of a change inside Datastream

* Log capture: Datastream reads the database transaction log to capture a reliable, ordered sequence of changes.
* Parse & filter: Logs are parsed into structured change events; filters (tables, columns, or operation types) can be applied to reduce noise.
* Delivery: Events are written to the destination in the configured format.
* Ordering & duplicates: Ordering is preserved as captured from transaction logs. Deduplication and exact delivery semantics depend on destination and consumer-side logic.

<Callout icon="warning">
  Important: CDC requires database transaction logging (e.g., MySQL binlog or PostgreSQL WAL), which may be disabled by default. Ensure transaction logs are enabled and that Datastream has network access and the necessary permissions to read them. Coordinate changes with your DBA or infra team before creating streams.
</Callout>

## Practical checklist before creating a Datastream stream

* Enable transaction logs on the source:
  * MySQL: enable `binlog`
  * PostgreSQL: enable `WAL` and logical replication settings
  * Oracle: enable redo logs and supplemental logging
* Ensure network connectivity:
  * VPC peering, private IP, or public connectivity with proper firewall rules
* Service account permissions:
  * Grant Datastream and any downstream services the needed IAM roles
* Define scope:
  * Choose tables/schemas to replicate, and whether to include DDL or only DML
* Choose output format and destination:
  * Avro or JSON for change events; convert to Parquet later for analytics if needed
* Plan for ordering & de-duplication:
  * Implement idempotent consumers or deduplication logic where required

## Example real-world scenario

E-commerce platform: Orders are created in a transactional database. Datastream captures new order inserts and updates, writes change events to Pub/Sub and Cloud Storage, and streams orders into BigQuery (via Dataflow or a native connector) for dashboards, fraud detection, and shipment workflows. This keeps downstream systems up to date without impacting OLTP performance.

## When to use Datastream

* Need low-latency replication of database changes with minimal source impact
* Want a managed CDC solution integrated with Google Cloud destinations
* Building event-driven architectures, streaming ETL, or real-time analytics

## Further reading and references

* Datastream documentation: [https://cloud.google.com/datastream](https://cloud.google.com/datastream)
* Cloud Pub/Sub: [https://cloud.google.com/pubsub](https://cloud.google.com/pubsub)
* BigQuery: [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)
* Database CDC concepts: [https://martinfowler.com/articles/201701-event-sourcing.html](https://martinfowler.com/articles/201701-event-sourcing.html)

Summary

Datastream is Google Cloud’s managed CDC service for streaming database changes (MySQL, PostgreSQL, Oracle) to destinations such as BigQuery, Cloud Storage, and Pub/Sub. Use Datastream when you need to replicate only the changes with low latency and minimal impact to the source. We’ll cover data store options in the next section.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/9d221f69-db4c-4640-8528-40ed06486c6b" />
</CardGroup>
