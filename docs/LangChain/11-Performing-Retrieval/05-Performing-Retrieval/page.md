# typically 1 for standard article pages
```

## 2) Inspect the loaded Document

A single Document usually contains full page content in `page_content` and any available metadata in `metadata`.

```python theme={null}
doc = data[0]
print(type(doc))                # e.g., <class 'langchain.schema.Document'>
print(doc.metadata)             # metadata dictionary (may include title, source url)
print(doc.page_content[:300])   # print the first 300 characters of the page
```

<Callout icon="lightbulb">
  Web pages are usually loaded as a single Document (so `len(data)` is often 1). Each Document has `page_content` (the full text) and `metadata` (title, source URL, etc., when available). Use these fields when adding provenance to your index or when building prompts that reference sources.
</Callout>

<Callout icon="warning">
  Respect website terms of service and robots.txt when scraping or ingesting web content. For production ingestion, consider rate limits, caching, and error handling for transient network issues.
</Callout>

## 3) Split (chunk) the text for embedding or indexing

Large documents should be split into smaller overlapping chunks before embedding or indexing. The RecursiveCharacterTextSplitter is a good default for general-purpose chunking.

Example:

```python theme={null}
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(data)  # splits the list of Documents
len(chunks)
```

Each element in `chunks` is a `Document` representing an excerpt of the original page. These chunks are ready to be passed to an embedding model or a vector store.

## Typical workflow after chunking

1. Create embeddings for each chunk.
2. Store embeddings and chunk metadata in a vector database.
3. Retrieve relevant chunks at query time and use them as context in a prompt to an LLM.

Links and references:

* [LangChain Documentation](https://langchain.readthedocs.io/)
* [LangChain Community Loaders](https://github.com/langchain-ai/langchain-community)
* Original article used: [https://www.theverge.com/2024/4/18/24133808/meta-ai-assistant-llama-3-chatgpt-openai-rival](https://www.theverge.com/2024/4/18/24133808/meta-ai-assistant-llama-3-chatgpt-openai-rival)

## Quick reference table

| Step      | Purpose                                  | Example / Command                                                    |
| --------- | ---------------------------------------- | -------------------------------------------------------------------- |
| Load page | Fetch and parse HTML -> `Document`       | `WebBaseLoader(URL).load()`                                          |
| Inspect   | View metadata and preview content        | `doc.metadata`, `doc.page_content[:300]`                             |
| Chunk     | Produce smaller Documents for embeddings | `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)` |

This completes loading a webpage and preparing it for chunking and embedding. From here, you can proceed to create embeddings, insert into a vector store (e.g., Pinecone, FAISS, Milvus), and build retrieval-augmented prompts for downstream applications.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-65c3-46f8-8bed-b075a18ab12b/lesson/c29062bc-7d53-4855-b98e-c9cb5ae6cbe3" />
</CardGroup>


# Performing Retrieval

Source: https://notes.kodekloud.com/docs/LangChain/Performing-Retrieval/Performing-Retrieval/page

Describes Retrieval-Augmented Generation and RAG pipelines for retrieving context, embeddings, and vector search to ground LLM outputs, reduce hallucinations, and enable citations.

Welcome back.

In this lesson we cover performing retrieval—an essential capability for building reliable LLM applications. By the end of this lesson you will understand Retrieval-Augmented Generation (RAG), the typical RAG pipeline, and how external context is retrieved and injected into prompts so an LLM can respond accurately with fewer hallucinations.

Why retrieval matters

* Context is the most important building block of an LLM application. Context means external information (documents, databases, APIs, or the web) retrieved and added to the prompt so the model has knowledge-rich background to generate factually correct responses.
* When you ground an LLM’s output in retrieved evidence, you reduce hallucinations and make answers explainable and auditable.

Where does context come from?

* Relational databases (SQL queries)
* Full-text search indexes (e.g., Elasticsearch)
* Semantic search over vector embeddings stored in a vector database
* Files and documents (PDF, Word, HTML), object storage (S3), or any external API
* Real-time web search for time-sensitive queries

<Frame>
  <img alt="The image displays logos of various database systems (MySQL, SQLite, PostgreSQL, MongoDB) alongside icons for different file types and storage formats (PDF, document, HTML, bucket, DOC, API)." />
</Frame>

In many applications the most common sources are documents—PDFs, web pages, or unstructured files. For time-sensitive answers, you may also pull context directly from a web search.

<Frame>
  <img alt="The image shows a web search icon above a search bar interface with a magnifying glass symbol." />
</Frame>

Retrieve only what’s relevant
The primary idea is to retrieve only the relevant passages (chunks) and place them into the prompt so the model has the right facts. This:

* Keeps answers accurate and grounded
* Reduces token usage and cost
* Limits exposure of private data to external models

RAG explained
Retrieval-Augmented Generation (RAG) is the established pattern that augments LLM responses with facts retrieved from external sources so the model can answer accurately and cite sources when needed.

<Frame>
  <img alt="The image illustrates the concept of Retrieval Augmented Generation (RAG), showing the interaction between external data sources and a large language model (LLM) to enhance information with additional facts." />
</Frame>

Why not send an entire document?
Two practical reasons:

1. Context window limits: Every model has a finite context window—the combined size of input (prompt + context) and output. Sending a full 100-page PDF is usually impossible or inefficient.
2. Relevance and privacy: Sending only the relevant subset minimizes exposure of sensitive data and makes it easier to trace the source of a fact.

Instead of sending full documents, RAG retrieves the most relevant chunks (paragraphs or passages) that fit in the model’s context window. This reduces hallucinations and enables transparency: you can cite the exact source and passage used to generate an answer.

<Frame>
  <img alt="The image displays the concept of Retrieval Augmented Generation (RAG) with icons representing four aspects: Explainability, Transparency, Access Control, and Data Privacy." />
</Frame>

Typical RAG workflow (end-to-end)

1. User submits a question or prompt to a chatbot or application.
2. The system encodes the prompt and queries a search layer (semantic or full-text) over your corpus.
3. Relevant context chunks are retrieved.
4. The retrieved context is injected into the prompt and sent to the LLM.
5. The LLM returns a grounded answer that can include citations, which is delivered to the user.

<Frame>
  <img alt="The image illustrates a RAG (Retrieval-Augmented Generation) workflow, showing the interaction between a user, a chatbot, a large language model (LLM), and databases/documents for search and retrieval of context." />
</Frame>

This workflow splits naturally into two phases: indexing and retrieval.

Indexing (Phase 1)

* Load unstructured data (HTML, PDF, DOCX, JSON, images, etc.).
* Split the data into chunks (sentences, paragraphs, or fixed-size windows of tokens). Smaller chunks improve granularity; larger chunks preserve more local context.
* Convert each chunk into an embedding vector using an embeddings model (which may be distinct from your generative LLM).
* Store the vectors and metadata (source, document id, chunk id, offsets) in a vector database (e.g., Chroma, Milvus, Weaviate, Qdrant).

<Frame>
  <img alt="The image illustrates &#x22;RAG – Phase 1,&#x22; showing a process flow from loading to splitting and embedding, with numerical representations as output." />
</Frame>

Note on embeddings
An embeddings model encodes text into fixed-length numeric vectors suitable for semantic comparison. Use the same embeddings model for indexing and for queries to ensure consistent similarity scores.

Retrieval (Phase 2)

* Encode the user query with the same embeddings model used for indexing.
* Perform a similarity search across your vector database to find the closest vectors (semantic matches).
* Retrieve the corresponding text chunks and metadata, then assemble the context.
* Inject the retrieved context into the prompt and send it to the LLM.
* The LLM uses the question + retrieved evidence to generate a grounded answer.

<Frame>
  <img alt="The image illustrates the RAG (Retrieval-Augmented Generation) Phase 2 process, depicting a flow from a question through a retrieval mechanism, context creation, prompting, and processing by a large language model (LLM)." />
</Frame>

Putting the pieces together
A RAG pipeline typically includes these components. Below is a concise breakdown to guide implementation.

| Component        | Purpose                                                  | Example / Link                                                                                                                       |
| ---------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Document loaders | Ingest files, web pages, or data into memory             | `PDFLoader`, `HTMLLoader` (LangChain)                                                                                                |
| Text splitters   | Break documents into chunks for indexing                 | Sentence/paragraph splitters or token-window splitters                                                                               |
| Embeddings       | Encode text chunks and queries as vectors                | See provider docs for embedding models                                                                                               |
| Vector database  | Store and search vectors by similarity                   | [Chroma](https://www.trychroma.com/), [Milvus](https://milvus.io/), [Weaviate](https://weaviate.io/), [Qdrant](https://qdrant.tech/) |
| Retriever        | Performs semantic search and returns top matching chunks | Retriever abstraction in LangChain or custom search layer                                                                            |

<Frame>
  <img alt="The image depicts a diagram related to LangChain, featuring elements like document loaders and external data sources, including icons for a web search and PDF." />
</Frame>

Minimal RAG pseudocode
Use the following high-level pseudocode as a checklist when implementing a RAG Q\&A service:

```text theme={null}
