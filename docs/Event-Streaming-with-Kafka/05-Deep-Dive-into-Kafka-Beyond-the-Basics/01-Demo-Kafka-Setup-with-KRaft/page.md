# Demo Kafka Setup with KRaft

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Deep-Dive-into-Kafka-Beyond-the-Basics/Demo-Kafka-Setup-with-KRaft/page

Step-by-step guide to setting up Apache Kafka in KRaft mode on CentOS including config inspection, generating cluster ID, formatting metadata storage, starting broker, and verifying logs.

Welcome back. In this lesson we walk through setting up Apache Kafka in KRaft (Kafka Raft Metadata) mode on a CentOS (KodeKloud Lab) machine. This step-by-step guide covers downloading Kafka, inspecting KRaft configuration, generating a cluster ID, formatting local metadata storage, starting Kafka in KRaft mode, and verifying the startup logs.

Why KRaft?

* KRaft removes the dependency on ZooKeeper by storing cluster metadata in a Raft quorum.
* Recommended for new Kafka deployments, since Kafka is migrating metadata management to KRaft.

Overview

* Download a Kafka release
* Extract and inspect the Kafka directory
* Inspect `config/kraft` and key KRaft config files
* Generate a cluster ID (UUID)
* Format local storage for KRaft metadata
* Start Kafka in KRaft mode and verify logs

Prerequisites

* CentOS (or similar Linux) with wget and tar installed
* Java installed and JAVA\_HOME configured
* Sufficient disk space for Kafka logs (default uses `/tmp` unless changed in config)

Download and extract Apache Kafka

1. Download Kafka 3.0.0 (Scala 2.13) tarball:

```bash theme={null}
wget https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz
```

Example wget output (truncated):

```text theme={null}
Resolving archive.apache.org... connected.
HTTP request sent, awaiting response... 200 OK
Length: 86396520 (82M) [application/x-gzip]
Saving to: ‘kafka_2.13-3.0.0.tgz’

kafka_2.13-3.0.0.tgz   100%[====================================>]  82.39M   22.4MB/s    in 4.5s
‘kafka_2.13-3.0.0.tgz’ saved [86396520/86396520]
```

2. Extract the archive:

```bash theme={null}
tar -xvf kafka_2.13-3.0.0.tgz
```

Inspect the Kafka directory

Change into the extracted directory and list the top-level contents:

```bash theme={null}
cd kafka_2.13-3.0.0
ls -lrt
```

You should see familiar top-level folders such as `config`, `bin`, `libs`, and `site-docs`.

Inspect the config directory and KRaft-specific configs

Change into `config` and examine KRaft-related files:

```bash theme={null}
cd config
ls -lrt
```

There is a dedicated `kraft/` subdirectory containing KRaft config files:

```bash theme={null}
cd kraft
ls -lrt
```

Common contents of `config/kraft`:

| File                    | Purpose                                                     |
| ----------------------- | ----------------------------------------------------------- |
| `server.properties`     | Main server configuration used to start Kafka in KRaft mode |
| `controller.properties` | Controller-specific tuning and Raft settings                |
| `broker.properties`     | Broker-specific settings for broker behavior                |
| `README.md`             | Notes and examples for KRaft configuration                  |

For simple single-node testing you often can use the defaults. For production clusters tune the `controller.properties` and `broker.properties` as needed.

Generate a cluster ID (random UUID)

KRaft stores metadata locally and requires an initial formatting step. First generate a cluster ID (a random UUID) using Kafka’s helper script:

```bash theme={null}
bin/kafka-storage.sh random-uuid
```

Sample output (your UUID will be different):

```text theme={null}
rRoS-vwkR9uEvWh5CaMwxw
```

Format the local storage with the generated UUID

Use the `kafka-storage.sh format` command to initialize the local metadata storage. Replace the UUID below with the one returned by `random-uuid`. Also point to the `server.properties` inside `config/kraft`.

```bash theme={null}
bin/kafka-storage.sh format -t rRoS-vwkR9uEvWh5CaMwxw -c ~/kafka_2.13-3.0.0/config/kraft/server.properties
```

What this does:

* Initializes the KRaft metadata directory (default path is typically `/tmp/kraft-combined-logs` unless changed in `server.properties`)
* Writes the initial metadata snapshot and prepares the node to become part of a Raft quorum

Start Kafka in KRaft mode

After formatting the storage, start the Kafka broker using the same `server.properties`:

```bash theme={null}
bin/kafka-server-start.sh ~/kafka_2.13-3.0.0/config/kraft/server.properties
```

When started, the broker runs with the KRaft controller logic enabled (no separate ZooKeeper or controller process needed for KRaft).

Verify KRaft startup in the logs

As Kafka starts in KRaft mode, the logs will include Raft and controller lifecycle events. Look for messages indicating Raft transitions, controller startup, and the broker listening on configured ports.

Example log excerpts (truncated):

```text theme={null}
[2025-04-17 14:18:02,580] INFO  [LogLoader partition=__cluster_metadata=0, dir=/tmp/kraft-combined-logs] Reloading from producer snapshot and rebuilding producer (kafka.Log)
[2025-04-17 14:18:03,196] INFO  [RaftManager nodeId=1] Completed transition to Candidate(state=localId=1, epoch=1, retries=1, electionTimeoutMs=1283) (org.apache.kafka.raft.QuorumState)
[2025-04-17 14:18:03,374] INFO  [RaftManager nodeId=1] Completed transition to Leader(localId=1, epoch=1, epochStartOffset=0, highWatermark=Optional.empty, voters=1) (org.apache.kafka.raft.QuorumState)
[2025-04-17 14:18:03,381] INFO  Starting controller (kafka.server.ControllerServer)
[2025-04-17 14:18:04,569] INFO  Awaiting socket connections on 0.0.0.0:9093. (kafka.network.Acceptor)
[2025-04-17 14:18:06,771] INFO  Kafka version: 3.0.0 (org.apache.kafka.common.utils.AppInfoParser)
[2025-04-17 14:18:06,772] INFO  [Kafka Server] started (kafka.server.KafkaServer)
[2025-04-17 14:18:06,894] INFO  [BrokerLifecycleManager id=1] The broker has been unfenced. Transitioning from RECOVERY to RUNNING. (kafka.server.BrokerLifecycleManager)
```

How to tell if KRaft is being used

* Look for Raft/Controller-related logs such as `RaftManager`, `KafkaRaftClient`, `ControllerServer` — these indicate KRaft mode.
* If ZooKeeper were in use, you would instead see ZooKeeper connection logs and `zookeeper.*` properties being used.

Configuration notes and key properties

Below are examples of server properties and status values you may see when running in KRaft mode. These illustrate that ZooKeeper is not used and show transaction/replication defaults.

```text theme={null}
transaction.state.log.min.isr = 1
transaction.state.log.num.partitions = 50
transaction.state.log.replication.factor = 1
transaction.state.log.segment.bytes = 104857600
transactional.id.expiration.ms = 604800000
unclean.leader.election.enable = false
zookeeper.connect = null
zookeeper.session.timeout.ms = null
zookeeper.set.acl = false
zookeeper.ssl.protocol = TLSv1.2
zookeeper.sync.time.ms = 2000
```

Common KRaft-related settings to review

| Setting                     | Purpose / Notes                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------- |
| `process.roles`             | Defines node roles (e.g., `broker,controller`) for combined or separate controller nodes |
| `node.id`                   | Unique numeric ID for the node in the Raft quorum                                        |
| `controller.listener.names` | Listener names for controller communication                                              |
| `controller.quorum.voters`  | List of controller voters in the Raft quorum                                             |
| `metadata.log.dir`          | Directory for metadata logs (default often under `/tmp` or configured path)              |

Recommendation

<Callout icon="lightbulb">
  For new Kafka deployments, prefer KRaft mode (ZooKeeper-less) because Kafka is moving towards KRaft for metadata management. Use the `config/kraft` files (`server.properties`, `controller.properties`, `broker.properties`) to tune controller and broker behavior as your cluster grows.
</Callout>

Troubleshooting tips

* If the broker fails to start, check that the `node.id`, `process.roles`, and `controller.quorum.voters` values are correct for your topology.
* Ensure the metadata directory specified in `server.properties` is writable by the Kafka process.
* If you see ZooKeeper-related settings populated, confirm you are using the `config/kraft/server.properties` file when formatting and starting Kafka.

Links and References

* Apache Kafka: [https://kafka.apache.org/](https://kafka.apache.org/)
* KRaft documentation: [https://kafka.apache.org/documentation/#kraft](https://kafka.apache.org/documentation/#kraft)
* ZooKeeper: [https://zookeeper.apache.org/](https://zookeeper.apache.org/)
* Kafka downloads archive: [https://archive.apache.org/dist/kafka/](https://archive.apache.org/dist/kafka/)

That is all for this lesson/article. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/771b0d3a-2c97-4e0e-840a-36e435c4f7da" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/9aa104e8-faa5-4099-977f-71744306b99d/lesson/bb6373a2-26b6-4c17-a2e0-a09bd240325c" />
</CardGroup>
