# Demo Ask Warren Anything You Want

Source: https://notes.kodekloud.com/docs/Vector-Database-for-GenAI/Introduction-to-Vector-Databases-and-Generative-AI/Demo-Ask-Warren-Anything-You-Want/page

A demo showing how a vector database and embeddings enable semantic search over Warren Buffett shareholder letters without using large language models

Welcome back. This lesson is a hands‑on demo that shows how a vector database can power semantic document search without calling a large language model. We'll index a small corpus of Warren Buffett's shareholder letters, convert them into embeddings, store them in a vector database, and run semantic queries that return relevant excerpts by meaning — not just by keyword.

<Frame>
  <img alt="The image depicts a diagram with annual letters being processed into a vector database for querying, titled &#x22;Ask Warren Buffet Anything You Want.&#x22;" />
</Frame>

## The demo app

The demo uses a simple web app with two primary views:

* A vector search interface for asking natural‑language questions.
* A document viewer/reference where you can inspect each uploaded letter.

I opened the document viewer to inspect the letters we’ll index.

<Frame>
  <img alt="The image displays a web interface titled &#x22;VectorDB Quickstart: Warren Buffett Letters (2020-2024)&#x22; with a button labeled &#x22;Store All Letters in VectorDB.&#x22;" />
</Frame>

Here’s an example of a loaded shareholder letter (2020). You can open any letter to review the original PDF content before or after indexing.

<Frame>
  <img alt="The image shows a webpage titled &#x22;Shareholder Letter Viewer,&#x22; displaying a PDF document titled &#x22;2020ltr.pdf.&#x22; The document contains a table comparing Berkshire's performance to the S&P 500." />
</Frame>

## Indexing: chunking → embeddings → vectors

Indexing is a three-step pipeline in the backend:

1. Split each document into smaller chunks (chunking).
2. Convert each chunk into an embedding vector using an embedding model.
3. Store the embedding vectors in the vector database for fast similarity search.

In this demo I indexed five letters (2020–2024). After clicking the `Store All Letters in VectorDB` button, the system processed the documents and returned these metrics:

| Metric              | Value     |
| ------------------- | --------- |
| Documents processed | 5 letters |
| Chunks processed    | 436       |
| Embedding dimension | `384`     |

Notes:

* Chunking splits long documents into indexable pieces so retrieval returns manageable passages.
* The embedding dimension (`384`) is the length of each numeric vector produced by the embedding model; vector comparisons operate on those fixed‑length representations.

## Semantic search (meaning-based retrieval)

When you submit a query, the app converts the text into an embedding and compares it with stored vectors to find semantically similar chunks. This returns passages that match the intent of the query rather than exact keywords.

Example query: `What are Warren Buffett's thoughts on the impact of COVID-19?`\
The app generates an embedding for the question, searches the vector index, and returns top matches ranked by similarity (or distance). The UI shows the source documents, the excerpt, and a distance/score for each match.

<Frame>
  <img alt="The image shows a semantic search interface displaying a query about Warren Buffett's thoughts on COVID-19 and suggests related questions. It also shows some processed information metrics and a section with search results." />
</Frame>

The results identify which letters the excerpts came from — for example, 2024, 2023, 2022 — and include a distance score. Important: some systems report similarity (higher = more similar) while others report distance (lower = more similar). Interpret the displayed metric according to the system you use.

Quick interpretation guide:

| Reported metric  | How to read it                     |
| ---------------- | ---------------------------------- |
| Distance         | Lower = more semantically similar  |
| Similarity score | Higher = more semantically similar |

## Example queries and behavior

Try different natural‑language phrasings. The system matches meaning, so related terms are often found even if the exact word isn’t used.

* Query: `What are his thoughts on Apple?`\
  Returns passages discussing Apple’s role in Berkshire, praise of its leadership, and references to Apple shares.

<Frame>
  <img alt="The image shows a webpage displaying search results related to thoughts on Apple in letters, with excerpts from a 2021 PDF document mentioning Apple and Berkshire." />
</Frame>

* Related query: `What are his thoughts on iPhone?`\
  Even if “iPhone” does not appear verbatim in an excerpt, the semantic search can return Apple‑related content because the meaning aligns.

<Frame>
  <img alt="The image shows search results related to Apple's stock, with excerpts from annual reports discussing Berkshire's holdings and repurchasing of Apple shares. The document snippets highlight financial aspects and managerial praise." />
</Frame>

## When to use this pattern

Document search using a vector database is widely used to:

* Index internal company documents, contracts, and policies.
* Power knowledge bases and help centers for natural‑language queries.
* Enable fast, meaning‑based retrieval for downstream workflows.

<Callout icon="lightbulb">
  This demo uses only a vector database and semantic search. No LLMs or external AI APIs (e.g., ChatGPT or Claude) were required to perform the searches shown here.
</Callout>

## Next topics

In upcoming lessons we’ll cover:

* How embeddings are generated and tradeoffs between models.
* Chunking strategies and how they influence retrieval accuracy.
* Distance metrics (cosine, Euclidean) and how to interpret scores in practice.

## Links and references

* Vector database concepts and providers: [https://www.vector-db.org/](https://www.vector-db.org/) (example directory)
* Embedding models and documentation: [https://platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings) (reference)
* Semantic search best practices and chunking strategies: [https://www.deeplearning.ai/](https://www.deeplearning.ai/) (guides and learning resources)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/841f0a59-96ec-4dc1-b84f-b577ab5a5bb7/lesson/76a3d461-f14a-436f-9835-6a43afbde74e" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/vector-database-for-genai/module/841f0a59-96ec-4dc1-b84f-b577ab5a5bb7/lesson/d40b2634-f33d-456b-a544-ff36b0448c61" />
</CardGroup>
