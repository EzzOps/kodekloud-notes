# change to the Kafka installation directory
cd /root/kafka

# list the top-level files
ls -l
```

The Kafka command-line scripts live in the `bin` directory. Change into `bin` to see helper scripts used for managing Kafka:

```bash theme={null}
cd /root/kafka/bin
ls -l
```

Example excerpt (truncated):

```text theme={null}
-rwxr-xr-x 1 root root   863 Sep 13  2022 kafka-topics.sh
-rwxr-xr-x 1 root root   895 Sep 13  2022 kafka-console-producer.sh
-rwxr-xr-x 1 root root   723 Sep 13  2022 kafka-console-consumer.sh
-rwxr-xr-x 1 root root  1010 Sep 13  2022 kafka-server-start.sh
...
```

## Quick reference: common Kafka CLI commands

| Purpose                    | Command example                                                                                                                        |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Create or manage topics    | `./kafka-topics.sh --create --topic <name> --bootstrap-server localhost:9092`                                                          |
| Describe topic metadata    | `./kafka-topics.sh --describe --topic <name> --bootstrap-server localhost:9092`                                                        |
| Change topic config        | `./kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name <name> --alter --add-config retention.ms=...` |
| Broker API versions & list | `./kafka-broker-api-versions.sh --bootstrap-server localhost:9092`                                                                     |

## Create a simple topic

Create a topic named `demo_topic` with the Kafka topics script:

```bash theme={null}
# create a topic named demo_topic
./kafka-topics.sh --create --topic demo_topic --bootstrap-server localhost:9092
```

What the flags mean:

* `--create` — create a new topic.
* `--topic demo_topic` — the topic name.
* `--bootstrap-server localhost:9092` — address of a broker to bootstrap against (replace with your cluster's bootstrap server(s)).

Typical response:

```bash theme={null}
WARNING: Due to limitations in metric names, topics with a period ('.') or underscore ('_') could collide. To avoid issues it is best to use either, but not both.
Created topic demo_topic.
```

You can also verify the newly created topic using a web UI such as `Kafdrop` or Confluent Control Center.

<Frame>
  <img alt="The image is a screenshot of a Kafdrop interface showing a Kafka Cluster Overview, including details about bootstrap servers, brokers, and topics." />
</Frame>

Clicking the topic in the UI will display configuration and partition metadata.

## Create a topic with partitions and replication

Partitions increase throughput and parallelism by spreading data across brokers. Create a topic with three partitions and a replication factor of 1:

```bash theme={null}
./kafka-topics.sh --create --topic partitioned_topic --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
```

Best practices:

<Callout icon="lightbulb">
  Align partition counts to your throughput and consumer parallelism needs. More partitions can improve parallelism but add overhead for management, disk usage, and leader elections.
</Callout>

<Callout icon="warning">
  Replication factor must not exceed the number of available brokers. If you set `--replication-factor` greater than your broker count, topic creation will fail.
</Callout>

## Describe a topic (inspect metadata)

To view topic metadata—partition count, leader, replicas, in-sync replicas (ISR), and per-topic configs—use the `--describe` option:

```bash theme={null}
./kafka-topics.sh --describe --topic partitioned_topic --bootstrap-server localhost:9092
```

Sample output:

```bash theme={null}
Topic: partitioned_topic    TopicId: X8KJGSg5hThQHfo3DTm3eg    PartitionCount: 3    ReplicationFactor: 1    Configs: segment.bytes=1073741824
    Partition: 0    Leader: 1    Replicas: 1    Isr: 1
    Partition: 1    Leader: 1    Replicas: 1    Isr: 1
    Partition: 2    Leader: 1    Replicas: 1    Isr: 1
```

## Change topic configuration (retention example)

Topic-level configurations can be updated with `kafka-configs.sh`. For example, set retention to 2 days (milliseconds):

```bash theme={null}
# set retention to 2 days (in milliseconds)
./kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name partitioned_topic --alter --add-config retention.ms=172800000
```

Expected response:

```bash theme={null}
Completed updating config for topic partitioned_topic.
```

Verify the change by re-describing the topic:

```bash theme={null}
./kafka-topics.sh --describe --topic partitioned_topic --bootstrap-server localhost:9092
```

Sample updated output showing `retention.ms`:

```bash theme={null}
Topic: partitioned_topic    TopicId: X8KJGSg5hThQHfo3DTm3eg    PartitionCount: 3    ReplicationFactor: 1    Configs: segment.bytes=1073741824,retention.ms=172800000
    Partition: 0    Leader: 1    Replicas: 1    Isr: 1
    Partition: 1    Leader: 1    Replicas: 1    Isr: 1
    Partition: 2    Leader: 1    Replicas: 1    Isr: 1
```

## Inspect broker API versions and broker list

To confirm broker identities and supported API versions (useful when troubleshooting compatibility or determining available features), run:

```bash theme={null}
./kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

Sample output (truncated):

```bash theme={null}
kafka-node:9092 (id: 1 rack: null) ->
    Produce(0): 0 to 9 [usable: 9],
    Fetch(1): 0 to 13 [usable: 13],
    ListOffsets(2): 0 to 7 [usable: 7],
    Metadata(3): 0 to 12 [usable: 12],
    LeaderAndIsr(4): 0 to 6 [usable: 6],
    ...
    CreatePartitions(37): 0 to 3 [usable: 3],
    DescribeCluster(60): 0 [usable: 0]
```

In this lab you have a single broker (sufficient for practicing topic creation and configuration changes). In production, use at least three brokers for fault tolerance and to support replication.

## Further reading and resources

* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
* [Kafdrop (open-source Kafka web UI)](https://github.com/obsidiandynamics/kafdrop)
* [Confluent Control Center](https://www.confluent.io/product/control-center)

That is it for this lesson. See you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/ee6ed9ab-202a-4dfc-bcd5-8a6941e1440b/lesson/8c70b1fb-467f-4b96-8bc5-c05ee4c2e5af" />
</CardGroup>


# Kafka Brokers The Foundation of Message Storage

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Building-Blocks-of-Kafka/Kafka-Brokers-The-Foundation-of-Message-Storage/page

Explains Kafka brokers as durable, scalable servers for storing and serving event streams using an EV charging use case, covering replication, partitions, scalability, and operations

Welcome back. In this lesson we’ll drill into the core Kafka components that provide durable, scalable message storage: Kafka brokers and how they operate in a cluster. To make the concepts concrete, we’ll continue using our EV charging use case.

Producers (for example, EV charging stations) publish events to a logical stream called a topic. Consumers (the app, analytics, billing, or monitoring services) read those topics to act on data. Where are these events stored? On Kafka brokers — the servers that persist and serve message data for the cluster.

<Frame>
  <img alt="The image is a flowchart illustrating how Kafka is used to provide real-time updates on EV charger availability, power levels, and maintenance status, featuring charging sessions, station status, and payment systems." />
</Frame>

Use case: charging station status reports

* When a user searches for available chargers, the app must show free/occupied status for a given time window.
* Each charging station (producer) emits status and availability events to a topic (for example, `charger-status`).
* The authoritative, persisted stream of those events lives on Kafka brokers. Consumers read and materialize the current availability view as needed.

What is a Kafka broker?
A Kafka broker is the server process that stores topic data on disk, serves client requests for reads and writes, and coordinates with other brokers for replication and leadership. Brokers are the backbone of Kafka’s durability and throughput.

<Frame>
  <img alt="The image is a diagram illustrating the role of a Kafka broker in managing message storage within an EV charging station network. It shows data flow between charging stations, brokers, and consumers, emphasizing Kafka's role in storing and managing messages in a cluster." />
</Frame>

Key characteristics of Kafka brokers

|                          Feature | What it does                                                                                                         | Relevance to EV charging use case                                                             |
| -------------------------------: | -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
|               Message management | Persists messages to disk, serves producer writes and consumer reads, enforces retention and partition ordering      | Ensures status events are durably stored and can be replayed to rebuild state                 |
|                     Cluster node | Each broker is a node that participates in the distributed cluster                                                   | Multiple brokers provide capacity and redundancy for high availability                        |
| Partition placement & leadership | Topics are split into partitions; a leader broker handles reads/writes for each partition, followers act as replicas | Partitioning allows parallelism (throughput) for many chargers; leaders handle client traffic |
|                      Scalability | Add brokers to distribute partitions and load horizontally                                                           | Scale ingestion as more chargers or regions are added                                         |
|     Fault tolerance & durability | Replication across brokers protects against data loss; followers can be promoted if a leader fails                   | Maintains accurate charger state despite broker failure                                       |
|               Dynamic membership | Brokers can join/leave; the cluster controller reassigns leadership/replicas as needed                               | Enables rolling upgrades and elastic growth without service disruption                        |

Operational examples

* Inspect topic partitions and replication:

```bash theme={null}
bin/kafka-topics.sh --bootstrap-server broker:9092 --describe --topic charger-status
```

* Produce a sample status event:

```bash theme={null}
echo '{"chargerId":"C-100","status":"AVAILABLE","timestamp":"2026-07-15T10:00:00Z"}' | \
  bin/kafka-console-producer.sh --broker-list broker:9092 --topic charger-status
```

* Consume latest events to verify state:

```bash theme={null}
bin/kafka-console-consumer.sh --bootstrap-server broker:9092 --topic charger-status --from-beginning --max-messages 10
```

<Frame>
  <img alt="The image explains key features of Kafka Broker including message management, cluster node, scalability, fault tolerance, and dynamic membership. Each feature is briefly described in relation to message storage and cluster functionality." />
</Frame>

<Callout icon="lightbulb">
  Retention vs durability: Kafka persists messages to disk and applies retention rules (time- or size-based). Replication across brokers provides durability — preventing data loss — while retention determines how long data remains queryable in the cluster.
</Callout>

Real-world scale and examples
Large companies run Kafka at vast scale to support real-time systems. Examples include:

* Netflix — thousands of brokers across many clusters for event-driven streaming and personalization.
* Pinterest — multi-trillion messages per day at very high throughput.
* PayPal — large broker fleets to provide reliable transaction and event delivery.
* LinkedIn — Kafka’s originator, operating large clusters for core real-time pipelines.

<Frame>
  <img alt="The image showcases the logos of four companies alongside text that highlights Pinterest's daily message usage and data storage statistics, illustrating Kafka's role in message storage." />
</Frame>

These deployments demonstrate how brokers deliver throughput, durability, and availability for streaming use cases — from payments to IoT and social platforms.

<Frame>
  <img alt="The image shows several company logos with text describing Kafka Broker as a foundation for message storage, noting LinkedIn's significant usage statistics." />
</Frame>

Summary
Kafka brokers are the durable storage and serving layer for event streams. In the EV charging scenario they store charger status events, enable replay and state reconstruction, and scale horizontally to support large fleets and high throughput.

Links and references

* [Apache Kafka documentation](https://kafka.apache.org/documentation/)
* [Kafka operations: topics, partitions, and replication](https://kafka.apache.org/documentation/#basic_ops)
* [Designing for durability and availability with Kafka](https://kafka.apache.org/intro)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/ee6ed9ab-202a-4dfc-bcd5-8a6941e1440b/lesson/503a0eea-65bd-4578-875c-4827c949f268" />
</CardGroup>
