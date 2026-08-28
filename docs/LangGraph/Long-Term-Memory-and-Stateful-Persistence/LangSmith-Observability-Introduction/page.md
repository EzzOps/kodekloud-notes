# imports
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage
```

## Step 1 — Define the conversation state

The graph's state is the shared memory between nodes. Keep it minimal for this demo: a `messages` list holding `HumanMessage` and `AIMessage` objects.

```python theme={null}
class ChatState(TypedDict):
    messages: list
```

## Step 2 — Create the chatbot node

This node inspects the latest message in `state["messages"]`, forms a reply (simulated here), appends the reply to the history, and returns the updated state.

```python theme={null}
def chatbot_node(state: ChatState) -> ChatState:
    history = list(state.get("messages", []))
    if not history:
        # No messages yet; nothing to respond to
        return {"messages": history}

    last_message = history[-1]

    if isinstance(last_message, HumanMessage):
        user_text = last_message.content
    else:
        user_text = str(last_message)

    reply = AIMessage(
        content=f"I remember our conversation. You just said: '{user_text}'"
    )

    return {"messages": history + [reply]}
```

## Step 3 — Build and compile the graph with a checkpointer

Create a `StateGraph`, register the node, set entry/finish points, and compile the graph while attaching an `InMemorySaver` checkpointer. The checkpointer persists the graph state after each invocation under a thread identifier.

```python theme={null}
builder = StateGraph(ChatState)
builder.add_node("chatbot", chatbot_node)
builder.set_entry_point("chatbot")
builder.set_finish_point("chatbot")

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

## Step 4 — Start the first session (create a thread)

Use a `config` including a `thread_id` to uniquely identify this conversation. Invoke the graph with an initial `HumanMessage`. The graph processes input, appends a reply, and the checkpointer saves the resulting state under `thread_id`.

```python theme={null}
config = {"configurable": {"thread_id": "user_123"}}

result_1 = graph.invoke(
    {"messages": [HumanMessage(content="I am planning a trip to Rome next month.")]},
    config=config,
)

for msg in result_1["messages"]:
    print(type(msg).__name__, ":", msg.content)
```

## Step 5 — Simulate the user returning later (resume the thread)

When the user returns, invoke the graph again with the same `thread_id`. LangGraph will load the previously saved state automatically so the assistant "remembers" the prior conversation history.

```python theme={null}
result_2 = graph.invoke(
    {
        "messages": result_1["messages"] + [
            HumanMessage(content="Can you remind me what I told you earlier?")
        ]
    },
    config=config,
)

for msg in result_2["messages"]:
    print(type(msg).__name__, ":", msg.content)
```

Expected console output (example):

```text theme={null}
HumanMessage : I am planning a trip to Rome next month.
AIMessage : I remember our conversation. You just said: 'I am planning a trip to Rome next month.'
HumanMessage : Can you remind me what I told you earlier?
AIMessage : I remember our conversation. You just said: 'Can you remind me what I told you earlier?'
```

## Step 6 — Inspect the saved state

You can verify persistence by calling `get_state` with the same `config` (same `thread_id`). The saved state will include the full conversation history.

```python theme={null}
saved_state = graph.get_state(config)

for i, msg in enumerate(saved_state["messages"], start=1):
    print(f"{i}. {type(msg).__name__}: {msg.content}")
```

This confirms the system stored and restored the conversation memory.

<Callout icon="warning">
  Avoid using `InMemorySaver` for production: in-memory checkpointers do not survive process restarts or multi-instance deployments. Always choose a durable backing store (see examples below).
</Callout>

<Callout icon="lightbulb">
  In this lesson we used an in-memory checkpointer for simplicity. For production deployments, replace `InMemorySaver` with a durable checkpoint implementation so conversations persist across restarts and multiple instances.
</Callout>

## Checkpointer options and recommendations

Use a durable store for production — here are common choices:

| Storage Type   | Use Case                                        | Typical implementation                    |
| -------------- | ----------------------------------------------- | ----------------------------------------- |
| Redis          | Fast in-memory with persistence and clustering  | `Redis`-backed checkpointer               |
| Postgres       | Durable relational storage with ACID guarantees | `Postgres`-backed checkpointer            |
| Object storage | Long-term archival for large histories          | `S3` / object storage-backed checkpointer |

For links and references:

* [Redis](https://redis.io/)
* [Postgres](https://www.postgresql.org/)
* [AWS S3](https://aws.amazon.com/s3/)

## Wrap-up

Persistent memory is essential for realistic conversational AI. LangGraph implements this via stateful workflows plus checkpointing:

* Nodes read and update a shared state,
* The checkpointer persists that state under a conversation identifier (e.g., `thread_id`),
* Later invocations with the same identifier restore the saved state so the assistant resumes the conversation seamlessly.

This pattern — shared state, checkpoint after each invocation, and restore by conversation identifier — forms the foundation for assistants that maintain continuity across sessions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/e0cd494a-00a7-4c52-88e9-b3932b03ff9f/lesson/5d61391b-1eed-4ca1-9333-2ef0a43d6d7b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/langgraph/module/e0cd494a-00a7-4c52-88e9-b3932b03ff9f/lesson/7caa0f21-eaee-4ff3-9f8c-291e75424b05" />
</CardGroup>


# LangSmith Observability Introduction

Source: https://notes.kodekloud.com/docs/LangGraph/Long-Term-Memory-and-Stateful-Persistence/LangSmith-Observability-Introduction/page

Introduction to LangSmith observability showing how execution traces in LangGraph and LangChain record prompts, tool calls, state changes, errors, and performance for debugging

When you deploy AI agents in production, observability becomes critical. Without visibility into internal execution—what nodes ran, which prompts were used, what inputs were processed, and how state changed—debugging is nearly impossible. LangSmith provides observability tools built specifically for large language model (LLM) applications to make these internals visible and actionable.

LangSmith is an observability platform created by the [LangChain](https://learn.kodekloud.com/user/courses/langchain) team for monitoring, debugging, and improving systems built with frameworks like [LangChain](https://learn.kodekloud.com/user/courses/langchain) and [LangGraph](https://learn.kodekloud.com/user/courses/langgraph). Its core concept is the execution trace: every run of your application is recorded in full. Traces capture model inputs and outputs, prompt versions, tool calls, errors, latency, and workflow state changes so you can inspect exactly how an agent behaved.

<Frame>
  <img alt="The image is an overview of LangSmith, a platform for applications built with LangChain and LangGraph, featuring a central &#x22;Execution Trace&#x22; surrounded by factors like Prompt Versions, Inputs, Outputs, Errors, Latency, and State Transitions." />
</Frame>

You can trace each step of a workflow to find where errors occurred, examine which prompts and tools contributed to a result, and analyze execution latency. Practically, LangSmith acts like mission control for LLM applications, giving developers complete visibility into agent internals.

Every time an agent runs, multiple components interact: models receive inputs, prompts are constructed and versioned, tools may be called, graph state can change, and the model generates outputs. Complex agent systems may perform thousands of decisions and interactions in a single run. Without observability, this all looks like a black box—you only see the final response.

<Frame>
  <img alt="The image titled &#x22;LangSmith – Overview&#x22; shows a robot with data charts on screens, accompanied by a text bubble explaining that LangSmith records traces whenever an agent runs." />
</Frame>

LangSmith records an execution trace whenever your agent runs. A trace is a detailed timeline describing:

* Model inputs and outputs
* Tool calls and external API interactions
* Node execution sequence and state transitions
* Latency measurements and timing per step
* Errors and full tracebacks
* Prompt versions used during the run

Inspecting traces lets you see the exact prompt that was sent, which tool was invoked, how state evolved, and where failures or slowdowns occurred—turning guesswork into diagnosis.

Robby used to just deliver packages. Now his clipboard tracks every step — which doors he knocked on, what he said, and where he had issues. LangSmith is that clipboard, but for your graph.

[LangGraph](https://learn.kodekloud.com/user/courses/langgraph) integrates natively with LangSmith, so enabling tracing usually requires only a few lines of configuration. Once enabled, detailed traces are automatically sent to LangSmith for every LangGraph run.

<Frame>
  <img alt="The image shows a concept of &#x22;LangGraph Integration&#x22; with a person sitting at a desk, coding on a laptop, and integration lines connecting &#x22;LangGraph&#x22; to &#x22;LangSmith.&#x22; It suggests enabling tracing in code." />
</Frame>

Traces include per-step details (inputs, outputs, tool calls, node transitions, latency) and can be enriched with custom metadata such as session IDs, user IDs, or experiment tags. This metadata helps correlate user activity and configuration with system behavior—critical for robust debugging and production monitoring.

Getting started with LangSmith tracing is simple. Add the tracing initialization early in your application:

```python theme={null}
from langgraph.tracing.langsmith import enable_tracing
