# Dataflow Exam Summary

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Dataflow-Exam-Summary/page

Summary of Apache Beam and Google Dataflow concepts for Data Engineer exam covering unified batch and streaming, windowing, watermarks, triggers, state, autoscaling, templates, integration, and monitoring

Welcome back.

This lesson reviews the core Apache Beam / Dataflow concepts most relevant to the Google Cloud Professional Data Engineer Certification. These topics appear either directly or embedded in scenario-style questions on the exam. Read with the exam focus in mind: the same concepts are used when designing reliable streaming pipelines in production.

Key SEO topics covered: Apache Beam unified model, bounded vs unbounded data, PCollections/PTransforms, windowing & watermarks, triggers & allowed lateness, autoscaling, state & timers, Dataflow templates, and monitoring/integration with Pub/Sub, BigQuery, and GCS.

## Unified programming model: batch and streaming

One powerful Beam feature is that identical pipeline code can handle both batch and streaming workloads. Beam supports both bounded (batch) and unbounded (streaming) PCollections, enabling a single programming model for both processing modes.

Exam-style question:

* Which Beam model feature allows the same code to be used for both batch and streaming pipelines?
* Answer: The unified model supporting both bounded and unbounded data.

Example: switch a single pipeline between batch and streaming by changing the source (TextIO for batch, Pub/Sub for streaming):

```python theme={null}
import apache_beam as beam

def parse_line(line):
    # parse CSV or JSON and return dict-like object
    return {"customer_id": "cust1", "amount": 100}

with beam.Pipeline(options=options) as p:
    # For streaming:
    lines = p | 'Read' >> beam.io.ReadFromPubSub(topic='projects/PROJECT/topics/TOPIC')
    # For batch (uncomment to use):
    # lines = p | 'Read' >> beam.io.ReadFromText('gs://bucket/input/*.csv')

    results = (lines
        | 'Parse' >> beam.Map(parse_line)
        | 'KeyByCustomer' >> beam.Map(lambda x: (x['customer_id'], x['amount']))
        | 'SumPerCustomer' >> beam.CombinePerKey(sum))

    results | 'Write' >> beam.io.WriteToBigQuery('PROJECT:dataset.table')
```

## Core building blocks of a Beam pipeline

Think of a Beam pipeline as a sequence of instructions operating on collections:

| Component             | Description                                        | Examples                                                 |
| --------------------- | -------------------------------------------------- | -------------------------------------------------------- |
| PCollection           | The dataset being processed (bounded or unbounded) | streaming Pub/Sub messages or batch CSV files            |
| PTransform            | A transformation applied to PCollections           | `ParDo`, `Map`, `CombinePerKey`, `GroupByKey`, `Flatten` |
| DoFn / ParDo          | Element-wise processing and user-defined functions | parsing, enrichment, filtering                           |
| Combine / Aggregation | Reduce per-key values                              | `CombinePerKey(sum)`                                     |
| GroupByKey            | Group records by key prior to combining            | sessionization or per-user aggregations                  |

A simple analogy: a PCollection is a box of invoices; ParDo scans invoices to extract amounts; GroupByKey groups by customer ID and Combine computes per-customer totals.

## Event time vs processing time, windowing, triggers, and watermarks

Understand these core streaming concepts and how they interact:

* Event time: when the event actually occurred (timestamp embedded in the event).
* Processing time: when the event is processed by the pipeline (system time).
* Windowing: groups events by event time (fixed windows, sliding windows, sessions).
* Triggers: decide when to emit results for a window (e.g., after watermark passes end-of-window, or after a processing-time delay).
* Watermarks: an estimate of event-time progress—used to decide when to close windows and emit results even with out-of-order arrivals.
* Allowed lateness: how long late events are accepted and processed for a closed window.

| Window Type      | Use Case                         | Example                                 |
| ---------------- | -------------------------------- | --------------------------------------- |
| Fixed (tumbling) | Periodic aggregation             | 1-minute fixed windows                  |
| Sliding          | Overlapping analysis windows     | 5-minute window sliding every 1 minute  |
| Session          | Variable-length activity windows | User sessions defined by inactivity gap |

Exam-style question:

* What Beam concept helps manage out-of-order or late-arriving events?
* Answer: Watermarks (used along with windowing and triggers).

## Autoscaling and cost management

* Dataflow autoscaling dynamically adjusts worker count according to pipeline load.
* Benefits: reduces cost, simplifies testing, allows stress-testing without provisioning a large static cluster, and helps pipelines recover from bursts.
* Consider autoscaling policies and worker types when optimizing cost and latency.

## Advanced streaming logic: state and timers

* Per-key state: store small, bounded state per key (e.g., counts, last-seen timestamp).
* Timers: schedule a future callback for a key to implement time-driven behaviors (e.g., expire session after inactivity, send alerts after a delay).
* Use cases: sessionization, de-duplication, per-user activity windows, delayed actions (e.g., check for missing payment 10 minutes after checkout).

<Callout icon="lightbulb">
  Exam tip: Focus on the distinctions between windowing, triggers, and watermarks—questions often test when and why a pipeline emits results and how late data is handled.
</Callout>

## Deployment strategies and Dataflow templates

Dataflow offers templates to simplify pipeline deployment and reuse:

| Template Type | Runtime flexibility                                                                | Typical use case                                                  |
| ------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Classic       | Limited runtime parameterization; stored in GCS                                    | Simple reusable pipelines                                         |
| Flex          | Supports runtime parameters, custom container images, and more flexible deployment | Production workloads with custom dependencies and runtime options |

Exam-style question:

* Which type of Dataflow template allows runtime parameterization?
* Answer: Flex Template.

## Integration and monitoring

Dataflow integrates tightly with core GCP services:

* Pub/Sub — streaming ingestion: [https://cloud.google.com/pubsub](https://cloud.google.com/pubsub)
* BigQuery — analytics and storage: [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)
* Cloud Storage (GCS) — staging, batch inputs, templates: [https://cloud.google.com/storage](https://cloud.google.com/storage)

Monitoring & SRE:

* Key metrics: throughput, latency, system resource usage, worker CPU/memory, and backpressure.
* Backpressure occurs when downstream systems slow ingestion or processing; monitor and tune I/O and worker types.
* Use Cloud Monitoring / Logging and Dataflow job metrics to build alerts and dashboards.

That covers the high-level exam-relevant Dataflow concepts. Review these sections, practice with small pipelines (both batch and streaming), and focus on how windowing, watermarks, triggers, state, and timers interact.

<Frame>
  <img alt="A slide titled &#x22;GCP Data Engineer Exam – Key Points to Remember&#x22; summarizing major topics. It lists items like unified batch & streaming, core building blocks (PCollections/transforms), windowing/triggers (event vs processing time), autoscaling/optimization, advanced streaming logic, prod-ready deployment templates, and SRE/monitoring." />
</Frame>

That is it for this lesson. Speak with you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/6f4400cc-8784-4016-9aec-7b95a72084c1" />
</CardGroup>
