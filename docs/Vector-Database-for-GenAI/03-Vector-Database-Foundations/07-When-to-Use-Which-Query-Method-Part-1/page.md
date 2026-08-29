# When to Use Which Query Method Part 1

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Vector-Database-Foundations/When-to-Use-Which-Query-Method-Part-1/page

Guidance on when to use semantic search, KNN, and hybrid vector query methods, with recaps, usage signals, and practical examples.

Hello and welcome back.

Previously we covered all seven vector database query methods. The practical question now is: which one should you use, and when?

This lesson breaks that down for the first three methods. For each method we provide:

* a concise recap of what it does,
* clear signals for when to use it, and
* concrete example use cases.

The remaining four query methods are covered in Part 2.

***

## 1) Semantic search

Recap\
Semantic search converts a natural-language query into a vector embedding and returns items that are conceptually similar to that query. It prioritizes meaning over exact keyword matches.

When to use semantic search

* Users type free-form text (not selecting from menus or entering product/model codes).
* You need meaning-based matching instead of exact keyword matching.
* Your data lacks consistent keywords; users describe intent or attributes rather than naming items.
* You are building conversational interfaces (chatbots, AI assistants) that must interpret intent.
* You are building Retrieval-Augmented Generation (RAG) systems where a retriever finds relevant documents to feed an LLM.

<Callout icon="lightbulb">
  RAG stands for Retrieval-Augmented Generation. In RAG, a retriever (often a vector search) finds relevant documents which are then provided to a generative model to produce more accurate, context-aware responses.
</Callout>

Examples

* E-commerce: A shopper types “comfortable shoes for walking.” Semantic search matches that intent to product listings labeled “sneakers,” “walking shoes,” or “athletic footwear” even if the exact words differ.
* Customer support: A new support ticket written in different words than past tickets still returns relevant historical tickets and resolutions because semantic similarity captures intent and meaning.

<Frame>
  <img alt="The image is a table titled &#x22;When to Use Which Query Method? - Part 1&#x22; and describes &#x22;Semantic Search&#x22; as a query method. It outlines when to use it, including for free-form text inputs, meaning-based matching, and conversational interfaces, with example use cases in e-commerce and customer support." />
</Frame>

***

## 2) K nearest neighbor (KNN) search

Recap\
KNN returns a fixed number `K` of the most similar vectors using a chosen similarity or distance metric (e.g., `cosine similarity`, Euclidean distance, or dot product). Results are ordered from most to least similar.

When to use KNN

* You require an exact number of results (for example `top-5` or `top-10`).
* Results must be ranked by similarity.
* Your UI or business logic expects a fixed count of recommendations or responses.
* The choice of similarity metric matters for relevance and should be selected intentionally.

Examples

* Recommendations: Show exactly 20 movies similar to the one a user just watched. Use KNN to retrieve the 20 closest movie vectors.
* Visual search: Upload an image and return the ten most visually similar products using cosine similarity over image embeddings.

***

## 3) Hybrid search

Recap\
Hybrid search combines vector similarity (semantic relevance) with deterministic metadata filtering. It returns semantically relevant items while enforcing exact constraints such as price ranges, availability, or location.

When to use hybrid search

* You need both semantic matching and hard attribute filters at the same time.
* Business constraints must be enforced (for example price caps or inventory availability).
* You want meaning-based retrieval but also reliable, deterministic filtering for exact fields.

Examples

* Real estate: Interpret “modern apartments near downtown” semantically, then apply filters such as `price < 2000`, `bedrooms = 2`, and `pet_friendly = true` to produce the final set of results.
* Job search: Semantically match on skills and role (e.g., “machine learning engineer”) while applying filters like `location`, `salary_range`, and `remote`/`on-site` flags.

<Frame>
  <img alt="The image is a three-column chart describing when to use the &#x22;Hybrid Search&#x22; query method, highlighting its combination of vector similarity with metadata filtering, and providing example use cases in real estate and job search." />
</Frame>

***

## Quick comparison

| Method          | Best for                                                 | Typical outputs                                    |
| --------------- | -------------------------------------------------------- | -------------------------------------------------- |
| Semantic search | Free-text intent, conversational queries, RAG retrievers | Semantically similar items (no fixed count)        |
| KNN search      | Fixed-count, ranked recommendations                      | Top-`K` nearest neighbors ordered by similarity    |
| Hybrid search   | Semantic relevance + exact constraints                   | Semantically relevant results filtered by metadata |

***

Next steps

* Use semantic search when you need meaning-based matching or are feeding documents into an LLM.
* Use KNN when you need a fixed, ranked set of nearest items.
* Use hybrid when you must combine semantic relevance with strict metadata filters.

We're done with Part 1. The remaining four query methods are covered in Part 2.

## Links and references

* [Vector search and semantic retrieval concepts](https://en.wikipedia.org/wiki/Semantic_search)
* [Introduction to Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/82014ec3-9709-44d1-bd41-577af87083ed/lesson/fe2804d3-4d5c-4b8a-b8f1-2b97995924b7" />
</CardGroup>
