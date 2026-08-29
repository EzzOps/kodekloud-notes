# SQL vs NoSQL

Source: https://notes.kodekloud.com/docs/System-Design-For-Beginners/Data-Reads-and-Writes/SQL-vs-NoSQL/page

Comparing SQL and NoSQL databases, their trade offs, use cases, and guidance for choosing between relational and schema-less stores with examples and polyglot persistence recommendations

You've identified the key data you need to store. The next decision is whether to use an SQL (relational) or a NoSQL (schema-less) database. The primary deciding factor is the shape of your data and the queries you need to run:

* Structured, consistent schemas → SQL is usually a better fit.
* Unstructured or highly variable records → NoSQL often works better.

Below we walk through the differences, trade-offs, and practical guidance using a photo-sharing app as an example.

## Why choose SQL (relational databases)?

SQL databases enforce a fixed schema and store data in tables (rows and columns). This strong structure makes it easy to model entities and relationships, for example: users, photos, likes, and follows. Modern relational systems like Postgres and MySQL also support semi-structured data (JSON/JSONB columns), adding flexibility where needed.

SQL makes relational queries straightforward. For example, to show all photos posted by people Alan follows, you join the `follows` table to the `photos` table and filter by the relevant user:

<Frame>
  <img alt="The image shows a diagram of SQL data relationships, featuring tables for &#x22;Follows&#x22; and &#x22;Photos&#x22; combined through a join to show which photos are associated with users that &#x22;alan&#x22; follows." />
</Frame>

SQL databases also provide transactions and referential integrity. Transactions let you group multiple operations so they either all succeed or all fail together. Referential integrity (foreign keys, cascading deletes) helps ensure consistent relationships between rows. For example, when Alan deletes a photo, you can wrap deletion of the photo plus its likes and comments in a single transaction so no orphaned rows remain.

<Frame>
  <img alt="The image illustrates a SQL database schema showing the relationship between tables for photos, likes, and comments, highlighting the transactional deletion of a photo." />
</Frame>

<Callout icon="lightbulb">
  ACID stands for Atomicity, Consistency, Isolation, and Durability — properties that help ensure reliable transactions in relational databases.
</Callout>

Common relational database examples:

* Postgres ([postgresql.org](https://www.postgresql.org/))
* MySQL ([mysql.com](https://www.mysql.com/))

Use cases where SQL commonly excels:

* Strongly relational data (users, orders, relationships)
* Complex joins and transactional workflows
* Data that benefits from enforced schema and constraints

## Why choose NoSQL?

NoSQL databases relax the fixed schema requirement. Each record (document) can have a different shape, which makes NoSQL a natural fit for heterogeneous or rapidly evolving data models such as event logs, analytics events, or user preferences.

NoSQL systems are often designed for horizontal scalability and high throughput across many machines. Common NoSQL examples:

* MongoDB ([mongodb.com](https://www.mongodb.com/)) — document store
* DynamoDB ([aws.amazon.com/dynamodb/](https://aws.amazon.com/dynamodb/)) — managed key-value/document store
* Elasticsearch ([elastic.co](https://www.elastic.co/elasticsearch/)) — search and analytics engine, often used as a document store for search use cases

When data shape varies by record or you need extremely high write/read throughput with flexible schema, NoSQL is a good choice.

## Example: deciding for a photo-sharing app

In our photo app, most data is structured and relational: photos, users, likes, follows. That clearly points toward a relational database for the core domain — for example, Postgres.

Conceptual example of the `photos` table:

```sql theme={null}
PHOTOS
  id
  posted_by
  caption
  upload_time
  image_link
```

User preferences, on the other hand, can vary per user and change frequently. They are a good candidate for a NoSQL store:

```yaml theme={null}
Alan's preferences:
  theme: dark
  notifications: on
  language: en
```

In real systems, it's common to use both types of databases (polyglot persistence):

* SQL (e.g., Postgres) for structured, relational data: users, photos, likes, follows, orders.
* NoSQL (e.g., MongoDB, DynamoDB) for flexible or high-volume data: preferences, clickstreams, event logs, search indexes.

<Frame>
  <img alt="The image contrasts SQL and NoSQL databases, highlighting their features and uses PostgreSQL for structured data and MongoDB for flexible data handling. It suggests real systems use both types for different data needs." />
</Frame>

## Quick comparison (SQL vs NoSQL)

| Characteristic |                                        SQL (Relational) | NoSQL (Schema-less)                                             |
| -------------- | ------------------------------------------------------: | --------------------------------------------------------------- |
| Schema         |                             Fixed schema, strong typing | Dynamic schema, flexible document shapes                        |
| Relationships  |                       First-class (joins, foreign keys) | Usually embedded or referenced, joins limited                   |
| Transactions   |                                     Strong ACID support | Varies by product; some support limited transactions            |
| Scalability    |         Vertical scaling typical; some support sharding | Designed for horizontal scaling across nodes                    |
| Use cases      | Payments, relational apps, consistency-critical systems | Event stores, logs, flexible preferences, high-scale read/write |
| Examples       |                                     `Postgres`, `MySQL` | `MongoDB`, `DynamoDB`, `Elasticsearch`                          |

## Practical guidance: when to use which

* If your domain model has many relationships and requires consistency: start with SQL.
* If your data is highly varied or you need to ingest massive volumes of log-like events: NoSQL is often better.
* If you’re unsure: starting with SQL is a safe choice for most business applications because it covers a wide range of cases and makes it easier to reason about correctness.
* For production-scale systems, consider polyglot persistence: use the best tool for each data type and access pattern.

Common application mappings:

* Build a user feed with relational joins and index-backed queries → query Postgres.
* Load per-user preferences or feature flags stored as flexible JSON → query MongoDB or DynamoDB.
* Full-text search or analytics over large text fields → use Elasticsearch or a search-optimized store.

## Final note

A database is software that runs on standard servers with CPU, RAM, and disk — not special hardware. Choosing between Postgres, MongoDB, DynamoDB, or Elasticsearch is about data model, query patterns, and operational trade-offs rather than special-purpose machines.

## Links and references

* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [MySQL](https://www.mysql.com/)
* [MongoDB Documentation](https://www.mongodb.com/docs/)
* [DynamoDB](https://aws.amazon.com/dynamodb/)
* [Elasticsearch](https://www.elastic.co/elasticsearch/)
* [ACID (Wikipedia)](https://en.wikipedia.org/wiki/ACID_\(database_systems\))

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/system-design-for-beginners/module/3ee9409c-c2ff-4102-9a76-af9840dc6e23/lesson/2b5a1335-edfa-4cfb-aba6-6d1a19668588" />
</CardGroup>
