# The Actor Review of LangChain Primitives

Source: https://notes.kodekloud.com/docs/LangGraph/The-Core-Workflow-Nodes-Edges-and-Routing/The-Actor-Review-of-LangChain-Primitives/page

Review of LangChain primitives and how LangGraph composes LLMChains tools agents and memory into orchestrated graph nodes and workflows

Before diving into graphs, revisit the core primitives of [LangChain](https://learn.kodekloud.com/user/courses/langchain). LangGraph builds directly on those primitives: it does not replace them, it orchestrates them. Every node in LangGraph executes a LangChain component (an LLM chain, a tool, a retriever, or an agent). If you don't understand what LangChain components can do, you won't be able to design effective nodes or graphs.

<Callout icon="lightbulb">
  LangGraph composes and routes primitive components. Design the components first (LLM chains, tools, agents, memory) and then use LangGraph to connect and orchestrate them.
</Callout>

<Frame>
  <img alt="The image is a flowchart titled &#x22;Why Revisit LangChain Primitives?&#x22; showing connections between elements like LLM Chain, Tool, Retriever, Agent, and a central &#x22;LangGraph&#x22; node, which represents nodes running LangChain components." />
</Frame>

This lesson reviews the "actors" of your graph-based system — the primitives that perform actions. Understanding them is essential to building expressive, maintainable, and testable LangGraph graphs. The core LangChain primitives are:

* LLMChain: a prompt template paired with an LLM; returns generated text for inputs.
* Tools: Python functions (or connectors) wrapped with metadata so agents or orchestrators can call them safely.
* Agents: decision-makers that inspect inputs, choose tools/LLMChains, and orchestrate steps.
* Memory: state that preserves prior messages or facts to support multi-step interactions.

<Frame>
  <img alt="The image is an infographic titled &#x22;What Are LangChain Primitives?&#x22; and it explains four components: LLMChain, Tools, Agents, and Memory, each with a brief description." />
</Frame>

Quick reference: primitives summary

|  Primitive | Purpose                                              | Typical Use Cases                                              |
| ---------: | ---------------------------------------------------- | -------------------------------------------------------------- |
| `LLMChain` | Prompt + model wrapper that maps inputs → outputs    | Summarization, rewrite, classification, intermediate reasoning |
|     `Tool` | External function or connector exposed with metadata | Search, math evaluation, API calls, DB/file I/O                |
|    `Agent` | Controller that selects tools/steps dynamically      | Open-ended tasks, iterative planning, tool orchestration       |
|   `Memory` | Stores conversation or task state across calls       | Multi-turn chat, user profiles, retrieval-augmented context    |

Below we break each primitive down and explain how it maps into LangGraph nodes, with short examples and recommended patterns.

## LLMChain

The LLMChain is the foundation for most language-centric flows. It wraps a prompt template and an LLM, accepts inputs, and returns generated outputs. In LangGraph, an LLMChain typically becomes a node that you call whenever language generation is needed.

Key properties:

* Stateless by default: processes inputs and returns outputs without persistent state.
* Can be paired with Memory when you need context across invocations.
* Typical uses: summarization, rephrasing, query rewrite, content generation, prompt-based classification, and intermediate reasoning steps.

Small example (conceptual Python using LangChain-style API):

```python theme={null}
from langchain import LLMChain, PromptTemplate, OpenAI

prompt = PromptTemplate.from_template("Summarize this text: {text}")
chain = LLMChain(llm=OpenAI(model="gpt-4"), prompt=prompt)

result = chain.run({"text": "Long article content..."})
```

In LangGraph: wrap this `LLMChain` into a node that accepts `text` and outputs `summary`. Add Memory to the node only when the model must refer to prior exchanges.

<Frame>
  <img alt="The image illustrates an LLM Chain as a basic node, featuring a &#x22;Prompt&#x22; and a &#x22;Language Model (LLM)&#x22; in a diagram." />
</Frame>

## Tools

Tools expose external functionality (search, compute, REST calls, DB access) to agents or to deterministic nodes. Conceptually they are Python functions enriched with metadata (name, description, arg schema) so orchestration layers and agents can call them safely and explainably.

Common tool types:

* `SearchTool`: queries a search index or engine.
* `MathTool`: evaluates expressions.
* `APITool`: calls REST APIs.
* DB connectors, file readers, and other I/O utilities.

How to use tools in LangGraph:

* Call tools directly from nodes when the workflow is deterministic.
* Let an agent pick the appropriate tool dynamically for open-ended tasks.
* Route execution conditionally based on tool outputs.

Example tool definition (conceptual):

```python theme={null}
def weather_api(city: str) -> dict:
    # call external API and return parsed JSON
    ...

tool = Tool.from_function(weather_api, name="get_weather", description="Get weather for a city")
```

In LangGraph, attach tools to nodes or make them discoverable to agent nodes. Define clear input/output schemas so downstream nodes can validate responses.

<Frame>
  <img alt="The image illustrates how tools wrap Python functions and metadata to enable interactions between a system and the outside world. It visually depicts a flow from a system to tools and then to the outside world." />
</Frame>

Common tool usage patterns in LangGraph:

<Frame>
  <img alt="The image is an informational graphic explaining how to use LangGraph tools, featuring three options: calling tools directly from nodes, using agents to select tools, and routing based on tool output." />
</Frame>

## Agents

Agents are higher-order actors that make decisions: they inspect inputs, select tools or LLMChains, and orchestrate multi-step strategies to reach a goal. In LangChain, agents often run loops (think of a planner that uses tools iteratively). In LangGraph, agents can either be single nodes encapsulating that logic, or you can implement agent-like behavior explicitly with multiple nodes and edges (intent classification → tool selection → iterative steps).

When to use an agent vs. explicit routing:

* Use an agent when the task is open-ended, requires dynamic tool selection, or benefits from iterative reasoning.
* Use explicit nodes and edges when the control flow is well-known and you need stronger observability, reproducibility, and testability.

Design tip: if you expect nondeterministic tool choice or need the model to plan steps, agent nodes are appropriate. If you need reproducible pipelines with clear logs and tests, prefer explicit nodes and explicit routing.

## Memory

Memory provides context across node invocations—storing conversation history, user state, or facts for retrieval-augmented flows. Add Memory to an LLMChain or agent when the model must consider prior interactions.

Common memory patterns:

* Short-term conversational memory (recent messages window).
* Long-term memory for user profiles or persistent facts.
* Retrieval-augmented memory that uses a vector database to fetch relevant past context.

Example sketch:

```python theme={null}
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(k=10)  # keep last 10 messages
chain = LLMChain(llm=OpenAI(), prompt=some_prompt, memory=memory)
```

Use retrieval-augmented memory when you need scalable long-term context (see resources on Vector Databases for GenAI).

## Putting it together

Every LangGraph node maps to one of these primitives or a small composition of them. Design the primitives deliberately to make graphs easier to build and maintain.

Recommended design workflow:

1. Define prompts and LLMChains for core transformations.
2. Implement tools with clear schemas for inputs/outputs.
3. Decide where agents are necessary versus explicit routing via edges.
4. Add memory selectively where context continuity is required.
5. Compose nodes into LangGraph graphs, using edges for routing, retries, and conditional logic.

With well-defined primitives, LangGraph becomes a powerful coordinator: it composes nodes into graphs, routes execution by design, integrates tools and state, and helps you solve complex tasks reliably.

<Callout icon="warning">
  Agents can execute tools that have side effects (API calls, DB writes). Always model and test tool behavior, and apply safety checks or sandboxing where necessary.
</Callout>

Links and references

* [LangChain course (KodeKloud)](https://learn.kodekloud.com/user/courses/langchain)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Vector Database for GenAI (KodeKloud)](https://learn.kodekloud.com/user/courses/vector-database-for-genai)
* [Fundamentals of RAG (KodeKloud)](https://learn.kodekloud.com/user/courses/fundamentals-of-rag)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/2e37c751-0429-43c9-8ecf-2df222ce0663/lesson/ea1e518a-33cd-4753-8635-5852a265b51b" />
</CardGroup>
