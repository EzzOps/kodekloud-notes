# TAVILY_API_KEY="Your Tavily API Key"  # set this in your environment if required
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# Some tool implementations accept an explicit api_key parameter; others read from env.
search = TavilySearchResults(api_key=TAVILY_API_KEY)

# Build the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Think step by step before responding."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)
```

Explanation:

* `ChatPromptTemplate.from_messages(...)` composes the prompt with system instructions, a `chat_history` placeholder, the user input placeholder (`{input}`), and the `agent_scratchpad`.
* `search` is the Tavily search tool used by the agent to retrieve web results.
* `MessagesPlaceholder` and `ChatMessageHistory` enable in-memory chat history persistence for a session.

<Callout icon="lightbulb">
  Using `MessagesPlaceholder("agent_scratchpad")` gives the agent a workspace to append intermediate reasoning and tool calls. This helps the LLM and the tool orchestrator maintain context across a single turn and between turns when history is preserved.
</Callout>

<Callout icon="warning">
  Be careful with API keys in code or logs. Prefer environment variables, secrets managers, or encrypted stores. If a tool reads the key from the environment, do not hardcode it in production.
</Callout>

## Create LLM, tools, and the message history

Create the LLM instance, assemble the tools list, and initialize an in-memory `ChatMessageHistory` for this demo.

```python theme={null}
llm = ChatOpenAI()
tools = [search]
message_history = ChatMessageHistory()
```

## Agent creation and wrapping with message history

* Use `create_tool_calling_agent` to construct a tool-calling agent with the LLM, tools, and prompt.
* Use `AgentExecutor` to manage execution and orchestrate tool calls.
* Wrap the executor with `RunnableWithMessageHistory` to provide session-aware message history retrieval.

The example below uses a simple lambda that returns the same `ChatMessageHistory` for any `session_id`. In production, map each `session_id` to its own persisted `ChatMessageHistory` (Redis, database, etc.).

```python theme={null}
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

agent1 = RunnableWithMessageHistory(
    agent_executor,
    # In real-world usage, map session_id -> ChatMessageHistory instance
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
```

## Invoking the agent (examples)

When invoking the runnable agent, pass the user input using the `input` key and include a `config` that carries a `session_id`. `RunnableWithMessageHistory` uses this `session_id` to look up and persist the chat history across calls.

Say hello to the agent:

```python theme={null}
agent1.invoke({"input": "hi!"}, config={"configurable": {"session_id": "session1"}})
```

Possible returned structure (example):

```json theme={null}
{
  "input": "hi!",
  "chat_history": [],
  "output": "Hello! How can I assist you today?"
}
```

Ask the agent a question that requires search:

```python theme={null}
response = agent1.invoke(
    {"input": "When is the ICC Men's T20 2024 World Cup scheduled?"},
    config={"configurable": {"session_id": "session1"}}
)
print(response["output"])
```

Expected (example) output:

```text theme={null}
The ICC Men's T20 World Cup 2024 is scheduled to take place from June 1 to June 29, 2024. It will feature 16 teams competing in this global cricket tournament.
```

Follow-up question that uses conversation context and search:

```python theme={null}
response = agent1.invoke(
    {"input": "Which countries are hosting?"},
    config={"configurable": {"session_id": "session1"}}
)
print(response["output"])
```

Expected (example) output:

```text theme={null}
The ICC Men's T20 World Cup 2024 will be hosted by the West Indies and the United States. The tournament venues include Antigua & Barbuda, Barbados, Guyana, Saint Lucia, St. Vincent and the Grenadines, Trinidad & Tobago, and three venues in the USA (e.g., Dallas, Florida, and New York).
```

### Example: compute days until the tournament

A follow-up that relies on context and a date calculation:

```python theme={null}
response = agent1.invoke(
    {"input": "How many days before the first match starts?"},
    config={"configurable": {"session_id": "session1"}}
)
print(response["output"])
```

You may observe the LLM returning an incorrect or imprecise numeric answer (for example, saying "17 days" when the current date or calculation is not accurate). This highlights a limitation.

<Callout icon="warning">
  LLMs are not always reliable for precise arithmetic or time-based calculations unless you explicitly delegate the calculation to a deterministic tool (like a Python REPL or a date utility). For exact answers (e.g., "days until a date"), add a deterministic tool to the agent that performs the arithmetic and returns the correct result.
</Callout>

## How the agent adds value over raw search

* A plain search tool typically returns raw documents, snippets, or URLs.
* The agent can call the search tool, aggregate results, and ask the LLM to synthesize a concise, user-friendly answer.
* With session-aware message history, follow-up questions that refer to earlier turns are handled naturally because the prompt includes previous chat and the agent scratchpad.

## Extending this agent

To make the agent more robust and capable of deterministic computation:

* Add a Python REPL or date-calculation tool so the agent can delegate numeric or date arithmetic to a deterministic environment.
* Persist `ChatMessageHistory` per `session_id` using Redis, a database, or another storage backend for production usage.
* Add more retrieval tools or structured data sources (APIs, knowledge bases) to broaden the agent's factual coverage.

## Conclusion and next steps

In this lesson we built a session-aware agent that:

* Uses a search tool (Tavily) to fetch web results.
* Uses an LLM (ChatOpenAI) to synthesize and present answers.
* Persists message history via `RunnableWithMessageHistory`.
* Uses an `agent_scratchpad` in the prompt to manage intermediate reasoning and tool calls.

Next steps:

* Add a deterministic tool (Python REPL or date calculator) to handle precise calculations.
* Implement a per-session persistent store for chat history (e.g., Redis).
* Explore multi-tool orchestration and richer prompts to improve answer reliability.

## Links and references

* [LangChain Python Docs](https://python.langchain.com/en/latest/)
* [Tavily — community tool integrations](/) (check the relevant tool implementation in your SDK)
* [OpenAI API and Chat Models](https://platform.openai.com/docs/models)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-8948-4806-8824-19eb10923d1d/lesson/cb8e55e0-21b4-4980-8418-ece887303e7a" />
</CardGroup>


# What are Agents

Source: https://notes.kodekloud.com/docs/LangChain/Building-Agents/What-are-Agents/page

Explains how LangChain agents combine LLMs, memory, tools, and RAG to orchestrate multi-step reliable workflows that mitigate LLM limitations like hallucinations and lack of internet

Welcome back to the final lesson in the "Building Agents" series.

In this lesson we combine prompt engineering, memory, tools, and Retrieval-Augmented Generation (RAG) to build a practical agent. We'll explain why agents are useful, how they address common LLM limitations, and show the typical architecture and operational flow you'll implement with LangChain.

<Callout icon="lightbulb">
  This lesson ties together previous concepts: prompt engineering, memory systems, tool integration, and RAG. If you followed earlier lessons, you’ll recognize the building blocks used here to create reliable, multi-step agents.
</Callout>

<Frame>
  <img alt="The image lists four prerequisites: Prompt Engineering, Adding Memory, Using Tools, and Performing Retrieval Augmented Generation (RAG)." />
</Frame>

## Key observations about large language models (LLMs)

* Stateless by default: a single API call does not persist knowledge across sessions unless you provide history or attach memory.
* Sub-symbolic: LLMs learn statistical patterns in text and don't perform symbolic reasoning unless guided.
* Variable reasoning ability: models like [GPT-4](https://platform.openai.com/docs/models/gpt-4) often show strong reasoning, while smaller models may struggle.
* Hallucination risk: LLMs can invent facts when asked about topics outside their knowledge or training data.
* No native internet access: LLMs are limited by training cutoffs unless you add retrieval or browsing tools.
* Limited precision for math: complex calculations can be incorrect without an external tool.
* Non-deterministic outputs: repeated prompts can produce different results without strict formatting and output parsing.

<Callout icon="warning">
  LLMs can hallucinate and produce incorrect or outdated facts. Use retrieval (RAG), authoritative tools, and output validation to ground model outputs before acting on them.
</Callout>

## How we address these limitations

Use of modular components—memory, retrieval, tools, and output parsers—lets agents mitigate typical LLM weaknesses. The following table maps common LLM issues to the practical solutions agents provide:

| LLM limitation                   |                                     Agent solution | Typical LangChain module or approach            |
| -------------------------------- | -------------------------------------------------: | ----------------------------------------------- |
| Statelessness                    |   Persist history with short- and long-term memory | Message history, memory modules                 |
| Hallucination / Knowledge cutoff |               Ground responses via retrieval (RAG) | Vector DBs, retrievers, RAG pipelines           |
| Poor math / precise computation  |                    Delegate to deterministic tools | Python REPL tool, calculators                   |
| Non-deterministic output         |                  Enforce formats and parse outputs | Output parsers, strict prompt templates         |
| No internet access               |               Invoke search/browsing tools or APIs | Web search, browsing tools, custom API tools    |
| Complex reasoning                | Decompose using chain-of-thought or ReAct patterns | Chains, scratchpad, stepwise reasoning patterns |

LangChain provides ready-made primitives to implement each of these solutions, and agents orchestrate them into a cohesive workflow.

## What are LangChain agents?

Agents in LangChain are orchestrators that combine an LLM “brain” with external capabilities: tools (search, APIs, Python REPL), memory stores (short- and long-term), retrieval systems (for RAG), and structured prompting. Instead of wiring many primitives together manually, an agent coordinates thinking (LLM reasoning) and acting (tool execution), reducing development time and complexity.

<Frame>
  <img alt="The image illustrates the role of agents in technology, highlighting their ability to bring modules together, increase efficiency compared to writing code, reduce time and complexity, and connect the dots." />
</Frame>

## Agents bring flexibility and scale

Agents can be adapted to many domains — healthcare, customer service, education, travel, scheduling, and more. By orchestrating a sequence of reasoning steps, tool calls, and stored context, agents usually provide a better user experience than a single LLM reply.

<Frame>
  <img alt="The image illustrates the roles of agents in three areas: healthcare, customer service, and educational guidance, each represented with corresponding icons." />
</Frame>

Agents also allow human-in-the-loop workflows for verification or approvals and ensure the model has appropriate context and instructions before outputting a final answer.

## How agents address LLM limitations (detailed)

* Statelessness: Agents attach message history and memory stores under the hood so past interactions inform current decisions.
* Synchronous APIs: Agents can manage background or multi-step workflows that appear asynchronous from the user’s perspective (e.g., spawn a long-running task and report back).
* Reasoning: Agents support chain-of-thought style decomposition and stepwise approaches so the LLM reasons with intermediate context.
* Hallucination: Agents ground answers by retrieving authoritative documents or calling APIs.
* Internet access: Agents invoke browsing/search and other external APIs to get up-to-date information.
* Math: Agents call a Python tool or calculator for precise computations.
* Structured outputs: Agents enforce JSON, XML, CSV, or markdown using output parsers and strict prompt templates.

<Frame>
  <img alt="The image compares how agents enhance user experience by providing long-term memory, working asynchronously, making LLMs more intelligent, and supplying data and context, against the limitations of LLMs such as being stateless, synchronous, and lacking internet access." />
</Frame>

## Typical agent architecture

At a high level:

* User sends a query to the agent.
* The agent uses an LLM as the reasoning core.
* The agent has access to tools (Wikipedia/search, custom APIs, Python interpreter), memory stores, a scratchpad for intermediate reasoning, and advanced prompting strategies (chain-of-thought, ReAct).
* The agent automates tool selection and prompt engineering to fulfill the user’s request.

<Frame>
  <img alt="The image is a flowchart illustrating a process involving a user interacting with agents, which access various resources like Wikipedia, custom functions, memory, and a Python interpreter, leading to an LLM (Large Language Model)." />
</Frame>

## How an agent operates — step-by-step

1. User sends a query to the agent.
2. Agent prompts the LLM to determine what additional information or actions are required.
3. LLM identifies needed data points or sub-steps (A, B, C).
4. Agent maps those needs to tools and executes them (search, API call, Python computation); results are passed back to the LLM.
5. LLM updates its plan or requests more resources; the agent repeats tool use and reasoning until completion.
6. Agent assembles a structured response and returns it to the user.

This interleaving of LLM reasoning and deterministic actions allows agents to complete multi-step tasks that a single model call could not reliably accomplish.

<Frame>
  <img alt="The image illustrates a flowchart of how agents work, depicting a user sending a query to agents, which then query a large language model (LLM) that requires specific data points to respond." />
</Frame>

## Example interaction

* LLM requests data point A → agent runs a web search tool and returns results.
* LLM requests data point B → agent queries Wikipedia and returns results.
* LLM combines both results, optionally calls a Python tool for calculations, formats the final output, and returns it to the user.

Agents coordinate tool calls and LLM reasoning iteratively until the user’s objective is achieved.

<Frame>
  <img alt="The image illustrates the process of how agents work, showing a user querying agents, which then query a large language model (LLM), with a speech bubble highlighting a question about data points." />
</Frame>

## Representative agent use cases

| Use case                    | Description                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| Customer support automation | Handle multi-turn troubleshooting, fetch knowledge-base articles, and escalate when needed |
| Student tutoring            | Break down problems, retrieve references, and show worked solutions step-by-step           |
| Travel planning             | Compare flights/hotels, build itineraries, and book reservations via APIs                  |
| Meeting scheduling          | Read calendar availability and manage invites across providers                             |
| Domain-specific agents      | Integrate internal APIs and private data sources for tailored workflows                    |

Agents automate complex, multi-step tasks by combining LLM reasoning with deterministic tools and data.

<Frame>
  <img alt="The image illustrates two aspects of agent work: &#x22;Customer Service and Counseling&#x22; represented by a headset icon, and &#x22;Academic Guidance&#x22; depicted with a graduation cap and diploma icon." />
</Frame>

## Wrap-up

Agents are orchestrators: they combine LLMs, tools, memory, and prompt engineering into robust, reliable workflows. In this lesson you learned:

* Why agents are necessary and what problems they solve.
* How agents improve LLM reliability using memory, tools, and RAG.
* Typical architecture and the step-by-step agent runtime loop.
* Example scenarios and concrete use cases.

This lesson will be followed by demos that build end-to-end agents so you can see these concepts in action and apply them to real projects.

## Links and references

* [LangChain](https://langchain.com)
* Retrieval-Augmented Generation (RAG): [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
* ReAct (Reason+Act): [https://arxiv.org/abs/2210.03307](https://arxiv.org/abs/2210.03307)
* [GPT-4 model details](https://platform.openai.com/docs/models/gpt-4)
* [Python](https://www.python.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-8948-4806-8824-19eb10923d1d/lesson/6321298e-ef4e-4acd-b383-4745a68eee9c" />
</CardGroup>
