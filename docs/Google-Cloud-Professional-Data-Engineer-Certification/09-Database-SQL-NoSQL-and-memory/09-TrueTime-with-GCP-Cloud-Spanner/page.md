# TrueTime with GCP Cloud Spanner

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/TrueTime-with-GCP-Cloud-Spanner/page

Explains Google Cloud Spanner's TrueTime, an interval-based time service that bounds clock uncertainty to enable globally consistent, externally ordered ACID transactions.

Welcome back. This article explains Google Cloud Spanner's TrueTime: the high-precision, distributed time service that makes Spanner's external consistency and global ACID transactions possible. You'll learn the clock-skew problem TrueTime solves, how TrueTime exposes bounded uncertainty, how Spanner uses it to order transactions globally, and why this matters for distributed systems.

> **lightbulb** TrueTime is a central piece of Spanner's design. If you want a deeper dive, see the [Cloud Spanner documentation](https://cloud.google.com/spanner/docs) for implementation details and design notes.

## Problem: clock skew in a distributed system

In globally distributed systems, server clocks drift. Even with NTP (Network Time Protocol), perfectly synchronized clocks across continents are unrealistic. Small differences—milliseconds or less—make it ambiguous which event happened first. That ambiguity undermines strong consistency and can break serializability guarantees in distributed databases.

## TrueTime: interval-based time with bounded uncertainty

Instead of returning a single timestamp, TrueTime returns a time interval that is guaranteed to contain the real time now. Each API call yields:

```text theme={null}
TrueTime.now() = [earliest, latest]
Example: [03:00:00.004, 03:00:00.010]  ->  uncertainty = 6 ms
```

The difference (latest − earliest) is the uncertainty window. Google keeps this window small (typically \< 7 ms) by using redundant, high-precision time sources and careful filtering. Clients and Spanner components reason about time using these intervals rather than a single instant.

## Time sources and infrastructure

TrueTime maintains accuracy and bounds uncertainty using multiple, independent references:

| Time source                                          | Role                                                                  |
| ---------------------------------------------------- | --------------------------------------------------------------------- |
| Dedicated time masters (usually two per data center) | Aggregate and validate time from local references and network sources |
| GPS receivers                                        | Provide precise UTC time when available                               |
| Atomic clocks (co-located)                           | Serve as a stable local reference when GPS is unavailable             |
| Cross-checking & filtering                           | Compare, filter, and reject anomalous readings to bound uncertainty   |

These redundant sources and filtering reduce the risk that a single failed source causes incorrect time readings.

## How Spanner uses TrueTime to guarantee external consistency

Spanner leverages TrueTime intervals to assign globally meaningful timestamps and to enforce a single global ordering of transactions. Conceptually, a write (commit) transaction follows three steps:

1. Assign a commit timestamp
   * The transaction coordinator picks a commit timestamp that respects previously observed timestamps and read dependencies. The chosen timestamp must be at least as large as any timestamp the coordinator has seen and must account for current TrueTime uncertainty.

2. Commit-wait (wait out uncertainty)
   * Before making the write visible, the coordinator waits until the commit timestamp is guaranteed to be in the past globally. Concretely:
     ```Python theme={null}
     wait until TrueTime.now().earliest > commit_timestamp
     ```
   * This "commit-wait" makes the assigned timestamp unambiguous for all clients, preventing a future transaction from being assigned a timestamp earlier than this commit.

3. Finalize and make the commit visible
   * After the wait completes, the transaction is durable and can be published with the assigned timestamp. Because the system has waited out the uncertainty window, the timestamp now represents a globally consistent ordering.

Below is a concise view of the steps and their purpose.

| Step             | Purpose                                                                                     |
| ---------------- | ------------------------------------------------------------------------------------------- |
| Assign timestamp | Choose a globally consistent commit timestamp that incorporates observed dependencies       |
| Commit-wait      | Ensure the chosen timestamp is in the past for all nodes to avoid ambiguity from clock skew |
| Publish commit   | Make the transaction visible with a durable, globally meaningful timestamp                  |

<Frame>
  <img alt="A diagram titled &#x22;How TrueTime Works&#x22; showing time references (Satellite Time and Atomic Clocks). Below it are three steps describing how Spanner uses TrueTime: get a TrueTime interval at transaction start, wait for the uncertainty to pass (commit-wait), then assign a timestamp to guarantee external consistency across the globe." />
</Frame>

## Operational considerations

* TrueTime's uncertainty window is intentionally small, but it is non-zero. The commit-wait introduces a small latency (on the order of the uncertainty window) to guarantee correctness.
* Spanner combines TrueTime-based timestamps with distributed replication and consensus (Paxos/raft-like protocols) to ensure both durability and external consistency.

> **warning** Commit-wait ensures correctness but adds a small, bounded latency equal to TrueTime's uncertainty. For low-latency workloads, design your data and transaction patterns accordingly (e.g., minimize cross-region contention).

## Why this matters — key benefits

* Global ordering of transactions
  * Distributed transactions behave as if executed on a single, serial system. This simplifies application reasoning and correctness proofs.
* Eliminates ambiguity from clock skew
  * The commit-wait ensures assigned timestamps are consistent across regions, avoiding anomalies from unsynchronized clocks.
* Enables true ACID transactions at global scale
  * By combining global timestamping (TrueTime) with distributed consensus for replication, Spanner provides serializable, strongly consistent transactions across regions.

## Summary

TrueTime provides a small, bounded interval for "now" and enables Spanner to enforce an externally consistent, globally ordered timeline of transactions. By assigning timestamps that account for uncertainty and waiting until those timestamps are safely in the past, Spanner removes the ambiguity that clock skew introduces—making global ACID guarantees practical.

Links and references

* Google Cloud Spanner documentation: [https://cloud.google.com/spanner/docs](https://cloud.google.com/spanner/docs)
* Network Time Protocol (NTP): [https://www.ntp.org/](https://www.ntp.org/)
* Research paper: "Spanner: Google's Globally-Distributed Database" — for design and paper-level details.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/0fdb422b-200f-42f4-b25e-cd112e9c1941)
