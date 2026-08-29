# Create a dataset in the US location using the bq CLI
bq --location=US mk --dataset my_project:us_operations
```

Create a native table:

```sql theme={null}
-- Create a native table with a simple schema
CREATE TABLE `my_project.us_operations.oil_production` (
  site_id STRING,
  production_date DATE,
  barrels FLOAT64
);
```

Create a standard view:

```sql theme={null}
-- Create a standard view that aggregates daily production
CREATE VIEW `my_project.us_operations.daily_production_summary` AS
SELECT
  production_date,
  SUM(barrels) AS total_barrels
FROM `my_project.us_operations.oil_production`
GROUP BY production_date;
```

Create a materialized view:

```sql theme={null}
-- Create a materialized view to cache aggregated results
CREATE MATERIALIZED VIEW `my_project.us_operations.mv_daily_production` AS
SELECT
  production_date,
  SUM(barrels) AS total_barrels
FROM `my_project.us_operations.oil_production`
GROUP BY production_date;
```

## Views: behavior and best practices

* Standard view: stores only SQL logic. Querying a view runs its SQL against the underlying tables and returns up-to-date data.
* Authorized view: use this pattern to expose a restricted column set or aggregated metrics without granting direct access to the base tables.
* Materialized view: stores precomputed results to accelerate repeated queries (useful for dashboards and KPI lookups).

Performance note: materialized views speed up repeated queries, but they are not a substitute for a well-designed schema and efficient SQL. Partitioning, clustering, and query optimization remain crucial.

<Frame>
  <img alt="A presentation slide titled &#x22;Views Features&#x22; showing four blue panels labeled Virtual Table, Security Layer, Types of Views, and Performance Consideration, each with an icon and a short description about SQL/view behavior and materialized views. The slide has a clean turquoise/white design with a © Copyright KodeKloud note at the bottom." />
</Frame>

## Quick exam-style question

Which BigQuery object physically stores the data?

* A) Dataset
* B) Table
* C) View

Answer: B) Table — tables physically store the data. Datasets are logical containers and views are stored SQL logic.

> **lightbulb** Remember: datasets organize and secure your data, tables store it, and views present or cache query logic. Use dataset locations and labels for governance and compliance, and prefer partitioning/clustering for performance.

## Hands-on practice

Use the BigQuery console to:

* Create a dataset in the appropriate location.
* Create native tables and load sample data.
* Create a standard view to expose aggregated results.
* Optionally create a materialized view for a frequently queried aggregation and observe query performance improvements.

## Links and references

* [BigQuery documentation — Concepts](https://cloud.google.com/bigquery/docs/introduction)
* [Creating and managing datasets](https://cloud.google.com/bigquery/docs/datasets)
* [Materialized views in BigQuery](https://cloud.google.com/bigquery/docs/materialized-views)

That’s it for this lesson — see you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/2e71375e-838c-44bb-a184-3feb8f3ab09c)


# BigQuery Federated Queries

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/BigQuery-Federated-Queries/page

Explains BigQuery federated queries, how to query external data sources at runtime, use cases, performance and cost considerations, examples and best practices for ad hoc and prototyping analysis.

Welcome — in this lesson you'll learn what BigQuery federated queries are, when to use them, and how they work in practice.

A federated query lets BigQuery read external data at query time and combine it with native BigQuery tables without first ingesting the data. This is ideal for quick, ad-hoc analysis and multi-source joins when building and maintaining an ETL pipeline is impractical.

<Frame>
  <img alt="A slide titled &#x22;BigQuery Federated Queries&#x22; showing a simple diagram of a user querying a BigQuery icon and getting results. To the right are bullet points saying data may reside outside BigQuery, might not be movable, and asking if it can still be queried together." />
</Frame>

Key points

* Federated queries let BigQuery read external data sources at query time and join that data with native BigQuery tables.
* Supported external sources include Cloud Storage (CSV, JSON, Avro, Parquet, ORC), Google Drive / Google Sheets, Cloud SQL (MySQL/PostgreSQL) and Cloud Spanner via BigQuery connections, Cloud Bigtable, and other sources exposed through connectors.
* Conceptually similar to query engines like [Presto](https://prestodb.io) that present a single SQL interface across multiple data sources.

Supported external sources (summary)

| External resource         |                                                        Access method / formats | Typical use case                                                |
| ------------------------- | -----------------------------------------------------------------------------: | --------------------------------------------------------------- |
| Cloud Storage             | `CSV`, `JSON`, `Avro`, `Parquet`, `ORC` via external table `OPTIONS(uris=...)` | Query logs or exported files without loading them into BigQuery |
| Google Sheets / Drive     |                                    External tables with `GOOGLE_SHEETS` driver | Blend client-provided spreadsheets with production datasets     |
| Cloud SQL / Cloud Spanner |                 BigQuery Connections + federated queries or `EXTERNAL_QUERY()` | Ad-hoc analysis of transactional DBs (use cautiously)           |
| Cloud Bigtable            |                                Connector for large, low-latency key-value data | Analytical joins with time-series or wide-column data           |

When to use federated queries

* Short-lived, ad-hoc analysis where ingesting data into BigQuery is slower or unnecessary.
* Prototyping, proof-of-concept, or exploratory analysis to validate hypotheses before committing to ingestion and ETL.
* Blending small client-supplied datasets (for example, a Google Sheet) with a production BigQuery dataset to avoid building a pipeline for transient data.

Important cautions

> **warning** Federated queries can increase latency and may generate charges from both BigQuery and the external data source. Querying transactional systems (Cloud SQL or Cloud Spanner) can affect production performance. For recurring, large-scale analytics, ingesting data into BigQuery is generally more performant and cost-effective.

How it works (high-level)

* Define an external table or create a BigQuery Connection that references the remote data source.
* When your SQL references that external table, BigQuery reads the source data at query time and processes it together with native tables.
* External data is not persisted in BigQuery unless you explicitly load it into a native table.

Example: define and query a Cloud Storage external table

* Create an external table that points to CSV files in Cloud Storage, then join it with a native table:

```sql theme={null}
-- Create an external table that reads CSV files directly from Cloud Storage
CREATE EXTERNAL TABLE `mydataset.external_orders`
OPTIONS (
  format = 'CSV',
  uris = ['gs://my-bucket/orders/*.csv'],
  skip_leading_rows = 1
);

-- Query and join with a native BigQuery table
SELECT t.order_id, t.total_amount, e.region
FROM `myproject.mydataset.transactions` AS t
LEFT JOIN `myproject.mydataset.external_orders` AS e
  ON t.order_id = CAST(e.order_id AS INT64)
WHERE t.event_date >= '2024-01-01';
```

Example: query a Google Sheet as an external table

* Create an external table with `GOOGLE_SHEETS` format and query it in place (useful for small, client-managed sheets).

Cost and performance tips

> **lightbulb** Federated queries are excellent for quick results and small-to-medium datasets. For high-frequency queries or large datasets, prefer loading data into BigQuery to reduce latency and cost. Monitor query plan and bytes processed, and avoid scanning unnecessary columns or files in the external source.

Best practices

* Limit the scanned data: use file filtering (for Cloud Storage URIs), column projection, and WHERE clauses to reduce bytes read.
* Use federated queries for prototyping and low-frequency use; move stable, high-volume data into BigQuery for repeated analysis.
* For Cloud SQL or Spanner, consider creating read replicas or exporting snapshots if analytical queries would impact production performance.
* Track and monitor costs that may come from both BigQuery processing and the external source (e.g., Cloud SQL I/O).

Links and references

* [BigQuery External Data Sources and Federated Queries (official docs)](https://cloud.google.com/bigquery/external-data-sources)
* [Querying Cloud SQL and Spanner from BigQuery](https://cloud.google.com/bigquery/docs/remote-service-querying)
* [Presto / Trino — querying multiple data sources](https://trino.io/)

Summary
BigQuery federated queries let you query and join external data where it lives without first ingesting it into BigQuery. They're powerful for ad-hoc analysis, prototyping, and blending external client data, but consider latency, cost, and the potential impact on source systems when using them. See you in the next lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/ec083a59-6e52-4b6c-9182-a7e70a1c8cd4)
