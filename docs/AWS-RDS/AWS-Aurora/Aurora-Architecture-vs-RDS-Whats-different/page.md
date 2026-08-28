# Aurora Architecture vs RDS Whats different

Source: https://notes.kodekloud.com/docs/AWS-RDS/AWS-Aurora/Aurora-Architecture-vs-RDS-Whats-different/page

Comparison of Amazon Aurora and RDS architectures, highlighting differences in storage, replication, performance, failover, and backup to guide migration or deployment choices.

This lesson compares Amazon Aurora’s architecture with Amazon RDS across five key dimensions: storage architecture, performance, replication, automatic failover, and backup & restore. This side-by-side view helps you decide whether to migrate an existing RDS workload to Aurora or select the right option for a new deployment.

Covered topics:

1. Storage architecture
2. Performance
3. Replication
4. Automatic failover
5. Backup and restore

## Storage architecture

The fundamental architectural difference between Aurora and RDS is how they handle storage.

* RDS: Each database instance typically uses instance-attached block storage (Amazon EBS). Storage is tied to the instance lifecycle, and scaling storage or IOPS requires provisioning larger EBS volumes or different volume types.
* Aurora: Compute (database instances) is decoupled from a distributed, fault-tolerant storage layer. Data is split into 10 GB segments and each segment is replicated across multiple storage nodes in the cluster. Aurora keeps multiple copies of each segment across Availability Zones (AZs) to provide high durability and availability.

Practical implications:

* Aurora’s shared, distributed storage enables independent scaling of compute and storage, reduces single points of failure, and improves resilience out of the box.
* RDS’s block-storage model is simpler to reason about for many legacy deployments, but resiliency and scaling require different operational approaches (EBS snapshots, resizing, Multi-AZ setups).

## Performance

Aurora is optimized for low-latency, high-throughput workloads—especially read-heavy applications—because of its separation between compute and a shared storage layer.

<Frame>
  <img alt="A presentation slide titled &#x22;Performance&#x22; noting that Aurora's architecture is more efficient for read-heavy workloads and offloads reads to replicas to reduce load on the primary instance. A vertical step menu on the left shows items 01–05 with &#x22;02&#x22; highlighted and a small &#x22;© Copyright KodeKloud&#x22; at the bottom." />
</Frame>

* Aurora offers reader endpoints and multiple read replicas that can offload read traffic from the writer without duplicating storage, which reduces replication lag and improves read scaling.
* RDS read replicas (where supported) usually use asynchronous replication, which can create replication lag under load and make strongly consistent reads harder to guarantee.

Key takeaway: For applications with heavy read requirements or unpredictable read traffic, Aurora typically delivers more predictable, higher read throughput and lower latency than a comparable RDS setup.

## Replication

Aurora’s storage layer uses a quorum-based replication model that differs significantly from many traditional RDS replication approaches.

<Frame>
  <img alt="A minimalist presentation slide titled &#x22;Replication&#x22; with a bullet saying &#x22;Aurora has a quorum-based approach, which allows for faster crash recovery and less replication lag.&#x22; The left sidebar shows a vertical list of numbered circular steps (01–05) with &#x22;03&#x22; highlighted in blue." />
</Frame>

* Aurora divides data into segments and maintains multiple copies (typically six copies across three AZs). A write is considered durable once a quorum of storage nodes acknowledges it. Because readers share the same storage layer, replication lag is very low.
* RDS replication depends on the engine: asynchronous logical/physical replication for read replicas, and synchronous replication only for RDS Multi-AZ standbys in many engines. Behavior varies by engine version and configuration.

Why it matters: Aurora’s quorum-based replication reduces the window for data loss and enables faster crash recovery and near-real-time reads from replicas.

## Automatic failover

The mechanics and speed of automatic failover differ between Aurora and traditional RDS Multi-AZ setups.

<Frame>
  <img alt="A presentation slide titled &#x22;Automatic Failover&#x22; explaining that Aurora provides automated failover with zero data loss while RDS may experience some data loss during failover. The left side shows numbered step circles (01–05) with &#x22;04&#x22; highlighted, and a small &#x22;© Copyright KodeKloud&#x22; at the bottom." />
</Frame>

* Aurora: Because compute is separate from storage and storage is synchronized across AZs, a reader or another instance can be promoted quickly to writer. The shared, quorum-backed storage minimizes risk of data loss and reduces failover time.
* RDS Multi-AZ: Uses a standby instance in another AZ (often with synchronous replication). Failover requires promoting the standby instance and redirecting connections; this typically takes longer than Aurora failover and behavior can vary by engine.

In short: Aurora is designed for faster failovers with minimal data loss in common failure scenarios, while RDS Multi-AZ focuses on durability and availability but can have longer failover times.

## Backup and restore

Backup behavior and restore performance are another area where Aurora provides operational advantages.

<Frame>
  <img alt="A presentation slide titled &#x22;Backup and Restore&#x22; noting that Aurora backups are continuous and incremental, reducing backup times and improving restore performance compared to RDS. The left side shows a vertical step list (01–05) with 05 highlighted and a small © KodeKloud notice at the bottom." />
</Frame>

* Aurora: Continuous, incremental backups to Amazon S3 are built into the storage layer. Incremental snapshots and point-in-time recovery are fast and efficient, lowering operational overhead for backups and restores.
* RDS: Automated backups and snapshots are supported and operate against instance block storage. Depending on database size, workload, and EBS snapshot behavior, backups/restores can be slower or more resource-intensive.

Operational benefit: For large or highly changeable databases, Aurora’s continuous incremental backups reduce downtime and speed recovery.

## Side-by-side comparison

| Dimension     | Amazon Aurora                                                  | Amazon RDS                                                       |
| ------------- | -------------------------------------------------------------- | ---------------------------------------------------------------- |
| Storage model | Distributed, shared storage (segmented, replicated across AZs) | Instance-attached block storage (EBS)                            |
| Replication   | Quorum-based storage replication (low lag)                     | Varies by engine: async read replicas or sync Multi-AZ           |
| Read scaling  | Reader endpoints + shared storage → low-lag reads              | Read replicas (async) → higher potential lag                     |
| Failover      | Fast promotion, minimal data loss (shared storage)             | Multi-AZ standby promotion → typically slower, engine-dependent  |
| Backups       | Continuous, incremental to S3 → fast PITR & snapshots          | Automated backups/snapshots on EBS → can be slower for large DBs |

Which should you choose?

* Choose Aurora when you need:
  * High read throughput and low-latency reads
  * Fast, low-lag replication and quick failover
  * Seamless compute scaling independent of storage
  * Continuous, incremental backups with fast restores
* Choose RDS when you need:
  * A traditional instance-attached storage model (EBS) or specific database engine behaviors/extensions not available in Aurora
  * Simpler single-instance setups or compatibility with legacy tooling

<Callout icon="lightbulb">
  If your workload is read-heavy, requires rapid failover, or needs highly available, scalable storage with minimal operational overhead, Amazon Aurora is often the better choice. For legacy requirements, specialized engine features, or when you prefer instance-attached storage semantics, RDS remains a robust option.
</Callout>

Links and references

* Amazon Aurora documentation: [https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP\_AuroraOverview.html](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)
* Amazon RDS documentation: [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
* AWS whitepaper: AWS Database Migration & Modernization (for migration considerations)

That concludes this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-rds/module/dbfb72c4-207e-424e-ac83-55f55758740a/lesson/98d21a15-0c01-4a74-b04c-6466afe72d63" />
</CardGroup>
