# query: [ _, _, _ ]  (type unspecified)
[02, 417, 23]
[03, 375, 50]
[02, 450, 23.4]
[01, 375, 19.99]
[04, 490, 45.2]
[02, 415, 30]
[03, 350, 27.5]
[02, 150, 50]
[04, 475, 35.5]
[02, 490, 35.75]
[03, 250, 34]
[01, 475, 40]
[04, 550, 45]
[02, 413, 38.2]
[02, 390, 42.99]
```

When she refines to `gym bag`, the query vector sets the type to `02` and filters out non-gym-bag types. When she further specifies `blue gym bag`, the color dimension is set to `450` (or nearby codes for light/dark shades) and the results are ranked by closeness in the color and price dimensions.

Filtered example results for `blue gym bag`:

```python theme={null}
[02, 417, 23]     # Gym bag, light blue, $23
[02, 450, 23.4]   # Gym bag, blue, $23.40
[02, 415, 30]     # Gym bag, light blue, $30
[02, 490, 35.75]  # Gym bag, dark blue, $35.75
[02, 413, 38.2]   # Gym bag, light blue variant, $38.20
[02, 390, 42.99]  # Gym bag, teal-ish, $42.99
[02, 150, 50]     # Gym bag, red (less relevant by color)
```

Numeric color codes allow the system to distinguish light blue from navy; similarity measures rank the closest shades higher.

<Frame>
  <img alt="The image features a woman speaking with a graphical illustration of a person holding a tablet labeled &#x22;nile.&#x22; It includes text describing &#x22;Easy matched search&#x22; using vectors and &#x22;Find related products&#x22; using matrices." />
</Frame>

Alice found a light-blue gym bag for \$23 and wants similar items — same type, similar color, and comparable price. To support this, Nile uses vector comparisons for similarity and may employ matrices or tensors for richer recommendations (for example, item-by-item co-purchase matrices or user × item × context tensors).

What we covered in this lesson:

* How vectors encode item attributes and user queries for search and similarity.
* Why categorical encodings should be handled carefully (one-hot, embeddings, normalization).
* How masking unspecified query dimensions improves search relevance.
* How precomputed vectors and fast nearest-neighbor indexes enable responsive search and related-item suggestions.

Next lessons will explore matrices and tensors: how they express relationships across many items and users and how they power collaborative filtering, matrix factorization, and multi-dimensional recommendation models.

Further reading and references:

* [Vector search and ANN libraries](https://www.mongodb.com/ann) (example resources)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — foundational infra concepts for serving models
* Embeddings, one-hot encoding, and normalization strategies in modern recommendation systems

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mathematics-for-computing/module/d8fa251f-80d2-4813-8b52-ad57051b1dcf/lesson/9330b081-e3b4-41cf-a560-5818bf204b63" />
</CardGroup>


# Vectors Matrices and Tensors Part 2

Source: https://notes.kodekloud.com/docs/Mathematics-for-Computing/Linear-Algebra/Vectors-Matrices-and-Tensors-Part-2/page

Explains vectors, matrices, and tensors and how multi-dimensional arrays power recommendation systems by representing products, features, users and interactions for richer predictions

Vectors let us compare one attribute at a time — for example, filtering strictly for “blue gym bags.” To combine and compare multiple attributes at once (colour and price, for example), we use matrices.

A matrix is a two-dimensional array (an m-by-n table): each row is an observation (one product), and each column is a feature (type, colour, price, rating, etc.). In mathematical notation we write a matrix as rows of numbers inside square brackets; in code it’s a 2-D array or list of lists.

<Frame>
  <img alt="The image shows a matrix notation concept with a table listing products, their types, colors, prices, and ratings. There is also a person standing next to the table, possibly explaining the concept." />
</Frame>

Each row represents one bag and each column represents a feature. For example, Alice has found a light-blue gym bag in the inventory — that corresponds to a single row in the matrix.

<Frame>
  <img alt="The image shows a table titled &#x22;Finding the Perfect Bag With Matrix,&#x22; listing bag attributes like ID, type, color, price, and rating, alongside a person presenting the information." />
</Frame>

Rather than applying filters one at a time, a matrix lets us combine multiple criteria (e.g., `colour ≈ blue` AND `price ≈ 23`) and run vectorized operations to select matching rows efficiently. This is much faster and more scalable than iterating through each record and applying individual checks.

<Callout icon="lightbulb">
  In data terms: rows = observations (products), columns = features. A matrix with m rows and n columns is often called an m-by-n matrix.
</Callout>

Simple Python example showing a matrix as a list of rows and filtering by price:

```python theme={null}
