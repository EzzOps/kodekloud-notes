# Structured Datastore Options in GCP

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/Structured-Datastore-Options-in-GCP/page

Comparison of Cloud SQL and Cloud Spanner for structured GCP datastores, with guidance on choosing by scale, consistency, availability, operational effort, and cost.

Hello and welcome back.

This article expands on database fundamentals and the distinctions between OLTP and OLAP, and focuses on GCP services built for structured data—data organized in rows and columns with a schema—commonly used for transactional or relational workloads.

Choosing the right datastore affects performance, scalability, operational effort, and cost. Selecting an inappropriate service can lead to overspending, poor performance, or failing to meet application requirements. Below we compare GCP’s two primary managed services for structured data and provide guidance to pick the right one for your architecture.

## Why datastore choice matters

* Performance: Latency and throughput characteristics differ between vertically scaled and horizontally scaled systems.
* Scalability: Some services scale vertically (bigger machines), others horizontally (shard and distribute).
* Consistency and transactions: ACID, strong consistency, and distributed transactions vary by product.
* Operational overhead and cost: Managed features (backups, patches, HA) reduce operational load but affect pricing.

When talking about structured data storage in GCP, the two main managed services are:

* Cloud SQL
* Cloud Spanner

## Cloud SQL (Managed MySQL / PostgreSQL / SQL Server)

Cloud SQL is a fully managed relational database service that provides MySQL, PostgreSQL, and SQL Server instances. It is best suited for conventional OLTP workloads, small-to-medium scale applications, and lift-and-shift migrations where application compatibility and familiar relational features are important.

Key characteristics:

* Engines: MySQL, PostgreSQL, SQL Server
* Scaling: Vertical scaling (increase machine size); supports read replicas for read scaling
* High availability: Regional high-availability with automated failover to a standby in a different zone
* Operational features: Automated backups, patching, maintenance windows, point-in-time recovery
* Use cases: Web apps, content management systems, single-region transactional workloads, legacy RDBMS migrations

Limitations:

* Not designed for transparent global horizontal scaling
* Cross-region synchronous replication and globally consistent transactions are not native features

## Cloud Spanner (Horizontally scalable, globally distributed RDBMS)

Cloud Spanner is Google’s fully managed, horizontally scalable relational database combining relational schema and SQL semantics with global distribution and strong consistency. It is designed for large-scale transactional systems that require global availability and low-latency reads/writes across regions.

Key characteristics:

* Scaling: Horizontal scaling across nodes and regions
* Consistency: Strong (external) consistency using Google’s TrueTime
* Availability: Built-in multi-region configurations for high availability
* Transactions: Distributed ACID transactions at global scale
* Use cases: Global financial systems, large-scale OLTP, gaming backends with cross-region users, inventory/order systems with global consistency needs

Limitations:

* Higher cost for small workloads compared with Cloud SQL
* Different operational model and SQL dialect nuances compared with standard MySQL/Postgres

<Frame>
  <img alt="A slide titled &#x22;GCP – Structured Datastore Options&#x22; showing two cards: Cloud SQL on the left and Cloud Spanner on the right, each with a blue hexagon icon." />
</Frame>

## Which one to pick? — Quick guidance

* Use Cloud SQL when you need:
  * A managed MySQL/PostgreSQL/SQL Server instance
  * Single-region transactional workloads or lift-and-shift of existing apps
  * Simpler operations and lower cost for small-to-medium workloads
* Use Cloud Spanner when you need:
  * Horizontal scalability across nodes and regions
  * Global consistency with low-latency reads/writes across multiple regions
  * Built-in high availability and distributed transactions at scale

<Callout icon="lightbulb">
  When exam or architecture keywords include global scale, horizontal scalability, multi-region availability, or strong transactional consistency at scale, Cloud Spanner is usually the intended choice. For traditional relational needs, compatibility with existing MySQL/Postgres apps, or simpler operational requirements, Cloud SQL is the common answer.
</Callout>

## Feature comparison (at a glance)

| Feature             | Cloud SQL                                 | Cloud Spanner                                                  |
| ------------------- | ----------------------------------------- | -------------------------------------------------------------- |
| Typical workloads   | OLTP, single-region apps, lift-and-shift  | Global OLTP, large-scale transactional systems                 |
| Engines             | MySQL, PostgreSQL, SQL Server             | Spanner SQL (ANSI-like but with Spanner specifics)             |
| Scaling model       | Vertical scaling; read replicas for reads | Horizontal scaling across nodes and regions                    |
| Global consistency  | Not native across regions                 | Strong external consistency (TrueTime)                         |
| High availability   | Regional HA (zonal failover)              | Multi-region HA configurations                                 |
| Best for            | Smaller apps, legacy DB compatibility     | Global-scale applications, consistent distributed transactions |
| Cost considerations | Lower for small/medium workloads          | Higher baseline; cost-effective at large scale                 |

## Decision checklist

* Does your app require multi-region global consistency? → Cloud Spanner
* Do you need a managed MySQL/Postgres instance for compatibility? → Cloud SQL
* Is your workload small-to-medium and single-region? → Cloud SQL
* Do you expect massive scale with distributed transactions? → Cloud Spanner

## Links and references

* [Cloud SQL Documentation](https://cloud.google.com/sql)
* [Cloud Spanner Documentation](https://cloud.google.com/spanner)
* [Choosing a database: Cloud SQL vs Cloud Spanner (GCP whitepaper)](https://cloud.google.com/solutions/databases)

Recap
Both Cloud SQL and Cloud Spanner handle structured data, but they target different scales and use cases. Cloud SQL fits conventional relational workloads and easier migrations, while Cloud Spanner targets global, horizontally scalable, strongly consistent transactional systems. Choose based on your application’s scale, consistency requirements, and operational constraints.

A deeper discussion of Cloud SQL—its features, operational model, and when to use it in your architectures—will follow in the next lesson.

That is it for this lesson. Speak with you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/b88d17c0-7e45-41f1-8bd0-319f2f516096" />
</CardGroup>
