# Lightweight, fast model suitable for many evaluation tasks
model = SentenceTransformer('all-MiniLM-L6-v2')

generated = "A quick brown fox jumps over the lazy dog."
reference = "A fast brown fox leaps over a sleeping dog."

# Encode texts to embeddings (use convert_to_tensor=True for GPU/fast cosine)
emb_gen = model.encode(generated, convert_to_tensor=True)
emb_ref = model.encode(reference, convert_to_tensor=True)

# Cosine similarity between embeddings (value typically between -1 and 1)
similarity = util.cos_sim(emb_gen, emb_ref).item()
print(f"Cosine similarity: {similarity:.4f}")
```

Interpreting the result:

* Values closer to 1 indicate higher semantic similarity.
* Values near 0 indicate little semantic relation.
* Values near -1 are rare for sentence embeddings but indicate opposite directions in vector space.

Comparison: which library to choose

| Library               | Use case for LLM evaluation                                                                   | Example / Notes                                         |
| --------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Sentence Transformers | Best for semantic similarity, embedding-based comparisons, and clustering                     | `from sentence_transformers import SentenceTransformer` |
| NumPy                 | Fundamental numeric operations and array math used downstream (not for embeddings themselves) | Use for manipulating vectors once obtained              |
| Matplotlib            | Visualization of results (e.g., similarity distributions, ROC curves)                         | Not for computing semantic similarity                   |
| pandas                | Organizing and analyzing tabular evaluation results (scores, metadata)                        | Great for storing per-sample metrics                    |

Why not the others?

* NumPy: Core numerical library but does not provide pretrained text embeddings or semantic models.
* Matplotlib: Useful for plotting evaluation outputs, not for producing embeddings or similarity metrics.
* pandas: Ideal for organizing results and aggregating metrics, but not designed to compute semantic similarity directly.

> **lightbulb** Tip: Select a model based on your accuracy/latency needs — `all-MiniLM-L6-v2` is efficient for bulk evaluations, while larger models (or fine-tuned ones) can yield higher semantic fidelity. For large-scale comparisons, use batch encoding and enable GPU acceleration where available.

Links and references

* [Sentence Transformers (SBERT)](https://www.sbert.net/)
* [Hugging Face Models](https://huggingface.co/models)
* [NumPy Documentation](https://numpy.org/doc/)
* [pandas Documentation](https://pandas.pydata.org/docs/)
* [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/nvidia-generative-ai-llms-associate-certification/module/607ae39a-4ae7-4cfb-92a5-564d0bda12cb/lesson/caba3333-fa51-4ac6-9e04-5fc53970c7ee)


# Python Package for RAG Vector Database Implementation

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Software-Development/Python-Package-for-RAG-Vector-Database-Implementation/page

Comparing FAISS and Pinecone as Python vector database options for storing and searching embeddings in Retrieval Augmented Generation systems, with examples and alternative tools.

Question 2.

Which Python package is most appropriate for implementing a vector database to store embeddings in a Retrieval Augmented Generation (RAG) system? NumPy, spaCy, FAISS or Pinecone, or Matplotlib?

Answer: [FAISS](https://github.com/facebookresearch/faiss) or [Pinecone](https://www.pinecone.io/).

Both FAISS and Pinecone are purpose-built for efficient storage and similarity search of high-dimensional vectors (embeddings) and are the right choices for vector databases in RAG systems.

> **lightbulb** FAISS and Pinecone both provide fast nearest-neighbor (similarity) search for dense vectors. Use FAISS for an on-premises, highly configurable, high-performance solution; use Pinecone for a managed, hosted vector database that minimizes operational overhead.

## Why FAISS or Pinecone?

Both systems are optimized for Approximate Nearest Neighbor (ANN) search, which is essential when your RAG pipeline needs fast similarity queries across many embeddings.

* FAISS (Facebook AI Similarity Search)
  * Open-source C++ library with Python bindings.
  * Extremely fast and memory-efficient; provides many indexing strategies such as `IndexFlatL2`, `IVF`, `HNSW`, `PQ`, and `OPQ`.
  * Best when you need fine-grained control over index type, quantization, and memory layout.
  * Ideal for on-premises deployments or self-managed cloud instances.

* Pinecone
  * Fully managed vector database service.
  * Handles scaling, replication, persistence, and operational concerns for you.
  * Simple APIs for upsert, query, and metadata filtering.
  * Best when you want a hosted, production-ready solution with minimal ops work.

## Why not the others?

* [NumPy](https://numpy.org/): Excellent for numerical operations and preprocessing embeddings, but not designed for efficient ANN indexing or production-scale similarity search.
* [spaCy](https://spacy.io/): A robust NLP toolkit (tokenization, parsing, embeddings generation), but not a vector database or ANN index.
* [Matplotlib](https://matplotlib.org/): A visualization library; irrelevant for storing/searching vectors.

## Quick examples

FAISS (local example)

```python theme={null}
import faiss
import numpy as np
