# Demo BM25 vs Semantic Search

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Semantic-Search-Embeddings/Demo-BM25-vs-Semantic-Search/page

Demonstration comparing BM25 token matching with sentence-transformer semantic retrieval and a weighted hybrid ranker, with runnable Jupyter notebook, code, and tuning guidance.

In this lesson we compare classic BM25 retrieval with true semantic search (using sentence-transformers), then build a simple hybrid ranker that blends both signals. This example is compact, corrected, and runnable in a Jupyter-friendly notebook.

BM25 is a token-statistics method that excels at matching exact terms and weighting important tokens, but it can miss synonyms, paraphrases, and deeper meaning. A bi-encoder (sentence-transformers) maps queries and documents to vectors and uses cosine similarity to retrieve semantically similar items. A hybrid approach combines both strengths and often yields more robust retrieval for real applications.

Quick links:

* SentenceTransformers: [https://www.sbert.net/](https://www.sbert.net/)
* rank\_bm25: [https://github.com/dorianbrown/rank\_bm25](https://github.com/dorianbrown/rank_bm25)

## Installation

Install the required Python packages (Jupyter-friendly):

```bash theme={null}
!pip install -q sentence-transformers rank-bm25 scikit-learn numpy
```

## Overview: how the demo works

1. Prepare a small document corpus and example queries.
2. Tokenize documents for BM25 and initialize the BM25 index.
3. Encode documents with a sentence-transformer to produce normalized embeddings.
4. For each query:
   * Get BM25 scores (token overlap / importance).
   * Get semantic scores (cosine similarity with embeddings).
   * Normalize both score vectors to \[0,1] and combine them with a weighted linear blend: hybrid = alpha \* semantic + (1-alpha) \* bm25.
5. Compare the top-k results for BM25, semantic, and hybrid.

## Corpus, queries, and imports

```python theme={null}
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util
import numpy as np

docs = [
    "Enable two-factor authentication (2FA) in your account settings to add an extra security step.",
    "HbA1c measures long-term glucose; talk to your physician about tests for glycated hemoglobin.",
    "Our PTO policy covers paid time off for vacations and sick leave.",
    "How to fix engine misfires caused by bad spark plugs.",
    "Kubernetes Ingress configuration for path-based routing.",
    "Configure MFA with authenticator apps.",
    "Doctor appointment scheduling policy."
]

queries = ["How do I set up 2FA?", "What does HbA1c mean?", "sick leave policy?"]
```

## Prepare BM25 and SentenceTransformer embeddings

```python theme={null}
