# AWS Aurora distributed storage

Source: https://notes.kodekloud.com/docs/AWS-RDS/AWS-Aurora/AWS-Aurora-distributed-storage/page

Amazon Aurora’s distributed, log-structured storage architecture decoupling compute and storage, using six-way replication, quorum-based writes, striping, auto-growing volumes, continuous S3 backups, and automated repair for durability.

Welcome back. In this lesson we’ll examine how Amazon Aurora implements distributed storage and why that design improves scalability, availability, and durability for managed relational databases.

## Decoupling compute and storage

Traditional single-instance databases combine compute and storage on the same server. That approach ties two different lifecycles together:

* Compute is often ephemeral and scaled independently (you may replace or resize instances).
* Storage must remain durable and highly available across failures and AZ outages.

Decoupling compute from storage gives independent scaling, faster failover, and more cost-effective lifecycle management for each layer.

> **lightbulb** This lesson explains Aurora’s distributed, log-structured storage architecture and how it uses replication and quorum rules to provide high durability and low-latency access.

<Frame>
  <img alt="A presentation slide titled &#x22;Traditional Database Architecture&#x22; showing a single database instance broken into separate Compute and Storage components. The slide notes that compute and storage should be decoupled for scalability, availability, and durability." />
</Frame>

## Overview — What makes Aurora storage different

Aurora separates the storage layer from compute and implements a purpose-built, log-structured distributed storage system optimized for cloud scale and fast recovery.

Key characteristics at a glance:

| Characteristic            | What it means                                                                                             |
| ------------------------- | --------------------------------------------------------------------------------------------------------- |
| Log-structured storage    | Changes are written as an append-only log, enabling fast sequential I/O and efficient crash recovery.     |
| Striping across SSDs      | Cluster volumes are striped across many storage nodes that use locally attached SSDs for low-latency I/O. |
| Continuous backups to S3  | Incremental backups are continuously streamed to Amazon S3 for durable, off-cluster snapshots.            |
| Multi-AZ distribution     | Data is replicated across multiple Availability Zones to tolerate AZ failures.                            |
| 10 GB protection segments | The cluster volume is segmented into 10 GB units (protection groups) for replication and repair.          |
| Auto-growing volumes      | Cluster volumes expand automatically up to 128 TB as needed.                                              |

## How the distributed storage is organized

When the database writes data, Aurora divides the cluster volume into 10 GB segments (protection groups). Each segment is replicated six times across the region — typically implemented as two copies per Availability Zone across three AZs (2 × 3 = 6).

This six-way replication across multiple AZs protects against individual storage node failures and AZ-level outages while enabling parallel I/O and fast rebuilds of damaged copies.

<Frame>
  <img alt="A diagram of Amazon Aurora architecture showing an application connecting to Aurora and an Aurora Storage Volume spread across three availability zones. Feature notes call out log-structured distributed storage, striping across many storage nodes with locally attached SSDs, continuous backup to S3, and multi‑AZ storage." />
</Frame>

## Reads, writes, and quorum behavior

Aurora uses quorum-based rules to balance durability with low-latency I/O. The cluster maintains six copies of each 10 GB segment and applies the following rules:

|                          Operation |                        Quorum required | Purpose                                                                                                      |
| ---------------------------------: | -------------------------------------: | ------------------------------------------------------------------------------------------------------------ |
|      Durable write acknowledgement |                        4 of 6 replicas | Guarantees that a majority of replicas have persisted the change before returning success.                   |
|                     Read servicing | Any healthy replica (often local/fast) | Reads may be served from any replica; specific recovery or consistency operations can require more replicas. |
| Minimal recovery/consistency check |                        3 of 6 replicas | Used in some repair and recovery workflows to determine segment health.                                      |

This design allows Aurora to acknowledge writes quickly (once 4 replicas persist the log record), while still tolerating up to two replica failures without losing durability guarantees.

## Replication, consistency, and repair

Aurora’s storage layer handles replication, integrity checking, and automated repair:

* Replication: Updates are propagated to the storage nodes that host the segment copies.
* Integrity: Checksums and metadata detect corruption or mismatch among copies.
* Repair: If a copy is corrupt or a node fails, Aurora copies data from healthy replicas to rebuild the missing/corrupt copy automatically.

Under the hood, Aurora uses background protocols (often described as gossip-like or membership/heartbeat mechanisms) to monitor node health, coordinate repair, and restore full redundancy without manual intervention.

<Frame>
  <img alt="A diagram of Amazon Aurora storage architecture showing applications reading and writing to an Aurora storage volume replicated across three availability zones (AZ-1, AZ-2, AZ-3). Annotations note a quorum model for I/O (4/6 writes, 3/6 reads), gossip-based node repair, and fault-tolerance behavior." />
</Frame>

## Security and transport

* Replication traffic between storage nodes travels over the AWS network and is protected by internal integrity checks.
* Client connections to Aurora support TLS for transport-level encryption.
* When you enable encryption for an Aurora cluster, data at rest is encrypted across the storage layer, and internal replication respects those protections.

## Why this design matters

Decoupling compute from a distributed, log-structured storage layer enables several operational and performance benefits:

* Independent scaling: Compute instances can be added or replaced without copying the whole dataset.
* Fast failover: Failover is faster because compute can reattach to the same durable storage without a costly sync.
* High durability: Six-way replication across AZs and automatic repair reduce the risk of data loss.
* Low-latency I/O: SSD-backed striping and quorum rules let Aurora serve reads and acknowledge writes with minimal latency.

## Summary

Amazon Aurora’s distributed storage is a core contributor to its performance and durability profile. The key elements are:

* Log-structured append-only storage
* 10 GB protection segments
* Six-way replication across multiple AZs (typically 2 copies per AZ × 3 AZs)
* Quorum rules (4/6 writes for durability; reads from healthy replicas)
* Continuous backups to Amazon S3
* Automated detection and repair of corrupted or missing copies

These features together deliver a resilient, scalable storage substrate for managed relational databases that supports large, auto-growing cluster volumes and fast, reliable operation.

## Links and references

* [Amazon Aurora documentation](https://docs.aws.amazon.com/aurora/)
* [Amazon S3 — Overview](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* [AWS RDS general documentation](https://docs.aws.amazon.com/rds/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-rds/module/dbfb72c4-207e-424e-ac83-55f55758740a/lesson/955035f3-7f54-4a69-8b86-8413a0f8ab09)
