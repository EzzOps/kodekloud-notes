# Download and extract Kafka binary
wget https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz
tar -xzf kafka_2.13-3.0.0.tgz
cd kafka_2.13-3.0.0
ls -l
```

The Kafka distribution contains `config`, `bin`, and `libs` — Kafka Connect is bundled, so no separate Connect install is required. Connector-specific JARs (for S3) will be added later.

## Install Java

KRaft and Kafka need a JDK. Check if Java is installed:

```bash theme={null}
java -version
# If not installed you will typically see: "bash: java: command not found"
```

Install Amazon Corretto 8 (or another supported JDK) if Java is missing:

```bash theme={null}
sudo yum install -y java-1.8.0-amazon-corretto
java -version
# Expected output example:
# openjdk version "1.8.0_442"
# OpenJDK Runtime Environment Corretto-8.442.06.1 (build 1.8.0_442-b06)
# OpenJDK 64-Bit Server VM Corretto-8.442.06.1 (build 25.442-b06, mixed mode)
```

## Format storage for KRaft metadata

KRaft stores metadata locally and requires initializing the storage directory with a cluster UUID.

Generate a UUID:

```bash theme={null}
# Generate a UUID for KRaft metadata storage
bin/kafka-storage.sh random-uuid
# Example output: IEDtYa9aQA8Wg7x8FWoQ
```

Use the UUID to format the storage path referenced in your KRaft config (adjust the path if you extracted Kafka elsewhere):

```bash theme={null}
bin/kafka-storage.sh format -t IEDtYa9aQA8Wg7x8FWoQ -c ~/kafka_2.13-3.0.0/config/kraft/server.properties
# Expected output:
# Formatting /tmp/kraft-combined-logs
```

## Edit the KRaft server.properties

Open `config/kraft/server.properties` and update the settings required for a single-node KRaft cluster. Key items:

* Enable both broker and controller roles: `process.roles=broker,controller`
* Assign a node id: `node.id=1`
* Define controller quorum voters for a single-node cluster
* Bind listeners to all interfaces (`0.0.0.0`)
* Set `inter.broker.listener.name`
* Advertise the EC2 public IP so remote clients can connect

Example entries to add or modify in `server.properties`:

```properties theme={null}
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093
listeners=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
inter.broker.listener.name=PLAINTEXT
advertised.listeners=PLAINTEXT://<EC2_PUBLIC_IP>:9092
```

Replace `<EC2_PUBLIC_IP>` with your instance's public IP (copy from the EC2 console) and save the file.

## Open the Kafka broker port in the security group

Before starting the broker, allow inbound traffic on TCP port `9092` in your instance's security group so clients can reach Kafka.

<Callout icon="warning">
  For production or organizational environments, never open Kafka to the entire internet. Restrict inbound rules to specific IP ranges (for example, your office IP or VPN CIDR). Allowing `0.0.0.0/0` exposes your cluster to attacks.
</Callout>

<Frame>
  <img alt="The image shows an AWS console interface for editing inbound rules, displaying security group settings for allowing specific traffic types and port ranges. There is a warning about rules allowing access from all IP addresses." />
</Frame>

## Start the KRaft Kafka service

Start Kafka with the KRaft configuration:

```bash theme={null}
bin/kafka-server-start.sh ~/kafka_2.13-3.0.0/config/kraft/server.properties
```

The server log streams to the terminal. Review the output for successful controller and broker startup messages and confirm that listeners bind to ports `9092` and `9093`. Watch for fatal errors — if you see errors, check the `server.properties` values and the storage format step.

<Frame>
  <img alt="The image shows an AWS EC2 management console with details of a running instance named &#x22;kafka_s3_demo,&#x22; including its state, type, and IP addresses." />
</Frame>

## What’s next

With a single-node KRaft broker+controller up and reachable, the next lessons will cover:

* Downloading and installing an S3 connector (Confluent S3 connector or a community connector)
* Preparing the connector configuration (including AWS credentials and S3 bucket settings)
* Running Kafka Connect and syncing topic data to S3

Links and references

* [Confluent S3 Connector](https://www.confluent.io/hub/confluentinc/kafka-connect-s3)
* [KRaft (KIP-500) overview and Kafka documentation](https://kafka.apache.org/documentation/)
* [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)

That’s it for this lesson — in the follow-up article we’ll install and configure the S3 connector and run a demo sync from a Kafka topic to S3.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/68c7ef21-4d7c-405e-8fae-5500f90b82a2/lesson/3648235d-a2f3-4d78-bb04-7995ee8ebb0d" />
</CardGroup>


# Demo Kafka Connect in Action

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Connect-Effortless-Data-Pipelines/Demo-Kafka-Connect-in-Action/page

Demonstration of producing Kafka events to a topic and using Kafka Connect S3 sink to write those events as JSON files into an S3 bucket.

Welcome back. In this lesson you'll produce events into the `cartevent` Kafka topic and observe how a Kafka Connect S3 sink moves those events into an S3 bucket. This walkthrough covers the producer commands, example events, and what to expect in S3 once the sink flushes data.

## Prerequisites

* A running Kafka broker accessible from the EC2 instance (example uses `98.81.233.254:9092`).
* Kafka Connect configured with an S3 sink connector that writes to your target bucket.
* Access to the EC2 instance that hosts Kafka Connect and Kafka client tools.

## Step 1 — Start a console producer

Open a terminal on the EC2 instance where Kafka is installed, become root, and change directory to the Kafka installation (the folder that contains the `bin` directory). Then start the Kafka console producer and point it at the `cartevent` topic:

```bash theme={null}
