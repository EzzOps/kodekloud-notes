# MemoryDB for Redis

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/MemoryDB-for-Redis/page

Overview of Amazon MemoryDB for Redis architecture, durability, features, and when to use it for low latency, highly available real time applications such as ride sharing

In this lesson you’ll learn what Amazon MemoryDB for Redis is, when to use it, and how its architecture addresses the common requirements of real‑time applications such as ride‑sharing or delivery platforms.

Use case: a ride‑sharing or delivery app

* Real-time apps (Uber, DoorDash) require extremely low-latency access to frequently changing data: location updates, ride/delivery requests, driver statuses, session state, and pricing calculations.
* They must process thousands of updates per second, remain available 24/7, preserve critical transactional state across failures, scale with demand, and keep state consistent across clients.

<Frame>
  <img alt="Slide titled &#x22;Amazon MemoryDB for Redis&#x22; showing a ride-sharing app icon and three short bullets: user profiles and session states; real-time driver location/status updates; and ride/delivery requests with matching logs." />
</Frame>

Key operational requirements for this scenario

* Speed: ultra-low read/write latency to handle frequent updates (e.g., driver locations).
* Reliability & Availability: continuous operation across infrastructure failures.
* Durability: no loss of transactional data (ride requests, matches) during failures.
* Scalability: capacity to absorb traffic spikes without performance degradation.
* Consistency: clients observe a single, up‑to‑date view of state.

<Frame>
  <img alt="A presentation slide titled &#x22;Amazon MemoryDB for Redis: Challenges&#x22; featuring a ride-sharing app icon and colored labels listing challenges: Speed, Reliability, Data Durability, Scalability, and Consistency." />
</Frame>

How MemoryDB addresses these requirements

* In-memory performance: stores dataset primarily in memory for microsecond to low‑millisecond reads and writes—ideal for real‑time updates.
* High availability: Multi‑AZ replication with automatic failover keeps clusters online when an Availability Zone fails.
* Durability: writes are append‑only to a distributed transaction log that is durably stored and replicated across AZs for recovery and minimal data loss.
* Scalability: horizontal scaling via shards and replicas to meet growing throughput and capacity needs.
* Strong consistency during failover: designed replication and transaction log mechanics reduce the risk of stale reads after failover.
* Redis compatibility: supports the Redis data model and protocol, so most existing Redis clients and tools work with minimal changes.

<Frame>
  <img alt="A presentation slide titled &#x22;Features&#x22; showing five numbered feature cards (01–05) with colorful circular icons: Fully Managed Service, Redis Compatibility, Built‑in Replication and Auto‑Failover, Scalability, and Cost‑Effectiveness. A small &#x22;© Copyright KodeKloud&#x22; notice appears at the bottom." />
</Frame>

Operational benefits of a fully managed service

* AWS handles provisioning, patching, and routine operations—reducing administrative overhead.
* MemoryDB can replace separate cache + persistent store architectures when you need both in‑memory performance and durable storage semantics.

Architecture overview

* Primary / Replica model: each shard hosts a primary (handles reads/writes) and one or more replicas (read scaling and failover candidates).
* Distributed transaction log: the primary appends updates to a transaction log that is durably stored and replicated across AZs; replicas consume the log to replicate updates reliably.
* Sharding: datasets are partitioned across multiple shards so the cluster can scale horizontally and distribute load.

<Frame>
  <img alt="A diagram titled &#x22;Amazon MemoryDB for Redis: Architecture&#x22; showing a VPC with three Availability Zones containing a Primary node and two Secondary Replicas. It illustrates a shared Transaction Log and arrows indicating sync writes to the primary and async writes to the replicas." />
</Frame>

Backup and recovery

* Transaction logs + snapshots: MemoryDB combines a distributed transaction log with periodic or on-demand snapshots. Together they enable point‑in‑time recovery and seeding of new clusters.
* Snapshots are stored durabley (e.g., in Amazon S3) and can be used to restore a cluster to a previous state or to create a copy for testing.

<Frame>
  <img alt="A slide titled &#x22;Amazon MemoryDB for Redis: Backup and Recovery&#x22; showing a MemoryDB transaction log automatically backing up to an S3 bucket where snapshots are stored. The diagram uses icons: a purple MemoryDB log on the left, an arrow to a green S3 bucket inside a dashed box with a &#x22;Snapshot&#x22; label." />
</Frame>

MemoryDB vs ElastiCache (Redis)

| Dimension         |                                                                                   MemoryDB | ElastiCache (Redis)                                                  |
| ----------------- | -----------------------------------------------------------------------------------------: | -------------------------------------------------------------------- |
| Purpose           |                 Durable, highly available in‑memory datastore for critical ephemeral state | Primary use as a fast cache layer; persistence is optional           |
| Durability        |              Built for durability with a distributed transaction log replicated across AZs | Supports snapshots and optional AOF/RDB, but durability is secondary |
| Replication       |                 Multi‑AZ replication and transaction logging designed for durable replicas | Replication groups and replicas supported; behavior varies by config |
| Typical use cases | Session stores, primary datastore for ephemeral but critical state (e.g., matching engine) | Caching, session caching when loss is acceptable or can be rebuilt   |
| Cost              |                                  Generally higher cost due to durable multi‑AZ replication | Typically lower cost when used purely as a cache                     |

When to choose MemoryDB

* Choose MemoryDB when you need:
  * Very low latency (in‑memory) plus durable storage semantics.
  * Multi‑AZ high availability and strong guarantees during failover.
  * Redis compatibility so you can reuse existing Redis client code.
  * Example: a ride‑sharing backend that cannot afford to lose transactional state during outages.

When to choose ElastiCache

* Choose ElastiCache when you primarily need caching and can tolerate data loss or rehydration from another persistent store. It’s a cost‑effective option for read scaling and short‑lived session caches.

Pricing and cost considerations

* MemoryDB’s stronger durability and multi‑AZ replication typically increase cost compared with ElastiCache used as a cache.
* Consider cost vs. risk: evaluate the business impact of losing ephemeral state versus the ongoing cost of a durable in‑memory store.

Practical examples and common Redis commands

* Common patterns used with MemoryDB:
  * Session store: `HSET session:<id> userId 123 lastSeen <timestamp>`
  * Real‑time location updates: `GEOADD drivers <lon> <lat> driver:<id>`
  * Matchmaking queue: `LPUSH rides:requests <requestId>` / `BRPOP rides:requests 0`
* Because MemoryDB is Redis‑compatible, existing Redis commands and client libraries continue to work.

> **lightbulb** MemoryDB is Redis‑compatible, so most Redis clients and commands work unchanged. You can migrate or reuse Redis-based code with minimal changes while gaining durability and Multi‑AZ availability.

> **warning** Evaluate failure modes and recovery procedures before switching to MemoryDB. Strong durability reduces data loss risk, but application-level handling for edge cases (split‑brain, propagation lag, or replica promotion) is still important.

Links and references

* AWS MemoryDB for Redis documentation: [https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html](https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html)
* Redis project: [https://redis.io/](https://redis.io/)
* AWS ElastiCache for Redis: [https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html)

Further reading

* Architectural patterns for real‑time systems
* Designing for eventual consistency vs. strong consistency
* Capacity planning for in‑memory datastores

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/6a7580a8-a2a6-4356-bc28-457f769ebff2)
