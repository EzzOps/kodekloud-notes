# Dataproc Introduction

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Dataproc-Introduction/page

Overview of Google Cloud Dataproc, a managed Hadoop and Spark service for running open source big data workloads with fast provisioning, autoscaling, and tight GCP integration.

Welcome back. In this article we explore Dataproc: Google Cloud’s managed Hadoop and Spark cluster service for running large-scale batch and interactive data processing jobs. After covering streaming with Dataflow, Dataproc is the natural choice when you need to run established big data frameworks (Hadoop, Spark, Hive, etc.) in the cloud with minimal ops overhead.

If you’re familiar with AWS, Dataproc is analogous to [EMR](https://aws.amazon.com/emr/). Teams migrating on-premises Hadoop or Spark workloads to Google Cloud often pick Dataproc because it preserves compatibility with existing jobs and tooling while adding the benefits of native GCP integration.

Dataproc processes large datasets stored in Cloud Storage (commonly used as a data lake), and it can access BigQuery and HDFS for hybrid or migrated workloads. Google manages cluster lifecycle, software versions, and orchestration so you can focus on jobs and analysis rather than infrastructure.

Common frameworks available on Dataproc:

* Hadoop (MapReduce)
* Spark (batch and fast analytics)
* Hive (SQL-on-Hadoop)
* Pig
* Presto / Trino (interactive SQL queries)
* Flink (streaming)
* Optional tools: Iceberg, Trino, and other ecosystem components you can enable on a cluster

<Frame>
  <img alt="A diagram titled &#x22;Managed Hadoop and Spark Cluster Service&#x22; showing a DataProc cluster with components like Hadoop (MapReduce), Spark (Fast Analytics), Hive (SQL), Pig, Presto and Flink. It shows inputs from Data Lakes and BigQuery/HDFS on the left and outputs to Analytics and ML Models on the right." />
</Frame>

Real-world example:
Your team receives a terabyte of log files and needs rapid insights. With Dataproc you can:

1. Spin up a Spark cluster in minutes.
2. Run Spark jobs against Cloud Storage input.
3. Persist results to Cloud Storage or load them into BigQuery for dashboards.
4. Feed processed data into ML model training.

Because Dataproc supports standard open-source tools, migrating existing Spark jobs is usually straightforward and requires minimal code changes.

Why organizations choose Dataproc

* Fast provisioning — clusters can be created in roughly 90 seconds, enabling rapid iteration.
* Autoscaling — clusters can grow or shrink to match demand (covered in a later article).
* Open-source compatibility — reuse your existing Hadoop/Spark/Hive tooling and libraries.
* Tight GCP integration — native access to Cloud Storage, BigQuery, Cloud Logging, Cloud Monitoring, IAM, and more.
* Cost efficiency — per-second billing, support for preemptible (Spot) worker VMs, and ephemeral clusters for short-lived jobs.

Frameworks and their typical use cases:

| Framework          | Typical use case                            |
| ------------------ | ------------------------------------------- |
| Hadoop (MapReduce) | Large-scale, batch-oriented ETL             |
| Spark              | Fast batch analytics, machine learning, ETL |
| Hive               | SQL queries over large datasets             |
| Presto / Trino     | Interactive SQL across data lakes           |
| Flink              | Streaming analytics and event processing    |

Quick CLI examples

* Create a basic Dataproc cluster:

```bash theme={null}
gcloud dataproc clusters create my-cluster \
  --region=us-central1 \
  --single-node \
  --image-version=2.1-debian10
```

* Submit a Spark job:

```bash theme={null}
gcloud dataproc jobs submit spark \
  --cluster=my-cluster \
  --region=us-central1 \
  --class=org.apache.spark.examples.SparkPi \
  --jars=file:///usr/lib/spark/examples/jars/spark-examples.jar \
  -- 1000
```

* Create an ephemeral cluster, run a job, then delete it (example workflow):

```bash theme={null}
