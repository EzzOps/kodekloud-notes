# example_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "data_engineer",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def extract(**kwargs):
    # Example: pull orders from Cloud SQL and store a file in GCS
    # Return a small reference (e.g., path or job id) that downstream tasks can use
    extracted_path = "gs://my-bucket/orders/2023-01-01.json"
    return extracted_path  # returned value becomes an XCom

def validate(**kwargs):
    ti = kwargs["ti"]
    extracted = ti.xcom_pull(task_ids="extract")
    # Validate extracted data
    valid = True
    if not valid:
        raise ValueError("Validation failed")
    return "validated"

def transform(**kwargs):
    ti = kwargs["ti"]
    extracted = ti.xcom_pull(task_ids="extract")
    # Launch Dataflow job or run transformation logic
    transformed_path = "gs://my-bucket/transformed/2023-01-01.parquet"
    return transformed_path

def load(**kwargs):
    ti = kwargs["ti"]
    transformed = ti.xcom_pull(task_ids="transform")
    # Load transformed data into BigQuery
    return "loaded"

with DAG(
    dag_id="ecommerce_etl",
    default_args=default_args,
    description="Daily ETL for e-commerce orders",
    schedule_interval="0 2 * * *",  # daily at 02:00
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    t_extract = PythonOperator(task_id="extract", python_callable=extract)
    t_validate = PythonOperator(task_id="validate", python_callable=validate)
    t_transform = PythonOperator(task_id="transform", python_callable=transform)
    t_load = PythonOperator(task_id="load", python_callable=load)

    # Set dependencies (extract -> validate -> transform -> load)
    t_extract >> t_validate >> t_transform >> t_load
```

Practical notes on XComs and the TaskFlow API

* Airflow 2.x′s TaskFlow API (using `@task`) pushes return values to XCom automatically and can simplify code.
* When using `PythonOperator`, return values can be pushed if `do_xcom_push` is enabled, or use `ti.xcom_push(...)`.
* Keep XCom payloads small — use references (GCS paths, job IDs) rather than large datasets.

Monitoring and troubleshooting Composer workloads

* Access the Airflow UI from the Cloud Composer environment page in the GCP Console.
* The UI shows DAG graphs, task instance status, logs, and historical runs.
* Task logs are stored in the configured Cloud Storage bucket; you can view logs via the UI or directly in GCS.
* Use Cloud Monitoring to create alerting policies for failed DAG runs or abnormal metrics.

Cost considerations and alternatives
Cloud Composer runs several managed services (Cloud SQL, GKE node pools, Cloud Storage, App Engine/managed runtime, monitoring). That can lead to significant cost for small or infrequent workloads.

Alternatives to consider for lower-cost or serverless orchestration:

* [Cloud Functions](https://cloud.google.com/functions) — event-driven single-purpose functions.
* [Cloud Workflows](https://cloud.google.com/workflows) — manage serverless orchestration for APIs and services.
* Combine scheduling with Dataflow or Dataproc jobs for batch pipelines.
* [Cloud Data Fusion](https://cloud.google.com/data-fusion) — low-code ETL for typical data integration scenarios.

<Callout icon="warning">
  Cloud Composer environments involve multiple managed services and can incur significant costs. Evaluate workload size and frequency before choosing Composer, and consider alternatives for small or infrequent jobs.
</Callout>

Summary

* Cloud Composer is Google’s managed Apache Airflow: author DAGs in Python and let Google manage the underlying infrastructure.
* Composer maps Airflow components to Google-managed services (GKE, Cloud SQL, Cloud Storage, App Engine/managed runtime, Cloud Monitoring).
* DAGs express workflows using tasks, operators, dependencies, schedules, context, and XComs.
* Composer is ideal for large-scale orchestration but evaluate cost and alternatives for simpler scenarios.

That’s it for this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/3066849e-e3c1-4137-bd2e-453ef5952d7f" />
</CardGroup>


# Cloud Composer Orchestration Patterns Triggering Methods

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Orchestration-Options/Cloud-Composer-Orchestration-Patterns-Triggering-Methods/page

Explains Cloud Composer DAG triggering methods and orchestration patterns for building reliable, decoupled, and scalable Airflow workflows on Google Cloud.

Welcome back. In this lesson we’ll cover orchestration patterns and DAG triggering methods in Google Cloud Composer. Cloud Composer is Google’s managed Apache Airflow service that simplifies building, scheduling, and monitoring data pipelines across Google Cloud services. This article focuses on how workflows (DAGs) are started and how to structure tasks inside those DAGs for clarity, reliability, and scalability.

Cloud Composer runs Apache Airflow under the hood, so most Airflow concepts apply. Google adds managed infrastructure and integrations for GCP services, which makes connecting your orchestration layer to the rest of your data stack easier and more reliable.

Before designing a complex pipeline, ask: what starts the DAG? A DAG (directed acyclic graph) represents a workflow composed of tasks that execute in a defined order with no loops — hence “acyclic.” Below are the most common methods to trigger DAG runs in Cloud Composer.

## Triggering methods overview

| Trigger type   | When to use                                            | Example / Implementation                                                                       |
| -------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Schedule-based | Regular, time-based workloads (nightly/weekly/monthly) | Cron-style `schedule_interval='0 2 * * *'` or Airflow schedules                                |
| Event-driven   | Start workflows in response to external events         | Publish a Pub/Sub message; a Cloud Function/Cloud Run translates event into an Airflow trigger |
| Manual         | Ad-hoc testing, reprocessing, or emergency runs        | Start DAG from Airflow UI or Google Cloud Console                                              |
| API-based      | Programmatic start from external systems               | Call Airflow REST API or Composer-provided endpoints from a microservice                       |
| Sensor-based   | Wait for data/files or external job completion         | Airflow `Sensor` or deferrable sensors that pause until conditions are met                     |

Use these patterns to make your architecture reactive rather than purely time-driven—improving responsiveness and often reducing idle compute cost.

### Schedule-based triggers

Schedule-based triggers use cron expressions or Airflow schedule strings to run DAGs at predictable intervals. They are ideal for recurring tasks such as nightly ETL, periodic reports, and monthly aggregations.

Example: `schedule_interval='0 2 * * *'` runs daily at 02:00.

### Event-driven triggers (Pub/Sub)

Event-driven pipelines react to messages or events. A common pattern on GCP is to publish a message to Pub/Sub when new data arrives; a lightweight component (Cloud Function or Cloud Run) then triggers the appropriate DAG by calling the Airflow REST API or using Composer-specific endpoints.

This pattern decouples your producers from Airflow and improves resilience.

### Manual triggers

Operators and developers can trigger DAGs manually using the Airflow web UI or the Google Cloud Console. Manual runs are useful for debugging, reprocessing failed runs, or one-off jobs that don’t belong on a schedule.

### API-based triggers

External applications can start DAGs programmatically via the Airflow REST API or Composer integration endpoints. Use this when a downstream system must trigger a workflow as part of a larger automated flow.

### Sensor-based triggers

Sensors are special Airflow tasks that wait until a condition is met (e.g., file arrival, partition availability, or external job completion). In managed environments, prefer deferrable sensors to reduce worker slot usage during long waits.

<Callout icon="warning">
  Avoid tight coupling between production microservices and Airflow. If a core service depends directly on Airflow availability, an Airflow outage could affect business-critical flows. Prefer decoupling patterns such as publishing events to Pub/Sub or a durable queue and letting an independent component trigger the DAG.
</Callout>

Quick exam hint: Which triggering method would you use when a Pub/Sub message indicates new data is available?\
Answer: event-driven triggers using Pub/Sub.

<Frame>
  <img alt="A presentation slide titled &#x22;Triggering Methods&#x22; showing five colorful rounded boxes that list trigger types: Schedule-based (Cron), Event-driven (Pub/Sub), Manual triggers (Console), API-based triggers, and Sensor-based (File/Data)." />
</Frame>

Triggering methods let your workflows be reactive and scalable, and they inform architectural choices around decoupling, error handling, and reliability.

## Orchestration patterns inside a DAG

How tasks are organized inside a DAG affects readability, performance, and scalability. These patterns apply to both open-source Airflow and Cloud Composer.

1. Linear (sequential)
   * Pattern: A → B → C
   * Use: Simple, predictable flows (e.g., extract → transform → load).

2. Parallel (fan-out / join)
   * Pattern: A triggers B, C, D in parallel → then E runs after all complete.
   * Use: Independent tasks that can run concurrently to speed up pipelines.

3. Branching (conditional paths)
   * Pattern: A → choose B or C → continue with D
   * Use: Conditional logic and alternative flows (e.g., if yesterday’s data exists proceed, else notify).

4. Dynamic task generation / mapping
   * Pattern: Create tasks at runtime based on input or metadata.
   * Use: One task per file/partition using Airflow’s task mapping or TaskFlow API to scale dynamically.

5. Grouping sub-workflows (TaskGroups / modular DAGs)
   * Pattern: Group related tasks together to simplify the main DAG view.
   * Use: Improve readability and maintainability. Prefer TaskGroups or separate DAGs over SubDAGs.

A minimal example of a scheduled, linear DAG (Airflow 2.x compatible):

```python theme={null}
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='example_schedule_dag',
    default_args=default_args,
    description='Example schedule-based DAG',
    schedule_interval='0 2 * * *',  # daily at 02:00
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    extract = BashOperator(task_id='extract', bash_command='echo extracting')
    transform = BashOperator(task_id='transform', bash_command='echo transforming')
    load = BashOperator(task_id='load', bash_command='echo loading to BigQuery')

    extract >> transform >> load
```

Visual summary of patterns:

* Linear: A → B → C
* Parallel: A → (B, C, D) → E (E waits for all)
* Branching: A → (B or C) → D
* Dynamic: number of tasks determined at runtime (task mapping)
* Grouping: collapse related tasks into a TaskGroup for clarity

## Design considerations & best practices

* Decouple triggers from your core microservices using durable messaging (Pub/Sub) to avoid single points of failure.
* Use deferrable sensors when available to reduce resource consumption during long waits.
* Prefer TaskGroups and modular DAGs over SubDAGs for readability and maintainability.
* Limit long-running synchronous API calls—use asynchronous notification patterns where possible.
* Monitor DAG runs and set alerting for failed runs, unexpected latencies, and resource saturation.

## Summary

* Triggering methods: schedule-based, event-driven (Pub/Sub), manual, API-based, and sensor-based.
* Orchestration patterns: linear, parallel, branching, dynamic task generation, and grouping (TaskGroups).
* Cloud Composer offers Airflow orchestration with managed GCP integrations—design choices around coupling, sensors, and dynamic tasks strongly affect reliability and cost.

See also:

* [Cloud Composer documentation](https://cloud.google.com/composer/docs)
* [Apache Airflow documentation](https://airflow.apache.org/)
* [Google Cloud Pub/Sub documentation](https://cloud.google.com/pubsub)

Cloud Composer monitoring, security, IAM, and operational practices are important complementary topics—we’ll cover those in a later lesson. See you next time.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/710e1434-40a3-4662-a03b-5903213be847" />
</CardGroup>
