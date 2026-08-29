# Dataflow Introduction

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Dataflow-Introduction/page

Overview of Google Cloud Dataflow, a managed serverless service running Apache Beam pipelines for unified batch and streaming data processing, autoscaling, and exporting results to BigQuery or Cloud Storage

Welcome back. In this lesson we'll introduce Google Cloud Dataflow and walk through an end-to-end view of how data is processed using the Apache Beam programming model. This will help you recognize Dataflow in architecture diagrams and prepare for exam-style questions.

What is Dataflow?

* Dataflow is Google Cloud’s fully managed, serverless service for running data processing pipelines written with the Apache Beam SDKs.
* It executes Beam pipelines (the sequence of transforms, windowing, and triggers you define), and it handles provisioning, autoscaling, checkpointing, and operational tuning so you can focus on logic rather than infrastructure.

When to use Dataflow

* Use Dataflow when you need a managed service that can run both batch and streaming workloads with minimal operational overhead.
* Dataflow is ideal for ETL, real-time analytics, event processing, and transforming data for sinks like BigQuery or Cloud Storage.

Batch vs streaming inputs

| Input type | Description                                                                                            | Typical use cases                                   |
| ---------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| Batch      | Processes data in discrete chunks (for example, nightly CSV exports or periodic database dumps).       | Daily reports, bulk ETL, backfills                  |
| Streaming  | Processes data continuously as it arrives (for example, IoT telemetry, app logs, or Pub/Sub messages). | Real-time dashboards, alerting, streaming analytics |

Dataflow supports both batch and streaming within the same Beam pipeline model, simplifying development and reuse.

Apache Beam and Dataflow

* Apache Beam is the open-source programming model and SDK that defines how to express data-processing pipelines (transforms, windowing, triggers, and I/O).
* Dataflow is a managed Beam runner on Google Cloud that executes Beam pipelines and manages underlying compute, autoscaling, and reliability concerns.
* The Beam portability model means you can run the same pipeline code on different runners (for example, Dataflow, Apache Flink, or Apache Spark) without changing business logic.

Where processed data goes
After processing, Dataflow pipelines typically write results to one or more sinks depending on your needs:

* Cloud Storage — for files, batch exports, or intermediate artifacts.
* BigQuery — for analytics, BI, or serving results to dashboards.
* Other sinks — Pub/Sub, databases, or custom sinks as required by your pipeline.

Key advantages of Dataflow

| Advantage            | What it provides                                              |
| -------------------- | ------------------------------------------------------------- |
| Unified model        | One programming model for both batch and streaming            |
| Portable code        | Beam pipelines can run on multiple runners                    |
| Serverless & managed | Google handles provisioning, autoscaling, and fault tolerance |
| Real-time processing | Low-latency streaming with Beam windowing and triggers        |

<Callout icon="lightbulb">
  Dataflow is best when you want a managed, autoscaling service to run Beam pipelines that handle both batch and streaming workloads with minimal infrastructure management.
</Callout>

Quick exam-style question

Which component provides the programming model used by Dataflow: Cloud Storage, Apache Beam, or BigQuery?

Answer: Apache Beam — Beam defines the pipeline programming model; Dataflow executes Beam pipelines.

Summary

* Dataflow is a serverless, autoscaling engine for running Apache Beam pipelines.
* It supports both batch and streaming workloads in the same programming model and writes results to sinks such as Cloud Storage or BigQuery.
* Use Dataflow when you need a managed solution for scalable ETL, streaming analytics, or other pipeline-based data processing tasks.

Internal components and deeper architecture (runners, worker pools, job graph, checkpointing, etc.) will be covered in a subsequent lesson.

<Frame>
  <img alt="A slide titled &#x22;Dataflow – Introduction&#x22; showing a serverless data-processing diagram where batch and streaming inputs go into Apache Beam/Dataflow and output to Cloud Storage and BigQuery. Below the diagram are highlighted benefits like a unified model, Apache Beam SDK, serverless auto-scaling, and real-time processing." />
</Frame>

Links and references

* [Google Cloud Dataflow](https://cloud.google.com/dataflow)
* [Apache Beam](https://beam.apache.org/)
* [Cloud Storage](https://cloud.google.com/storage)
* [BigQuery](https://cloud.google.com/bigquery)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/06ddd948-c36b-4056-bd79-00b31dffca64" />
</CardGroup>
