# Course Introduction

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Introduction/Course-Introduction/page

Introduction to Apache Kafka event streaming, covering core concepts, producers and consumers, partitioning strategies, hands-on labs, Docker sandbox, and cloud integration with IAM

Welcome to "Event Streaming with Kafka."

I'm Raghunandana Krishnamurthy — your instructor for this course. This class focuses on Apache Kafka, the industry-standard platform for building scalable, fault-tolerant, low-latency event streaming systems used by organizations like Netflix and LinkedIn. Through lectures and hands-on labs, you'll learn the core concepts and practical skills needed to design, build, and operate real-time data pipelines.

Quick highlights:

* Learn Kafka fundamentals: topics, partitions, brokers, and clusters.
* Understand producer and consumer workflows and tuning knobs for throughput, latency, and durability.
* Practice message keys and partitioning strategies to ensure ordering, locality, and parallelism.
* Complete a hands-on project that includes cloud-based components (IAM) and a brief comparison with Confluent’s enhanced platform.

To get started locally, launch a Kafka-enabled sandbox using the lensesio fast-data-dev Docker image. This gives you a single-node playground with producers, consumers, and a management UI.

```bash theme={null}
docker network create kafka-net

docker run --rm -d \
  --network kafka-net \
  -p 2182:2181 \
  -p 3030:3030 \
  -p 9091:9091 \
  -p 8081:8081 \
  -e ADV_HOST=kafka-cluster \
  --name kafka-cluster \
  lensesio/fast-data-dev
```

This setup provides a convenient playground for producers, consumers, and the Kafka management UI included in the image.

<Frame>
  <img alt="The image illustrates event streaming with a server sending packets to a television, where a person is watching breaking news. It also features a speaker from KodeKloud explaining the concept." />
</Frame>

Core building blocks

* Topics: Named streams where records are published.
* Partitions: Ordered, immutable sequences of records within a topic that enable parallelism.
* Brokers: Kafka server processes that host partitions and serve client requests.
* Clusters: Groups of brokers that collectively manage topics and replication for durability.

| Component | Purpose                                | Example / Note                          |
| --------- | -------------------------------------- | --------------------------------------- |
| Topic     | Logical feed name for records          | `user-events`                           |
| Partition | Parallelism and ordering unit          | `user-events` partition 0,1,2           |
| Broker    | Kafka server process                   | `kafka-1.example.com`                   |
| Cluster   | Collection of brokers for HA & scaling | 3+ brokers with replication factor >= 2 |

Moving beyond architecture, the course explains message flow: how producers send data, how consumers subscribe and fetch records, and how configuration options (acks, retries, batch size, linger.ms, compression) influence performance.

<Frame>
  <img alt="The image shows a person sitting at a desk with a microphone, wearing a &#x22;KodeKloud&#x22; shirt. On the left, there is a list of topics related to event streaming using Kafka." />
</Frame>

Message keys and partitioning
Understanding message keys is essential for designing ordering and data locality. Keys determine which partition a record is written to (via the partitioner), which affects consumer parallelism and ordering guarantees for keyed data. We cover strategies for key selection, deterministic partitioning, and when to rely on round-robin partitioning.

<Frame>
  <img alt="The image is an illustration explaining the role of message keys in Kafka, showing how a producer sends messages to different brokers and partitions. A person is speaking in the bottom right corner, likely explaining the concept." />
</Frame>

Hands-on project and cloud integration
You will apply course concepts to a real-world streaming project. Parts of the project touch on cloud resources where IAM roles may be required (for EC2, Lambda, IAM-integrated services). Below is an example of a minimal AWS trust policy that allows EC2 to assume a role:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sts:AssumeRole"
      ],
      "Principal": {
        "Service": [
          "ec2.amazonaws.com"
        ]
      }
    }
  ]
}
```

<Callout icon="warning">
  When using IAM roles, follow the principle of least privilege. Only grant the permissions required for the workload and rotate credentials where applicable.
</Callout>

We also include a short comparison with Confluent Kafka to highlight managed features and enterprise extensions so you can evaluate upstream Apache Kafka vs. managed distributions.

<Callout icon="lightbulb">
  Hands-on labs are the best way to learn Kafka. Expect to experiment, make mistakes, and iterate—these labs are designed to simulate production-like scenarios so you can build confidence.
</Callout>

Why learn Kafka with KodeKloud?
We provide the right infrastructure and timing to practice concepts alongside the lessons. KodeKloud offers lab environments, community support, and guided exercises so you can follow along, reinforce learning, and prepare for real-world challenges.

Join the community to ask questions, share solutions, and grow your event-streaming skills.

Links and references

* Kafka official docs: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
* Confluent: [https://www.confluent.io/](https://www.confluent.io/)
* Lenses fast-data-dev (Docker image): [https://hub.docker.com/r/lensesio/fast-data-dev](https://hub.docker.com/r/lensesio/fast-data-dev)
* AWS IAM roles: [https://docs.aws.amazon.com/IAM/latest/UserGuide/id\_roles.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
* AWS EC2: [https://aws.amazon.com/ec2/](https://aws.amazon.com/ec2/)

Let's begin.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/37830f43-1d16-4aa1-899d-2c6914ee72b0/lesson/ed42b38c-b387-4ec9-a6c2-273b37af0065" />
</CardGroup>
