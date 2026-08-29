# Adding Memory to LLM Apps

Source: https://notes.kodekloud.com/docs/LangChain/Adding-Memory-to-LLM-Apps/Adding-Memory-to-LLM-Apps/page

Explains how to add short and long term memory to LLM applications using stores like Redis and vector databases, plus persistence, retrieval, and privacy best practices.

Welcome back.

In this lesson we cover a core capability for conversational AI: adding memory to LLM applications. Memory (also called history or context) enables multi-turn conversations by supplying prior exchanges to the model so it can respond coherently over time.

<Frame>
  <img alt="The image is a flowchart showing the interaction between a user and an application, which processes a prompt and response through context, history, and a language model." />
</Frame>

Why history is necessary

* LLMs are stateless by default. Each request is treated independently unless you include prior context.
* Without history, the model has no memory of earlier turns and can produce inconsistent or hallucinated responses.
* To preserve continuity, you must capture relevant prior exchanges, persist them as needed, and send the appropriate context with each prompt.

> **lightbulb** LLMs do not remember past requests on their own. Think of each model call like a single HTTP request: to provide continuity, you need to re-supply the prior conversation or a summary of it with each request.

Memory: short-term vs long-term
Memory for LLMs generally falls into two categories:

| Memory Type            | Description                                                                                        | When to use                                                                                              |
| ---------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Short-term (session)   | Volatile, kept in application memory (e.g., RAM) for the duration of a user session.               | Real-time chats, single-session context where persistence across restarts is not required.               |
| Long-term (persistent) | Stored in an external durable store so history survives restarts and is available across sessions. | User preferences, personal profiles, long-running projects, or systems that require retrieval over time. |

<Frame>
  <img alt="The image shows three icons representing Short-Term Memory, History, and Long-Term Memory, with a note indicating &#x22;Stored at RAM&#x22; next to the Short-Term Memory icon." />
</Frame>

Choosing a long-term store
Long-term memory is implemented by externalizing conversational data to a database or vector store. Your choice depends on retrieval patterns, scale, and search needs. Common options include:

* Redis — simple to integrate, supports multiple data structures and expiration policies.
* SQLite — lightweight SQL database for local persistence.
* Vector stores — for semantic similarity search when using embeddings (e.g., Faiss, Milvus, Pinecone, Weaviate).
* Other databases — Postgres, MongoDB, cloud-managed stores.

<Frame>
  <img alt="The image lists Redis and SQLite as examples of long-term memory storage solutions." />
</Frame>

Example: basic Redis-backed conversation memory
Below is a minimal pattern for persisting and rehydrating conversational history to Redis. Store each message as a list element per `conversation_id`, then retrieve recent messages to build the prompt.

* Pseudocode to append a message:

```python theme={null}
