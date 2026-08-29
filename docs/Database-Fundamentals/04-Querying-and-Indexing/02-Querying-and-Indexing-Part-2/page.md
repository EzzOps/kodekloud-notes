# Querying and Indexing Part 2

Source: https://notes.kodekloud.com/docs/Database-Fundamentals/Querying-and-Indexing/Querying-and-Indexing-Part-2/page

How database indexes and EXPLAIN improve MySQL query performance by using composite and single-column indexes to avoid full scans and accelerate joins and date filters

If we don't query smartly, the database may end up checking every single row — like reading an entire book to find one sentence. Indexes act like bookmarks the database creates: each bookmark points to where matching rows live, and because bookmarks are sorted, the database can jump straight to the right place instead of scanning the whole table.

In this lesson we'll reproduce a real-world performance problem with a small schema, inspect how MySQL executes the query with EXPLAIN, then fix it with the right indexes to demonstrate the performance improvement.

## Schema and setup (MeowTube / miaowtube)

Create the database and switch to it:

```sql theme={null}
CREATE DATABASE miaowtube;
SHOW DATABASES;
USE miaowtube;
SELECT DATABASE();
```

Create two tables — `users` and `videos` — with a foreign key relationship:

```sql theme={null}
CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL
);

CREATE TABLE videos (
  video_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  title TEXT NOT NULL,
  link TEXT NOT NULL,
  upload_date DATE,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

Insert two users:

```sql theme={null}
INSERT INTO users (username, email) VALUES
('fluffy', 'fluffy@email.com'),
('paws', 'paws@email.com');
```

Populate `videos` with one million rows (MySQL 8+): we use a recursive CTE to generate sequential values. Note you may need privileges to change session variables.

```sql theme={null}
SET SESSION cte_max_recursion_depth = 1000000;

WITH RECURSIVE seq AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM seq WHERE n < 1000000
)
INSERT INTO videos (user_id, title, link, upload_date)
SELECT
  FLOOR(1 + RAND() * 2),        -- Randomly assign to fluffy (1) or paws (2)
  CONCAT('video_', n),
  CONCAT('www.miaowtube/watch/', n),
  DATE_ADD('2024-01-01', INTERVAL (n MOD 365) DAY)
FROM seq;
```

Each video is randomly assigned to Fluffy or Paws; upload dates are spread across 2024.

## The real question: How many videos did Fluffy upload in July?

We join `videos` with `users`, filter for `username = 'fluffy'` and the July 2024 range, then count rows:

```sql theme={null}
SELECT COUNT(*)
FROM videos v
JOIN users u ON v.user_id = u.user_id
WHERE u.username = 'fluffy'
  AND v.upload_date >= '2024-07-01'
  AND v.upload_date <  '2024-08-01';
```

On this dataset the query runs in under two seconds and returns roughly the expected value (\~42,000 rows given the distribution), but looking at EXPLAIN reveals why it still does more work than necessary.

### EXPLAIN output (before adding helpful indexes)

Run EXPLAIN for the same query:

```sql theme={null}
EXPLAIN
SELECT COUNT(*)
FROM videos v
JOIN users u ON v.user_id = u.user_id
WHERE u.username = 'fluffy'
  AND v.upload_date >= '2024-07-01'
  AND v.upload_date <  '2024-08-01'\G
```

Example (trimmed) output:

* `users (u)` scanned without an index (key: NULL) — acceptable for 2 rows, but not for many users.
* `videos (v)` used the foreign key index on `user_id`, but MySQL still applied the `upload_date` filter row-by-row ("Using where"), meaning it accessed all of Fluffy's videos and then filtered by date.

With tens of thousands of videos for Fluffy, those per-row date checks accumulate and slow the query.

## Fix: add the right indexes

Add an index on `users.username` and a composite index on `videos(user_id, upload_date)`. The composite index allows MySQL to find Fluffy's July uploads in a single indexed operation, avoiding per-row date checks.

```sql theme={null}
CREATE INDEX idx_username ON users(username);

CREATE INDEX idx_user_date ON videos(user_id, upload_date);
```

Index creation can take time for large tables, but it's a one-time cost that pays dividends when queries are frequent.

### EXPLAIN output (after indexing)

Run EXPLAIN again for the same query:

```sql theme={null}
EXPLAIN
SELECT COUNT(*)
FROM videos v
JOIN users u ON v.user_id = u.user_id
WHERE u.username = 'fluffy'
  AND v.upload_date >= '2024-07-01'
  AND v.upload_date <  '2024-08-01'\G
```

Example (trimmed) output summary:

* `users` now uses `idx_username` to find Fluffy immediately.
* `videos` uses the composite `idx_user_date` so MySQL can apply `user_id` + `upload_date` via the index without scanning all rows.

Performance in this demo dropped from \~2 seconds to \~0.1 seconds — roughly a 20x speedup. In production, where similar queries run thousands of times, the cumulative savings are substantial.

> **lightbulb** Indexes are the single most effective way to speed up lookups and joins in OLTP workloads. Build them thoughtfully: too many indexes slow writes, and composite indexes are valuable when you filter on several columns together.

## Index best-practices quick reference

| Index type                      | When to use                                                                    | Example                                                       |
| ------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| Single-column index             | When you frequently filter or join on a single column                          | `CREATE INDEX idx_username ON users(username);`               |
| Composite index                 | When you filter by multiple columns together (and the leftmost prefix is used) | `CREATE INDEX idx_user_date ON videos(user_id, upload_date);` |
| Primary key / foreign-key index | Automatically used for joins and lookups on the PK/FK                          | `user_id` in `videos` referencing `users(user_id)`            |

> **warning** Indexes speed reads but add overhead to writes (INSERT/UPDATE/DELETE). Monitor index usage (e.g., with EXPLAIN and perf tools) and avoid creating unused indexes.

## Additional query-performance habits (no index required)

* Select only needed columns — avoid `SELECT *` when you only need a few fields.
* Limit results when appropriate: `LIMIT 10` for previews.
* Apply filters early with WHERE so the engine processes less data.
* Break complex logic into simpler queries when that reduces scanned rows.

<Frame>
  <img alt="The image shows a person standing next to a list of SQL query optimization tips on a purple gradient background, with the text &#x22;KodeKloud&#x22; on their shirt." />
</Frame>

If you guide the database with concise filters and the right indexes, it won't need to grind through every row. Indexes provide the biggest speedup, and clean queries amplify that benefit.

## Quick challenge

Cody wants to show the most recent videos first, include only those uploaded after 1st of June, and display the top 3 results. Which query is correct?

A:

```sql theme={null}
SELECT * FROM videos
WHERE upload_date > '2025-06-01'
ORDER BY upload_date DESC
LIMIT 3;
```

B:

```sql theme={null}
SELECT * FROM videos
WHERE upload_date > '2025-06-01'
ORDER BY upload_date DESC
LIMIT 3;
```

C:

```sql theme={null}
SELECT * FROM videos
ORDER BY upload_date DESC
WHERE upload_date > '2025-06-01'
LIMIT 3;
```

Correct: A (and B are identical here). Option C is invalid because the `WHERE` clause must come before `ORDER BY`. The correct structure is:

```sql theme={null}
SELECT * FROM videos
WHERE upload_date > '2025-06-01'
ORDER BY upload_date DESC
LIMIT 3;
```

Remember clause order: FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY -> LIMIT.

## Recap

* SQL queries follow a specific clause order; write them accordingly to avoid syntax errors and to ensure correct results.
* Indexes are like bookmarks: with the right indexes (especially composite indexes when filtering on multiple columns), the database can jump directly to matching rows and avoid full scans.
* Even without indexes, you can improve performance by selecting only required fields, limiting results, simplifying queries, and applying filters early.

<Frame>
  <img alt="The image shows a person on the right side and three text boxes on the left side with information about SQL order and indexing. The person appears to be explaining or presenting the content." />
</Frame>

## Links and references

* [MySQL EXPLAIN](https://dev.mysql.com/doc/refman/en/explain.html)
* [MySQL Indexes](https://dev.mysql.com/doc/refman/en/mysql-indexes.html)
* [Understanding Composite Indexes](https://use-the-index-luke.com/sql/where-clause/basics/index-composite)

- [Watch Video](https://learn.kodekloud.com/user/courses/database-fundamentals/module/5edfd17e-97e6-4a23-9c91-4dee1d8a3024/lesson/f69ab33f-15d2-42ce-ac70-30ca268f225b)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/database-fundamentals/module/5edfd17e-97e6-4a23-9c91-4dee1d8a3024/lesson/a6abf81e-05f4-49b2-b469-6ea4c1e0b95b)
