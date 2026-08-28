# Example: Chat prompt template with system and human messages
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

sys_msg = "You are a {subject} teacher"
human_msg = "Tell me about {concept}"

prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(sys_msg),
        HumanMessagePromptTemplate.from_template(human_msg),
    ]
)

prompt = prompt_template.format_messages(subject="Chemistry", concept="Periodic Table")
# You can pass `prompt` to a chat model, e.g.:
# model = ChatOpenAI(temperature=0)
# response = model.generate(prompt)
```

Practical exercises and APIs
All hands‑on exercises are included in the course notebooks and managed via KodeKloud. To run them locally, supply your own API keys for OpenAI and any other third-party services used in the labs.

```python theme={null}
import os

# Set your API key as an environment variable before running notebooks
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
```

<Callout icon="warning">
  Never commit or share your secret keys. Use environment variables or secret management tools when running notebooks or deploying applications.
</Callout>

Course outcomes
When you finish this course you will be able to:

* Design prompt templates and chains that combine multiple LLM calls
* Implement memory and stateful interactions for multi-turn apps
* Use tools and agents to interact with APIs and external systems
* Parse and validate model outputs for downstream processing

Resources and references

* [LangChain Documentation](https://langchain.readthedocs.io/)
* [OpenAI API Documentation](https://platform.openai.com/docs)
* [KodeKloud Community](https://kodekloud.com/community)

Modules overview

| Module         | Primary focus                    | Example topics                             |
| -------------- | -------------------------------- | ------------------------------------------ |
| Model          | Choosing and using LLMs          | Chat models, temperature, streaming        |
| Input          | Prompts and prompt templates     | System/Human messages, LCEL                |
| Output         | Parsing & validating outputs     | Output parsers, structured responses       |
| Chains         | Composing multi-step flows       | Sequential, conditional, map-reduce chains |
| Memory         | Stateful interactions            | Conversation memory, vector stores         |
| Tools & Agents | External actions & orchestration | API calls, web search, tool selection      |

<Callout icon="lightbulb">
  Tip: Follow along with the demos in the provided notebooks and run the practical exercises to reinforce each concept. Use the KodeKloud community forum for questions and peer help.
</Callout>

Let's jump in and start building modern LLM applications with LangChain.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/d5e8b9a9-2511-4d5a-881b-aeeedeb44a4d/lesson/282a2855-f9c4-4bf3-a3ed-2a3a8d2762a1" />
</CardGroup>


# Building Blocks of LangChain

Source: https://notes.kodekloud.com/docs/LangChain/Key-Components-of-LangChain/Building-Blocks-of-LangChain/page

Overview of LangChain's core components and how they integrate LLMs, embeddings, vector stores, prompts, chains, memory, retrieval, and agents to build modular AI applications.

This article examines the core building blocks of LangChain and how they fit into real-world applications. At a high level, LangChain acts as middleware between your application and external services—language models (LLMs), embedding models, vector databases, and other data sources. It provides abstractions to compose prompts, preserve state, retrieve relevant context, and orchestrate complex behaviors.

Below is the big-picture overview of the components that live inside the LangChain layer.

<Frame>
  <img alt="The image illustrates the building blocks of LangChain, including elements like Model I/O, Memory, Retrieval, and Agents, which are integrated into an application. It also highlights components such as Language Models, Vector Databases, Embeddings, and External Data." />
</Frame>

Summary table — quick reference

| Building Block                | Purpose                                                                                  | Typical components / examples                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Model I/O (LLMs & Embeddings) | Interface with LLMs for generation and with embedding models for vector representations. | `OpenAI` wrappers, alternative LLM providers, embedding models, tokenizers, streaming support |
| Prompts                       | Structured templates and utilities for consistent prompt construction.                   | `PromptTemplate` classes, formatting helpers, few-shot/example injection                      |
| Chains                        | Composable workflows chaining model calls, tools, and logic.                             | Sequential chains, branching/control-flow chains, orchestration helpers                       |
| Memory                        | Maintain conversational or task state across interactions.                               | In-memory buffers, session stores, persistent key-value stores                                |
| Retrieval                     | Retrieve relevant documents or facts to augment prompts (RAG).                           | Vector stores (FAISS, Weaviate, Pinecone), retriever abstractions, indexing utilities         |
| Agents & Tools                | Let models choose tools or actions to perform external tasks.                            | Tool wrappers, ReAct-style controllers, safety/authorization layers                           |

The sections below expand each building block in the order you’ll typically encounter them when designing a LangChain system.

1. Model I/O (LLMs and Embeddings)

* What it is: Wrappers and interfaces for language models (text generation/completion) and embedding models (vector encodings).
* Role: Provide natural language generation, completions, and semantic embeddings used for tasks like RAG (retrieval-augmented generation) and similarity search.
* Typical components:
  * LLM provider wrappers (e.g., `OpenAI`, other hosted or self-hosted models)
  * Embedding APIs and models
  * Tokenizer utilities and streaming output handling
  * Provider-specific configuration (temperature, max tokens, batching)

2. Prompts (Prompt Templates and Formatting)

* What it is: Structured templates and utilities for building repeatable prompts.
* Role: Encapsulate prompt patterns, inject variables safely, and enable prompt engineering best practices (reusability, testability).
* Typical components:
  * `PromptTemplate` classes and formatters
  * Few-shot/example injection helpers and conditioning utilities
  * Prompt validation and safety checks

3. Chains (Composable Workflows)

* What it is: Sequences or graphs that compose multiple steps—model calls, retrievals, tool invocations, and business logic.
* Role: Turn atomic operations into higher-level pipelines (e.g., user question → retrieve docs → summarize → respond).
* Typical components:
  * Simple sequential chains for linear workflows
  * Branching/conditional chains for decision points
  * Orchestration utilities for error handling, retries, and parallelism

4. Memory (State and Context Management)

* What it is: Mechanisms for persisting conversational or application state between calls to the model.
* Role: Maintain context across multi-turn interactions so LLMs can reference prior exchanges, user preferences, or saved facts.
* Typical components:
  * In-memory buffers for short-lived sessions
  * Session-based memory for per-user conversations
  * Persistent integrations (databases, key-value stores) for long-term memory

5. Retrieval (Indexes and Vector Stores)

* What it is: Retrieval systems that provide relevant context—often powered by embeddings and vector similarity search.
* Role: Ground model outputs with external data by augmenting prompts with relevant documents or knowledge snippets (RAG).
* Typical components:
  * Vector stores and indexers: FAISS, Weaviate, Pinecone, etc.
  * Retriever interfaces and similarity search utilities
  * Document loaders and preprocessing/indexing pipelines

6. Agents and Tools (Decision-Making & External Actions)

* What it is: Agent frameworks enabling models to select and call external tools or APIs.
* Role: Let models do more than generate text—search, interact with APIs, run code, or perform automated workflows based on model reasoning.
* Typical components:
  * Tool wrappers (custom actions, API clients)
  * Agent controllers and reasoning patterns (e.g., ReAct)
  * Safety, authorization, and sandboxing layers to limit agent actions

<Callout icon="lightbulb">
  These building blocks are designed to be combined into complete applications. A common flow is: create embeddings (Model I/O) → index documents (Retrieval) → compose a retrieval-augmented prompt (Prompts + Chains) → maintain conversation history (Memory) → hand off to an agent when external actions are required.
</Callout>

Why this decomposition matters

* Modularity: Each block can be replaced or upgraded independently (swap vector DB, change LLM provider).
* Testability: Smaller, focused components are easier to unit test and validate.
* Maintainability: Clear separation of responsibilities helps manage complexity as features grow.
* Reusability: Standardized prompts, chains, and tools accelerate building new capabilities.

Links and references

* LangChain documentation: [https://python.langchain.com/](https://python.langchain.com/)
* Retrieval & Vector DBs: FAISS ([https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)), Weaviate ([https://www.semi.technology/](https://www.semi.technology/)), Pinecone ([https://www.pinecone.io/](https://www.pinecone.io/))
* OpenAI: [https://platform.openai.com/](https://platform.openai.com/)

Understanding these components sets the stage for practical patterns and code examples. Later sections will deep-dive into each building block with concrete integrations, sample code, and design patterns for production systems.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langchain/module/5bedac05-3eaa-4d0d-9892-e05b80c528fb/lesson/ccb34a44-28e4-478d-ae1a-13df8ef583c4" />
</CardGroup>
