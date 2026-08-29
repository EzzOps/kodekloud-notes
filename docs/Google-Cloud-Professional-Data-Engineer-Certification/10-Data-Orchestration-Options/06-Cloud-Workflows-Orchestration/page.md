# requirements:
# google-cloud-storage
# google-cloud-bigquery
#
import csv
import os
from tempfile import NamedTemporaryFile
from google.cloud import storage, bigquery

PROJECT_ID = "your-project-id"
BQ_DATASET = "your_dataset"
BQ_TABLE = "your_table"

storage_client = storage.Client()
bq_client = bigquery.Client(project=PROJECT_ID)

def gcs_csv_to_bigquery(event, context):
    """
    Cloud Function triggered by Cloud Storage when a CSV file is created.
    event contains keys like 'bucket' and 'name'.
    """
    bucket_name = event.get("bucket")
    object_name = event.get("name")
    if not bucket_name or not object_name:
        print("Missing bucket or name in event payload.")
        return

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    # Download file to a temporary local file
    with NamedTemporaryFile(delete=False) as tmp:
        blob.download_to_file(tmp)
        tmp_path = tmp.name

    try:
        # Simple CSV parsing and streaming into BigQuery via load job
        table_ref = bq_client.dataset(BQ_DATASET).table(BQ_TABLE)

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,  # adjust if CSV has header
            autodetect=True       # or provide schema explicitly
        )

        with open(tmp_path, "rb") as source_file:
            load_job = bq_client.load_table_from_file(
                source_file, table_ref, job_config=job_config
            )
        load_job.result()  # wait for completion
        print(f"Loaded {object_name} into {BQ_DATASET}.{BQ_TABLE}")

    except Exception as e:
        print(f"Error loading {object_name} to BigQuery: {e}")

    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
```

Practical tips and best practices:

* Keep functions small and focused; use them as glue code for reacting, transforming, routing, and automating data flows.
* Optimize for cold start where needed: choose runtimes with faster startup times, minimize dependency size, and prefer later-generation runtimes or smaller deployment artifacts.
* Use batching strategies (grouping multiple events into one processing job) to improve throughput and reduce per-invocation overhead where applicable.
* For high-throughput or long-running processing, evaluate concurrency settings, batching, and alternative compute options such as [Cloud Run](https://cloud.google.com/run/docs) or [Dataflow](https://cloud.google.com/dataflow/docs) depending on throughput, cost, and latency requirements.
* Ensure the function’s service account has least-privilege IAM permissions (e.g., read access to GCS objects, write access to BigQuery tables).
* Monitor cold starts, error rates, latency, and costs using Cloud Monitoring and Logs to tune memory, concurrency, and retry strategies.

> **lightbulb** Cloud Function quotas, free tiers, and supported features change over time and can differ by generation and region. Always consult the official Google Cloud documentation for current limits and pricing before production use.

References and further reading:

* [Cloud Functions Pricing](https://cloud.google.com/functions/pricing)
* [Cloud Functions Quotas](https://cloud.google.com/functions/quotas)
* [Google Cloud Run documentation](https://cloud.google.com/run/docs)
* [Google Cloud Dataflow documentation](https://cloud.google.com/dataflow/docs)
* [Kubernetes Concepts — if considering alternative orchestration](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

That wraps up performance characteristics and common data-processing patterns for Cloud Functions. The examples and patterns shown here illustrate how event-driven serverless functions integrate into real-world data pipelines.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/b69dec79-1428-41a6-8350-dd7443084b1d)


# Cloud Workflows Orchestration

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Orchestration-Options/Cloud-Workflows-Orchestration/page

Explains Google Cloud Workflows, a serverless orchestration service for sequencing API and microservice calls, when to use it and comparisons with Composer and Cloud Functions

Welcome back. In this lesson we focus on Cloud Workflows on Google Cloud: what it is, when to use it, and how it differs from Cloud Composer and Cloud Functions.

Previously we covered [Cloud Composer](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification), a managed Apache Airflow service for data pipelines. Cloud Workflows solves related but different problems: it’s a serverless orchestration service designed for sequencing API calls and microservice interactions rather than heavy-duty data engineering.

## What is Cloud Workflows?

Cloud Workflows is a serverless, event-driven orchestration service that sequences API and microservice calls as a single, maintainable execution. It’s ideal for application-level orchestration, business processes, and API sequencing where you want minimal operational overhead.

Key capabilities

* Event-driven, serverless execution: run workflows in response to HTTP requests, Pub/Sub events, Cloud Scheduler, and other triggers.
* Automatic scaling: scales from zero to meet demand — no capacity planning.
* Pay-per-invocation billing: you pay for workflow executions and steps.
* Multiple triggers: HTTP, Pub/Sub, Cloud Scheduler, and integrations with other Google Cloud services.
* Isolated, stateless executions: each run is independent; step-to-step data belongs to the execution.
* Fast startup: low latency for user-facing orchestrations.

> **lightbulb** A concise exam-style answer: Cloud Workflows is serverless orchestration because it is event-driven, auto-scales from zero, supports multiple triggers, bills per execution, and requires no server or VM management.

<Frame>
  <img alt="A slide titled &#x22;Cloud Workflows&#x22; showing six colorful boxes with key features. The boxes list: event-driven serverless compute; automatic scaling (0 to millions); pay-per-invocation model; multiple trigger types; stateless execution; and sub-second response times." />
</Frame>

## When to use Cloud Workflows

* Orchestrate ordered API calls that pass intermediate data between steps.
* Implement multi-step business processes (e.g., order processing) with conditional logic, retries, and error handling.
* Coordinate microservices without building or managing orchestration infrastructure.
* Replace brittle function chains with readable, maintainable orchestration logic.

## Why not just use a single Cloud Function?

* Cloud Functions are stateless and have execution-time limits; chaining complex logic across many steps quickly becomes hard to maintain.
* Workflows provides explicit sequencing, in-execution data passing, retry policies, and structured branching — all in one place.
* Use Cloud Functions for single-purpose handlers and short-running tasks; use Workflows to coordinate those functions as part of a larger process.

## Composer vs Workflows — short comparison

Use Cloud Composer (Apache Airflow) when:

* You need complex, scheduled, data-oriented pipelines.
* DAG-centric orchestration and heavy data-engineering integrations are required.

Use Cloud Workflows when:

* You need lightweight, serverless orchestration of APIs and microservices.
* You prefer pay-per-execution pricing and minimal operational overhead.

## Cloud Functions vs Workflows — clear differences

| Dimension          |                                                   Cloud Functions | Cloud Workflows                                                                                  |
| ------------------ | ----------------------------------------------------------------: | ------------------------------------------------------------------------------------------------ |
| Purpose            |            Single-purpose serverless compute responding to events | Orchestrates and sequences calls to services/APIs                                                |
| State & Sequencing | Stateless per invocation; chaining requires external coordination | Passes data between steps in a single execution                                                  |
| Best for           |                      Small handlers, webhooks, event-driven logic | Multi-step processes with conditionals, retries, branching                                       |
| Billing            |     Billed for execution time and resource usage of each function | Billed per workflow invocation and step execution (`https://cloud.google.com/workflows/pricing`) |
| Typical use case   |                                 Event transforms, background jobs | Order processing, API orchestration, microservice coordination                                   |

## Short scenario (example)

Placing an online order orchestration:

1. Workflow receives an order event.
2. Call payment API and wait for confirmation.
3. If payment succeeds, call inventory API.
4. If inventory is available, call shipment API and notify the customer.
5. If any step fails, perform retries or compensation actions (e.g., refund).

Cloud Workflows expresses this in readable steps with branching and retry policies, avoiding brittle chains of stateless functions.

## Minimal example — YAML workflow

Below is a simple illustrative YAML workflow that sequences two HTTP calls and handles a conditional response. This sample shows the high-level structure (steps, calls, and branching).

```yaml theme={null}
main:
  steps:
    - init:
        assign:
          - orderId: ${"ORD-12345"}
    - callPayment:
        call: http.post
        args:
          url: https://payments.example.com/charge
          body:
            orderId: ${orderId}
            amount: 100
    - checkPayment:
        switch:
          - condition: ${callPayment.status == 200}
            next: checkInventory
          - next: paymentFailed
    - checkInventory:
        call: http.post
        args:
          url: https://inventory.example.com/check
          body:
            orderId: ${orderId}
    - paymentFailed:
        return: "Payment failed; initiating compensation"
    - done:
        return: "Order processed"
```

Refer to the official [Cloud Workflows documentation](https://cloud.google.com/workflows/docs) for full syntax, retry strategies, and authentication patterns.

## Quick troubleshooting and tips

* Use step-level retries and exponential backoff for transient failures.
* Keep sensitive data out of logs; use Secret Manager and proper IAM roles.
* Visualize execution traces in the Cloud Console to debug step-by-step failures.
* Test each API call independently before composing them into a workflow.

## Comparison table (Composer, Workflows, Functions)

| Service                  |                                         Best for | Triggers                                | State handling                             | Example use                               |
| ------------------------ | -----------------------------------------------: | --------------------------------------- | ------------------------------------------ | ----------------------------------------- |
| Cloud Composer (Airflow) |     Complex data pipelines, DAGs, scheduled jobs | Scheduler, sensors, external triggers   | DAG-level state managed by Airflow         | ETL pipelines, data engineering workflows |
| Cloud Workflows          | API & microservice orchestration, business logic | HTTP, Pub/Sub, Scheduler, service calls | Passes data between steps within execution | Order processing, API sequencing          |
| Cloud Functions          |                 Event-driven single-task compute | Pub/Sub, HTTP, Storage, Firestore       | Stateless per invocation                   | Webhooks, lightweight data transforms     |

## Links and references

* [Cloud Workflows documentation](https://cloud.google.com/workflows/docs)
* [Cloud Workflows pricing](https://cloud.google.com/workflows/pricing)
* [Cloud Composer (Apache Airflow)](https://airflow.apache.org/)
* [Cloud Functions documentation](https://cloud.google.com/functions/docs)

Summary
Cloud Workflows provides serverless, scalable orchestration for APIs and microservices. Choose the right tool:

* Composer for complex, scheduled data pipelines;
* Workflows for application-level orchestration and API sequencing;
* Cloud Functions for single-purpose, event-driven compute.

We’ll follow up with hands-on comparisons and examples to help decide between Cloud Functions and Cloud Workflows in real scenarios.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/02c94efe-b61a-4c62-a410-e7bdb266a0f4)
