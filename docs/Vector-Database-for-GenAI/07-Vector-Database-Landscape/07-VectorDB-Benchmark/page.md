# VectorDB Benchmark

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Landscape/VectorDB-Benchmark/page

Open-source VDBench benchmarking for vector databases, comparing cost-normalized latency and throughput, streaming ingestion impact, recall versus performance, and filtered-search to guide production choices

Hello and welcome back.

Now that we've covered how to think about choosing the right vector database, the next question is: how do you measure which one actually performs better? This article walks through a real open-source benchmarking leaderboard called VDBench and explains how to interpret its key metrics so you can make data-driven choices for production vector search.

<Frame>
  <img alt="The image shows a leaderboard of vector search latency and QPS at a $1,000 monthly cost for different cloud services. It includes a bar chart comparing P99 latency and QPS for each service." />
</Frame>

## 1) Cost-normalized latency and QPS (fixed \$1,000 monthly budget)

Why fix the cost? Comparing raw performance without equalizing infrastructure spend is like comparing a sports car to a hatchback — not fair. VDBench fixes the budget at `$1,000/month` and asks: given that spend, what throughput (`QPS`) and tail latency (`P99`) can each database deliver?

This cost-normalized view surfaces real-world price/performance trade-offs. Key points:

* Use the dataset size selector (commonly `1M` or `10M` vectors) because index size affects memory, I/O patterns, and resource consumption.
* Rankings can change with dataset scale; validate the scale that mirrors your production workload.
* The leaderboard snapshot above shows Alibaba Cloud leading at this budget point, followed by services like AWS OpenSearch and Elastic Cloud — but your dataset and index configuration may change the order.

## 2) Streaming (ingestion-aware) performance

In production you rarely run only reads or only writes. Embeddings are ingested continuously while users query the system. VDBench measures search performance while concurrent inserts occur (for example, 500 or 1,000 rows/sec) to show how systems behave under realistic, mixed workloads.

<Frame>
  <img alt="The image shows a bar chart depicting streaming performance benchmarks for various cloud services under different ingestion pressures, comparing static and constant ingestion scenarios. The chart evaluates performance using QPS (Queries Per Second) metrics for services like ZillizCloud, Pinecone, and OpenSearch." />
</Frame>

Think of the static (no concurrent ingest) bar as the restaurant when it's empty, and the streaming bars as the dinner rush. The difference shows the "performance tax" of ingest:

* Look at both `QPS` under ingestion and `P99` under ingestion.
* Some systems maintain throughput but increase tail latency; others drop throughput significantly.
* Choose databases that match your read/write mixing requirements if you perform continuous ingest.

<Frame>
  <img alt="The image is a bar graph comparing streaming performance, measured in P99 latency, of different cloud services under various conditions of constant ingestion." />
</Frame>

This `P99` view highlights tail-latency sensitivity during ingestion. Even a small number of slow requests can degrade user experience in latency-sensitive applications.

## 3) Performance vs. Recall (throughput vs. quality trade-off)

Recall measures how many of the true nearest neighbors the search returns (for example, `recall = 0.95` means 95% of true neighbors were returned). Higher recall often requires scanning more candidates or using more accurate but expensive parameters, which reduces throughput.

<Frame>
  <img alt="The image shows a &#x22;Performance vs. Recall&#x22; graph comparing different datasets on query-per-second (QPS) performance. Various algorithm performances are plotted, each represented by a different colored line." />
</Frame>

This chart plots `QPS` vs `recall`. The ideal system sits at the top-right (high throughput and high recall). Key guidance:

* Decide the recall threshold your application requires (e.g., RAG pipelines typically need high recall to preserve context quality).
* Compare systems at equivalent recall thresholds rather than at default settings.
* Scale changes (1M → 10M) will shift the curve; re-evaluate at your target scale.

See [Fundamentals of RAG](https://learn.kodekloud.com/user/courses/fundamentals-of-rag) for context on why recall matters for downstream LLM quality.

## 4) Filtered-search performance (vector + metadata)

Most real-world searches add metadata filters (e.g., category, date range, tenant). Filtering can change execution plans and resource usage dramatically.

* Evaluate `QPS`, `P99`, and `recall` with filters enabled.
* Some databases excel at pure vector search but degrade heavily once filters are applied.
* If your application relies on attribute-scope (e.g., multi-tenant isolation or date-based filtering), prioritize filtered-search benchmarks.

## Quick reference: What each metric tells you

| Metric                |                            What it measures | Why it matters                                    | Action                                        |
| --------------------- | ------------------------------------------: | ------------------------------------------------- | --------------------------------------------- |
| `QPS`                 |          Throughput at given latency target | How many queries/sec you can serve                | Use for capacity planning                     |
| `P99`                 |              Tail latency (99th percentile) | Worst-case latency that impacts UX                | Use to size resources and assess stability    |
| `Recall`              | Fraction of true nearest neighbors returned | Search quality for RAG / relevance-sensitive apps | Set recall targets and compare across systems |
| Streaming performance |  `QPS` and `P99` under concurrent ingestion | Real-world mixed workload behavior                | Test with your ingest rate                    |
| Filtered search       |           Performance with metadata filters | Production query patterns                         | Benchmark queries with your filters           |

> **lightbulb** VDBench is open source: its methodology and code are publicly available, so you can reproduce every result yourself. Prefer transparent, reproducible benchmarks over vendor-only claims to increase confidence in performance comparisons.

> **warning** Beware of cherry-picked results. Always run benchmarks with dataset sizes, recall targets, and ingest patterns that reflect your production workload before choosing a database.

## How to use the leaderboard effectively (practical checklist)

* Select the dataset size (`1M`, `10M`, etc.) that matches your projected scale.
* Pick a recall threshold that reflects downstream quality requirements (e.g., `0.95` for RAG).
* Run streaming tests with your expected ingest rate to validate mixed-workload behavior.
* Include realistic filters and attribute queries if your product uses metadata scoping.
* Normalize cost (e.g., `$1,000/month` or your target budget) to understand price/performance.
* Reproduce tests with the open-source benchmark to validate results for your region/cloud/provider.

## Conclusion

VDBench surfaces the most important dimensions for choosing a vector database: cost-normalized latency/QPS, ingestion-aware stability, the throughput-vs-recall trade-off, and filtered search behavior. Use these dimensions together — and validate with your data and workloads — to select the best fit for your application and budget.

That is it for this lesson. Speak with you in the next lesson.

## Links and references

* [Fundamentals of RAG — course](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)
* VDBench — open-source benchmark (search the project repo or website to reproduce results)

- [Watch Video](https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/4fee20e9-5def-4971-b7a9-9363aaeb73c2/lesson/616afa70-0f09-4edb-8760-fe75b0885466)
