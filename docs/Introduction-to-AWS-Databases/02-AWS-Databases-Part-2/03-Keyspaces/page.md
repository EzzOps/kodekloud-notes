# Keyspaces

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-2/Keyspaces/page

Overview of Amazon Keyspaces, AWS’s managed, Cassandra‑compatible serverless database offering CQL compatibility, scalable capacity modes, multi‑region replication, security, and managed operational features.

In this lesson we cover Amazon Keyspaces — AWS’s managed, Cassandra-compatible database service for high-throughput, low-latency workloads.

Amazon Keyspaces (for Apache Cassandra) delivers a serverless Cassandra experience: AWS manages the underlying infrastructure, automatically scales capacity, and provides built-in security, availability, and monitoring. Applications use Cassandra Query Language (CQL) and standard Cassandra drivers to interact with Keyspaces, minimizing migration or tooling changes.

Key highlights:

* Fully managed, Cassandra-compatible service using familiar CQL and Cassandra drivers.
* Serverless scaling with on-demand billing or provisioned throughput (with auto scaling).
* High availability across Availability Zones, encryption at rest, IAM integration, and VPC endpoints.
* Built-in TTL (time-to-live) for automatic expiration of data and managed backups.
* Support for multi-region (active-active) deployments with storage-based asynchronous replication.

<Frame>
  <img alt="A diagram of AWS Keyspaces architecture showing Amazon Keyspaces (for Apache Cassandra) in the center connecting client interfaces (Cassandra drivers, cqlsh, and the Keyspaces console) on the left via TLS to multiple encrypted storage nodes on the right. Side notes highlight compatibility with Cassandra Query Language (CQL) and fully managed time-to-live (TTL)." />
</Frame>

What is Amazon Keyspaces

Amazon Keyspaces is designed to remove the operational burden of running Apache Cassandra clusters: provisioning, patching, node management, and scaling. Because Keyspaces is compatible with CQL and Cassandra drivers, you can often reuse existing application code with minimal changes.

How applications use Keyspaces

* Use CQL and standard Cassandra drivers (Java, Python, Node.js, etc.) to read and write data.
* Keyspaces encrypts data at rest and in transit, integrates with AWS IAM for auth, and supports VPC endpoints for private connectivity.
* TTL (time-to-live) is fully managed by Keyspaces — you don’t provision capacity separately for TTL operations.

Quick CQL examples

Create a keyspace (CQL):

```sql theme={null}
CREATE KEYSPACE IF NOT EXISTS demo_keyspace
WITH REPLICATION = {'class': 'SingleRegionStrategy'};
```

Create a table and use it:

```sql theme={null}
CREATE TABLE IF NOT EXISTS demo_keyspace.devices (
  device_id uuid,
  ts timestamp,
  temperature double,
  PRIMARY KEY (device_id, ts)
) WITH CLUSTERING ORDER BY (ts DESC);

INSERT INTO demo_keyspace.devices (device_id, ts, temperature)
VALUES (uuid(), toTimestamp(now()), 72.5);

SELECT * FROM demo_keyspace.devices WHERE device_id = 123e4567-e89b-12d3-a456-426655440000;
```

Capacity modes

Keyspaces supports two throughput capacity modes. Choose the mode that matches your workload characteristics:

| Mode                 | How it works                                                                                           | Best for                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| On-demand capacity   | You pay per read/write request. Keyspaces instantly scales to adapt to unpredictable or spiky traffic. | Applications with irregular, bursty, or unpredictable traffic.             |
| Provisioned capacity | You specify read/write capacity units; enable auto scaling to adjust capacity as load changes.         | Stable, predictable workloads where cost can be optimized by provisioning. |

<Callout icon="lightbulb">
  Choose on‑demand for unpredictable or bursty workloads and provisioned capacity (with auto scaling) for predictable workloads where cost optimization matters.
</Callout>

<Callout icon="warning">
  You can switch a table’s capacity mode (on‑demand ↔ provisioned) at most once per day. Plan capacity changes accordingly.
</Callout>

Multi-region Keyspaces

Keyspaces supports multi-region (global) tables implemented as replica tables — one replica per region — that share a single logical schema. Writes in any region are propagated to other regions using storage-based asynchronous replication. Typical replication lag is low (often under one second), and replication occurs in storage so it has minimal effect on query performance.

Benefits of multi-region Keyspaces:

* Active‑active global reads and writes with low latency for local users.
* Improved business continuity: if a region fails, traffic can be routed to another active region.
* Built-in conflict resolution for write conflicts across regions.

<Frame>
  <img alt="An AWS Keyspaces multi-region replication diagram showing three database nodes on a faint world map connected by dotted arrows. On the right are colored icons listing benefits: global reads and writes, improved business continuity, high-speed replication, and consistency/conflict resolution." />
</Frame>

When to use Keyspaces

Keyspaces is a strong fit when you need Cassandra compatibility without operational overhead. Typical use cases include:

* High-volume telemetry and time-series ingestion (industrial IoT).
* Real-time trading and market monitoring systems.
* Fleet management, routing, or any system that needs low-latency reads and high write throughput.

Key advantages:

* No Cassandra cluster management (provisioning, patching, repair).
* Seamless use of existing CQL-based tools and drivers.
* Built-in security and monitoring integrations.

<Frame>
  <img alt="A slide titled &#x22;Use Case&#x22; showing three colored panels: &#x22;Applications That Require Low Latency,&#x22; &#x22;Open-Source Cassandra APIs,&#x22; and &#x22;Cassandra Workloads to the Cloud,&#x22; each with a matching icon (speedometer, unlocked code padlock, and cloud)." />
</Frame>

Key features (quick reference)

| Feature                    | Description                                                                  |
| -------------------------- | ---------------------------------------------------------------------------- |
| CQL & driver compatibility | Use existing Cassandra drivers and CQL tools (cqlsh, DataStax drivers).      |
| Serverless scaling         | On-demand mode scales automatically; provisioned mode supports auto scaling. |
| Multi-AZ HA                | Data is replicated across Availability Zones for availability.               |
| Multi-region replication   | Active-active global tables with storage-based replication.                  |
| Security & compliance      | Encryption at rest/in transit, IAM integration, and VPC endpoints.           |
| Managed TTL & backups      | Automatic TTL handling and AWS-managed backups/retention.                    |

Summary

Amazon Keyspaces is a fully managed, Cassandra-compatible, serverless database service that reduces operational complexity while preserving the familiar CQL interface. Choose on-demand capacity for unpredictable traffic and provisioned capacity (with auto scaling) for steady, predictable workloads. Multi-region active-active tables provide global reads and writes with low latency and built-in conflict resolution, while the service handles security, replication, TTL, and monitoring for you.

<Frame>
  <img alt="A slide titled &#x22;Summary Keyspaces&#x22; with a turquoise gradient sidebar and three numbered points summarizing Amazon Keyspaces as a managed, Cassandra-compatible database service. The right side lists brief feature descriptions like scalability, automated management, and on‑demand capacity." />
</Frame>

Further reading and references

* Amazon Keyspaces (for Apache Cassandra) — [https://aws.amazon.com/keyspaces/](https://aws.amazon.com/keyspaces/)
* Cassandra Query Language (CQL) — [https://cassandra.apache.org/doc/latest/cql/](https://cassandra.apache.org/doc/latest/cql/)
* Cassandra drivers — [https://cassandra.apache.org/doc/latest/drivers/](https://cassandra.apache.org/doc/latest/drivers/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/6b775562-0b27-41e9-93fc-bb16dab05d87/lesson/fbfdea6c-92f2-4add-90d3-42d70ad5dc3a" />
</CardGroup>
