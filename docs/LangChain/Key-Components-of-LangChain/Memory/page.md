# Pseudo-code (conceptual)
prompt = PromptTemplate("Summarize the text: {text}")
llm_output = LLM.call(prompt.format(text=article))
structured = OutputParser.parse(llm_output)
return structured
```

* Retrieval-augmented generation (RAG) with a retriever and combiner

```python theme={null}
# Pseudo-code (conceptual)
query = "What does the user ask about X?"
docs = Retriever.search(query, top_k=5)        # fetch relevant documents
context = Combiner.combine(docs)               # combine/truncate for context window
response = LLM.call(prompt_with_context(query, context))
return OutputParser.parse(response)
```

* Parallel retrieval and aggregation

```python theme={null}
# Pseudo-code (conceptual)
results = parallel_run([RetrieverA.search(q), RetrieverB.search(q)])
merged = deduplicate_and_rank(results)
answer = LLM.call(prompt_with_context(q, merged[:10]))
```

Best practices

* Keep chains modular: encapsulate repeatable logic in sub-chains and reuse them as building blocks.
* Validate outputs: use output parsers or schema validators early when the downstream system expects structured data.
* Control context size: when combining many documents or tool outputs, apply truncation or scoring to fit the model's context window.
* Monitor latency and cost: parallel steps can increase responsiveness but may also raise cost; balance concurrency with budget and SLAs.
* Version and test sub-chains: since chains are composable, maintaining tests for each sub-chain prevents regression when reusing them.

<Callout icon="lightbulb">
  Chains provide a modular way to build complex pipelines by combining prompts, models, retrieval, parsing, and functions into reusable units.
</Callout>

Chains are a foundational capability in LangChain. For implementation details and API-specific examples, see the official LangChain documentation: [LangChain — Chains](https://langchain.readthedocs.io/) and related guides for retrieval, memory, and output parsers.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-3eaa-4d0d-9892-e05b80c528fb/lesson/79d145d4-21fc-49e3-af36-4616e469466f" />
</CardGroup>


# Memory

Source: https://notes.kodekloud.com/docs/LangChain/Key-Components-of-LangChain/Memory/page

Explains how LLMs are stateless and how LangChain adds short term and long term memory layers to persist and retrieve conversation context across sessions

In this lesson we explain how large language models (LLMs) handle memory, why they are effectively stateless, and how LangChain adds short-term and long-term memory layers so your application can "remember" across requests and sessions.

Key points:

* LLMs are stateless: each API call is independent and only has access to the prompt/context you send in that call.
* To make an LLM behave as if it remembers prior turns, you must include the relevant history in the prompt.
* LangChain provides memory components that automate collecting, persisting, and retrieving conversation context.

## Short-term vs Long-term memory

| Memory Type       | Purpose                                                               | Typical Storage                                                  | When to use                                                      |
| ----------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| Short-term memory | Maintain immediate conversational context within a session            | In-memory buffers (session/process)                              | Chat sessions, transient context, turn-by-turn conversation      |
| Long-term memory  | Persist facts, user profiles, or conversation history across sessions | External stores: `SQLite`, `Redis`, flat files, or vector stores | User preferences, searchable historical context, knowledge bases |

Short-term memory makes the model appear to remember during a single session by re-injecting prior messages into the prompt. Long-term memory persists important facts externally and retrieves only the most relevant items when composing a new prompt so the LLM can leverage past information without exceeding context limits.

## How LangChain implements memory

LangChain provides several built-in memory implementations:

* Conversation buffers: keep a running transcript.
* Summary memory: compress older context into a summary.
* Windowed buffers: keep only the latest N turns.
* Integrations with external stores: allow you to persist to databases or vector stores for retrieval later.

These abstractions let you focus on what to store, what to retrieve, and when to surface it to the LLM.

<Frame>
  <img alt="The image shows a diagram illustrating a memory system involving a user, memory, a language model, and connections to external databases like SQLite, Redis, and text files." />
</Frame>

## Example: short-term conversational memory with LangChain

The following shows a simple in-memory conversational setup using LangChain's `ConversationBufferMemory`. This keeps conversation context for the lifetime of the process/session.

```python theme={null}
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
