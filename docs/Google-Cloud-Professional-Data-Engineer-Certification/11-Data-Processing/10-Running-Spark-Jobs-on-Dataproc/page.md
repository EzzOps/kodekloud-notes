# Running Spark Jobs on Dataproc

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Running-Spark-Jobs-on-Dataproc/page

Guide to running Spark jobs on Google Cloud Dataproc covering preparation, submission, monitoring, storage, and cluster lifecycle for scalable ETL and analytics

Welcome back. In this lesson you'll learn the end-to-end lifecycle for running Spark jobs on Google Cloud Dataproc—covering code preparation, submission, execution, monitoring, and result storage. This workflow is ideal for scaling ETL or analytics jobs that would be slow on a local machine.

Dataproc provides a managed Spark environment with autoscaling and integrations with other Google Cloud services (Cloud Storage, BigQuery, Pub/Sub, Cloud Build), making it a natural choice for large-scale data processing.

## Typical lifecycle for a Dataproc Spark job

1. Data sources
   * Identify where your input data lives: BigQuery, Cloud Storage (GCS), Pub/Sub, or a local dataset you upload. These are prerequisites for any Spark job.

2. Prepare and upload code and dependencies
   * Develop locally (Python, Scala, Java). For Python, package your code as a directory, ZIP, or wheel; for JVM languages, produce a JAR.
   * Upload artifacts and any dependencies to a GCS bucket so Dataproc can access them. For ad-hoc runs you can also submit directly from your workstation using `gcloud` or `spark-submit`.

3. Submit the job to Dataproc
   * Submit to an existing long-lived cluster or create a short-lived cluster specifically for the job. Use `gcloud dataproc jobs submit` or the Dataproc API.

4. Execution and monitoring
   * Dataproc runs the Spark job. Monitor progress using the Spark UI, Spark History Server, Cloud Monitoring, or the Dataproc Jobs page in the Cloud Console.

5. Output and storage
   * Write results to the desired sink: GCS, BigQuery, Pub/Sub, or an external system. Typical patterns: write processed files to GCS or load results into BigQuery for analytics.

6. Cluster lifecycle and cleanup
   * For scheduled or infrequent batch jobs, spin up short-lived clusters and delete them when finished to minimize cost. For low-latency or interactive workloads, use a long-lived cluster with autoscaling that scales down when idle.

<Frame>
  <img alt="A schematic workflow for running Spark jobs on Google Cloud, showing data sources (BigQuery, local) used to create a Spark job (JAR/py/zip) that’s uploaded to a GCS bucket and submitted to a Dataproc cluster. The diagram then shows execution, monitoring, saving results to GCS/BigQuery, and optional cluster cleanup." />
</Frame>

## Concrete example workflow (CI/CD + scheduled batch)

A common production setup:

* Data lands in GCS (data lake).
* Code is developed locally and stored in GitHub.
* Cloud Build creates artifacts (ZIP/JAR) and uploads them to a GCS bucket.
* A scheduled trigger spins up a short-lived Dataproc cluster, runs the Spark job to process the previous day's data, writes results to BigQuery, and deletes the cluster when finished.

### Example commands

Create a short-lived cluster:

```bash theme={null}
gcloud dataproc clusters create my-dataproc-cluster \
  --region=us-central1 \
  --single-node \
  --image-version=2.1-debian10 \
  --optional-components=ANACONDA,JUPYTER \
  --properties=spark:spark.executor.memory=4g
```

Submit a Python Spark job (packaged as a ZIP) that uses additional Python files:

```bash theme={null}
gcloud dataproc jobs submit pyspark gs://my-bucket/artifacts/my_job.py \
  --cluster=my-dataproc-cluster \
  --region=us-central1 \
  --py-files=gs://my-bucket/artifacts/libs.zip \
  -- gs://my-bucket/input/2026-05-28/ gs://my-bucket/output/2026-05-28/
```

Submit a JVM job (JAR) with a main class:

```bash theme={null}
gcloud dataproc jobs submit spark \
  --cluster=my-dataproc-cluster \
  --jar=gs://my-bucket/artifacts/my-spark-job.jar \
  --class=com.example.Main \
  --region=us-central1 \
  -- arg1 arg2
```

Delete the short-lived cluster when the job completes:

```bash theme={null}
gcloud dataproc clusters delete my-dataproc-cluster --region=us-central1 --quiet
```

## When to use short-lived vs long-lived clusters

| Use case                              | Best option                     | Reason / example                                                             |
| ------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------- |
| Infrequent batch jobs (daily, hourly) | Short-lived cluster             | Reduces cost by deleting the cluster after the job completes                 |
| Low-latency or interactive workloads  | Long-lived, autoscaling cluster | Avoids startup overhead and supports quick responses for interactive queries |
| CI/CD or automated pipelines          | Short-lived cluster per run     | Ensures reproducible, isolated runs with clean environments                  |
| Streaming or always-on processing     | Long-lived cluster              | Required for continuous processing and stateful streaming jobs               |

> **lightbulb** Choose a short-lived cluster for intermittent batch jobs to minimize cost. Choose a long-lived, autoscaling cluster for low-latency or interactive workloads where startup time and job latency are important.

## Monitoring, logging, and debugging

* Spark UI: track stages, tasks, and executors during the job run.
* Spark History Server: inspect completed application logs and metrics.
* Cloud Logging & Monitoring: collect logs, set alerts, and visualize performance trends.
* Dataproc Jobs page (Cloud Console): view job status and details.
* For long-running clusters, enable component gateways (e.g., Spark History Server) for easier access.

References:

* [Dataproc documentation](https://cloud.google.com/dataproc/docs)
* [Spark on Dataproc best practices](https://cloud.google.com/dataproc/docs/guides/spark-best-practices)
* [Cloud Build documentation](https://cloud.google.com/build/docs)
* [BigQuery documentation](https://cloud.google.com/bigquery/docs)

## Interview / exam tip

When asked to justify a short-lived vs long-lived Dataproc cluster, structure your answer around:

* Job frequency (one-time vs recurring)
* Latency requirements (interactive vs batch)
* Cost constraints (pay-per-use vs idle resources)
* Operational overhead (automation of cluster lifecycle)
* Data locality and startup time

That’s the complete lifecycle overview for running Spark jobs on Dataproc—covering preparation, submission, monitoring, storage, and cluster lifecycle management. Thank you.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/f34d006a-44d6-404a-aea8-7ae02facb248)
