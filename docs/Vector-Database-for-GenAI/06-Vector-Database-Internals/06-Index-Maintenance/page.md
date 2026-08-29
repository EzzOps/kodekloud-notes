# Simplified HNSW query outline
entry = graph.top_entry_point
for level in descending_layers:
  entry = greedy_search(entry, query_vector, level)
# At level 0:
result = best_first_search(entry, query_vector, efSearch, k)
return result
```

The greedy steps are fast because nodes have few links in upper layers and you only follow links that improve distance. The bottom layer’s best-first search explores a candidate set and balances recall vs latency via `efSearch`.

<Frame>
  <img alt="The image illustrates the HNSW Search Process in three steps, showing entry at different layers, refining connections, and performing a final search to find the nearest neighbor." />
</Frame>

Key parameters and their effects

|                          Parameter | Purpose                                                      | Typical effect / tuning guideline                                                 |
| ---------------------------------: | ------------------------------------------------------------ | --------------------------------------------------------------------------------- |
|                                `M` | Max connections per node (graph degree)                      | Higher `M` → better recall and connectivity, more memory and slower construction. |
|                   `efConstruction` | Size of the dynamic candidate list during index build        | Larger → higher-quality index, longer build times and more memory.                |
|                         `efSearch` | Size of the candidate list at query time (often called `ef`) | Larger → higher recall at query time, increased latency and CPU per query.        |
| `level_mult` (or level generation) | Controls how many layers a node appears in                   | Affects height distribution and average search hops from top to bottom.           |

<Callout icon="lightbulb">
  HNSW is an approximate nearest neighbor algorithm. The most commonly tuned values are `M`, `efConstruction`, and `efSearch`. Adjust these to balance recall, query latency, and memory. For production, benchmark recall vs latency for representative queries and vectors.
</Callout>

Practical considerations and best practices

* Index construction: increase `efConstruction` and `M` if you need higher recall, especially for large or highly clustered datasets. Expect longer build times and higher memory use.
* Query tuning: raise `efSearch` to improve recall for difficult queries; lower it to reduce latency when recall requirements are modest.
* Memory vs performance: higher connectivity (`M`) and larger dynamic lists require more memory. Monitor memory consumption on nodes that host the index.
* Entry point strategy: most implementations pick a randomized or high-degree node as entry. Consistent entry strategies help with predictable latency.
* Parallelism: many HNSW libs support parallel index building and multi-threaded searching — use available cores carefully for a production workload.

Real-world example
Imagine an e-commerce recommendation engine. When a user views a product, the system uses HNSW instead of comparing the current product vector to every catalog item. The index quickly jumps to the correct product region (e.g., shirts, electronics), then refines within that local neighborhood to return relevant recommendations in milliseconds. This is how features like “customers who bought this also bought” are generated in near real time.

References and further reading

* Malkov, Y. A., & Yashunin, D. A. (2018). Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs (HNSW). [Original HNSW paper](https://arxiv.org/abs/1603.09320)
* [Faiss — Facebook AI Similarity Search](https://github.com/facebookresearch/faiss)
* [nmslib — Similarity Search library](https://github.com/nmslib/nmslib)

Next lessons will cover how HNSW integrates inside vector databases (index construction patterns, distributed deployments, and tuning strategies for production). Thanks for reading.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/dc7ea314-60b9-41b6-b63c-4a49c95a4e7a/lesson/2e31bbd2-da64-4ce2-bf07-9a636fe09f85" />
</CardGroup>


# Index Maintenance

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Internals/Index-Maintenance/page

Discusses challenges of maintaining nearest-neighbor vector indexes amid data mutations and strategies like buffering, compaction, and periodic rebuilding to preserve performance and accuracy.

Now that we have vectors stored and compressed, we must confront an important reality: data is not static.

Vector databases are constantly changing. You continuously insert new vectors, update existing ones, and delete obsolete entries. That’s normal for any production datastore, but it creates a problem for the indexes we use for nearest-neighbor search.

Nearest-neighbor indexes (for example, HNSW, IVF, PQ) are often designed and tuned for largely static or append-only datasets. Some structures (like HNSW) support dynamic updates, but frequent mutations can still fragment or stale the index. When the underlying data changes a lot, index components can drift from the true distribution of vectors: partitions and centroids become inaccurate, internal storage grows with many small fragments, and both latency and recall of searches can degrade.

Think of it like maintaining a perfectly cataloged library while patrons continually add books to random shelves and remove others without updating the catalog. Over time, the catalog becomes unreliable and locating books is slower and less accurate.

Also note: even with a managed vector-database service, the provider cannot fully optimize an index for your specific workload and business semantics. You still need engineering effort to maintain index quality for your use case.

Why index maintenance matters

* Performance: Fragmented indexes increase search latency and reduce throughput.
* Accuracy: Out-of-date centroids or partitions hurt recall and precision.
* Cost: Poor index quality forces larger search budgets (more probes, more compute).
* Predictability: Unmaintained indexes produce variable query latencies and inconsistent results.

Common strategies for index maintenance
To handle index maintenance at scale (for example, services like Netflix that add content and update user vectors hourly), teams generally use a mix of three strategies:

1. Write first, index later

* Buffer new writes (for example, in a write log, small in-memory shards, or a write-optimized store) and perform indexing asynchronously in the background.
* Pros: very low write latency; you can batch and tune indexing jobs for throughput.
* Cons: recent writes may be missing or lower-quality in search results until the background indexing completes.

2. Merge small pieces (compaction)

* Periodically merge many small or fragmented index shards into larger, optimized shards (similar to compaction in LSM trees).
* Pros: improves consistency and search performance without a full rebuild.
* Cons: requires scheduling and resource management; merges consume CPU, memory, and I/O while running.

3. Rebuild sometimes

* Run a full reindex from the canonical data store at scheduled intervals or when metrics indicate fragmentation exceeds a threshold.
* Pros: restores optimal index structure and accuracy by clearing accumulated fragmentation.
* Cons: expensive and potentially disruptive for large datasets; usually performed during low-traffic windows or on dedicated infrastructure.

<Frame>
  <img alt="The image explains a problem with data changes affecting search indexes and offers three strategies to keep the index healthy: &#x22;Write first, index later,&#x22; &#x22;Merge small pieces,&#x22; and &#x22;Rebuild sometimes.&#x22;" />
</Frame>

Summary table — quick decision guide

| Strategy                        |                                                When to use it | Key benefits                                        | Trade-offs                                                   |
| ------------------------------- | ------------------------------------------------------------: | --------------------------------------------------- | ------------------------------------------------------------ |
| Write first, index later        |           High write volume, tight write latency requirements | Fast writes, batch-friendly indexing                | Recent data may be temporarily unsearchable or lower-quality |
| Merge small pieces (compaction) |                       Steady mutation with many small updates | Keeps index tidy, improves steady-state performance | Requires periodic resources and careful scheduling           |
| Rebuild sometimes               | Periodic full refresh windows or when fragmentation is severe | Restores optimal index structure and accuracy       | Expensive; can be disruptive at scale                        |

Best practices and operational tips

* Monitor index health: track fragment counts, average shard size, query latency, and recall metrics.
* Define SLA-driven policies: decide acceptable staleness and schedule compaction/rebuilds around traffic windows.
* Combine strategies: buffer for low-latency writes, compact frequently to reduce fragmentation, and schedule periodic full rebuilds for a reset.
* Automate thresholds: trigger compaction or full reindexing based on measurable indicators (e.g., shard count, average search recall).
* Test on representative workloads: simulate production traffic to tune merge frequencies and batch sizes.

<Callout icon="lightbulb">
  Choose a mix of buffering, compaction, and periodic rebuilds based on your workload: write volume, read SLAs, and how fresh search results must be.
</Callout>

That concludes the index-maintenance problem statement. We will now discuss the first solution — write first and index later — in detail.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/dc7ea314-60b9-41b6-b63c-4a49c95a4e7a/lesson/66c3ce0a-643e-4781-a0f5-2be8ebf3fd3b" />
</CardGroup>
