# How does Cloud Spanner achieve Scalability High Availability

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Database-SQL-NoSQL-and-memory/How-does-Cloud-Spanner-achieve-Scalability-High-Availability/page

Explains how Cloud Spanner achieves horizontal scalability and high availability using automatic splitting, distributed replicas, leader election, and transparent rebalancing

Welcome back. This lesson explains how Cloud Spanner provides horizontal scalability and high availability by combining automatic data splitting, distributed replication, leader election, and transparent rebalancing. It builds on core Spanner concepts — nodes, splits (ranges/shards), and replicas — and shows how Spanner uses them to scale without manual sharding.

## Single-table growth and automatic splitting

Consider a single table (for example, `Users`) that grows to millions of rows. Spanner automatically partitions the table along the primary key into contiguous key ranges called splits (also called ranges or shards). Splits are created and managed by Spanner — no application-side sharding is required.

Example splits:

* Split 1: keys from A to M
* Split 2: keys from N to Z

A split is simply a contiguous range of keys. As data grows, Spanner creates new splits so that no single machine becomes a bottleneck.

## Distributing splits across nodes

Splits are distributed across nodes so work can be processed in parallel. Each split has multiple replicas and exactly one leader replica elected for that split:

* Leader: Coordinates writes and serves strongly consistent reads for that split. The leader maintains the authoritative state and coordinates replication.
* Followers/Replicas: Serve read traffic (depending on read configuration) and act as failover copies.

Because splits are independently owned by leaders on different nodes, Spanner can process reads and writes across many nodes in parallel, enabling high throughput and horizontal scale.

## Handling hotspots and automatic rebalancing

If traffic concentrates on a particular key range (a “hot” split), Spanner reacts automatically:

* Split the hot range into smaller ranges.
* Move ranges between nodes to spread CPU and I/O load.
* Add nodes to the instance and redistribute ranges for capacity growth.

This transparent rebalancing enables near-linear horizontal scalability: add nodes and Spanner redistributes splits to increase throughput and storage capacity without application downtime.

For example, if a new split appears and load spikes, Spanner may add node 4 and move some ranges to ensure CPU and disk I/O are balanced across nodes.

## Split, replication, and leader election

Key concepts to remember:

* A split is the unit of distribution and replication.
* Leaders handle writes and ensure strong consistency.
* Replicas are synchronized copies that protect availability and serve reads.
* Leader election and replica promotion are automatic (Spanner uses Paxos for replication and leader election).

These mechanisms let applications scale continuously while keeping data consistent and available.

<Frame>
  <img alt="An infographic titled &#x22;How Cloud Spanner Achieves Scalability and High Availability&#x22; showing a Users table split into key ranges that are distributed as leaders and replicas across nodes. It also illustrates auto-rebalancing of splits to handle load and a sidebar summarizing key concepts (split, leader, replica, split movement)." />
</Frame>

## High availability

Replicas continuously protect availability. If a leader fails, follower replicas can be promoted to leader automatically. When deployed across zones or regions, this replication and automatic failover support strong availability SLAs for multi-region instances.

Spanner’s combination of synchronous replication (within a Paxos group), automatic leader election, and cross-region configuration enables both low-latency reads and robust failover behavior.

<Callout icon="lightbulb">
  Use Cloud Spanner when you need horizontally scalable, strongly consistent relational storage across regions — for example, global transactions, high throughput, and high availability. For many simpler relational workloads, managed alternatives such as Cloud SQL may be more cost-effective.
</Callout>

<Callout icon="warning">
  Cloud Spanner is a fully managed, specialized service. Evaluate costs, operational requirements, and your need for global strong consistency before choosing Spanner over other managed databases.
</Callout>

## Quick reference

| Concept            | Role                          | Notes                                                       |
| ------------------ | ----------------------------- | ----------------------------------------------------------- |
| Split / Range      | Unit of distribution          | A contiguous range of keys that Spanner can move or split   |
| Leader             | Write/strong-read coordinator | Elected per split, coordinates replication (Paxos)          |
| Replica (Follower) | Read-serving & failover copy  | Can be promoted if leader fails                             |
| Rebalancing        | Load distribution mechanism   | Splitting ranges, moving ranges between nodes, adding nodes |

## When to use Cloud Spanner

Choose Cloud Spanner if your application needs:

* Global strongly consistent transactions
* Horizontal scale for high throughput and large datasets
* Low-latency reads and robust cross-region availability

For other cases (single-region, lower scale, or cost-sensitive workloads), consider Cloud SQL or other managed databases.

## Related topics and references

* TrueTime and global ordering: how Spanner uses TrueTime to produce externally consistent ACID transactions — see Google TrueTime.
* Paxos: the consensus algorithm Spanner uses for leader election and replication — see Paxos on Wikipedia.
* Cloud Spanner documentation: [https://cloud.google.com/spanner/docs](https://cloud.google.com/spanner/docs)

That is it for this lesson. See you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/8113b673-3c60-4b57-ae81-fd9533eba836/lesson/0374eac8-8045-4c63-951b-9681d382855d" />
</CardGroup>
