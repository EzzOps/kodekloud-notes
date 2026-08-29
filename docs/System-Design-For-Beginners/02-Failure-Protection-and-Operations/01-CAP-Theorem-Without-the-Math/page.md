# CAP Theorem Without the Math

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Failure-Protection-and-Operations/CAP-Theorem-Without-the-Math/page

Explains the CAP theorem and how to choose between consistency and availability during network partitions when designing distributed systems.

This article explains the CAP theorem in plain terms and shows how to apply its trade-offs when designing distributed systems.

CAP is a fundamental principle for distributed systems that store data across multiple machines. It codifies an unavoidable trade-off you must make when nodes can be cut off from one another by network failures.

CAP stands for three properties:

* C — Consistency\
  Every successful write is visible to all subsequent reads: once a write completes, every later read returns that latest value, regardless of which machine handles the request.
* A — Availability\
  Every request receives a response (success or failure); the system continues to answer queries even if some parts are degraded.
* P — Partition tolerance\
  The system continues to operate despite arbitrary network partitions — i.e., communication loss between nodes.

When the network is healthy (no partition), many systems can provide both consistency and availability. But when a network partition happens, you cannot guarantee both consistency and availability simultaneously.

A simple concrete scenario helps make this clear.

Imagine a photo app with a primary database and two replicas. A network partition is when the links between those machines break. Each machine may keep running, but they can't exchange updates until the network heals. Requests continue to arrive — users open feeds, tap like buttons — while the system is split. At that point you effectively have two choices:

* Keep answering requests on both sides: you preserve availability, but the primary and replicas may diverge (sacrificing consistency).
* Refuse or delay some requests until nodes can agree: you preserve consistency, but some operations become unavailable.

<Frame>
  <img alt="The image illustrates the concept of Consistency in a distributed system, showing how users interact with an app, which communicates with a primary and replica database, highlighting a network partition scenario." />
</Frame>

You cannot have both consistency and availability during a partition because the two partitions are physically unable to coordinate. Network failures are outside your control and can occur at any time, so the practical design trade-off becomes: consistency vs availability when partitions are possible.

Quick rule of thumb:

* If you prioritize availability, clients always get a response, but the response may be stale or conflicting.
* If you prioritize consistency, clients see the single latest agreed value, but some requests may be rejected or delayed during partitions.

<Frame>
  <img alt="The image illustrates the CAP theorem, highlighting the choice between availability and consistency. It explains that choosing availability means always getting an answer, though it might be outdated, while choosing consistency ensures the latest agreement." />
</Frame>

Decision checklist (short):

| Goal                                                                           | Favor                                                                      |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Keep system responsive under partition for non-critical data (feeds, counters) | Availability (eventual consistency)                                        |
| Prevent duplicated or lost resources (bank balances, inventory)                | Consistency (strong/linearizable)                                          |
| Systems facing frequent partitions (geo-distribution over unreliable links)    | Design for partition tolerance and choose C or A based on data criticality |

Example 1 — Likes on a photo:
If a partition causes two users to briefly see 1,000 likes vs 1,001 likes, that small divergence is usually acceptable. Favor availability: keep the app responsive, accept slightly stale counters, and reconcile counts when nodes rejoin.

<Frame>
  <img alt="The image illustrates a network partition scenario with emphasis on consistency, availability, and partition tolerance, showing how likes on a social media application are affected. One phone shows 1001 likes connected to a primary database, while another shows 1000 likes due to a network partition impacting the replica database." />
</Frame>

Example 2 — Account balances or payments:
If a partition lets a user spend the same \$10 twice because two sides can't see each other, the consequences are unacceptable. Favor consistency: refuse or delay transactions until the system can confirm funds safely. Payment systems typically prefer rejecting an operation over risking double-spend.

<Frame>
  <img alt="The image illustrates a network partition scenario affecting a payment transaction system, highlighting concepts of consistency, availability, and partition tolerance with two database nodes managing a $100 charge." />
</Frame>

> **lightbulb** When designing your system, classify each data type by how costly inconsistency is. Use eventual consistency for user-visible metrics and feed data, but require strong consistency for financial, inventory, or safety-critical operations.

> **warning** Remember: network partitions are inevitable in distributed systems. Never assume perfect connectivity when making consistency/availability trade-offs for critical data.

References and further reading:

* [CAP theorem — Wikipedia](https://en.wikipedia.org/wiki/CAP_theorem)
* Eric Brewer's original talk on the CAP intuition (see materials about the Brewer conjecture)
* Martin Kleppmann, "Designing Data-Intensive Applications" — practical patterns for consistency and availability
* [Kubernetes — distributed systems patterns overview](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

In summary: CAP tells you that when a partition divides your system, you must choose between consistency and availability. For ephemeral counters and feeds, teams usually prefer availability. For money, inventory, and other resources that must never be duplicated or lost, teams choose consistency. Your architecture should reflect these priorities explicitly and include reconciliation strategies for the cases where you accept temporary inconsistency.

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/c7a8e3b7-9370-4462-a298-4a441dd68f8a/lesson/e209f8e9-445f-4455-b568-d735efe34f9d)
