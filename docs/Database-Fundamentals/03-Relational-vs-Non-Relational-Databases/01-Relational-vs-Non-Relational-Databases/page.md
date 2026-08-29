# Relational vs Non Relational Databases

Source: https://notes.kodekloud.com/docs/Database-Fundamentals/Relational-vs-Non-Relational-Databases/Relational-vs-Non-Relational-Databases/page

Overview and comparison of relational and NoSQL databases, their types, tradeoffs, and use cases, with practical examples and CRUD operations in MongoDB

We've spent the last few lessons building tidy, structured databases using entities, relationships, and keys. To recap, here's what Kodi's MeowTube looks like as a relational database: three linked tables—users, videos, and comments—joined using primary and foreign keys. Each table has a fixed set of columns, which enforces consistency.

<Frame>
  <img alt="The image shows a person standing in front of a database schema diagram featuring tables for videos, users, and comments." />
</Frame>

That rigid structure keeps data clean, but it can become cumbersome as your data variety grows.

Consider an online store: at first a products table with columns like name, price, and category is fine. Later you may need size, color, voltage, or material—many of which are empty for some products. Splitting those attributes into separate tables leads to more joins, which slows searches as tables grow.

<Frame>
  <img alt="The image shows a person standing next to a graphic of an online shopping interface with categories like Name, Price, and Size. There's also a depiction of shopping elements like a cart and a credit card." />
</Frame>

One workaround is to store attributes as multiple rows for the same product (attribute-per-row). For example:

* 42, color, red
* 42, size, M
* 42, price, \$149.99

This trades columns for rows, but it doesn't scale well. If you have 10 million products and each has 100 attributes, you end up with 1 billion rows. Multi-filter searches then require multiple passes over the attribute table (one pass per filter), producing large intermediate result sets that must be intersected—an expensive operation. If numeric values are stored as text (e.g., price as a string), the database must also convert types during queries, adding extra overhead.

<Frame>
  <img alt="The image shows a diagram explaining a search query for a &#x22;Medium Red Jacket under $150,&#x22; highlighting filtering criteria and processes, along with a person standing in front." />
</Frame>

This approach can work for small datasets but struggles at scale. That’s where non-relational (NoSQL) databases often provide a better fit.

By the end of this lesson you'll be able to:

* Describe different types of non-relational databases
* Compare relational and non-relational approaches
* Perform and interpret CRUD operations in a NoSQL database (we'll use MongoDB as a concrete example)

<Frame>
  <img alt="The image shows a person standing next to a list outlining three tasks related to databases, with a cartoon cat on the side. The tasks include describing non-relational databases, comparing relational and non-relational databases, and performing CRUD operations in a NoSQL database." />
</Frame>

What does NoSQL mean? It stands for Not Only SQL — a family of databases that relax the rigid relational schema to gain flexibility, performance, or scalability for specific data access patterns.

> **lightbulb** NoSQL databases are not a single technology. They include document stores, key-value stores, wide-column stores, graph databases, time-series databases, and vector databases—each optimized for different workloads and query patterns.

Below is an overview of common NoSQL flavors and how they apply to an app like MeowTube.

<Frame>
  <img alt="The image shows a person standing next to a list of database types, including document stores, key-value stores, wide-column stores, graph databases, time-series databases, and vector databases, with a stylized folder icon in the center." />
</Frame>

Document stores

* Store related data together in a single document (typically JSON/BSON).
* Great for objects with many optional or evolving fields because you can add attributes without schema migrations.
* Example document for a MeowTube video (JSON):

```json theme={null}
{
  "video_id": 1,
  "title": "Cat Skateboard",
  "link": "www.miaowtube/watch1",
  "upload_date": "2025-05-25",
  "user": {
    "user_id": 1,
    "username": "fluffy"
  },
  "comments": [
    {
      "comment_id": 1,
      "user_id": 1,
      "username": "fluffy",
      "text": "This is so cute!",
      "timestamp": "2025-07-01"
    },
    {
      "comment_id": 2,
      "user_id": 2,
      "username": "paws",
      "text": "Instant classic.",
      "timestamp": "2025-07-02"
    }
  ]
}
```

Objects are human- and machine-readable. Curly braces denote objects and square brackets denote lists. Sensitive fields (like email) can be omitted or kept in a separate collection with stricter access controls.

If you need to add a new field—say `dislikes`—you can simply insert it into the document without changing a schema or running migrations:

```json theme={null}
{
  "video_id": 1,
  "title": "Cat Skateboard",
  "link": "www.miaowtube/watch1",
  "upload_date": "2025-05-25",
  "dislikes": 3,
  "user": {
    "user_id": 1,
    "username": "fluffy"
  },
  "comments": [
    {
      "comment_id": 1,
      "user_id": 1,
      "username": "fluffy",
      "text": "This is so cute!",
      "timestamp": "2025-07-01"
    },
    {
      "comment_id": 2,
      "user_id": 2,
      "username": "paws",
      "text": "Instant classic.",
      "timestamp": "2025-07-02"
    }
  ]
}
```

If you prefer to store sensitive user details separately:

```json theme={null}
{
  "email": "fluffy@gmail.com"
}
```

Key-value stores

* Think of these as supercharged dictionaries: a unique key maps to a value (often a blob or JSON document).
* Extremely fast for single-key lookups.
* You lose automatic grouping of related data; you must fetch multiple keys and assemble results in the application.

Example key-value entries (pseudocode):

```text theme={null}
Key: user:1
Value: { "username": "fluffy", "email": "fluffy@email.com" }

Key: video:1
Value: {
  "title": "Cat Skateboard",
  "link": "www.miaowtube/watch1",
  "upload_date": "2025-05-25",
  "user_id": 1
}

Key: comment:2
Value: {
  "video_id": 1,
  "user_id": 2,
  "text": "Instant classic.",
  "timestamp": "2025-07-02"
}
```

Wide-column stores

* Rows resemble tables but columns are flexible per row.
* Each row can have variable columns; you design "wide tables" optimized for specific access patterns.
* Excellent for very large datasets and distributed workloads (e.g., regional sales metrics across millions of products).

<Frame>
  <img alt="The image illustrates a wide-column store database structure, showing tables for videos, users, and comments. It includes labels for various database types and a person standing beside the graphic." />
</Frame>

Graph databases

* Model data as nodes (entities) and edges (relationships).
* Extremely efficient at traversing relationships (e.g., "users who liked videos uploaded by Fluffy").
* Ideal for social networks, recommendation engines, and fraud detection, where relationship queries are frequent and complex.

Time-series databases

* Optimized for timestamped data where "when" is as important as "what".
* Rather than updating a single record, time-series DBs append new entries with timestamps to build a full history (e.g., daily views for a video).
* Great for monitoring, metrics, analytics, and trend detection.

<Frame>
  <img alt="The image features a person in a &#x22;CodeKoda&#x22; shirt discussing data trends over time, with a focus on time-series databases. There are also cartoon cat characters labeled Kody, Kofi, and Kade." />
</Frame>

Vector databases

* Store vectors (lists of numbers) produced by machine learning models that capture semantic meaning.
* Support nearest-neighbor searches to find similar items even when text or IDs don’t match exactly (e.g., "cat skateboard" → "fluffy kitten longboard").
* Useful for semantic search, recommendations, and AI-driven retrieval.

<Frame>
  <img alt="The image features a person in a &#x22;KodeKloud&#x22; shirt next to a graphic depicting a vector database search interface with cat illustrations. It highlights the use of vector databases for recommendations and AI-powered search." />
</Frame>

Quick comparison table

| Database Type     | Best For                                                     | Example                                                       |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------- |
| Relational (SQL)  | Strong consistency, complex joins, transactional systems     | `Orders, inventory, banking systems`                          |
| Document store    | Evolving schemas, nested objects, fast reads of full objects | `{"video_id":1, "title":"Cat Skateboard", "comments":[...]} ` |
| Key-value store   | Extremely fast single-key lookups                            | `Key: video:1 -> Value: {...}`                                |
| Wide-column store | Massive, sparse datasets with varied columns                 | `Regional sales stats across millions of products`            |
| Graph database    | Deep relationship traversal and network queries              | `Users and their connections/likes`                           |
| Time-series DB    | Time-indexed metrics and historical trends                   | `Daily video view counts over time`                           |
| Vector database   | Semantic search and similarity queries                       | `Vectors produced by NLP/vision models`                       |

When to choose what

* Use a relational database when you need transactions and strict schema/enforced integrity.
* Use document stores when your objects are hierarchical, have many optional fields, or the schema evolves quickly.
* Use key-value stores for caches and sessions when you only need single-key access.
* Use wide-column stores for huge, sparse datasets distributed across many machines.
* Use graph databases when relationships are first-class and you need fast traversals.
* Use time-series DBs for metrics and monitoring.
* Use vector DBs for semantic search and AI-driven recommendations.

Links and references

* [MongoDB](https://www.mongodb.com/) — document store used in NoSQL examples
* [Cloud Computing Fundamentals](https://learn.kodekloud.com/user/courses/cloud-computing-fundamentals) — upcoming course for scaling patterns and distributed architectures
* [Database Design Patterns](https://en.wikipedia.org/wiki/Database_normalization) — background on normalization and trade-offs

> **warning** Flexible schemas simplify development but don’t eliminate the need for thought: design for your query patterns, enforce constraints where necessary, and keep sensitive data properly separated and secured.

- [Watch Video](https://learn.kodekloud.com/user/courses/database-fundamentals/module/222257ca-7414-41c1-b5ca-5a1059cc8ba0/lesson/aa102504-cc09-4423-9432-7e6a835d2529)
