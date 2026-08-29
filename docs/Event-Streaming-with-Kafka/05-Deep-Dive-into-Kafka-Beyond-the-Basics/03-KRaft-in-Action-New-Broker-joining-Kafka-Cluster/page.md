# KRaft in Action New Broker joining Kafka Cluster

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Deep-Dive-into-Kafka-Beyond-the-Basics/KRaft-in-Action-New-Broker-joining-Kafka-Cluster/page

Explains how a new Kafka broker joins a KRaft cluster via controller leader registration, Raft metadata log commits, and subsequent metadata updates and rebalancing.

Welcome back. This lesson explains, step-by-step, how a new broker joins a Kafka cluster when the cluster is running in KRaft mode. The flow focuses on controller leadership, the Raft-backed metadata log, the broker registration request, and subsequent rebalancing. Use this as a concise technical reference for KRaft broker-join behavior.

## Quick overview

When a new broker starts in KRaft mode:

* It contacts the controller leader to register.
* The controller proposes the registration change to the Raft metadata log.
* A quorum commit makes the registration authoritative and durable.
* The controller publishes updated metadata and may trigger rebalancing.

This guarantees consistency because all control-plane changes are coordinated and committed via Raft.

## Step-by-step broker join flow

### 1) New broker process starts

A new broker process boots and attempts to join the cluster by contacting the cluster controller(s). In combined deployments the controller may run in the same process as a broker, but logically controller endpoints are distinct.

Key data the broker sends (or requests):

* Broker ID (or request for automatic assignment)
* Advertised listeners
* Rack or availability-zone information (optional)
* Any additional broker-level metadata

### 2) Controller leader check and election

KRaft maintains a controller quorum. The first check from the broker-side is whether there is a current controller leader:

* If a controller leader exists, the broker will send its registration to that leader.
* If there is no leader, the controller quorum runs a Raft leader election. The elected controller leader will handle metadata changes (including this registration).

<Callout icon="lightbulb">
  KRaft uses the [Raft consensus algorithm](https://raft.github.io/) for controller state. Any metadata change (broker registration, topic creation, partition reassignments, config updates) must be proposed and committed to the Raft metadata log, and acknowledged by a majority of controllers, to be durable and visible cluster-wide.
</Callout>

### 3) Broker sends registration to the controller leader

Once a leader is available, the broker sends a RegisterBroker-style request. The controller leader validates the request; validation typically includes:

* Broker ID uniqueness and ranges
* Listener and advertised address validation
* Compatibility with cluster-level policies (e.g., rack-awareness constraints)

Example (simplified) registration payload:

```json theme={null}
{
  "brokerId": -1,
  "host": "broker-9.example.com",
  "port": 9092,
  "advertisedListeners": ["PLAINTEXT://broker-9.example.com:9092"],
  "rack": "rack-az-3"
}
```

(The actual Kafka wire format differs; this illustrates the typical fields.)

### 4) Controller proposes the registration to the Raft metadata log

The controller leader does not apply the registration locally and return success immediately. Instead it:

* Proposes a metadata change entry (broker-registration) to the Raft metadata log.
* Sends AppendEntries to the controller quorum to replicate the proposed change.
* Waits for acknowledgements from a majority (quorum) of controllers.

Only after the Raft majority acknowledges the entry is the registration considered committed and authoritative.

### 5) Controller acknowledges the broker (post-commit)

After the registration entry is committed in the metadata log:

* The controller leader responds to the broker confirming registration and the assigned broker ID (if it was assigned).
* The controller broadcasts updated cluster metadata (or ensures brokers can read it from the metadata log), so other brokers learn about the newly joined broker.
* Brokers update their local metadata cache and may perform any necessary connection setup.

### 6) Optional: Controller triggers rebalancing and partition reassignment

With the new broker now part of cluster metadata, the controller may decide to rebalance replicas and leadership to utilize the new capacity:

* Each reassignment or leader movement is a metadata change that must be proposed and committed to the Raft log.
* Once committed, brokers receive the updated partition assignments and either fetch new replicas or truncate existing replicas as needed.
* Reassignments are applied incrementally and are visible only after the metadata commit.

### 7) Final commit and new cluster state

After registration and any reassignments are committed:

* The metadata log persists the cluster state transitions.
* The cluster transitions to the updated state where the new broker can participate in serving replicas, accepting produce/consume traffic per the committed metadata.

## Component responsibilities (at a glance)

| Component         | Responsibility                                  | Example actions                                                |
| ----------------- | ----------------------------------------------- | -------------------------------------------------------------- |
| Controller leader | Coordinates metadata changes                    | Validate registration, propose Raft entry, respond on commit   |
| Controller quorum | Provides fault-tolerant metadata replication    | Run leader election, acknowledge AppendEntries, commit entries |
| New broker        | Requests to join and applies committed metadata | Send register request, read metadata, fetch replicas           |

## Important notes and guarantees

* A leader-coordinated, quorum-committed metadata change ensures consistency and durability across controller failures.
* Any control-plane operation (broker join, topic/partition creation, config change) follows the same propose-and-commit Raft lifecycle.
* Rebalancing only becomes authoritative after a commit to the metadata log; until committed, changes are not visible cluster-wide.

## Summary

KRaft centralizes control-plane operations in Raft-backed controllers. When a broker joins:

* It registers with the controller leader.
* The registration is proposed to the Raft metadata log and must be committed by a quorum.
* Once committed, the broker is acknowledged and cluster metadata is updated; rebalancing follows the same commit lifecycle.

This architecture replaces ZooKeeper-based coordination with a Raft-consistent metadata log, improving operational simplicity and providing strong consistency for metadata operations.

## Links and references

* [Raft consensus algorithm](https://raft.github.io/)
* [Apache Kafka KRaft documentation](https://kafka.apache.org/documentation/#kraft)
* [ZooKeeper project (for comparison)](https://zookeeper.apache.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/f928821c-14b1-49d0-83cb-414074d06e1a" />
</CardGroup>
