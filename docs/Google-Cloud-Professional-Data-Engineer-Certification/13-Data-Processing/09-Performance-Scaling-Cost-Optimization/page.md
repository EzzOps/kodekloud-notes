# Read CSV with header and schema inference
df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_path)

# Aggregate: total spend per customer
result_df = df.groupBy("customer_id").agg(_sum("amount").alias("total_spend"))

# Write result to GCS (CSV, overwrite mode)
result_df.write.mode("overwrite").csv(output_path)

print("Job completed successfully.")
spark.stop()
```

Notes:

* The script expects two arguments: the input GCS path (CSV) and the output GCS folder path where Spark will write part files.
* It uses `SparkSession` to read the CSV, group by `customer_id`, sum `amount`, and write CSV output.

## Upload files to Cloud Storage

Upload both `orders.csv` and `process_orders.py` to your bucket. If you uploaded the wrong file name, delete and re-upload the corrected files.

<Frame>
  <img alt="A screenshot of the Google Cloud Console Storage &#x22;Buckets&#x22; page showing several &#x22;dataproc&#x22; buckets with a filter dropdown open. Columns for location, default storage class, last modified date, and public access are visible." />
</Frame>

Helpful file layout (example)

| File           | Example GCS path                     | Purpose                                        |
| -------------- | ------------------------------------ | ---------------------------------------------- |
| Input data     | `gs://your-bucket/orders.csv`        | Raw CSV input for the Spark job                |
| PySpark script | `gs://your-bucket/process_orders.py` | Main job entrypoint                            |
| Job output     | `gs://your-bucket/output/`           | Spark writes `part-*` CSV files and `_SUCCESS` |

## Create a Dataproc cluster

Open Dataproc in the GCP Console (search for “Dataproc”), go to Clusters, and click Create cluster. For this demo you can choose:

* Standard cluster (1 master + workers) for distributed workloads.
* Single-node cluster (master-only) to save cost for small tests.

Select additional components (Hive, Jupyter, etc.) if needed and click Create. Cluster provisioning usually takes a few minutes.

<Frame>
  <img alt="A Google Cloud Console screenshot of the Dataproc &#x22;Create a Dataproc cluster on Compute Engine&#x22; setup page with the &#x22;Set up cluster&#x22; step selected. The Components pane shows &#x22;Enable component gateway&#x22; checked and a list of optional components (Jupyter, Zeppelin, Trino, etc.), with a blue &#x22;Create&#x22; button on the left." />
</Frame>

Monitor cluster creation; when the cluster status becomes Running, open the cluster details.

<Frame>
  <img alt="A screenshot of the Google Cloud Console Dataproc &#x22;Clusters&#x22; page. It shows one demo-cluster listed as Running in us-central1 with an error banner saying &#x22;Sorry, the server was not able to fulfill your request.&#x22;" />
</Frame>

## Submit the PySpark job from the Console

From the Dataproc cluster details page, click Submit job. Set the job type to PySpark, provide a job name (for example `example-spark-job`), and set the main Python file path to your uploaded script (for example `gs://your-bucket/process_orders.py`). Provide the two required arguments, each on its own line:

Example arguments (each on a separate line):

```text theme={null}
gs://your-bucket/orders.csv
gs://your-bucket/output/
```

Then submit the job. The job will appear in the Jobs list; click it to view logs and status.

<Frame>
  <img alt="A screenshot of the Google Cloud Console showing Dataproc cluster details on the left and a &#x22;Submit a job&#x22; form on the right prefilled for a PySpark job (job ID and main Python file path visible). The cluster is named &#x22;demo-cluster&#x22; and the form includes fields for additional Python files, JARs, and other job options." />
</Frame>

While the job runs you can stream logs from the job details page to troubleshoot issues.

<Frame>
  <img alt="A screenshot of the Google Cloud Console showing a Dataproc job details page for &#x22;example-spark-job&#x22; with status &#x22;Running,&#x22; an &#x22;Insights by Gemini&#x22; panel, and an Output area at the bottom." />
</Frame>

## Inspect the job via Spark History Server and Console

From the cluster details, open Web Interfaces and launch the Spark History Server to inspect completed applications, stages, and executors. If the job has not finished you may initially see “No completed applications found.” After completion the History Server lists the application and stages for deeper debugging and performance analysis.

<Frame>
  <img alt="A screenshot of the Google Cloud Console showing Dataproc cluster details for a cluster named &#x22;demo-cluster&#x22; with status &#x22;Running.&#x22; The Web Interfaces tab is open, listing SSH tunnel info and component gateway links like YARN ResourceManager, Spark History Server, and HDFS NameNode." />
</Frame>

<Frame>
  <img alt="A screenshot of an Apache Spark History Server web page showing the event log directory, last updated timestamp and client time zone. The page displays a prominent &#x22;No completed applications found!&#x22; message." />
</Frame>

When the job completes successfully the Console shows a green Succeeded status. You can inspect logs to confirm processing details and check the output folder for result files.

<Frame>
  <img alt="A Google Cloud Console Dataproc job details page showing a Spark job named &#x22;example-spark-job&#x22; with its Job UUID and a green &#x22;Succeeded&#x22; status. The Summary tab displays an &#x22;Insights by Gemini&#x22; preview and an Output panel with a note that Spark jobs take ~60 seconds to initialize." />
</Frame>

## Note: alternatives to console submission

<Callout icon="lightbulb">
  You can also submit Dataproc jobs using the `gcloud` CLI, Dataproc REST or client libraries (Python, Java), or orchestrate them via Airflow operators for production workflows. See the Dataproc docs for examples and best practices: [https://cloud.google.com/dataproc/docs/reference](https://cloud.google.com/dataproc/docs/reference)
</Callout>

Cost and cleanup warning

<Callout icon="warning">
  Dataproc clusters incur compute and networking costs while running. For demos, delete or stop clusters when not in use to avoid unexpected charges. Consider using single-node clusters or autoscaling for cost savings.
</Callout>

## Verify the output in Cloud Storage

After the job succeeds, refresh your Cloud Storage bucket. The output folder contains Spark’s CSV part files (for example `part-00000-*.csv`) and a `_SUCCESS` file indicating completed write.

<Frame>
  <img alt="A Google Cloud Console screenshot showing the details of a Storage bucket named &#x22;dataproc-demo-kodekloud-gcp-training&#x22; with location us-central1 and Standard storage class. The objects list shows files like orders.csv, an output/ folder, and process_orders.py." />
</Frame>

## Typical production pipeline considerations

In production you’ll commonly separate storage layers (raw, processed, analytics). A typical flow:

* Raw data ingested into a raw-data bucket.
* ETL/processing Spark jobs write to a processed bucket.
* Final aggregated results loaded into BigQuery or an analytics store for reporting.

Common production patterns include:

| Area           | Recommendation                                                            |
| -------------- | ------------------------------------------------------------------------- |
| Orchestration  | Use Airflow or Cloud Composer to schedule and retry jobs                  |
| Monitoring     | Send Dataproc/Cloud Logging logs to a central monitoring/alerting system  |
| Storage layout | Use separate buckets or prefixes for raw, processed, and analytics layers |
| Permissions    | Use least-privilege IAM roles for job/service accounts                    |

Links and references

* Dataproc: [https://cloud.google.com/dataproc](https://cloud.google.com/dataproc)
* Cloud Storage: [https://cloud.google.com/storage](https://cloud.google.com/storage)
* Apache Spark: [https://spark.apache.org/](https://spark.apache.org/)
* Spark History Server: [https://spark.apache.org/docs/latest/monitoring.html#spark-history-server](https://spark.apache.org/docs/latest/monitoring.html#spark-history-server)
* BigQuery: [https://cloud.google.com/bigquery](https://cloud.google.com/bigquery)

## Closing

This walkthrough showed how to create a bucket, prepare data and a PySpark job, spin up a Dataproc cluster, submit a job from the Console, inspect it, and verify results in Cloud Storage. Thanks for following along — try extending the script to write Parquet output or to load results into BigQuery for analytics.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/5beb9b6a-81ea-49c6-92fd-30603cbb543c" />
</CardGroup>


# Performance Scaling Cost Optimization

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Processing/Performance-Scaling-Cost-Optimization/page

Guidance for improving Google Cloud Dataflow pipeline performance, autoscaling, shuffle strategies, handling data skew, Streaming Engine benefits, and cost optimization best practices.

Welcome back. This lesson covers practical guidance for improving performance, autoscaling behavior, and cost efficiency of Google Cloud Dataflow pipelines. Over months or years of production use, these are frequent operational concerns—this guide highlights key concepts, trade-offs, and mitigation techniques to keep pipelines healthy and affordable.

Topics covered:

* Autoscaling behavior: streaming vs batch
* Shuffle service trade-offs
* Detecting and mitigating data skew / hot keys
* Streaming Engine: separation of compute and service-managed state
* Cost optimization and periodic design reviews

Let’s get started.

## Autoscaling behavior: streaming vs batch

Streaming pipelines run continuously and typically autoscale gradually as load changes. Batch pipelines usually start many workers quickly, process the workload, then scale down when the job completes. These different behaviors imply distinct design and cost trade-offs:

* Streaming: steady, incremental autoscaling; optimized for sustained workload and low-latency processing.
* Batch: fast ramp-up and ramp-down; optimized for burst throughput and short-lived runs.

When choosing a pipeline model, consider the trigger cadence. For example, a job that must run every 2 seconds is usually better implemented as a streaming pipeline—attempting to run a batch job that frequently will cause rapid worker churn and unnecessary cost.

| Characteristic      |                         Streaming |                          Batch |
| ------------------- | --------------------------------: | -----------------------------: |
| Runtime             |                        Continuous |                    Short-lived |
| Autoscaling pattern |                   Gradual scaling |       Fast ramp-up / ramp-down |
| Best for            |        Low-latency, steady events |  High-throughput batch windows |
| Cost risk           | Overprovisioning if misconfigured | Worker churn for frequent runs |

<Frame>
  <img alt="A slide titled &#x22;Autoscaling Behavior&#x22; showing two charts: a &#x22;Streaming&#x22; graph with a green line that gradually increases workers over time (gradual scaling), and a &#x22;Batch&#x22; graph with a red line that rapidly ramps up to a plateau then drops off (fast ramp-up/down)." />
</Frame>

## Shuffle service: local disk vs external shuffle

By default, Dataflow can store intermediate shuffle data on worker VMs’ local disks. In this mode, if a worker fails, the stage may need to restart and reprocess lost intermediate data—costly in time and compute.

Enabling the Dataflow Shuffle Service stores intermediate data in a separate, resilient service so workers become effectively stateless for intermediate data. A replacement worker can continue from the external shuffle store without reprocessing the entire stage, improving fault tolerance and enabling faster, more reliable scaling.

However, the external shuffle service introduces overhead and may not be beneficial for very short-lived batch jobs (e.g., tasks that run for only a minute or two). Evaluate expected job duration, failure tolerance, and cost trade-offs before enabling it.

<Callout icon="warning">
  Use the external shuffle service for long-running or failure-sensitive jobs. For tiny, short-lived batch jobs, the external shuffle overhead can increase latency and cost.
</Callout>

<Frame>
  <img alt="An infographic titled &#x22;Shuffle Service&#x22; comparing two architectures: the left shows workers each containing shuffle data (&#x22;Without Shuffle Service&#x22; — limited sharing), and the right shows separate workers using a centralized &#x22;Shuffle Service (External Storage)&#x22; (&#x22;With Shuffle Service&#x22; — better scaling)." />
</Frame>

## Detecting and mitigating data skew / hot keys

Data skew (hot keys) happens when a small subset of keys receives a disproportionate share of the data. This creates bottlenecks: the worker handling the hot key becomes overloaded while others are idle, reducing parallelism and increasing latency.

Common mitigations:

* Key salting (sharding / key prefixing): split a hot key into multiple salted keys for partial aggregation, then remove the salt and perform a final aggregation.
* Reshuffle / multi-stage aggregation: perform partial combines (fanout) before a final CombinePerKey.
* Worker-side combining: reduce the amount of shuffle data by aggregating locally where possible.

Practical detection and steps:

* Monitor per-key throughput and latency using Dataflow job metrics and logs to identify skew.
* For identified hot keys, implement a two-stage combine pattern:

Example pattern (pseudocode):

Step 1 — Shard and partial combine:

```Java theme={null}
PCollection<KV<String, V>> input = ...;
PCollection<KV<String, V>> sharded =
  input.apply(MapElements.into(...).via(kv -> KV.of(salt(kv.getKey()), kv.getValue())));
PCollection<KV<String, Accum>> partial = sharded.apply(Combine.perKey(partialCombineFn));
```

Step 2 — Remove salt and final combine:

```Java theme={null}
PCollection<KV<String, Accum>> unsalted =
  partial.apply(MapElements.into(...).via(kv -> KV.of(unsalt(kv.getKey()), kv.getValue())));
PCollection<KV<String, Result>> finalResults =
  unsalted.apply(Combine.perKey(finalCombineFn));
```

* Choose the number of shards based on observed load for the hot key (e.g., K-0..K-N).
* Use fanout/combiner patterns to reduce intermediate shuffle volume.

These mitigations often yield large speedups when a few keys dominate the workload.

<Frame>
  <img alt="An infographic titled &#x22;Data Skew and Hot Keys&#x22; showing a problem diagram where one hot key (Key A) accounts for 90% of load and overloads one worker, and a solution diagram illustrating key salting (splitting Key A into A-1/A-2/A-3) to achieve balanced distribution and better parallelization." />
</Frame>

## Streaming Engine: separation of compute and service-managed state

Dataflow supports two runtime models:

* Legacy worker-centric streaming (worker holds state and coordination),
* Managed Streaming Engine (service-managed state and coordination).

The Streaming Engine moves pipeline state and coordination off worker VMs into a Google-managed service, decoupling compute from state storage. Key benefits:

* Faster autoscaling (workers can be added/removed more quickly),
* Lower worker memory footprint,
* Improved worker resource utilization,
* Better support for low-latency, short-interval streaming.

If your pipeline has short trigger gaps (e.g., events every 1–3 seconds) or strict autoscaling/latency needs, the Streaming Engine is usually recommended.

For more details, see the official documentation: [Dataflow Streaming Engine](https://cloud.google.com/dataflow/docs/guides/streaming-engine).

## Cost optimization and ongoing design review

Control costs by selecting appropriate machine types, autoscaling settings, and shuffle/engine configurations. Practical ideas:

* Right-size worker machine types for CPU and memory needs.
* Use preemptible workers for batch jobs where occasional interruptions are acceptable (significant cost savings).
* Tune autoscaling parameters and set reasonable minimum/maximum worker counts to balance latency and cost.
* Avoid enabling shuffle service for tiny, short-lived jobs where overhead outweighs reliability gains.
* Apply partial aggregation or fanout to reduce shuffle volume and network I/O.

Checklist for practical optimization:

| Area              | Action                                                                          |
| ----------------- | ------------------------------------------------------------------------------- |
| Machine selection | Right-size CPUs/memory; consider custom machine types                           |
| Autoscaling       | Set min/max workers; tune scaling policies                                      |
| Shuffle           | Enable external shuffle for long or failure-sensitive jobs; avoid for tiny jobs |
| Workers           | Consider preemptible workers for batch                                          |
| Data partitioning | Mitigate hot keys with salting / fanout                                         |
| Review cadence    | Re-evaluate pipelines periodically (see note)                                   |

<Callout icon="lightbulb">
  Do a design review at regular intervals (for example, yearly). Re-evaluating pipelines against newer managed services and features often yields both performance and cost benefits.
</Callout>

Operational practice: schedule periodic architecture reviews—cloud features and pricing evolve quickly, so a pipeline that was optimal two years ago may no longer be the best choice. Ask whether long-running jobs should remain in Dataflow, be simplified, consolidated, or migrated to newer services.

That’s it for this lesson. See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/0883bfdc-7d2f-4371-910d-b996380ce4ac/lesson/15458068-1437-424f-a4ac-509f5d8d9bfa" />
</CardGroup>
