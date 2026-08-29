# The API response contains the embedding vector:
# embedding.data[0].embedding -> [0.032, -0.112, 0.540, 0.891, -0.234, 0.678, ...]
# (vector truncated; embeddings may have hundreds or thousands of dimensions)
```

Each element of the vector contributes to positioning the text in semantic space; the vector as a whole represents meaning, not random numbers.

## Storage and retrieval: vector databases

Embeddings are most useful when stored in vector databases designed for similarity search at scale. These systems use specialized indexes (including approximate nearest neighbor algorithms) to find the closest vectors quickly, even across millions or billions of items.

Common steps when preparing documents for a RAG system:

1. Convert each document (or document chunk) into an embedding using a chosen model.
2. Store embeddings and metadata (document IDs, text, source, timestamps) in a vector database.
3. At query time, embed the user query with the same model and search the vector DB for nearest neighbors.
4. Use the top retrieved documents as grounding context for an LLM to generate factual, relevant responses.

<Callout icon="lightbulb">
  Always embed both your documents and user queries with the same embedding model — mixing models will produce inconsistent vector spaces and degrade similarity results.
</Callout>

Vector database examples

| Vector DB                                                                                | Use case                                                     |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `Pinecone` ([pinecone.io](https://www.pinecone.io/))                                     | Managed vector DB with production-ready indexing and scaling |
| `FAISS` ([github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)) | High-performance local/cluster library for ANN search        |
| `Chroma` ([trychroma.com](https://www.trychroma.com/))                                   | Lightweight open-source vector store for prototyping         |
| `Weaviate` ([weaviate.io](https://weaviate.io/))                                         | Schema-driven vector DB with semantic search features        |

## Why embeddings power RAG systems

Embeddings enable RAG systems to:

* Perform semantic matching by placing queries and documents in the same vector space.
* Reduce hallucinations by grounding LLM outputs in retrieved, relevant documents.
* Support dynamic knowledge: add or update embeddings as information changes without retraining the LLM.

<Frame>
  <img alt="The image explains why RAG (Retrieval-Augmented Generation) needs embeddings, highlighting semantic matching, reduced hallucinations, and dynamic knowledge." />
</Frame>

## Choosing an embedding model: trade-offs

Model selection is a balance of accuracy, speed, and cost:

| Consideration         | Trade-off                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| Dimensionality & size | Larger models often yield higher-quality vectors but increase storage and compute costs.                      |
| Latency               | Smaller models return embeddings faster and at lower cost — useful for high-throughput systems or prototypes. |
| Accuracy              | Higher-fidelity embeddings improve retrieval relevance and downstream LLM performance.                        |
| Total cost            | Evaluate total cost of ownership: embedding count, dimensionality, query volume, and infrastructure.          |

For enterprise-grade systems where accuracy is critical, invest in higher-quality embeddings and thorough evaluation. For prototypes or cost-sensitive deployments, smaller models can provide acceptable performance with lower cost and latency.

## Key takeaways

* Meaning as math: embeddings convert words and sentences into numerical vectors that capture semantic relationships.
* Semantic search: embeddings enable retrieval by meaning rather than exact text matches.
* RAG foundation: embeddings allow LLMs to draw on relevant, retrieved context for grounded responses.
* Quality matters: better embeddings yield more accurate, reliable, and performant retrieval-based systems.

<Frame>
  <img alt="The image displays four key takeaways titled &#x22;Meaning as Math,&#x22; &#x22;Semantic Search,&#x22; &#x22;RAG Foundation,&#x22; and &#x22;Quality Matters,&#x22; each with an illustrative icon. The slide is labeled &#x22;Key Takeaways&#x22; with a dark background." />
</Frame>

Embeddings are the quiet engine behind semantic search and RAG: they bridge natural language and vector mathematics so systems can find and retrieve the information that best matches user intent.

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/) (general infrastructure reference)
* [Pinecone](https://www.pinecone.io/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Chroma](https://www.trychroma.com/)
* [Weaviate](https://weaviate.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/14bc5c47-4554-4c21-9f00-67c0f7e7f17d/lesson/2cc0d546-f34e-4f31-9ed3-768c4fffaf84" />
</CardGroup>


# Demo ChromaDB Implementation

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Vector-Databases/Demo-ChromaDB-Implementation/page

Guide to building a persistent local ChromaDB semantic search using SentenceTransformers embeddings, text chunking, idempotent ingestion, and similarity queries with optional metadata filters.

In this hands-on guide we'll build a local ChromaDB-backed semantic search workflow that persists to disk and demonstrates both ingestion and similarity queries using SentenceTransformers embeddings.

What you'll end up with:

* A persistent local ChromaDB instance.
* A simple ingestion flow that chunks text files and upserts embeddings.
* A query function that runs similarity searches with optional metadata filters.

Dataset used in this demo: several public-domain texts such as The Adventures of Huckleberry Finn, Sherlock Holmes, Beowulf, Complete Works of William Shakespeare, and Frankenstein.

<Frame>
  <img alt="This image shows an open Visual Studio Code window with a file explorer on the left displaying several text files. The terminal at the bottom indicates a command line in use." />
</Frame>

Note: this is a demo of using a vector database for retrieval. It is not a complete search engine (there are additional components like LLM-based re-ranking, result aggregation, and QA prompt engineering you would add later).

<Callout icon="warning">
  This lesson/article demonstrates basic ingestion and retrieval with [ChromaDB](https://www.trychroma.com/). You will get document hits and snippet-level results but not a fully featured QA system out of the box. Consider adding an LLM re-ranker and result post-processing for production-quality answers.
</Callout>

<Callout icon="lightbulb">
  Tip: If you run into compatibility issues with `PersistentClient`, check your installed chromadb version and adapt to `chromadb.Client(...)` or the version-appropriate persistent API. Also consider pinning `chromadb` and `sentence-transformers` versions in a `requirements.txt` for reproducible environments.
</Callout>

## Quick overview

The demo demonstrates:

* Setting a local persistence path for ChromaDB.
* Using a SentenceTransformers model to produce embeddings.
* Reading `.txt` files from `data/`, chunking long documents into overlapping segments, and creating deterministic chunk IDs for idempotent ingestion.
* Upserting (idempotent) into a Chroma collection.
* Running similarity queries with optional `where` metadata filters.

Files produced in this example:

| File                  | Purpose                                                                        |
| --------------------- | ------------------------------------------------------------------------------ |
| `ingest_and_query.py` | Ingests `.txt` files into ChromaDB, then runs demo queries.                    |
| `data/*.txt`          | Source plain-text documents to index (e.g., `beowulf.txt`, `shakespeare.txt`). |

## Environment and dependencies

Create and activate a Python virtual environment, then install required packages.

```bash theme={null}
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install chromadb sentence-transformers
```

Note: Installing `sentence-transformers` can pull several dependencies (transformers, torch) depending on your environment. Consider using a GPU-enabled environment or CPU-only builds as appropriate.

## Implementation — single consolidated script

Below is a consolidated, cleaned-up example that shows the key steps. Save as `ingest_and_query.py` (or split into `ingest.py` and `query.py` if you prefer to separate concerns).

```python theme={null}
