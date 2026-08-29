# Euclidean Distance

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Similarity-Explained/Euclidean-Distance/page

Explains Euclidean distance, compares it to cosine similarity, discusses use cases, examples, and caveats for high dimensional data like embeddings

Hello and welcome.

Cosine similarity measures the angle between two (or n) vectors. In this article we introduce its counterpart: Euclidean distance, which asks a different, more direct question about vector comparison.

What question does Euclidean distance ask?

Simply: how far apart are two points? Think of it as measuring with a ruler. Given two points in 2D space, you draw the shortest straight line between them — the length of that line is the Euclidean distance. The closer the points, the more similar they are; the farther apart, the less similar.

## Example in 2D

Suppose point A = (-3, -1) and point B = (3, 2). The horizontal gap Δx is 6 and the vertical gap Δy is 3. Using the Pythagorean theorem, the squared distance is:

```text theme={null}
d² = Δx² + Δy²
```

More generally, for two n-dimensional vectors x and y, the Euclidean distance is:

```python theme={null}
import math

def euclidean_distance(x, y):
    return math.sqrt(sum((xi - yi) ** 2 for xi, yi in zip(x, y)))
```

Compute the distance for A and B:

```python theme={null}
A = (-3, -1)
B = (3, 2)
print(euclidean_distance(A, B))  # outputs 6.708203932499369
```

## Euclidean distance vs. cosine similarity

Use this table to quickly compare the two similarity/distance concepts:

| Concept            | What it measures                      | Sensitive to                    | Typical use cases                                                            |
| ------------------ | ------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------- |
| Euclidean distance | Straight-line distance between points | Magnitude and absolute position | Physical measurements, clustering with k-means, low-dimensional spatial data |
| Cosine similarity  | Angle between vectors (direction)     | Direction, not magnitude        | Text embeddings, document similarity, high-dimensional normalized embeddings |

Key conceptual differences:

* Euclidean distance measures actual positions in space (absolute differences).
* Cosine similarity measures the angle between vectors (direction), ignoring magnitude.
* Two vectors can point in the same direction but be far apart in magnitude; cosine similarity may treat them as similar while Euclidean distance will not.

## When to use Euclidean distance

* Use Euclidean distance when magnitude matters: comparing prices, physical measurements, or sensor readings where absolute differences are meaningful.
* Clustering: k-means typically uses (squared) Euclidean distance by default, so many clustering pipelines rely on it for grouping similar datapoints (e.g., user behavior segments, product grouping).
* Low-dimensional spatial data: for 2D or 3D Cartesian coordinates (local maps, geometry), Euclidean distance is the natural choice.

<Callout icon="lightbulb">
  Euclidean distance is the straight-line distance between two points: smaller distance means more similar, larger distance means less similar.
</Callout>

## Caveat: high-dimensional data and the curse of dimensionality

When working with very high-dimensional embeddings (hundreds or thousands of dimensions, as is common for text embeddings), Euclidean distance can lose discriminative power. In very high-dimensional spaces, many points tend to appear similarly distant from one another, which reduces the usefulness of Euclidean measures for distinguishing nearest neighbors. This is why cosine similarity or other normalized measures are often preferred for high-dimensional text embeddings.

<Frame>
  <img alt="The image explains Euclidean distance with a graph and compares it to cosine similarity, highlighting key insights and best use cases for each method." />
</Frame>

<Callout icon="warning">
  Be cautious using Euclidean distance for high-dimensional embeddings: the curse of dimensionality can make distances less meaningful. Consider cosine similarity or other normalized measures for many text-embedding tasks.
</Callout>

## Summary

* Euclidean distance = straight-line distance between two points.
* Smaller distance → more similar; larger distance → less similar.
* Best for magnitude-sensitive comparisons, low-dimensional spatial data, and algorithms like k-means.
* Avoid relying solely on Euclidean distance for very high-dimensional text embeddings.

A related concept is the dot product.

That is it for this article.

## Links and references

* [K-Means Clustering — scikit-learn](https://scikit-learn.org/stable/modules/clustering.html#k-means)
* [Great-circle distance / Haversine formula — Wikipedia](https://en.wikipedia.org/wiki/Haversine_formula)
* [Cosine similarity — Wikipedia](https://en.wikipedia.org/wiki/Cosine_similarity)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/a08ffc6a-28a9-442f-9dae-d751f40e8bd9" />
</CardGroup>
