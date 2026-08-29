# Prepare data for plotting
names = list(fruit_vectors.keys())
vectors = np.array(list(fruit_vectors.values()))

fig = plt.figure(figsize=(12, 5))

# Plot 1: 3D scatter plot
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(vectors[:, 0], vectors[:, 1], vectors[:, 2], s=100, alpha=0.6, label='Fruits', c='blue')
ax1.scatter(mango_query[0], mango_query[1], mango_query[2], c='red', s=200, marker='*', label='Mango Query')

for i, name in enumerate(names):
    ax1.text(vectors[i, 0], vectors[i, 1], vectors[i, 2], name, fontsize=8)

ax1.set_xlabel('Red')
ax1.set_ylabel('Yellow')
ax1.set_zlabel('Green')
ax1.set_title('Fruit Vectors in 3D Color Space')
ax1.legend()

# Plot 2: 2D projection (Red vs Yellow)
ax2 = fig.add_subplot(122)
ax2.scatter(vectors[:, 0], vectors[:, 1], c='blue', s=100, alpha=0.6, label='Fruits')
ax2.scatter(mango_query[0], mango_query[1], c='red', s=200, marker='*', label='Mango Query')

for i, name in enumerate(names):
    ax2.annotate(name, (vectors[i, 0], vectors[i, 1]), fontsize=8)

ax2.set_xlabel('Red Intensity')
ax2.set_ylabel('Yellow Intensity')
ax2.set_title('Red vs Yellow (Top View)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\nNotice how fruits with similar colors cluster together!")
print("Papaya, nectarine, peach, and apricot are in the high-red corner (top-right).")
```

<Frame>
  <img alt="The image is a screenshot of a Jupyter Notebook displaying a 3D and 2D plot showing fruit vectors in color space, with fruits represented by blue dots and a mango query by a red star, illustrating clustering based on color similarity." />
</Frame>

This visualization should make it intuitive which fruits are likely nearest the mango query (for example: papaya, peach, nectarine).

## 3) Define and compute three similarity/distance metrics

We will compare three commonly used metrics:

| Metric             | What it measures                                             | Matching rule                                        |
| ------------------ | ------------------------------------------------------------ | ---------------------------------------------------- |
| Cosine similarity  | Angle between vectors (direction), normalized for magnitude  | Higher = more similar                                |
| Euclidean distance | Straight-line distance in vector space (magnitude-sensitive) | Lower = more similar                                 |
| Dot product        | Unnormalized projection combining direction and magnitude    | Higher = more similar (if magnitudes are meaningful) |

Compute each metric and produce sorted rankings:

```python theme={null}
import numpy as np
from typing import Dict, List, Tuple

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity (higher = more similar)."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Euclidean distance (lower = more similar)."""
    return float(np.linalg.norm(a - b))

def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """Dot product (higher = more similar if magnitudes are meaningful)."""
    return float(np.dot(a, b))

# Compute rankings for each metric
metrics_results: Dict[str, List[Tuple[str, float]]] = {
    "Cosine Similarity (higher = more similar)": sorted(
        [(name, cosine_similarity(vec, mango_query)) for name, vec in fruit_vectors.items()],
        key=lambda x: x[1],
        reverse=True
    ),
    "Euclidean Distance (lower = more similar)": sorted(
        [(name, euclidean_distance(vec, mango_query)) for name, vec in fruit_vectors.items()],
        key=lambda x: x[1]
    ),
    "Dot Product (higher = more similar)": sorted(
        [(name, dot_product(vec, mango_query)) for name, vec in fruit_vectors.items()],
        key=lambda x: x[1],
        reverse=True
    ),
}
```

Print a formatted comparison of rankings:

```python theme={null}
print("=" * 60)
print("|| SIMILARITY RANKINGS COMPARISON ||")
print("=" * 60)

for metric_name, ranking in metrics_results.items():
    print(f"\n{metric_name}:")
    for rank, (name, value) in enumerate(ranking, start=1):
        print(f"  {rank}. {name:12} {value:.4f}")
```

Observed ordering (example from these vectors):

* Cosine top 3: papaya, peach, pear
* Euclidean top 3: papaya, peach, pear
* Dot product top 3: pear, pineapple, peach

To extract the top-k results for quick comparison:

```python theme={null}
# Get top 5 for each metric
top_cosine = [x[0] for x in metrics_results["Cosine Similarity (higher = more similar)"][:5]]
top_euclidean = [x[0] for x in metrics_results["Euclidean Distance (lower = more similar)"][:5]]
top_dot = [x[0] for x in metrics_results["Dot Product (higher = more similar)"][:5]]

print("🏆 Top 5 Fruits by Each Metric:")
print("-" * 50)
print(f"Cosine: {top_cosine} | Euclidean: {top_euclidean} | Dot Product: {top_dot}")
```

Note: all three metrics can often agree on which items are closest (e.g., papaya is near the top for cosine and Euclidean), but they can disagree on exact ordering because they emphasize different vector properties (direction vs magnitude).

## 4) Visualize metric scores

A bar chart or grouped bar plot makes it easier to compare scores across metrics and highlight how one metric (e.g., dot product) can favor high-magnitude vectors like `pear`.

<Frame>
  <img alt="The image shows a Jupyter notebook interface with a code snippet and visualizations comparing fruit similarity across three metrics: Cosine Similarity, Euclidean Distance, and Dot Product. The bars indicate that papaya is the top match across all metrics." />
</Frame>

## Summary and next steps

```python theme={null}
print("=" * 60)
print("🔴 Stage 2 COMPLETE!")
print("=" * 60)
print("\n📝 What you learned:")
print("  1. Visualized fruit vectors in 3D color space")
print("  2. Compared 3 different similarity metrics (cosine, euclidean, dot product)")
print("  3. Saw how rankings can differ while the top result may still agree")
print("\n👉 Next steps:")
print("  - Try changing the mango_query vector and observe how results change.")
print("  - In real applications, you'd use embedding models (e.g., sentence-transformers: https://www.sbert.net/)")
print("    to create vectors from text; search logic is the same.")
```

> **lightbulb** Similarity search powers recommendation engines and RAG (retrieval-augmented generation). In recommendations it matches queries to products and user embeddings (purchase history); in RAG it retrieves documents that ground generation, making ranking quality critical to final output quality.

Practical tips:

* In recommendation systems, a short query like `shoe` combined with a user embedding quickly improves relevance (sports vs formal vs ski).
* In RAG, better similarity ranking yields more useful supporting documents and better generated answers.

References:

* LanceDB: [https://github.com/lancedb/lance](https://github.com/lancedb/lance)
* Sentence-Transformers (for real-world text embeddings): [https://www.sbert.net/](https://www.sbert.net/)

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/d4142cf0-fe03-4deb-83b8-b621bcf9d152)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/09aa9e12-af9a-427e-80b7-08992ebda480)


# Demo Setting up Vectors for Fruits

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Similarity-Explained/Demo-Setting-up-Vectors-for-Fruits/page

Demo demonstrating how to create, store, and query handcrafted 3D fruit vectors in a local LanceDB instance for similarity search using a mango query vector.

Hello and welcome back.

Now that we've covered similarity search concepts both theoretically and visually, let's implement the same example practically. We'll create a few handcrafted vectors for fruits and store them in a local LanceDB instance so we can run similarity comparisons. This demo uses simple 3-dimensional vectors representing hypothetical features (for example: sweetness, sourness, texture) so the results are easy to reason about.

Below are the steps to create the LanceDB table, insert the fruit vectors, and prepare a query vector for a mango.

> **lightbulb** We use handcrafted 3-dimensional vectors here for clarity. In production, you would typically generate higher-dimensional embeddings using a machine learning model (for example, sentence or image encoders).

## 1) Setup: imports, paths, and model/table definition

Run the cell below to import dependencies, create a local directory for the DB, connect to [LanceDB](https://www.lancedb.org), and define a Pydantic-backed LanceModel schema for our fruit vectors.

```python theme={null}
import numpy as np
import lancedb
from lancedb.pydantic import LanceModel, Vector
from pathlib import Path

DB_PATH = Path("fruits_lancedb")
TABLE_NAME = "fruit_vectors"
DB_PATH.mkdir(exist_ok=True)

db = lancedb.connect(str(DB_PATH))

class FruitVector(LanceModel):
    name: str
    vector: Vector(3)

def prepare_table():
    if TABLE_NAME in db.table_names():
        db.drop_table(TABLE_NAME)
    return db.create_table(TABLE_NAME, schema=FruitVector)

table = prepare_table()
```

This creates (or recreates) a table named `fruit_vectors` in the local directory `fruits_lancedb`. If you point `lancedb.connect()` to a remote LanceDB instance, the DB files will be stored remotely and won't appear in the local directory.

## 2) Insert handcrafted fruit vectors

Define each fruit as a 3-dimensional NumPy vector and add the records to the LanceDB table. We convert vectors to plain Python lists (`vector.tolist()`) before insertion because LanceDB stores JSON-like serializable data.

```python theme={null}
fruit_vectors = {
    "papaya": np.array([0.88, 0.35, 0.05]),
    "peach": np.array([0.81, 0.32, 0.12]),
    "pear": np.array([0.62, 0.51, 0.38]),
    "pineapple": np.array([0.15, 0.85, 0.79]),
    "apple": np.array([0.28, 0.42, 0.69]),
    "apricot": np.array([0.77, 0.44, 0.21]),
    "guava": np.array([0.10, 0.74, 0.58]),
    "nectarine": np.array([0.83, 0.30, 0.11])
}

records = [
    {
        "name": name,
        "vector": vector.tolist(),
    }
    for name, vector in fruit_vectors.items()
]

table.add(records)

stored = table.to_pandas()
print(f"💾 Stored {len(stored)} handcrafted fruit vectors.")
print("Available fruits:", ", ".join(stored["name"].tolist()))
print(stored[["name", "vector"]])
```

Fruit vector summary (readable table):

| Fruit     | Vector (sweetness, sourness, texture) |
| --------- | ------------------------------------- |
| papaya    | `[0.88, 0.35, 0.05]`                  |
| peach     | `[0.81, 0.32, 0.12]`                  |
| pear      | `[0.62, 0.51, 0.38]`                  |
| pineapple | `[0.15, 0.85, 0.79]`                  |
| apple     | `[0.28, 0.42, 0.69]`                  |
| apricot   | `[0.77, 0.44, 0.21]`                  |
| guava     | `[0.10, 0.74, 0.58]`                  |
| nectarine | `[0.83, 0.30, 0.11]`                  |

> **warning** A local directory named `fruits_lancedb` will be created and populated. If you run this demo multiple times, the table is dropped and recreated by `prepare_table()` to ensure a clean state.

Notes:

* Converting NumPy arrays via `vector.tolist()` ensures the data is JSON-serializable for LanceDB.
* Use `table.to_pandas()` to inspect stored records as a pandas DataFrame.

## 3) Prepare the query vector (mango)

Construct the mango query vector. This vector is used only for querying and is not inserted into the table in this demo (unless you intentionally add it).

```python theme={null}
mango_context = np.array([0.90, 0.34, 0.08])
print("✔ Query vector (mango):", mango_context.tolist())
```

Now you have:

* A LanceDB table `fruit_vectors` containing handcrafted 3-dimensional fruit vectors.
* A query vector `mango_context` ready for similarity comparisons.

## Next steps — similarity search examples

You can now run similarity searches (for example, cosine similarity, Euclidean distance, or dot product) against the stored vectors to see how the mango ranks among the fruits under different metrics. Typical steps:

* Normalize vectors (if using cosine similarity).
* Run a nearest-neighbors query in LanceDB using the mango vector.
* Compare top-k results across different metrics to see how rankings change.

Helpful links and references:

* [LanceDB Documentation](https://www.lancedb.org)
* [NumPy](https://numpy.org)
* [Pandas](https://pandas.pydata.org)
* [Pydantic](https://docs.pydantic.dev/)

What you might try next:

* Replace handcrafted vectors with model-generated embeddings (for example, text or image embeddings).
* Scale the table to higher-dimensional embeddings and larger datasets.
* Benchmark different similarity metrics (cosine vs. Euclidean vs. dot product) for your application.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/8e06787b-1ff8-4f2f-82f3-64f588e6637b/lesson/039fbc21-8dd5-4294-89b1-9805f90e7f75)
