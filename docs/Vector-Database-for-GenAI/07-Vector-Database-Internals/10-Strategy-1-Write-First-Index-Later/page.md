# Strategy 1 Write First Index Later

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Internals/Strategy-1-Write-First-Index-Later/page

Explains the write-first, index-later pattern where writes are durably logged and acknowledged immediately while indexing happens asynchronously to reduce latency and ensure durability with eventual consistency.

Keeping an index consistent while data is continuously changing is hard. This lesson introduces a widely used solution: write-first, index-later. The core concept is simple and powerful: persist incoming writes immediately, acknowledge the user quickly, and update the searchable index asynchronously when the system can do so. This approach reduces user-facing latency while guaranteeing durability.

## How it works (high level)

1. Append the incoming write (insert/update) to a durable write-ahead log. Appending and flushing is very fast because it is sequential I/O.
2. Return success to the client as soon as the log write is safely persisted.
3. A background indexing worker consumes the log asynchronously, batching many entries and applying consolidated updates to the index.

Think of it like jotting a quick note during a meeting and filing it properly later: the information is saved right away; the organized filing (indexing) happens when time and resources allow.

In database systems this pattern is commonly implemented with a write-ahead log (WAL). Persisting first provides both low-latency writes and a reliable recovery point — if the system crashes you can replay the log to restore state. See the diagram below for the end-to-end flow.

<Frame>
  <img alt="The image explains the &#x22;Write First, Index Later&#x22; strategy, highlighting the process of fast data writing by appending to a log file immediately, followed by indexing later in the background to ensure fast and safe writes without blocking the user." />
</Frame>

## Why this strategy works

* Low write latency: user requests are acknowledged immediately, without blocking on expensive index updates.
* Durability: writes are persisted to stable storage before acknowledging success.
* High throughput: indexers can batch many log entries into larger, more efficient index operations.
* Fault tolerance: after failure, the persisted log enables replay and index reconstruction.

## Benefits vs Trade-offs

| Benefit                                     | Trade-off                                                                                          |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Fast, predictable write latency             | Eventual consistency — recent writes may not be immediately visible in the index or search results |
| Durable persistence via an append-only log  | Added system complexity: log retention, background workers, checkpointing, and replay logic        |
| Better indexing throughput through batching | Storage growth management required (compaction/checkpointing)                                      |

## Practical considerations and implementation tips

* Durable log management: rotate, compact, and checkpoint logs to prevent unbounded growth.
* Background workers: design indexers to consume at whatever rate system resources permit, with backpressure and idempotency.
* Batching and coalescing: combine multiple updates to the same key to reduce redundant index work.
* Recovery and replay: ensure replay logic is deterministic and compatible with your index format.
* Observability: monitor the lag between log persistence and index application to detect issues early.

> **lightbulb** Write-first, index-later is ideal when low write latency and durability are top priorities and your application can tolerate eventual consistency for reads.

## When to use this pattern

* High write volumes where immediate acknowledgment matters (e.g., profile updates, telemetry collection).
* Systems where reads can accept slight staleness or where a secondary fast read path (cache) covers most reads.
* Architectures that already rely on append-only logs (WALs, Kafka, or CDC streams).

## When this pattern may not be appropriate

* Applications that require strong read-after-write consistency for all operations.
* Small systems where the added complexity of background indexing outweighs the performance gains.

## Production examples

Many large-scale platforms persist user changes immediately and let search or analytics indices catch up asynchronously. For example, social networks often accept a profile edit instantly and update full-text search indices later to avoid blocking the user.

## Links and references

* [Write-ahead logging (WAL)](https://en.wikipedia.org/wiki/Write-ahead_logging) — overview and motivation
* [Apache Kafka](https://kafka.apache.org/) — an example durable log used for streaming and indexing pipelines
* [Change Data Capture (CDC) patterns](https://en.wikipedia.org/wiki/Change_data_capture) — techniques for propagating changes

The "Merge Small Pieces" strategy focuses on how to combine many small index updates efficiently.

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/dc7ea314-60b9-41b6-b63c-4a49c95a4e7a/lesson/2a1b44e6-b2f3-4e1f-8e26-3f996dcb40f5)
