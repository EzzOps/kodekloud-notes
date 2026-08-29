# vector dimension
d = 128

# sample dataset (1000 vectors)
xb = np.random.random((1000, d)).astype('float32')

# create a simple L2 index (exact search / brute force)
index = faiss.IndexFlatL2(d)
index.add(xb)  # add vectors to the index

# query: 5 random vectors
xq = np.random.random((5, d)).astype('float32')
k = 5  # number of nearest neighbors
distances, indices = index.search(xq, k)

print("indices.shape:", indices.shape)
print("distances.shape:", distances.shape)
```

Pinecone (managed service example)

```python theme={null}
import pinecone
import numpy as np

# initialize (replace with your API key and environment)
pinecone.init(api_key="YOUR_API_KEY", environment="us-west1-gcp")

# create or connect to an index (index is created in Pinecone console or via API)
index_name = "example-index"
index = pinecone.Index(index_name)

# upsert vectors: list of (id, vector) tuples
embedding = np.random.random(128).astype('float32')
index.upsert(vectors=[("id-1", embedding.tolist())])

# query the index
query_embedding = np.random.random(128).astype('float32')
result = index.query(queries=[query_embedding.tolist()], top_k=5)
print(result)
```

> **warning** When using managed services like Pinecone, pay attention to data residency, privacy, and API key security. For sensitive data or strict compliance requirements, evaluate on‑premises or private cloud options (e.g., FAISS, Milvus).

## When to choose which

* Choose FAISS when:
  * You need full control over index type, quantization, and memory layout.
  * You want to avoid vendor lock-in and manage your own infrastructure.
  * You require the highest possible raw performance and can handle operational complexity.

* Choose Pinecone when:
  * You want a hosted, scalable service that handles persistence, replication, and availability.
  * You prefer simple APIs with metadata filtering and fast time-to-production.
  * You want to offload operational complexity (monitoring, scaling) to a provider.

## Feature comparison

| Feature              | FAISS                                              | Pinecone                                                      |
| -------------------- | -------------------------------------------------- | ------------------------------------------------------------- |
| Type                 | Open-source library (C++/Python)                   | Managed vector database (SaaS)                                |
| Scaling              | Manual (you manage nodes/VMs)                      | Automatic/managed by provider                                 |
| Persistence & HA     | Manual (depends on your setup)                     | Built-in (managed)                                            |
| Index options        | `IndexFlatL2`, `IVF`, `HNSW`, `PQ`, `OPQ`, etc.    | Hides low-level index details; provides configuration options |
| Metadata filtering   | No built-in metadata DB; requires external mapping | Built-in metadata filtering                                   |
| Operational overhead | High (self-managed)                                | Low (managed)                                                 |
| Best for             | Custom tuning, on-premises, research               | Production cloud, rapid deployment                            |

## Other alternatives to consider

* [Annoy (Spotify)](https://github.com/spotify/annoy) — simple, disk-backed ANN index.
* [hnswlib](https://github.com/nmslib/hnswlib) — HNSW-based ANN with extremely fast queries.
* [Milvus](https://milvus.io/) — open-source vector database with both cloud and on-prem options.
* [Weaviate](https://www.semi.technology/) — vector search engine with semantic search and schema support.

These alternatives may be preferable depending on requirements for persistence, query latency, memory footprint, and deployment model.

## Links and References

* [FAISS GitHub](https://github.com/facebookresearch/faiss)
* [Pinecone](https://www.pinecone.io/)
* [NumPy](https://numpy.org/)
* [spaCy](https://spacy.io/)
* [Matplotlib](https://matplotlib.org/)
* [Annoy GitHub](https://github.com/spotify/annoy)
* [hnswlib GitHub](https://github.com/nmslib/hnswlib)
* [Milvus](https://milvus.io/)

Summary

* Correct answer: [FAISS](https://github.com/facebookresearch/faiss) or [Pinecone](https://www.pinecone.io/).
* FAISS and Pinecone are purpose-built for vector storage and similarity search; NumPy, spaCy, and Matplotlib are not appropriate as vector databases for RAG systems.

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/cce68739-7c5b-4b74-ae18-f9183b1accdc)


# RAG Component for Determining Document Relevance

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/RAG-Component-for-Determining-Document-Relevance/page

Explains RAG pipeline components and emphasizes the re-ranker as the component that determines retrieved documents' relevance to a user query.

Question 6.

In a RAG system implementation, which component is responsible for determining the relevance of retrieved documents to the user query?

Vector database, chunking mechanism, re-ranker, or tokenizer?

Answer: re-ranker.

A re-ranker is the component that determines the relevance of retrieved documents to the user query in a Retrieval-Augmented Generation (RAG) pipeline.

* The vector database performs the initial similarity-based retrieval (fast approximate nearest neighbors on embeddings).
* The re-ranker refines those initial results by applying more accurate relevance criteria. Typical re-rankers use cross-attention or cross-encoder architectures that jointly consider the query and each candidate document to compute a more accurate relevance score than simple embedding similarity.
* Chunking prepares long documents into pieces (chunks) so they fit model context windows and produce focused embeddings.
* Tokenizers convert raw text into tokens appropriate for the embedding model or language model.

This article explains how these components cooperate, why re-ranking matters, and how to implement a retrieval + re-ranking step.

## Quick flow (step-by-step)

1. The user asks a question.
2. The question is converted into an embedding that encodes its semantic meaning.
3. The vector database is searched using that embedding to retrieve the top-N candidate documents or chunks (initial retrieval).
4. The candidate documents are passed to a re-ranker which compares the original query against each candidate (typically using a cross-encoder or an LLM scoring method).
5. The re-ranker scores and reorders the candidates to place the most relevant items at the top.
6. The top-ranked documents are returned to the RAG pipeline (for example, used as context for a generative model).

## Component responsibilities and when to use them

| Component          | Primary role                                                                                         | Typical trade-offs                                             |
| ------------------ | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Vector database    | Fast initial retrieval of semantically similar documents using embeddings                            | High recall, low latency, but may produce noisy candidates     |
| Re-ranker          | Refines and reorders candidates by computing fine-grained relevance between query and candidate text | Higher precision, higher compute cost and latency              |
| Chunking mechanism | Splits long documents into manageable chunks for embedding and retrieval                             | Improves embedding quality and fit within model context window |
| Tokenizer          | Converts raw text into tokens and token IDs for models                                               | Low-level preprocessing; model-dependent behavior              |

## Why re-ranking improves RAG quality

* Embedding similarity methods are efficient but often approximate — they evaluate query-to-document similarity in a single vector space and can miss fine-grained signals.
* Re-rankers use models that jointly encode the query and document (cross-encoders) or use LLM-based scoring to capture contextual interactions, improving ordering and final relevance.
* Because re-rankers are more expensive, the typical pattern is: run a high-recall initial search (e.g., top 50–200) then re-rank to a much smaller set (e.g., top 3–10).

## Example retrieval + re-ranking pseudocode

```python theme={null}
