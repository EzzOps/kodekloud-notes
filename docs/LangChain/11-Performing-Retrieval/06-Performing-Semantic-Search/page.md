# Indexing
documents = load_documents(source_paths)
chunks = text_splitter.split(documents)
embeddings = embed_model.encode(chunks)
vector_db.upsert(chunks, embeddings, metadata)

# Query time
query_embedding = embed_model.encode(query_text)
matches = vector_db.similarity_search(query_embedding, top_k=5)
context = assemble_context(matches)
prompt = build_prompt(query_text, context)
answer = llm.generate(prompt)
return answer, matches.metadata
```

Best practices

* Use the same embeddings model for indexing and querying.
* Tune chunk size to balance context preservation vs retrieval granularity.
* Store rich metadata (source URL, document id, chunk offsets) so answers can include citations.
* For highly sensitive data, use access controls or on-premise vector stores to minimize exposure.

References and tooling

* LangChain: an ecosystem of components for building RAG pipelines and LLM apps.
* Vector DBs: [Chroma](https://www.trychroma.com/), [Milvus](https://milvus.io/), [Weaviate](https://weaviate.io/), [Qdrant](https://qdrant.tech/)

> **lightbulb** RAG combines semantic search with generation: the search finds evidence and the LLM composes the answer. For reliable semantic matching, always use the same embeddings model for both indexing and query encoding.

- [Watch Video](https://learn.kodekloud.com/user/courses/langchain/module/e47b44c9-65c3-46f8-8bed-b075a18ab12b/lesson/fa08ba22-b76f-4355-8a50-4a40dd49aba8)


# Performing Semantic Search

Source: https://notes.kodekloud.com/docs/LangChain/Performing-Retrieval/Performing-Semantic-Search/page

Guide to creating embeddings with OpenAI, storing them in Chroma, and performing semantic similarity search using LangChain for retrieval augmented applications

In this lesson you'll convert text into embeddings, store them in a vector database (Chroma), and run a simple semantic (similarity) search using LangChain and OpenAI embeddings. This pattern is useful for retrieval-augmented generation (RAG), search interfaces, and any application that needs semantic relevance rather than exact text matches.

## Prerequisites

Make sure you have:

* Installed the required Python packages (for example, [langchain](https://python.langchain.com/) and [Chroma](https://www.trychroma.com/)).
* Configured your OpenAI API key (for example by setting the `OPENAI_API_KEY` environment variable). Creating embeddings calls the [OpenAI API](https://platform.openai.com/docs/guides/embeddings).

Useful references:

* [LangChain Documentation](https://python.langchain.com/)
* [Chroma (vector DB)](https://www.trychroma.com/)
* [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

## Step 1 — Imports and Example Documents

Import the required modules, create an embeddings object, and define a small set of example documents (headlines). These headlines will be embedded and indexed in the vector store.

```python theme={null}
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

docs = [
    "Thrilling Finale Awaits: The Countdown to the Cricket World Cup Championship",
    "Global Giants Clash: Football World Cup Semi-Finals Set the Stage for Epic Showdowns",
    "Record Crowds and Unforgettable Moments: Highlights from the Cricket World Cup",
    "From Underdogs to Contenders: Football World Cup Surprises and Breakout Stars"
]
```

## Step 2 — Create the Chroma Vector Store

Chroma is an open-source vector database that:

* Indexes and stores vectors (embeddings) with optional metadata.
* Performs fast similarity search / retrieval over those vectors.

You can create a Chroma vector store directly from strings, or from pre-chunked documents/pages. Here we pass raw text strings:

```python theme={null}
vectorstore = Chroma.from_texts(texts=docs, embedding=embeddings)
```

If you have metadata (source, URL, id), pass documents with metadata instead of plain strings to make downstream identification easier.

## Step 3 — Run Semantic Similarity Searches

When you query the vector store, the query is embedded with the same model and compared to the stored vectors. Use the `k` parameter to control how many nearest neighbors you retrieve.

```python theme={null}
