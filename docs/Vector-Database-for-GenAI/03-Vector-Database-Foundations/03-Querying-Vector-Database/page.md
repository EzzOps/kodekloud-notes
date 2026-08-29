# Querying Vector Database

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Foundations/Querying-Vector-Database/page

Explains how vector databases use embeddings and nearest neighbor search to enable semantic search, contrasting with traditional exact-match databases and covering practical considerations

Welcome back.

Previously we covered how traditional databases perform exact keyword matching. That raises a big question: how do you search by meaning instead of exact words? In this lesson we’ll walk through that process and explain how vector databases enable semantic (meaning-based) search.

## Overview

* In a vector database, both your stored items and incoming queries are represented as vectors (numeric arrays called embeddings).
* The system performs nearest-neighbor searches in a semantic vector space and returns items whose vectors are closest to the query vector.
* This enables searching by meaning rather than by exact keyword matches.

## How queries work in a vector database

When you submit a search phrase, it is converted into an embedding (a vector) using an embedding model. All documents or items in the database are stored as vectors produced by the same or a compatible model. The database compares the query vector to stored vectors and returns the most similar items.

Example:

Query text:

```plaintext theme={null}
"portable computing device"
```

Query (embedded):

```plaintext theme={null}
[−0.80, −0.31, 0.45, …, 0.67]  (query vector)
```

Think of the embedding space as a coordinate map where semantically similar concepts cluster close together. The database finds items whose vectors lie nearest the query vector using a nearest-neighbor search.

### Example results and similarity scores

* Laptop — similarity: 0.91 (very close): matches the query well.
* Tablet — similarity: 0.89 (also relevant).
* Chair — similarity: 0.29 (irrelevant).

Similarity scores come from applying a distance or similarity metric to vectors. Common metrics:

| Metric                      | Description                                                                                 | Typical range / notes                                         |
| --------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Cosine similarity           | Measures the cosine of the angle between vectors; commonly used for text                    | −1..1 (often normalized to 0..1 for ranking)                  |
| Euclidean distance          | Geometric distance in embedding space                                                       | Lower is better (0 = identical)                               |
| Dot product / inner product | Sum of element-wise products; sometimes used with specific models or hardware optimizations | Larger values indicate more similarity for normalized vectors |

<Callout icon="lightbulb">
  Choosing the right embedding model and similarity metric is crucial. Models trained on your domain (or fine-tuned) will place domain-specific concepts closer together and improve retrieval quality.
</Callout>

<Callout icon="warning">
  Similarity scores are model-dependent. Unexpected high or low scores may indicate an embedding/model mismatch or data-quality issue — inspect both embeddings and the model choice before tuning thresholds.
</Callout>

## Semantic search vs. exact-match SQL

Here’s a side-by-side contrast to clarify the difference.

Traditional database (exact-match SQL)

* Operates on structured fields and exact values.
* Best for transactional workloads, aggregates, joins, and ACID guarantees.

Example SQL:

```sql theme={null}
SELECT * FROM products
WHERE category = 'electronics';
```

Example result (exact match):

```plaintext theme={null}
ID: 101 | Name: Laptop | Category: electronics
ID: 102 | Name: Phone  | Category: electronics
ID: 103 | Name: Tablet | Category: electronics
```

Vector database (semantic search)

* Converts text into embeddings and searches a semantic vector space for nearest neighbors.
* Returns items ranked by semantic similarity rather than exact keyword matches.

Conceptual flow:

```plaintext theme={null}
Query (text): "portable computing device"
Query (embedded): [−0.80, −0.31, 0.45, …, 0.67]

Vector embeddings (semantic space):
Laptop  -> [−0.81, −0.29, …]  similarity: 0.91
Tablet  -> [−0.79, −0.28, …]  similarity: 0.89
Chair   -> [ 0.12,  0.73, …]  similarity: 0.29
```

## When to use each system

| Resource Type                             | Use Case                                                            | Which to use and why                                    |
| ----------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| Structured records (orders, transactions) | Exact queries, joins, aggregates, ACID needs                        | Traditional relational DB                               |
| Search across documents, notes, or media  | Meaning-based relevance, fuzzy queries, multi-modal retrieval       | Vector database + embeddings                            |
| Hybrid use (filters + relevance)          | Combine structured filters (e.g., date, user) with semantic ranking | Use both: SQL/NoSQL for filters + vector DB for ranking |

## Practical considerations

* Indexing & performance: For large datasets, approximate nearest neighbor (ANN) indexes (HNSW, IVF, PQ, etc.) drastically improve query speed with modest accuracy trade-offs.
* Scaling: Vector indexes and storage require different resource considerations compared to relational indexes (CPU/GPU for embedding generation, memory/SSD for ANN indexes).
* Model choice: Off-the-shelf models often work well, but fine-tuning or using domain-specific embeddings improves relevance.
* Evaluation: Validate retrieval using domain-specific relevance labels and metrics (e.g., recall\@k, MRR).

## Real-world example

Tools like [Notion AI](https://www.notion.so/product/ai) convert user queries into vectors and retrieve the most relevant notes by semantic similarity. This allows the system to return relevant content even when the user uses different words than the original notes — making search feel more like understanding than keyword matching.

## Next steps / Further reading

Topics to explore next:

* Embedding generation: comparing popular models and their trade-offs.
* ANN indexes: HNSW, IVF, PQ and how they impact speed vs. accuracy.
* Hybrid search: combining structured filtering with semantic ranking.
* Evaluation: building labeled datasets and metrics for tuning retrieval.

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/) — (general ops reference)
* [Notion AI product page](https://www.notion.so/product/ai)
* Search terms to explore: `vector database`, `semantic search`, `embeddings`, `approximate nearest neighbor (ANN)`, `cosine similarity`, `HNSW`

Thanks — in the next lesson we’ll examine nearest-neighbor indexes and practical trade-offs between accuracy and latency for production semantic search systems.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/82014ec3-9709-44d1-bd41-577af87083ed/lesson/377fc1a1-e225-4d7f-bdb5-50a8ca0468b4" />
</CardGroup>
