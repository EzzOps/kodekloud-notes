# download: s3://kafka-s3-jar-file-confluent-lab/confluentinc-kafka-connect-s3-10.5.23.zip to ./confluentinc-kafka-connect-s3-10.5.23.zip
```

Verify and unzip:

```bash theme={null}
ls -l
unzip confluentinc-kafka-connect-s3-10.5.23.zip
ls -l
# Should show a directory like: confluentinc-kafka-connect-s3-10.5.23
```

3. Configure the Kafka Connect worker (standalone)

Open the worker properties shipped with Kafka (adjust the path if your Kafka distro is elsewhere):

```bash theme={null}
vim kafka_2.13-3.0.0/config/connect-standalone.properties
```

Edit or confirm the following key settings. Replace the `bootstrap.servers` value with your broker's IP/hostname and set `plugin.path` to the directory where you unpacked the connector.

Example connect-standalone.properties:

```properties theme={null}
# Worker configuration
bootstrap.servers=34.224.82.66:9092

# Converters: how Connect converts Kafka bytes into Connect data structures
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
# If you're using schemaless JSON, disable schemas
key.converter.schemas.enable=false
value.converter.schemas.enable=false

# Offsets
offset.storage.file.filename=/tmp/connect.offsets
offset.flush.interval.ms=10000

# Where Connect looks for plugin directories (must point to the unpacked connector)
plugin.path=/root/confluentinc-kafka-connect-s3-10.5.23
```

Save and exit the editor.

Quick reference — important `connect-standalone.properties` entries

| Property                            | Purpose                                             | Example                                       |
| ----------------------------------- | --------------------------------------------------- | --------------------------------------------- |
| `bootstrap.servers`                 | Kafka broker endpoint Connect should reach          | `34.224.82.66:9092`                           |
| `key.converter` / `value.converter` | Data format converters used by Connect tasks        | `org.apache.kafka.connect.json.JsonConverter` |
| `plugin.path`                       | Directory where Connect scans for connector plugins | `/root/confluentinc-kafka-connect-s3-10.5.23` |
| `offset.storage.file.filename`      | Local offset storage for standalone mode            | `/tmp/connect.offsets`                        |

4. Create the S3 Sink connector configuration

Create a connector properties file that describes connector behavior (topics to read, S3 bucket, formatting, etc.):

```bash theme={null}
vim kafka_2.13-3.0.0/config/s3-sink-connector.properties
```

Example `s3-sink-connector.properties` — replace `s3.bucket.name`, `s3.region`, and `topics` as appropriate:

```properties theme={null}
name=s3-sink-connector
connector.class=io.confluent.connect.s3.S3SinkConnector
tasks.max=1
topics=cartevent

# Replace with your S3 bucket name (example)
s3.bucket.name=kafka-connect-s3-sink-example
s3.region=us-east-1

# When to flush objects to S3
flush.size=5
rotate.schedule.interval.ms=60000

storage.class=io.confluent.connect.s3.storage.S3Storage
format.class=io.confluent.connect.s3.format.json.JsonFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner
timezone=UTC

# Converters should be compatible with worker converters
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=false
value.converter.schemas.enable=false

behavior.on.null.values=ignore
```

Connector properties explained (high-level)

* `topics`: Kafka topic(s) to sink to S3.
* `s3.bucket.name` / `s3.region`: Target S3 bucket and region.
* `flush.size`: Number of records before writing to S3.
* `format.class`: Output format (JSON in this example).
* `plugin.path` in the worker must include the connector JARs for Connect to load the `io.confluent.connect.s3.S3SinkConnector` class.

5. Create the S3 bucket (if you haven't already)

Create the bucket via the AWS Console and ensure the region matches `s3.region` in the connector config.

<Frame>
  <img alt="The image shows the AWS S3 bucket creation interface, displaying encryption options and a message indicating that the specified bucket name is already taken." />
</Frame>

6. Start Kafka Connect (standalone)

Change into the Kafka installation directory (or reference the full path to the script) and start Connect with the worker and connector config files:

```bash theme={null}
cd kafka_2.13-3.0.0
bin/connect-standalone.sh config/connect-standalone.properties config/s3-sink-connector.properties
```

> **warning** Run the `connect-standalone.sh` script from the Kafka root directory (the directory that contains `bin/`), or supply the full path. If you run it from the wrong folder you will see `No such file or directory`.

On startup the worker will scan plugin paths and attempt to load the S3 connector. Example logs showing plugin scanning and consumer group assignment:

```text theme={null}
[2025-05-10 11:41:944] INFO Scanning for plugin classes. This might take a moment ... (org.apache.kafka.connect.cli.ConnectStandalone)
[2025-05-10 11:41:968] INFO Loading plugin from: /root/confluentinc-kafka-connect-s3-10.5.23/doc/ (org.apache.kafka.connect.runtime.isolation.DelegatingClassLoader)
[2025-05-10 11:41:989] INFO Added 0 plugins. (org.apache.kafka.connect.runtime.isolation.DelegatingClassLoader)
[2025-05-10 11:11:49,961] INFO  [3-sink-connector-0] Successfully joined group with generation Generation(generationId=1, memberId='connector-consumer-s3-sink-connector-0', protocol='range')
[2025-05-10 11:11:53,066] INFO  [3-sink-connector-0] Found no committed offset for partition cartevent-0
[2025-05-10 11:11:53,088] INFO  [3-sink-connector-0] Resetting offset for partition cartevent-0 to position(offset=0)
```

Important notes and troubleshooting

* Topic existence: If the configured topic (for example `cartevent`) does not exist, Kafka Connect will not create it for you. Topic creation is controlled by the broker setting `auto.create.topics.enable`. Create the topic ahead of time with your desired partitions and replication: `kafka-topics.sh --create ...`
* plugin.path: Ensure `plugin.path` points to the directory containing the unpacked connector JARs. Each plugin typically lives in its own subdirectory under `plugin.path`; if Connect cannot find the S3 connector classes it will not load the plugin.
* Permissions: Confirm the EC2 instance IAM role has S3 permissions for the bucket (PutObject, ListBucket).
* Converters: Keep worker and connector converters compatible. If you disable schemas (`schemas.enable=false`) ensure your messages are formatted accordingly.

Recap — what we did

* Downloaded and unpacked the Confluent S3 Sink connector.
* Updated `connect-standalone.properties` to reference the connector via `plugin.path`.
* Created a connector configuration describing topics, S3 bucket, converters, and formatting.
* Started Kafka Connect in standalone mode and verified plugin scanning and consumer assignment via logs.

Next steps

* Produce events to the configured topic (`cartevent`) and observe Kafka Connect writing files to the S3 bucket.
* Monitor the S3 bucket for objects written by the connector and adjust `flush.size` / `rotate.schedule.interval.ms` to balance latency and file sizes.

See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/68c7ef21-4d7c-405e-8fae-5500f90b82a2/lesson/c67b242d-4f9d-489b-9125-06c4172662dd)


# Streaming data from Kafka to other systems

Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Kafka-Connect-Effortless-Data-Pipelines/Streaming-data-from-Kafka-to-other-systems/page

Guide to Kafka Connect for building scalable fault tolerant pipelines that stream Kafka topics into long term stores like S3 data warehouses and databases

Hello and welcome back.

In this lesson/article we focus on Kafka Connect — the runtime and framework that helps you build reliable, production-ready data pipelines to and from Kafka with minimal custom code. This guide explains when and why to use Connect, how connectors are configured and deployed, and practical tips for streaming Kafka topics into long-term stores like Amazon S3, data warehouses, or databases.

## Why use Kafka Connect?

Kafka is designed for high-throughput, low-latency stream processing. However, it is not a replacement for long-term archival or analytical storage:

* Kafka stores data on disk with retention policies (time- or size-based). Retention keeps your cluster from growing indefinitely, but it is not a substitute for archival or analytics storage.
* For analytics, reporting, or ML pipelines you typically need durable, queryable storage such as object stores (Amazon S3, Google Cloud Storage), databases, or data warehouses (BigQuery, Redshift).
* Writing and maintaining custom consumer code to copy data from Kafka to these systems quickly becomes an operational burden.

<Frame>
  <img alt="The image shows a comparison between using Kafka for real-time processing versus databases for long-term analysis, highlighting Kafka's limitations in space and retention, and databases' strengths in efficient querying and storage." />
</Frame>

## Real-world example: shopping application

Imagine a shopping app that emits `click`, `cart`, and `checkout` events into an `events` Kafka topic. You use those events for:

* Real-time dashboards and alerts (stream processing).
* Long-term analytics (sales trends, customer lifetime value, ML features).

Rather than building and operating a custom consumer that polls Kafka and writes to S3 or a data warehouse, use Kafka Connect with a sink connector (for example, an S3 sink). Connect handles batching, partitioning, retries, and scaling so you can focus on analytics rather than operational plumbing.

<Frame>
  <img alt="The image is a flowchart showing data streaming from a shopping application to other systems using Kafka. It illustrates events going through an Events Kafka Topic and Kafka Connect Cluster to a monitor and S3 storage." />
</Frame>

## What is Kafka Connect?

Kafka Connect is:

* A framework and long-running runtime for connectors that move large collections of data into and out of Kafka.
* Typically run as a separate service in either standalone or distributed mode.
* Connector-based: source connectors bring external data into Kafka; sink connectors move Kafka data out to external systems.

Benefits of using connectors:

* Minimal custom code
* Standardized configuration and lifecycle
* Built-in scaling and fault tolerance (in distributed mode)

## Connector configuration and REST API

Connectors are configured by supplying JSON (distributed mode) or properties files (standalone mode) to the Connect runtime. In distributed mode you typically POST a connector definition to the Connect REST API. The configuration includes:

* Connection to Kafka (bootstrap servers)
* Topics to read or write
* Connector-specific settings (e.g., for S3: bucket, region, format, flush size)

Example (simplified) S3 sink connector configuration to POST to the Connect REST API:

```json theme={null}
{
  "name": "s3-sink-events",
  "connector.class": "io.confluent.connect.s3.S3SinkConnector",
  "tasks.max": "3",
  "topics": "events",
  "s3.bucket.name": "my-company-events-bucket",
  "s3.region": "us-east-1",
  "flush.size": "1000",
  "storage.class": "io.confluent.connect.s3.storage.S3Storage",
  "format.class": "io.confluent.connect.s3.format.json.JsonFormat"
}
```

Example curl command to create the connector (distributed Connect REST API usually on port 8083):

```bash theme={null}
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  --data '@s3-sink-events.json'
```

Note: exact configuration keys differ between connector implementations (Confluent, community, cloud-managed). Always consult the connector documentation for required and optional properties.

## Connector types: quick reference

| Connector type | Use case                              | Examples                                      |
| -------------: | ------------------------------------- | --------------------------------------------- |
|         Source | Import external data into Kafka       | Databases (Debezium), cloud services, logs    |
|           Sink | Export Kafka data to external systems | `S3`, `BigQuery`, `Postgres`, `Elasticsearch` |

| Common S3 sink properties | Purpose                             |
| ------------------------- | ----------------------------------- |
| `topics`                  | Kafka topic(s) to consume           |
| `s3.bucket.name`          | Destination S3 bucket               |
| `flush.size`              | Number of records before flush      |
| `format.class`            | Output format (JSON, Avro, Parquet) |

Wrap any examples with curly braces in code ticks to avoid MDX parsing issues (for example, use `` `{"key":"value"}` `` when required).

## Deployment considerations

Kafka Connect is a separate long-lived service from Kafka. You can deploy it:

* On VMs (for example, EC2)
* Containerized on Kubernetes
* As a managed/cloud Connect service (Confluent Cloud, cloud providers)

Although serverless functions are excellent for short-lived tasks, Kafka Connect expects persistent workers and coordinated task management—so running Connect in serverless or ephemeral environments is not recommended.

> **lightbulb** Kafka Connect runs as a long-lived process in either standalone or distributed mode. For production deployments, prefer containerized or VM-based deployments (for example Kubernetes) or a managed Connect service.

> **warning** Do not use short-lived serverless functions (for example, AWS Lambda) to replace a Connect cluster. Connect relies on persistent workers, task coordination, and rebalancing that serverless platforms do not provide.

## Why use Kafka Connect? Key benefits

<Frame>
  <img alt="The image describes the benefits of streaming data from Kafka to other systems, highlighting scalability, fault tolerance, extensibility, and real-time streaming." />
</Frame>

* Scalability: Connect clusters scale independently of Kafka. Add workers to increase connector throughput.
* Fault tolerance: Distributed mode provides task rebalancing and resumption on worker failure. Connectors include retry and error handling options.
* Extensibility: Large ecosystem of connectors covers S3, GCS, BigQuery, databases, search, and more—reducing custom development.
* Near-real-time analytics: Stream events from Kafka into analytics systems (S3 → Athena, BigQuery, Redshift, Looker Studio) to enable immediate querying and historical analysis.

## Summary

* Kafka is excellent for real-time stream processing but not intended for indefinite archival storage.
* Use Kafka Connect to build standardized, scalable, and fault-tolerant pipelines that move data from Kafka to durable stores (S3, databases, data warehouses).
* Configure connectors via the Connect REST API (JSON) or properties files, and deploy Connect as a long-running service (VMs, containers, or managed offerings).
* Choose connector implementations and tuning parameters (batch size, flush interval, serialization format) based on throughput, downstream query patterns, and storage cost.

## Links and references

* [Kafka Connect overview — Apache Kafka documentation](https://kafka.apache.org/documentation/#connect)
* [Confluent Hub — connectors](https://www.confluent.io/hub/)
* [Amazon S3 documentation](https://docs.aws.amazon.com/s3/)
* [BigQuery documentation](https://cloud.google.com/bigquery)
* [Debezium (change data capture) connectors](https://debezium.io/)

With this foundation, the next lesson/article will show a practical demo: setting up Kafka Connect and using an Amazon S3 sink connector to move topic data into an S3 bucket.

That is it for this lesson/article. See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka/module/68c7ef21-4d7c-405e-8fae-5500f90b82a2/lesson/d8beead0-6a5a-4ca3-976b-bb84f6bf0cb4)
