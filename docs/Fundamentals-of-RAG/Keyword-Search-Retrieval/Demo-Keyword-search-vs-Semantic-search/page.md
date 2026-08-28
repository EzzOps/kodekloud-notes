# Demo Keyword search vs Semantic search

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Keyword-Search-Retrieval/Demo-Keyword-search-vs-Semantic-search/page

Demonstrates and compares TF-IDF keyword search with semantic embeddings for document retrieval using Whoosh and SentenceTransformers, highlighting differences and tradeoffs.

In this lesson we demonstrate two common document retrieval approaches using a small automotive troubleshooting corpus:

* Keyword search (TF-IDF) with Whoosh
* Semantic retrieval using SentenceTransformers + cosine similarity

We'll build a tiny corpus, run both methods on the same query, and compare the ranked results side-by-side so you can see how exact-match ranking (TF-IDF) and meaning-based retrieval (embeddings) differ.

Keywords: TF-IDF, semantic search, embeddings, Whoosh, SentenceTransformers, cosine similarity

Prerequisites (run once):

```bash theme={null}
pip install whoosh sentence-transformers scikit-learn pandas
```

Corpus and titles used in this lesson:

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

<Callout icon="lightbulb">
  SentenceTransformers will download model weights on first use. If you're running this in a restricted environment, pre-download models or set `SENTENCE_TRANSFORMERS_HOME` to a writable cache folder. For larger corpora consider batching embeddings to avoid memory spikes.
</Callout>

## 1) Keyword search with Whoosh (TF-IDF)

Whoosh is a pure-Python search library that indexes documents and computes TF-IDF style relevance under the hood. The example below creates a temporary Whoosh index, adds our documents, and runs a simple keyword query. Whoosh matches query terms and ranks results by term frequency / inverse document frequency.

```python theme={null}
