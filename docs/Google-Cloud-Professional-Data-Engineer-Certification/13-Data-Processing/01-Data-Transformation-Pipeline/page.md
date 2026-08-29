# Data Transformation Pipeline

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Data-Transformation-Pipeline/page

Explains a Cloud Dataflow Apache Beam pipeline that ingests Pub/Sub events, applies ParDo transforms and GroupByKey aggregates, and writes results to sinks like Cloud Storage or BigQuery

Welcome back. In this lesson we’ll walk through a data transformation pipeline implemented with Cloud Dataflow (Apache Beam). You’ll learn how raw events enter the pipeline, how Dataflow transforms them step‑by‑step, and where processed results are stored. After this lesson you should be able to read a Dataflow pipeline diagram and explain what each box represents and how data flows between them.

Example scenario

* Imagine a networking company managing thousands of routers and switches. Each device periodically emits logs and performance metrics.
* Raw events are published to a Cloud Pub/Sub topic — a scalable, durable streaming source that captures the event stream.
* Pub/Sub is the pipeline’s source; Dataflow consumes the stream, transforms it, and writes the results to a sink such as Cloud Storage or BigQuery.

Core concepts (quick reference)

* PCollection — the fundamental distributed, immutable dataset in Apache Beam / Cloud Dataflow.
* Transform — a computation (map, filter, group, aggregate) that consumes one or more PCollections and emits new PCollections.
* ParDo — per-element processing (map/filter/enrich); can emit zero, one, or many outputs per input.
* GroupByKey / Aggregation — grouping elements by key and computing per-key aggregates.
* Source / Sink — where data enters and leaves the pipeline (Pub/Sub, Cloud Storage, BigQuery, etc.).

<Callout icon="lightbulb">
  PCollections are like in-memory tables or DataFrames conceptually, but they are distributed and immutable. Use the PCollection + transforms model when you need scalable, parallel processing across many workers rather than single-node operations.
</Callout>

PCollection (detailed)

* Definition: a PCollection is a distributed, immutable collection of elements (events or records) that Beam/Dataflow processes in parallel.
* Immutability: applying a transform never mutates the original PCollection; it produces a new PCollection representing the transformed data.
* Visuals: in pipeline diagrams, each blue box labeled “PCollection” represents a distinct, versioned dataset produced by a previous transform. At scale, a PCollection’s elements are partitioned across multiple workers.

Transformations (how they work)

* A transform consumes one or more PCollections and returns one or more new PCollections.
* Transforms are applied in parallel across elements; think of them as distributed functions.
* Common transforms:
  * ParDo: element-wise processing (parse, enrich, filter).
  * Filter: drop unwanted elements.
  * Map: transform each element.
  * GroupByKey + Combine: group elements by a key and compute aggregates (sum, count, average, custom combine).

ParDo (primary per-element operator)

* ParDo is Beam’s flexible per-element transform. It applies a user-defined function to each element and may emit zero, one, or many outputs.
* Use ParDo for parsing message payloads, field-level enrichment, or filtering logic before grouping or aggregation.

GroupByKey and Aggregation

* GroupByKey groups elements by a specified key (for example, device ID).
* After grouping, apply a Combine or custom aggregator to produce per-key metrics (counts, sums, averages, top‑N, etc.).
* Grouping often triggers a shuffle across workers, so design keys and windows carefully for performance.

Source and Sink

* Source (ingest): where pipeline data originates — e.g., Cloud Pub/Sub, Cloud Storage, BigQuery exports.
* Sink (output): where processed data is written — e.g., Cloud Storage, BigQuery, Pub/Sub.
* In this lesson’s example we use Cloud Storage as the final sink, but BigQuery is a common choice for analytics queries.

Step-by-step flow (example)

1. Devices publish events to a Cloud Pub/Sub topic (Source).
2. Dataflow reads messages from Pub/Sub into an initial PCollection.
3. A ParDo transform parses message payloads, validates fields, and optionally filters out malformed or irrelevant records. The parsed/filtered results become a new PCollection.
4. Records are keyed by an attribute (e.g., device ID), then GroupByKey is applied. A Combine/aggregation computes per-device metrics (counts, averages, deltas). Aggregated results form another PCollection.
5. The final PCollection is written to a Sink (Cloud Storage in this example, or BigQuery for analytics).

To visualize this flow, refer to the diagram below showing Pub/Sub -> multiple PCollections and transforms -> Cloud Storage sink.

<Frame>
  <img alt="A schematic diagram of a Google Cloud Dataflow pipeline showing raw data read from Cloud Pub/Sub flowing through PCollections and transforms (ParDo filter/map, GroupByKey aggregate) and then written to Cloud Storage as the final output. A small legend on the right explains PCollection, Transform, and Source/Sink." />
</Frame>

Mapping diagram elements to purpose

| Diagram element     | Purpose                                               | Typical examples                                        |
| ------------------- | ----------------------------------------------------- | ------------------------------------------------------- |
| PCollection         | Distributed, immutable dataset produced at each stage | Parsed events, filtered records, aggregated metrics     |
| ParDo               | Element-wise processing (map/filter/enrich)           | JSON parsing, field normalization, dropping bad records |
| GroupByKey          | Group elements by a key before aggregation            | Group by `device_id`, `region`                          |
| Aggregate / Combine | Compute per-key metrics                               | `sum(bytes)`, `count(events)`, `average(latency)`       |
| Source              | Ingest raw events into the pipeline                   | `Cloud Pub/Sub`                                         |
| Sink                | Persist processed results for downstream use          | `Cloud Storage`, `BigQuery`                             |

Best practices (brief)

* Keep ParDo functions stateless or manage state carefully to enable parallel scaling.
* Avoid heavy computations inside GroupByKey to reduce shuffle cost.
* Choose appropriate windows and triggers for streaming aggregates to balance latency and completeness.
* For analytics sinks, prefer BigQuery for queryability; use Cloud Storage for archival or batch outputs.

Summary

* Cloud Pub/Sub provides a scalable, streaming source for raw events.
* PCollections are immutable, distributed datasets that represent intermediate pipeline state.
* Transforms (ParDo for per-element processing, GroupByKey/Aggregate for grouping/aggregation) consume and produce PCollections.
* The final PCollection is written to a sink such as Cloud Storage or BigQuery depending on downstream needs.

Links and references

* Apache Beam: [https://beam.apache.org/](https://beam.apache.org/)
* Cloud Dataflow: [https://cloud.google.com/dataflow](https://cloud.google.com/dataflow)
* Cloud Pub/Sub: [https://cloud.google.com/pubsub](https://cloud.google.com/pubsub)
* Cloud Storage: [https://cloud.google.com/storage](https://cloud.google.com/storage)
* BigQuery: [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)

That’s it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/63b29580-746d-49a8-bf85-07eb2b60a9f6" />
</CardGroup>
