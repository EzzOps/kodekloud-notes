# LLM Context

Source: https://notes.kodekloud.com/docs/LangChain/Building-Blocks-of-LLM-Apps/LLM-Context/page

How to supply programmatic external context and use retrieval augmented generation to reduce LLM hallucinations via ingestion, embeddings, vector stores, chunking, and prompt construction

When building applications with large language models (LLMs), "context" refers to the external information supplied to the model at query time so it can generate accurate, up-to-date, and relevant responses. Because LLMs are trained on datasets with a fixed cutoff date, supplying fresh context is essential to avoid out-of-date answers and reduce erroneous outputs.

<Frame>
  <img alt="The image shows a chatbot interface with a message explaining that it cannot answer questions due to a training cutoff date. There's also a &#x22;Context&#x22; icon and text by KodeKloud in the lower left corner." />
</Frame>

Why programmatic context matters

* In production you cannot manually paste long documents or many records into prompts.
* Context must be gathered, preprocessed, and injected automatically.
* Properly supplied context helps the LLM produce grounded, verifiable answers instead of guesses.

Hallucinations: the problem context solves
Hallucinations occur when an LLM confidently produces incorrect or fabricated information. These are particularly risky in domains requiring factual accuracy (legal, medical, financial, etc.). Supplying relevant, sourceable context is one of the most effective ways to reduce hallucinations.

<Frame>
  <img alt="The image shows a diagram labeled &#x22;Hallucinations&#x22; with an icon of a brain, stars, and a chat message box illustrating a flawed logical deduction by an AI model." />
</Frame>

How context is used
To minimize hallucinations and improve relevance, systems query external data sources, retrieve the most relevant pieces, and add them to the LLM prompt. The diagram below summarizes the core building blocks and flow of a typical LLM application: user input → application logic → retrieval of external context → prompt construction → language model → response.

<Frame>
  <img alt="The image illustrates the key building blocks of an LLM application, including user interaction, application, prompt and response handling, language model, context, and external data sources. It shows the flow and interconnections between these components." />
</Frame>

Common sources of context
Use the following types of storage and services to provide the LLM with relevant external context:

| Source type           | Typical use case                                                   | Example                                                                                             |
| --------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| Relational databases  | Structured transactional data, joins and reporting                 | PostgreSQL, MySQL                                                                                   |
| NoSQL databases       | Flexible schemas, hierarchical documents, high-scale reads         | MongoDB, Cassandra                                                                                  |
| Vector databases      | Similarity search on embeddings for semantic retrieval             | See [Vector Database for GenAI](https://learn.kodekloud.com/user/courses/vector-database-for-genai) |
| Full-text search      | Unstructured document search (PDFs, Word, HTML)                    | Elasticsearch, OpenSearch                                                                           |
| External APIs         | Real-time data such as flight status, stock quotes, order tracking | REST/GraphQL APIs                                                                                   |
| Web search / scraping | Aggregating information from multiple web pages                    | Custom scrapers or search APIs                                                                      |

Typical production pipeline for supplying context
In production you usually automate several steps: ingesting content, preprocessing, generating embeddings, storing them in a vector store, and then retrieving the best-matching chunks at query time. These retrieved chunks are assembled into a prompt that the LLM can use as factual evidence.

<Callout icon="lightbulb">
  A typical pipeline to provide context programmatically:

  1. Ingest documents (PDFs, web pages, DB rows, API responses).
  2. Chunk long documents into manageable pieces.
  3. Generate embeddings for each chunk.
  4. Store embeddings in a vector database.
  5. At query time, embed the user query and perform a similarity search to retrieve the most relevant chunks.
  6. Assemble those chunks into context and inject them into the prompt (Retrieval-Augmented Generation — see [Fundamentals of RAG](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)).
</Callout>

Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) combines retrieval and generation so the LLM answers queries grounded in fetched documents rather than only its training data. A common RAG workflow:

* Embed the user query and perform a semantic search over your vector index.
* Optionally rank, filter, or deduplicate the retrieved passages.
* Construct a prompt that includes the selected passages plus the user question.
* Send the composed prompt to the LLM to generate a grounded response.
  RAG reduces hallucinations by providing sourceable facts and makes it possible to answer questions about content that the LLM was not trained on. For a deeper dive, see [Fundamentals of RAG](https://learn.kodekloud.com/user/courses/fundamentals-of-rag).

Putting it all together

* Design your ingestion pipeline to preserve provenance (timestamps, source IDs, URLs) so generated answers can cite sources.
* Choose chunking and embedding strategies that balance retrieval precision and context length.
* Use a vector database optimized for nearest-neighbor and hybrid search when you need high-quality semantic retrieval.
* Validate responses where possible by cross-referencing retrieved sources and adding verification steps in your application logic.

Further reading and references

* [Vector Database for GenAI](https://learn.kodekloud.com/user/courses/vector-database-for-genai)
* [Fundamentals of RAG](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)

This lesson will cover chunking strategies, embedding model selection, vector storage patterns, prompt construction best practices, and response verification techniques to build robust, low-hallucination LLM applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/bb8afda8-9de9-4865-aabf-bc71786440b2/lesson/710cf4ad-299d-49bb-86f0-6b06a41502f7" />
</CardGroup>
