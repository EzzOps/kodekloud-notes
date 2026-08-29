# Fix the Slow Query

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/Fix-the-Slow-Query/page

Hands-on lab demonstrating how adding an index to a PostgreSQL table transforms a slow query on five million rows into a fast one using EXPLAIN ANALYZE

This hands-on lab demonstrates how a single index can transform a slow PostgreSQL query into a fast one. You'll:

* Populate a table with 5 million rows.
* Run a representative query and observe poor performance.
* Inspect the query plan to identify the bottleneck.
* Add an appropriate index.
* Re-run the query and observe the performance improvement.

Follow the steps below on a local PostgreSQL instance. Adjust database names and connection strings as needed.

> **lightbulb** This lesson uses PostgreSQL for examples ([PostgreSQL documentation](https://www.postgresql.org/docs/current/)). The same concepts apply to other relational databases, though bulk-insert and EXPLAIN output may differ slightly.

## At-a-glance: What you will run

| Step           | Command / Action | Purpose                                                                     |
| -------------- | ---------------- | --------------------------------------------------------------------------- |
| Create table   | See section 1    | Create a simple `events` table with `user_id` and `created_at`              |
| Bulk load      | See section 2    | Populate table with 5,000,000 rows using `generate_series()`                |
| Baseline query | See section 3    | Run `EXPLAIN ANALYZE` on a filter by `user_id` to observe a sequential scan |
| Add index      | See section 5    | Create an index on `user_id` (optionally `CONCURRENTLY`)                    |
| Re-test        | See section 6    | Re-run `EXPLAIN ANALYZE` to verify index usage and speedup                  |

## 1) Create the table

Create a compact schema to simulate an events log. This table uses `bigserial` for a primary key and stores `user_id`, a timestamp, and a payload.

```sql theme={null}
CREATE TABLE IF NOT EXISTS events (
  id bigserial PRIMARY KEY,
  user_id integer NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  payload text
);
```

## 2) Populate the table with 5 million rows

Use PostgreSQL's `generate_series()` to insert rows efficiently in a single statement. This example distributes `user_id` values across 1..100000 to ensure repetition and realistic selectivity for WHERE filters.

```sql theme={null}
INSERT INTO events (user_id, created_at, payload)
SELECT (i % 100000) + 1,
       now() - (i % 365)::int * interval '1 day',
       'payload ' || i::text
FROM generate_series(1, 5000000) AS s(i);
```

Why this approach:

* One-statement bulk inserts avoid round-trips and are fast.
* The modulus on `user_id` creates repeated values useful for selective queries.

After loading, update planner statistics so EXPLAIN has accurate estimates:

```sql theme={null}
ANALYZE events;
```

## 3) Run the baseline query that will be slow

Run an aggregation filtered by a non-indexed column to produce a worst-case plan. Use `EXPLAIN ANALYZE` to capture both the planner's decision and the actual runtime.

```sql theme={null}
EXPLAIN ANALYZE
SELECT count(*) FROM events WHERE user_id = 12345;
```

Expected behavior: With no index on `user_id`, PostgreSQL will typically do a sequential scan across all 5 million rows, resulting in high I/O and long execution time.

Example conceptual output you might see:

```text theme={null}
Seq Scan on events  (cost=0.00..120000.00 rows=50000 width=8) (actual time=10000.000..10000.500 rows=50 loops=1)
  Filter: (user_id = 12345)
  Rows Removed by Filter: 4999950
Planning Time: 0.500 ms
Execution Time: 10000.600 ms
```

## 4) Diagnose why the query is slow

Key points:

* A sequential scan reads every row because no index exists to target matching `user_id` values.
* Use `EXPLAIN` / `EXPLAIN ANALYZE` to confirm scan type and estimated row counts.
* If the predicate is selective (matches a small fraction of rows), an index will reduce I/O dramatically.

Tools and references:

* `EXPLAIN` / `EXPLAIN ANALYZE` — [PostgreSQL EXPLAIN documentation](https://www.postgresql.org/docs/current/sql-explain.html)
* `ANALYZE` — [PostgreSQL ANALYZE documentation](https://www.postgresql.org/docs/current/sql-analyze.html)

## 5) Create an index on the filtered column

Add an index on `user_id` so the planner can avoid scanning the entire table.

```sql theme={null}
CREATE INDEX CONCURRENTLY idx_events_user_id ON events (user_id);
```

Notes:

* `CONCURRENTLY` prevents write-locking the table during index build (recommended in production). It must run outside an explicit transaction.
* For a local test where you can afford a quick lock, you may omit `CONCURRENTLY` for a faster build:
  ```sql theme={null}
  CREATE INDEX idx_events_user_id ON events (user_id);
  ```
* After index creation, run:
  ```sql theme={null}
  ANALYZE events;
  ```
  PostgreSQL often updates stats during a concurrent build, but an explicit `ANALYZE` is safe.

## 6) Re-run the query and compare performance

Run the same query again with `EXPLAIN ANALYZE` to confirm the planner uses the index and that execution time drops significantly:

```sql theme={null}
EXPLAIN ANALYZE
SELECT count(*) FROM events WHERE user_id = 12345;
```

Example conceptual output showing the improvement:

```text theme={null}
Index Scan using idx_events_user_id on events  (cost=0.29..50.00 rows=50 width=8) (actual time=0.100..0.200 rows=50 loops=1)
  Index Cond: (user_id = 12345)
Planning Time: 0.300 ms
Execution Time: 0.250 ms
```

Notes on results:

* If the planner chooses an `Index Only Scan`, that indicates the index contains all required columns and PostgreSQL avoided accessing the heap.
* Performance gains depend on selectivity, caching, and the storage layout of your table.

## 7) Wrap-up, tips, and best practices

* Always use `EXPLAIN` / `EXPLAIN ANALYZE` to verify the planner's decisions before and after adding indexes.
* Indexes improve read performance but increase write latency and storage use—index only what is necessary.
* For queries filtering on multiple columns, consider multi-column or composite indexes that match the WHERE clause.
* On heavy write workloads, prefer `CREATE INDEX CONCURRENTLY` to avoid blocking writes.
* For frequent COUNT(\*) queries over large tables, consider summary tables, materialized views, or approximate-count solutions instead of repeatedly scanning millions of rows.

Helpful links and references:

* [PostgreSQL Documentation — CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
* [PostgreSQL Documentation — EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
* [PostgreSQL Documentation — ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html)

> **lightbulb** If you want to repeat this experiment from a clean state, drop the index and truncate the table between runs:

  ```sql theme={null}
  DROP INDEX IF EXISTS idx_events_user_id;
  TRUNCATE TABLE events;
  ```

- [Watch Video](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/9afb0146-2b6e-43f0-bf70-c1a007d2260e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/685e02e8-1a11-4ea5-aa7c-f9d814c29caa)
