# Pipeline Design Optimization

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Pipeline-Design-Optimization/page

Guide to designing and optimizing Google Cloud Dataflow pipelines, focusing on fusion, shuffles, parallelization, autoscaling, handling data skew, and when to break fusion for better throughput and latency

Welcome back. This guide covers pipeline design and performance optimization for Google Cloud Dataflow (Apache Beam). We focus on how the runner parallelizes work, where bottlenecks appear, and practical techniques — like breaking fusion — to improve throughput and reduce tail latency.

Key concepts covered:

* Inputs and outputs (sources & sinks)
* Bounded vs unbounded data
* Parallelization, autoscaling, and shuffle behavior
* Fusion: benefits and pitfalls
* When and how to break fusion (Reshuffle, GroupByKey, ParDo boundaries)
* A real-world skew example and recommended patterns

## Inputs and outputs

Dataflow supports a wide range of connectors. Typical sources and sinks include:

| Connector type |          Typical use case | Example                                                 |
| -------------- | ------------------------: | ------------------------------------------------------- |
| Source         | Stream ingest (unbounded) | `ReadFromPubSub(topic='projects/PROJECT/topics/TOPIC')` |
| Source         |     Batch files (bounded) | `ReadFromText('gs://bucket/*.csv')`                     |
| Sink           |   Analytics / warehousing | `WriteToBigQuery(table='PROJECT:DATASET.TABLE')`        |
| Sink           |               File output | `WriteToText('gs://bucket/output/')`                    |

Two important data categories to design for:

| Data type | Description                                                 | When to use                      |
| --------- | ----------------------------------------------------------- | -------------------------------- |
| Bounded   | Fixed-size dataset processed in batch (e.g., invoice files) | Batch pipelines, one-off ETL     |
| Unbounded | Potentially infinite stream (e.g., Pub/Sub messages)        | Streaming, continuous processing |

<Frame>
  <img alt="A Pipeline I/O diagram showing Sources (BigQueryIO, Pub/SubIO, TextIO) on the left and Sinks (BigQueryIO, Cloud Storage, AvroIO) on the right. A Data Types column notes Bounded (batch) and Unbounded (streaming) inputs." />
</Frame>

Design tips:

* Choose bounded sources for finite ETL jobs and unbounded for continuous/real-time processing.
* Match sink semantics to your downstream needs (streaming inserts vs bulk loads).
* Consider windowing and triggering behavior on unbounded sources to control lateness and output cadence.

## Parallelization and autoscaling

Dataflow parallelizes work by splitting inputs into work units (bundles) and scheduling bundles across worker instances. Each transform can execute concurrently on many workers when the computation is parallelizable.

Important runtime behaviors:

* Autoscaling: Dataflow adds workers when there is more work or resource pressure and removes them when load subsides.
* Shuffle operations (e.g., `GroupByKey`) redistribute elements between workers and act as synchronization barriers.
* Dynamic work rebalancing can break large, long-running bundles into smaller pieces to reduce stragglers.

Implications:

* Stateless, element-wise transforms parallelize easily.
* Operations that require redistribution (shuffles) introduce network and synchronization overhead but are necessary for grouping/aggregation workloads.
* Long-running or blocking fused operations can impede dynamic splitting and autoscaling effectiveness.

## Fusion: what it is and when to break it

Apache Beam applies fusion (also called "operator fusion") to combine adjacent transforms into a single execution unit when possible. Fusion reduces materialized intermediates and network I/O, often improving latency and resource usage.

Benefits of fusion:

* Fewer intermediate materializations
* Reduced network traffic and overhead
* Lower per-element latency for short operations

Fusion drawbacks:

* Hotspots/data skew: a dominant key or element may cause one worker to do most work.
* Long-running fused sequences reduce opportunities for dynamic splitting and rebalancing.
* Difficult to isolate expensive CPU- or I/O-bound steps for targeted scaling.

Common ways to break fusion:

* Reshuffle (a lightweight forced shuffle)
* Explicit `GroupByKey` or other aggregations
* Introducing independent `ParDo`/DoFn boundaries for expensive steps

<Frame>
  <img alt="A presentation slide titled &#x22;Fusion Optimization&#x22; showing diagrams that compare &#x22;Without Fusion&#x22; (three separate transforms across multiple stages) versus &#x22;With Fusion&#x22; (a single fused transform stage), plus a &#x22;Break Fusion&#x22; section highlighting Reshuffle and ParDo boundary with notes about &#x22;force split&#x22; benefits like better load balance and preventing skew. The slide is © KodeKloud." />
</Frame>

When to deliberately break fusion:

* You see data skew causing a single worker to become a bottleneck.
* Upstream and downstream steps are long-running and should be isolated for independent scaling.
* You need the runner to be able to split and rebalance work more aggressively.

### Example: forcing a shuffle with Reshuffle (Python SDK)

The example shows a pipeline with an expensive step, followed by an explicit reshuffle to break fusion so downstream expensive work can be balanced across workers.

```python theme={null}
import apache_beam as beam
from apache_beam.transforms.util import Reshuffle

class HeavyCompute(beam.DoFn):
    def process(self, element):
        # Simulate a CPU- or I/O-intensive operation
        result = do_expensive_work(element)
        yield result

with beam.Pipeline(options=pipeline_options) as p:
    (p
     | "ReadPubSub" >> beam.io.ReadFromPubSub(topic='projects/PROJECT/topics/TOPIC')
     | "Parse" >> beam.Map(parse_message)
     | "HeavyStep1" >> beam.ParDo(HeavyCompute())
     # Reshuffle forces a shuffle barrier and breaks fusion here
     | "Reshuffle" >> Reshuffle()
     | "HeavyStep2" >> beam.ParDo(HeavyCompute())
     | "WriteToBQ" >> beam.io.WriteToBigQuery(table='PROJECT:DATASET.TABLE')
    )
```

Reshuffle behavior:

* Inserts a lightweight shuffle that redistributes elements across workers.
* Helps avoid single-worker bottlenecks when one key or element dominates.
* Adds network and shuffle costs — use it only when needed.

<Callout icon="lightbulb">
  Break fusion when you observe hotspots, heavy keys, or long-running fused transforms. `Reshuffle`, `GroupByKey`, or adding `ParDo` boundaries are practical ways to create runnable boundaries that enable rebalancing.
</Callout>

<Callout icon="warning">
  Avoid overusing forced shuffles. Each additional shuffle increases network traffic, I/O, and cost. Apply shuffle barriers only when they address clear performance issues such as skew or long-running fused operations.
</Callout>

## Real-world skew example

Imagine a purchase stream where one product ID appears 1,000,000 times while other IDs appear \~100 times. In a fused pipeline, that heavy key could be pinned to one worker, causing a long tail for the whole job.

How breaking fusion helps:

* A shuffle redistributes records for the heavy key across workers (or allows the runner to split the heavy bundle).
* Isolating expensive processing steps into separate transforms improves the runner’s ability to parallelize and scale those steps independently.
* Combined with autoscaling, this reduces tail latency and improves throughput.

## Recommended patterns and best practices

| Problem                       | Recommended action                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------- |
| Data skew / hotspots          | Force a shuffle (`Reshuffle` or `GroupByKey`) or use key-salting techniques; monitor per-key load |
| Long-running fused operations | Separate into multiple `ParDo`/DoFn transforms to create boundaries                               |
| Need to reduce network I/O    | Allow fusion for short, stateless transforms to avoid materialization                             |
| Controlling cost vs latency   | Minimize forced shuffles; benchmark before/after to validate ROI                                  |
| Windowing of unbounded data   | Choose windows and triggers that balance latency, completeness, and cost                          |

Operational tips:

* Use Dataflow monitoring to identify bundle duration, worker CPU/memory, and shuffle metrics.
* Benchmark with representative data distributions (including skewed keys).
* Combine code-level changes (reshuffle, boundaries) with pipeline options like autoscaling and worker machine type adjustments.

## Summary

* Use bounded sources for batch workflows and unbounded sources for streaming.
* Dataflow parallelizes via bundles and workers and adjusts capacity with autoscaling.
* Fusion reduces I/O but can create hotspots and make splitting harder.
* Break fusion selectively using `Reshuffle`, `GroupByKey`, or `ParDo` boundaries when you encounter skew or long-running fused steps.
* Always measure before and after changes — forced shuffles trade added network cost for better balance and lower tail latency.

## Links and references

* Apache Beam programming model: [https://beam.apache.org/](https://beam.apache.org/)
* Google Cloud Dataflow documentation: [https://cloud.google.com/dataflow/docs](https://cloud.google.com/dataflow/docs)
* Pub/Sub documentation: [https://cloud.google.com/pubsub/docs](https://cloud.google.com/pubsub/docs)

Thanks for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/73132211-ac55-49a0-9485-36b56b86346a" />
</CardGroup>
