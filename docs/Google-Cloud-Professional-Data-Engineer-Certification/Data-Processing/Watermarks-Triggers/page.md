# Copy a directory recursively to a GCS bucket (parallelized)
gsutil -m cp -r /local/data/path gs://my-bucket/path

# Or synchronize source to destination (efficiently updates changed files)
gsutil -m rsync -r /local/data/path gs://my-bucket/path
```

* For very large or offline transfers, consider Transfer Appliance or the Storage Transfer Service. Use checksums or object metadata to validate integrity after transfer.

<Callout icon="warning">
  Always validate transferred data (checksums, row counts) and run representative jobs on Dataproc before decommissioning legacy clusters. Small-file patterns and schema differences are common migration pitfalls.
</Callout>

4. Execution

* Provision test Dataproc clusters sized for your peak workloads, using initialization actions if you need extra libraries.
* Update job configuration to reference `gs://` paths and test end-to-end.
* Measure runtime and I/O characteristics; iterate on partitioning, shuffle behavior, and executor sizing.
* After validation, schedule a cutover: run final incremental sync if needed, switch production jobs to Dataproc, and decommission old clusters.

<Frame>
  <img alt="An infographic titled &#x22;Migration to Dataproc&#x22; showing four steps—Step 01 Assessment, Step 02 Planning, Step 03 Data Transfer, and Step 04 Execution—each with bulleted tasks underneath. Examples of tasks include analyzing the existing cluster, choosing storage/designing cluster size, moving data with gsutil or Storage Transfer, and deploying and testing jobs on Dataproc." />
</Frame>

## Final notes and best practices

* Prefer GCS for long-term analytics datasets on Dataproc. It decouples storage from compute and reduces lifecycle management overhead.
* Use ephemeral HDFS or Local SSD for shuffle or temporary caches only while the cluster is running.
* Keep Persistent Disks for workloads that need durable block storage.
* Apply a phased migration (assess → plan → transfer → execute) and validate at each phase.
* Monitor costs and performance post-migration; tune partition sizes and file formats (Parquet/Avro) to reduce small-file overhead.

## Links and references

* Dataproc: [https://cloud.google.com/dataproc](https://cloud.google.com/dataproc)
* GCS connector and Dataproc: [https://cloud.google.com[AWS_SECRET_ACCESS_KEY]-storage](https://cloud.google.com[AWS_SECRET_ACCESS_KEY]-storage)
* gsutil: [https://cloud.google.com/storage/docs/gsutil](https://cloud.google.com/storage/docs/gsutil)
* Storage Transfer Service: [https://cloud.google.com/storage-transfer-service](https://cloud.google.com/storage-transfer-service)
* Transfer Appliance: [https://cloud.google.com/transfer-appliance](https://cloud.google.com/transfer-appliance)
* Signed URLs for ingestion: [https://cloud.google.com/storage/docs/access-control/signed-urls](https://cloud.google.com/storage/docs/access-control/signed-urls)

This concise overview provides a practical decision framework for Dataproc storage and a migration checklist you can act on. A follow-up hands-on demo can walk through provisioning a Dataproc cluster and running sample jobs to validate these patterns in your environment.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/d5278dc0-a324-4ec9-a034-a1fdbc7237e9" />
</CardGroup>


# Watermarks Triggers

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Watermarks-Triggers/page

Explains watermarks, triggers, and allowed lateness in Dataflow and Apache Beam streaming, showing trigger types, handling late events, and balancing latency versus correctness.

Welcome back.

In this lesson we’ll explore watermarks and triggers in Google Cloud Dataflow and Apache Beam streaming pipelines. After covering windowing (grouping streaming data into time-based buckets), the next challenges are: how to handle late-arriving events and when to emit windowed results. Watermarks and triggers let Dataflow make those decisions reliably and flexibly.

## Scenario: counting website clicks in 10-second windows

* Imagine counting website clicks in fixed, 10-second event-time windows (0–10s, 10–20s, ...).
* Some clients are on slow networks, so click events for a window may arrive late.

Example timeline:

* Clicks with event timestamps 3s, 5s, and 8s arrive before the window end (0–10s) — these are on-time.
* Other clicks with event timestamps within 0–10s may arrive after the window end (after 10s) and are considered late.
* Questions to answer: when should we emit the aggregated result for that window? Wait for late events or emit early and update later?

## How watermarks help

* A watermark is the system’s estimate of event-time progress: the best guess of how far event time has advanced for the stream.
* If the watermark is at 8s, Dataflow estimates that most events with event-time ≤ 8s have been seen.
* When the watermark passes a window end (for example, 10s), that commonly triggers emission of that window’s result.
* As the watermark advances (e.g., to 15s), Dataflow assumes late events for earlier windows are increasingly unlikely.

<Callout icon="lightbulb">
  Watermarks are heuristics, not strict guarantees. They represent the system’s estimate of completeness for event-time processing. Design triggers and allowed-lateness with that uncertainty in mind.
</Callout>

In short: watermarks track event-time progress and guide when to trigger windowed outputs.

## Trigger types

There are several trigger patterns you can apply to emit results for windows. Below is a concise comparison, followed by a diagram that visualizes the common trigger types.

| Trigger Type                         | When it fires                                 | Typical use case                                 | Example                                          |
| ------------------------------------ | --------------------------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| Event-time trigger (watermark-based) | When the watermark passes the window end      | Correctness relative to event timestamps         | Final aggregation when watermark > window end    |
| Processing-time trigger              | Based on system clock (processing time)       | Low-latency dashboards or periodic early updates | Emit partial results every 5s of processing time |
| Data-driven trigger                  | When a data condition is met (count, pattern) | Emit when enough data or a condition occurs      | Fire after N elements or on pattern detection    |

<Frame>
  <img alt="A presentation slide titled &#x22;Common Trigger Types&#x22; showing three colored boxes: Event Time Trigger, Processing Time Trigger, and Data-Driven Trigger with brief &#x22;When&#x22; and &#x22;Use&#x22; notes beneath each. Examples listed include &#x22;watermark passes window end,&#x22; &#x22;fixed intervals of processing time,&#x22; and &#x22;after N elements or specific conditions.&#x22;" />
</Frame>

Details:

* Event-time (watermark) triggers are the most common for event-time correctness because they align output with event timestamps.
* Processing-time triggers give predictable low-latency outputs regardless of event-time progress.
* Data-driven triggers are ideal when the business logic requires emission after a condition (e.g., first 100 events).

Combining triggers

* It’s common to combine triggers in a multi-stage strategy:
  * Early firings (processing-time or data-driven) to provide low-latency, partial results.
  * A final firing when the watermark passes the window end to provide a stable, accurate result.
* This hybrid approach balances latency and correctness.

## Handling late data (allowed lateness)

* Allowed-lateness (also called grace period) defines how long late events can still update a closed window.
* Example: an allowed-lateness of 5 minutes means late events for a given window that arrive within 5 minutes after the window end will still be incorporated, and the window result can be re-emitted (updated).
* After the allowed-lateness expires, events that belong to that window are considered too late. Dataflow can:
  * Drop them, or
  * Route them to a dead-letter or side output for separate handling and analysis.

<Frame>
  <img alt="A slide titled &#x22;Handling Late Data&#x22; showing a flow from a &#x22;Late Data&#x22; block to an &#x22;Update Window&#x22; block. Below is an &#x22;Allowed Lateness&#x22; note explaining a grace period (e.g., 5 minutes), that late data within the period updates the window, and data after the period is dropped or sent to a dead letter." />
</Frame>

<Callout icon="warning">
  If you set allowed-lateness too short, you may lose valid late events. If you set it too long, you increase state retention and resource usage. Tune allowed-lateness to balance accuracy and cost.
</Callout>

## Choosing the right balance

* Use event-time (watermark) triggers when correctness relative to event timestamps matters most (financial aggregation, audits).
* Use processing-time triggers when you need consistent, low-latency updates (live dashboards, monitoring).
* Combine early (processing-time or data-driven) firings with a final watermark-based firing to get both low latency and eventual correctness.
* Configure allowed-lateness to control how long you accept updates for closed windows, balancing result accuracy against state and cost.

## Links and references

* [Apache Beam Windowing and Triggers Guide](https://beam.apache.org/documentation/programming-guide/#windowing)
* [Google Cloud Dataflow Documentation](https://cloud.google.com/dataflow/docs)
* [Streaming Analytics Patterns and Best Practices](https://cloud.google.com/solutions/streaming-analytics)

That concludes this lesson on watermarks and triggers.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/1f2d95bd-0cda-4780-8697-4f002acfa85b" />
</CardGroup>
