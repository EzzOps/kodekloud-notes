# connect as user 'bob'
mysql -u bob -p
```

Create and select a database

* A database in MySQL is a logical namespace that holds tables and other objects. Create a database, list available databases, and switch to the new one:

```sql theme={null}
CREATE DATABASE miaowtube;
SHOW DATABASES;
USE miaowtube;
SELECT DATABASE();
```

* `CREATE DATABASE miaowtube;` creates an empty database named `miaowtube`.
* `SHOW DATABASES;` lists all databases on the server.
* `USE miaowtube;` selects the database for subsequent commands.
* `SELECT DATABASE();` confirms the current database.

Why create `users` first?

* The `videos` table references `users.user_id` with a foreign key. MySQL requires the referenced table to exist when adding a foreign key (unless both are created in a single statement where supported). Creating `users` first avoids needing an extra `ALTER TABLE` later.

<Frame>
  <img alt="The image shows an entity-relationship diagram with tables for &#x22;Videos&#x22; and &#x22;Users,&#x22; illustrating database structure alongside a person presenting." />
</Frame>

Table design decisions (from the ERD)

* Use `INT AUTO_INCREMENT PRIMARY KEY` for `user_id` and `video_id` so the database assigns unique IDs automatically.
* `VARCHAR(100)` for `username` and `title`.
* `VARCHAR(500)` for `link` to safely store longer URLs.
* `VARCHAR(255)` for `email` (common, index-friendly choice).
* `DATE` for `upload_date` (format YYYY-MM-DD).
* Use `InnoDB` engine for foreign key support.
* `ON DELETE CASCADE` on the foreign key ensures referential integrity by removing related videos if a user is deleted (only use this if that is the desired behavior).

Create the database and both tables

```sql theme={null}
CREATE DATABASE miaowtube;
USE miaowtube;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE videos (
    video_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(100) NOT NULL,
    link VARCHAR(500) NOT NULL,
    upload_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;
```

Key SQL elements explained

* `INT AUTO_INCREMENT PRIMARY KEY` — auto-incrementing integer primary key.
* `VARCHAR(n)` — variable-length string up to n characters.
* `NOT NULL` — value is required in that column.
* `DATE` — stores `YYYY-MM-DD`.
* `FOREIGN KEY (user_id) REFERENCES users(user_id)` — enforces that every `user_id` in `videos` exists in `users`.
* `ON DELETE CASCADE` — deletes dependent `videos` rows when the referenced `users` row is removed.
* `ENGINE=InnoDB` — required for foreign key enforcement in MySQL.

CRUD quick-reference table

| CRUD operation | SQL statement(s) | Example                                                                    |
| -------------- | ---------------- | -------------------------------------------------------------------------- |
| Create         | `INSERT`         | `INSERT INTO users (username, email) VALUES ('cody', 'cody@example.com');` |
| Read           | `SELECT`         | `SELECT * FROM videos WHERE user_id = 1;`                                  |
| Update         | `UPDATE`         | `UPDATE users SET email = 'new@addr.com' WHERE user_id = 1;`               |
| Delete         | `DELETE`         | `DELETE FROM videos WHERE video_id = 10;`                                  |

Column types and rationale

| Column                | Type                 | Reason                                           |
| --------------------- | -------------------- | ------------------------------------------------ |
| `user_id`, `video_id` | `INT AUTO_INCREMENT` | Simple numeric PKs, efficient joins and indexing |
| `username`, `title`   | `VARCHAR(100)`       | Fixed upper bound for user-friendly text         |
| `email`               | `VARCHAR(255)`       | Common practice for email length & indexes       |
| `link`                | `VARCHAR(500)`       | Accommodate long URLs                            |
| `upload_date`         | `DATE`               | Stores date without time portion                 |

Tips for using the MySQL client

* If you make a typo while entering a long statement, press Ctrl-C to cancel the current input.
* Alternatively, finish the statement with a semicolon, then use your shell history (up-arrow) to retrieve and edit previous commands.
* Use `DESCRIBE table_name;` or `SHOW CREATE TABLE table_name;` to inspect table definitions.

<Callout icon="lightbulb">
  If you need to add a foreign key after creating both tables, use ALTER TABLE to add the constraint. However, creating the referenced table first avoids extra ALTER steps.
</Callout>

Links and references

* MySQL Documentation: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
* [Kubernetes Documentation](https://kubernetes.io/docs/) (for related deployment topics)
* KodeKloud Playground (use the playground for interactive MySQL practice)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/database-fundamentals/module/aab35c82-07d0-4b02-90e5-68b6bb04a242/lesson/fe0c1ef8-042e-4cce-a544-e1000c103734" />
</CardGroup>


# Tables Keys and ERDs

Source: https://notes.kodekloud.com/docs/Database-Fundamentals/Relational-Databases/Tables-Keys-and-ERDs/page

Explains moving from flat files to relational databases using tables, primary and foreign keys, and ERDs to reduce redundancy and maintain data integrity.

Earlier we cleaned up Kodi's vet records by adding column headings, fixing data types, and improving structure. Structure alone, however, doesn't solve every problem.

Kodi and her friends built a video-sharing site called MeowTube and started tracking uploads in a single spreadsheet. At first that flat-file approach was fine — but as the site grows, the spreadsheet's limitations become obvious.

<Frame>
  <img alt="The image shows a screenshot of a website interface with a list of video titles, usernames, emails, links, and upload dates, alongside illustrations of cartoon cats and a person speaking or presenting." />
</Frame>

Each row currently stores: video title, uploader username, email, link, and upload date. That design leads to repeated user details. For example, rows 1 and 3 both belong to Fluffy and duplicate his username and email. This repetition is called data redundancy.

Problems that arise from redundancy:

* Updating a user's email requires changing every row that contains it.
* Missed updates produce inconsistent records (stale or conflicting email addresses).
* Duplicating private contact information across many rows increases exposure risk.

With a few records the work is manual but manageable. With thousands of rows it becomes error-prone and insecure. Kodi and the team need a better design that separates personal data from video records, enforces consistency, and preserves relationships between entities. In this article we will:

* explain the limitations of a flat-file approach,
* introduce primary and foreign keys for linking data, and
* interpret a simple Entity Relationship Diagram (ERD).

<Frame>
  <img alt="The image shows a person in a KodeKloud shirt standing next to a presentation slide with a cartoon character. The slide lists three topics: limitations of flat file databases, primary and foreign keys, and interpreting an Entity Relationship Diagram." />
</Frame>

What Kodi has is a flat file: one unsplit table containing all data. Flat files are simple and fast to set up for small datasets, but they struggle with consistency, security, and scalability. A better option for MeowTube is a relational database.

Relational approach overview:

* Split related data into separate tables (for example, a `videos` table and a `users` table).
* Replace repeated user fields in `videos` with a reference to the `users` table.

This raises a question: how do we link a video to its uploader without repeating user details? The answer is primary keys and foreign keys.

Primary keys (PK)

* Every table should have a primary key.
* PK values must be unique for every row and cannot be NULL.
* A common PK is a simple auto-incrementing integer (e.g., `user_id`, `video_id`).
* Composite primary keys (multiple columns) are possible but out of scope here.

Example: add `video_id` to the `videos` table and `user_id` to the `users` table. Then store `user_id` in `videos` instead of username/email.

What is a foreign key (FK)?
A foreign key is a field (or set of fields) in one table that references a primary key in another table. In our example, the `user_id` column in `videos` is a foreign key pointing to `users.user_id`.

<Frame>
  <img alt="The image shows a database schema diagram with tables for video records and user information, featuring video details and user data, alongside a person wearing a &#x22;KodeKloud&#x22; t-shirt." />
</Frame>

Key points about foreign keys:

* A foreign key references the primary key of another table.
* It creates and enforces relationships between tables (e.g., which user uploaded which video).
* The FK value should match a value in the referenced table’s PK (unless the FK is allowed to be `NULL`).
* Foreign keys help maintain referential integrity: you generally cannot create a `videos` row that points to a non-existent `users` record.

Benefits in practice:

* Store personal details once in `users`; `videos` contains only `user_id`.
* Updating a user’s email is a single change in `users`, and all their video records remain correct.
* Data duplication is reduced, making the database safer and easier to maintain.

ERDs — visualizing structure and relationships
As you add tables, an Entity Relationship Diagram (ERD) helps you see how entities connect. In an ERD:

* Each box (entity) represents a table.
* Attributes (fields) are listed inside entities.
  * The primary key is typically listed first and marked `PK`.
  * Foreign keys are listed below and marked `FK`.
* Lines between entities show relationships; symbols at line ends indicate cardinality.

Crow's Foot notation (common ERD symbols) describes cardinality:

| Symbol meaning                | Common description |
| ----------------------------- | ------------------ |
| Single line with vertical bar | exactly one        |
| Crow's Foot                   | many               |
| Circle + vertical bar         | zero or one        |
| Circle + crow's foot          | zero or many       |
| Vertical bar + crow's foot    | one or many        |

In our MeowTube example:

* Each video is uploaded by exactly one user (one side).
* Each user can upload zero or many videos (many side with a crow's foot).
* This is a one-to-many relationship.

Inside entity boxes you may also see data types (e.g., `integer` for IDs, `date` for `upload_date`, `text` for `title` or `email`). Simple ERDs show entity-to-entity lines; more detailed diagrams can show the specific attribute-to-attribute links.

Quick comparison table: primary key vs foreign key

| Key type         |                                                   Purpose | Example                                      |
| ---------------- | --------------------------------------------------------: | -------------------------------------------- |
| Primary Key (PK) |                Uniquely identifies rows in the same table | `user_id` in the `users` table               |
| Foreign Key (FK) | References a PK in another table to create a relationship | `videos.user_id` referencing `users.user_id` |

Pop quiz time.

Which of the following statements is true?

A. Flat files use foreign keys to reduce data redundancy.\
B. A foreign key links a record in one table to a record in another.\
C. Crow's Foot notation is used to label column data types.

Pause for a moment to think.

The correct answer is B. A foreign key links a record in one table to a record in another — that is how relational databases avoid repeating data while preserving relationships.

<Frame>
  <img alt="The image shows a question about foreign keys, stating that a foreign key links a record in one table to a record in another. There are two tables labeled &#x22;Table 01&#x22; and &#x22;Table 02,&#x22; with a foreign key connecting them, and a person wearing a &#x22;KodeKloud&#x22; t-shirt is standing beside the text." />
</Frame>

Clarifications on the incorrect options:

* Flat files generally do not enforce primary or foreign key constraints; without these constraints, duplication and inconsistency are common.
* Crow's Foot notation indicates relationship cardinality between entities, not column data types.

Recap

* Flat-file databases keep all data in a single table, which can cause redundancy, inconsistency, and security issues.
* Relational databases split data into linked tables to improve consistency, security, and scalability.
* A primary key uniquely identifies records in a table.
* A foreign key connects one table to another by referencing a primary key.
* ERDs visually represent entities and relationships; Crow's Foot shows cardinality (one-to-one, one-to-many, many-to-many).

<Callout icon="lightbulb">
  Using primary and foreign keys reduces redundancy and makes updates safer: change user details once in the users table, and all related rows remain correct.
</Callout>

Next up, we'll look at how databases perform operations: how they store, query, and manipulate data using SQL and other database tools.

Further reading and references

* [Relational Database Concepts — Wikipedia](https://en.wikipedia.org/wiki/Relational_database)
* [Entity–Relationship Model — Wikipedia](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model)
* [Crow's Foot Notation Guide (ERD)](https://vertabelo.com/blog/crows-foot-notation-explained/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/database-fundamentals/module/aab35c82-07d0-4b02-90e5-68b6bb04a242/lesson/5b730c92-ff78-4489-a5af-58e1e5f81374" />
</CardGroup>
