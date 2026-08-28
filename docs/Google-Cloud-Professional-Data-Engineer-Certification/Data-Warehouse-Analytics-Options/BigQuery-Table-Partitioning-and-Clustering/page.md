# BigQuery Table Partitioning and Clustering

Source: https://notes.kodekloud.com/docs/Google-Cloud-Professional-Data-Engineer-Certification/Data-Warehouse-Analytics-Options/BigQuery-Table-Partitioning-and-Clustering/page

Explains BigQuery table partitioning and clustering benefits, differences, examples, best practices, and sample DDL to improve query performance and reduce cost.

Welcome — in this lesson you'll learn how table partitioning and clustering work in BigQuery, why they matter for cost and performance, and when to use each. If you’ve used Hive or other data warehouses, these concepts will feel familiar. This article maps those ideas to BigQuery with a concise example to show the practical differences and benefits.

## Example scenario

Imagine a simple `orders` table with these columns:

* `order_id`
* `country`
* `status`
* `order_date`

Start with the table unpartitioned and unclustered, then examine how queries behave as you apply clustering and partitioning.

## Unoptimized table behavior

When the table has no partitioning or clustering, BigQuery cannot prune by date or specific column values. For example:

```sql theme={null}
SELECT * FROM dataset.orders;
```

This query scans the entire table. Even a filtered query such as:

```sql theme={null}
SELECT * FROM dataset.orders WHERE country = 'US';
```

may still scan much of the table because the storage layout does not group rows by `country` or `order_date`. On very large tables this increases query latency and cost—especially with billions of rows.

## Clustering by a column (example: country)

Clustering organizes data so rows with similar values for the clustered columns are stored physically close together. If you cluster by `country`, values like `Japan`, `UK`, and `US` will tend to reside in nearby blocks on disk.

When you run:

```sql theme={null}
SELECT * FROM dataset.orders WHERE country = 'US';
```

BigQuery can use cluster metadata to skip blocks that are unlikely to contain `US` rows, reducing the amount of data scanned. Clustering is most effective when your queries frequently filter on the clustered columns (equality predicates, GROUP BY, or JOIN keys) and when the clustered columns have moderate cardinality.

## Partitioning (example: order\_date)

Partitioning splits a table into segments, often by `DATE` or `TIMESTAMP`. A typical pattern is partitioning by `order_date`, so each day (or range) lives in a separate partition.

If your query filters on the partition column, e.g.:

```sql theme={null}
SELECT * FROM dataset.orders WHERE order_date = '2022-08-05';
```

BigQuery performs partition pruning first and scans only the relevant partition(s). This reduces the scanned data dramatically for time-bounded queries.

## Combining partitioning and clustering

The best efficiency often comes from combining partitioning and clustering:

* Partitioning prunes large swaths of data (for example, specific date ranges).
* Clustering then prunes within those partitions to find rows for specific values (for example, `country`).

Example:

```sql theme={null}
SELECT * FROM dataset.orders
WHERE order_date = '2022-08-05' AND country = 'US';
```

Execution flow:

1. Partition pruning: BigQuery scans only the `2022-08-05` partition.
2. Cluster pruning: Within that partition, BigQuery reads only the blocks that likely contain `country = 'US'`.

This two-stage pruning minimizes scanned bytes, lowers query latency, and reduces cost.

## Sample DDL for a partitioned and clustered table

Use this DDL to create a table partitioned by `order_date` and clustered by `country`:

```sql theme={null}
CREATE TABLE dataset.orders (
  order_id STRING,
  country STRING,
  status STRING,
  order_date DATE
)
PARTITION BY order_date
CLUSTER BY country;
```

## Best practices and guidance

| Topic                        |                                                                                                                      Recommendation | Why it matters                                                                                            |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------: | --------------------------------------------------------------------------------------------------------- |
| Partition column             |                                                        Choose a column used commonly in date or range filters (e.g., `order_date`). | Partition pruning avoids scanning irrelevant time ranges.                                                 |
| Clustering columns           |    Cluster on columns used in equality filters, GROUP BY, or JOIN predicates. Prefer moderate-cardinality columns (not unique IDs). | Enables block-level pruning and speeds selective queries.                                                 |
| Number of clustering columns |                                                                                              Keep it small (typically 1–4 columns). | More columns dilute clustering effectiveness and increase maintenance overhead.                           |
| When to define partitions    | Define partitioning at table creation where possible. To partition an existing table, create a new partitioned table and copy data. | Initial partitioning produces the cleanest storage layout and best early performance.                     |
| Adding clustering            |                                                          You can add clustering to existing tables; subsequent writes will benefit. | Enables incremental improvement without full rewrite, though initial data may not be optimally clustered. |

## Quick example queries

```sql theme={null}
SELECT * FROM dataset.orders;
SELECT * FROM dataset.orders WHERE country = 'US';
SELECT * FROM dataset.orders WHERE order_date = '2022-08-05' AND country = 'US';
```

<Callout icon="lightbulb">
  Partition pruning (by the partition column) runs first; clustering then prunes within the selected partitions. Together, they significantly reduce scanned data and query cost.
</Callout>

<Callout icon="warning">
  If your queries rarely filter on the partition column or clustered columns, BigQuery will still scan large portions of the table. Design partitions and clusters based on real query patterns to avoid unexpected costs.
</Callout>

## Further reading and references

* BigQuery partitioned tables: [https://cloud.google.com/bigquery/docs/partitioned-tables](https://cloud.google.com/bigquery/docs/partitioned-tables)
* BigQuery clustered tables: [https://cloud.google.com/bigquery/docs/clustered-tables](https://cloud.google.com/bigquery/docs/clustered-tables)

Designing partitioning and clustering thoughtfully for base models is a core responsibility for data engineers — these decisions directly affect performance and cost for everyone who queries the data.

See you in the next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-cloud-professional-data-engineer-certification/module/5918fa46-3bfb-4bd1-a53b-41f2a2a77532/lesson/15c85131-ed11-46ea-a1eb-3d6b906e9802" />
</CardGroup>
