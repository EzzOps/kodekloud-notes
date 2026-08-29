# BM25 Algorithm

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Keyword-Search-Retrieval/BM25-Algorithm/page

Explains the BM25 ranking function, why it improves on TF and TF-IDF by applying term saturation and length normalization for fairer document relevance

In this lesson we explain the BM25 ranking function, why it was developed, and how it improves on simple term-frequency (TF) and TF-IDF approaches.

Example scenario: suppose the query is `valve`. Doc A contains the word `valve` 50 times — does that automatically make Doc A the most relevant result? Not necessarily. Document length and term density both matter.

Document lengths and occurrences:

| Document | Length (words) | `valve` occurrences | Density (occurrences / length) |
| -------- | -------------- | ------------------: | -----------------------------: |
| Doc A    | 1,100          |                  50 |                          0.045 |
| Doc B    | 20             |                   2 |                           0.20 |
| Doc C    | 18             |                   0 |                           0.00 |

If you use a naive term-frequency ranking, Doc A (50 occurrences) would rank highest. But when you consider density, Doc B is actually more focused on the query term despite having far fewer absolute mentions.

<Frame>
  <img alt="The image illustrates the problem of length bias in TF-IDF by comparing three documents, showing differences in length (characters), keyword count, and keyword density. Doc A is longer with more keywords, while Docs B and C are shorter with varying densities." />
</Frame>

TF-IDF and simple term-frequency approaches can therefore be biased toward long documents or pages that repeat a term many times. This creates two problems: (1) long documents gain an unfair advantage simply by size, and (2) malicious actors can exploit this with "keyword stuffing" to manipulate rankings.

<Callout icon="warning">
  Keyword stuffing — repeating a keyword excessively to inflate relevance — can cause TF-IDF-based systems to return spammy or low-quality results. Modern ranking functions like BM25 were designed to reduce that risk.
</Callout>

<Frame>
  <img alt="The image outlines the problem of length bias in TF-IDF, emphasizing how it favors long or repetitive documents, allows repeated terms to dominate, and enabled early SEO keyword stuffing." />
</Frame>

BM25 was developed to address these issues. It introduces two key behaviors:

* Diminishing returns for repeated occurrences of the same term (saturation).
* Length normalization so shorter, more focused documents can compete against longer ones.

<Frame>
  <img alt="The image introduces BM25 as a better alternative to TF-IDF, highlighting issues with longer documents and keyword stuffing using an example document containing repetitive terms." />
</Frame>

What is BM25?

BM25 (Best Match 25) is a probabilistic retrieval function used widely in information retrieval systems and search engines. Its core ideas:

* It counts how often a query term appears in a document (`term frequency`), but applies a saturation function so each additional occurrence contributes less.
* It normalizes scores by document length so long documents do not automatically win.
* It multiplies by an inverse document frequency (`IDF`) term to give more weight to rare terms across the corpus.

<Frame>
  <img alt="The image outlines the BM25 (Best Match 25) text retrieval ranking function, highlighting its features: counting word frequency, boost rising then tapering, and preventing long documents from having an unfair advantage." />
</Frame>

Intuition with another example: searching for "racing cars". Under TF-IDF a long document that repeats "racing cars" many times might outrank a concise, authoritative article that contains the phrase fewer times but in a more focused way. BM25 increases the long document's score for initial occurrences, then tapers additional gain; a shorter, concentrated document can therefore rank higher.

<Frame>
  <img alt="The image illustrates a comparison between two documents using the BM25 algorithm related to the query &#x22;racing cars.&#x22; It highlights how BM25 handles word occurrence frequency, allowing shorter, focused documents to compete by preventing repetitive words from dominating." />
</Frame>

Now, the BM25 formula and its parts. The formula is often written as:

```text theme={null}
score = IDF * ( (f * (k1 + 1)) / (f + k1 * (1 - b + b * (L / AVGL))) )
```

Parameter definitions:

* `f` — term frequency in the document (how many times the query term appears).
* `L` — document length (typically number of words).
* `AVGL` — average document length across the collection.
* `k1` — term frequency saturation parameter (commonly 1.2–2.0). Larger `k1` reduces saturation (gives more weight to additional occurrences).
* `b` — length normalization parameter in \[0, 1]; `b = 0` disables length normalization, `b = 1` enables full normalization (common default \~0.75).
* `IDF` — inverse document frequency that boosts rare terms and downweights common terms.

<Frame>
  <img alt="The image shows the BM25 formula used for information retrieval, involving parameters like IDF, term frequency ( f ), and document length normalization." />
</Frame>

Tuning tips:

<Callout icon="lightbulb">
  * Use `k1` to control how quickly additional term occurrences saturate; increase `k1` if repeated terms should count more.
  * Use `b` to control how much length affects scores; lower `b` if document length should matter less.
  * Defaults (`k1 ≈ 1.2–1.5`, `b ≈ 0.75`) work well for many text collections, but always validate on your dataset.
</Callout>

Workflow summary — how BM25 scores are computed:

1. Compute term frequency `f` for each query term in each document.
2. Normalize `f` by document length using `L`, `AVGL`, and `b`.
3. Apply saturation using `k1` so the contribution from `f` levels off.
4. Multiply by `IDF` to emphasize rare, informative terms.

This combination yields fairer rankings: concise, high-quality documents that are focused on the query can outrank much longer documents that merely repeat terms. For these reasons BM25 is a foundational ranking function used in search engines (e.g., Lucene/Elasticsearch) and many information retrieval systems.

Links and references:

* [BM25 (Wikipedia)](https://en.wikipedia.org/wiki/Okapi_BM25)
* [Elasticsearch relevance documentation](https://www.elastic.[AWS_SECRET_ACCESS_KEY]scoring.html)
* Robertson, S., Walker, S. — “Okapi at TREC” (original BM25 research)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/316bc17d-74b4-4bc8-bac7-62286dc8eee8/lesson/b04656aa-f6c3-404b-b8b8-1edaca8bd6dc" />
</CardGroup>
