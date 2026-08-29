# Querying and Indexing

Source: https://notes.kodekloud.com/docs/Database-Fundamentals/Querying-and-Indexing/Querying-and-Indexing/page

Explains SQL SELECT query construction, filtering, sorting, joins, clause order, limiting and introduces indexing for improving relational database query performance.

KodeKloud's MeowTube is growing fast. Videos, users, and comments are accumulating into a large, structured dataset. After weighing relational vs non-relational options, KodeKloud chose a relational database for MeowTube — it's predictable, reliable, and well suited to the kinds of queries the app needs.

But as the dataset grows, simple SELECTs start taking longer. Understanding SQL query structure and how to optimize it (including using indexes) is essential for DevOps and cloud engineers to keep applications responsive at scale.

This lesson builds on CRUD basics and shows how to:

* Construct common SELECT queries correctly
* Use filtering, sorting, limiting, and joins
* Understand clause order and why it matters
* Prepare for the next topic: indexes and performance

We’ll use the `users` and `videos` tables as examples. Pay attention to the order of clauses — SQL expects them in a specific sequence, similar to following a recipe.

## Inspecting whole tables

To return every column and every row from a table, use `SELECT * FROM table_name;` — don’t forget the semicolon.

```sql theme={null}
mysql-> SELECT * FROM users;
+---------+----------+-------------------+
| user_id | username | email             |
+---------+----------+-------------------+
|       1 | fluffy   | fluffy@email.com  |
|       2 | paws     | paws@email.com    |
+---------+----------+-------------------+
2 rows in set (0.00 sec)

mysql-> SELECT * FROM videos;
+----------+---------+------------------+---------------------------+--------------+
| video_id | user_id | title            | link                      | upload_date  |
+----------+---------+------------------+---------------------------+--------------+
|        1 |       1 | Cat Skateboard   | www.miaowtube/watch1      | 2025-05-25   |
|        2 |       2 | Epic Cat Jump    | www.miaowtube/watch2      | 2025-05-27   |
|        3 |       1 | Cat vs Curtain   | www.miaowtube/watch3      | 2025-05-29   |
+----------+---------+------------------+---------------------------+--------------+
3 rows in set (0.00 sec)
```

## Selecting specific columns

If you only need certain columns, list them instead of `*`:

```sql theme={null}
mysql-> SELECT title FROM videos;
+------------------+
| title            |
+------------------+
| Cat Skateboard   |
| Epic Cat Jump    |
| Cat vs Curtain   |
+------------------+
3 rows in set (0.00 sec)
```

Return multiple columns by separating them with commas:

```sql theme={null}
mysql-> SELECT video_id, title, upload_date FROM videos;
+----------+------------------+--------------+
| video_id | title            | upload_date  |
+----------+------------------+--------------+
|        1 | Cat Skateboard   | 2025-05-25   |
|        2 | Epic Cat Jump    | 2025-05-27   |
|        3 | Cat vs Curtain   | 2025-05-29   |
+----------+------------------+--------------+
3 rows in set (0.00 sec)
```

## Filtering rows with WHERE

Use `WHERE` to restrict rows. Column names must match the table schema (here `upload_date`):

```sql theme={null}
mysql-> SELECT * FROM videos
    -> WHERE upload_date = '2025-05-27';
+----------+---------+----------------+---------------------------+--------------+
| video_id | user_id | title          | link                      | upload_date  |
+----------+---------+----------------+---------------------------+--------------+
|        2 |       2 | Epic Cat Jump  | www.miaowtube/watch2      | 2025-05-27   |
+----------+---------+----------------+---------------------------+--------------+
1 row in set (0.00 sec)
```

Tip: If you press Enter without a terminating semicolon, the MySQL prompt shows `->` and waits for the statement to be completed. This makes multi-line queries easier to read.

## Sorting with ORDER BY

Sort results using `ORDER BY`. Use `DESC` for descending (newest first) and `ASC` for ascending:

```sql theme={null}
mysql-> SELECT * FROM videos ORDER BY upload_date DESC;
+----------+---------+------------------+---------------------------+--------------+
| video_id | user_id | title            | link                      | upload_date  |
+----------+---------+------------------+---------------------------+--------------+
|        3 |       1 | Cat vs Curtain   | www.miaowtube/watch3      | 2025-05-29   |
|        2 |       2 | Epic Cat Jump    | www.miaowtube/watch2      | 2025-05-27   |
|        1 |       1 | Cat Skateboard   | www.miaowtube/watch1      | 2025-05-25   |
+----------+---------+------------------+---------------------------+--------------+
3 rows in set (0.00 sec)

mysql-> SELECT * FROM videos ORDER BY upload_date ASC;
+----------+---------+------------------+---------------------------+--------------+
| video_id | user_id | title            | link                      | upload_date  |
+----------+---------+------------------+---------------------------+--------------+
|        1 |       1 | Cat Skateboard   | www.miaowtube/watch1      | 2025-05-25   |
|        2 |       2 | Epic Cat Jump    | www.miaowtube/watch2      | 2025-05-27   |
|        3 |       1 | Cat vs Curtain   | www.miaowtube/watch3      | 2025-05-29   |
+----------+---------+------------------+---------------------------+--------------+
3 rows in set (0.00 sec)
```

## Limit the result set with LIMIT

Use `LIMIT` to restrict how many rows are returned. `LIMIT` should come last in the statement:

```sql theme={null}
mysql-> SELECT * FROM videos ORDER BY upload_date DESC LIMIT 2;
+----------+---------+------------------+---------------------------+--------------+
| video_id | user_id | title            | link                      | upload_date  |
+----------+---------+------------------+---------------------------+--------------+
|        3 |       1 | Cat vs Curtain   | www.miaowtube/watch3      | 2025-05-29   |
|        2 |       2 | Epic Cat Jump    | www.miaowtube/watch2      | 2025-05-27   |
+----------+---------+------------------+---------------------------+--------------+
2 rows in set (0.00 sec)
```

## Combining tables with JOIN

To combine related data from multiple tables use `JOIN`. `JOIN` appears immediately after `FROM` and defines how rows from each table match. In this example we join `videos` to `users` on the shared `user_id`, then sort and limit the result:

```sql theme={null}
mysql-> SELECT *
    -> FROM videos
    -> JOIN users ON videos.user_id = users.user_id
    -> ORDER BY videos.upload_date DESC
    -> LIMIT 2;
+----------+---------+------------------+---------------------------+--------------+---------+----------+------------------+
| video_id | user_id | title            | link                      | upload_date  | user_id | username | email            |
+----------+---------+------------------+---------------------------+--------------+---------+----------+------------------+
|        3 |       1 | Cat vs Curtain   | www.miaowtube/watch3      | 2025-05-29   |       1 | fluffy   | fluffy@email.com |
|        2 |       2 | Epic Cat Jump    | www.miaowtube/watch2      | 2025-05-27   |       2 | paws     | paws@email.com   |
+----------+---------+------------------+---------------------------+--------------+---------+----------+------------------+
2 rows in set (0.00 sec)
```

When columns appear in more than one table, use explicit table qualification (dot notation) like `videos.user_id` and `users.user_id` to avoid ambiguity.

> **lightbulb** Clause order matters: `FROM` (and `JOIN`) determine which tables are involved, `WHERE` filters rows, `ORDER BY` sorts them, and `LIMIT` trims the final result set. Writing queries in the correct sequence helps the database optimize execution.

## Typical clause order and purpose

Use the table below as a quick reference for the common SELECT clause sequence and what each clause does.

| Clause      | Purpose                                | Example                                                    |
| ----------- | -------------------------------------- | ---------------------------------------------------------- |
| FROM / JOIN | Choose tables and combine related rows | `FROM videos JOIN users ON videos.user_id = users.user_id` |
| WHERE       | Filter rows based on conditions        | `WHERE upload_date = '2025-05-27'`                         |
| ORDER BY    | Sort the filtered rows                 | `ORDER BY upload_date DESC`                                |
| LIMIT       | Restrict how many rows are returned    | `LIMIT 10`                                                 |

These patterns underpin searching, filtering, sorting feeds, and generating recommendations. As data scales, even well-formed queries can slow down — that’s when indexes become essential for performance. In the next part of this lesson we’ll cover what a database index is, how it speeds up queries, and when to add one.

## Links and references

* [MySQL Documentation](https://dev.mysql.com/doc/)
* [SQL JOINs Explained](https://www.w3schools.com/sql/sql_join.asp)
* [Introduction to Indexes](https://www.postgresql.org/docs/current/indexes.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/database-fundamentals/module/5edfd17e-97e6-4a23-9c91-4dee1d8a3024/lesson/0f69efca-7b97-4f8c-b3ce-8f750f565b37)
