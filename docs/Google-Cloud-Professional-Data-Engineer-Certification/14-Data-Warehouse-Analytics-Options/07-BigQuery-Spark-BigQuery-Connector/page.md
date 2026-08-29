# BigQuery Spark BigQuery Connector

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/BigQuery-Spark-BigQuery-Connector/page

Explains the Spark BigQuery connector, its Dataproc integration, usage patterns, code examples, performance and IAM considerations for reading and writing BigQuery from Spark jobs

This article explains the Spark–BigQuery connector: what it is, when to use it, and how it integrates into a Dataproc + BigQuery workflow. It covers typical usage patterns, code examples, operational considerations, and best practices for production workloads.

Why use Spark with BigQuery?

* BigQuery excels at large-scale SQL analytics, but some workflows require capabilities beyond SQL:
  * Complex transformations and multi-step pipelines that are easier or more efficient in Spark.
  * Custom machine learning training and feature engineering with Spark MLlib.
  * Enrichment of BigQuery data with files in Cloud Storage or other external sources.
* Spark provides distributed, in-memory processing for iterative workloads and advanced transformations that complement BigQuery's SQL capabilities.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Move Data From BigQuery to Spark?&#x22; that says to leverage Spark’s distributed in-memory processing for complex transformations, custom ML workflows, and data enrichment. It adds these use cases go beyond standard SQL capabilities." />
</Frame>

What the connector does

* The Spark–BigQuery connector bridges Spark and BigQuery so Spark jobs can:
  * Read BigQuery tables into Spark DataFrames.
  * Write Spark DataFrames back to BigQuery tables.
* On Dataproc, the connector is included with the image and uses the BigQuery Storage API to read data in parallel for improved performance.
* Typical workflow: extract (BigQuery) → transform/train (Spark on Dataproc) → load (BigQuery) — often described as ETTL (extract, transform, train, load).

How it works (high level)

1. Read path:
   * Spark requests data via the connector, which uses the BigQuery Storage API to stream data in parallel into Spark partitions.
   * Optionally the connector uses temporary Cloud Storage files for certain jobs or to optimize writes.
2. Transform/train:
   * Data is processed in-memory across the Dataproc cluster; you can join, filter, and run MLlib jobs.
3. Write path:
   * DataFrames are written back to BigQuery by the connector using BigQuery streaming inserts or load jobs (which may use GCS as temporary storage).

Typical usage examples (PySpark)

* Read a BigQuery table into a Spark DataFrame:

```python theme={null}
