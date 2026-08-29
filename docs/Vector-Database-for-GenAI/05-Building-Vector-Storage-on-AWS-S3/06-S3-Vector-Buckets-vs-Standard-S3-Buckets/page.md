# S3 Vector Buckets vs Standard S3 Buckets

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Building-Vector-Storage-on-AWS-S3/S3-Vector-Buckets-vs-Standard-S3-Buckets/page

Comparing S3 Vector Buckets and standard S3 buckets for AI versus general object storage, explaining differences in data models, APIs, querying, and ideal use cases.

Hello and welcome back.

S3 Vector Buckets and standard S3 buckets share the same "S3" branding, but they serve very different use cases. Don’t let the name fool you—these are distinct storage systems with different data models, APIs, query capabilities, and access patterns. This guide compares them side-by-side and explains when to use each for AI and general storage workloads.

## What each stores

* S3 Vector Buckets store numerical vector embeddings: fixed-length arrays (embeddings) that represent the semantic meaning of content such as sentences, images, or product descriptions. Embeddings are organized into vector indexes optimized for similarity search.
* Standard S3 stores unstructured objects: files like PDFs, images, videos, database backups—retrieved by object keys and prefixes.

## API surface

The APIs reflect the intended use:

* S3 Vector Buckets typically expose vector-focused operations such as `PutVectors`, `QueryVectors`, `GetVectors`, and `DeleteVectors` (actual names vary by provider).
* Standard S3 exposes object-oriented operations such as `PutObject`, `GetObject`, `DeleteObject`, and `ListObjects` (key-based access).

Example: storing a document and its embedding

* Store the raw file in standard S3:

```bash theme={null}
aws s3 cp ./docs/report.pdf s3://my-doc-bucket/reports/report.pdf
```

* Store the embedding in an S3 Vector Bucket (pseudocode):

```json theme={null}
{
  "IndexName": "customer_support_docs",
  "Vectors": [
    { "id": "chunk-123", "values": [0.012, -0.234, 0.981], "metadata": { "s3_key": "reports/report.pdf#chunk-1" } }
  ]
}
```

## Data organization

* S3 Vector Buckets: Organized into vector indexes inside a bucket. Each index contains vectors grouped by dimension and index metadata. A bucket can contain many indexes (limits depend on provider). The index layer is optimized for approximate nearest neighbor (ANN) search.
* Standard S3: Flat namespace of object keys and prefixes with optional prefixes acting like folders. No native similarity-query layer—access is key-based and you can optionally use features like S3 Select for filtering content inside objects.

## Query capability — the key distinction for AI

* S3 Vector Buckets provide native similarity search (ANN). You query with a vector and retrieve nearest neighbors using distance metrics such as cosine or Euclidean. You can usually apply metadata filters on top of vector results (e.g., time ranges, tags).
* Standard S3 does not provide native similarity search. You can perform exact key lookups or use content-based filtering via S3 Select or downstream indexing systems (e.g., Elasticsearch, OpenSearch), but you cannot natively "find similar" objects by meaning.

## Access patterns — analogy

* Standard S3 = key-based retrieval: You know the key (like an ISBN), you fetch the object. Predictable and deterministic.
* S3 Vector Buckets = semantic retrieval: You provide a vector (or embed a query) and ask for the nearest neighbors by meaning—like describing a book’s blurb to get recommendations for similar books.

## Storage tiers and lifecycle

* S3 Vector Buckets generally use an optimized storage tier for index performance and query latency. They often auto-optimize indexes and do not expose multiple S3-style storage classes in the same way standard S3 does.
* Standard S3 offers multiple storage classes (Standard, Standard-IA, Glacier) and lifecycle rules for cost management and archival.

## Versioning and durability semantics

* S3 Vector Buckets may not support object-style versioning; overwrites or deletes can be final. Check your provider’s documentation for exact semantics.
* Standard S3 supports full object versioning, which is useful for backups, compliance, and data recovery.

## Public access and security defaults

* S3 Vector Buckets commonly default to private access and often have Block Public Access enabled; they are typically not intended for public hosting.
* Standard S3 is configurable: you can make buckets public for static website hosting or CDNs, or lock them down for private data.

<Callout icon="lightbulb">
  A common production pattern is to use both: store raw source files (PDFs, knowledge base articles, images) in a standard S3 bucket, and store document or chunk embeddings in an S3 Vector Bucket. Use vector search to find relevant chunks and then fetch the original content from standard S3.
</Callout>

## Quick comparison table

| Feature          |                                   Standard S3 buckets | S3 Vector Buckets                                                        |
| ---------------- | ----------------------------------------------------: | ------------------------------------------------------------------------ |
| Primary data     |                 Files/objects (images, PDFs, backups) | Numerical embeddings in vector indexes                                   |
| Access model     |                  Key-based (`PutObject`, `GetObject`) | Vector-based (`PutVectors`, `QueryVectors`, `GetVectors`)                |
| Query capability |       Exact lookup, `S3 Select` for content filtering | Native ANN / similarity search (cosine, Euclidean) with metadata filters |
| Storage tiers    | Multi-class (Standard, IA, Glacier) + lifecycle rules | Usually single optimized tier for index/query performance                |
| Versioning       |                      Full object versioning supported | Varies — often limited or different semantics                            |
| Public hosting   |                            Supported and configurable | Generally blocked or discouraged                                         |
| Ideal use cases  |                Asset storage, backups, static hosting | Semantic search, RAG systems, similarity retrieval                       |

## Real-world example: Retrieval-Augmented Generation (RAG) workflow

1. Store raw documents in a standard S3 bucket:

```bash theme={null}
aws s3 cp ./knowledge/article.md s3://kb-bucket/articles/article-1.md
```

2. Split documents into chunks, generate embeddings, and store them in a vector index:

```json theme={null}
POST /putVectors
{
  "IndexName": "kb-index",
  "Vectors": [
    { "id": "article-1-chunk-1", "values": [0.11, 0.23, ...], "metadata": { "s3_key": "articles/article-1.md#chunk-1" } }
  ]
}
```

3. At query time, embed the user’s query and call `QueryVectors` to retrieve nearest neighbors:

```json theme={null}
POST /queryVectors
{
  "IndexName": "kb-index",
  "QueryVector": [0.07, -0.12, ...],
  "TopK": 5,
  "Filters": { "source": "product_docs" }
}
```

4. Use returned metadata (for example, `s3_key`) to fetch the original chunk from standard S3:

```bash theme={null}
aws s3 cp s3://kb-bucket/articles/article-1.md ./article-1.md
```

Two buckets, two complementary roles: vector indexes for semantic lookup and standard S3 for raw content storage.

## When to use which

* Use standard S3 when:
  * You need reliable object storage, multi-tier lifecycle, or static hosting.
  * You require versioning and archival options.
  * Your access pattern is key-based retrieval.

* Use S3 Vector Buckets when:
  * You need semantic similarity search, nearest-neighbor retrieval, or ANN for AI applications.
  * You want a native index for embeddings with metadata filtering.
  * You need low-latency vector queries tied to a vector-aware service.

## Further reading and references

* [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/)
* For vector search patterns and ANN concepts, search for "semantic search", "approximate nearest neighbor", and "retrieval-augmented generation (RAG)" articles and provider docs.

That’s it on S3 Vector Buckets vs standard S3 buckets — thanks for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/afa51fbf-32d5-4459-a9de-0a764b24682b/lesson/3a6f5583-1a3e-430b-84c7-a74edd73da16" />
</CardGroup>
