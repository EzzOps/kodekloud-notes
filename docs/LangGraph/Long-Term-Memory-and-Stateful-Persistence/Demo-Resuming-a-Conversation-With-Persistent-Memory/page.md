# Load vector store as a retriever (use the same embedding model used to create the index)
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.load_local(
    "ltm_index",
    embeddings=embedding_model
)
retriever = vectorstore.as_retriever()

# Define a LangGraph-compatible node that performs semantic retrieval
def retrieve_memory(state: dict) -> dict:
    query = state.get("user_input", "")
    # Use the retriever's standard API to get relevant documents
    docs = retriever.get_relevant_documents(query)
    # Return retrieved documents into the graph state under the `retrieved_memory` key
    return {"retrieved_memory": docs}

retrieve_node = RunnableLambda(retrieve_memory)
```

Key notes about the example:

* Use the same embedding model to create and to load the FAISS index.
* `as_retriever()` provides a stable retriever API (e.g., `get_relevant_documents`).
* Wrapping the function with `RunnableLambda` makes it usable as a node within LangGraph workflows.

How to use retrieved memories

Decide how to inject retrieved documents into the LLM prompt. Common strategies:

* Direct injection: place raw retrieved text under a labeled "User Facts" or "Context" section.
* Summarize first: reduce token usage by summarizing documents before injecting them.
* Merge into conversation state: append selected facts to the state buffer consumed by later nodes.

Example: prompt injection by joining retrieved documents

```python theme={null}
# Build a prompt by joining the page content of retrieved documents
retrieved_facts = "\n".join([doc.page_content for doc in state["retrieved_memory"]])
user_input = state["user_input"]

prompt = f"""
User Facts:
{retrieved_facts}

User: {user_input}
Assistant:"""
```

This retrieval-augmented generation (RAG) pattern lets the LLM reason with external memory as if it were part of the context window without permanently expanding the model’s internal state. See also: Retrieval-augmented generation.

Memory hygiene and best practices

* Store consistent metadata: user ID, timestamps, source, and tags improve targeted retrieval.
* Preprocess text: chunk long documents, remove irrelevant content, and normalize formatting before embedding. Clean inputs yield better embeddings.
* Tune retrieval: experiment with similarity thresholds and `k` (how many items to return). Often top 3–5 documents work best.
* Maintain indexes: deduplicate, merge similar entries into summaries, archive or delete stale entries periodically.

<Frame>
  <img alt="The image outlines three best practices: using consistent metadata, preprocessing text before storing, and experimenting with similarity thresholds and k-values." />
</Frame>

<Callout icon="lightbulb">
  Store and index metadata alongside embeddings (e.g., user ID, timestamp, source). This drastically improves targeted retrieval and enables efficient filtering of memories.
</Callout>

Avoid over-injecting

Injecting too much retrieved text into the prompt can inflate token usage and confuse the model. Prefer filtering, summarizing, or selecting the most relevant items for the current intent. Use structured prompts that clearly label retrieved facts and the current user query.

<Frame>
  <img alt="The image outlines strategies for memory hygiene and management, addressing a noisy LLM problem with actions like periodic cleaning and merging redundant memory, enabled by strong metadata tagging for better accuracy and speed." />
</Frame>

Real-world value

Long-term memory makes agents persistent and context-aware:

* Customer support: retrieve past tickets and resolutions to maintain continuity.
* Education: remember which topics a learner covered and adapt future lessons.
* Sales: surface lead-specific details during conversations.
* Copilots: fetch relevant docs or past decisions to assist with context.

Whether you choose vector stores for semantic memory or databases for structured facts, the architecture of your memory layer controls how personalized and consistent your agent will be over time.

Further reading and references

* FAISS: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Retrieval-augmented generation (RAG): [https://en.wikipedia.org/wiki/Retrieval-augmented\_generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
* LangGraph concepts and workflow patterns (see your LangGraph docs for implementation specifics)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-00a7-4c52-88e9-b3932b03ff9f/lesson/286ff108-f2af-457e-914f-5665501b7ec0" />
</CardGroup>


# Demo Resuming a Conversation With Persistent Memory

Source: https://notes.kodekloud.com/docs/LangGraph/Long-Term-Memory-and-Stateful-Persistence/Demo-Resuming-a-Conversation-With-Persistent-Memory/page

Demonstrates using LangGraph checkpointing to persist and resume conversation state across sessions using a thread identifier and a simple in memory checkpointer

In this lesson we demonstrate how to implement persistent conversational memory with LangGraph. Real-world assistants must often resume conversations across sessions: users close an app and return hours or days later expecting the assistant to remember earlier context. LangGraph addresses this with checkpointing — saving the graph state after each interaction so a conversation can be resumed later by loading that saved state.

What you'll learn

* How to model a minimal conversation state for LangGraph
* How to implement a simple chatbot node that updates state
* How to attach a checkpointer (here: `InMemorySaver`) to persist state per conversation thread
* How to resume a conversation using the same `thread_id`

Keywords: LangGraph, persistent memory, checkpointing, stateful workflows, resume conversation, chat history

## Overview of the approach

1. Define a TypedDict for the shared conversation state.
2. Create a node that reads the latest message, produces a reply, and updates state.
3. Build and compile a `StateGraph`, attaching a checkpointer.
4. Invoke the graph with a `thread_id` to save state.
5. Re-invoke with the same `thread_id` to resume the conversation.
6. Inspect saved state via `get_state`.

## Step 0 — Required packages and imports

```python theme={null}
