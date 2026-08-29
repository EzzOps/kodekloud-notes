# In the Session Manager shell
sudo su
cd
```

Install Kafka and Java

1. Download and extract Kafka (example uses Kafka 3.0.0 for Scala 2.13):

```bash theme={null}
# From the home directory
wget https://downloads.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz
tar -xzf kafka_2.13-3.0.0.tgz
cd kafka_2.13-3.0.0
ls -lrt
```

2. Check if Java is installed:

```bash theme={null}
java -version
# If Java is missing you'll see: java: command not found
```

3. Install OpenJDK 1.8 if needed:

```bash theme={null}
sudo yum install -y java-1.8.0-openjdk
```

4. Verify the Java installation:

```bash theme={null}
java -version
# Example:
# openjdk version "1.8.0_442"
# OpenJDK Runtime Environment (build 1.8.0_442-b06)
# OpenJDK 64-Bit Server VM (build 25.442-b06, mixed mode)
```

Configure Kafka to run in KRaft mode (ZooKeeperless)
KRaft (Kafka Raft) mode lets Kafka manage metadata itself without ZooKeeper. The main steps are:

* Generate a cluster ID and format storage for KRaft.
* Update `config/kraft/server.properties` with KRaft-specific settings.
* Start the Kafka server.

Generate the cluster ID and format KRaft storage

```bash theme={null}
# Generate a UUID for the cluster ID
CLUSTER_ID=$(uuidgen)
# If uuidgen is not available:
# Format the storage directory for KRaft using the server properties file
bin/kafka-storage.sh format -t "$CLUSTER_ID" -c config/kraft/server.properties

# Example output:
# Formatting /tmp/kraft-combined-logs
```

Edit the KRaft server properties
Open `config/kraft/server.properties` (for example, with `vim`) and update the following key settings:

* `process.roles=broker,controller`
* `node.id=1`
* `controller.quorum.voters=1@localhost:9093`
* `listeners` should bind to `0.0.0.0` so Kafka accepts remote connections
* `advertised.listeners` should use the EC2 public IP so external clients can connect
* `controller.listener.name=CONTROLLER` and `inter.broker.listener.name=PLAINTEXT`

Example critical sections for `config/kraft/server.properties`:

```properties theme={null}
# KRaft mode basics
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093

# Socket server settings
listeners=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
inter.broker.listener.name=PLAINTEXT

# Use your EC2 instance public IP for advertised.listeners so external clients can reach the broker
advertised.listeners=PLAINTEXT://3.95.58.45:9092

controller.listener.name=CONTROLLER
```

Why listen on 0.0.0.0? Binding to `0.0.0.0` ensures the broker accepts connections from external network interfaces. If listeners bind only to loopback, external clients will be unable to connect.

Open the Kafka port (security group)
Edit the instance security group inbound rules and add a custom TCP rule for port `9092`. For quick testing you may allow `0.0.0.0/0`, but be cautious — restrict access in production to specific IP ranges, VPCs, or CIDR blocks.

<Frame>
  <img alt="The image shows an AWS console screen for editing inbound rules in a security group, with settings for allowing traffic from any IP address (0.0.0.0/0). There is also a warning about allowing access from all IP addresses." />
</Frame>

> **warning** Do not leave port 9092 open to the entire internet in production. Restrict access to trusted IP ranges, your VPC, or known CIDR blocks.

Start the Kafka broker (KRaft)
Start Kafka in the foreground to watch logs while it initializes:

```bash theme={null}
bin/kafka-server-start.sh config/kraft/server.properties
```

You should see logs indicating the Kafka Raft server and controllers started:

```text theme={null}
[2025-05-10 10:32:02,941] INFO kafka version: 3.0.0 (org.apache.kafka.common.utils.AppInfoParser)
[2025-05-10 10:32:02,965] INFO Kafka Server started (kafka.server.KafkaRaftServer)
[2025-05-10 10:32:02,971] INFO [Controller 1] UnfenceBrokerRecord(id=1, epoch=0) (org.apache.kafka.controller.BrokerHeartbeatManager)
[2025-05-10 10:32:02,975] INFO [BrokerLifecycleManager id=1] The broker has been unfenced. Transitioning from RECOVERY to RUNNING. (kafka.server.BrokerLifecycleManager)
```

Create a demo topic
Open a second Session Manager terminal (leave the broker terminal running) and create the topic `cartevent`:

```bash theme={null}
# From the kafka installation directory
bin/kafka-topics.sh --create \
  --topic cartevent \
  --bootstrap-server 3.95.58.45:9092 \
  --partitions 3 \
  --replication-factor 1

# Expected output:
# Created topic cartevent.
```

Troubleshooting checklist

| Issue                            | Quick checks                                                                                                           |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `kafka-topics.sh` cannot connect | Verify `advertised.listeners` contains the correct public IP; verify the broker is running                             |
| Cannot reach broker remotely     | Confirm security group inbound rule allows port `9092` from your client IP                                             |
| KRaft storage format errors      | Ensure you ran `kafka-storage.sh format -t "$CLUSTER_ID" -c config/kraft/server.properties` before starting the broker |
| Java not found                   | Install OpenJDK 1.8: `sudo yum install -y java-1.8.0-openjdk`                                                          |

Useful links and references

* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
* [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
* [Amazon EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)

Recap

* You launched an EC2 instance with an IAM role that enables Session Manager access.
* Installed Java and Kafka, formatted KRaft storage, and configured `server.properties` for KRaft mode.
* Opened port 9092 and started the Kafka broker.
* Created the `cartevent` topic ready for producers and consumers.

You're now ready to configure your front-end service to produce events to the `cartevent` topic. See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/95f49caf-8e0b-4ed9-b7dd-9f43ff31ed9a/lesson/f9f1dee1-dd0e-4476-8ee0-a0a343a59d6c)


# Demo Starting Our Frontend Interface

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Project-Building-an-Event-Driven-System/Demo-Starting-Our-Frontend-Interface/page

Guide to building a Flask Toy Shop frontend that produces JSON order events to a Kafka cartevent topic, runs locally, and shows how to verify messages on the broker.

Welcome back. In the previous lesson we provisioned a VM on Amazon Elastic Compute Cloud (EC2), installed Kafka (using the Raft protocol), created an IAM role, launched an EC2 instance, and created the `cartevent` topic. In this article we'll build a simple front-end that produces order events to the Kafka cluster and verify those events on the broker.

Below you'll find the project layout, installation steps, the complete Flask app that produces events, how to run the UI, check logs, and validate messages on the Kafka broker.

## Project layout

| Path                                     | Purpose                                                     |
| ---------------------------------------- | ----------------------------------------------------------- |
| `final_project/ToyShop/`                 | Frontend Flask app — "Toy Shop" UI (static, templates, app) |
| `final_project/ToyShop/static/`          | CSS, images                                                 |
| `final_project/ToyShop/templates/`       | HTML templates for each endpoint                            |
| `final_project/ToyShop/app.py`           | Flask application that produces events to Kafka             |
| `final_project/ToyShop/requirements.txt` | Python dependencies                                         |
| `final_project/WarehouseUI/`             | Internal dashboard — consumer (placeholder)                 |

Open a terminal, switch into the project folder, and install dependencies:

```bash theme={null}
cd final_project/
cd ToyShop
```

Requirements (contents of `requirements.txt`):

```text theme={null}
Flask==2.2.3
python-dotenv==1.0.0
Werkzeug==2.2.3
confluent-kafka
```

Install them:

```bash theme={null}
pip3 install -r requirements.txt
```

## Flask app — producing order events to Kafka

Open `app.py` in your editor. The example below shows the essential, corrected parts of the Flask application: imports, logging, Kafka producer configuration, a delivery callback, sample product data, routes for cart operations, and the handler that produces an order event to the `cartevent` topic.

```python theme={null}
