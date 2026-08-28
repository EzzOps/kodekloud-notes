# TF IDF Algorithm

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Keyword-Search-Retrieval/TF-IDF-Algorithm/page

Explains TF-IDF scoring, intuition, formulas, a worked example, document ranking usage, practical considerations and limitations for retrieval systems

In this lesson we explain TF-IDF, a classic document-ranking technique used across search systems and retrieval pipelines. You’ll learn what the acronym means, the core intuition, how to compute the scores, and a short worked example you can compute by hand.

This lesson covers:

* What TF-IDF stands for and the role of each component.
* The core intuition: amplify words that are frequent inside a document and downweight words that appear across many documents.
* How TF-IDF is applied to rank documents for queries.
* A concise worked example with step-by-step calculations.

TF-IDF helps identify which words are informative for each document: common words get low scores, while rare, topic-specific words get high scores.

<Frame>
  <img alt="The image shows an agenda for a presentation on TF-IDF, detailing four main points: its meaning, the core concept, document ranking, and a simple example. It includes numbered bullet points in a vertical list format." />
</Frame>

## Intuition

Before jumping into formulas, consider how you naturally infer a document’s subject. You tend to ignore filler words like "the", "and", or "of" because they appear everywhere and don’t help identify topics. In contrast, specific terms such as "four-stroke", "valve", or "piston" strongly indicate the text is about engines. Those distinctive terms — and their co-occurrence patterns — provide the most informative cues.

<Frame>
  <img alt="The image illustrates the intuition behind TF-IDF using engine-related terms like &#x22;four-stroke,&#x22; &#x22;valve,&#x22; and &#x22;piston,&#x22; highlighting how unique terms serve as clues." />
</Frame>

TF-IDF encodes this intuition mathematically: give higher weight to terms that are frequent in a document but rare across the collection.

<Frame>
  <img alt="The image illustrates the concept of TF-IDF, showing how common words appearing everywhere are transformed into topic words that appear less frequently, with the formula &#x22;Frequency in document × Rarity across collection.&#x22;" />
</Frame>

## Pipeline overview

A typical TF-IDF ranking pipeline:

1. Receive the query terms.
2. Tokenize the query and each document into terms.
3. Count term occurrences per document and compute Term Frequency (TF).
4. Compute Inverse Document Frequency (IDF) from how many documents contain each term.
5. Multiply TF × IDF to obtain per-term weights.
6. Sum the TF-IDF weights for the query terms in each document to produce a relevance score.
7. Rank documents by that relevance score (highest first).

Use TF-IDF as a fast first-pass filter in multi-stage retrieval systems: it’s inexpensive, interpretable, and often effective when vocabulary is distinctive.

## Term Frequency (TF)

Term Frequency measures how prominent a term is within a single document. Variants include:

| Variant              | Description                  | Formula / Example                                |
| -------------------- | ---------------------------- | ------------------------------------------------ |
| Raw count            | Simple number of occurrences | `f(t, d)`                                        |
| Normalized frequency | Accounts for document length | `TF(t, d) = f(t, d) / sum_k f(k, d)`             |
| Log-scaled           | Dampens large counts         | `TF(t, d) = 1 + log(f(t, d))` (for `f(t,d) > 0`) |

A common normalized TF formula:

```text theme={null}
TF(t, d) = (term count in d) / (total terms in d)
```

TF measures how "loud" a term is within a document: repeated terms are often more important for that document.

## Inverse Document Frequency (IDF)

IDF measures how rare or common a term is across the whole collection. If a term appears in many documents, it is less useful for distinguishing them.

Common IDF variants:

| Variant           | Formula                           | Notes                                                    |
| ----------------- | --------------------------------- | -------------------------------------------------------- |
| Basic natural log | `IDF(t) = ln(N / df_t)`           | `N` = total documents, `df_t` = documents containing `t` |
| Smoothed          | `IDF(t) = ln(1 + N / (1 + df_t))` | Prevents division by zero and reduces extremes           |

Example:

```text theme={null}
IDF(t) = ln(N / df_t)
```

If `df_t` is large (term appears everywhere), IDF is small. If `df_t` is small (term is rare), IDF is large. In production pipelines you usually remove very common stop words before scoring to avoid distorted IDF on small collections.

<Frame>
  <img alt="The image illustrates the concept of Inverse Document Frequency (IDF), showing multiple documents containing the term &#x22;Piston&#x22; and indicating that if many documents contain a term, it results in a small IDF value." />
</Frame>

## Combining TF and IDF

TF-IDF multiplies the two signals so that high scores require both within-document prominence and cross-document rarity:

```text theme={null}
TF-IDF(t, d) = TF(t, d) × IDF(t)
```

High TF-IDF means a term is frequent in the document yet uncommon across the library — a strong indicator of that document’s topic.

<Frame>
  <img alt="The image illustrates the concept of Inverse Document Frequency (IDF), showing several documents with the word &#x22;Piston&#x22; and highlighting that a large IDF value is associated with terms appearing in fewer documents." />
</Frame>

## Worked example (step-by-step)

Three short documents:

* Doc A: piston, piston, valve
* Doc B: valve, valve, engine
* Doc C: engine, piston, the

The table below (image) summarizes the term counts:

<Frame>
  <img alt="The image illustrates a simple example of term frequency in documents, showing word occurrences for &#x22;Piston,&#x22; &#x22;Valve,&#x22; &#x22;Engine,&#x22; and &#x22;The&#x22; across three documents (Doc A, Doc B, Doc C) in a table format." />
</Frame>

From the counts:

* Vocabulary: `piston`, `valve`, `engine`, `the`
* Document frequencies (df):
  * `piston` appears in Doc A and Doc C → `df_piston = 2`
  * `valve` appears in Doc A and Doc B → `df_valve = 2`
  * `engine` appears in Doc B and Doc C → `df_engine = 2`
  * `the` appears only in Doc C → `df_the = 1`
* Total documents: `N = 3`

Using normalized TF and natural-log IDF:

```text theme={null}
TF(t, d) = count(t, d) / total_terms_in_d
IDF(t) = ln(N / df_t)
```

Calculate IDF values:

```text theme={null}
IDF(piston) = ln(3 / 2) ≈ 0.405465
IDF(valve)  = ln(3 / 2) ≈ 0.405465
IDF(engine) = ln(3 / 2) ≈ 0.405465
IDF(the)    = ln(3 / 1) ≈ 1.098612
```

Calculate TF and TF-IDF for each term (key entries shown):

* piston
  * Doc A: TF = 2/3 ≈ 0.6667 → TF-IDF ≈ 0.6667 × 0.4055 ≈ 0.2703
  * Doc B: TF = 0           → TF-IDF = 0
  * Doc C: TF = 1/3 ≈ 0.3333 → TF-IDF ≈ 0.3333 × 0.4055 ≈ 0.1352

* valve
  * Doc A: TF = 1/3 ≈ 0.3333 → TF-IDF ≈ 0.1352
  * Doc B: TF = 2/3 ≈ 0.6667 → TF-IDF ≈ 0.2703
  * Doc C: TF = 0           → TF-IDF = 0

* engine
  * Doc A: TF = 0           → TF-IDF = 0
  * Doc B: TF = 1/3 ≈ 0.3333 → TF-IDF ≈ 0.1352
  * Doc C: TF = 1/3 ≈ 0.3333 → TF-IDF ≈ 0.1352

* the
  * Doc C: TF = 1/3 ≈ 0.3333 → TF-IDF ≈ 0.3333 × 1.0986 ≈ 0.3662

Note that in this tiny collection the word "the" appears only in Doc C, giving it a high IDF. In large, real-world corpora `the` appears in nearly every document and its IDF would be near zero; search pipelines typically remove common stop words before computing scores.

## Query-dependent ranking

TF-IDF scores are computed per query term and summed to create a document score. For single-term queries:

* Query "piston": Doc A (0.2703) > Doc C (0.1352) > Doc B (0). Doc A ranks highest.
* Query "valve": Doc B (0.2703) > Doc A (0.1352) > Doc C (0). Doc B ranks highest.
* Query "engine": Doc B and Doc C tie (both ≈ 0.1352) and would be co-ranked unless tie-breaking rules apply.

Key point: the same document collection is re-ranked depending on the query because TF-IDF weights are query-specific.

## Where TF-IDF is used

TF-IDF remains useful across many scenarios:

* Classic search engines (historically a backbone of ranking).
* Automatic keyword extraction and tagging.
* Fast baselines for relevance: quick, interpretable signals that require no training.
* Document deduplication and near-duplicate detection via TF-IDF vectors and similarity measures (e.g., cosine similarity).
* Content analysis to surface themes and important terms across large corpora.

<Callout icon="lightbulb">
  TF-IDF is fast, transparent, and requires no labeled training data. It’s especially effective when documents use distinctive vocabulary (for example, technical or legal texts) and when you need an interpretable baseline.
</Callout>

<Callout icon="warning">
  Limitations: TF-IDF has no semantic understanding (synonyms are distinct), ignores word order and context (bag-of-words), and is sensitive to corpus size and stop-word handling. Combine TF-IDF with embeddings or re-rankers when you need semantic relevance.
</Callout>

## Limitations (expanded)

* No semantic similarity: synonyms and related concepts (e.g., "car" vs "automobile") are treated as different tokens.
* Bag-of-words: ignores order and phrase structure (e.g., "dog bites man" ≠ "man bites dog").
* Static and not adaptive: TF-IDF does not learn from user feedback unless combined with behavioral signals.
* Corpus sensitivity: small collections can give misleading IDF values for a few words.
* Stop-word handling: must filter or treat common words carefully to avoid noisy signals.

Modern retrieval systems often use TF-IDF as a fast first stage, followed by semantic methods (word embeddings, dense retrieval) and supervised re-rankers to capture deeper meaning and user intent.

## References and further reading

* [TF-IDF — Wikipedia](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
* [Khan Academy — Term Frequency–Inverse Document Frequency](https://www.khanacademy.org) (introductory resources)
* [Scikit-learn — Feature extraction text](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting) — practical implementation notes

For practical implementations, consider libraries that compute TF-IDF vectors and support normalization and stop-word filtering (e.g., scikit-learn, Gensim, Apache Lucene).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/316bc17d-74b4-4bc8-bac7-62286dc8eee8/lesson/14c13360-8479-478b-a884-a2fd10c55afc" />
</CardGroup>
