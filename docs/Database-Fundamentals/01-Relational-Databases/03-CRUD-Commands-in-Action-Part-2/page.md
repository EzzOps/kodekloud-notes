# CRUD Commands in Action Part 2

Source: https://notes.kodekloud.com/docs/Database-Fundamentals/Relational-Databases/CRUD-Commands-in-Action-Part-2/page

Demonstrates MySQL foreign keys, ON DELETE/ON UPDATE behaviors, cascading actions, and runnable CRUD examples for creating, querying, updating, and deleting related tables

This lesson continues the CRUD walkthrough by demonstrating how foreign keys create relationships between tables in MySQL, how cascading actions work, and concrete CREATE / INSERT / SELECT / UPDATE / DELETE examples you can run locally.

Quick summary: use primary keys to uniquely identify rows, foreign keys to enforce relationships between tables, and `ON DELETE`/`ON UPDATE` actions to control what happens to dependent rows when a parent row changes.

## One-to-many relationships (user → videos)

A one-to-many relationship exists when a single row in a parent table (users) can be referenced by many rows in a child table (videos). For example, a `user_id` is unique in `users` but may appear multiple times in `videos`.

Without a foreign key constraint, MySQL will accept any integer in the `user_id` column of `videos`, including values that do not exist in `users`. A foreign key enforces referential integrity so all referenced values in the child table must exist in the parent table.

If you wanted:

* a one-to-one relationship — add `UNIQUE` to the foreign key column in the child table;
* a many-to-many relationship — create a join (linking) table.

## Common foreign key actions (ON DELETE / ON UPDATE)

| Action                             | Description                                                                                 | When to use                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `ON DELETE CASCADE`                | When a parent row is deleted, all child rows referencing it are also deleted automatically. | Use when child rows are meaningless without the parent (e.g., videos that must belong to a user).             |
| `ON DELETE SET NULL`               | When a parent row is deleted, the child foreign key column is set to `NULL`.                | Use when you want to preserve the child row but remove its parent reference. The FK column must allow `NULL`. |
| `RESTRICT` / `NO ACTION` (default) | Prevents deleting the parent if child rows exist.                                           | Use when you want to avoid accidental deletion that would orphan child rows.                                  |

> **lightbulb** Use `ON DELETE CASCADE` when the child table (e.g., `videos`) should not exist without the parent (e.g., `users`). Use `ON DELETE SET NULL` when you want to keep the child row but remove its parent reference.

## Create a database and two tables (example with `ON DELETE CASCADE`)

Run these statements to create the demo database and tables. This example uses `ON DELETE CASCADE` so deleting a user will delete their videos automatically.

```sql theme={null}
CREATE DATABASE miaowtube;
SHOW DATABASES;
USE miaowtube;
SELECT DATABASE();

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE videos (
    video_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(100) NOT NULL,
    link VARCHAR(255) NOT NULL,
    upload_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
```

If you prefer to keep video rows but remove the user reference when the user is deleted, use `ON DELETE SET NULL` and allow the `user_id` column to be nullable:

```sql theme={null}
CREATE TABLE videos (
    video_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(100) NOT NULL,
    link VARCHAR(255) NOT NULL,
    upload_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE SET NULL
);
```

Note: `ON DELETE SET NULL` requires the foreign key column to accept `NULL`, so `user_id` should not be declared `NOT NULL`.

## Inspecting table schema with DESCRIBE

Use `DESCRIBE` (or `SHOW COLUMNS FROM`) to check field names, types, nullability, keys, and auto-increment behavior.

Example DESCRIBE output (for the CASCADE version):

```mysql theme={null}
mysql> DESCRIBE users;
+----------+---------------+------+-----+---------+----------------+
| Field    | Type          | Null | Key | Default | Extra          |
+----------+---------------+------+-----+---------+----------------+
| user_id  | int           | NO   | PRI | NULL    | auto_increment |
| username | varchar(100)  | NO   |     | NULL    |                |
| email    | varchar(255)  | NO   |     | NULL    |                |
+----------+---------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)

mysql> DESCRIBE videos;
+-----------+----------------+------+-----+---------+----------------+
| Field     | Type           | Null | Key | Default | Extra          |
+-----------+----------------+------+-----+---------+----------------+
| video_id  | int            | NO   | PRI | NULL    | auto_increment |
| user_id   | int            | YES  | MUL | NULL    |                |
| title     | varchar(100)   | NO   |     | NULL    |                |
| link      | varchar(255)   | NO   |     | NULL    |                |
| upload_date| date          | YES  |     | NULL    |                |
+-----------+----------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)
```

* `PRI` = Primary Key
* `MUL` = Multiple occurrences allowed (indexed column, typical for foreign keys)
* `YES` under `Null` means the column accepts `NULL`, which is required for `ON DELETE SET NULL`.

## Insert demo data (Create)

Insert users (auto-increment handles `user_id`):

```sql theme={null}
INSERT INTO users (username, email)
VALUES
    ('fluffy', 'fluffy@email.com'),
    ('paws', 'paws@email.com');
```

Output:

```mysql theme={null}
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

Insert videos with valid `user_id` values that reference existing users:

```sql theme={null}
INSERT INTO videos (user_id, title, link, upload_date)
VALUES
    (1, 'Cat Skateboard', 'www.miaowtube/watch1', '2023-05-25'),
    (1, 'Cat vs Curtain',  'www.miaowtube/watch3', '2023-05-29'),
    (2, 'Epic Cat Jump',   'www.miaowtube/watch2', '2023-05-27');
```

## Read data (SELECT)

Show all videos:

```sql theme={null}
SELECT * FROM videos;
```

Example result:

```mysql theme={null}
+----------+---------+------------------+-----------------------+-------------+
| video_id | user_id | title            | link                  | upload_date |
+----------+---------+------------------+-----------------------+-------------+
|        1 |       1 | Cat Skateboard   | www.miaowtube/watch1  | 2023-05-25  |
|        2 |       1 | Cat vs Curtain   | www.miaowtube/watch3  | 2023-05-29  |
|        3 |       2 | Epic Cat Jump    | www.miaowtube/watch2  | 2023-05-27  |
+----------+---------+------------------+-----------------------+-------------+
3 rows in set (0.00 sec)
```

If you only need video titles:

```sql theme={null}
SELECT title FROM videos;
```

## Update data (UPDATE)

Update a single row by matching the primary key in the `WHERE` clause to avoid accidental bulk updates:

```sql theme={null}
UPDATE videos
SET title = 'Flufferson on Skateboard'
WHERE video_id = 1;

SELECT * FROM videos;
```

Expected feedback:

```mysql theme={null}
Query OK, 1 row affected (0.00 sec)
```

Updated table snapshot:

```mysql theme={null}
+----------+---------+-----------------------------+-----------------------+-------------+
| video_id | user_id | title                       | link                  | upload_date |
+----------+---------+-----------------------------+-----------------------+-------------+
|        1 |       1 | Flufferson on Skateboard    | www.miaowtube/watch1  | 2023-05-25  |
|        2 |       1 | Cat vs Curtain              | www.miaowtube/watch3  | 2023-05-29  |
|        3 |       2 | Epic Cat Jump               | www.miaowtube/watch2  | 2023-05-27  |
+----------+---------+-----------------------------+-----------------------+-------------+
```

## Delete data (DELETE)

Delete a specific video:

```sql theme={null}
DELETE FROM videos
WHERE video_id = 2;

SELECT * FROM videos;
```

Example result after deletion:

```mysql theme={null}
Query OK, 1 row affected (0.00 sec)

+----------+---------+-------------------------------+-----------------------+-------------+
| video_id | user_id | title                         | link                  | upload_date |
+----------+---------+-------------------------------+-----------------------+-------------+
|        1 |       1 | Flufferson on Skateboard      | www.miaowtube/watch1  | 2023-05-25  |
|        3 |       2 | Epic Cat Jump                 | www.miaowtube/watch2  | 2023-05-27  |
+----------+---------+-------------------------------+-----------------------+-------------+
```

## Demonstrating cascade behavior

If `videos` was created with `ON DELETE CASCADE` on `user_id`, deleting `users.user_id = 1` will remove all videos referencing `user_id = 1` automatically:

```sql theme={null}
DELETE FROM users
WHERE user_id = 1;

SELECT * FROM videos;
```

Example cascading delete result:

```mysql theme={null}
Query OK, 1 row affected (0.00 sec)

+----------+---------+------------------+-----------------------+-------------+
| video_id | user_id | title            | link                  | upload_date |
+----------+---------+------------------+-----------------------+-------------+
|        3 |       2 | Epic Cat Jump    | www.miaowtube/watch2  | 2023-05-27  |
+----------+---------+------------------+-----------------------+-------------+
1 row in set (0.00 sec)
```

You can see videos that belonged to user 1 were removed as part of the cascading delete.

## CRUD and SQL quick reference

| CRUD Action | SQL Command      | Purpose                 |
| ----------- | ---------------- | ----------------------- |
| Create      | `INSERT INTO`    | Add new records         |
| Read        | `SELECT`         | Retrieve records        |
| Update      | `UPDATE ... SET` | Modify existing records |
| Delete      | `DELETE FROM`    | Remove records          |

Common misconception quiz (answer below):
A. CREATE TABLE is the SQL command used to create new records.\
B. A primary key can appear multiple times in the same table.\
C. A foreign key ensures data in one table matches values in another.\
D. INSERT is used to read information from a table.

Correct answer: C.

Why:

* A is incorrect — `CREATE TABLE` makes the table structure; `INSERT` adds records.
* B is incorrect — primary keys must be unique in a table.
* D is incorrect — `SELECT` reads or retrieves data; `INSERT` writes data.

## Recap

* Primary keys uniquely identify rows.
* Foreign keys enforce relationships and referential integrity.
* Choose `ON DELETE` actions (`CASCADE`, `SET NULL`, or default `RESTRICT`) based on application logic.
* Use `DESCRIBE` to inspect schema and ensure columns match the intended constraints.
* Practice Create, Read, Update, Delete operations to solidify understanding.

## Next steps

Try creating a `comments` table and perform CRUD operations on it. Experiment with different `ON DELETE` actions and observe how `DESCRIBE` changes. If you want to learn alternatives, explore NoSQL document stores such as MongoDB for non-relational approaches.

## Links and references

* [MySQL Reference Manual - Foreign Key Constraints](https://dev.mysql.com/doc/refman/en/innodb-foreign-key-constraints.html)
* [SQL Language Reference (SELECT, INSERT, UPDATE, DELETE)](https://dev.mysql.com/doc/refman/en/)

- [Watch Video](https://learn.kodekloud.com/user/courses/database-fundamentals/module/aab35c82-07d0-4b02-90e5-68b6bb04a242/lesson/b62e73c8-6d86-4d4c-8db7-7f8beae4d6ea)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/database-fundamentals/module/aab35c82-07d0-4b02-90e5-68b6bb04a242/lesson/066ff8ab-a4d0-4346-bda4-d0e12bdcfd5e)
