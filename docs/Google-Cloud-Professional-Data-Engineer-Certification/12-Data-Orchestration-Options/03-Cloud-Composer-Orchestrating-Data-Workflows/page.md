# Cloud Composer Orchestrating Data Workflows

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Orchestration-Options/Cloud-Composer-Orchestrating-Data-Workflows/page

Introduction to Cloud Composer, Google’s managed Apache Airflow for orchestrating, scheduling, and monitoring data pipelines across GCP services.

Hello and welcome back.

In this lesson we’ll explore Cloud Composer — Google Cloud’s managed service for orchestrating data workflows. Composer runs Apache Airflow for you, so you get familiar DAG-based workflow authoring and the Airflow UI while Google handles the underlying infrastructure: scaling, monitoring, upgrades, and other operational tasks.

What problem does an orchestrator solve? Data pipelines typically require ordered steps (extract → transform → load → validate) and reliable scheduling. A workflow orchestrator ensures steps run in the correct order, handles retries, and centralizes monitoring and alerting.

<Frame>
  <img alt="A slide titled &#x22;Orchestrating Data Workflow&#x22; showing a central &#x22;Workflow Orchestrator&#x22; banner above three rounded boxes labeled &#x22;Data stored,&#x22; &#x22;Data processed,&#x22; and &#x22;Data shared&#x22; inside a dashed container. The slide also includes a small &#x22;© Copyright KodeKloud&#x22; at the bottom left." />
</Frame>

By the end of this lesson you will understand what Cloud Composer does, its core components, and how it fits into a typical data pipeline.

Scenario: a simple e-commerce ETL pipeline

* Regularly extract orders from Cloud SQL
* Transform the data (for example with Dataflow)
* Load the transformed results into BigQuery
* Send alerts when steps fail

Cloud Composer orchestrates and schedules these steps so they run automatically and reliably.

<Frame>
  <img alt="A slide diagram of a GCP — Apache Airflow e‑commerce data pipeline showing five colored stages: Extract, Transform, Load, Orchestrate, and Monitor. It notes sources and tools (Orders from Cloud SQL, clean in Dataflow, results to BigQuery, schedule with Composer, alerts via Cloud Functions)." />
</Frame>

Why use an orchestrator?

* Centralized scheduling and dependency management
* Standardized retry and failure handling
* Centralized logs, metrics, and alerting
* Easier to author and maintain many pipelines

What is Cloud Composer?

* Managed Apache Airflow environment hosted on Google Cloud.
* You write DAGs in Python and use the familiar Airflow UI.
* Google manages the underlying services (provisioning, scaling, upgrades, monitoring).

<Callout icon="lightbulb">
  Cloud Composer exposes the familiar Airflow UI and DAG semantics but handles provisioning and management of the underlying services for you.
</Callout>

How Composer maps Airflow to Google-managed services

| Composer component          |                          Backing Google-managed service | Purpose                        |
| --------------------------- | ------------------------------------------------------: | ------------------------------ |
| Airflow workers & scheduler |       [GKE](https://cloud.google.com/kubernetes-engine) | Runs tasks and the scheduler   |
| Airflow metadata DB         |               [Cloud SQL](https://cloud.google.com/sql) | Task states, DAG history       |
| DAGs & logs storage         |       [Cloud Storage](https://cloud.google.com/storage) | Stores DAG files and task logs |
| Airflow webserver / UI      |                           App Engine or managed runtime | Access the Airflow UI          |
| Monitoring & alerts         | [Cloud Monitoring](https://cloud.google.com/monitoring) | Metrics and alerting           |

Core Airflow/DAG fundamentals

* Tasks: units of work inside a DAG.
* Operators: task templates that define work to execute.
* Dependencies: edges that control execution order.
* Schedules: cron or preset expressions that trigger DAG runs.
* Context: runtime metadata available to tasks.
* XCom: small payload mechanism for task-to-task data exchange.

Common GCP-focused operators

| Operator                                                                                            | Typical use                       |
| --------------------------------------------------------------------------------------------------- | --------------------------------- |
| [BigQuery operator](https://cloud.google.com/bigquery)                                              | Querying/loading data to BigQuery |
| [Dataflow operator](https://cloud.google.com/dataflow)                                              | Launch Dataflow pipelines         |
| [Dataproc operator](https://cloud.google.com/dataproc)                                              | Submit Spark/Hadoop jobs          |
| [GCS operator](https://cloud.google.com/storage)                                                    | Transfer or manage objects in GCS |
| [Pub/Sub operator](https://cloud.google.com/pubsub)                                                 | Publish/subscribe messages        |
| [Python operator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html) | Run custom Python logic           |

You can also use third-party operators (e.g., AWS S3, Salesforce). Store credentials securely (for example in [Secret Manager](https://cloud.google.com/secret-manager)) and expose them to Airflow via Connections.

<Frame>
  <img alt="A slide titled &#x22;DAG Development and Workflow Design&#x22; that lists DAG components like Tasks, Operators, Dependencies, Schedule, Context and XComs. Below it is a row of common GCP operators (BigQuery, Dataflow, Dataproc, GCS, Pub/Sub, Python) and a KodeKloud copyright." />
</Frame>

Minimal DAG example
Below is a compact DAG that runs daily and demonstrates extract → validate → transform → load with XCom usage. Replace the function bodies with your real extraction, validation, and transformation logic or the appropriate GCP operators.

```python theme={null}
