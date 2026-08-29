# whoosh_keyword_search.py
import os
import shutil
import tempfile
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

# Create temp index
index_dir = tempfile.mkdtemp()
schema = Schema(title=ID(stored=True), content=TEXT(stored=True))
ix = index.create_in(index_dir, schema)

# Add documents to index
writer = ix.writer()
for t, d in zip(titles, docs):
    writer.add_document(title=t, content=d)
writer.commit()

# Helper to run a keyword query
def whoosh_query(query_text, top_k=10):
    with ix.searcher() as searcher:
        parser = QueryParser("content", ix.schema)
        q = parser.parse(query_text)
        results = searcher.search(q, limit=top_k)
        return [(r["title"], r.score) for r in results]

# Examples
print("Whoosh results for 'engine troubleshooting':", whoosh_query("engine troubleshooting"))
print("Whoosh results for 'piston':", whoosh_query("piston"))

# Cleanup when finished (uncomment to remove index)
# shutil.rmtree(index_dir)
```

Example Whoosh outputs (your scores may vary slightly):

```plaintext theme={null}
Whoosh results for 'engine troubleshooting': [('Engine Troubleshooting 101', 3.688410483089193)]
Whoosh results for 'piston': [('Piston Wear & Compression', 2.110439158172188)]
```

Notes on Whoosh behavior:

* Whoosh returns documents where the query terms appear and ranks by TF-IDF-like importance.
* If a conceptually relevant document doesn't contain the exact query terms (e.g., "Motor Diagnostics Checklist" for the query "engine troubleshooting"), Whoosh will not return it unless the text contains matching tokens.

<Callout icon="warning">
  This example stores the index in a temporary directory. In production or repeated runs, persist the index directory or rebuild as needed. Remember to clean up temporary files to avoid disk bloat (`shutil.rmtree(index_dir)`).
</Callout>

## 2) Semantic search with SentenceTransformers (cosine similarity)

Semantic search embeds documents and queries into a vector space and ranks by vector similarity (cosine). This approach captures conceptual relationships beyond exact token overlap. We use the `paraphrase-MiniLM-L6-v2` model for compact, fast embeddings.

```python theme={null}
# semantic_search.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Query used for comparison
query_text = "engine troubleshooting"

# Embed documents and query (normalized embeddings)
doc_embeddings = model.encode(docs, convert_to_numpy=True, normalize_embeddings=True)
query_embedding = model.encode([query_text], convert_to_numpy=True, normalize_embeddings=True)

# Compute cosine similarity and rank (descending)
sims = cosine_similarity(query_embedding, doc_embeddings).flatten()
sem_hits_idx = np.argsort(-sims)
sem_hits = [(titles[i], float(sims[i])) for i in sem_hits_idx]

# Top semantic hits
sem_hits[:6]
```

Example semantic ranking (scores will vary by model version and environment):

```plaintext theme={null}
[
  ('Engine Troubleshooting 101', 0.84),
  ('Valve Timing Problems', 0.63),
  ('Motor Diagnostics Checklist', 0.61),
  ('Piston Wear & Compression', 0.46),
  ('Airflow & Intake Issues', 0.42),
  ('Oil System Basics', 0.35)
]
```

Why semantic search differs:

* The embedding model captures conceptual similarity, so queries like "engine troubleshooting" will surface "motor diagnostics" and "valve timing" even without exact word overlap.
* Semantic retrieval improves recall for related documents; TF-IDF provides more precision for literal matches.

## 3) Compare TF-IDF and Semantic rankings side-by-side

We can combine Whoosh (TF-IDF) hits and SentenceTransformers (cosine similarity) hits into a pandas DataFrame to compare ranks and scores. This lets you directly inspect differences in ordering and the presence/absence of documents in each result set.

```python theme={null}
# compare_rankings.py
import pandas as pd

# Assume kw_hits is the list returned by the whoosh_query for the given query
kw_hits = whoosh_query(query_text)  # from the Whoosh example above
sem_hits = sem_hits                   # from the semantic example above

# Normalize/pretty print both lists with rank
kw_df = pd.DataFrame(kw_hits, columns=["Title", "TFIDF_Score"])
kw_df["KW_Rank"] = range(1, len(kw_df) + 1)

sem_df = pd.DataFrame(sem_hits, columns=["Title", "CosineSim"])
sem_df["SEM_Rank"] = range(1, len(sem_df) + 1)

# Merge on title to show both ranks together
comparison = pd.merge(sem_df, kw_df, on="Title", how="outer")

# Sort by semantic rank to highlight semantic ordering
comparison_sorted = comparison.sort_values(by="SEM_Rank", na_position="last")

comparison_sorted[["Title", "SEM_Rank", "CosineSim", "KW_Rank", "TFIDF_Score"]]
```

Sample comparison table output:

```plaintext theme={null}
                      Title  SEM_Rank  CosineSim  KW_Rank  TFIDF_Score
0  Engine Troubleshooting 101         1       0.84      1.0     3.688410
2      Valve Timing Problems         2       0.63      NaN         NaN
3  Motor Diagnostics Checklist         3       0.61      NaN         NaN
1   Piston Wear & Compression         4       0.46      NaN         NaN
4       Airflow & Intake Issues         5       0.42      NaN         NaN
5              Oil System Basics         6       0.35      NaN         NaN
```

Performance and practical considerations:

| Method                | Strengths                                             | Typical Use Cases                                  | Example behavior on "engine troubleshooting"                                                      |
| --------------------- | ----------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| TF-IDF (Whoosh)       | Fast, interpretable, precise for exact token matches  | Keyword search, filtering, small to medium corpora | Finds documents that contain the exact words "engine" and "troubleshooting" (high score)          |
| Semantic (Embeddings) | Captures conceptual similarity, robust to paraphrases | QA retrieval, recommendation, broader recall       | Returns "Motor Diagnostics Checklist" and "Valve Timing Problems" even without exact term overlap |

Interpretation:

* Whoosh (TF-IDF) excels at precision for literal queries and is simple to run locally.
* Semantic search returns documents ranked by conceptual relevance and can surface related material that lacks exact tokens from the query.
* A hybrid approach often works best: use TF-IDF for exact matches and embeddings to expand recall, or rerank TF-IDF candidates with embeddings for a balance of speed and semantic quality.

Conclusion

* This lesson illustrated the differences between keyword (TF-IDF) search and semantic retrieval using a small corpus.
* You can run the provided notebook-style code to experiment with queries, model choice, and ranking strategies.

Links and References

* Whoosh documentation: [https://whoosh.readthedocs.io/](https://whoosh.readthedocs.io/)
* SentenceTransformers: [https://www.sbert.net/](https://www.sbert.net/)
* scikit-learn cosine similarity: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine\_similarity.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
* pandas: [https://pandas.pydata.org/](https://pandas.pydata.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/316bc17d-74b4-4bc8-bac7-62286dc8eee8/lesson/f2ccbff1-5fad-4887-a049-04c1d6af8eec" />
</CardGroup>


# Introduction to Retrieval Methods

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Keyword-Search-Retrieval/Introduction-to-Retrieval-Methods/page

Guide to retrieval methods and system design for retrieval augmented generation covering hybrid, sparse and dense search, chunking, re-ranking, caching, security, observability, and operational trade-offs

This lesson explains retrieval methods and the critical design considerations for building retrieval-augmented generation (RAG) systems. Retrieval is the foundation of RAG quality: an LLM generates grounded answers only when the retrieved context is relevant and correct. Even a strong LLM will produce incorrect output if retrieval returns irrelevant or wrong documents.

<Frame>
  <img alt="The image explains the importance of retrieval in Retrieval-Augmented Generation, highlighting that if retrieval is incorrect, the resulting answer will be wrong despite a strong model, showing a combination of LLM and a knowledge base." />
</Frame>

Key system design dials

* Latency — users expect fast responses; the retrieval path must be optimized for P95/P99 latency.
* Cost — compute (re-rankers, LLM tokens) and storage (indexes, embeddings) grow with scale.
* Trust — freshness, provenance, and cited answers increase user confidence.

<Frame>
  <img alt="The image explains why retrieval matters, highlighting two points: latency issues because people won’t wait, and cost concerns as compute and storage add up." />
</Frame>

Common failure modes

* Wrong chunking: retrieving tangential fragments instead of the exact answer.
* Stale index: returning outdated information because the index wasn’t refreshed.
* ACL leaks: returning documents a user shouldn’t see.

Plan mitigations early (refresh schedules, fine-grained ACLs, chunking rules) and add observability so you can detect these failure modes quickly.

<Frame>
  <img alt="The image explains why retrieval matters, highlighting three issues: wrong chunk retrieval resulting in irrelevant content, stale index causing outdated information, and ACL leak leading to unauthorized data exposure." />
</Frame>

Retrieval pipeline (high level)

* Ingest: split documents into chunks, create embeddings, and index them.
* Query: convert user query to keywords + vector, perform filtered searches, and re-rank candidates.
* Generation: pack and send the assembled context + query to the LLM to produce a grounded answer.

Each stage is an opportunity to measure, optimize, and secure data flows.

<Frame>
  <img alt="The image outlines a retrieval pipeline consisting of three phases: Ingest Phase for data indexing, Query Phase for retrieval and filtering, and LLM Generation for producing responses." />
</Frame>

Cross-cutting concerns

* Security: enforce who can see what (ACLs, filtering, query-time authorization).
* Caching: accelerate the fast path to reduce latency and cost.
* Observability: instrument ingest, retrieval, re-ranking, and generation for latency, error rates, and data correctness.

<Frame>
  <img alt="The image is a diagram titled &#x22;Retrieval Pipeline at a Glance,&#x22; featuring three key components: Security, Caching, and Observability, each with a brief description and an icon." />
</Frame>

Retrieval methods — quick overview

* Sparse search (keyword-based): precise for exact tokens, code snippets, error strings, and legal text.
* Dense retrieval (embeddings): finds semantic matches and paraphrases; good for natural-language questions and cross-lingual queries.
* Hybrid search: fuses sparse + dense signals (often via score fusion). A safe default because it captures both exact matches and paraphrases.

Recommendation: start with hybrid search for broad coverage, monitor failure modes, and then optimize weights and tuning based on real traffic data.

Chunking basics

Chunking breaks documents into retrieval units. Chunk size and overlap strongly affect recall and precision:

* Smaller chunks → higher precision, but can lose global context.
* Larger chunks → preserve context, but may decrease specificity and increase token costs.

<Frame>
  <img alt="The image illustrates the concept of chunking with the emphasis on &#x22;High Recall Wins&#x22; and explains that smaller chunks provide better precision but may lose context." />
</Frame>

Common chunking approaches

* Fixed-size chunks (tokens or characters) with a small overlap (10–20%) to preserve continuity.
* Semantic chunks aligned to natural boundaries (sections, paragraphs).
* Structure-aware chunking that preserves headings, titles, and document hierarchy.

Preserve document structure and attach rich metadata (titles, section headers, source IDs). Metadata helps re-rankers and the LLM understand relationships between chunks.

<Frame>
  <img alt="The image explains &#x22;Chunking Basics: High Recall Wins&#x22; with two types of text chunking: fixed-size chunks and semantic chunks." />
</Frame>

Preserve structure and metadata

1. Keep titles and section headers with their content.
2. Maintain logical document hierarchy when chunking.
3. Add metadata fields (source, section ID, published timestamp) to each chunk.

<Frame>
  <img alt="The image outlines &#x22;Chunking Basics&#x22; for achieving high recall, emphasizing the importance of preserving structure through three steps: keeping titles and section headers with content, maintaining logical document hierarchy, and adding rich metadata." />
</Frame>

Special cases

Tables, code blocks, images, and scanned documents often need dedicated extractors or OCR and syntax-aware chunkers. Source code should be treated differently from prose—preserve imports, function boundaries, and call graphs. Consider language-aware chunking for code and binary data.

Vector search

Two common ANN index families to consider:

| Index family                              | When to use                                                        | Notes                                                                            |
| ----------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| HNSW (Hierarchical Navigable Small World) | Default for many production setups where recall and latency matter | Excellent recall and low-latency queries; higher memory footprint                |
| IVF / IVF-PQ                              | Very large corpora where memory is constrained                     | More memory-efficient, can be faster at scale if tuned; higher tuning complexity |

Important tuning knobs

* `K` (candidates): number of nearest neighbors returned by the ANN search. Typical starting points: `K=50` for re-ranking pipelines, `K=10` for direct results.
* `efSearch` / `nprobe`: controls internal search breadth. Higher values increase recall at the cost of latency (`efSearch` for HNSW; `nprobe` for IVF/IVF-PQ).

Start with HNSW defaults, measure P95 latency and Precision\@K on real traffic, then tune `K` and `efSearch`/`nprobe` against your SLAs.

<Frame>
  <img alt="The image is a slide titled &#x22;Vector Search in One Slide,&#x22; highlighting two parameters: &#x22;K (candidates)&#x22; for retrieving nearest neighbors and &#x22;efSearch/nprobe&#x22; for controlling the recall-latency tradeoff, with a suggestion to start with HNSW defaults and monitor performance metrics." />
</Frame>

Re-ranking and context packing

Typical flow

1. Initial retrieval (hybrid) returns top N candidates (e.g., top 50).
2. Cross-encoder re-ranker scores query-document pairs with a more expensive model and selects a smaller, high-precision set (e.g., top 5).
3. Context packing: dedupe, order by relevance and document structure, and assemble the context with citations for transparency.

This “cheap broad retrieval → expensive targeted re-ranking” pattern converts good retrieval into great retrieval.

<Frame>
  <img alt="The image outlines a process for reranking and context packing, including initial retrieval of candidates, cross-encoder reranking of query-document pairs, and context packing for relevance and citation." />
</Frame>

Costs and trade-offs

* Cross-encoder re-ranking often yields 15–30% better relevance for the final assembled context but increases compute cost.
* Always set timeouts: if re-ranking exceeds the budget, fallback to initial candidates. Users generally prefer a fast, approximate answer to a slow, perfect one.

<Frame>
  <img alt="The image outlines the benefits of reranking and context packing, highlighting improved precision, 15-30% better relevance, and enhanced retrieval in RAG systems." />
</Frame>

Graceful degradation

Implement fallback paths to cheaper or cached results when re-rankers or downstream services are slow. Maintain user experience by returning timely answers even during partial failures.

<Frame>
  <img alt="The image is a slide titled &#x22;Reranking and Context Packing,&#x22; explaining why time budgets matter. It lists three points: setting timeouts, valuing speed over perfect answers, and maintaining performance during slowdowns." />
</Frame>

Operational knobs and caching

Key configuration knobs to monitor and tune:

* Hybrid weights (sparse vs dense).
* Retrieve depth (`K` candidates).
* ANN search parameters (`efSearch` / `nprobe`).
* Re-rank depth (how many candidates to re-score).

Caching recommendations

* Cache query embeddings for frequent queries.
* Cache ANN candidate sets and assembled context packs for hot queries.
* Use cache warming for predictable traffic (e.g., daily reports, scheduled queries).

<Frame>
  <img alt="The image outlines a caching strategy involving embeddings, candidate sets, and context packs with suggestions for caching query embeddings, ANN results, and assembled contexts. It also recommends using cache warming for predictable traffic patterns." />
</Frame>

Example SLOs (starting points)

| Metric                | Example target                            |
| --------------------- | ----------------------------------------- |
| Latency (end-to-end)  | \~700 ms (tune to your application)       |
| Freshness (index lag) | \~10 minutes (depends on data volatility) |
| Security              | Zero critical ACL leaks                   |
| Availability          | ≥ 99.9%                                   |

Start conservative, measure real traffic, and iterate.

Takeaways

* Start with hybrid search as a safe default for production.
* Invest in chunking and metadata: preserve structure, include titles/headers/source IDs, and choose chunk sizes and overlaps based on use case.
* Instrument every stage (ingest, retrieval, re-ranking, context assembly) for latency, accuracy, and security metrics — you can’t optimize what you don’t measure.
* Use re-ranking selectively where it produces measurable precision gains; don’t re-rank everything by default.
* Implement timeouts and graceful degradation so the system remains responsive under load.

<Callout icon="lightbulb">
  Begin with hybrid search, put effort into chunking and metadata, and instrument the pipeline. Optimize re-ranking and caching based on measured cost-benefit for your workload.
</Callout>

Further reading and references

* HNSW: [https://github.com/nmslib/hnswlib](https://github.com/nmslib/hnswlib)
* FAISS (IVF/PQ): [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Dense vs. sparse retrieval overview: [https://arxiv.org/abs/2004.08266](https://arxiv.org/abs/2004.08266)
* Best practices for RAG pipelines: search for “retrieval-augmented generation best practices”

This material next dives deeper into re-ranking and how to measure its cost-benefit trade-offs before rolling it out broadly.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/316bc17d-74b4-4bc8-bac7-62286dc8eee8/lesson/a5beb0d3-88fa-441c-95ee-b710f6989379" />
</CardGroup>
