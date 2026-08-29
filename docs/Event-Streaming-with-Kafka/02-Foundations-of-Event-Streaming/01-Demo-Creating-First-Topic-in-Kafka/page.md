# Demo Creating First Topic in Kafka

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Foundations-of-Event-Streaming/Demo-Creating-First-Topic-in-Kafka/page

Guide to creating and configuring a Kafka topic using UI and CLI, explaining partitions, replication, retention, cleanup policies and best practices for development and production.

Hello and welcome back.

Earlier we set up a Kafka cluster using Docker and installed a Kafka UI to make exploration and management easier.

In this lesson we’ll create our first Kafka topic and walk through the common configuration options you’ll encounter when creating topics, both via the UI and the CLI.

## What is a Kafka topic?

* A topic is a named stream (or category) in Kafka where related events/messages are published and stored.
* Each topic is split into one or more partitions. Partitions provide parallelism and define message ordering within each partition.
* Topics include policies that govern retention and cleanup (how long messages are kept and how they’re removed).

## Create a topic using the Kafka UI

Open the Kafka UI, go to the Topics section, and click Add Topic.

* Enter a topic name (no spaces — the UI validates names and will show an error for invalid input).
* Choose the number of partitions. More partitions → more parallel consumers and higher throughput, but also more management overhead.
* Set retention (how long messages are retained). For local development a simple default is 1 partition and a 7-day retention.

<Frame>
  <img alt="The image shows a web interface for creating a new topic in Apache Kafka. It includes fields for topic name, number of partitions, cleanup policy, and other configuration options." />
</Frame>

After completing the fields (for example: Topic name = `KafkaLab`, Partitions = `1`, Retention = `7 days`), click Create Topic. The UI submits the configuration to the cluster and the topic is created.

## Create a topic from the command line

Creating topics from the CLI is useful for automation, scripts, and environments without a UI. Example using the bundled Kafka tools:

```bash theme={null}
