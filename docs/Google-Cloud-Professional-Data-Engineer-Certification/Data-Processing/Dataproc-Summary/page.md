# Create
gcloud dataproc clusters create ephemeral-cluster --region=us-central1 --single-node

# Submit job
gcloud dataproc jobs submit pyspark --cluster=ephemeral-cluster --region=us-central1 job.py

# Delete
gcloud dataproc clusters delete ephemeral-cluster --region=us-central1 --quiet
```

Best practices for cost efficiency

* Use ephemeral clusters for ad-hoc or short batch jobs.
* Choose preemptible (Spot) worker VMs for non-critical tasks to save up to 80% on compute costs.
* Combine autoscaling with job-driven cluster policies to right-size resources.

<Frame>
  <img alt="A presentation slide titled &#x22;Managed Hadoop and Spark Cluster Service&#x22; showing four feature boxes: Fast Provisioning, Open Source, Integrated, and Cost Effective. Each box has brief bullets like &#x22;Clusters in 90 seconds,&#x22; &#x22;Hadoop, Spark, Hive,&#x22; &#x22;GCP services,&#x22; and &#x22;Per-second billing.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  Tip: For short batch jobs, consider creating ephemeral clusters (spin up, run the job, then delete the cluster) and using preemptible/Spot worker nodes to reduce cost. Dataproc’s per-second billing further minimizes charges for brief workloads.
</Callout>

Summary
Dataproc brings the familiar power of Hadoop and Spark to Google Cloud with minimal operational overhead. It’s designed for teams that want:

* fast provisioning,
* open-source compatibility,
* deep GCP integration,
* and cost-efficient execution of batch and interactive analytics workloads.

Autoscaling and advanced cluster customization (init actions, custom images, and cluster policies) are covered in follow-up articles to show how Dataproc adjusts cluster size and configuration to save time and money.

Links and references

* [Google Cloud Dataproc documentation](https://cloud.google.com/dataproc)
* [Cloud Storage](https://cloud.google.com/storage)
* [BigQuery](https://cloud.google.com/bigquery)
* [Google Cloud Logging](https://cloud.google.com/logging)
* [AWS EMR (for comparison)](https://aws.amazon.com/emr/)

That's it for this article.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/e3ae69a4-d6af-49da-853f-3cbe9d1b5570" />
</CardGroup>


# Dataproc Summary

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Dataproc-Summary/page

Overview of Google Cloud Dataproc, a managed Apache Spark and Hadoop service, covering features, storage options, cost and scaling strategies, use cases, and integration with GCP.

Hello — welcome back. This lesson wraps up everything covered about Dataproc. It refreshes the key concepts, explains why Dataproc is useful, and shows where it fits into real-world Google Cloud architectures. If you plan to run Apache Spark or Hadoop workloads on Google Cloud, this summary highlights the important pieces and is useful for exam preparation.

## What is Dataproc?

Dataproc is Google Cloud’s fully managed Apache Spark and Hadoop service. It automates cluster creation, scaling, and lifecycle management so you don’t need to provision or maintain VMs manually. Dataproc clusters start quickly, scale to match workloads, and integrate tightly with other Google Cloud services. Dataproc is optimized for speed, simplicity, and cost-efficiency — you pay only for what you use.

Key SEO terms: Google Cloud Dataproc, managed Spark, managed Hadoop, Dataproc clusters, Spark on GCP.

## Core features that make Dataproc convenient

* Fast deployment: Typical cluster spin-up is on the order of a minute or two (commonly \~90 seconds), enabling fast iteration for development and testing.
* Auto-scaling: Built-in autoscaling policies and cluster resizing let you add or remove worker nodes automatically, lowering idle costs.
* Google Cloud integration: Native integrations with Cloud Storage, BigQuery, Pub/Sub, Cloud Monitoring (Stackdriver), and IAM make Dataproc a first-class component of GCP data platforms.
* Cost controls: Support for preemptible VMs and ephemeral (short-lived) clusters helps reduce costs for batch and transient workloads.
* Customization: Initialization actions, component gateways (web UIs), custom images, and image versioning let you control software stacks and bootstrap behavior.

| Feature                                | Benefit                           | When to use                                      |
| -------------------------------------- | --------------------------------- | ------------------------------------------------ |
| Fast cluster creation                  | Rapid development and testing     | Short-lived jobs, iterative development          |
| Autoscaling                            | Reduced idle costs                | Variable or bursty workloads                     |
| GCP integrations                       | Seamless data movement & security | Pipelines integrating Storage, BigQuery, Pub/Sub |
| Preemptible VMs                        | Lower compute costs               | Fault-tolerant batch jobs                        |
| Initialization actions & custom images | Consistent environment            | Complex dependency or library requirements       |

<Callout icon="lightbulb">
  Dataproc supports initialization actions, component gateways (for web UIs), custom images, and image-versioning so you can control software stacks and bootstrap behavior at cluster creation.
</Callout>

## Storage options in Dataproc

Choose storage based on durability, cost, and performance. Below is a concise comparison and guidance.

| Storage option               | Characteristics                                                                 | Best use cases                                                            |
| ---------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `Google Cloud Storage (GCS)` | Object storage, highly durable, decoupled from cluster lifecycle                | Primary choice for input/output, long-term storage, and shared datasets   |
| `HDFS (on-cluster)`          | Local HDFS on cluster VMs, low-latency disk access but tied to cluster lifetime | Temporary fast scratch space during jobs requiring local disk speed       |
| `Local SSDs`                 | Highest I/O performance, ephemeral                                              | Caching, I/O-intensive operations where speed matters                     |
| `Persistent Disk (PD)`       | Durable block storage that survives VM restarts                                 | When you require persistent block volumes or specific block-level configs |

Optimization levers:

* Use preemptible VMs where jobs tolerate interruptions to lower costs.
* Right-size node types (CPU, memory, and disk) to match workload characteristics.
* Leverage autoscaling and ephemeral clusters for variable workloads.
* Optimize storage layout (partitioning, file formats like Parquet/ORC, and file sizes) for better I/O and query performance.

<Frame>
  <img alt="An infographic titled &#x22;Dataproc in GCP&#x22; summarizing core features, storage options, and optimization techniques for running Apache Spark/Hadoop on Google Cloud. Color-coded boxes highlight points like fast deployment, auto-scaling, preemptible VMs, right sizing, cluster management, and storage optimization." />
</Frame>

<Callout icon="warning">
  [Preemptible VMs](https://cloud.google.com/compute/docs/instances/preemptible) are much cheaper but can be reclaimed at any time. Use them for fault-tolerant batch jobs, and ensure your job or workflow can handle worker interruptions.
</Callout>

## Typical use cases

* Running Spark jobs: Managed Spark clusters for Spark SQL, DataFrame jobs, MLlib, and Spark Streaming.
* Apache Flink and other engines: Dataproc can run Flink and other frameworks though Dataproc’s core strength is Spark.
* Interactive SQL / Presto: Run Presto on Dataproc to query data in GCS; for many ad-hoc analytics and warehousing scenarios, BigQuery is often a simpler, fully managed alternative with higher performance on large datasets.
* ETL, batch processing, and machine learning pipelines: When you need the Hadoop/Spark ecosystem integrated with GCP services and want tight control over cluster topology for performance or cost.

When to choose Dataproc vs BigQuery:

* Choose Dataproc when you need full control over Spark/Hadoop libraries, custom runtime dependencies, or complex distributed processing logic.
* Choose BigQuery for serverless, high-performance analytics, ad-hoc SQL querying, and workloads where you don’t need direct control over the execution environment.

## Closing

This concise summary covered what Dataproc is, its core features, supported storage options, optimization strategies, and common use cases. Dataproc is best when you need managed Spark/Hadoop infrastructure with flexible lifecycle control and close integration with Google Cloud services.

See you in the next lesson.

## Links and references

* [Dataproc documentation](https://cloud.google.com/dataproc)
* [Apache Spark](https://spark.apache.org/)
* [Apache Hadoop](https://hadoop.apache.org/)
* [Google Cloud Storage (GCS)](https://cloud.google.com/storage)
* [BigQuery](https://cloud.google.com/bigquery)
* [Preemptible VMs](https://cloud.google.com/compute/docs/instances/preemptible)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/6f5c2733-e2c0-411b-9893-49fc5132267a" />
</CardGroup>
