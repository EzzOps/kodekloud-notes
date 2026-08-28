# Architecting Long Term Memory LTM

Source: https://notes.kodekloud.com/docs/LangGraph/Long-Term-Memory-and-Stateful-Persistence/Architecting-Long-Term-Memory-LTM/page

Guide to designing long-term memory for conversational agents using vector stores and databases, covering retrieval and write patterns, RAG integration, storage formats, and memory hygiene best practices

Why long-term memory matters

Long-term memory (LTM) is what turns a simple chatbot into a true personal assistant. While short-term context only persists within a single conversation or execution, LTM preserves facts, preferences, events, and outcomes across sessions. This persistence enables continuity, personalization, and better decision-making over time—key elements for assistants that feel consistent and useful.

<Frame>
  <img alt="The image compares a basic chatbot with short-term memory to a true personal assistant with long-term memory, highlighting the benefits of personalized interactions and continuity." />
</Frame>

LTM in LangGraph

In LangGraph, long-term memory typically lives outside the graph: vector stores, databases, or file systems are common choices. Specific graph nodes read from or write to these external stores during execution. Retrieved information is merged into the current state or prompt so the model can reason with past context without permanently bloating the graph’s internal state.

Think of it this way: if Robbie has a notebook for today’s deliveries, LTM is the file cabinet where he keeps all past routes, preferences, and customer notes.

<Frame>
  <img alt="The image shows a person named Ravi holding a clipboard, with documents flying from his position towards a file cabinet labeled &#x22;LTM (File Cabinet)&#x22; under the title &#x22;Long-Term Memory in LangGraph.&#x22;" />
</Frame>

Common LTM storage formats

Choose the storage format according to the type of memory you need:

| Storage Type                 | Best for                                                   | Example / Notes                                                                                        |
| ---------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Vector store (embeddings)    | Semantic memories: conversations, ideas, summaries         | Good for similarity search and retrieval-augmented generation (RAG). Examples: FAISS, Pinecone, Milvus |
| Relational/NoSQL DB          | Structured facts: preferences, order history, account data | Use for strongly-typed queries and transactions                                                        |
| File system / Object storage | Logs, summaries, raw documents                             | Suitable for archival, simple summaries, or large binaries                                             |

<Frame>
  <img alt="The image illustrates the long-term memory structure in LangGraph, comprising a vector store, relational database, and raw text file to manage embeddings, structured data, and summaries/logs." />
</Frame>

Read and write patterns

Reading: retrieval nodes query external stores (for example, a vector database) before an important decision point. The retrieved facts or documents are merged into the graph state or prompt so the LLM can reason with that context. Note that injected context consumes the model’s context window.

Writing: after an interaction, summarize or extract relevant details (task outcomes, preferences, goals, recurring intents) and persist them. Store metadata such as user ID, timestamp, and source to improve later retrieval accuracy.

<Frame>
  <img alt="The image illustrates a workflow for writing to Long-Term Memory (LTM) after execution, showing steps from post-interaction summarization to writing and indexing with metadata into a vector store and structured database. It includes elements like task outcomes, user facts, goals, and recurring intents." />
</Frame>

A common semantic-memory flow (vector store)

* Convert texts into embeddings and index them in a vector store.
* At runtime, query the vector store using the current user input to find relevant documents.
* Inject retrieved documents (or summaries) into the graph state or prompt.
* Use the enriched inputs for downstream reasoning or response generation.
* Optionally summarize and persist new information back to the vector store with metadata.

<Frame>
  <img alt="The image is a diagram illustrating the &#x22;Vector Store Memory Pattern,&#x22; showing how text is converted into vector embeddings for storing and retrieving information to solve short-term memory limitations. It highlights components like semantic similarity search and accessible memory items for improving agent intelligence and consistency." />
</Frame>

Concise, practical example

The example below demonstrates loading a saved FAISS index, turning it into a retriever, and wrapping retrieval logic as a LangGraph-compatible node using `RunnableLambda`. Ensure you use the same embedding model when loading the index that you used when creating it.

```python theme={null}
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.runnables import RunnableLambda
