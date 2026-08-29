# Demo Query a New Fruit Across 3 Searches

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Similarity-Explained/Demo-Query-a-New-Fruit-Across-3-Searches/page

Demonstrates querying a mango vector against fruit embeddings using three similarity metrics and visualizations

Welcome back. This tutorial assumes you already have LanceDB set up with vectors for several fruits and that a mango query vector is defined. We'll:

* Reload the stored fruit vectors from LanceDB,
* Visualize vectors in 3D and 2D (Red vs Yellow) color-space,
* Run three similarity/distance searches (Cosine similarity, Euclidean distance, Dot product),
* Compare rankings and visualize metric differences.

<Callout icon="lightbulb">
  If you're following along in a fresh notebook, run each code block sequentially so variables (like `fruit_vectors` and `mango_query`) are available for plotting and metric computation.
</Callout>

## 1) Reload LanceDB and fruit vectors

Run this in a fresh notebook cell to ensure data is present:

```python theme={null}
import numpy as np
import lancedb
from pathlib import Path

DB_PATH = Path("fruits_lancedb")
TABLE_NAME = "fruit_vectors"

db = lancedb.connect(str(DB_PATH))
table = db.open_table(TABLE_NAME)
stored = table.to_pandas()
fruit_vectors = {row.name: np.array(row.vector) for row in stored.itertuples()}

mango_query = np.array([0.9, 0.34, 0.08])

print(f"🔄 Reloaded {len(fruit_vectors)} fruits from LanceDB")
print(f"🍑 Mango query vector: {mango_query}")
```

This confirms the dataset is available and shows the query vector we will search with.

Verify the loaded fruits and their vectors:

```python theme={null}
print(f"Reloaded {len(fruit_vectors)} fruits from LanceDB")
print(f"Mango query vector: {mango_query}")
print("\nStored fruits:")
for name, vec in fruit_vectors.items():
    print(f"{name:9} -> {vec}")
```

Example console output:

```text theme={null}
Reloaded 8 fruits from LanceDB
Mango query vector: [0.9  0.34 0.08]

Stored fruits:
papaya    -> [0.80 0.35 0.05]
peach     -> [0.82 0.41 0.38]
pear      -> [0.89 0.42 0.54]
pineapple -> [0.75 0.64 0.45]
apple     -> [0.44 0.52 0.36]
apricot   -> [0.41 0.47 0.52]
guava     -> [0.39 0.58 0.31]
nectarine -> [0.48 0.72 0.68]
```

## 2) Visualize the vectors (3D and 2D projection)

Plot the fruit vectors in 3D color-space plus a 2D top-down projection (Red vs Yellow). This helps reason about which fruits should be nearest the mango query by color.

```python theme={null}
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D projection)
