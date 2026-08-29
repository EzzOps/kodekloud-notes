# Vector Databases in RAG

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/n8n-RAG-Agent/Vector-Databases-in-RAG/page

Explains vector databases powering RAG by storing embeddings for semantic search, detailing RAG pipelines, similarity metrics, ANN indexing, and security and governance practices.

In this lesson we’ll explain vector databases and how they power Retrieval-Augmented Generation (RAG) systems. You’ll learn why RAG agents combine large language models with retrieval, what a vector database stores, and the typical RAG pipeline used in production systems.

What is a RAG agent?
A RAG (Retrieval-Augmented Generation) agent pairs an LLM with a retrieval system so the model can augment its generation with external, relevant information.

<Frame>
  <img alt="The image explains what a RAG Agent is, describing it as a combination of a large language model (LLM) with a retrieval system, accompanied by illustrative icons." />
</Frame>

Instead of relying only on knowledge encoded during pretraining, the agent pulls fresh, domain-specific content from a knowledge store. That retrieved content becomes additional context for the LLM, which helps produce more accurate, up-to-date, and grounded answers — reducing hallucinations and improving relevance.

Why this matters
Large language models are powerful but not infallible. They can produce plausible-sounding but incorrect responses. A retrieval step ensures the LLM’s output can be verified and tied to authoritative source material.

High-level RAG flow

* User issues a query.
* System retrieves the most relevant documents or passages from an external knowledge base.
* Retrieved content is provided to the LLM as contextual input.
* The LLM generates a response augmented by the retrieved material.

<Frame>
  <img alt="The image is a flowchart explaining a RAG (Retrieve and Augment Generation) agent process, involving a query, an AI agent, a database for retrieval and augmentation, and a response." />
</Frame>

To perform semantic matching — finding content that *means* the same thing, not just uses the same words — RAG systems use vector databases.

<Frame>
  <img alt="The image depicts a 3D plot showing various labeled points like &#x22;Wolf,&#x22; &#x22;Cat,&#x22; and &#x22;Apple,&#x22; demonstrating vectors in space, alongside text explaining that vector databases are specialized for storing and searching vectors (embeddings)." />
</Frame>

What is a vector database?

* A vector database stores embeddings: high-dimensional numeric vectors that encode the semantics of text, images, or other media.
* Embeddings capture meaning rather than surface tokens, so semantically related items map to nearby vectors in embedding space.
* Vector stores are optimized for nearest-neighbor / similarity search over high-dimensional vectors so queries return relevant content quickly.

How vector (semantic) search differs from keyword search

* Keyword search looks for exact tokens and phrase matches. Searching for “car” may miss content that uses “automobile” or related concepts.
* Vector-based semantic search finds conceptually similar content by comparing vector distances (e.g., cosine similarity), returning items that are relevant even when exact words differ.

<Frame>
  <img alt="The image explains the benefits of using vector databases in RAG, highlighting text storage as embeddings and enabling semantic search to find similar ideas." />
</Frame>

Key technical points

* Embeddings are numeric arrays (common sizes: 512, 768, 1024, or 1536 dimensions) produced by an encoder model.
* Similarity search uses metrics such as cosine similarity, dot product, or Euclidean distance.
* For large collections, vector databases use Approximate Nearest Neighbor (ANN) algorithms and indexes (e.g., HNSW, IVF) to return fast, high-quality matches while trading a small amount of recall for speed.

> **lightbulb** Vector databases store embeddings and provide fast nearest-neighbor search using specialized indexes. Typical similarity metrics include cosine similarity and dot product. Approximate algorithms (HNSW, IVF, etc.) trade a tiny amount of recall for significant speed and scale improvements.

Comparing semantic vs keyword search

| Search type              | Strengths                                                   | Typical use cases                                                      |
| ------------------------ | ----------------------------------------------------------- | ---------------------------------------------------------------------- |
| Keyword search           | Precise token matching, boolean queries, structured filters | Exact string matching, logs, code search                               |
| Semantic (vector) search | Finds conceptually similar content regardless of wording    | QA over documents, FAQ matching, recommendation, multi-modal retrieval |

Typical RAG pipeline (practical steps)

1. Chunk and preprocess source documents (split long documents into smaller passages).
2. Convert each passage into an embedding using an embedding model (e.g., OpenAI embeddings, or open-source encoders).
3. Insert embeddings into the vector database along with metadata (document ID, snippet, source URL, timestamps).
4. When a user asks a question, convert the query into an embedding.
5. Perform a similarity search in the vector store to retrieve the top-k most relevant passages.
6. Provide those retrieved passages to the LLM (usually via a prompt template) so the model can generate a grounded response.

In orchestration platforms like [n8n: Zero to Hero](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero-2) the pattern is the same: embed → store → retrieve → augment → generate.

Security and governance

* Access control: limit who and which services can query or export vectors and metadata.
* Data minimization: avoid storing sensitive fields in raw form when not needed.
* Encryption: encrypt data at rest and in transit for both vectors and metadata.
* Audit logging: record retrievals and updates to detect inappropriate access.

> **warning** Be cautious about storing sensitive data in vector stores. Embeddings can reveal information about the underlying text, and retrieval may expose private content. Apply access controls, encryption, and data governance policies as needed.

Summary

* RAG agents combine LLMs with an external retrieval step to produce more accurate, verifiable, and current answers.
* Vector databases enable semantic search by storing embeddings and performing nearest-neighbor lookups, not just keyword matches.
* The core RAG pipeline is: chunk → embed → index → retrieve → augment → generate. This approach reduces hallucinations and improves relevance for document-grounded tasks.

Links and references

* [Retrieval-Augmented Generation (overview)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
* [Approximate Nearest Neighbors (ANN) algorithms — HNSW, IVF](https://en.wikipedia.org/wiki/Approximate_nearest_neighbor_search)
* \[Open-source vector databases: Milvus, Faiss, Annoy, Weaviate]

- [Watch Video](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/0fde2722-cb9f-4240-bedb-c3dbcb75ba79/lesson/a6a26092-2d7c-4f8a-b42e-8232d7a6feaf)
