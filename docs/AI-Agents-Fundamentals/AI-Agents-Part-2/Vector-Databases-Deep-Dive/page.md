# Vector Databases Deep Dive

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-2/Vector-Databases-Deep-Dive/page

Describes how embeddings and vector databases power semantic search and RAG, including chunking, similarity metrics, indexing options, and deployment trade offs for production

Large language models (LLMs) rely on a context window to process input and generate useful responses. When an organization like TechCorp needs to search 500 GB of internal documents, traditional keyword search struggles with semantic variation (e.g., “vacation” vs “time off”). Embeddings and vector databases enable semantic search at scale and are a common foundation for retrieval-augmented generation (RAG) applications built with frameworks such as LangChain.

<Frame>
  <img alt="A hand-drawn chalkboard-style diagram labeled &#x22;Tech Corp's AI Application&#x22; sits in the center with arrows radiating outward. It links to sketches of components like a Large Language Model, LangChain pipeline, R.A.G., prompt engineering, and a vector/database icon." />
</Frame>

Problem scenario

* Suppose the 500 GB dataset contains an employee handbook covering policies like time off, dress code, and equipment use.
* Users may phrase the same intent using different words: “vacation policy”, “time off guidelines”, or “Can I request time off on a holiday?” Keyword-based search often misses relevant content unless the exact words are present.

Traditional SQL / keyword approach

* SQL and text-index approaches use exact or pattern matching (LIKE, full-text search). Users must guess correct words or rely on manual synonym expansion.

```sql theme={null}
-- Traditional SQL approach: keyword search
SELECT * FROM documents
WHERE content LIKE '%Vacation%' OR content LIKE '%vacation policy%';

-- Example user query:
-- "Can I request time off on a holiday?"
```

* Drawbacks: brittle to phrasing, requires query engineering, and often produces noisy or incomplete results.

Why embeddings + vector databases?

* Embeddings convert text into fixed-length numeric vectors that capture semantic meaning. Related texts (e.g., “vacation” and “holiday”) map to nearby vectors in the embedding space.
* When a user asks a natural language question, the system compares the embedding of the query with document embeddings and returns semantically similar content even if the wording differs.
* This approach is ideal for RAG systems and LLM-driven assistants because it surfaces relevant context without retraining the LLM.

Popular vector databases and when to use them

| Vector Database | Best Use Case                                     | Notes                                                 |
| --------------- | ------------------------------------------------- | ----------------------------------------------------- |
| Pinecone        | Production-grade semantic search at scale         | Managed service, easy integration, strong performance |
| ChromaDB        | Local prototyping and small-to-medium deployments | Open-source, developer-friendly embedding store       |

(Also commonly used: FAISS for offline/embedded ANN indexing, Milvus for large-scale open-source vector search.)

Embeddings: turning text into meaning

* Embedding models map text chunks (sentences, paragraphs) to numeric vectors. Similar meanings yield nearby vectors.
* Example workflow:
  1. Split documents into chunks (paragraphs or sections).
  2. Call an embedding model to convert each chunk into a vector.
  3. Store vectors in a vector DB with metadata (source, offsets, timestamps).
  4. For a user query, embed the query and retrieve the nearest vectors (top-K or above a threshold).
* Benefit: the LLM receives relevant passages for context regardless of exact phrasing.

Dimensionality trade-offs

| Dimension size | Pros                                                  | Cons                                               |
| -------------- | ----------------------------------------------------- | -------------------------------------------------- |
| \~256          | Lower storage & compute                               | May miss fine-grained semantic distinctions        |
| \~768–1536     | Good semantic expressiveness (common for many models) | Higher storage & retrieval cost                    |
| >1536          | Captures more nuance                                  | Increased cost; diminishing returns beyond a point |

* Choose dimensionality based on the embedding model you select and the latency/storage budget.

Retrieval: scoring and chunking
Two core decisions determine retrieval quality: similarity scoring and how you chunk documents.

Scoring / similarity metrics

* Common similarity measures:
  * Cosine similarity: robust when vectors are length-normalized.
  * Dot product: often used for models that produce normalized vectors or when scaling factors matter.
* Index types:
  * Exact: brute-force nearest neighbors (slow for large corpora).
  * ANN (approximate): e.g., HNSW — trades minimal accuracy for large speed and memory gains.
* Tuning:
  * Choose top-K results and/or a similarity threshold to filter noisy matches.
  * Too-low thresholds can return loosely related content (false positives); too-high may omit relevant passages.

Chunking and overlap

* Rather than embedding whole documents, split into chunks (paragraphs, sliding windows) and embed each chunk.
* Overlap windows (e.g., 200-token chunks with 50-token overlap) preserve context across boundaries.
* Trade-offs:
  * Smaller chunks → more precise matches, but more vectors to store and search.
  * Larger chunks → fewer vectors but higher risk of mixing topics and lowering retrieval precision.

Comparison: SQL vs Vector-based retrieval

| Characteristic           | SQL / Keyword Search              | Vector / Embedding Search                     |
| ------------------------ | --------------------------------- | --------------------------------------------- |
| Query type               | Keyword/pattern matching          | Natural language / semantic                   |
| Robustness to paraphrase | Low                               | High                                          |
| Setup complexity         | Low                               | Medium–High (embeddings, chunking, indexes)   |
| Best for                 | Exact matches, structured queries | Unstructured documents, LLM context retrieval |

Operational considerations and trade-offs

* Design choices: embedding model, dimensionality, chunk size, overlap, similarity metric, ANN configuration, scoring thresholds.
* Costs: storage for vectors, runtime cost of embedding generation, and compute for ANN queries.
* Monitoring: track retrieval precision, false positives, and downstream LLM output quality to iterate on knobs.
* Integration: vector DBs pair well with LangChain-style retrieval chains and RAG pipelines for chatbots and assistants.

<Frame>
  <img alt="A hand-drawn diagram comparing a traditional SQL database (rows, user burden) on the left to a vector database workflow on the right, showing retrieval feeding into scoring and chunk-overlap and then into an LLM. The sketch highlights chunking, overlap arrows, and notes like &#x22;no training required.&#x22;" />
</Frame>

Resources and next steps

* Prototype: use a small subset of documents with an open-source embedding model and Chroma/FAISS to validate chunk size and overlap choices.
* Production: evaluate managed options (Pinecone, managed Milvus) for indexing, scaling, and operational support.
* RAG integration: feed retrieved chunks into your LLM prompt or LangChain retrieval chain and measure answer quality.

<Callout icon="lightbulb">
  When designing a vector-backed retrieval system, treat embedding creation, chunking strategy, similarity metric, and scoring thresholds as tunable knobs. Proper configuration upfront reduces noise in retrieval and improves downstream LLM responses.
</Callout>

Links and references

* [LangChain course](https://learn.kodekloud.com/user/courses/langchain)
* [Fundamentals of RAG](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)
* [Pinecone](https://www.pinecone.io)
* [ChromaDB](https://www.trychroma.com)
* [Kubernetes Documentation](https://kubernetes.io/docs/) (general infra reference)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/ff68d510-a374-46e6-ac61-0ac106069c3b/lesson/35e732e6-79e8-483e-8c3c-f0aa2fa00da4" />
</CardGroup>
