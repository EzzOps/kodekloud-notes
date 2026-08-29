# Whoosh imports
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

# Create temp index
index_dir = tempfile.mkdtemp()
schema = Schema(title=ID(stored=True), content=TEXT(stored=True))
ix = index.create_in(index_dir, schema)

# Add documents
writer = ix.writer()
for t, d in zip(titles, docs):
    writer.add_document(title=t, content=d)
writer.commit()

# Run a keyword query (lexical retrieval)
query_text = "engine troubleshooting"

with ix.searcher() as searcher:
    parser = QueryParser("content", ix.schema)
    q = parser.parse(query_text)
    results = searcher.search(q, limit=10)
    kw_hits = [(r['title'], float(r.score)) for r in results]

# (Optional) cleanup the temporary index directory when done:
# import shutil
kw_hits
```

Example lexical output:

```plaintext theme={null}
[('Engine Troubleshooting 101', 3.688410483089193)]
```

Explanation: The lexical retriever returns the exact-match document containing the words "engine troubleshooting". Documents that convey the same concept but use different words (for example, "motor diagnostics") do not appear because they lack lexical overlap with the query.

## 2) Semantic retrieval (Sentence Transformers + cosine similarity)

Embed the documents and the query using a Sentence Transformers model (`all-MiniLM-L6-v2`), then rank documents by cosine similarity.

```python theme={null}
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a small, fast sentence-transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Embed documents and the query
doc_embeddings = model.encode(docs, normalize_embeddings=True)
query_embedding = model.encode([query_text], normalize_embeddings=True)

# Cosine similarity scores
sims = cosine_similarity(query_embedding, doc_embeddings).flatten()

# Rank by semantic similarity (descending)
sem_hits_idx = np.argsort(-sims)
sem_hits = [(titles[i], float(sims[i])) for i in sem_hits_idx]

# Show top 5 semantic hits
sem_hits[:5]
```

Example semantic-ranking output:

```plaintext theme={null}
[('Engine Troubleshooting 101', 0.6778184771537781),
 ('Valve Timing Problems', 0.4548088024031136),
 ('Motor Diagnostics Checklist', 0.4505075285693745),
 ('Oil System Basics', 0.32172026519309644),
 ('Piston Wear & Compression', 0.23938072054235867)]
```

Explanation: Semantic search returns several related documents beyond the exact lexical match. Because embeddings capture conceptual similarity, "Motor Diagnostics Checklist" and "Valve Timing Problems" appear as relevant even though they do not share exact wording with the query.

## 3) Side-by-side comparison (TF-IDF vs Semantic)

Normalize the results into DataFrames and merge them to compare ranks and scores across both methods. The Whoosh/lexical search may return only exact matches, while the semantic search gives a ranked list for all documents.

```python theme={null}
import pandas as pd

# Normalize/pretty print both lists with rank
kw_df = pd.DataFrame(kw_hits, columns=["Title", "TFIDF_Score"])
kw_df["KW_Rank"] = range(1, len(kw_df) + 1)

sem_df = pd.DataFrame(sem_hits, columns=["Title", "CosineSim"])
sem_df["SEM_Rank"] = range(1, len(sem_df) + 1)

# Merge on title to show both ranks together
comparison = pd.merge(sem_df, kw_df, on="Title", how="outer")

# Sort by semantic rank to highlight the "meaning" ordering
comparison_sorted = comparison.sort_values(by="SEM_Rank", na_position="last")

comparison_sorted[["Title", "SEM_Rank", "CosineSim", "KW_Rank", "TFIDF_Score"]]
```

Example merged result (conceptual):

```plaintext theme={null}
Title                        SEM_Rank  CosineSim    KW_Rank  TFIDF_Score
Engine Troubleshooting 101   1         0.677818     1        3.688410
Valve Timing Problems        2         0.454809     NaN      NaN
Motor Diagnostics Checklist  3         0.450508     NaN      NaN
Oil System Basics            4         0.321720     NaN      NaN
Piston Wear & Compression    5         0.239381     NaN      NaN
Airflow & Intake Issues      6         0.087xxx     NaN      NaN
```

The NaNs indicate documents not returned by the lexical keyword search.

> **lightbulb** Practical pattern: use a hybrid pipeline. First retrieve a broad candidate set quickly (lexical methods like TF-IDF/BM25 or a fast ANN index), then re-rank that subset with a semantic model for better precision. This balances speed, recall, and semantic coverage.

## Quick comparison: Lexical vs Semantic vs Hybrid

| Retriever Type                                       | Strengths                                                | Typical Use Case                                                                  |
| ---------------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Lexical (TF-IDF / BM25, e.g., Whoosh)                | Fast, interpretable, exact match ranking                 | Keyword-based search UIs, faceted search, queries where exact terms matter        |
| Semantic (Sentence Transformers + cosine similarity) | Finds conceptually related content, robust to paraphrase | QA reranking, semantic discovery, content recommendation                          |
| Hybrid (lexical retrieval -> semantic re-rank)       | High recall + high precision, scalable                   | Large-scale production search pipelines, conversational agents, enterprise search |

## Tips for experimentation and scaling

* Try larger Sentence Transformers models for improved semantic quality at the cost of latency.
* For bigger corpora, use an approximate nearest neighbor (ANN) index (e.g., FAISS, Annoy, HNSW) to retrieve candidate embeddings efficiently.
* Consider normalization strategies (L2-normalization vs. no normalization) depending on your similarity metric and model outputs.
* When using Whoosh in production, evaluate BM25 configuration and tokenization for your domain language.

## Summary

* Lexical retrievers like Whoosh excel at exact lexical matches and are low-latency and interpretable.
* Semantic retrieval using sentence embeddings recovers conceptually related documents even with different surface wording.
* A hybrid system (lexical retrieval for recall + semantic re-ranking for precision) is a practical production pattern that often yields the best results.

## Links and References

* [Whoosh documentation](https://whoosh.readthedocs.io/en/latest/)
* [Sentence Transformers (SBERT)](https://www.sbert.net/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (reference for general systems design patterns)
* [FAISS (Facebook AI Similarity Search)](https://github.com/facebookresearch/faiss) — for scalable nearest-neighbor search

You can reuse the notebook snippets above to experiment with different models, retrieval thresholds, or corpora to see how lexical and semantic methods compare in your domain.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/14bc5c47-4554-4c21-9f00-67c0f7e7f17d/lesson/2df569cd-a18f-4e0a-b62c-794bae693a39)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/14bc5c47-4554-4c21-9f00-67c0f7e7f17d/lesson/ae3b17c7-d0e5-4db5-a6d9-de8745b1ada8)


# Limitations of Keyword Search

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Semantic-Search-Embeddings/Limitations-of-Keyword-Search/page

Explains keyword search limitations and how semantic retrieval and hybrid RAG improve recall, disambiguation, passage retrieval, and robustness to synonyms, typos, and long documents.

In this lesson we explain the limits of keyword search and why Retrieval‑Augmented Generation (RAG) benefits from semantic retrieval. You’ll learn how keyword search works, four common failure modes, how semantic retrieval addresses them, and a practical checklist for building a robust RAG pipeline.

> **lightbulb** Keyword search remains useful and widely used — this lesson explains where it excels and where semantic retrieval is necessary.

## How keyword search works

At a high level, keyword search answers questions like “Which documents mention ‘engine’?” or “Which documents contain both ‘engine’ and ‘piston’?” Naively scanning every document at query time is slow, so search engines precompute a data structure called an inverted index.

An inverted index maps each token (term) to the list of documents that contain it. At query time the engine looks up each query term and intersects those document lists to produce matches quickly — this precomputation is the performance secret behind keyword search.

<Frame>
  <img alt="The image explains how keyword search works using an inverted index, showing a mapping between words (camshaft, piston, valve, engine) and associated documents (Document 1, 2, 3)." />
</Frame>

Because the inverted index is term → document, exact token overlap is the strongest signal for retrieval. Lightweight preprocessing (tokenization, stemming, stop‑word removal) is applied to normalize queries and documents.

<Frame>
  <img alt="The image illustrates how keyword search works using an inverted index, linking words like &#x22;camshaft&#x22; and &#x22;engine&#x22; to corresponding documents." />
</Frame>

Historically, even major search engines like Google started from this inverted‑index model rather than neural ranking. The inverted index remains a core building block for fast retrieval.

<Frame>
  <img alt="The image explains how keyword search works, showing a Google logo with three options below: &#x22;Neural networks,&#x22; &#x22;Artificial intelligence,&#x22; and &#x22;Inverted index,&#x22; where only &#x22;Inverted index&#x22; is marked as correct." />
</Frame>

## Ranking: which matches should appear first?

When many documents match a query (e.g., "piston valve timing"), ranking determines the order. Ranking combines signals like exact matches, near-exact matches, term frequency, and document frequency.

* Exact match: query tokens appear verbatim (high weight).
* Near-exact match: variations produced by stemming, pluralization, or synonym expansion.
* Partial match: documents containing only a subset of query terms (lower weight).

Example: for the query “intake valve”, a document titled “Intake Valve Design” is an exact match. Documents like “Valve Timing System” are related but score lower unless synonyms or phrase matches are used.

<Frame>
  <img alt="The image illustrates the concept of exact match search, showing a query for &#x22;Intake Valve&#x22; and highlighting &#x22;Document 1&#x22; as a relevant match with &#x22;Intake Valve Design.&#x22;" />
</Frame>

Systems can surface near-exact and partial matches via configurables like synonym maps and fuzzy matching; they are typically scored lower than exact matches.

<Frame>
  <img alt="The image illustrates a user interface for &#x22;Visualizing Match Types – Near-Exact Match,&#x22; showing search results for &#x22;Intake Valve&#x22; with documents related to &#x22;Valve Timing System&#x22; and &#x22;Engine Pistons and Valves.&#x22;" />
</Frame>

## Scoring: TF, IDF, TF‑IDF, and BM25

Common lexical scoring components:

* Term Frequency (TF): how often a term appears in a document.
* Inverse Document Frequency (IDF): downweights terms that appear in many documents.
* TF‑IDF: multiplies TF by IDF to favor documents where a term is frequent but not ubiquitous.
* BM25: improves TF‑IDF by applying a saturation function to TF and normalizing for document length, reducing reward for keyword stuffing.

<Frame>
  <img alt="The image illustrates TF-IDF weighting for the term &#x22;piston&#x22; across three documents, indicating high, low, and medium term frequencies with 10, 2, and 5 mentions respectively." />
</Frame>

TF‑IDF can favor long documents because they have more tokens, while BM25 compensates with length normalization and a saturation curve so that additional occurrences contribute diminishing returns.

<Frame>
  <img alt="The image presents a comparison of two types of documents discussed by BM25: a very long document mentioning &#x22;piston&#x22; 12 times among many topics, and a short document mentioning &#x22;piston&#x22; twice but focusing solely on pistons." />
</Frame>

A typical shape comparison shows TF‑IDF scores growing roughly linearly with term occurrences, while BM25 flattens after a point due to saturation.

<Frame>
  <img alt="The image is a line graph comparing TF-IDF and BM25 scores against term occurrence, illustrating the saturation effect. TF-IDF increases steeply, while BM25 and term occurrence grow more moderately." />
</Frame>

These components — inverted indexes, TF‑IDF/BM25 scoring, and ranking heuristics — form the backbone of modern keyword retrieval.

<Frame>
  <img alt="The image displays the title &#x22;The Invisible Librarian at Work&#x22; and a labeled section about &#x22;Organization,&#x22; describing the process of building inverted indexes that map every word to its documents." />
</Frame>

## Four failure modes of keyword search

Even with BM25 and query expansion, keyword search fails in predictable ways. Below are four common failure modes and how semantic retrieval (dense embeddings + re-ranking) addresses them.

| Failure Mode                                     | Why it fails                                                                                                   | How semantic retrieval helps                                                                        |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Lexical mismatch (synonyms, acronyms)            | Tokens differ (e.g., `2FA`, `two-factor authentication`, `MFA`) — low recall unless you add synonyms manually. | Embeddings capture semantic equivalence; hybrid search + synonym maps improves recall.              |
| Polysemy & context blindness                     | Bag-of-words ignores context (e.g., “Jaguar speed” could be animal or car).                                    | Contextual embeddings encode surrounding words, enabling disambiguation and better re-ranking.      |
| Long documents & passage granularity             | Answer may be a paragraph inside a long PDF; document-level scoring buries passages.                           | Chunk/passage-level embeddings and retrieval return focused passages for the LLM to consume.        |
| Noisy language (typos, variants, cross‑language) | Typos, spelling variants, or cross-language queries create OOV tokens and tokenization issues.                 | Multilingual/tolerant embeddings, fuzzy matching, and better tokenization reduce noise sensitivity. |

1. Lexical mismatch (synonyms, acronyms)
   * Example: `2FA`, `two-factor authentication`, and `MFA` are lexically different but equivalent. Keyword search needs synonym maps or query expansion to achieve good recall.
   * Query expansion can help, but it requires manual curation or domain rules.

<Frame>
  <img alt="The image presents a topic, &#x22;Failure #1: Lexical Mismatch,&#x22; with reasons why keywords struggle, such as &#x22;No overlap, low recall&#x22; and &#x22;Synonyms must be added manually.&#x22;" />
</Frame>

2. Polysemy and context blindness
   * Example: “Jaguar speed” could refer to the animal or the car; “Java memory model” could mean the programming language or the island. Bag‑of‑words lacks context to disambiguate.
   * Mitigations: phrase queries, field boosts, or manual disambiguation. RAG uses contextual embeddings that encode neighboring words, improving disambiguation and enabling semantic matches (e.g., mapping `2FA` to `two-factor authentication` within context).

<Frame>
  <img alt="The image explains polysemy and context blindness in search, highlighting challenges with keyword searches and how RAG (Retrieval-Augmented Generation) addresses these issues with context and re-ranking." />
</Frame>

> **lightbulb** Note: very short or ambiguous queries remain challenging even for semantic systems — adding context, session history, or query expansion often helps.

3. Long documents and passage granularity
   * The relevant answer may be a short passage inside a long document. Document-level indexing treats the whole file as one item and can bury the passage.
   * Best practice: chunk documents into passages and index passages as first-class retrieval units. RAG systems commonly use passage-level embeddings so the LLM receives concise, relevant content.

4. Noisy language (typos, variants, cross-language)
   * Typos (e.g., “ingress” vs “inrgess”), spelling variants (licence vs license), or a query in a different language create tokenization and OOV problems.
   * Use multilingual or fuzzily tolerant embeddings, improve tokenization, and normalize text to reduce noise impact.

<Frame>
  <img alt="The image explains &#x22;Failure #4: Noisy Language,&#x22; detailing why keywords struggle with OOV words, small fuzzy distance, and language-specific tokenization, and how RAG addresses these with language-specific tokenization and cross-language semantic matching." />
</Frame>

## Implementation checklist for RAG

When combining keyword and semantic retrieval, follow this practical checklist:

* Use hybrid retrieval (BM25 + dense vectors) to combine precise keyword matching with semantic recall.
* Optimize chunking: common chunk sizes are 300–600 tokens with 10–20% overlap; tune based on document type.
* Select embeddings that match your domain and language requirements (domain‑specific or multilingual models).
* Apply cross‑encoder re‑ranking: re-rank the top‑K hits from BM25 + dense retrieval with a cross‑encoder for higher precision.
* Use query expansion techniques such as hypothetical document embeddings or curated synonym maps for very short or ambiguous queries.
* Maintain data hygiene: dedupe, strip boilerplate/navigation, normalize text, and correct common spelling errors.
* Maintain synonym/acronym maps for known domain equivalences (e.g., `2FA` ↔ `two-factor authentication`).
* Evaluate with realistic test sets and metrics: recall\@K, MRR, and “answer found in top K.”

Hybrid search preserves the speed and determinism of inverted indexes while extending recall with embeddings and re‑ranking.

> **lightbulb** Hybrid search preserves the speed and precision of keyword methods while extending recall and semantic matching through embeddings.

## When to keep using keyword search

Keyword search is still the right tool for many cases:

* Exact lookups: IDs, SKUs, and log lines.
* Compliance and audit workflows where deterministic operator semantics (AND/OR/NOT) matter.
* Power users familiar with precise query syntax and domain jargon.
* Very large-scale, low-latency lookups that depend on inverted indexes for performance.

Keyword search is fast, well-understood, and robust — RAG augments it rather than fully replacing it.

***

This lesson summarized how keyword search works, common limitations that motivate semantic retrieval, and practical steps to combine lexical and dense retrieval effectively in RAG systems.

## Links and references

* [TF‑IDF — Wikipedia](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
* [BM25 — Information Retrieval Background](https://en.wikipedia.org/wiki/Okapi_BM25)
* [Retrieval‑Augmented Generation (RAG) — Paper / Overview](https://arxiv.org/abs/2005.11401)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) (example external reference)

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/14bc5c47-4554-4c21-9f00-67c0f7e7f17d/lesson/df507583-d236-4998-8b2f-da38915d819f)
