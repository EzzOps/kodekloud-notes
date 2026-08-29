# Data Fusion Architecture Core Components

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Integration-Transformation-Tools/Data-Fusion-Architecture-Core-Components/page

Overview of Google Cloud Data Fusion, a managed visual, code-free ETL service that builds, runs, and monitors data integration pipelines with connectors, autoscaling, batch and streaming support

Hello and welcome back.

This lesson explores Google Cloud Data Fusion and why a managed visual ETL service like this exists. We'll cover what Data Fusion is, its core capabilities, how it fits into a modern data architecture, and a practical e-commerce example that shows its value.

Problem statement

* Organizations collect data across many systems: customer orders in MySQL, product catalogs in PostgreSQL, and clickstream logs in Cloud Storage.
* Business users need a unified, analytics-ready view, but assembling and transforming that data traditionally required custom ETL code, multiple tools, and ongoing maintenance.
* A managed, visual data-integration platform reduces development and operational overhead while improving time-to-insight.

What is Cloud Data Fusion?

* Cloud Data Fusion is a fully managed data integration service on Google Cloud that provides a visual, drag-and-drop interface to build, run, and monitor ETL/ELT pipelines.
* It is built on the open-source CDAP platform; Google manages the control plane and runtime so you don’t have to provision or maintain servers.
* Typical use cases include data ingestion, transformation, enrichment, and loading into analytics systems like BigQuery.

Key capabilities

| Capability                 | What it provides                                                           | Typical examples                                                         |
| -------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Code-free visual ETL       | Drag-and-drop pipeline builder for sources, transforms, and sinks          | Create joins, aggregations, and schema mappings without writing Java/SQL |
| 150+ pre-built connectors  | Out-of-the-box plugins to common sources and targets                       | MySQL, PostgreSQL, Cloud Storage, BigQuery, Pub/Sub                      |
| Autoscaling via Dataproc   | Dynamically scale underlying Spark/Dataproc clusters for heavy jobs        | Handle large batch loads or compute-heavy transformations                |
| Batch & streaming          | Support for both scheduled batch and streaming pipelines                   | Periodic data syncs or near-real-time event processing                   |
| Monitoring & lineage       | Runtime metrics, logs, and data lineage for troubleshooting and governance | Track how records move and change through your pipelines                 |
| Hybrid/multi-cloud support | Connect on-premises and multi-cloud sources                                | Ingest from databases behind a firewall or other cloud providers         |

How it adds value to your architecture

* Accelerates development by lowering the learning curve for ETL tasks and enabling data engineers and analysts to prototype quickly.
* Reduces operational complexity because the platform and CDAP runtime are managed by Google.
* Provides enterprise-grade security controls and data lineage for governance and compliance.
* Enables faster delivery of analytics and operational insights by simplifying the path from sources to analytics targets.

Real-world example: e-commerce data integration
Scenario: Thousands of transactions land in a MySQL orders table daily; product metadata lives in PostgreSQL; clickstream events are written to Cloud Storage. The analytics team needs consolidated, cleaned data in BigQuery for dashboards.

Pipeline (visual, no-code steps):

1. Source: Ingest orders from MySQL.
2. Enrichment: Look up product metadata from PostgreSQL and join with orders.
3. Optional: Process clickstream events (batch or streaming) and map sessions to orders.
4. Transform: Clean, deduplicate, and compute derived metrics (e.g., order value, product category).
5. Sink: Write the consolidated dataset to BigQuery for reporting and ML.

Outcome: Business teams receive near-real-time dashboards for product performance, revenue trends, and fraud detection without maintaining bespoke ETL scripts.

Developer experience

* Visual GUI to assemble source → transform → sink stages with drag-and-drop.
* Validate and test pipelines in the UI; inspect sample records during design.
* Access runtime metrics, cluster logs, and lineage for troubleshooting.
* Integration with Dataproc for autoscaled compute: you get cluster scaling without manual cluster lifecycle management.

Exam tip

* If asked which GCP service provides visual, code-free data pipelines for ETL and integration, the correct answer is Cloud Data Fusion.
* Don’t confuse Cloud Composer with Cloud Data Fusion: Composer (based on Apache Airflow) is a workflow orchestration and scheduling service — it is not a visual ETL studio.

> **lightbulb** Cloud Data Fusion is the visual, code-free tool for building and running data integration pipelines. Cloud Composer is an orchestration service (based on [Apache Airflow](https://airflow.apache.org/)) for scheduling and managing workflows, and is not a visual ETL studio.

Next topic to consider

* What happens behind the scenes in Data Fusion to scale pipelines automatically? In the next lesson we’ll dive into autoscaling mechanics, how Dataproc clusters are orchestrated, and best practices for tuning performance and cost.

Links and references

* [Cloud Data Fusion](https://cloud.google.com/data-fusion) — official product page
* [CDAP (open source)](https://cdap.io/) — underlying platform for Data Fusion
* [Dataproc](https://cloud.google.com/dataproc) — managed Spark/Hadoop service used for scaling
* [BigQuery](https://cloud.google.com/bigquery) — common analytics sink for Data Fusion pipelines
* [Cloud Composer](https://cloud.google.com/composer) — workflow orchestration (Apache Airflow)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/36c7f00a-93ef-43ff-8baa-7d73914196ca/lesson/ff779828-374f-486d-bf62-e546caf662d1)
