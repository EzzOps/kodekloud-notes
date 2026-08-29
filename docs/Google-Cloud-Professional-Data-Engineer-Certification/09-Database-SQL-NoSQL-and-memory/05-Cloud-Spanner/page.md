# Cloud Spanner

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/Cloud-Spanner/page

Overview of Cloud Spanner, Google Cloud’s globally scalable, strongly consistent relational database with SQL, ACID transactions, automatic sharding, Paxos replication, and managed high availability.

Welcome back.

In this lesson we explore Cloud Spanner — Google Cloud’s horizontally scalable, strongly consistent relational database. Previously we covered Cloud SQL (managed MySQL, PostgreSQL, SQL Server). Cloud Spanner takes relational semantics and transactional guarantees to global scale, making it ideal for mission-critical applications that require both SQL and massive horizontal scalability.

Why Cloud Spanner matters

* Strong consistency + relational semantics: schemas, ACID transactions, and SQL queries (GoogleSQL).
* Horizontal scale: scale out by adding nodes; Spanner automatically shards and rebalances data.
* Global consistency and high availability: consistent reads and strongly consistent transactions across regions using TrueTime and distributed consensus.
* Fully managed: Google handles infrastructure, replication, patching, backups, and maintenance.
* High SLA: Multi-region configurations can provide very high availability for production-critical systems.

Core capabilities

* Relational semantics: ACID transactions, schema support, and a SQL dialect compatible with standard SQL.
* Horizontal scale: Elastic, node-based scaling for throughput and storage growth.
* Global consistency: External consistency across regions due to TrueTime (bounded clock uncertainty) and Paxos-based replication.
* Automatic sharding and replication: Data is shard-balanced and replicated automatically for resilience and performance.
* Managed operations and backups: Built-in automated backups, maintenance, and monitoring.

<Frame>
  <img alt="A slide titled &#x22;Cloud Spanner&#x22; showing its logo and two feature boxes labeled &#x22;Relational Semantics&#x22; and &#x22;Horizontal Scale System.&#x22; A list of benefits on the right highlights fully managed service, SQL+NoSQL scalability, global consistency, and strong transactional support." />
</Frame>

Exam tip

> **lightbulb** If a requirement calls for global scale + SQL + strong consistency, Cloud Spanner is the appropriate Google Cloud product to consider.

How Cloud Spanner achieves both strong consistency and scale
Cloud Spanner merges distributed systems techniques with relational database design. Key technologies include:

* TrueTime: bounded clock uncertainty that enables externally consistent distributed transactions.
* Paxos-based replication: consensus algorithms to ensure durability and consistency across replicas.
* Automatic sharding (splits) and load balancing: Spanner partitions data across nodes and moves splits as workload changes.
* Distributed transaction manager: coordinates multi-row and multi-shard ACID transactions across the cluster.

Common decision point: Cloud Spanner vs Cloud SQL
Use the following table to quickly decide which managed Google Cloud relational database fits your needs.

|      Resource | When to choose                                                                                                                             | Example use cases                                                                                          |
| ------------: | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
|     Cloud SQL | Single-region managed relational DB, compatibility with MySQL/PostgreSQL/SQL Server, lower scale and cost-sensitive OLTP/OLAP              | Small-to-medium web apps, existing apps requiring Postgres/MySQL compatibility                             |
| Cloud Spanner | Globally distributed, strongly consistent relational storage that scales horizontally and supports high-throughput transactional workloads | Global financial systems, large-scale e-commerce, globally distributed user bases requiring ACID semantics |

When to pick Cloud Spanner

* You require SQL plus global, strongly consistent transactions.
* Your workload needs horizontal scale beyond what a single-region RDBMS can provide.
* You need high availability and disaster recovery across regions with strong consistency.

When Cloud Spanner might not be right

> **warning** Cloud Spanner is powerful but introduces additional cost and operational considerations compared to single-region Cloud SQL. If you don't need global scale or strong cross-region consistency, Cloud SQL is often a simpler and more cost-effective choice.

Next steps and references

* Cloud Spanner documentation: [https://cloud.google.com/spanner](https://cloud.google.com/spanner)
* TrueTime and how Spanner provides external consistency: [https://research.google/pubs/pub38166/](https://research.google/pubs/pub38166/)
* Spanner best practices and architecture: [https://cloud.google.com/spanner/docs](https://cloud.google.com/spanner/docs)

We’ll cover Spanner internals (TrueTime, Paxos, splits, replication topologies) and deeper comparisons versus Cloud SQL later in the course.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/3ef85af0-54fc-4f60-b1be-537fd5457dbc)
