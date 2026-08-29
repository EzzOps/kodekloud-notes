# Real World Example of Quantization

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Internals/Real-World-Example-of-Quantization/page

Demonstrates how vector embedding quantization reduces storage and improves large-scale e-commerce search performance while balancing accuracy, indexing, and retrieval trade-offs.

Welcome back.

Now that we’ve covered the core quantization methods, this lesson demonstrates how they perform in a high-scale production environment. We’ll use a concrete scenario — an e-commerce product search at scale — to show how quantization interacts with indexing and retrieval to deliver large infrastructure savings while preserving user experience.

## Concrete example: why quantize?

Imagine 50 million product embeddings with \~1,000 dimensions each. Storing these as float32 quickly becomes expensive:

```text theme={null}
50,000,000 items × 1,000 dims × 4 bytes (float32) = 200,000,000,000 bytes ≈ 200 GB
```

Converting embeddings from float32 to int8 (scalar quantization) reduces the per-value storage to 1 byte, yielding roughly a 4× compression:

```text theme={null}
50,000,000 items × 1,000 dims × 1 byte (int8) = 50,000,000,000 bytes ≈ 50 GB
```

Beyond memory reduction, quantization reduces cache pressure, lowers I/O and network transfer costs, and often improves throughput and latency for vector searches at scale.

## Production pipeline: ingestion → quantization → indexing → search

Below is a typical production pipeline that makes large-scale, low-latency vector search feasible.

Step 1 — Ingestion

* Extract product metadata (titles, descriptions, attributes).
* Embed texts using a model to produce high-dimensional float vectors (full-precision embeddings).
* Persist full-precision vectors until the chosen batch or streaming quantization step is applied.

Step 2 — Quantization

* Convert full-precision floats (usually float32) to lower-precision representations (commonly int8 for scalar quantization).
* This typically yields \~4× memory reduction (excluding small per-channel scales/zero-points), lowers network transfer, and reduces cache/memory bandwidth pressure.
* Quantization is lossy and introduces approximation error; evaluate retrieval quality on representative queries to tune parameters (per-channel scales, zero-points, or more advanced schemes).

<Callout icon="lightbulb">
  Quantization reduces memory footprint and speeds up search, but it is lossy. Always validate retrieval quality on representative queries and tune quantization parameters (per-channel scales, zero-points, or more advanced methods) to balance accuracy and resource savings.
</Callout>

Step 3 — Indexing

* Index the quantized vectors with ANN (approximate nearest neighbor) algorithms such as HNSW or IVF.
* ANN indices operate efficiently on compressed representations and enable sub-linear average query time.
* Combine scalar quantization with product quantization (PQ), inverted files, or hybrid schemes to further reduce memory and improve throughput.

Step 4 — Search

* At query time, embed the user query into the same vector space.
* Optionally quantize the query vector and perform ANN search against the compressed index, often using distance computations that avoid full dequantization.
* With good engineering (index sharding, cache-friendly layouts, SIMD/vectorized kernels), you can achieve sub-100 ms latencies at the 50M-item scale.
* The combined effect of quantization + efficient ANN indexing yields major infrastructure savings (the example here can correspond to \~75% lower infrastructure cost) while keeping the experience near-instantaneous.

<Frame>
  <img alt="The image illustrates an e-commerce product search process at scale, showcasing steps for ingesting, quantizing, indexing, and searching product embeddings to achieve efficient and cost-effective results. It compares scenarios with and without quantization, highlighting significant improvements in speed and resource usage with scalar quantization." />
</Frame>

## Quick comparison: trade-offs and when to use what

| Component                        |                                            Benefit | Typical trade-offs / notes                                        |
| -------------------------------- | -------------------------------------------------: | ----------------------------------------------------------------- |
| Scalar quantization (e.g., int8) |                       \~4× compression, faster I/O | Simple, lossy; good baseline for production                       |
| Per-channel quantization         |                   Better accuracy vs. scalar quant | Slightly more metadata (scales/zero-points)                       |
| Product quantization (PQ)        | Much lower memory than int8 for very large corpora | More complex, may require asymmetric distances and careful tuning |
| ANN index (HNSW, IVF, etc.)      |                  Sub-linear query latency at scale | Indexing & memory trade-offs depend on graph/cluster params       |

## Best practices and validation checklist

* Validate retrieval quality on representative queries and business metrics (click-through, conversion).
* Measure end-to-end latencies including embedding generation and network hops.
* Tune quantization parameters (per-channel vs. global scales, symmetric/asymmetric) to balance accuracy and compression.
* Combine quantization with ANN techniques and index optimizations (sharding, caching, vectorized kernels).
* Monitor production drift — re-quantize or re-index periodically as embeddings or product catalogs change.

## Links and references

* HNSW: [https://arxiv.org/abs/1603.09320](https://arxiv.org/abs/1603.09320)
* Product Quantization (PQ): [https://hal.inria.fr/inria-00514415/document](https://hal.inria.fr/inria-00514415/document)
* FAISS (Facebook AI Similarity Search): [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Annoy: [https://github.com/spotify/annoy](https://github.com/spotify/annoy)
* General vector search concepts: [https://www.vectorsearch.org/](https://www.vectorsearch.org/)

I hope this practical walkthrough helps you remember quantization’s role when embedding memory and latency become constraints. That is it for this lesson — see you in the next one.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/dc7ea314-60b9-41b6-b63c-4a49c95a4e7a/lesson/4de36fa5-0cda-4ee2-99bf-3944a2d4ca8c" />
</CardGroup>
