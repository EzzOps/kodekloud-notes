# Prepare BM25
tokenized_corpus = [d.lower().split() for d in docs]
bm25 = BM25Okapi(tokenized_corpus)

# Choose a model (fast general-purpose)
model = SentenceTransformer('all-MiniLM-L6-v2')
doc_emb = model.encode(docs, convert_to_tensor=True, normalize_embeddings=True)
```

## Helper: show results for a query (BM25, semantic, and weighted hybrid)

```python theme={null}
def show_results(query, k=3, alpha=0.8):
    """
    Show BM25 top-k, semantic top-k, and hybrid top-k for `query`.
    alpha: semantic weight in [0,1] for hybrid. hybrid = alpha*semantic + (1-alpha)*bm25
    """
    print(f"\nQUERY: {query}\n" + "="*60)
    # BM25 scores
    bm25_scores = np.array(bm25.get_scores(query.lower().split()))
    top_bm25 = np.argsort(-bm25_scores)[:k]
    print("BM25 top-k:")
    for i in top_bm25:
        print(f"  [{i}] {bm25_scores[i]:.3f}  {docs[i]}")

    # Semantic (SentenceTransformer) scores (cosine similarity)
    q_emb = model.encode([query], convert_to_tensor=True, normalize_embeddings=True)
    cos = util.cos_sim(q_emb, doc_emb)[0].cpu().numpy()
    top_st = np.argsort(-cos)[:k]
    print("\nSemantic (SentenceTransformer) top-k:")
    for i in top_st:
        print(f"  [{i}] {cos[i]:.3f}  {docs[i]}")

    # Normalize both scores into [0,1] to combine them
    bm25_min, bm25_max = bm25_scores.min(), bm25_scores.max()
    bm25_norm = (bm25_scores - bm25_min) / (bm25_max - bm25_min + 1e-9)

    st_min, st_max = cos.min(), cos.max()
    st_norm = (cos - st_min) / (st_max - st_min + 1e-9)

    # Hybrid: semantic-weighted combination
    hybrid = alpha * st_norm + (1.0 - alpha) * bm25_norm
    top_h = np.argsort(-hybrid)[:k]
    print(f"\nHybrid (BM25 + Semantic) top-k (alpha={alpha}):")
    for i in top_h:
        print(f"  [{i}] {hybrid[i]:.3f}  {docs[i]}")
```

## Run the demo for all queries (default semantic weight alpha=0.8)

```python theme={null}
for q in queries:
    show_results(q, k=3, alpha=0.8)
```

## Discussion and example behavior

* BM25 relies on token overlap and term importance. It may favor documents that share surface words with the query (even if the meaning differs).
* SentenceTransformer returns semantically similar results by embedding meaning, so it better handles synonyms and paraphrases (e.g., mapping "2FA" to "two-factor authentication").
* The hybrid approach blends both signals using `alpha`. Values:
  * `alpha > 0.5` favors semantic matching.
  * `alpha < 0.5` favors BM25.
* Normalizing both score arrays to \[0,1] before combining allows a simple weighted linear blend that is robust to differing score scales. The small epsilon (`1e-9`) prevents division-by-zero for degenerate score distributions.

<Frame>
  <img alt="The image shows a Jupyter notebook interface comparing retrieval results using BM25, Semantic (SentenceTransformer), and a hybrid method for different queries related to HbA1c and sick leave policy. The results include top-k entries for each query with associated scores." />
</Frame>

## Sample (cleaned) output for illustration

```plaintext theme={null}
QUERY: How do I set up 2FA?
============================================================
BM25 top-k:
  [3] 1.487  How to fix engine misfires caused by bad spark plugs.
  [0] 0.000  Enable two-factor authentication (2FA) in your account settings to add an extra security step.
  [5] 0.000  Configure MFA with authenticator apps.

Semantic (SentenceTransformer) top-k:
  [0] 0.689  Enable two-factor authentication (2FA) in your account settings to add an extra security step.
  [5] 0.583  Configure MFA with authenticator apps.
  [3] 0.064  How to fix engine misfires caused by bad spark plugs.

Hybrid (BM25 + Semantic) top-k (alpha=0.8):
  [0] 0.720  Enable two-factor authentication (2FA) in your account settings to add an extra security step.
  [5] 0.670  Configure MFA with authenticator apps.
  [3] 0.574  How to fix engine misfires caused by bad spark plugs.
```

## Tuning guidance

> **lightbulb** Tune `alpha` and experiment with different sentence-transformer models (for example, `all-MiniLM-L6-v2` for speed or `multi-qa-MiniLM-L6-cos-v1` for QA-style retrieval). Use a labeled validation set (queries with known correct docs) to measure precision/recall and choose alpha and model for your dataset. If BM25 returns many identical scores (common in small corpora), the semantic signal typically helps; if semantic matching over-generalizes in your domain, increase BM25 weight.

### Switching the embedding model (example)

```python theme={null}
# Example: use a QA-tuned model
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
doc_emb = model.encode(docs, convert_to_tensor=True, normalize_embeddings=True)

# Re-run show_results with the new embeddings:
for q in queries:
    show_results(q, k=3, alpha=0.8)
```

## Quick comparison

| Method                | Strengths                                                        | When to use                                                     |
| --------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------- |
| BM25                  | Fast, interpretable, strong on exact matches and term importance | Short queries, domain with consistent terminology               |
| Semantic (bi-encoder) | Handles synonyms, paraphrase, and deeper meaning                 | Natural-language queries, varied vocabulary                     |
| Hybrid (weighted)     | Combines both signals, tunable with `alpha`                      | Real-world retrieval where both surface form and meaning matter |

## Final notes

* This demo uses a very small toy corpus for illustration. On larger corpora you'll get more stable BM25 distributions and richer semantic matches.
* Keep the retrieval pipeline configurable: `alpha`, `k`, and `model` selection should be part of your evaluation loop.
* Validate hybrid weighting with representative queries and metrics (e.g., recall\@k, MRR) before deploying to production.

References and further reading:

* [SentenceTransformers documentation](https://www.sbert.net/)
* [rank\_bm25 GitHub repository](https://github.com/dorianbrown/rank_bm25)
* [BM25 overview (Wikipedia)](https://en.wikipedia.org/wiki/Okapi_BM25)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/14bc5c47-4554-4c21-9f00-67c0f7e7f17d/lesson/71e8f0a4-fe13-45d6-a634-c7c10201d3b1)


# Demo From Keyword to Semantic Search

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Semantic-Search-Embeddings/Demo-From-Keyword-to-Semantic-Search/page

Compares keyword lexical search and sentence-transformer semantic search with code examples, illustrating differences, evaluation, and recommending hybrid retrieval with semantic re-ranking for better recall and precision.

This tutorial compares a classic lexical retriever (TF-IDF / BM25 via Whoosh) with a lightweight semantic retriever using Sentence Transformers. The aim is to demonstrate how semantic search can surface conceptually related documents (for example, documents about "motor diagnostics") even when the query uses different wording (for example, "engine troubleshooting").

What you'll learn:

* How to run a simple Whoosh keyword search.
* How to embed text with a Sentence Transformers model and rank by cosine similarity.
* How the two approaches differ in practice and how to compare them side-by-side.

## Prerequisites

Install the required Python packages (run in a notebook or virtual environment):

```bash theme={null}
%pip install whoosh sentence-transformers scikit-learn pandas
```

> **lightbulb** If you plan to run this in a production-like environment, use a dedicated virtual environment and pin package versions to ensure reproducibility.

## Corpus: small, focused, intentionally non-overlapping

We use a tiny corpus of six short documents and titles to make the difference between keyword and semantic retrieval obvious:

```python theme={null}
docs = [
    "A beginner's guide to engine troubleshooting: check fuel lines, spark, and air intake before replacing parts.",
    "Piston wear can cause loss of compression; regular maintenance and proper lubrication extend engine life.",
    "Valve timing issues often masquerade as rough idle—inspect the timing belt and camshaft alignment.",
    "Motor diagnostics for intermittent power loss: scan error codes, inspect sensors, and test the ignition coil.",
    "Understanding airflow: clogged filters, intake leaks, and MAF sensor failures reduce performance.",
    "Basic oil system checks: pressure light warnings, pump failures, and choosing the right viscosity."
]

titles = [
    "Engine Troubleshooting 101",
    "Piston Wear & Compression",
    "Valve Timing Problems",
    "Motor Diagnostics Checklist",
    "Airflow & Intake Issues",
    "Oil System Basics"
]
```

## 1) Keyword search (Whoosh — lexical retrieval)

Build a temporary Whoosh index storing `title` and `content` fields, then run a keyword query. The example query is `"engine troubleshooting"`.

```python theme={null}
import tempfile
