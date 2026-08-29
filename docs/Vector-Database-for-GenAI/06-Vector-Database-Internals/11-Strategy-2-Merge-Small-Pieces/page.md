# Strategy 2 Merge Small Pieces

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Internals/Strategy-2-Merge-Small-Pieces/page

Background merging compacts many small write fragments into larger segments to reduce query overhead, balancing write performance and query efficiency through tunable compaction policies.

When you adopt a "write-first, index-later" ingestion model, you optimize for fast writes but often end up with a large number of tiny data fragments. Each small write becomes a separate chunk on disk. Over time, the system accumulates dozens, hundreds, or even thousands of these tiny files.

That fragmentation is particularly costly at query time: search must touch many small files to assemble results. Think of it as searching for one note among thousands of sticky notes — it’s possible, but repeatedly opening and scanning each tiny file adds significant overhead and increases query latency.

The practical solution is to periodically merge those tiny pieces into larger, more efficient units. This background compaction (commonly called segment merge in search and storage systems) combines many small fragments into a single larger segment. With fewer, denser segments, a search engine examines far fewer files, reducing both IO operations and metadata overhead and dramatically improving retrieval performance.

<Frame>
  <img alt="The image depicts &#x22;Strategy 2 – Merge Small Pieces&#x22; for faster search by combining small data chunks into larger pieces, reducing the number of pieces to check. It describes this process as similar to combining sticky notes into a single document." />
</Frame>

Key benefits

* Runs in the background without blocking incoming writes, keeping the system responsive during cleanup.
* Reduces the number of segments a query must scan, lowering per-query overhead and improving retrieval speed.
* Is tunable: administrators can adjust merge frequency, size thresholds, and merge policies to trade off write throughput, storage efficiency, and query latency.

Important trade-offs and tuning tips

<Callout icon="lightbulb">
  Background merging greatly reduces query overhead, but you should tune merge frequency and thresholds to match your workload. For write-heavy systems, favor less aggressive merges to keep write latency low; for read-heavy systems, more aggressive merging improves query performance. Consider metrics such as segment count, average segment size, and query latency when tuning.
</Callout>

<Callout icon="warning">
  Aggressive merging can cause temporary CPU and IO spikes that impact overall throughput. Schedule heavier compaction during off-peak hours and monitor system load to avoid introducing instability.
</Callout>

When to merge vs. when to reindex

* Merge small pieces (compaction) is ideal when fragmentation from frequent small writes causes high query overhead but the index structure itself remains valid.
* Full rebuild/reindex is appropriate when you need to change indexing structure (e.g., new vector codec, different clustering parameters, or schema changes), or when compaction alone cannot recover desired storage or performance characteristics.

Quick comparison

| Strategy               | Use Case                                                   | Pros                                                            | Cons                                                                   |
| ---------------------- | ---------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Merge / Compaction     | Reduce fragment count from write-first ingestion           | Lowers IO & metadata overhead; incremental; keeps system online | Needs careful tuning; can cause IO spikes during merges                |
| Full Reindex / Rebuild | Change index structure or recover from heavy fragmentation | Produces optimal layout and allows structural changes           | Resource-intensive; may require downtime or heavy background resources |

References and further reading

* [Log-Structured Merge Trees (LSM)](https://en.wikipedia.org/wiki/Log-structured_merge-tree) — background on compaction strategies used in many storage engines
* [RocksDB Compaction](https://rocksdb.org/blog) — practical implementations and tuning examples
* [Vector search architectures and segmenting](https://milvus.io/docs/) — examples and design discussions for vector databases

This merge-small-pieces strategy is a pragmatic balance between immediate write performance and long-term query efficiency. When combined with sensible monitoring and tuning, it keeps systems responsive while preventing the performance penalties that arise from too many tiny data fragments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/dc7ea314-60b9-41b6-b63c-4a49c95a4e7a/lesson/cb0ad32b-2e10-47ad-b759-832f53c53b32" />
</CardGroup>
