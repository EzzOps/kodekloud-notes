# When to Use Which Query Method Part 2

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Foundations/When-to-Use-Which-Query-Method-Part-2/page

Guidance on choosing vector similarity query methods — range thresholds, multi-vector, ANN, and two-stage retrieve-and-rerank — with trade-offs, use cases, and tuning tips.

Welcome back. In this lesson we continue from Part 1 and finish the remaining vector query methods used in modern similarity search systems. We explain when to choose each approach, the trade-offs you’ll face, and concise real-world examples you can use when designing or debating architectures with engineers and data scientists.

Key topics covered:

* Range / Threshold Search (quality-first filtering)
* Multi-Vector Search (multimodal queries)
* Approximate Nearest Neighbor (ANN) Search (scale and latency)
* Two-Stage Search (retrieve-and-rerank for both speed and accuracy)

## Range / Threshold Search

Range or threshold search filters results by a minimum similarity score rather than returning a fixed number of neighbors. Use this when you care about the absolute quality of each match instead of the top-K set.

When to use it

* You require high-confidence matches (not simply the top-k results).
* Correctness and compliance matter (e.g., legal, regulatory, or safety checks).
* You want deterministic filtering across different queries and model versions.

Real-world examples

* Plagiarism detection: return all documents with similarity > 0.85 to a submitted paper.
* Fraud detection: flag transactions with similarity > 0.9 against known fraudulent patterns.

Practical tip: validate thresholds on representative labeled data to balance precision and recall. Too low a threshold increases noise; too high misses borderline but valid matches.

<Callout icon="lightbulb">
  Thresholds are a filtering step. Choose them based on validation data: too low yields noise, too high may miss valid matches.
</Callout>

Example query patterns

* Generic threshold pseudocode:

```sql theme={null}
-- Pseudocode: filter by similarity score
SELECT id, similarity_score
FROM vector_index
WHERE similarity_score >= 0.8
ORDER BY similarity_score DESC;
```

* API-style:

```json theme={null}
{
  "query_vector": [0.01, 0.23, ...],
  "min_similarity": 0.8
}
```

## Multi-Vector Search (Multimodal Queries)

Multi-vector search is for queries that combine different input types (text, image, audio). Each modality gets encoded to its own vector and the system merges or scores them jointly to find items that satisfy multiple signals.

When to use it

* User queries include mixed modalities (e.g., image + text).
* You need results that match several signals simultaneously (visual features + textual intent).
* Cross-modal relevance is critical for user experience.

Real-world examples

* E-commerce: upload an image of a dress and type “red dress for summer” — the system merges image and text vectors to find matching inventory.
* Social media search: combine uploaded image, caption text, and hashtag vectors to surface relevant posts.

<Frame>
  <img alt="The image is an infographic titled &#x22;When to Use Which Query Method? - Part 2&#x22; and explains the use of Multi-Vector Search for multi-modal inputs with example use cases in e-commerce and social media." />
</Frame>

Implementation notes

* Fusion strategies include weighted dot-product sums, concatenation with a learned MLP, or late fusion via re-ranking.
* Tune modality weights based on validation metrics and user intent: e.g., if visual similarity is more important, raise image weight.

## Approximate Nearest Neighbor (ANN) Search

Approximate Nearest Neighbor (ANN) search is optimized for extremely large vector stores (millions to billions of vectors) where sub-second latency is required. ANN uses indexing structures and heuristics to return very likely nearest neighbors far faster than an exhaustive exact KNN scan, at a controlled loss in recall.

When to use it

* Very large datasets (millions–billions of vectors).
* Real-time or low-latency applications where slight accuracy trade-offs are acceptable.
* Services where throughput and fast tail latency are primary constraints.

Real-world examples

* Web-scale search (e.g., search engines): serving billions of documents with strict latency SLOs.
* Recommendation systems at scale (Spotify, Pinterest) where fast retrieval across massive catalogs is required.

<Frame>
  <img alt="The image is a table explaining when to use the Approximate Nearest Neighbor (ANN) query method, listing scenarios like large-scale databases and real-time apps, with example use cases from Google Search, Spotify, and Pinterest." />
</Frame>

Performance trade-offs and tuning

* ANN provides massive speedups but may reduce recall. Tune index parameters (e.g., number of probes, ef\_search, M) to balance latency vs. accuracy.
* Monitor recall/precision on labeled queries to guide the acceptable operating point.

<Callout icon="warning">
  ANN is a trade-off: optimize index parameters and measure recall on real query workloads. A misconfigured ANN index can silently degrade user experience.
</Callout>

Example ANN parameters (tool-specific)

```text theme={null}
