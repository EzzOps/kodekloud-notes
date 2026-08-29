# Python
pip install google-cloud-pubsub

# Node.js
npm install @google-cloud/pubsub
```

## Minimal code examples

Python — publish (synchronous)

```python theme={null}
from google.cloud import pubsub_v1

project_id = "my-project"
topic_id = "my-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

data = "Hello, Pub/Sub!".encode("utf-8")
future = publisher.publish(topic_path, data, origin="python-sample")
message_id = future.result()
print(f"Published message ID: {message_id}")
```

Python — subscribe (streaming pull with callback)

```python theme={null}
from google.cloud import pubsub_v1

project_id = "my-project"
subscription_id = "my-subscription"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
```

Node.js — publish (async)

```javascript theme={null}
const {PubSub} = require('@google-cloud/pubsub');
const pubsub = new PubSub({projectId: 'my-project'});

async function publishMessage() {
  const topicName = 'my-topic';
  const dataBuffer = Buffer.from('Hello, Pub/Sub!');
  const messageId = await pubsub.topic(topicName).publish(dataBuffer);
  console.log(`Published message ID: ${messageId}`);
}

publishMessage().catch(console.error);
```

## Operational considerations

* Batching and latency: Publishers batch messages to improve throughput. Tune batch size and delay to balance latency and throughput.
* Flow control: Configure max outstanding messages/bytes on subscribers to avoid resource exhaustion and to maintain predictable memory/CPU usage.
* Retries and dead-letter topics: Configure retry policies and consider a dead-letter topic for messages that fail processing repeatedly so they can be inspected and reprocessed.
* Push endpoints: Ensure push endpoints use HTTPS, validate requests as needed (e.g., authentication or token validation), and respond with the correct status codes to control acknowledgment behavior.
* Monitoring and alerting: Track metrics such as publish/ack latency, undelivered message backlog, and subscriber errors to detect and respond to issues quickly.

## Security warning

<Callout icon="warning">
  Never commit service account keys to source control. Use secret management, environment-level credentials (ADC), or workload identity to securely provision credentials.
</Callout>

## Quick reference: patterns and choices

| Use case                          | Recommended pattern                                                    |
| --------------------------------- | ---------------------------------------------------------------------- |
| High-throughput ingestion         | Asynchronous publishing with batching                                  |
| Real-time processing with scaling | Pull subscribers using streaming pull or serverless subscribers        |
| Webhook-style delivery            | Push subscriptions to HTTPS endpoints (must handle retries/validation) |
| Error isolation                   | Use dead-letter topics and retry policies                              |

## Links and references

* Cloud Pub/Sub documentation: [https://cloud.google.com/pubsub](https://cloud.google.com/pubsub)
* Pub/Sub client libraries: [https://cloud.google.com/pubsub/docs/reference/libraries](https://cloud.google.com/pubsub/docs/reference/libraries)
* Authentication overview (ADC): [https://cloud.google.com/docs/authentication/production](https://cloud.google.com/docs/authentication/production)

Summary

* Publishers and subscribers connect to Cloud Pub/Sub via Google Cloud client libraries.
* Libraries abstract network, auth, retries, batching, and flow control so you can focus on message handling.
* Choose publish/pull/push based on latency, throughput, and runtime environment.
* Use Application Default Credentials or secure credential provisioning and follow least-privilege IAM.

That’s it for this lesson—see you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/37c5cf57-e254-4e8e-bb44-c8fc4d03cb13" />
</CardGroup>


# Data Ingestion Introduction

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Ingestion-Options/Data-Ingestion-Introduction/page

Overview of data ingestion patterns, contrasting batch and streaming approaches, pipeline stages, trade-offs, and GCP services for building reliable ingestion pipelines

Welcome back. In this lesson we dive into one of the foundational topics in data engineering: data ingestion patterns. Whether you are building a small application or a large data platform, reliably moving data from sources into a storage or processing system is essential for analytics, reporting, and machine learning. Here we introduce core concepts and the two primary ingestion approaches: batch and streaming.

At a high level, a data ingestion pipeline moves raw data from sources into a storage/processing system where it becomes available for analysis or model training. Typical pipeline stages are:

* Raw data sources\
  The original, unprocessed data from systems such as transactional databases, application logs, IoT sensors, or social media feeds.
* Ingestion framework\
  The mechanisms or services that pull or receive data from sources: connectors, agents, APIs, or messaging systems (for example, change-data-capture connectors, log collectors, or Pub/Sub).
* Staging / raw landing\
  Where ingested raw data is stored (often a data lake or staging bucket). This stage usually includes lightweight validation, schema tagging, and deduplication; heavier enrichment and joins occur later in processing.
* Processing and transformation\
  Jobs or streaming processors that clean, normalize, and enrich data to create analysis-ready datasets.
* Final storage and consumption\
  Processed datasets are written to destinations such as a data warehouse, curated data lake, or analytics platform for reporting, dashboards, or downstream ML pipelines.

<Callout icon="lightbulb">
  Choosing the right ingestion approach affects latency, throughput, operational complexity, and how you handle ordering, duplicates, and failures. Consider business SLAs (latency vs. completeness), data volume, and toolchain maturity when designing your ingestion layer.
</Callout>

Why the ingestion pattern matters

* The ingestion pattern determines end-to-end latency, resource usage, fault tolerance, and operational complexity.
* It affects the choice of tools and architecture (batch schedulers, stream processors, messaging systems, CDC tools).
* It drives design decisions for ordering, exactly-once or at-least-once semantics, duplicate handling, and state management.

<Frame>
  <img alt="An infographic titled &#x22;Data Ingestion – Introduction&#x22; showing raw data sources (Database, Web/App, IoT Sensor, Social Media) funneled through a central &#x22;Data Ingestion&#x22; process that collects, cleans, and transfers data. The processed data flows to destination systems (Data Warehouse, Data Lake, Analytics Platform) and highlights batch and streaming ingestion." />
</Frame>

Two primary ingestion patterns

* Batch ingestion
  * Moves data in discrete groups (batches) on a schedule (hourly, daily, nightly).
  * Common use cases: nightly ETL that aggregates yesterday’s transactions; large backfills; bulk data movement to a data warehouse.
  * Characteristics: higher end-to-end latency, simpler processing model, easier to reason about correctness for large bulk operations.
  * Variants:
    * Full loads (replace entire dataset)
    * Incremental loads (only new or changed rows)
    * Change data capture (`CDC`) for near-real-time incremental loads
    * Micro-batching (small batches at high frequency) as a hybrid to reduce latency

* Streaming ingestion
  * Continuously ingests and processes events in near real time as they are produced.
  * Common use cases: live user-event analytics, real-time monitoring, fraud detection, anomaly detection, feature pipelines for online ML.
  * Characteristics: low latency, event-driven, often requires windowing semantics, state management, idempotency, and careful handling of event-time vs processing-time.
  * Considerations: event ordering, backpressure, checkpointing, retention, and duplicate event handling. Guarantees vary by platform (at-least-once, exactly-once).

Comparison: Batch vs Streaming

| Dimension   | Batch ingestion                                      | Streaming ingestion                                       |
| ----------- | ---------------------------------------------------- | --------------------------------------------------------- |
| Latency     | Minutes to hours (or longer)                         | Milliseconds to seconds                                   |
| Typical use | Periodic aggregations, backfills, ELT into warehouse | Real-time analytics, alerts, feature updates              |
| Complexity  | Simpler semantics, easier reprocessing               | Harder: state, windowing, ordering, checkpoints           |
| Fault model | Retry entire batch or re-run job                     | Checkpoints, replay from message broker, idempotent sinks |
| Examples    | Scheduled ETL jobs, nightly loads                    | Event streams, CDC into Pub/Sub, real-time pipelines      |

Both patterns can coexist in a modern data platform: use batch for large-scale transformations and historical reprocessing, and streaming for low-latency analytics and timely alerts. Hybrid architectures (e.g., streaming ingestion with periodic micro-batch reprocessing) are common.

This lesson examines available GCP services for both batch and streaming ingestion and dives deeper into their technical trade-offs. Common GCP building blocks include Cloud Storage, Cloud Pub/Sub, Dataflow, Dataproc, and BigQuery for different stages of ingestion and processing:

* Ingestion: Cloud Pub/Sub, Transfer Service, direct connector agents, Cloud Storage uploads
* Processing: Dataflow (stream & batch), Dataproc (batch Spark/Hadoop), Cloud Run/Cloud Functions (light-weight ingestion)
* Storage & consumption: Cloud Storage (raw landing), BigQuery (analytics), BigTable/Firestore (low-latency lookups)

<Callout icon="warning">
  Be careful with ordering and deduplication. Streaming systems often deliver at-least-once by default; implement idempotent writes or deduplication windows in sinks to avoid data inflation. When exact ordering matters, design with partition keys and windowing semantics in mind.
</Callout>

This lesson also covers the specific differences between batch and streaming ingestion in more detail.

Links and references

* [Google Cloud Pub/Sub documentation](https://cloud.google.com/pubsub/docs)
* [Google Cloud Dataflow documentation](https://cloud.google.com/dataflow/docs)
* [BigQuery ingestion best practices](https://cloud.google.com/bigquery/docs/loading-data)
* [Change Data Capture (CDC) patterns](https://martinfowler.com/articles/201701-event-sourcing.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/55ff91cf-92cb-4d54-932a-f95075fd3f68/lesson/e725c030-134d-45cf-9724-5ba0f2c5d206" />
</CardGroup>
