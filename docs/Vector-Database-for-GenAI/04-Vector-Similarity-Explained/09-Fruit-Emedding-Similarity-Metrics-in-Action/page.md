# Fruit Emedding Similarity Metrics in Action

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Similarity-Explained/Fruit-Emedding-Similarity-Metrics-in-Action/page

Demonstrates a fruit recommendation example showing how different embedding similarity metrics like Euclidean, cosine, and dot product affect nearest neighbor rankings

Welcome back. In this lesson we move from theory to practice by building a tiny fruit recommendation example and experimenting with different similarity metrics on embeddings. The central question is: someone picks mango — which other fruits are most similar?

This is the exact kind of query used by product recommendation engines, semantic search systems, and retrieval-augmented generation (RAG) pipelines. We use a compact, concrete example to illustrate how similarity search works and how metric choice affects ranking.

## Scenario and dataset

We store the following items in a vector database:

* Query fruit: mango
* Other fruits in the database: pineapple, banana, orange, papaya, lemon

Each fruit is encoded as a 3-dimensional vector with components: sweetness, sourness, and tropicalness. The image below visualizes those vectors and highlights some high-level observations.

<Frame>
  <img alt="The image displays a table titled &#x22;Fruit Embedding Demo&#x22; that presents various fruits and their properties (sweetness, sourness, tropical) in a vector format, alongside key observations about their similarities." />
</Frame>

## Interpreting the vectors

Each fruit vector locates the item in a 3D feature space (sweetness, sourness, tropicalness). When comparing fruits you compare vectors — not isolated features. Which dimensions matter depends on the question you ask:

* “Find a fruit with the same sweetness as mango” — prioritize the sweetness component.
* “Find a fruit like mango but less tropical” — prioritize tropicalness.
* “Find similar fruits to mango” — compare the full vector using a similarity or distance metric.

Important: a tabular listing of vectors (like the image above) does not imply geometric proximity — proximity must be computed using a metric.

## 2D projection for intuition

Projecting the vectors into two dimensions (for example, sweetness vs tropicalness) helps build visual intuition. Below, mango is the query point and other fruits are plotted relative to it. Note: the sourness axis is not shown, so the 2D projection only approximates true 3D proximity.

<Frame>
  <img alt="The image shows a 2D plot comparing fruits based on sweetness and tropical score, highlighting mango as a query point. It includes visual insights about the proximity of other fruits like banana, orange, lemon, apple, and grape to the mango." />
</Frame>

From this projection you can typically observe:

* Banana appears very close to mango (both sweet and tropical).
* Orange is moderately close.
* Lemon is far away (low sweetness, low tropicalness).
* Pineapple and papaya are tropical and may appear near mango depending on their sweetness and sourness.

## Why the metric matters

Visual inspection is useful for intuition, but exact ranking requires choosing a similarity or distance metric. Common metrics:

| Metric             | What it measures                                                   | When to use                                                                        |
| ------------------ | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Euclidean distance | L2 distance between vectors — absolute difference in feature space | Use when absolute differences in features matter (exact sweetness levels)          |
| Cosine similarity  | Angle between vectors (directional similarity)                     | Use when relative proportions matter and you want size-invariant similarity        |
| Dot product        | Raw inner product — depends on alignment and magnitude             | Use when vector magnitude encodes importance (stronger features should weigh more) |

Formulas:

```text theme={null}
Euclidean distance: distance(a,b) = sqrt(sum((a_i - b_i)^2))
Cosine similarity: cosine(a,b) = (a · b) / (||a|| * ||b||)
Dot product: dot(a,b) = sum(a_i * b_i)
```

All three metrics often agree on the top match when one neighbor is clearly closest and vector magnitudes are similar. Differences typically appear in the top-k ranking (rank 2, rank 3, etc.), which matters for recommendation systems that return multiple candidates.

<Callout icon="lightbulb">
  When building recommendations, check ranking differences across metrics. The top result may be the same, but the ordering of subsequent candidates can change significantly depending on whether you use Euclidean distance, cosine similarity, or dot product.
</Callout>

## How this applies to our fruit example

* Cosine similarity: prioritizes direction (relative proportions of sweetness, sourness, tropicalness). Good when you want size-invariant similarity (e.g., proportional taste profile).
* Euclidean distance: prioritizes absolute differences across features. Use this if exact feature magnitudes matter (you need the same level of sweetness).
* Dot product: favors vectors with larger magnitudes and good alignment. Use when strong feature values should dominate the ranking.

In practice, you would compute the three metrics for each candidate fruit and then compare the top-3 results to see how they differ. For this mango example you can expect banana to often be top-ranked, while the order of pineapple, papaya, and orange may shift depending on the metric.

## Practical guidance and tips

* If your embeddings are normalized (unit length), cosine similarity and dot product yield equivalent rankings — consider normalization if you care about direction only.
* If feature scales vary a lot, consider standardizing or normalizing features before computing Euclidean distance.
* For production systems, benchmark top-k precision across metrics using held-out queries to pick the metric that matches your business objective (user satisfaction, click-through, conversion).

| Use case                                            | Recommended metric |
| --------------------------------------------------- | ------------------ |
| Match by taste proportions (size-invariant)         | Cosine similarity  |
| Match by exact taste intensity                      | Euclidean distance |
| Favor items with strong signals (magnitude matters) | Dot product        |

## Links and references

* [Retrieval-Augmented Generation (RAG) overview](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)
* [Understanding cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
* [Euclidean distance explanation](https://en.wikipedia.org/wiki/Euclidean_distance)
* [Dot product (inner product) notes](https://en.wikipedia.org/wiki/Dot_product)

That’s it for this lesson — a compact, hands-on demonstration of how embedding similarity metrics shape recommendations and search results.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/8b72b738-81b5-465e-9ba6-0b91a6612448" />
</CardGroup>
