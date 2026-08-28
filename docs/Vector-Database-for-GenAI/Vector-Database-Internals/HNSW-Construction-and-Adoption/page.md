# demo_setup.py
import chromadb
import numpy as np
```

Dataset and deterministic embedding

* We use 6 short documents to keep the demo compact.
* The embedding is a 3-dimensional count vector that measures matches against three small keyword buckets: travel, policy, and service.
* This deterministic embedder makes results reproducible and easy to reason about.

```python theme={null}
# data_and_embed.py
docs = [
    "book flight ticket",
    "cancel booking refund",
    "hotel room reservation",
    "baggage allowance policy",
    "airport security rules",
    "meal options onboard",
]
ids = [f"d{i}" for i in range(len(docs))]

# Small deterministic vocabulary: three buckets
vocab = {
    "travel": {"flight", "ticket", "airport", "booking", "reservation"},
    "policy": {"policy", "rules", "allowance", "security"},
    "service": {"meal", "onboard", "refund", "cancel", "hotel"},
}

def embed(text: str):
    """
    Return a 3-d embedding as counts of words matching each bucket.
    Order: [travel, policy, service]
    """
    words = text.lower().split()
    vec = [
        sum(w in vocab[k] for w in words)
        for k in ("travel", "policy", "service")
    ]
    return np.array(vec, dtype=float)

# Precompute embeddings for the documents
embeddings = [embed(d).tolist() for d in docs]
```

Store vectors in ChromaDB (optional)

* This demonstrates how to upsert a list of vectors into a Chroma collection.
* Many production vector DBs perform indexing in the background; we still build a toy index here to illustrate pruning.

```python theme={null}
# store_in_chroma.py
client = chromadb.Client()
collection = client.get_or_create_collection(name="simple_index_demo")

# Upsert embeddings into the collection.
# chromadb expects lists, so embeddings is a list of lists.
collection.upsert(ids=ids, documents=docs, embeddings=embeddings)

# Confirm count
print("Stored", collection.count(), "vectors in ChromaDB")

# Example: load them back (if needed)
data = collection.get(include=["documents", "embeddings"])
docs = data["documents"]
embeddings = data["embeddings"]
```

Linear (brute-force) search

* Linear scanning computes the Euclidean (L2) distance from the query embedding to every stored embedding.
* We count how many distance computations ("checks") occur.

```python theme={null}
# linear_search.py
def linear_search(query: str, top_k: int = 2):
    q = embed(query)
    scores = []
    checks = 0
    # Linear scan = compute distance to every stored vector
    for i, e in enumerate(embeddings):
        checks += 1
        dist = np.linalg.norm(q - np.array(e))  # Euclidean distance
        scores.append((dist, docs[i]))

    scores.sort(key=lambda x: x[0])
    return scores[:top_k], checks

query = "flight rules"
linear_top, linear_checks = linear_search(query)
print("Query:", query)
print("Top results:", linear_top)
print("Distance checks:", linear_checks)
```

Expected linear-search behavior (example)

* Query: "flight rules"
* Top results (approx): `('airport security rules', distance 1.0)`, `('book flight ticket', distance ~1.4142)`
* Distance checks: 6\
  Note: exact tuple formatting may vary, but distances and counts are deterministic for this embedder.

Why indexing matters

* Linear scans grow linearly with dataset size — for millions or billions of vectors this becomes infeasible.
* Indexing partitions or prunes the search space, so the system computes distances only for a small subset of candidates.

Toy index (pre-partition into 3 buckets)

* We build a very small index by grouping documents based on argmax of their 3-d embedding.
* This produces three buckets: 0 = travel-ish, 1 = policy-ish, 2 = service-ish.

```python theme={null}
# build_index.py
index_groups = {0: [], 1: [], 2: []}

# Pre-partition vectors into 3 buckets using the dimension with the largest value.
for i, e in enumerate(embeddings):
    group = int(np.argmax(e))  # 0=travel-ish, 1=policy-ish, 2=service-ish
    index_groups[group].append(i)

# Inspect group membership (optional)
print("Index groups:", index_groups)
```

Indexed (pruned) search

* For a query, compute its embedding, pick the target bucket with argmax, and compute distances only inside that bucket.

```python theme={null}
# indexed_search.py
def indexed_search(query: str, top_k: int = 2):
    q = embed(query)
    target_group = int(np.argmax(q))

    # Compare only against vectors inside the selected group.
    candidate_ids = index_groups[target_group]
    scores = []
    checks = 0
    for i in candidate_ids:
        checks += 1
        dist = np.linalg.norm(q - np.array(embeddings[i]))
        scores.append((dist, docs[i]))

    scores.sort(key=lambda x: x[0])
    return scores[:top_k], checks, target_group

indexed_top, indexed_checks, used_group = indexed_search(query)
print("Used group:", used_group)
print("Top results:", indexed_top)
print("Distance checks:", indexed_checks)
```

Compare linear vs indexed search

* The linear scan checks every vector (6 checks in this demo).
* The toy index prunes to the selected bucket; for our example it checks only the vectors in that bucket (2 checks), saving work.

```python theme={null}
# compare_results.py
print("\nComparison")
print("-- Linear scan checks:", linear_checks)
print("-- Indexed search checks:", indexed_checks)
print("-- Saved checks:", linear_checks - indexed_checks)
```

Example outputs for this demo

* Used group: 0
* Top results (indexed): `('book flight ticket', distance ~1.4142)`, `('hotel room reservation', distance ~1.4142)`
* Distance checks (indexed): 2
* Comparison:
  * Linear scan checks: 6
  * Indexed search checks: 2
  * Saved checks: 4

<Callout icon="lightbulb">
  This toy index is intentionally simple to demonstrate pruning. Production vector databases use much more advanced indexing strategies (examples: [IVF](https://github.com/facebookresearch/faiss/wiki/Indexing), [HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world_graph), [PQ](https://en.wikipedia.org/wiki/Product_quantization)) and often manage indexing automatically behind the scenes.
</Callout>

Summary and takeaway

* Linear (brute-force) search computes distances against every stored vector and does not scale well.
* Indexing partitions or prunes candidate vectors so queries require far fewer distance checks.
* Even a trivial 3-bucket partition illustrates how pruning reduces checks from 6 to 2 in this example.
* Understanding indexing (and index types) is crucial when designing large-scale vector search systems.

Further reading and references

* [ChromaDB docs](https://www.trychroma.com/docs/usage)
* [Jupyter](https://jupyter.org)
* FAISS (IVF, PQ) and HNSW resources linked above for deeper exploration.

That's it for this lesson — see you in the next article.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/dc7ea314-60b9-41b6-b63c-4a49c95a4e7a/lesson/1493a62e-d381-43e7-982f-d4fe1cd78f4b" />
</CardGroup>


# HNSW Construction and Adoption

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Internals/HNSW-Construction-and-Adoption/page

Guide to constructing and tuning HNSW graphs for vector search, detailing insertion, layer assignment, neighbor selection, and key parameters M efConstruction and ef for performance trade-offs

Hello and welcome back.

Now that HNSW is understood as a multi-layer graph, this guide shows how to build and use it in practice. We walk through how a new vector is inserted and how the structure is tuned for performance.

Insertion into HNSW is a multi-step process:

1. Assign a random maximum layer to the new vector\
   Each new element is assigned a random maximum layer. Higher layers are exponentially rarer than lower ones, producing a pyramid-like topology: only a small subset of vectors appear in top layers while most vectors remain near the base. This sparsity at higher layers keeps long-range routing efficient. The distribution is controlled by a level-distribution parameter (often tied to `M` and implementation defaults).

2. Navigate from the top layer down to the target layer\
   Insertion starts from a global entry point (typically a node located in the top layer). At each layer, the algorithm performs a greedy search: move to the neighbor that is closer to the new vector repeatedly until reaching a local minimum (no neighbor is closer). That local minimum becomes the entry point for the next lower layer. Repeat this until you reach the layer where the new vector will be inserted.

3. Connect the new vector to its neighbors\
   For every layer where the new vector should appear, HNSW performs a best-first search (candidate list size determined by `efConstruction`) to find the best neighbor candidates. The algorithm then connects the new node to up to `M` nearest neighbors at that layer. Connections are bidirectional—if A connects to B, B also links back to A—ensuring bidirectional navigability.

4. Prune and select neighbors (diversification)\
   If connecting the new node would exceed a node’s `M` limit, a neighbor-selection heuristic prunes connections to keep the closest and most diversifying neighbors. This diversification preserves search quality while preventing layers from becoming overly dense.

Key parameters that control HNSW behavior

<Frame>
  <img alt="The image is a flowchart explaining the steps for HNSW (Hierarchical Navigable Small World) construction and adoption, detailing the process of inserting a new vector into the structure." />
</Frame>

| Parameter         | What it controls                                     | Typical effect / guidance                                                                                                        |
| ----------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `M`               | Maximum number of connections per node at each layer | Higher `M` → better connectivity and recall but more memory and maintenance overhead. Common defaults: `16` or `32`.             |
| `efConstruction`  | Candidate list size during index construction        | Larger `efConstruction` → better-connected index and higher recall, at the cost of slower indexing and more memory during build. |
| `ef` / `efSearch` | Candidate list size during queries                   | Larger `ef` → higher recall at query time, but with increased query latency. Tune to the desired recall/latency balance.         |

Tuning notes:

* Increase `efConstruction` and/or `M` to improve index quality (higher recall) — expect longer build times and greater memory use.
* Increase query `ef` to improve accuracy at query time — expect longer queries.
* Typical production strategy: tune `efConstruction` and `M` once (at index build time), then adjust `ef` dynamically per-query to meet latency/recall requirements.

<Callout icon="lightbulb">
  Tune `efConstruction` to prioritize index-build quality and tune `ef` at query time to meet your recall versus latency goals. Higher values improve recall but consume more resources.
</Callout>

Why HNSW is popular

* High recall: HNSW often achieves very high recall (commonly in the mid-90s to high-90s percentiles), approximating true nearest neighbors closely.
* Very fast queries: On modern hardware, many queries run in sub-millisecond to single-digit-millisecond ranges, making HNSW suitable for real-time applications.
* Tunable trade-offs: `M`, `efConstruction`, and `ef` let you balance accuracy, build time, memory, and query latency.
* Broad ecosystem adoption: Many vector databases and libraries use HNSW as a default or recommended index (for example, [Pinecone](https://www.pinecone.io/), [Weaviate](https://weaviate.io/), [Qdrant](https://qdrant.tech/)). If you use production semantic search or recommendation systems, they’re likely powered by HNSW or a variant.

The trade-off: HNSW stores explicit links between vectors, so it typically requires more memory than simpler approximations (for example, inverted-file or PQ-based methods). In many applications the extra memory cost is justified by the speed and accuracy gains.

<Frame>
  <img alt="The image explains the construction and adoption of HNSW, detailing steps for inserting a new vector and highlighting its advantages. It also lists HNSW as the default index in several platforms such as Pinecone and Weaviate." />
</Frame>

Summary
HNSW construction centers on four ideas:

1. Assign elements to exponentially distributed layers.
2. Navigate from a top-level entry point down using greedy search.
3. Connect new elements to up to `M` neighbors per layer using a best-first search sized by `efConstruction`.
4. Prune neighbors to preserve diversity and sparsity.

Properly tuning `M`, `efConstruction`, and `ef` lets you trade recall, indexing cost, memory, and query latency—making HNSW a practical default for production vector search.

That concludes the HNSW construction and adoption overview.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/dc7ea314-60b9-41b6-b63c-4a49c95a4e7a/lesson/119f9dd9-f0d8-4a0a-8f20-300c8519e814" />
</CardGroup>
