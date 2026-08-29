# Relational vs Non Relational Databases Part 2

Source: https://notes.kodekloud.com/docs/Database-Fundamentals/Relational-vs-Non-Relational-Databases/Relational-vs-Non-Relational-Databases-Part-2/page

Compares relational and NoSQL databases, explains trade-offs, data models, performance and scaling, and demonstrates MongoDB CRUD mirroring typical SQL workflows.

Different jobs require different tools. In real-world systems it's common to combine database types, selecting the right tool for each workload. This article compares relational and non-relational (NoSQL) databases, explains their core trade-offs, and shows a practical MongoDB CRUD demo that mirrors typical SQL workflows.

NoSQL databases generally fall into four families: document, key-value, column, and graph. Each family targets different data shapes and access patterns.

Table of contents

* Comparison summary (analogy: library vs filing cabinet)
* Structure, integrity, performance, and scale (with visual aids)
* Quick pop quiz
* MongoDB CRUD demo (Create, Read, Update, Delete)
* Summary and key takeaways
* Links and references

Why this matters (quick primer)

* Relational databases: well-defined schemas, ACID guarantees, great for accuracy and complex transactions.
* NoSQL databases: schema-flexible, often designed for horizontal scale and simple high-volume operations.
* Choosing the right database depends on data shape, access patterns, and consistency requirements.

NoSQL families at a glance

| Family    |                                                                     Description | Common use cases                                | Examples                           |
| --------- | ------------------------------------------------------------------------------: | ----------------------------------------------- | ---------------------------------- |
| Document  | Stores semi-structured JSON-like documents; each record can have varying fields | Content management, user profiles, event logs   | MongoDB, Couchbase                 |
| Key-value |                              Simple mapping from `key -> value` (opaque values) | Caching, session stores, feature flags          | Redis, DynamoDB (in some patterns) |
| Column    |    Wide-column stores optimized for large-scale writes and reads across columns | Time-series, analytics, IoT                     | Apache Cassandra, ScyllaDB         |
| Graph     |                      Stores nodes and edges to represent relationships directly | Social graphs, fraud detection, recommendations | Neo4j, Amazon Neptune              |

Analogy: library (relational) vs filing cabinet (NoSQL)

* Library (relational): every book follows the same catalog — title, author, ISBN, subject — placed on the correct shelf. That predictable catalog is a schema (tables, columns, data types).
* Filing cabinet (NoSQL): drawers can be organized independently; each folder may contain different fields. You can add new fields without redesigning the entire system.

Structure

* Libraries are predictable and consistent; schemas enforce the shape of data before it’s stored.
* Filing cabinets (documents, key-value, etc.) are flexible, allowing varied records and easy schema evolution.

Why it matters: fixed schemas are ideal for predictable data (e.g., invoices). Schema flexibility works best for evolving data models (e.g., user-generated content).

Data integrity

* Libraries have librarians who enforce uniqueness and cross-references — analogous to relational constraints (primary keys, foreign keys, data types).
* Filing cabinets can accept diverse entries quickly and reconcile them later — many NoSQL systems favor eventual consistency for higher write throughput.

Why it matters: strong consistency and constraints are essential when correctness matters (banking). Eventual consistency is often acceptable for social feeds or tag systems.

<Frame>
  <img alt="The image compares relational and non-relational databases using visual metaphors of a city library and a cabinet, highlighting aspects such as structure, integrity, performance, and scale. There's a person wearing a KodeKloud shirt speaking." />
</Frame>

Performance

* Libraries are optimized for deep research and complex cross-references — similar to SQL queries and joins across multiple normalized tables.
* Filing cabinets can be faster for simple lookups when related data is stored together; many NoSQL systems store denormalized records for quick reads.

Why it matters: relational systems typically excel at analytical queries; NoSQL often outperforms for high-throughput key lookups and simple read/write operations.

<Frame>
  <img alt="The image compares relational and non-relational databases, highlighting features like schema structure, consistency, and scalability. It includes illustrations of a city library and a cabinet to represent each database type." />
</Frame>

Scale

* Vertical scaling (adding CPU, RAM) is like enlarging a library building — effective but expensive and finite.
* Horizontal scaling (adding more cabinets/machines) is often simpler for NoSQL systems; many are built to shard and replicate across nodes.

Why it matters: NoSQL solutions typically simplify horizontal scaling for very large ingest rates and distributed workloads (e-commerce catalogs, streaming events).

<Frame>
  <img alt="The image compares relational and non-relational databases, illustrating differences in structure, integrity, performance, and scalability, with an explanation from a person in a KodeKloud shirt." />
</Frame>

Which is better?

* There is no universally “better” choice. Use relational databases when data integrity and complex transactions are critical. Use NoSQL when flexibility, massive scale, or specialized access patterns are more important.
* Hybrid architectures are common: relational systems for core transactional data and NoSQL for flexible or high-throughput services.

Pop quiz
Which statement is true?

A. NoSQL databases are always faster than relational databases.\
B. Relational databases require a fixed schema.\
C. Graph databases store data in rows and columns.

Answer: B is correct. Relational databases typically use a fixed schema (tables, columns, and data types are defined before storing data).

Why the others are false:

* A is false: NoSQL can be faster for simple operations, but relational databases may outperform for complex queries.
* C is false: Graph databases use nodes and edges, not rows and columns.

From MySQL to MongoDB — same CRUD, different shape
Below is a MongoDB demo that mirrors typical SQL CRUD operations. MongoDB stores flexible, JSON-like documents and returns JSON-style responses in the shell.

Connect to mongosh and create a `miaowtube` database with `users` and `videos` collections:

```bash theme={null}
bob@mongodb-host ~ % mongosh --authenticationDatabase "admin" -u "myUserAdmin" -p
Enter password: ********
Current Mongosh Log ID: 688ca1c3d12a696511d6795
Connecting to: mongodb://<credentials>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.4.2
Using MongoDB: 5.0.8
Using Mongosh: 1.4.2

> use miaowtube
switched to db miaowtube

> db.createCollection("users");
{ ok: 1 }

> db.createCollection("videos");
{ ok: 1 }

> show collections
users
videos
```

<Callout icon="lightbulb">
  MongoDB collections are schema-flexible by default. You can enforce validation rules if you need stricter structure, but it’s optional and can be applied incrementally.
</Callout>

Create (insert) users
Insert two user documents. We add a numeric `user_id` to mimic a conventional primary-key reference:

```javascript theme={null}
miaowtube> db.users.insertMany([
  { user_id: 1, username: "fluffy", email: "fluffy@email.com" },
  { user_id: 2, username: "paws",  email: "paws@email.com" }
]);
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("688ca2030aad588906929b1f"),
    '1': ObjectId("688ca2030aad588906929b2f")
  }
}
```

Read users
Verify the inserted documents:

```javascript theme={null}
miaowtube> db.users.find({});
[
  {
    _id: ObjectId("688ca2030aad588906929b1f"),
    user_id: 1,
    username: "fluffy",
    email: "fluffy@email.com"
  },
  {
    _id: ObjectId("688ca2030aad588906929b2f"),
    user_id: 2,
    username: "paws",
    email: "paws@email.com"
  }
]
```

Create videos
Insert three videos, each referencing `user_id`:

```javascript theme={null}
miaowtube> db.videos.insertMany([
  { user_id: 1, title: "Cat Skateboard",  link: "www.miaowtube/watch1", upload_date: "2025-05-25" },
  { user_id: 2, title: "Epic Cat Jump",   link: "www.miaowtube/watch2", upload_date: "2025-05-27" },
  { user_id: 1, title: "Cat vs Curtain",   link: "www.miaowtube/watch3", upload_date: "2025-05-29" }
]);
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("688ca2310aad588906929b3f"),
    '1': ObjectId("688ca2310aad588906929b4f"),
    '2': ObjectId("688ca2310aad588906929b5f")
  }
}
```

Read videos (full documents)
List all videos:

```javascript theme={null}
miaowtube> db.videos.find({});
[
  {
    _id: ObjectId("688ca2310aad588906929b3f"),
    user_id: 1,
    title: "Cat Skateboard",
    link: "www.miaowtube/watch1",
    upload_date: "2025-05-25"
  },
  {
    _id: ObjectId("688ca2310aad588906929b4f"),
    user_id: 2,
    title: "Epic Cat Jump",
    link: "www.miaowtube/watch2",
    upload_date: "2025-05-27"
  },
  {
    _id: ObjectId("688ca2310aad588906929b5f"),
    user_id: 1,
    title: "Cat vs Curtain",
    link: "www.miaowtube/watch3",
    upload_date: "2025-05-29"
  }
]
```

Read videos (projection)
Request only titles using a projection:

```javascript theme={null}
miaowtube> db.videos.find({}, { title: 1, _id: 0 });
[
  { title: "Cat Skateboard" },
  { title: "Epic Cat Jump" },
  { title: "Cat vs Curtain" }
]
```

Update
Rename "Cat Skateboard" -> "Flufferson on Skateboard":

```javascript theme={null}
miaowtube> db.videos.updateOne(
  { title: "Cat Skateboard" },
  { $set: { title: "Flufferson on Skateboard" } }
);
{
  acknowledged: true,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedId: null
}
```

Verify update:

```javascript theme={null}
miaowtube> db.videos.find({}, { title: 1, _id: 0 });
[
  { title: "Flufferson on Skateboard" },
  { title: "Epic Cat Jump" },
  { title: "Cat vs Curtain" }
]
```

Delete
Remove "Cat vs Curtain":

```javascript theme={null}
miaowtube> db.videos.deleteOne({ title: "Cat vs Curtain" });
{ acknowledged: true, deletedCount: 1 }

miaowtube> db.videos.find({});
[
  {
    _id: ObjectId("688ca2310aad588906929b3f"),
    user_id: 1,
    title: "Flufferson on Skateboard",
    link: "www.miaowtube/watch1",
    upload_date: "2025-05-25"
  },
  {
    _id: ObjectId("688ca2310aad588906929b4f"),
    user_id: 2,
    title: "Epic Cat Jump",
    link: "www.miaowtube/watch2",
    upload_date: "2025-05-27"
  }
]
```

<Callout icon="warning">
  Schema flexibility is powerful but can lead to inconsistent or inefficient queries if unchecked. Use indexes and, where appropriate, schema validation to maintain performance and data quality.
</Callout>

Summary of the MongoDB demo

* CRUD operations map directly to familiar SQL concepts, but MongoDB uses flexible JSON-like documents.
* Shell responses return JSON-style objects (`acknowledged`, `insertedIds`, `matchedCount`, etc.).
* Schema and integrity: SQL enforces structure up front; MongoDB gives you flexibility but lets you add validation rules or handle constraints in application logic.
* Performance and scale: document models and horizontal-sharding designs commonly make MongoDB and other NoSQL systems suitable for high-throughput workloads.

<Frame>
  <img alt="The image compares MySQL and MongoDB in terms of structure, data integrity, and performance and scale, with a person wearing a KodeKloud t-shirt standing beside the comparison chart." />
</Frame>

Key takeaways

* Relational databases: structured tables, strong consistency, ideal for accuracy and complex transactions.
* NoSQL databases: flexible formats (document, key-value, column, graph), better for varied or rapidly changing data and massive scale.
* Use the right tool for the job — many systems combine relational and non-relational databases to leverage strengths from both.
* Indexes and well-designed queries matter in both paradigms for search speed and overall performance.

Links and references

* MongoDB manual: [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)
* Choosing a database: [https://martinfowler.com/articles/nosql-intro.html](https://martinfowler.com/articles/nosql-intro.html)
* Database scaling patterns: [https://www.digitalocean.com/community/tutorials/](https://www.digitalocean.com/community/tutorials/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/database-fundamentals/module/222257ca-7414-41c1-b5ca-5a1059cc8ba0/lesson/c8a95810-4733-4434-aa19-bc356f3f1a30" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/database-fundamentals/module/222257ca-7414-41c1-b5ca-5a1059cc8ba0/lesson/81e1108e-77aa-4a46-8e88-ea465c441df1" />
</CardGroup>
