# Inspect basic page count
len(pages)
# Inspect the first page's text (print a slice if long)
pages[0].page_content[:400]
```

This gives you page-level Document objects with `page_content` and default metadata (e.g., `source`, `page`).

## 2. Create a text splitter to produce chunks

We commonly use `RecursiveCharacterTextSplitter` for robust splitting that respects sentence boundaries and reduces awkward cuts. Here we create a splitter configured with a chunk size of 200 characters and 50 characters of overlap between consecutive chunks:

```python theme={null}
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = text_splitter.split_documents(pages)
```

Why use a splitter:

* It transforms long pages into passage-sized Documents suitable for embeddings and vector stores.
* It can preserve natural language boundaries (sentences, paragraphs) when configured properly.

## 3. Why chunk with overlap?

Overlap between chunks preserves context across chunk boundaries so that ideas cut near a boundary remain recoverable. Overlap reduces the chance of losing relevant context during retrieval and increases the probability that a retrieved chunk contains a complete thought.

Benefits:

* Better context for LLM prompts when a single chunk lacks all required information.
* Smoother transitions across document segments for multi-sentence ideas.
* Tolerates noisy splits and improves recall at retrieval time.

Tradeoffs:

* Introduces redundancy (more tokens to embed/store).
* Larger total storage and slightly higher retrieval cost.

> **lightbulb** Tip: If queries require longer context, increase `chunk_size`. For precise answers on short queries, reduce `chunk_size` but keep a modest `chunk_overlap` (e.g., 25–50 characters).

## 4. Inspect the resulting chunks and metadata

After splitting, inspect chunk count and a sample chunk to confirm expected behavior:

```python theme={null}
len(chunks)
# -> 40
```

Each chunk is a Document-like object containing `page_content` and `metadata` (for example, `source` and `page`). Example representation:

```python theme={null}
chunks[0]
# -> Document(page_content='LakeSide Bicycles Employee Handbook Welcome to the team! LakeSide Bicycles is a company that values quality, innovation, and customer satisfaction. We are passionate about creating and selling', metadata={'source': 'data/handbook.pdf', 'page': 0})
```

Notes on metadata:

* By default, PDF splitting includes `source` and `page` metadata. This is useful for citing sources in model responses.
* When processing multiple documents, robust metadata (filename, URL, document ID) helps trace every chunk to its origin.

## 5. Choosing chunk size and overlap (practical guidance)

Choose `chunk_size` and `chunk_overlap` based on document characteristics, retrieval goals, and the LLM context window. The table below summarizes common scenarios:

| Chunk Size              | Use Case                                                   | Recommendation                                                                        |
| ----------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Small (50–300 chars)    | Short notes, chatty text, fine-grained retrieval           | Good for precise answers; increase overlap slightly (25–75 chars)                     |
| Medium (300–1500 chars) | Typical articles, documentation, manuals                   | Balanced: good precision and context without too much redundancy                      |
| Large (>1500 chars)     | Long-form content when retrieval must return large context | Use when LLM context window is large; keep overlap moderate to avoid large duplicates |

Factors to consider:

* Document structure (long paragraphs vs short bullets).
* Expected query type (fact lookup vs long-answer generation).
* Vector store and embedding cost/performance.
* LLM prompt budget (context window size).

## 6. Summary: chunking workflow

1. Load the document into page-level Documents (e.g., with `PyPDFLoader`).
2. Configure `RecursiveCharacterTextSplitter` with appropriate `chunk_size` and `chunk_overlap`.
3. Call `split_documents(pages)` to produce a list of chunk Document objects.
4. Each chunk contains `page_content` and `metadata` and can be embedded and stored in a vector store for semantic search and RAG.

## 7. Next steps: embeddings and semantic search

After chunking, the typical next steps are:

* Create embeddings for each chunk (e.g., OpenAI embeddings, other models).
* Store embeddings in a vector store (FAISS, Pinecone, Milvus, etc.).
* Implement semantic search and retrieve relevant chunks for LLM prompts.

Useful references:

* LangChain text splitters and document loaders: [https://python.langchain.com/docs/](https://python.langchain.com/docs/)
* Vector stores (FAISS, Pinecone) and embeddings documentation: [https://langchain.readthedocs.io/en/latest/modules/indexes.html](https://langchain.readthedocs.io/en/latest/modules/indexes.html)

A solid understanding of chunking helps ensure your RAG pipeline retrieves coherent, contextually complete passages and produces higher-quality responses from LLMs.

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/e47b44c9-65c3-46f8-8bed-b075a18ab12b/lesson/fc020e0a-7253-4445-8fff-d30d8d639315)


# Generating Embeddings

Source: https://notes.kodekloud.com/docs/LangChain/Performing-Retrieval/Generating-Embeddings/page

Explains how to create text embeddings, convert documents to numeric vectors, and use them for semantic search and retrieval augmented generation workflows.

We are now in the third phase of the workflow: generating embeddings. In this lesson we convert text chunks into numeric vectors (embeddings). Before returning to the PDF-based workflow where we already loaded and chunked documents, let's take a short detour to understand embeddings as a standalone concept — this will clarify how retrieval-augmented generation (RAG) works and why embeddings are central to semantic search.

Embeddings are numeric vector representations of text that preserve semantic meaning and context. Once converted, these vectors enable similarity comparisons (for example, via cosine similarity) so you can retrieve semantically related documents from a vector store.

## Step 1 — Initialize the embeddings model

First, import and initialize the embeddings object. In this example we use LangChain's `OpenAIEmbeddings` with the `text-embedding-3-large` model:

```python theme={null}
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
```

## Step 2 — Prepare documents to embed

Create a small list of documents. In a real pipeline these would be the chunks extracted from your PDFs or other sources; here we use example news headlines for illustration:

```python theme={null}
docs = [
    "Thrilling Finale Awaits: The Countdown to the Cricket World Cup Championship",
    "Global Giants Clash: Football World Cup Semi-Finals Set the Stage for Epic Showdowns",
    "Record Crowds and Unforgettable Moments: Highlights from the Cricket World Cup",
    "From Underdogs to Contenders: Football World Cup Surprises and Breakout Stars"
]
```

## Step 3 — Convert text to embeddings

Call `embed_documents` to convert the list of strings into a list of numeric vectors:

```python theme={null}
embed_docs = embeddings.embed_documents(docs)
```

You can verify that the number of returned embeddings matches the number of input documents:

```python theme={null}
len(embed_docs)
```

```plaintext theme={null}
4
```

Each element in `embed_docs` is an array of floating-point numbers (the embedding vector). Inspecting the first embedding (truncated) might look like this:

```python theme={null}
embed_docs[0][:16]
```

```plaintext theme={null}
[-0.03236965773282924, -0.03388830823998, -0.01959451046452, 0.00590366532974,
 0.00387870070599, 0.00891787786988, -0.01084504675850, -0.02438912601325,
 0.02694678889459, -0.02784329818992, 0.00495443632714, -0.00387356763555,
 0.01617953250937, -0.05444381939771, 0.00328312295737, 0.01673573782502]
```

The dimensionality of each vector depends on the chosen embedding model. For `text-embedding-3-large` the vectors have 3072 dimensions:

```python theme={null}
len(embed_docs[0])
```

```plaintext theme={null}
3072
```

> **lightbulb** Embeddings are not meant to be human-readable. They are high-dimensional numeric representations used by algorithms to compute semantic similarity (for example, via cosine similarity) during semantic search or retrieval.

## Quick reference — embedding workflow

| Step              | Purpose                      | Example / Result                                             |
| ----------------- | ---------------------------- | ------------------------------------------------------------ |
| Initialize model  | Create an embeddings client  | `OpenAIEmbeddings(model="text-embedding-3-large")`           |
| Prepare documents | Text chunks to convert       | `docs = ["headline1", "headline2", ...]`                     |
| Embed documents   | Convert to vectors           | `embed_docs = embeddings.embed_documents(docs)`              |
| Validate          | Ensure counts and dims match | `len(embed_docs) == len(docs)`; `len(embed_docs[0]) == 3072` |

## What to do with these vectors

Once you have these vectors you typically:

* Store them in a vector database (ANN index) for efficient similarity search.
* Use similarity metrics (cosine similarity, dot product) to retrieve the most relevant chunks for a given user query.
* Combine retrieved context with a generative model for retrieval-augmented generation (RAG) — e.g., building a Q\&A chatbot over your PDF corpus.

For vector storage and retrieval, consider vector databases or specialized libraries that support approximate nearest neighbor (ANN) search and persistence.

## Links and references

* [Vector Database for GenAI](https://learn.kodekloud.com/user/courses/vector-database-for-genai)
* LangChain embeddings docs — see relevant model usage and parameters
* OpenAI embeddings documentation — model options and dimensionality

In the next part of this lesson we'll introduce a vector database and demonstrate a simple similarity search. After covering retrieval and storage, we'll continue building the Q\&A chatbot for the PDF.

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/e47b44c9-65c3-46f8-8bed-b075a18ab12b/lesson/187f5776-2d66-4326-bee6-86ba7569e581)
