# Given vectors a and b:
dot = sum(ai * bi for ai, bi in zip(a, b))
norm_a = sqrt(sum(ai * ai for ai in a))
norm_b = sqrt(sum(bi * bi for bi in b))
cosine_similarity = dot / (norm_a * norm_b)
```

References and further reading

* [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
* [SentenceTransformers (SBERT)](https://www.sbert.net/)
* [Pinecone Vector Database](https://www.pinecone.io/)
* [Weaviate](https://weaviate.io/)
* [Fundamentals of RAG](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)

That's the essence of cosine similarity: a compact, direction-focused similarity measure that excels in semantic tasks. Euclidean distance is another common metric and can be preferable when absolute vector magnitudes and raw distances are meaningful for your application.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/e0eab5c9-aa81-4399-bd93-e354acb9a7bc)


# Three Ways to Measure Similarity

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Similarity-Explained/Three-Ways-to-Measure-Similarity/page

Describes cosine similarity, Euclidean distance, and dot product and their applications for semantic search, recommendations, and retrieval

Welcome back.

In machine learning and vector databases, measuring similarity between vectors is a fundamental task. After you store embeddings in a vector store, the retrieval logic—how you compare an incoming query vector to stored vectors—determines the relevance of results. Should you require exact matches, or return nearest neighbors? Which similarity or distance metric best captures semantic similarity for your use case? Picking the right metric is essential for building effective semantic search, recommendation engines, and RAG (retrieval-augmented generation) systems.

This article explains the three most common approaches to compare vectors: cosine similarity, Euclidean distance, and the dot product. For each method you'll get the intuition, the formula, the numeric range, and practical guidance for when to use it.

Why this choice matters

* The metric determines which candidates are considered “close” and therefore returned to downstream systems.
* Embedding generation (model architecture, normalization) often dictates which metric is appropriate.
* Wrong choices can yield results that are numerically close but semantically irrelevant.

Cosine similarity

* Intuition: measures the angle between two vectors and ignores their magnitudes. Vectors pointing in the same direction are similar regardless of length.
* Formula: `cosine(u, v) = (u · v) / (||u|| ||v||)`
* Range: `-1` to `1` (`1` = same direction, `0` = orthogonal/unrelated, `-1` = opposite).
* When to use: ideal for text embeddings and semantic search where topic/ direction matters more than length. Short and long texts about the same topic can still be similar.
* Typical usage: commonly used with text embedding services such as [OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings) and supported by vector databases like [Pinecone](https://www.pinecone.io/).

Euclidean distance

* Intuition: the straight-line distance between two points in vector space (like measuring with a ruler). It depends on magnitude.
* Formula: `euclidean(u, v) = ||u - v||`
* Range: `0` to `∞` (`0` = identical vectors; larger values = more distant).
* When to use: appropriate when absolute magnitude encodes important information, for example in some image similarity tasks, sensor measurements, or anomaly detection where vector length represents intensity or scale.
* Typical usage: supported by vector databases such as [Weaviate](https://weaviate.io/) and often used in computer vision scenarios.

Dot product (inner product)

* Intuition: combines direction and magnitude — it measures alignment while scaling by vector lengths.
* Formula: `dot(u, v) = Σ u_i * v_i`
* Range: `-∞` to `+∞` (unbounded).
* When to use: useful when both direction and magnitude matter, for example recommendation systems where raw model outputs (scores) are meaningful and should affect ranking.

> **lightbulb** Practical tip: if you normalize all vectors to unit length, the dot product becomes equivalent to cosine similarity. Normalization is common when you want to remove magnitude and compare only direction.

Quick comparison table

| Metric             | Intuition                              | Numeric range | Use cases                                            | Common tools                  |
| ------------------ | -------------------------------------- | ------------: | ---------------------------------------------------- | ----------------------------- |
| Cosine similarity  | Angle between vectors; ignores length  |   `-1` to `1` | Text/semantic search, when topic matters over length | `OpenAI embeddings`, Pinecone |
| Euclidean distance | Straight-line distance; uses magnitude |    `0` to `∞` | Vision tasks, sensor intensity, anomaly detection    | Weaviate, FAISS               |
| Dot product        | Alignment weighted by magnitude        |  `-∞` to `+∞` | Recommenders, when magnitudes encode signal          | Model scoring, ANN libraries  |

How to choose between them

* If you care only about semantic direction/topic and want to ignore length differences, use cosine similarity (or normalize vectors and use dot product).
* If absolute magnitude encodes meaningful signals (intensity, confidence, energy), prefer Euclidean distance or unnormalized dot product.
* Use dot product when the model’s raw outputs (magnitudes) should directly influence ranking or scoring.

<Frame>
  <img alt="The image describes three ways to measure similarity: Cosine Similarity (measures the angle between vectors), Euclidean Distance (measures straight-line distance), and Dot Product (combines direction and magnitude). Each method's range is also illustrated." />
</Frame>

Before finalizing a metric, inspect how your embeddings are produced and whether vector magnitudes carry semantic meaning. If needed, experiment with normalization and test retrieval quality on held-out queries to evaluate real-world relevance rather than relying purely on numeric closeness.

Further reading and references

* [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
* [Pinecone Vector Database](https://www.pinecone.io/)
* [Weaviate Vector Search](https://weaviate.io/)
* [FAISS — Facebook AI Similarity Search](https://github.com/facebookresearch/faiss)
* [Milvus — an open-source vector database](https://milvus.io/)

That’s it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/674e62ac-3920-4ef6-bb4a-3854aa6db8f3)
