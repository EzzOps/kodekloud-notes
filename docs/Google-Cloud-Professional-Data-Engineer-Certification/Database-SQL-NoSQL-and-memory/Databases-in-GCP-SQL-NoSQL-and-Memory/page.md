# Databases in GCP SQL NoSQL and Memory

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/Databases-in-GCP-SQL-NoSQL-and-Memory/page

Comparison of GCP database families and services, their use cases, tradeoffs, and guidance for choosing SQL, NoSQL, and in memory solutions like Spanner BigQuery Firestore Bigtable Memorystore

Welcome back. This lesson explains the primary database options available on Google Cloud Platform (GCP) and how to pick the best datastore for your workload. We cover three broad families commonly used by GCP data engineers:

* Relational (SQL) databases
* NoSQL databases
* In-memory databases

You’ll learn each family’s strengths, typical use cases, and the managed GCP services that implement them so you can optimize for performance, scalability, and operational simplicity.

<Frame>
  <img alt="A slide titled &#x22;Database in GCP&#x22; showing data engineers working with SQL, NoSQL, and in-memory databases. To the right are colorful icons and the benefits: &#x22;Optimize performance,&#x22; &#x22;Enhance scalability,&#x22; and &#x22;Increase flexibility.&#x22;" />
</Frame>

## Overview of GCP database families

Relational, NoSQL, and in-memory systems target different data models, latency requirements, and scale. Choose by matching your data model, consistency needs, throughput, and query patterns to the right service.

* SQL / Relational
  * Strong consistency and ACID transactions (product-dependent), structured schemas, and SQL query interfaces.
  * Typical workloads: OLTP transactional systems (financial systems, order processing, ERP).
  * GCP services: Cloud SQL, Cloud Spanner, BigQuery (analytics-oriented).

* NoSQL
  * Flexible schemas (document, wide-column, key-value), designed for massive scale and high throughput.
  * Typical workloads: user profiles, catalogs, IoT telemetry, time-series.
  * GCP services: Firestore (Native mode) for documents; Cloud Bigtable for wide-column, high-throughput workloads.

* In-memory
  * Extremely low-latency reads/writes; ideal for caching, session stores, leaderboards, and ephemeral state.
  * GCP service: Memorystore for Redis or Memcached (managed).

Table: quick feature summary

| Family           |              Key characteristics | GCP products                                   | Ideal for                                   |
| ---------------- | -------------------------------: | ---------------------------------------------- | ------------------------------------------- |
| Relational (SQL) |    ACID, structured schemas, SQL | Cloud SQL, Cloud Spanner, BigQuery (analytics) | OLTP, transactional apps, complex joins     |
| NoSQL            | Flexible schema, high throughput | Firestore, Cloud Bigtable                      | Mobile/web backends, telemetry, time-series |
| In-memory        |          Sub-millisecond latency | Memorystore (Redis/Memcached)                  | Caching, sessions, leaderboards             |

## GCP options — product highlights

* Cloud SQL — managed MySQL, PostgreSQL, and SQL Server. Best for lift-and-shift relational applications and standard OLTP in a single region or limited multi-region setup.
* Cloud Spanner — horizontally scalable, globally-distributed relational database with strong consistency and ACID transactions. Use this for large-scale transactional systems needing global consistency and high availability.
* BigQuery — serverless, columnar analytic warehouse for OLAP, reporting, and large-scale aggregations. Not intended for low-latency transactional workloads.
* Firestore (Native mode) — document database with real-time synchronization and excellent integration with serverless and mobile applications.
* Cloud Bigtable — wide-column store for very high throughput and low-latency single-row reads/writes. Suited to time-series, telemetry, and workloads that map to Bigtable’s access patterns. Note: no secondary indexes or ad-hoc SQL—often paired with BigQuery or Dataflow for analytics.
* Memorystore — managed Redis or Memcached for in-memory caching and sub-millisecond response requirements.

## Choosing the right database: key decision factors

Match these criteria to your application requirements to guide the selection:

| Decision factor            | What to consider                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Data model                 | Relational tables vs documents vs wide-column vs key-value                                                                                 |
| Consistency & transactions | Do you require multi-row ACID transactions or is eventual consistency acceptable?                                                          |
| Latency & throughput       | Sub-millisecond needs → in-memory (Memorystore). Point reads at scale → Cloud Bigtable or Firestore. Large scans/analytics → BigQuery.     |
| Scale                      | Global, strongly-consistent scale → Spanner. Single region or smaller scale → Cloud SQL or Firestore.                                      |
| Query patterns             | Ad hoc analytics/aggregations → BigQuery. Point reads/low-latency writes → Cloud SQL, Spanner, Firestore, Bigtable depending on model.     |
| Operational model          | Serverless/fully managed (lower ops) → BigQuery, Firestore. Managed instances (some sizing/maintenance) → Cloud SQL, Spanner, Memorystore. |

<Callout icon="warning">
  Be mindful of trade-offs: global consistency, latency, and scale each impact cost and complexity. Review pricing, backup/restore options, and networking (VPC, cross-region replication) when designing production systems.
</Callout>

## Mapping common use cases to GCP services

| Use case                                                     | Best-fit GCP service                           | Why                                                                                    |
| ------------------------------------------------------------ | ---------------------------------------------- | -------------------------------------------------------------------------------------- |
| Transactional relational systems (banking, order processing) | Cloud Spanner (global) or Cloud SQL (regional) | ACID transactions; Spanner for global scale; Cloud SQL for traditional relational apps |
| Mobile/web backends with flexible schema and real-time sync  | Firestore (Native mode)                        | Document model, realtime sync, serverless integration                                  |
| Massive throughput, time-series, telemetry                   | Cloud Bigtable                                 | Wide-column design with very high throughput and low-latency single-row ops            |
| Analytics and data warehousing                               | BigQuery                                       | Columnar storage, serverless, fast aggregations and ad-hoc SQL analytics               |
| Caching and ultra-low latency responses                      | Memorystore (Redis / Memcached)                | In-memory performance for sessions, caches, leaderboards                               |

<Callout icon="lightbulb">
  If you want a simple starting rule-of-thumb:

  * Analytics → BigQuery.
  * Flexible document apps → Firestore.
  * Large-scale transactional systems with global consistency → Spanner.
  * Cache or sub-millisecond responses → Memorystore.
</Callout>

## Understanding OLTP vs OLAP

* OLTP (Online Transaction Processing)
  * Focus: many small, fast transactions that touch a few rows (create order, update balance).
  * Characteristics: low latency, high concurrency, normalized schemas, strong consistency.
  * Typical GCP choices: Cloud SQL, Cloud Spanner.

* OLAP (Online Analytical Processing)
  * Focus: complex, large-scale read queries and aggregations (reporting, BI).
  * Characteristics: columnar storage, optimized for scans and aggregations rather than single-row transactions.
  * Typical GCP choice: BigQuery.

## Operational considerations and recommendations

* Backups & recovery: confirm automated backups, point-in-time recovery (if needed), and cross-region restore options.
* Networking & latency: colocate databases with application services and use VPC peering or private IP for secure low-latency traffic.
* Monitoring & scaling: use Cloud Monitoring, autoscaling where possible, and design for the service limits and instance sizing of the chosen product.
* Analytics pipeline: consider pairing OLTP stores with BigQuery (via Dataflow, Datastream, or export jobs) for analytics and reporting.

## Next steps / References

To confidently choose and operate a datastore in GCP, dive deeper into architecture patterns, pricing, sizing, migration approaches, and operational best practices for each product.

Links and documentation:

* [Cloud SQL documentation](https://cloud.google.com/sql/docs)
* [Cloud Spanner documentation](https://cloud.google.com/spanner/docs)
* [BigQuery documentation](https://cloud.google.com/bigquery/docs)
* [Firestore documentation](https://cloud.google.com/firestore/docs)
* [Cloud Bigtable documentation](https://cloud.google.com/bigtable/docs)
* [Memorystore documentation](https://cloud.google.com/memorystore/docs)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/ee8704e7-ca0c-4df5-a19b-01acb27b163f" />
</CardGroup>
