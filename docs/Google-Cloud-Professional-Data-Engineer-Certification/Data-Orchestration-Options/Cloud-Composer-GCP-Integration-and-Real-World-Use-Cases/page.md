# Cloud Composer GCP Integration and Real World Use Cases

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Orchestration-Options/Cloud-Composer-GCP-Integration-and-Real-World-Use-Cases/page

Overview of using Cloud Composer to orchestrate Google Cloud services like Cloud Functions, Pub/Sub, GCS, BigQuery, Dataflow and Dataproc for production data pipelines

Hello and welcome back.

This lesson builds on production best practices such as scalability, scheduling, and error handling. Here we map those operational concepts to concrete integrations: how Cloud Composer (managed Apache Airflow on GCP) becomes more powerful when it orchestrates different Google Cloud services together.

<Callout icon="lightbulb">
  Cloud Composer is Google Cloud's managed Apache Airflow service. It uses Airflow DAGs to orchestrate tasks and interacts with GCP through a set of Airflow operators, sensors, and hooks provided by the Airflow GCP provider package.
</Callout>

Below are common service integrations you will encounter in data engineering projects, with concise explanations of how Composer typically interacts with each and short examples showing typical patterns.

## Quick summary table

| GCP Service         | Typical Airflow operators / sensors                                                                            | Typical use case                                                                                         |
| ------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Cloud Functions     | Use from DAG via operators or invoke via client libraries (e.g., `PythonOperator` calling Cloud Functions API) | Run lightweight, on-demand compute for event-based tasks (e.g., validate a landed file, update metadata) |
| Pub/Sub             | Use publish operators or trigger DAGs via sensors / external triggers                                          | Event-driven pipelines and decoupling producers and consumers                                            |
| Cloud Storage (GCS) | `GCSHook`, `GCSListObjectsOperator`, `GCSToGCSOperator`, `GCSToBigQueryOperator`                               | Staging raw data, intermediate artifacts, and outputs                                                    |
| BigQuery            | `BigQueryInsertJobOperator`, `BigQueryExecuteQueryOperator`                                                    | Analytical storage and query engine for batch/interactive analytics                                      |
| Dataflow            | `DataflowCreatePythonJobOperator`, `DataflowCreateJavaJobOperator`                                             | Scalable streaming or batch ETL/ELT pipelines                                                            |
| Dataproc            | `DataprocCreateClusterOperator`, `DataprocSubmitJobOperator`                                                   | Run Spark/Hadoop jobs with on-demand clusters to save costs                                              |

## Integration patterns and examples

* Cloud Functions
  * Use case: Run a small, single-purpose function when an event occurs (e.g., validate or enrich a file after it lands in Cloud Storage).
  * How Composer invokes it: From a DAG task either by using a dedicated Cloud Functions operator or by calling the Cloud Functions REST API / client library from a `PythonOperator`.
  * Why use it: Keeps light business logic out of DAG definitions and provides fast, event-driven execution.
  * Example (invoke via Python client inside a `PythonOperator`):
    ```python theme={null}
    def call_cloud_function(**kwargs):
        from google.cloud import functions_v1
        client = functions_v1.CloudFunctionsServiceClient()
        name = "projects/<PROJECT>/locations/<REGION>/functions/<FUNCTION>"
        response = client.call_function(name=name, data='{"file":"gs://bucket/path"}')
        return response

    call_fn_task = PythonOperator(
        task_id="call_fn",
        python_callable=call_cloud_function,
    )
    ```

* Pub/Sub
  * Use case: Decouple producers and consumers; use messages to trigger downstream processing.
  * How Composer interacts: Publish messages from a DAG (or use a sensor / Cloud Function to trigger DAGs on message arrival).
  * Why use it: Enables scalable, loosely coupled architectures and event-driven orchestration.
  * Example (publish using client library inside a `PythonOperator`):
    ```python theme={null}
    def publish_message(**kwargs):
        from google.cloud import pubsub_v1
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path("my-project", "my-topic")
        publisher.publish(topic_path, b'{"file":"gs://bucket/path"}')

    publish_task = PythonOperator(
        task_id="publish_msg",
        python_callable=publish_message,
    )
    ```

* Cloud Storage
  * Use case: Landing zone for raw files, intermediate artifacts, and final outputs.
  * How Composer interacts: Use GCS operators/hooks to transfer files, list objects, or stream content to downstream tasks (Dataflow, BigQuery).
  * Why use it: Durable, highly available storage integrated across GCP.
  * Example (list objects using GCS hook):
    ```python theme={null}
    from airflow.providers.google.cloud.hooks.gcs import GCSHook

    def list_gcs(**kwargs):
        hook = GCSHook(gcp_conn_id='google_cloud_default')
        return hook.list(bucket_name='my-bucket', prefix='incoming/')
    ```

* BigQuery
  * Use case: Analytical warehouse for queries, table refreshes, and materialized results.
  * How Composer interacts: Submit jobs with `BigQueryInsertJobOperator` or `BigQueryExecuteQueryOperator`, monitor completion and branch downstream tasks.
  * Why use it: Fast, serverless analytics that pairs naturally with Composer orchestration.
  * Example (submit a query job):
    ```python theme={null}
    bq_query = BigQueryInsertJobOperator(
        task_id="bq_query",
        configuration={
            "query": {
                "query": "SELECT COUNT(*) FROM `project.dataset.table`",
                "useLegacySql": False,
            }
        }
    )
    ```

* Dataflow
  * Use case: Scalable streaming or batch ETL (e.g., log ingestion, enrichment, ML feature processing).
  * How Composer interacts: Launch, monitor, and retry Dataflow jobs using the Dataflow operators; Composer handles orchestration and job lifecycle.
  * Why use it: Offload heavy processing to a managed, autoscaling system while Composer coordinates when jobs start and complete.
  * Example (submit a Python Dataflow job — conceptual):
    ```python theme={null}
    dataflow_task = DataflowCreatePythonJobOperator(
        task_id="run_dataflow",
        py_file="gs://my-bucket/jobs/my_pipeline.py",
        options={"project": "my-project", "region": "us-central1", "tempLocation": "gs://my-bucket/tmp"}
    )
    ```

* Dataproc
  * Use case: Run Spark, Hive, or Hadoop jobs that need JVM-based engines.
  * How Composer interacts: Create ephemeral clusters and submit jobs using Dataproc operators to minimize costs.
  * Why use it: Best for existing Spark/Hadoop workloads where Composer schedules and monitors jobs.
  * Example (submit a job to Dataproc):
    ```python theme={null}
    dataproc_task = DataprocSubmitJobOperator(
        task_id="submit_spark",
        job={
            "reference": {"project_id": "my-project"},
            "placement": {"cluster_name": "my-cluster"},
            "spark_job": {"main_python_file_uri": "gs://my-bucket/spark_job.py"},
        },
    )
    ```

## Practical orchestration considerations

* Use the appropriate GCP Airflow operators and sensors so your DAGs stay declarative and maintainable.
* Favor idempotent tasks and explicit retry policies to handle transient service failures (timeouts, quota errors).
* Correlate Airflow task logs with service-level logs and metrics (Cloud Logging, Cloud Monitoring) to troubleshoot cross-system failures faster.
* Keep cost in mind: prefer ephemeral Dataproc clusters or on-demand Dataflow jobs and set TTLs where applicable.
* Design tasks to be small, testable, and observable: simple tasks are easier to retry and to reason about in distributed systems.

## Choosing between Cloud Composer and Cloud Workflows

Cloud Composer (Airflow) and Cloud Workflows solve different orchestration problems:

* Cloud Composer
  * Best for complex, long-running DAGs, data pipelines, and dependencies between heterogeneous tasks (Python code, SQL jobs, long-running jobs).
  * Benefits from the Airflow ecosystem of operators, sensors, and scheduling features.

* Cloud Workflows
  * Best for short, operational orchestration and API-driven workflows (service orchestration, retries with backoff, lightweight sequences).
  * Lightweight, ideal for calling REST APIs and composing short-lived service interactions.

Selecting the right tool depends on pipeline complexity, developer expertise, and integrations required. For large data engineering workflows involving batch processing, scheduled tasks, and complex branching, Composer is typically the preferred choice. For quick API orchestration and short workflows, Cloud Workflows can be simpler and cheaper.

## Links and references

* [Cloud Composer documentation](https://cloud.google.com/composer/docs)
* [Apache Airflow GCP provider (operators & hooks)](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html)
* [BigQuery documentation](https://cloud.google.com/bigquery/docs)
* [Dataflow documentation](https://cloud.google.com/dataflow/docs)
* [Dataproc documentation](https://cloud.google.com/dataproc/docs)
* [Cloud Functions documentation](https://cloud.google.com/functions/docs)
* [Pub/Sub documentation](https://cloud.google.com/pubsub/docs)
* [Cloud Storage documentation](https://cloud.google.com/storage/docs)

This short overview shows how Composer acts as the central conductor—connecting serverless functions, messaging systems, durable storage, analytics engines, and scalable processing frameworks into reliable, production-ready data workflows.

This concludes the lesson. Speak with you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/ff8693f0-36fe-4cca-9b05-f27ffa81ccb4/lesson/047fb69a-605c-4095-ac06-827b722daf50" />
</CardGroup>
