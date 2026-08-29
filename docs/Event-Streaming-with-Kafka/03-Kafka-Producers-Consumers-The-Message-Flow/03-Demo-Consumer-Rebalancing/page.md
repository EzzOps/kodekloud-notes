# Demo Consumer Rebalancing

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Producers-Consumers-The-Message-Flow/Demo-Consumer-Rebalancing/page

Demo showing how to create a multi-partition Kafka topic, produce keyed messages, and run consumers in a group to observe automatic partition rebalancing as consumers join and leave.

Welcome back.

This practical demo shows Kafka consumer rebalancing in action. You'll create a topic with multiple partitions, produce keyed messages so they land in specific partitions, and run multiple consumers in the same consumer group to observe how Kafka redistributes partition ownership as group membership changes.

What we'll do

* Create a Kafka topic with 4 partitions
* Produce keyed messages using a Python producer so messages map deterministically to partitions
* Run Python consumers that join the same consumer group and observe rebalancing when consumers join/leave

Prerequisites

* Kafka is installed and running on the host used in this demo (`localhost:9092`)
* Python 3.8+ (or compatible) available

Quick commands

| Task               | Command / File                                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Create topic       | `./kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 4 --topic consumer-rebalancing-demo` |
| Create Python venv | `python3 -m venv kafka-demo-env`                                                                                                                 |
| Activate venv      | `source kafka-demo-env/bin/activate`                                                                                                             |
| Install client     | `pip install kafka-python`                                                                                                                       |
| Producer script    | `producer.py`                                                                                                                                    |
| Consumer script    | `consumer.py`                                                                                                                                    |

Useful references

* [Apache Kafka documentation](https://kafka.apache.org/documentation/)
* [kafka-python on PyPI](https://pypi.org/project/kafka-python/)

***

## 1) Create the topic (4 partitions)

Create a topic named `consumer-rebalancing-demo` with 4 partitions and replication factor 1:

```bash theme={null}
/root/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 4 --topic consumer-rebalancing-demo
```

This registers the topic with the local Kafka broker running on `localhost:9092`.

***

## 2) Prepare a Python virtual environment and install kafka-python

Update packages and enable the Python venv module (if needed). Then create and activate a virtual environment and install `kafka-python`:

```bash theme={null}
sudo apt update
sudo apt install -y python3.8-venv
