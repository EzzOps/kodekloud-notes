# HNSW Multi Layered Graph Structure

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Internals/HNSW-Multi-Layered-Graph-Structure/page

Explains HNSW multi-layered graph index for fast approximate nearest neighbor search in vector databases, covering intuition, search workflow, parameters, and practical tuning.

Welcome back. This lesson explains HNSW (Hierarchical Navigable Small World), a multi-layered graph index commonly used inside vector databases to enable fast approximate nearest neighbor (ANN) search.

Why it matters: graph-based indexes like HNSW are the backbone of high-performance vector search. They let systems find similar vectors at scale with low latency while trading off a controlled amount of accuracy. This guide covers the intuition, the search workflow, and practical tuning considerations for HNSW.

What is HNSW (intuition)

* HNSW is conceptually similar to a skip list: a hierarchy of layers where upper layers are sparse and lower layers are increasingly dense.
* Upper layers provide long-range shortcuts for coarse navigation across the embedding space.
* The bottom layer (level 0) contains all vectors and dense local links for precise nearest-neighbor retrieval.

At a glance:

* Top layers: very sparse, long-range links — fast coarse jumps.
* Middle layers: intermediate connectivity — guide search toward the target region.
* Bottom layer: dense connectivity with all points — final fine-grained search.

<Frame>
  <img alt="The image illustrates the HNSW multi-layered graph structure, showing its inspiration from a skip list and detailing three layers with varying densities and connections." />
</Frame>

How HNSW navigates search space

* Entry points at the top layer let you quickly traverse large distances in vector space.
* Each lower layer adds more nodes and more local edges, increasing search accuracy as you descend.
* The algorithm transitions from coarse to fine search: greedy climbs on sparse layers, and a more exhaustive candidate expansion on the bottom layer.

Search workflow (high-level)

1. Provide a query vector and start from an entry point at the highest layer.
2. At each upper layer, perform greedy hill-climbing: repeatedly move to the neighbor that reduces distance to the query until no neighbor is closer. The goal is coarse localization.
3. Take the best point found in the current layer as the entry point into the next (denser) layer.
4. Repeat the greedy descent until reaching level 0 (the bottom layer).
5. At level 0, perform a best-first (priority queue) search controlled by `ef` (often called `efSearch`) to collect the final k nearest neighbors.

Pseudocode (simplified)

```text theme={null}
