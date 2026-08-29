# How Similarity Results Can Differ

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Similarity-Explained/How-Similarity-Results-Can-Differ/page

Shows how cosine similarity, Euclidean distance, and dot product produce different similarity rankings for identical fruit embeddings.

Hello and welcome back.

We created embeddings for different fruits and stored them in a vector database. This article demonstrates how similarity search results can change depending on the similarity metric you choose. The objective is not to focus on an absolute winner but to understand how cosine similarity, Euclidean distance, and dot product change the ranking order for the same query and stored embeddings.

Our query for every example below is identical: find fruits similar to mango. To keep things concrete, imagine the mango embedding is approximately:
`mango = [0.9, 0.2, 0.8]`\
(encoding sweetness, sourness, and tropicalness). Different similarity metrics interpret these vectors in distinct ways and therefore produce different rankings.

Cosine similarity
Cosine similarity compares direction only. It measures the cosine of the angle θ between two vectors and is invariant to vector magnitude. Vectors that point in the same direction produce a cosine near 1, regardless of their lengths.

How do the results look with cosine similarity? In this run, the ranking produced was: banana (clear winner), then orange, grapes, apple, and lemon last.

<Frame>
  <img alt="The image shows cosine similarity results for comparing different fruits to mango based on sweetness, sourness, and tropical attributes, with banana being the most similar." />
</Frame>

A few observations from the cosine results:

* Banana is the closest directional match to mango, so it wins under cosine similarity.
* Lemon finishes last because its embedding `lemon = [0.1, 0.95, 0.3]` points in a very different direction (high sourness, low sweetness and tropicalness). The large angle between mango and lemon causes the cosine score to drop.
* Some intermediate placements (e.g., grapes vs. apple) can be surprising — cosine cares only about direction and ignores scale.

<Frame>
  <img alt="The image displays a table of cosine similarity results for different fruits, with scores and interpretations indicating how closely each aligns with a reference. Banana has the highest similarity, while lemon has the least." />
</Frame>

Euclidean distance
Euclidean distance (L2) measures the straight-line distance between points in vector space. It depends on absolute coordinates and therefore reflects both magnitude and direction as spatial positions.

Using the same query (`find fruits similar to mango`), the Euclidean ranking in this example is: banana, orange, apple, grape, and lemon.

<Frame>
  <img alt="The image displays a table ranking fruits based on their Euclidean distance scores, with banana ranked closest and lemon farthest. The table includes vectors, cosine scores, interpretations, and visual indicators for each fruit." />
</Frame>

Key point:

* Banana remains closest under Euclidean distance.
* Notice the swap between apple and grape compared to the cosine ranking: cosine placed grape ahead of apple while Euclidean placed apple ahead of grape. This happens because Euclidean considers absolute coordinates; grape may point in a different direction but have coordinate values that place it slightly farther from mango than apple. Cosine missed that because it normalizes vector length first.

This difference matters for practical systems (e.g., recommendation engines) where the ordering beyond the top result influences what users see.

Dot product
The dot product (unnormalized inner product) is sensitive to both direction and magnitude. It favors vectors that are aligned and have larger magnitudes.

With the same mango query, the dot product ranking in this run became: papaya, pineapple, orange, banana (dropped to 4th), and so on.

<Frame>
  <img alt="The image is a chart showing dot product results for finding fruits similar to mango, using vectors for sweetness, sourness, and tropical qualities. It ranks fruits like papaya, pineapple, and orange based on their similarity to mango with corresponding cosine scores and interpretations." />
</Frame>

Why did banana drop with dot product?

* Banana’s vector in this example is `banana = [0.45, 0.10, 0.47]`. It points in a similar direction to mango but has a much smaller magnitude (roughly half the values). The dot product multiplies components directly and therefore penalizes small-magnitude vectors. Think of it as two people agreeing, but one is whispering — the dot product prefers the louder (higher-magnitude) match.
* Papaya wins because its embedding has larger overall values (higher magnitude) that align well with mango; the magnitude compensates for small directional differences.

<Frame>
  <img alt="The image shows a ranked table of fruits based on dot product scores related to sweetness, sourness, and tropical characteristics, with Papaya ranked highest due to good alignment and large values. Additional comments explain why Banana's score dropped despite being first in cosine alignment." />
</Frame>

Practical takeaway
You just saw three different similarity measures (cosine, Euclidean, dot product) produce three distinct rankings for the same query and the same stored embeddings. This happens because:

* Cosine focuses on direction only (ignores magnitude).
* Euclidean measures absolute spatial distance (magnitude and direction combined).
* Dot product emphasizes both alignment and magnitude (favoring larger vectors that point in the same direction).

| Metric                  |                          What it measures | When to use                                                           | Likely effect on ranking                                                                     |
| ----------------------- | ----------------------------------------: | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Cosine similarity       |           Angle/direction between vectors | When only semantic direction matters (normalize embeddings first)     | Favors vectors with similar direction regardless of length — good for semantics-only matches |
| Euclidean distance (L2) | Straight-line distance in embedding space | When absolute coordinates matter (magnitude carries semantic meaning) | Penalizes differences in absolute values — can reorder neighbors compared to cosine          |
| Dot product             |             Alignment scaled by magnitude | When magnitude encodes importance or confidence                       | Rewards large aligned vectors — can push high-magnitude items to the top                     |

<Callout icon="lightbulb">
  Choosing a similarity metric is a design decision, not just a configuration option. If your embeddings are not normalized, dot product results will be dominated by magnitude; Euclidean and cosine will produce different orderings. Consider whether you want direction-only matches (cosine), absolute-position matches (Euclidean), or magnitude-aware matches (dot product), and normalize embeddings if required by your use case.
</Callout>

Vector normalization and how to apply it within a vector database deserve a dedicated discussion. For now, remember: you should not expect all three search types to produce the same ranking or winner. How you embed, store, and retrieve vectors determines what your system considers “relevant.”

Links and references

* [Vector databases and similarity search concepts](https://en.wikipedia.org/wiki/Similarity_search)
* [Cosine similarity overview](https://en.wikipedia.org/wiki/Cosine_similarity)
* [Euclidean distance (L2) definition](https://en.wikipedia.org/wiki/Euclidean_distance)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/a92bb6dd-f890-4549-8f84-67f654c48965" />
</CardGroup>
