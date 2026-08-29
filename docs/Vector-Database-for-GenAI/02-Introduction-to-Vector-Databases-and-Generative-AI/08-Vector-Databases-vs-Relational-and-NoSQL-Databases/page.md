# Vector Databases vs Relational and NoSQL Databases

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Introduction-to-Vector-Databases-and-Generative-AI/Vector-Databases-vs-Relational-and-NoSQL-Databases/page

Comparison of vector, relational, and NoSQL databases, highlighting data models, query patterns, use cases, scalability, and integration for AI tasks like semantic search and RAG

Welcome back. This lesson explains how vector databases compare with the relational and NoSQL databases you already know. You'll get a clear sense of their data models, query patterns, typical use cases, and where each fits in a modern architecture—especially for AI-driven workflows like semantic search and retrieval-augmented generation (RAG).

## Data models: what each database stores

* Vector databases
  * Store high-dimensional vectors (embeddings). Each vector is a dense array of floating-point numbers—often hundreds to thousands of dimensions—that encode the semantics of text, images, audio, or other modalities. Conceptually, these are points in a high-dimensional space (an extension of a 2D coordinate system).
  * Optimized for similarity comparisons between vectors (semantic closeness), not attribute-level filtering.

* Relational databases
  * Store structured data in tables (rows and columns) with enforced schemas, foreign keys, and constraints.
  * Excellent for transactional systems and operations that require ACID guarantees and complex joins.

* NoSQL databases
  * Include document stores, key-value stores, and wide-column stores; they store flexible data (e.g., JSON documents) and often do not require a fixed schema.
  * Designed for high throughput, horizontal scaling, and schema evolution.

## Querying: exact-match vs. semantic similarity

* Vector databases
  * Optimized for similarity search: instead of exact matches, you retrieve the nearest or most similar items to a query vector. Common distance/similarity metrics include cosine similarity, Euclidean distance, and inner product.
  * At scale, they rely on approximate nearest neighbor (ANN) algorithms and specialized indexes such as HNSW, IVF, and product quantization (PQ). Implementations and libraries: FAISS, Annoy, and many native cloud offerings.
  * Helpful links:
    * Approximate nearest neighbor: [https://en.wikipedia.org/wiki/Approximate\_nearest\_neighbor\_search](https://en.wikipedia.org/wiki/Approximate_nearest_neighbor_search)
    * HNSW: [https://github.com/nmslib/hnswlib](https://github.com/nmslib/hnswlib)
    * FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
    * Annoy: [https://github.com/spotify/annoy](https://github.com/spotify/annoy)

* Relational databases
  * Use declarative SQL for exact filtering, joins, aggregations, and transactional operations:

```sql theme={null}
SELECT ...
FROM ...
JOIN ...
WHERE ...
-- Exact match filtering and relational operations
```

* NoSQL databases
  * Use flexible, attribute-based queries (document or key-based). They are suited to queries that filter on fields, ranges, or indexed attributes rather than dense-vector similarity.

## Comparison at a glance

| Resource Type | Data Model                                    | Query Style                             | Best For                                                       | Scaling                                                  |
| ------------- | --------------------------------------------- | --------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------- |
| Vector DB     | High-dimensional `embeddings` (dense vectors) | Nearest-neighbor / similarity search    | Semantic search, RAG, recommendations, image/audio matching    | Horizontal with ANN indexes and sharding                 |
| Relational DB | Structured `tables` with schema               | SQL (joins, aggregations, transactions) | Transactional systems, analytics requiring ACID, complex joins | Traditionally vertical; distributed SQL/sharding options |
| NoSQL DB      | Flexible `documents` / key-values             | Document/key queries, attribute filters | Web-scale apps, telemetry, flexible schema workloads           | Built for horizontal scaling                             |

## Typical use cases

* Vector databases
  * Semantic search, content-based retrieval, recommender systems, question-answering systems, and other AI/ML use cases that depend on meaning rather than exact attribute matches.
  * Retrieval-augmented generation (RAG): index embeddings from documents, retrieve semantically relevant passages, then feed into a language model.

* Relational databases
  * Systems that rely on strong consistency, transactional integrity, complex joins, and strict schemas—examples: banking, CRM, ERP.

* NoSQL databases
  * High-throughput web services, real-time telemetry, social platforms, and any application benefiting from flexible document models and horizontal scaling.

## Scalability and operational considerations

* Vector databases
  * Designed to scale horizontally and serve fast nearest-neighbor queries across millions or billions of vectors. Use sharding and distributed ANN indexes to maintain latency at scale.
  * Expect trade-offs between recall and throughput when using approximate methods.

* Relational databases
  * Often scale vertically (bigger machines); horizontal scaling requires distributed SQL products, read replicas, or complex sharding strategies.

* NoSQL databases
  * Architected for horizontal distribution and large-scale writes/reads with eventual consistency options, tunable consistency, and flexible replication models.

## Integration patterns: how these databases work together

A practical pattern is to combine systems so each holds what it does best:

* Keep transactional and structured metadata (user records, orders, logs) in a relational or NoSQL store.
* Store embeddings and ANN indexes in a vector database for similarity search.
* Link records via IDs or metadata so that a vector search returns candidate IDs, which you then enrich with data from the primary store.

Example flow for a RAG pipeline:

1. Ingest docs → create embeddings → index in vector DB.
2. Query with user prompt → compute query embedding → perform ANN search in vector DB.
3. Retrieve top-K document IDs → fetch full metadata/content from relational/NoSQL store → feed into language model.

## When to use what

* Use a vector database when:
  * Your problem is semantic or similarity-based and requires fast nearest-neighbor search over dense embeddings.
  * Examples: semantic search, image similarity, RAG, personalized recommendations.

* Use a relational database when:
  * You need strong schema enforcement, complex joins/aggregations, and transactional integrity (ACID).

* Use NoSQL when:
  * You need flexible schemas, rapid iteration, and horizontal scaling for high throughput read/write workloads.

<Frame>
  <img alt="The image is a comparison chart of vector, relational, and NoSQL databases, detailing their data structures, query methods, primary use cases, and scalability. It highlights attributes such as high-dimensional vectors, SQL queries, and document/key queries for each type." />
</Frame>

Why do we need another kind of database when we already have NoSQL or SQL databases?

The short answer: different primary use cases. Vector databases are specialized for extracting and operating on meaning encoded in embeddings. They are not drop-in replacements for relational or document stores:

* Transactional analytics, precise counts, and complex aggregations are still best handled by relational databases—these queries may be unsupported or inefficient in vector DBs.
* Vector databases are best used as complementary systems. A common architecture persists: store structured records and metadata in relational/NoSQL stores, and store embeddings with ANN indexes in a vector database for semantic retrieval.

<Callout icon="lightbulb">
  Use vector databases for semantic, similarity, and retrieval-first problems. Keep structured transactional data and complex relational queries in relational databases; use NoSQL for flexible, high-throughput document or key-value workloads.
</Callout>

That’s it for this lesson. See you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/841f0a59-96ec-4dc1-b84f-b577ab5a5bb7/lesson/f752dd17-2be1-47b6-8d16-1dc55ce4aeb7" />
</CardGroup>
