# Vectors Matrices and Tensors Part 1

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Linear-Algebra/Vectors-Matrices-and-Tensors-Part-1/page

Explains how vectors, matrices, and tensors represent data for search, related-item discovery, and personalized recommendations in e-commerce.

Welcome — I'm Alan Chapman from KodeKloud.

In this lesson we’ll see how computers use linear algebra — vectors, matrices, and tensors — to represent, compare, and process data. These primitives are the foundation for search, related-item discovery, and recommendations in real-world systems.

<Frame>
  <img alt="The image shows a presentation slide with three topics related to vectors and search engine modeling, alongside a person speaking and a cartoon character." />
</Frame>

We’ll cover practical, concrete examples: finding the right product with search, discovering related items, and creating personalized recommendations.

Have you ever wondered how software recommends a product, ranks search results, or predicts what you might want next? At a high level, computers organize data into three fundamental shapes:

* Vectors — ordered lists of numbers that represent single items or queries (often called feature vectors or embeddings).
* Matrices — 2D arrays that express relationships across collections of items (for example, item-by-feature or user-by-item matrices).
* Tensors — higher-dimensional arrays used for richer interactions (user × item × context, multi-modal data, etc.).

Each structure is chosen based on the complexity of the data and the modeling task: vectors for single-item similarity, matrices for pairwise relationships and linear transforms, tensors for multi-way relationships.

<Frame>
  <img alt="The image features a search bar with the query &#x22;blue gym bag&#x22; and a display of six blue gym bag icons with varying prices. There is also a person standing on the right side of the image." />
</Frame>

Soon you’ll see how these shapes power typical e-commerce behaviors.

Meet Jay, who launched an e-commerce app called Nile. As ML engineers we make shopping on Nile easy and personalized. We’ll focus on three tasks:

* Search — convert user queries into vectors and match them to product vectors.
* Related products — surface complementary or similar items using vector/matrix comparisons.
* Recommendations — learn from user behavior using matrices and tensors.

<Frame>
  <img alt="The image shows a person standing on the right side, and on the left, there's an animated cat and a diagram with the word &#x22;Vectors.&#x22; The background is a gradient of dark purple tones." />
</Frame>

Machine learning models learn from user actions — searches, clicks, purchases — and translate that data into numeric representations that can be compared and ranked efficiently. The core idea: convert text, images, and attributes into numbers the computer can reason about.

<Frame>
  <img alt="The image illustrates the concepts of vectors, matrices, and tensors, with corresponding visual examples and a person in a &#x22;KodeKloud&#x22; shirt. A cartoon cat is standing on a representation of a tensor." />
</Frame>

Example scenario: Alice searches for a “blue gym bag.” We’ll follow her journey to illustrate how data is encoded and used for search and recommendations.

When Alice first types “bag” she sees many categories: handbags, backpacks, briefcases. Not very useful. When she narrows to “blue gym bag” the results improve because the system encodes both products and queries as vectors and compares them with similarity measures (e.g., dot product, cosine similarity).

Computers only understand numbers, so we must encode words and attributes as numeric features. There are many encoding strategies (binary, categorical codes, one-hot, embeddings); below we show a simple illustrative approach for product attributes.

At the lowest level data can be binary (for illustration):

```python theme={null}
0101001001101001
0101010001101001
0101001101101001
0110100001101001
```

More usefully for search, we build structured numeric features. For our bag example we might map common product attributes to numeric codes:

| Attribute | Example encoding                                                                | Notes                                                                                        |
| --------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Type      | `01` = backpack, `02` = gym bag, `03` = tote                                    | Use one-hot or learned embeddings in production to avoid implying order                      |
| Color     | `150` = red, `250` = green, `415` = light blue, `450` = blue, `490` = dark blue | Use ranges so similar shades have nearby codes; embeddings or color vectors are often better |
| Price     | `23.40`                                                                         | Normalize prices for distance-based comparisons (e.g., scale to 0–1)                         |

Combine these feature values into a vector for each product. Think of the mapping from attributes to numbers as a dictionary the system can read.

<Callout icon="lightbulb">
  Integer categorical codes here are illustrative. In production, raw ordinal integers can mislead similarity calculations because they imply scale. Prefer one-hot encoding, normalized numeric features, or learned embeddings for categorical attributes. When a query omits a feature, systems commonly mask that dimension so it doesn't affect similarity.
</Callout>

<Frame>
  <img alt="The image shows a presentation slide with tables translating bag types and colors from human-readable terms to numeric codes, and a person speaking beside it." />
</Frame>

For example, a blue gym bag priced at \$23.40 could be represented as:

```python theme={null}
[02, 450, 23.4]
```

Other examples:

```python theme={null}
[01, 550, 34]    # Backpack, pink, $34
[03, 150, 42.6]  # Tote, red, $42.60
```

<Frame>
  <img alt="The image shows a person standing in front of a representation of creating a vector for a blue gym bag, with tables categorizing type, color, and price for bags." />
</Frame>

When a customer searches, the system converts the query into a query vector and compares it with stored product vectors using vector math (dot product, cosine similarity, or L2 distance) to find the closest matches. Query dimensions that are unspecified can be masked or treated as wildcards.

<Callout icon="lightbulb">
  Using a wildcard (an underscore or `None` in implementation) indicates the query doesn't constrain that feature. The search logic then ignores that dimension when ranking matches.
</Callout>

Nile precomputes product vectors for all inventory items and stores them for fast nearest-neighbor lookup (vector indexes, ANN libraries). Example product catalog vectors:

<Frame>
  <img alt="The image shows a comparison chart for bag types, colors, and prices represented in human-readable and computer-readable formats, with a person speaking in the foreground." />
</Frame>

A small catalog of product vectors:

```python theme={null}
[ 01, 550, 34 ]     # Backpack, pink, $34
[ 03, 150, 42.6 ]   # Tote, red, $42.60
[ 02, 415, 23 ]     # Gym bag, light blue, $23
[ 02, 417, 23 ]     # Gym bag, light blue variant, $23
[ 02, 450, 23.4 ]   # Gym bag, blue, $23.40
[ 01, 375, 19.99 ]  # Backpack, teal variant, $19.99
[ 04, 490, 45.2 ]   # Another type, dark blue, $45.20
[ 03, 350, 27.5 ]
[ 02, 150, 50 ]
[ 04, 475, 35.5 ]
[ 02, 490, 35.75 ]
[ 03, 250, 34 ]
[ 01, 475, 40 ]
[ 04, 550, 45 ]
[ 02, 413, 38.2 ]
[ 02, 390, 42.99 ]
```

When Alice types `bag` broadly, the query vector leaves the type unspecified and the search returns many types:

```python theme={null}
