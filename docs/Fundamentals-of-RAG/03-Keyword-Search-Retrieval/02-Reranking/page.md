# Reranking

Source: https://notes.kodekloud.com/docs/Fundamentals-of-RAG/Keyword-Search-Retrieval/Reranking/page

Explains reranking in retrieval pipelines, using stronger models to reorder retrieved candidates for improved relevance and final answer quality.

Reranking is a refinement step in modern retrieval pipelines (often part of Retrieval-Augmented Generation, or RAG) that re-orders candidate documents returned by a first-stage retriever to improve final relevance and answer quality. It sits between a fast retrieval stage (vector DB / bi-encoder / BM25) and a final answer generator (LLM or downstream application), using a stronger contextual model (cross-encoder or LLM) to score each candidate against the query.

<Frame>
  <img alt="The image is a flowchart explaining the concept of a &#x22;Reranker,&#x22; involving a user interacting with an application, vector database, LLM context scoring, and the reranker process." />
</Frame>

How reranking fits into the search process

1. A user submits a query to an application.
2. The application encodes the query and queries a vector database or first-stage retriever.
3. The retriever returns the top K candidate documents or passages (fast, high-recall).
4. A reranker evaluates the top K candidates using richer contextual information and assigns relevance scores.
5. The pipeline selects the top N reranked items (N ≤ K) for final answer generation or display.

> **lightbulb** Rerankers are most effective when the initial retrieval stage achieves good recall but struggles with precision or contextual disambiguation. They trade a small amount of latency for noticeably higher final-answer quality.

Why reranking is necessary

* Vector similarity (e.g., bi-encoders) surfaces semantically similar items but can return items that match on keywords, entities, or topics without capturing full contextual intent.
* A reranker uses joint query-document context (via a cross-encoder or LLM) to reason over subtle signals and reorder candidates by true relevance.
* This reduces noise and ensures the final LLM or application consumes higher-quality evidence for generation or decisioning.

Example: finding a Jim Carrey movie
Suppose the user asks: "What is the Jim Carrey movie where he and his best friend go on a road trip to Aspen?"

<Frame>
  <img alt="The image shows a UI panel titled &#x22;Reranker in Action&#x22; with a question about a Jim Carrey movie, entered into an application interface." />
</Frame>

At the vector-retrieval stage, the DB may return a list of Jim Carrey movies that are semantically nearby but not equally relevant: Ace Ventura: Pet Detective, Sonic the Hedgehog, Dumb and Dumber, Bruce Almighty. These candidates are plausible because they share actors, locations, or certain scenes, but the vector stage alone doesn't resolve which movie precisely matches "best friend + road trip + Aspen."

<Frame>
  <img alt="The image illustrates the concept of a &#x22;Reranker in Action,&#x22; showing a vector database connected to a list of movies: &#x22;Ace Ventura: Pet Detective,&#x22; &#x22;Sonic the Hedgehog,&#x22; &#x22;Dumb and Dumber,&#x22; and &#x22;Bruce Almighty.&#x22;" />
</Frame>

A reranker evaluates each candidate jointly with the query (e.g., via a cross-encoder or an LLM scoring prompt) and assigns a relevance score. Because it can combine signals — Jim Carrey + best friend + road trip + Aspen — the reranker correctly ranks "Dumb and Dumber" highest.

<Frame>
  <img alt="The image shows a diagram labeled &#x22;Reranker in Action&#x22; with a &#x22;Reranker&#x22; box connected to an &#x22;LLM&#x22; box containing a list of phrases." />
</Frame>

Reranking pipeline (concise)

* User query → Initial retrieval (Top K)
* Reranker scores top K with a cross-encoder or LLM (joint scoring)
* Select top N reranked candidates → Final LLM or downstream use

The reranker output can be:

* Scalar scores (e.g., 0.0–1.0)
* Likelihood labels (e.g., unlikely / likely / very likely)
  These signals are used to sort candidates before final generation or presentation.

<Frame>
  <img alt="The image shows a &#x22;Reranker in Action&#x22; with a list of movie titles and corresponding rank numbers, featuring a &#x22;Reranker&#x22; icon on the left." />
</Frame>

Benefits of reranking

* Improves specificity and precision of the final results
* Increases robustness to noisy or semantically similar but irrelevant candidates
* Prioritizes contextually correct documents for LLM generation, reducing hallucinations and improving factuality

When to add a reranker
Use a reranker when one or more of the following apply:

* You can tolerate a small extra latency in exchange for higher precision
* The first-stage retriever returns many semi-relevant chunks (high recall, low precision)
* Queries are short or ambiguous and require contextual disambiguation
* The domain contains heavy jargon or domain-specific phrasing that needs deeper matching

> **lightbulb** Use reranking when the improvement in final-answer precision justifies additional compute and latency. For latency-sensitive applications, consider hybrid configurations such as smaller reranker models or reducing K / N values.

<Frame>
  <img alt="The image lists three scenarios ideal for reranking, including allowing for a small latency hit, having weak precision in first-stage recall, and dealing with short, ambiguous, or jargon-heavy queries." />
</Frame>

Reranking vs. initial retrieval — quick comparison

| Dimension   | Initial retrieval (bi-encoder / BM25 / ANN)                           | Reranking (cross-encoder / LLM)                                  |
| ----------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Speed       | Very fast, optimized for high recall                                  | Slower — introduces extra latency                                |
| Scoring     | Independent embeddings or term matching (moderate semantic relevance) | Joint query-document scoring (higher-quality semantic reasoning) |
| Accuracy    | Good recall but lower precision in ambiguous contexts                 | Better final precision and contextual correctness                |
| Typical use | Produce top K candidates quickly                                      | Reorder top K to pick the best N for downstream use              |

Common architectural pattern

| Stage   | Typical component             | Role                                                          |
| ------- | ----------------------------- | ------------------------------------------------------------- |
| Stage 1 | Bi-encoder / ANN index        | Fast retrieval of top K candidates (maximize recall)          |
| Stage 2 | Cross-encoder or LLM reranker | Joint scoring for high-quality relevance (improves precision) |
| Stage 3 | Final LLM / application       | Generate answer or display the top N reranked items           |

Practical considerations

* Cost & latency: Rerankers add compute; choose model size and K carefully.
* Candidate sizes: Typical flows use K (retriever) large enough for recall, then N (reranker output) small enough for efficient downstream generation.
* Model choices: Cross-encoders are efficient for pairwise scoring; LLM-based rerankers provide flexible reasoning but often at higher cost.

Related reading and tools

* Retrieval-Augmented Generation (RAG) concepts and best practices: [https://www.retrieval-augmented-generation.example](https://www.retrieval-augmented-generation.example) (replace with your internal docs)
* Cross-encoders and pairwise ranking models: [https://huggingface.co/docs](https://huggingface.co/docs)
* Vector databases and ANN indices (Pinecone, Milvus, Faiss) for first-stage retrieval

This lesson focused on reranking — complementary topics to explore next include cross-encoders, LLM-based rerankers, and practical tuning of K and N for cost/latency trade-offs.

- [Watch Video](https://learn.kodekloud.com/user/courses/fundamentals-of-rag/module/316bc17d-74b4-4bc8-bac7-62286dc8eee8/lesson/5a2b2cb8-f512-44c3-b9b4-d7d1217aaacd)
