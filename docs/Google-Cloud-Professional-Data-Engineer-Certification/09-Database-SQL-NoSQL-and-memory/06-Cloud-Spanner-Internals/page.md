# Cloud Spanner Internals

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/Cloud-Spanner-Internals/page

Explains Google Cloud Spanner internals, covering global API gateway, regional processing, TrueTime commit semantics, Colossus-backed split storage, replication, and scalability for globally consistent transactions.

Welcome back. In the previous lesson we covered what Cloud Spanner is; here we'll peel back the layers and explain how Spanner delivers global scale with strong (external) consistency. This walkthrough preserves the original system sequence—clients, global API gateway, regional processing, TrueTime, and Colossus storage—so you can see how components interact end-to-end.

## High-level request flow

* Clients target a database but all requests are sent to the global endpoint: `spanner.googleapis.com`.
* A global API gateway handles authentication, authorization, and routes traffic to the nearest regional frontend.
* Regional frontends and request routers forward requests to local processing units for query execution and transaction coordination.

This global-to-regional routing lets clients use a single logical endpoint while the platform routes work into Google’s regional infrastructure for low latency and locality.

## Per-region processing units

Each region runs processing units that implement Spanner’s execution engine. Responsibilities include:

* Planning and executing reads and writes
* Coordinating transactions across replicas
* Interacting with the storage layer to read/write splits (tablets)

Processing units are where SQL planning, RPC handling, and transaction orchestration occur. They collaborate with storage replicas and TrueTime to maintain correctness and performance.

## TrueTime and external (linearizable) consistency

A core Spanner innovation is TrueTime: a globally synchronized clock service that provides a bounded uncertainty interval. TrueTime enables:

* A globally-agreed ordering of transactions
* Spanner’s commit-wait protocol, which uses TrueTime uncertainty bounds to ensure external consistency (linearizability) across regions

Because each commit waits past the upper bound of the transaction’s timestamp uncertainty, clients observe a single, globally consistent order of transactions—even across geographic regions.

## Storage: Colossus and splits (tablets)

Spanner’s storage layer sits on Colossus, Google’s distributed file system. Instead of one monolithic file, Spanner partitions data into contiguous key ranges called splits (also called tablets). Important characteristics:

* Each split is replicated according to the instance’s replication policy (single-region, multi-region, or custom multi-region).
* Replicas are placed across regions for availability and locality.
* Leader replicas handle primary writes; followers serve reads and replicate state.

As the system grows or load shifts, Spanner automatically splits or merges ranges and rebalances replica placement to maintain performance and availability.

<Frame>
  <img alt="A multi-region architecture diagram for Google Cloud Spanner showing a global API gateway and per-region API frontends, request routers, load balancers, processing units (query execution and transaction management), and underlying Colossus storage split across Regions A, B, and Region C. The diagram illustrates how API, compute, and storage layers are replicated and connected across regions." />
</Frame>

## How Spanner achieves scalability and availability

Key design choices that enable Spanner’s global scale and high availability:

* Replication: Each split is replicated across zones/regions for fault tolerance and locality.
* Automatic split management: Ranges are split and merged dynamically based on load and size.
* Leader election and placement: Leaders are placed to optimize latency and availability; elections ensure continuity when failures occur.
* Commit-wait (TrueTime): Ensures transactions are externally consistent across regions.
* Local processing units: Keep query planning and transaction coordination close to replica data and clients.

## Quick reference: architecture layers

| Layer                        | Purpose                                  | Notes / Examples                                              |
| ---------------------------- | ---------------------------------------- | ------------------------------------------------------------- |
| Global API gateway           | Single global endpoint, auth, routing    | Endpoint: `spanner.googleapis.com`; handles TLS, IAM          |
| Regional frontends & routers | Route requests to local processing units | Load balancing, request routing to nearest region             |
| Processing units             | Query planning, transaction management   | Execute SQL, coordinate commits with TrueTime                 |
| Storage (Colossus)           | Persistent, replicated storage of splits | Data partitioned into splits/tablets; replicas across regions |

## Deployment and replication options

| Configuration                 | Use case                           | Typical characteristics                                |
| ----------------------------- | ---------------------------------- | ------------------------------------------------------ |
| Single-region                 | Low-latency local workloads        | Lower cost, no cross-region replication                |
| Multi-region (Google-managed) | Global apps needing geo-redundancy | Replication across multiple regions; high availability |
| Custom multi-region           | Control over replica placement     | Tunable for compliance or latency needs                |

For more details on configuration and pricing, see the Cloud Spanner documentation: [Cloud Spanner Documentation](https://cloud.google.com/spanner/docs).

> **lightbulb** Exam tip: Cloud Spanner is a globally distributed relational database that provides strong (external) consistency and horizontal scaling. Remember: global, strongly consistent, horizontally scalable.

> **warning** Cost note: Cloud Spanner is generally more expensive than single-region relational options (e.g., [Cloud SQL](https://cloud.google.com/sql)) because it provides global replication, automatic split management, and TrueTime-driven consistency. Choose Spanner when you need global consistency and high availability; for smaller or single-region use cases, consider lower-cost alternatives.

## Summary

Cloud Spanner combines a global API gateway, regionally distributed processing units, TrueTime-based commit semantics, and Colossus-backed replicated storage to deliver a strongly consistent, horizontally scalable relational database suitable for mission-critical, globally distributed applications. The interplay of replication, split management, and TrueTime is what enables both low latency and external consistency at scale.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/a002e579-83fa-4946-a62a-ecda7f2a997a)
