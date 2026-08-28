# Interview Byte Consistency or Availability Per Data

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Failure-Protection-and-Operations/Interview-Byte-Consistency-or-Availability-Per-Data/page

Guidance for answering CAP theorem interview questions by choosing consistency or availability per operation, explaining rationale, user effects, and implementation techniques.

When the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem) appears in an interview, the interviewer rarely expects a verbatim definition. Instead, you will typically be asked: "During a network partition, does this part of your system favor consistency or availability?"

The most common mistake is answering for the entire system. A strong candidate answers per operation and explains trade-offs, user-visible behavior, and the implementation choices that enforce that behavior.

For each class of operation you should explicitly state:

* Which you choose: Consistency (C) or Availability (A) during a partition.
* Why this choice makes sense for user experience and business correctness.
* How you will implement it (replication strategy, consensus or async replication, reconciliation, etc.).
* What the user will see during a partition and how you will recover or reconcile afterwards.

<Callout icon="lightbulb">
  Always answer per operation. Explain the user-visible behavior during a partition, the trade-offs, and the reconciliation or protection mechanisms you will use.
</Callout>

## Example: High-throughput, Non-critical Actions — Prefer Availability

Operations like "likes", many types of social feed writes, or analytics events usually prioritize availability. The goal is to keep the service responsive even when some nodes or network segments are down. If you choose availability, be explicit that the system accepts writes locally and reconciles state later, so users may see temporarily inconsistent or stale data.

<Frame>
  <img alt="The image illustrates a data flow diagram featuring users interacting with an app, which sends data to primary and replica databases with a focus on availability. It includes stick figures labeled &#x22;interviewer&#x22; and &#x22;you,&#x22; and emphasizes &#x22;likes&#x22; and &#x22;feed data.&#x22;" />
</Frame>

Techniques you can mention when favoring availability:

* Asynchronous replication: accept local writes and propagate them to replicas later.
* Conflict resolution: use strategies like [last-write-wins](https://en.wikipedia.org/wiki/Last-write-wins), domain-specific merge functions, or [CRDTs](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type).
* Reconciliation jobs: background read-repair, anti-entropy, or periodic convergence processes.
* Idempotency and monotonic counters: make retries safe and reconciliation deterministic.
* Clear UX messaging: show eventual states (e.g., "Saved locally — syncing...") where appropriate.

## Example: Critical Operations — Prefer Consistency

Operations that can cause financial loss or data corruption—charging a customer, reserving the last inventory item, or transferring funds—usually prefer consistency. In these cases you must avoid conflicting updates and enforce a single source of truth even if it reduces availability during a partition.

<Frame>
  <img alt="The image depicts a flowchart illustrating a process involving a user interface for boosting a post, an app, and a database system with a primary and replica for data handling. It also shows two stick figures labeled &#x22;Interviewer&#x22; and &#x22;You.&#x22;" />
</Frame>

Mechanisms to describe when choosing consistency:

* Synchronous replication or quorum-based reads/writes so acknowledged writes are durable and visible immediately.
* Leader-based replication and consensus protocols (e.g., [Raft](https://en.wikipedia.org/wiki/Raft_\(computer_science\)), [Paxos](https://en.wikipedia.org/wiki/Paxos_\(computer_science\))) to maintain a single agreed-upon history.
* Distributed transactions or two-phase commit where necessary; use compensating transactions and idempotent retries for failure handling.
* Strategies to reduce unavailability windows: strong cache invalidation, circuit breakers, or graceful degraded modes with explanatory UI.

## How to Structure Your Interview Answer (Template)

When asked in an interview, be explicit and structured. For each operation:

1. Pick a specific operation (e.g., "like", "feed read", "payment", "inventory reservation").
2. State your choice: Consistency (C) or Availability (A) during a partition.
3. Explain why: user experience and correctness rationale.
4. Describe the implementation: replication, consensus/quorum, reconciliation, retries, idempotency.
5. Describe user-visible effects during a partition and how you recover or reconcile afterward.

This approach shows both theoretical knowledge of the CAP trade-offs and practical system-design thinking.

## Quick Comparison Table

| Operation type                     | Recommended during partition | Why                                                              | Example techniques                                                                  |
| ---------------------------------- | ---------------------------: | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Social "like", feed append         |             Availability (A) | Keep users interacting; transient inconsistencies are acceptable | Asynchronous replication, CRDTs, read-repair, idempotent writes                     |
| Feed read (when freshness matters) |   Consistency (C) or Tunable | Freshness-sensitive reads may require quorum reads               | Read quorums, leader reads, strong caching/invalidation                             |
| Payment, bank transfer             |              Consistency (C) | Prevent double-spend and financial loss                          | Consensus (Raft/Paxos), synchronous replication, distributed transactions           |
| Inventory of last item             |              Consistency (C) | Ensure correct stock levels                                      | Leader-based reservations, quorum writes, optimistic locking + compensating actions |
| Analytics/event ingestion          |             Availability (A) | Max throughput and capture; correctness can be eventual          | Append-only logs, CDC, eventual reconciliation                                      |

## Links and References

* [CAP theorem — Wikipedia](https://en.wikipedia.org/wiki/CAP_theorem)
* [Quorum (distributed computing)](https://en.wikipedia.org/wiki/Quorum_\(distributed_computing\))
* [Raft consensus algorithm](https://en.wikipedia.org/wiki/Raft_\(computer_science\))
* [Paxos consensus algorithm](https://en.wikipedia.org/wiki/Paxos_\(computer_science\))
* [Conflict-free replicated data type (CRDT)](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)
* [Last-write-wins](https://en.wikipedia.org/wiki/Last-write-wins)
* [Idempotence](https://en.wikipedia.org/wiki/Idempotence)
* [Circuit Breaker pattern — Martin Fowler](https://martinfowler.com/bliki/CircuitBreaker.html)

By answering per operation with clear rationale and specific mechanisms, you demonstrate practical command of CAP trade-offs and how to build resilient, user-friendly systems.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/c7a8e3b7-9370-4462-a298-4a441dd68f8a/lesson/ff3f0189-2026-478e-84b1-c1a418c5656e" />
</CardGroup>
