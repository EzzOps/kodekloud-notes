# AWS RDS Overview

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/AWS-RDS-Overview/page

Overview of Amazon RDS, a managed relational database service that handles backups, patching, storage, high availability, read scaling, and supports multiple engines

In this lesson, we explore Amazon Relational Database Service (RDS) — a managed relational database platform that removes much of the operational overhead of running production databases.

Imagine an e-commerce site that stores user profiles, products, orders, and payment data. That data requires persistent, secure, highly available storage that can scale as traffic grows. Running and maintaining production-grade relational databases yourself means provisioning hardware, configuring OS and DB software, managing backups, patching, monitoring, scaling, and ensuring high availability and security — all tasks typically handled by DBAs and operations teams.

<Frame>
  <img alt="A slide diagram titled &#x22;RDS&#x22; showing a managed database stack in the center. The left side lists inputs (Hardware, Software, Human Resources) and the right side lists outcomes/requirements (Availability, Security, Scalability)." />
</Frame>

Instead of managing all of that yourself, you can use Amazon RDS. RDS is a fully managed relational database service that offloads routine operational tasks to AWS so you can focus on application development and performance.

Key platform capabilities

* Automatic OS and database patching to keep instances secure and up to date.
* Automated backups, database snapshots, and point-in-time recovery.
* Durable, high-performance storage: most RDS engines use Amazon Elastic Block Store (EBS); snapshots are stored in Amazon Simple Storage Service (S3).
* Storage autoscaling to grow capacity when you approach configured limits.
* Multi-AZ deployments for high availability and automatic failover.
* Support for multiple popular engines: Amazon Aurora, MySQL, PostgreSQL, MariaDB, Oracle, and Microsoft SQL Server.

Table — Supported engines and notable characteristics

| Engine        | Use cases / notes                                                                                       | Links                                                                |
| ------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Amazon Aurora | High-performance, cloud-native; distributed storage subsystem; fast failover and multiple read replicas | [Aurora](https://aws.amazon.com/rds/aurora/)                         |
| MySQL         | Widely used open-source relational DB                                                                   | [https://www.mysql.com/](https://www.mysql.com/)                     |
| PostgreSQL    | Advanced SQL features, extensions, GIS support                                                          | [https://www.postgresql.org/](https://www.postgresql.org/)           |
| MariaDB       | Drop-in MySQL replacement in many cases                                                                 | [https://mariadb.org/](https://mariadb.org/)                         |
| Oracle        | Enterprise features and licensing options                                                               | [https://www.oracle.com/database/](https://www.oracle.com/database/) |
| MS SQL Server | Microsoft SQL Server compatibility                                                                      | [https://www.microsoft.com/sql](https://www.microsoft.com/sql)       |

Storage, snapshots, and backups

For most RDS engines, RDS instances use Amazon EBS for durable, high-performance block storage. EBS-backed volumes support automated snapshots that are stored in Amazon S3, enabling point-in-time recovery and restoration to new volumes if needed.

Amazon Aurora differs: it uses a distributed, purpose-built storage subsystem rather than conventional EBS volumes. Aurora’s architecture improves performance and availability for clustered workloads.

<Frame>
  <img alt="A diagram titled &#x22;RDS – Storage Autoscaling&#x22; showing an RDS instance's storage automatically increasing from 100GB to 150GB when a storage threshold is reached. The illustration uses database and autoscaling icons to show the before-and-after change." />
</Frame>

Storage autoscaling

Because many RDS engines rely on EBS, RDS can automatically increase provisioned storage when usage approaches your configured threshold. This reduces the risk of an application-facing outage due to running out of disk space. EBS snapshots are saved to Amazon S3, ensuring durable backup copies and the ability to restore volumes if corruption or failure occurs.

<Frame>
  <img alt="A simplified AWS RDS architecture diagram showing a DB instance in an Availability Zone reading and writing to an EBS volume. The EBS volume is shown sending snapshots to an S3 bucket (with a failure warning icon displayed)." />
</Frame>

Read scaling with read replicas

To handle read-heavy workloads (e.g., product browsing, reporting), RDS supports read replicas. Read replicas let you offload read traffic from the primary instance and scale horizontally.

* Primary instance accepts reads and writes.
* Asynchronous replication streams data from primary to replicas.
* You can provision multiple read replicas (limits vary by engine and configuration — check current AWS quotas).
* Applications should send writes to the primary; route read-only queries to replicas.
* Cross-region replicas incur inter-region data-transfer charges; intra-region replication typically does not.

<Frame>
  <img alt="A simplified architecture diagram of AWS RDS Read Replicas: a Master RDS asynchronously replicates to two RDS Read Replicas (in a dashed Region A), while a client has read/write access to the master and read access to the replicas." />
</Frame>

High availability with Multi-AZ deployments

Multi-AZ deployments are designed for production-grade availability:

* The primary DB instance runs in one Availability Zone (AZ).
* A standby replica runs in a different AZ and is kept synchronized via synchronous replication.
* The standby is not used for application read/write traffic; it is maintained solely for failover.
* If the primary fails, RDS automatically fails over to the standby and updates the DNS endpoint so your application continues using the same connection string with minimal downtime.

> **lightbulb** Standby instances used for Multi-AZ failover are not exposed for read traffic. For read scaling, provision read replicas. Amazon Aurora uses a different model where multiple replicas can serve reads and participate in faster failover.

How application connectivity and failover work

* RDS provides a managed DNS endpoint for each DB instance or cluster.
* Under normal operation, the endpoint resolves to the primary instance.
* During a Multi-AZ failover, RDS promotes the standby to primary and updates the DNS record so connections resolve to the new primary. This enables automatic failover with minimal change required in application configuration.
* For read scaling, applications should explicitly route read requests to replica endpoints (or use a proxy/load-balancer layer).

Comparing Multi-AZ and Read Replicas

| Feature                | Multi-AZ                                 | Read Replicas                                                                               |
| ---------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------- |
| Purpose                | High availability and automatic failover | Read scaling and analytics offload                                                          |
| Replication type       | Synchronous                              | Asynchronous                                                                                |
| Read traffic supported | No (standby not exposed)                 | Yes                                                                                         |
| Failover               | Automatic                                | Not for automatic failover of primary (replicas can be promoted manually or via automation) |
| Cross-region option    | Typically same-region                    | Supports cross-region replicas (costs apply)                                                |

Summary

* Amazon RDS is a managed relational database service that reduces operational overhead (provisioning, patching, backups, snapshots).
* Supported engines include Amazon Aurora, MySQL, PostgreSQL, MariaDB, Oracle, and Microsoft SQL Server.
* For many engines, RDS uses Amazon EBS for storage and stores snapshots in Amazon S3; Aurora uses a distributed storage subsystem.
* RDS supports storage autoscaling to avoid running out of space.
* Use Multi-AZ deployments to achieve synchronous replication and automatic failover for high availability.
* Use read replicas to scale read-heavy workloads; replicas are asynchronously replicated and can be in the same region or cross-region (cross-region replication incurs data transfer fees).
* RDS exposes a DNS endpoint; on failover RDS updates that endpoint to minimize application disruption.

Links and references

* [Amazon RDS](https://aws.amazon.com/rds/)
* [Amazon Aurora](https://aws.amazon.com/rds/aurora/)
* [Amazon EBS](https://aws.amazon.com/ebs/)
* [Amazon S3](https://aws.amazon.com/s3/)
* [Kubernetes and RDS integrations — general guidance](https://kubernetes.io/docs/concepts/storage/)

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/d8a734ed-504d-4a0a-952e-3ea3b699c3da)
