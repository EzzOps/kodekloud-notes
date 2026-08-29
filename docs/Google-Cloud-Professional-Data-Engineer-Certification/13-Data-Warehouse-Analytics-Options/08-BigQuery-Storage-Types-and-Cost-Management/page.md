# PySpark: read from BigQuery
df = spark.read.format("bigquery") \
    .option("table", "my-project.my_dataset.my_table") \
    .load()
```

* Write a Spark DataFrame back to BigQuery:

```python theme={null}
# PySpark: write to BigQuery
df.write.format("bigquery") \
    .option("table", "my-project.my_dataset.output_table") \
    .mode("overwrite") \
    .save()
```

* Read via SQL (register as temp view, then run Spark SQL):

```python theme={null}
# Register BigQuery table as a temporary view, then query
df = spark.read.format("bigquery") \
    .option("table", "my-project.my_dataset.my_table") \
    .load()
df.createOrReplaceTempView("bq_table")
result = spark.sql("SELECT user_id, COUNT(*) AS cnt FROM bq_table GROUP BY user_id")
```

Operational notes and IAM

* Dataproc: the connector is preinstalled in Dataproc images — no extra JARs required when using supported images.
* Authentication:
  * Dataproc clusters use the cluster service account to authenticate to BigQuery and Cloud Storage.
  * If running Spark outside Dataproc, you must add the connector artifact and configure credentials (e.g., ADC or service account key).
* Performance considerations:
  * Use the BigQuery Storage API for faster reads.
  * Tune Spark cluster size and partitioning to match the input table size.
  * For large writes, prefer load jobs (temporary GCS files) over streaming inserts when appropriate.

Permissions quick reference

| Operation                            | Minimum IAM role (example)                                        |
| ------------------------------------ | ----------------------------------------------------------------- |
| Read from BigQuery                   | `roles/bigquery.dataViewer`                                       |
| Write to BigQuery (create/overwrite) | `roles/bigquery.dataEditor` or `roles/bigquery.dataOwner`         |
| Use temporary GCS for writes         | `roles/storage.objectAdmin` (or scoped permissions to the bucket) |
| Dataproc cluster actions             | `roles/dataproc.worker` / `roles/dataproc.editor` as applicable   |

> **lightbulb** On Dataproc the Spark–BigQuery connector comes preinstalled with the image; this lets you read and write BigQuery tables from Spark jobs without manually adding connector jars or dependencies.

Real-world scenario (example flow)
A retail company trains a recommendations model:

1. Query historical sales and user interaction tables from BigQuery into Spark DataFrames on Dataproc.
2. Enrich those DataFrames with product metadata stored in Cloud Storage.
3. Train a recommendation model using Spark MLlib and evaluate it across partitions.
4. Write model outputs (predictions, feature tables, or aggregates) back to BigQuery for dashboards and downstream consumers.

Exam tip

* If asked which Google Cloud service includes the Spark–BigQuery connector out of the box, the answer is Dataproc.

> **warning** Ensure the Dataproc cluster's service account has the necessary BigQuery and Cloud Storage IAM roles. The connector will be present, but read/write operations will fail without proper permissions.

Additional resources

* BigQuery Storage API: [https://cloud.google.com/bigquery/docs/reference/storage](https://cloud.google.com/bigquery/docs/reference/storage)
* Dataproc documentation: [https://cloud.google.com/dataproc/docs](https://cloud.google.com/dataproc/docs)
* Spark BigQuery Connector GitHub: [https://github.com/GoogleCloudDataproc/spark-bigquery-connector](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)

Summary

* The Spark–BigQuery connector simplifies moving data between BigQuery and Spark, unlocking advanced transformations, iterative ML workflows, and enrichment with external files.
* Dataproc makes integration straightforward by including the connector and managing the runtime; ensure IAM and temporary GCS access are configured for production runs.

Another option for accessing external data is BigQuery federated queries, where BigQuery queries data that remains in an external system without importing it.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/a51396ea-1996-4201-a41e-4124f3126787)


# BigQuery Storage Types and Cost Management

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/BigQuery-Storage-Types-and-Cost-Management/page

Explains BigQuery storage tiers, physical vs logical storage, slot-based compute pricing, and practical cost management techniques like partitioning, clustering, and choosing on-demand or flat-rate/flex slots.

Welcome back. In this lesson we explain how BigQuery storage types and compute pricing interact, and how to manage costs effectively. We cover:

* BigQuery storage tiers: active vs long-term
* Physical vs logical storage and how billing is applied
* Compute (slots) and pricing models: on-demand, flat-rate, and flex slots
* Practical guidance to reduce storage and query costs

Table partitioning and clustering improve performance and lower query costs by reducing the bytes scanned. Even after optimizing table design, storage and processing fees can still add up. This article shows how BigQuery charges for storage and compute so you can choose the best cost-management approach.

## Active vs Long-Term Storage

BigQuery applies two main storage tiers with automatic billing behavior:

* Active storage: Data modified or ingested in the last 90 days. Billed at the standard storage rate and kept ready for frequent access.
* Long-term storage: Data unchanged for 90 consecutive days. BigQuery automatically applies a discounted long-term rate (typically about half of active pricing).

Use cases:

* Active: frequently queried datasets (recent product catalog, operational tables).
* Long-term: historical reports, compliance archives, backups that are rarely modified.

| Storage Tier      | When it applies                          | Typical use case            | Pricing example        |
| ----------------- | ---------------------------------------- | --------------------------- | ---------------------- |
| Active storage    | Data modified within the last 90 days    | Frequently queried datasets | `~$0.020 / GB / month` |
| Long-term storage | Data unmodified for 90+ consecutive days | Archival/historical data    | `~$0.010 / GB / month` |

<Frame>
  <img alt="A presentation slide titled &#x22;Storage Types and Cost Management&#x22; showing a table that compares storage types (Active, Long-Term, Physical, Logical) with descriptions, pricing, and use cases. It notes example prices for active and long-term storage (0.020 and 0.010 per GB/month) and billing based on compressed or logical size for the others." />
</Frame>

## Physical vs Logical Storage (and billing considerations)

Understanding physical vs logical storage helps explain why you might see differences between storage billed and query bytes processed.

* Physical storage: The actual bytes written to disk after BigQuery’s columnar compression. Billing and reported storage usage in the console are based on this compressed size.
* Logical storage: The uncompressed size or the conceptual amount of data in table columns. Logical layout determines how many bytes a query reads (bytes processed).

Key billing points:

* Storage charges are based on the physical (compressed) size and the applied storage tier (active or long-term).
* Query charges (on-demand) are based on bytes processed—driven by logical size and which columns/partitions the query reads.
* Compression reduces storage costs and I/O, but query charges depend on which logical data the query scans; compression alone won’t eliminate query costs.

| Concern          | Billing basis                        | Impact on cost                                                   |
| ---------------- | ------------------------------------ | ---------------------------------------------------------------- |
| Storage          | Physical (compressed) bytes          | Reduces storage costs when compression effective                 |
| Query processing | Logical bytes scanned (columns read) | Drives on-demand query charges; partition/clustering reduce this |

> **lightbulb** BigQuery automatically applies the long-term storage discount to data that hasn't been modified for 90 consecutive days—no manual action required.

## Compute and Slot Pricing

BigQuery executes queries on slots (virtualized CPU capacity). You can pay for slots in multiple ways, depending on predictability and scale of workloads.

* On-demand (pay-per-query)
  * Pricing: pay per bytes processed (commonly quoted per TB processed).
  * Best for: ad-hoc analysis, unpredictable workloads, experimentation.
  * Pros: no upfront commitment.
  * Cons: costs can spike with many or inefficient queries, or when large unpartitioned tables are scanned.

* Flat-rate (reservations)
  * Pricing: reserve a fixed number of slots for a predictable monthly cost.
  * Best for: steady, production workloads requiring predictable performance.
  * Pros: consistent performance and predictable spend for large teams.
  * Cons: higher upfront cost; typically used by organizations with sustained usage.

* Flex slots
  * Pricing: short-term slot reservations (hourly) to temporarily increase capacity.
  * Best for: short bursts (end-of-month reporting, heavy ETL window).
  * Pros: scale up only when needed without long-term commitment.
  * Cons: limited to temporary bursts; may require orchestration to use effectively.

> **warning** Choose the right compute model carefully: on-demand can be cost-effective for small or sporadic workloads, while flat-rate is usually more economical for sustained, high-volume query traffic. Monitor slot utilization and query efficiency to avoid overspending.

## How costs add up

Your BigQuery bill typically includes:

* Storage: active and long-term rates depending on last modification.
* Query processing: on-demand (bytes processed) or slot usage (flat-rate/flex).
* Data ingestion: streaming inserts or certain loading methods may incur additional fees.

Simple guidance to manage costs:

* Use partitioning and clustering to limit the amount of data scanned by queries.
* Select only the columns you need in queries to reduce logical bytes processed.
* Move rarely modified data to long-term tier automatically by allowing 90 days without modification.
* Choose on-demand for low/unpredictable usage; choose flat-rate for stable, predictable workloads; use flex slots for short bursts.

| Cost area        | How to reduce it                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |
| Storage          | Columnar compression, table design, remove unused data, rely on automatic long-term discount                       |
| Query processing | Partitioning, clustering, selective column projection, optimize SQL and use approximate functions where applicable |
| Ingestion        | Batch load instead of streaming when possible to avoid streaming costs                                             |

## References and further reading

* BigQuery documentation: [https://cloud.google.com/bigquery/docs](https://cloud.google.com/bigquery/docs)
* BigQuery pricing (storage and analysis): [https://cloud.google.com/bigquery/pricing](https://cloud.google.com/bigquery/pricing)

<Frame>
  <img alt="A presentation slide titled &#x22;Pricing Models&#x22; that outlines storage pricing components (data storage, query processing, data ingestion) and shows a comparison table of pricing models. The table lists On-Demand (5 per TB processed), Flat-Rate (2,000+ per month), and Flex Slots ($4 per slot-hour) with columns for what each is best for and considerations." />
</Frame>

## Summary

* Organize datasets so queries read only what they need: use partitioning, clustering, and column projection to minimize bytes processed.
* BigQuery automatically applies long-term storage pricing after 90 days of no modifications—leverage this for archival/backup data.
* Choose on-demand, flat-rate, or flex slots based on usage patterns to control compute costs.
* Monitor both storage and query processing charges for a complete picture of BigQuery spend.

That is it for this lesson. See you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/1dc07282-50eb-43b3-91bd-7344302059ed)
