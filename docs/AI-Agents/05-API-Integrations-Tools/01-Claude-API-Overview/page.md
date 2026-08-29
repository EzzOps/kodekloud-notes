# Example: activate your virtualenv (update path if your venv is elsewhere)
source /root/venv/bin/activate && python /root/code/verify_environment.py
```

> **lightbulb** Make sure your virtual environment is activated before running verification or lab scripts. If you created the venv in a different path, update the `source` command to point to your activate script.

Tools, libraries, and resources

* LangChain — orchestration of prompts and chains
* ChromaDB / Chroma — lightweight vector database options
* sentence-transformers — high-quality embedding models
* numpy — numerical operations for preprocessing
* Additional tooling: Docker, cloud object stores, monitoring/observability tools (for advanced labs)

Vector databases and semantic search
Vector databases let you store and query embeddings so retrieval is based on semantic similarity instead of keyword matches. In this course you’ll create a semantic search engine for technical documentation, then use embeddings to retrieve relevant passages for downstream tasks.

<Frame>
  <img alt="A screenshot of an &#x22;Environment Setup&#x22; slide showing a checklist of vector search libraries and models to be installed (e.g., sentence-transformers, langchain, chromadb, numpy). A small circular video inset of a speaker appears in the bottom-right corner." />
</Frame>

Key steps in a semantic search pipeline

1. Ingest documents (split into passages / chunks).
2. Compute embeddings with a suitable encoder (e.g., sentence-transformers).
3. Store embeddings in a vector store (ChromaDB, FAISS, Milvus, etc.).
4. Query by embedding for nearest neighbors, then re-rank or filter before use.

Retrieval-Augmented Generation (RAG)
RAG pipelines first retrieve relevant context and then condition a generative model on that context. This reduces hallucination and improves factuality by grounding the model’s responses in retrieved documents.

Common RAG flow:

* User query → embedding → nearest-neighbor documents → concat or summarization → conditioned generation

<Frame>
  <img alt="A split-screen image: the left side shows a slide titled &#x22;AI Fundamentals&#x22; with bullet points about making AI API calls, LangChain, semantic search, RAG, and building AI agents. On the right a bearded man wearing glasses and a &#x22;KodeKloud&#x22; shirt speaks into a microphone." />
</Frame>

Verifying package installation (sample pip output)
When installing Python packages you may see output confirming dependencies are already satisfied in your virtual environment. Example pip output:

```console theme={null}
Requirement already satisfied: watchfiles>=0.13 in ./venv/lib/python3.12/site-packages (1.1.0)
Requirement already satisfied: websockets>=10.4 in ./venv/lib/python3.12/site-packages (15.0.1)
Requirement already satisfied: humanfriendly>=9.1 in ./venv/lib/python3.12/site-packages (10.0)
Requirement already satisfied: MarkupSafe>=2.0 in ./venv/lib/python3.12/site-packages (3.0.3)
Requirement already satisfied: oauthlib>=3.0.0 in ./venv/lib/python3.12/site-packages (3.3.1)
Requirement already satisfied: joblib>=1.2.0 in ./venv/lib/python3.12/site-packages (1.5.2)
Requirement already satisfied: threadpoolctl>=3.1.0 in ./venv/lib/python3.12/site-packages (3.6.0)
```

Then run the verification script:

```bash theme={null}
python3 /root/code/verify_environment.py
```

Building stateful agents with a graph-based approach
Graph-based workflows allow agents to maintain state across steps, support structured messaging, and enable multi-step reasoning. These primitives are useful when agents must remember past interactions, update state, and decide next actions conditionally.

Example: imports and a simple message field (excerpt)

```python theme={null}
# /root/code/task_1_understanding_imports.py (excerpt)
from langgraph.graph import StateGraph, END
from typing import TypedDict

# Example field that will hold messages in this workflow
messages: list
```

Run the import verification and view the script:

```bash theme={null}
python3 /root/code/task_1_understanding_imports.py
```

Advanced topics and production considerations
In advanced labs you will:

* Integrate external tools (APIs, databases, search) into graph workflows.
* Add observability and logging for debugging and auditing agent behavior.
* Apply safety patterns and guardrails (rate limits, input sanitization, rejection sampling).
* Compose multi-step flows and orchestrate complex agent behavior suitable for production.

Links and references

* LangChain: [https://docs.langchain.com/](https://docs.langchain.com/)
* Chroma (ChromaDB): [https://www.trychroma.com/](https://www.trychroma.com/)
* sentence-transformers: [https://www.sbert.net/](https://www.sbert.net/)
* Retrieval-Augmented Generation (overview): [https://en.wikipedia.org/wiki/Retrieval-Augmented\_Generation](https://en.wikipedia.org/wiki/Retrieval-Augmented_Generation)

Conclusion
This course equips you to go from a single API call to complete, stateful AI agents that perform semantic retrieval, grounded generation, and multi-step reasoning. Follow the hands-on labs to verify your environment, build a semantic search index, implement RAG pipelines, and design graph-based agents that persist state and make informed decisions.

Whether you are starting out or deepening your skills, the practical examples and lab exercises will help you build and deploy robust AI-driven applications.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/b76cbd0c-cb08-464d-aba4-6fae38fe7019/lesson/92aff189-412f-4ad9-907b-90518807160d)


# Claude API Overview

Source: https://notes.kodekloud.com/docs/AI-Agents/API-Integrations-Tools/Claude-API-Overview/page

Overview of Anthropic's Claude API, its design, models, message-based interface, tools, file handling, and agent best practices.

Welcome back.

This lesson provides a structured overview of Claude: its design philosophy, common use cases, the Claude Messages API and key endpoints, message roles and prompt structuring, tool/function calling, agent capabilities, code and file handling features, model variants, rate limits and pricing considerations, and best practices for integrating Claude into agent systems.

<Frame>
  <img alt="The image shows a section of an agenda outlining four topics: Claude's capabilities in agent systems, Claude Code Interpreter and file handling, rate limits, pricing, model differences, and best practices for Claude API usage." />
</Frame>

Overview: Claude in context

Claude is a production-grade, safety-first large language model from Anthropic that focuses on steerability, alignment, and reliable multi-turn behavior. Its API is designed to integrate with agent pipelines and conversational applications — supporting long-context reasoning, structured tool use, and file interactions that are essential for automation and developer workflows.

<Frame>
  <img alt="The image is an infographic titled &#x22;Why Learning Claude API Is Valuable?&#x22; It lists benefits including unlocking advanced reasoning, supporting multi-turn dialogue, ensuring safe AI responses, and easy integration with custom tools." />
</Frame>

Key strengths and agent capabilities

Claude excels in nuanced instruction-following, long-document understanding, and multi-step reasoning. These capabilities make it a strong choice for agents that must read large documents, summarize complex reports, execute multi-stage tasks, or work with external tools and APIs. Claude’s design emphasizes safety and alignment, so it is well-suited for higher-stakes or regulated environments.

<Frame>
  <img alt="The image illustrates Claude's capabilities in agent systems, highlighting aspects such as handling long prompts, natural language understanding, tool use via API, context retention, and safety with moderation features." />
</Frame>

Background and alignment

Claude is Anthropic’s flagship conversational and assistive AI model, named after Claude Shannon in homage to information theory and structured reasoning. It is trained with techniques that emphasize safety and self-consistency, notably Constitutional AI, which helps the model critique and refine its outputs against a set of guiding principles.

<Frame>
  <img alt="The image describes &#x22;Claude&#x22; as Anthropic's flagship AI model for conversational tasks, named after Claude Shannon. It includes an illustration of a robot interacting with a person through a phone." />
</Frame>

Design philosophy and common use cases

Claude is engineered to be helpful, honest, and harmless. Its strengths include steerability (prompt-driven behavior control), debuggability (more traceable reasoning), and robust instruction-following — useful for applications like document parsing, coding assistance, conversational agents, and autonomous agent workflows.

<Frame>
  <img alt="The image outlines Claude's design philosophy and use cases, highlighting three key aspects: steerability, debuggability, and instruction-following." />
</Frame>

Examples of practical applications

* Document parsing and extraction (financial reports, contracts)
* Pair programming and code review automation
* Long-form summarization and multi-turn conversational assistants
* Agent pipelines that perform planning, tool execution, and verification

<Frame>
  <img alt="The image presents &#x22;Claude’s Design Philosophy and Use Cases,&#x22; highlighting examples such as document analysis, coding assistants, and multi-turn conversations." />
</Frame>

Models and the message-based API

Anthropic exposes several Claude model families (for example, Opus, Sonnet, and Haiku). Claude’s API is message-first: you send a sequence of messages (system, user, assistant) and receive assistant responses. This mirrors chat-style interactions and maps cleanly to agent workflows where context and roles are important.

<Frame>
  <img alt="The image is an overview of the Claude API, highlighting a message-based interface with an illustration of a person and a robot interacting. The key endpoint is shown as &#x22;POST /v1/messages&#x22;." />
</Frame>

Primary endpoint

The main HTTP endpoint for the message-based API is:

* POST `/v1/messages`

This endpoint accepts system-level instructions, user prompts, and optional tool or file references. It supports streaming responses and is designed for multi-turn, stateful interactions.

Example: calling the Claude Messages API

Below is a minimal Python example demonstrating the message format used by the Messages API via a direct HTTP call. Replace `ANTHROPIC_API_KEY` with your key or use your preferred SDK for additional features like retries and streaming.

```python theme={null}
