# Example (HNSW-style) tuning knobs:
- M (max neighbors per node): 16–64
- efConstruction (index build time): 200–1000
- efSearch (query quality vs latency): 50–200
```

## Two-Stage Search (Retrieve-and-Rerank)

Two-stage search (retrieve-and-rerank) mixes a fast retrieval stage with a more expensive re-ranking stage. Typically you use an ANN or lightweight vector index to fetch a candidate set, then apply a stronger cross-encoder or business-logic-aware model to re-rank the candidates.

When to use it

* You need both low latency and high final ranking quality.
* Ranking must incorporate complex signals: recency, personalization, seller priorities, or business rules.
* The quality of the top results (e.g., top 10) is critical to user satisfaction.

Real-world examples

* Search engines: retrieve \~1000 candidates with ANN, rerank the top subset using a cross-encoder, and display the best \~10 results.
* E-commerce: retrieve product candidates, then rerank by personalization, conversion likelihood, and business constraints.

Benefits

* Keeps initial retrieval cheap and scalable.
* Allows sophisticated models to focus on a much smaller candidate set, improving final relevance without prohibitive cost.

<Frame>
  <img alt="The image is a table explaining when to use a two-stage search with re-ranking, detailing the query method, use cases, and examples such as speed, accuracy, and complex ranking factors in environments like e-commerce and search engines." />
</Frame>

Architecture example

* Stage 1 (fast): ANN -> 1,000 candidates
* Stage 2 (expensive): cross-encoder or ensemble model -> rerank top 100 -> final top 10

## Comparison Table

| Query Method                  | Best For                      | Pros                                           | Cons                                               | Example Use Cases                               |
| ----------------------------- | ----------------------------- | ---------------------------------------------- | -------------------------------------------------- | ----------------------------------------------- |
| Range / Threshold Search      | High-confidence filtering     | Deterministic quality control, simple          | May return variable counts, sensitive to threshold | Plagiarism, compliance checks                   |
| Multi-Vector Search           | Multimodal queries            | Captures multiple modalities, richer relevance | More complex encoding/fusion                       | Image+text e-commerce, multimodal social search |
| ANN Search                    | Very large scale, low latency | Extremely fast, scalable                       | Potential recall loss; requires tuning             | Web search, large recommenders                  |
| Two-Stage (Retrieve & Rerank) | Speed + high-quality ranking  | Balances latency and top-result quality        | More complex pipeline, higher cost                 | Search engines, conversion-optimized e-commerce |

## Summary — Choosing the Right Strategy

* Range / Threshold: Use when you must enforce a strict quality bar for each returned item.
* Multi-Vector: Use when user intent spans multiple modalities and you need joint relevance.
* ANN: Use for massive datasets and strict latency requirements where a small accuracy trade-off is acceptable.
* Two-Stage (Retrieve-and-Rerank): Use when you need both fast retrieval and the highest-quality top results incorporating complex signals.

With these patterns and trade-offs in mind, you’ll be better prepared to design vector search systems that match your performance, accuracy, and business requirements. Discuss these options with engineers and data scientists to select the right combination for your product.

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [ANN Index Tuning (HNSW)](https://arxiv.org/abs/1603.09320)
* [Multimodal Retrieval Research](https://arxiv.org/abs/2003.04659)

That is it for this lesson. See you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/82014ec3-9709-44d1-bd41-577af87083ed/lesson/ab950728-bc57-4187-9608-0c29b569e5a6" />
</CardGroup>


# Cosine Similarity

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Similarity-Explained/Cosine-Similarity/page

Explains cosine similarity as an angle-based vector comparison that ignores magnitude, used for measuring semantic similarity in text embeddings and semantic search.

Welcome back.

In this lesson we'll take a focused look at cosine similarity — a fundamental technique for comparing vectors in high-dimensional spaces. At a high level, cosine similarity answers the question: are two vectors pointing in the same direction? It measures the angle between them, not their lengths.

A few key points:

* Each vector can be thought of as an arrow in n-dimensional space.
* Cosine similarity depends on the angle between vectors, so differences in magnitude (length) do not change the similarity if the direction remains the same.
* When two vectors point in the same direction, their cosine similarity approaches `1`. If they are orthogonal, the similarity is `0`. Opposite directions yield `-1`.

<Callout icon="lightbulb">
  Cosine similarity focuses on angular alignment between vectors. Differences in magnitude (length) are ignored, which makes it ideal for comparing semantic content across short and long texts.
</Callout>

Mathematical definition:

```text theme={null}
cos(θ) = (A · B) / (‖A‖ * ‖B‖)

Where:
- A · B is the dot product of vectors A and B
- ‖A‖ and ‖B‖ are the magnitudes (L2 norms) of A and B
- cos(θ) ∈ [-1, 1]
```

Canonical angle cases:

* `θ = 0°` → cos = `1` : vectors point in exactly the same direction (highly similar).
* `θ = 90°` → cos = `0` : vectors are orthogonal (no directional relationship).
* `θ = 180°` → cos = `-1` : vectors point in opposite directions (maximally different).

Practical reasons cosine similarity matters

1. Robustness to document length differences\
   Cosine similarity ignores vector magnitude. For search and retrieval, this means a short query can match a long document based on topic alignment rather than penalizing the longer document for having more words.

2. Short vs. long text matching\
   A short social post and a long article can still be recognized as semantically similar because cosine similarity compares direction (topic) rather than raw count.

3. Widely adopted default for text embeddings and semantic search\
   Many embedding models and vector databases default to cosine similarity because it captures topical alignment across documents of different lengths.

<Frame>
  <img alt="The image explains cosine similarity, focusing on measuring angles between vectors to determine similarity based on direction. It includes visual examples and highlights why cosine similarity matters in computing document similarity." />
</Frame>

Example: news recommendation\
Imagine a user's short query about "inflation and interest rates" and a full-length economics article on the same topic. Despite a 20-word query and a 1,000-word article, cosine similarity will identify strong topical alignment because the direction of their embedding vectors is similar.

Industry adoption\
OpenAI's text embeddings, SentenceTransformers, and many vector databases prefer cosine similarity for semantic search.

They all default to cosine similarity for text-based search.

<Frame>
  <img alt="The image explains cosine similarity with a diagram showing vectors and examples of angles between them. It highlights that cosine similarity focuses on direction, not length, and provides practical applications." />
</Frame>

When you build a semantic search system or a RAG (Retrieval-Augmented Generation) pipeline, cosine similarity is usually the first similarity metric to try — it answers "Are these documents about the same thing?" regardless of how much each document expresses that topic.

Cosine similarity vs. Euclidean distance

| Metric             |                                                 What it measures | When to use                                                                                                                          |
| ------------------ | ---------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------ |
| Cosine similarity  | Directional alignment (angle) between vectors; ignores magnitude | Best for semantic search, text embeddings, when document length varies                                                               |
| Euclidean distance |                      Absolute distance in vector space (L2 norm) | Useful when magnitude and absolute distances matter (e.g., low-dimensional feature spaces, clustering with scale-sensitive features) |

Quick implementation note (pseudocode):

```python theme={null}
