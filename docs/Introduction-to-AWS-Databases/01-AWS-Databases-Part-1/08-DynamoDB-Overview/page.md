# DynamoDB Overview

Source: https://notes.kodekloud.com/docs/Introduction-to-AWS-Databases/AWS-Databases-Part-1/DynamoDB-Overview/page

High-level overview of Amazon DynamoDB features, data model, primary keys, scalability, ACID transactions, PartiQL queries, and AWS integrations for building scalable NoSQL applications.

This lesson gives a high-level overview of Amazon DynamoDB, AWS's fully managed NoSQL database service. Expect DynamoDB to appear frequently on AWS certification exams (for example, the AWS Certified Developer — Associate). Before diving into DynamoDB specifics, it's useful to briefly review NoSQL concepts.

NoSQL databases trade rigid schemas for flexible data models and horizontal scalability. They are optimized for large volumes of unstructured or semi-structured data and different access patterns than relational databases.

NoSQL database types

| Data model          | Typical use case                 | Short description                                                                   |
| ------------------- | -------------------------------- | ----------------------------------------------------------------------------------- |
| Key-value store     | Session, cache, user preferences | Stores a unique key mapped to an opaque value. Fast lookups by key.                 |
| Document store      | JSON documents for apps          | Stores structured documents (JSON, XML) that can contain nested objects and arrays. |
| Column-family store | Time-series, analytics           | Rows and columns with flexible schemas — different rows can have different columns. |
| Graph database      | Social networks, recommendations | Models complex relationships using nodes and edges with properties.                 |

<Frame>
  <img alt="An infographic titled &#x22;NoSQL&#x22; showing four database types — Key-Value Stores, Document Stores, Column-Family Stores, and Graph Databases — each represented by a colored icon and label. The four panels are arranged side by side across the image." />
</Frame>

What is DynamoDB?

DynamoDB is AWS's managed NoSQL database designed for low-latency, predictable performance at any scale. It removes most operational overhead (provisioning, patching, replication, hardware management) while providing built-in high availability and durability.

A typical architecture places your application between end users and DynamoDB: the application issues reads and writes, and DynamoDB stores the application’s state, sessions, configuration, or business data.

<Frame>
  <img alt="A simple architecture diagram titled &#x22;DynamoDB&#x22; showing End Users on the left, an Application (laptop) in the center, and a DynamoDB database icon on the right. Bidirectional arrows indicate data flow between users and the application and between the application and the database." />
</Frame>

Key benefits and features

* Seamless scalability: DynamoDB scales automatically to handle growing traffic and data volumes.
* Predictable low latency: single-digit millisecond read/write latencies for typical use cases.
* Flexible data model: store items with attributes (including nested documents) without a fixed schema.
* Pay-as-you-go pricing: you pay for throughput and storage consumed; choose on-demand or provisioned capacity.

<Frame>
  <img alt="A DynamoDB slide showing four colored tiles. Each tile is labeled and iconified: Scalability, High Performance, Flexible Data Model, and Cost‑Effectiveness." />
</Frame>

Additional capabilities

* High availability & durability: data is replicated across multiple Availability Zones.
* Streams: DynamoDB Streams capture item-level changes in time order for change processing or replication.
* AWS integrations: works well with AWS Lambda, Amazon S3, Amazon Redshift, and many other services.

<Frame>
  <img alt="An infographic slide featuring a central DynamoDB icon surrounded by colorful icons and labels. The surrounding text lists features like Stream Integration, Integrated with AWS Ecosystem, Performance at Scale, Fully Managed, Seamless Scalability, and High Availability and Durability." />
</Frame>

ACID transactions

DynamoDB supports ACID transactions for multi-item, multi-table operations. When you need transactional guarantees, DynamoDB provides:

* Atomicity — all operations in a transaction succeed or none do.
* Consistency — transactions maintain defined constraints and consistency rules.
* Isolation — in-flight transaction changes are not visible until commit.
* Durability — committed transactions persist despite failures.

> **lightbulb** Use DynamoDB transactions when you require strong consistency across multiple items (for example, transferring balances between accounts). Transactions incur additional cost and throughput considerations, so use them only when necessary.

<Frame>
  <img alt="A slide titled &#x22;DynamoDB Transactions – ACID Properties&#x22; showing four colored panels labeled Atomicity, Consistency, Isolation, and Durability with corresponding icons beneath each. The slide appears to illustrate the ACID properties of DynamoDB transactions." />
</Frame>

DynamoDB data model: tables, items, attributes

* Table: a container for items (analogous to a table in other databases).
* Item: a single record in a table (e.g., a user or an order).
* Attribute: a key-value pair on an item. Attributes can be scalars (string, number, binary) or complex (lists, maps).

Example item (JSON):

```json theme={null}
{
  "EmployeeID": "E67890",
  "FirstName": "Jane",
  "LastName": "Smith",
  "Email": "jane.smith@example.com",
  "Position": "Product Manager",
  "Department": "Product",
  "HireDate": "2019-03-15",
  "ContactInfo": {
    "PhoneNumber": "555-1234",
    "Address": "123 Main St, Anytown, USA"
  }
}
```

<Frame>
  <img alt="A slide titled &#x22;DynamoDB&#x22; showing three stylized icons labeled &#x22;Table&#x22;, &#x22;Items&#x22;, and &#x22;Attribute&#x22; (each in a different color) representing database concepts." />
</Frame>

Naming rules and limits

* Names must be UTF-8 encoded and are case-sensitive.
* Table and index names: between 3 and 255 characters.
* Attribute names: at least 1 character; the attribute name size can be large (up to implementation limits).

Primary key overview

Every item must have a primary key that uniquely identifies it. Design the primary key to match your application's access patterns.

Two primary key types:

1. Partition key (simple primary key)
   * A single attribute.
   * Each item must have a unique partition key value in the table.

2. Composite primary key (partition key + sort key)
   * The partition key groups items; the sort key orders items within the partition.
   * The pair (partition key, sort key) must be unique. The same partition key can appear in multiple items if the sort key differs.

> **warning** Primary keys are immutable: you cannot change an item's primary key values. To "change" a primary key you must create a new item and delete the old one.

<Frame>
  <img alt="A presentation slide explaining primary/partition keys using a sample employee table where &#x22;employee_id&#x22; is marked as the partition key and &#x22;name&#x22;, &#x22;email&#x22;, and &#x22;salary&#x22; are shown as attributes. The table highlights duplicate employee_id values to illustrate the uniqueness requirement." />
</Frame>

Composite primary key example

Composite keys help model one-to-many or hierarchical relationships in a single table. Example: a Reviews table where a user can leave multiple reviews for different products.

* Partition key: `user_id`
* Sort key: `product_id`

This allows multiple reviews per user (same `user_id`, different `product_id`) while preventing duplicate `user_id`/`product_id` pairs.

<Frame>
  <img alt="A slide illustrating that a primary key is a combination of a partition key and sort key. It shows a sample table with columns user_id (partition key), product_id (sort key) and attributes rating and review." />
</Frame>

Querying with PartiQL

DynamoDB supports PartiQL, an SQL-compatible query language that simplifies querying and modifying items using familiar SQL syntax.

Example PartiQL query:

```sql theme={null}
SELECT * FROM reviews
WHERE user_id = 'sam@gmail.com' AND product_id = '99999';
```

PartiQL is convenient for quick reads and for people coming from relational databases, but keep in mind that DynamoDB still enforces primary key access patterns and scalability characteristics.

Summary

* NoSQL databases (including DynamoDB) provide flexible schemas and horizontal scalability for large datasets.
* DynamoDB is a fully managed, high-performance NoSQL service with automatic scaling, high availability, and integration across the AWS ecosystem.
* Data model: tables → items → attributes (attributes can be nested).
* Primary keys uniquely identify items: choose a single partition key or a composite key (partition + sort) based on your query patterns.
* DynamoDB supports ACID transactions and PartiQL for SQL-like queries.

<Frame>
  <img alt="A presentation summary slide that explains data is stored in tables with each item made of attributes and a primary key identifies items uniquely. It also lists two primary key options: partition key alone or partition key plus sort key." />
</Frame>

Further reading and references

* [DynamoDB Developer Guide — PartiQL reference](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html)
* [AWS Lambda documentation](https://learn.kodekloud.com/user/courses/aws-lambda)
* [Amazon S3 course](https://learn.kodekloud.com/user/courses/amazon-simple-storage-service-amazon-s3)
* Amazon Redshift: [https://aws.amazon.com/redshift/](https://aws.amazon.com/redshift/)

Use the above references to deepen your understanding of DynamoDB integration patterns, pricing models (on-demand vs provisioned), and best practices for table design and indexing.

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-aws-databases/module/001734a9-f7c2-4943-83a3-d64621fedfd2/lesson/da590403-c3a4-45ff-95e1-7f539adf90e8)
