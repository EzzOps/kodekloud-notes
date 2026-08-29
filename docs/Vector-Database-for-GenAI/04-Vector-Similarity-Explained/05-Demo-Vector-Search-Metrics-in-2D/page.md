# Demo Vector Search Metrics in 2D

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Similarity-Explained/Demo-Vector-Search-Metrics-in-2D/page

Visual explanation of cosine similarity, Euclidean distance, and dot product showing how each metric affects vector search rankings in 2D

Welcome back. In this lesson we revisit cosine similarity, Euclidean distance, and the dot product with a visual, 2D intuition so you can see how each metric changes ranking behavior in a vector search.

The starting point is the vector itself. The orange vector below is the query Q. Changing its length alters magnitude; rotating it alters angle:

```text theme={null}
q = (1.20, 0.90) · |q| = 1.50 · θ = 36.9°
```

<Frame>
  <img alt="The image shows a graph with several colored vectors originating from the origin point (0,0), labeled A to D, with an orange vector marked as the query. There's information about vector magnitude and angle on the side." />
</Frame>

What to observe from the diagram:

* d is the Euclidean distance between the query and another vector — how far apart they are in space.
* θ (theta) is the angle between vectors — the directional difference.
* Increasing arrow length increases magnitude; rotating the arrow changes angle. Both affect different metrics in different ways.

Metrics: formulas, intuition, and ranking behavior
Below are the three most common metrics used for nearest-neighbor ranking in embedding / vector databases, with the formula and an intuition for what each emphasizes.

| Metric             | Formula                                  | What it emphasizes |       |   |                                 |                                                                         |
| ------------------ | ---------------------------------------- | ------------------ | ----- | - | ------------------------------- | ----------------------------------------------------------------------- |
| Cosine similarity  | \`cosine\_similarity(a, b) = (a · b) / ( | a                  |       | b | )\`                             | Direction/angle only — ignores magnitude after normalization            |
| Euclidean distance | \`euclidean\_distance(a, b) =            |                    | a - b |   | = sqrt((a1-b1)^2 + (a2-b2)^2)\` | Absolute proximity in embedding space — shortest straight-line distance |
| Dot product        | \`dot\_product(a, b) = a · b =           | a                  |       | b | cos(θ)\`                        | Combination of magnitude and alignment — rewards both length and angle  |

Cosine similarity

* Intuition: after normalization, only the angle matters. Two vectors with the same direction are highly similar even if their lengths differ.
* Ranking behavior: whichever stored vector has the smallest angle with Q ranks highest, regardless of vector length.

<Frame>
  <img alt="The image shows a graphical representation of vectors in a coordinate system, presumably illustrating cosine similarity, with document B having a higher similarity than document A to a query vector." />
</Frame>

Example intuition:

* If Q rotates toward A, cosine similarity favors A.
* If Q rotates toward B, B may outrank A even if Q is farther from B in Euclidean terms — cosine cares about direction.

Euclidean distance

* Intuition: the closer two points are in space, the higher the similarity (lower the distance). Angle alone doesn’t matter.
* Ranking behavior: the vector with the smallest straight-line distance to Q becomes the top hit.

Dot product

* Intuition: combines both magnitude and alignment. Large aligned vectors get high scores; a very long vector can outrank a shorter one even with a slightly worse angle.
* Ranking behavior: balances length and angle — useful when embedding magnitudes encode importance or confidence.

Putting it together with a concrete query
Consider this query example:

```text theme={null}
`q = {1.50, 2.94} · |q| = 3.30 · θ = 62.9°`
```

<Frame>
  <img alt="The image shows a graph plotting vectors with labeled points, demonstrating query and metric results, alongside a list of ranked document results based on cosine similarity scores." />
</Frame>

* Cosine similarity: whichever stored vector minimizes θ with Q will rank highest.
* Euclidean distance: whichever stored vector has the smallest `||a - q||` ranks highest.
* Dot product: a combination — a moderately close vector with a large magnitude and good alignment can outrank a closer but smaller vector.

> **lightbulb** Remember: similarity search returns a ranked list, not a single winner. The chosen metric changes result ordering and so directly impacts downstream tasks like retrieval, recommendation, or reranking.

Quick reference summary

* Cosine similarity: direction-focused, magnitude-invariant — use when vector orientation is what encodes semantics.
* Euclidean distance: proximity-focused — use when absolute position in embedding space matters.
* Dot product: magnitude + alignment — use when embedding scale carries meaning (e.g., TF-IDF‑style weighting or confidence).

Further reading

* [Cosine similarity — Wikipedia](https://en.wikipedia.org/wiki/Cosine_similarity)
* [Euclidean distance — Wikipedia](https://en.wikipedia.org/wiki/Euclidean_distance)

That’s it for this lesson. See you in the next one.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/65f66940-9bbb-4098-9150-ef7f320d900e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/bb07fc7f-db22-495a-b401-8e71775191a7)
