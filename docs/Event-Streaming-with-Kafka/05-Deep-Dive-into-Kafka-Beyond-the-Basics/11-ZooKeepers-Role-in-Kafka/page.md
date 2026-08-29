# ZooKeepers Role in Kafka

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Deep-Dive-into-Kafka-Beyond-the-Basics/ZooKeepers-Role-in-Kafka/page

Explains ZooKeeper's historical role in Kafka cluster coordination, covering broker registration, controller election, metadata storage, notifications, offset history, operational risks, and KRaft replacement.

Hello and welcome back.

In this lesson we explore the role ZooKeeper has historically played in Apache Kafka's cluster coordination. Using our EV charging-station example, Kafka ingests live events from many stations, partitions them across brokers, and exposes up-to-date availability to producers and consumers (for example, a mobile app or a dashboard). The architecture looks like this:

<Frame>
  <img alt="The image illustrates Kafka's role in managing charging stations, showing how different stations are assigned to partitions across brokers, with a focus on the live status of free charging stations." />
</Frame>

Kafka must coordinate many real-time responsibilities: maintaining consistent topic metadata, handling broker additions/removals, managing producer and consumer membership (consumer groups), assigning partition leaders, and ensuring consumer offsets are reliably available. Historically, Apache ZooKeeper provided the coordination and metadata services that made these operations possible and deterministic.

Below we enumerate the operational complexities Kafka faces and show how ZooKeeper addressed them.

The first issue is lack of coordinated cluster state management. Broker leadership, partition ownership, and offset tracking must be managed consistently across the cluster; without a coordination service these tasks are error-prone and can lead to incorrect processing.

<Frame>
  <img alt="The image is a diagram titled &#x22;Kafka - ZooKeeper's Role,&#x22; highlighting issues like lack of coordination due to complex and error-prone management of broker leadership, partition ownership, and consumer offsets." />
</Frame>

Undetected failures are the next major concern. If a broker fails and replicas are not quickly promoted or re-synchronized, consumers can miss messages or read stale data — causing data loss or service disruption.

<Frame>
  <img alt="The image illustrates Kafka's ZooKeeper role, showing a sequence of events starting with a broker failure leading to service disruptions and potential data loss under undetected failures." />
</Frame>

Manual membership management becomes a burden as clusters scale. When brokers are added or removed — manually or via autoscaling — the cluster needs an automated, consistent way to update membership and rebalance partitions without human intervention.

<Frame>
  <img alt="The image illustrates the role of ZooKeeper in Kafka, highlighting manual membership management using brokers with symbols indicating addition or removal." />
</Frame>

Inconsistent or rogue broker configuration is another operational risk. A misconfigured broker that joins the cluster can receive partition assignments or otherwise destabilize the cluster; without a single source of truth, rebalancing and recovery can become chaotic.

Operational complexity and single points of failure amplify these risks: a component that manages cluster state going down can impair the cluster’s ability to perform coordinated changes.

<Frame>
  <img alt="The image illustrates the role of ZooKeeper in Kafka, highlighting a &#x22;Single Point of Failure&#x22; between a broker and critical information management, with a mention of a quorum mechanism." />
</Frame>

Offset management is critical. Consumers must reliably persist and retrieve offsets so message processing can resume correctly after failures or restarts. If offsets are lost or inconsistent, consumers can reprocess messages or skip them, both of which break correctness guarantees.

<Frame>
  <img alt="The image illustrates Kafka's role with ZooKeeper, focusing on the complexity of offset management and the difficulty in tracking without a centralized store, highlighting consumer offsets in a queue." />
</Frame>

How does ZooKeeper help?

When deploying Kafka historically, you also deployed a ZooKeeper ensemble. ZooKeeper runs as a quorum (typically an odd number like 3 or 5) so it can tolerate failures while requiring a majority for agreement. One ZooKeeper node is elected leader and the others are followers. ZooKeeper provides a consistent, reliable store and a notification mechanism for cluster metadata.

Key interaction points between ZooKeeper and Kafka:

* Brokers register their presence with ZooKeeper when they start; ZooKeeper maintains a dynamic registry of active brokers.
* ZooKeeper coordinates election of the Kafka controller (a special broker process). The controller assigns partition leaders and triggers leader elections among replicas when failures occur. ZooKeeper mediates controller election and stores the necessary metadata so the controller decision is consistent across the cluster.
* Topic configurations (number of partitions, replication factor, and other topic settings) are stored in ZooKeeper so all brokers share the same metadata view.
* ZooKeeper acts as a notification hub: when a broker fails, restarts, or when topics change, ZooKeeper notifies interested brokers and clients so they can react and reconfigure.

<Frame>
  <img alt="The image illustrates the role of ZooKeeper in a Kafka architecture, depicting a ZooKeeper ensemble with servers and brokers, highlighting the leader-follower configuration." />
</Frame>

Because ZooKeeper maintains consistent cluster metadata and provides reliable notifications, it enables coordinated controller election, membership management, and configuration propagation — all essential for high availability and correctness.

Here are the key roles ZooKeeper has historically played in Kafka:

* Maintain a dynamic registry of active brokers so the cluster knows its members and can make partition assignments reliably.
* Mediate controller election and, through the controller, assist in leader election for partitions to ensure a single authoritative leader per partition for reads and writes.
* Store topic metadata and configuration centrally so all brokers observe consistent settings (partitions, replication factors, topic configs).
* Serve as an event/notification system that informs brokers about cluster state changes (broker failure, topic changes), enabling coordinated responses.

<Frame>
  <img alt="The image outlines the role of ZooKeeper in Kafka, highlighting four functions: maintaining a dynamic registry of brokers, electing leaders for partitions, managing topic configurations, and acting as a notification system." />
</Frame>

Summary table — problems vs. how ZooKeeper addressed them:

| Problem                               | Impact                                               | How ZooKeeper helped                                                            |
| ------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| Cluster state inconsistency           | Wrong leader assignment, split-brain, stale metadata | Centralized store for broker/topic metadata and controller election             |
| Undetected broker failures            | Data loss, stale reads                               | Failure detection + controller-triggered leader elections and replica promotion |
| Manual membership/configuration drift | Operational overhead, misconfigurations              | Dynamic broker registry and centralized topic configs                           |
| Offset storage (historically)         | Incorrect consumer progress after restarts           | Initially stored offsets in ZooKeeper (later moved to Kafka internal topic)     |

Operational notes

* ZooKeeper quorum: Kafka depends on a ZooKeeper ensemble for certain control plane operations. The ensemble is available as long as a majority of ZooKeeper nodes are up; if the quorum fails, critical operations (for example, electing a new controller) cannot complete.
* Offset storage history: Older Kafka consumer clients stored offsets in ZooKeeper. Since the 0.9 consumer API and later, offsets are stored in an internal Kafka topic named `__consumer_offsets`, reducing direct dependency on ZooKeeper for offset storage while ZooKeeper continued to manage cluster metadata in those releases.

<Callout icon="lightbulb">
  Note: Kafka is evolving. Newer Kafka architectures (the KRaft mode introduced as part of [KIP-500: Replace ZooKeeper with a Kafka based metadata quorum](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Kafka+based+metadata+quorum) and production-ready in later releases) remove the ZooKeeper dependency by integrating the metadata quorum into Kafka itself. Whether your cluster uses ZooKeeper or KRaft depends on the Kafka version and deployment choices.
</Callout>

Recommended hands-on exercise

1. Stand up a local ZooKeeper ensemble and a small Kafka cluster (3 ZooKeeper nodes, 3 Kafka brokers).
2. Observe broker registration with ZooKeeper and the controller election:
   * Start ZooKeeper: `bin/zookeeper-server-start.sh config/zookeeper.properties`
   * Start Kafka: `bin/kafka-server-start.sh config/server.properties`
   * Inspect ZooKeeper znodes: `bin/zookeeper-shell.sh localhost:2181 ls /`
3. Create a topic and observe leader assignment and partition replicas:
   * Create topic: `bin/kafka-topics.sh --create --topic test-topic --partitions 3 --replication-factor 2 --bootstrap-server localhost:9092`
   * Describe topic: `bin/kafka-topics.sh --describe --topic test-topic --bootstrap-server localhost:9092`
4. Simulate a broker failure and watch Kafka/ZooKeeper handle controller and leader changes (stop one broker, then describe the topic again).

These exercises will help you inspect the ZooKeeper metadata that Kafka relies on and see coordinated cluster actions in real time.

In summary, ZooKeeper has historically provided Kafka with external coordination: broker discovery, controller election, configuration and metadata storage, and cluster notifications. Understanding this separation of concerns is important when operating, troubleshooting, and planning upgrades for Kafka clusters.

That is it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/658b8d51-f23e-4dc6-b30c-378aee128b3b" />
</CardGroup>
