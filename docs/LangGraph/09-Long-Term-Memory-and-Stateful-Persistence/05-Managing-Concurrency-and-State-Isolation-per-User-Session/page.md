# Define state schema
class AppState(TypedDict):
    messages: list[str]

# Create persistent checkpointer (stores checkpoints to a durable backend)
checkpointer = SQLiteSaver.from_conn_string("graph.db")

# Build and compile the graph
builder = StateGraph(AppState)
# builder.add_node(...), add edges, etc.
app = builder.compile(checkpointer=checkpointer)

# Run graph with persistent thread state
config = {"configurable": {"thread_id": "user_456"}}

result = app.invoke({"messages": ["Hi!"]}, config=config)

print(result)
```

> **lightbulb** Using the same `thread_id` on subsequent invokes lets LangGraph load the latest checkpoint for that session and resume from the stored state.

As the graph runs, LangGraph will save checkpoints automatically to supported backends (for example, SQLite or Redis). These checkpoints act as recoverable snapshots so workflows can continue later by reconnecting to the same checkpointer and invoking the graph again with the same `thread_id`.

Resuming a workflow

To continue a paused workflow (for instance after an external event or a user returns), reconnect to the same checkpointer and invoke the graph with the same execution identifier. The graph definition must match the original compilation so that rehydration reconstructs the expected state.

```python theme={null}
from langgraph.checkpoint.sqlite import SQLiteSaver
from langgraph.graph import StateGraph

# Reconnect to existing checkpoint database
checkpointer = SQLiteSaver.from_conn_string("graph.db")

# Rebuild graph (must match the original graph definition)
builder = StateGraph(AppState)
app = builder.compile(checkpointer=checkpointer)

# Same thread_id resumes the previous conversation
config = {"configurable": {"thread_id": "user_456"}}

result = app.invoke({"messages": ["Continue our conversation"]}, config=config)

print(result)
```

> **warning** Ensure the compiled graph's structure and state schema match the original run. Mismatched graph definitions can cause rehydration errors or inconsistent state.

Why checkpointing matters

Checkpointing unlocks production capabilities that are hard to achieve with ephemeral, single-run agents:

* Asynchronous assistance: pause workflows while waiting for user replies, external APIs, or human actions, and resume hours later without losing context.
* Diagnostics and auditing: checkpoints record how state changed, aiding root-cause analysis and compliance.
* State migration: transfer stored state between services or instances during redeployments or scaling.
* Reproducibility: replay saved checkpoints to test fixes, validate new logic, or compare behaviors.

<Frame>
  <img alt="The image is a diagram explaining the use of a checkpoint for persistent execution in modern AI systems, highlighting aspects like multiple users interacting simultaneously, long or delayed tasks, and error recovery." />
</Frame>

Checkpointer responsibilities

A checkpointer implements three essential roles:

* Storage: persist the graph state to a durable backend (SQLite, Redis, or other stores).
* Querying: enable inspection and analysis of previous executions and how state changed over time.
* Rehydration: reconstruct the graph state from a saved checkpoint so execution continues from where it left off.

<Frame>
  <img alt="The image is a diagram titled &#x22;Using a Checkpointer for Persistent Execution,&#x22; illustrating three components: Storage, Querying, and Rehydration, connected to the concept of Persistent Execution." />
</Frame>

Practical production use cases

Checkpointing and the LangGraph store enable real-world agent features such as:

* Long-running assistants preserving user-specific context across days or weeks.
* Workflows that wait for external tools, human approvals, or offline events.
* Auditable executions for support, compliance, and post-mortem investigations.
* Scalable distributed deployments where state must be shared, migrated, or sharded.

<Frame>
  <img alt="The image shows a circular diagram with four colorful puzzle pieces labeled with use cases: reproducibility, state migration, asynchronous assistants, and support diagnostics. Each section is associated with a representative icon." />
</Frame>

Best practices for production

* Log `thread_id` with user identifiers and relevant metadata for traceability and debugging.
* Combine checkpoints with tracing tools (e.g., distributed tracing) to visualize model calls, tool invocations, and graph transitions.
* Validate critical state fields and implement alerts if values are missing or malformed to avoid silent failures.
* Keep checkpoint retention and archival policies aligned with compliance and cost requirements.

<Frame>
  <img alt="The image presents best practices for logging, tracing, and alerts, focusing on &#x22;Log Linking,&#x22; &#x22;Pair Loading & Tracing,&#x22; and &#x22;Automate Alerts,&#x22; with mention of a &#x22;LangGraph&#x22; system." />
</Frame>

Backend flexibility

LangGraph’s checkpointing is pluggable — choose the backend that fits your environment:

| Backend         | When to use                                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| `SQLite`        | Local development, prototypes, or small deployments where installing additional infra is undesirable |
| `Redis`         | Distributed systems needing low-latency shared state across multiple workers                         |
| Custom adapters | Enterprise databases, audit systems, or specialized storage for compliance and scalability needs     |

LangGraph supports custom adapters so the same workflow can run locally during development and scale to a robust backend in production.

<Frame>
  <img alt="The image illustrates backend flexibility with various storage options such as Redis, SQLite, and custom storage, highlighting their pluggable and customizable features. It shows how these components can be integrated and customized within a system." />
</Frame>

Observability and debugging

Checkpoints provide a temporal record of state evolution. Combine checkpoint histories with tracing and logging to:

* Inspect how decisions were made by the agent.
* Replay executions to reproduce and fix issues.
* Correlate model outputs and external tool calls with state changes.

These observability capabilities are essential to improving reliability and validating production agents.

Summary

Persistence — via the LangGraph store and checkpointing — is a foundational capability for production-grade agents. By separating durable state management from the agent logic, and pairing checkpointing with observability tools, developers can:

* Build assistants that keep context across sessions.
* Implement long-running, interruptible workflows.
* Reproduce and audit executions for compliance and debugging.
* Scale from local development to distributed production deployments.

Links and references

* [SQLite](https://www.sqlite.org)
* [Redis](https://redis.io)
* [LangGraph repository and docs](/)

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/e0cd494a-00a7-4c52-88e9-b3932b03ff9f/lesson/55b77569-eff2-40c3-859a-a5e5de30cbd9)


# Managing Concurrency and State Isolation per User Session

Source: https://notes.kodekloud.com/docs/LangGraph/Long-Term-Memory-and-Stateful-Persistence/Managing-Concurrency-and-State-Isolation-per-User-Session/page

Guidance on isolating per-user LangGraph executions using unique session identifiers, session-aware state, checkpointing, and concurrency best practices for scalable, auditable multi-tenant systems

In production you typically serve hundreds or thousands of users with a single LangGraph application. Each user session must be isolated so one user's data, progress, or memory never leaks into another's flow — e.g., you would not want Ravi's shopping cart to appear in someone else's checkout.

<Frame>
  <img alt="The image illustrates the importance of concurrency and isolation using a diagram of a concurrency engine distributing tasks to multiple users, each within their isolated lanes." />
</Frame>

Concurrency management means safely running many graph executions in parallel: chatbot sessions, workflows, or event-triggered runs. Each graph run must keep its own runtime state, memory, and execution history. LangGraph exposes isolated runtime state, but your application must wire up session tracking, persistence, and identifiers correctly.

<Frame>
  <img alt="The image is a diagram illustrating concurrency in LangGraph, showing session tracking, control flow, chatbot sessions, workflow flow, event triggers, and memory & state management." />
</Frame>

Conceptually, think of each user as a delivery agent with a unique route, tools, and checklist. They never share bags or notes. To enforce isolation, assign a unique session identifier to each user flow and tie every piece of graph state to that ID — whether state lives in-process, Redis, or a database. Avoid shared mutable objects unless they are intentionally protected; state collisions are a silent and costly failure mode.

<Frame>
  <img alt="The image illustrates the concept of state isolation per session, showing best practices with unique session IDs for isolation and the risks of collision when shared sessions without unique keys are used, leading to potential failures." />
</Frame>

When hundreds or thousands of graph executions run concurrently, each must maintain its own execution context (current node, history, checkpoints) so workflows do not interfere. Typically this is done by generating a unique session or thread identifier for every graph invocation. The graph definition can be shared; runtime state must be stored and queried per-session.

Unpacking a common scenario: a chatbot platform or a data pipeline serving many users concurrently. Although all users reference the same graph definition, each user requires an independent execution context: progress, messages, and intermediate results must be isolated. LangGraph supports this by associating runtime state with a session-specific identifier.

<Frame>
  <img alt="The image illustrates session management by showing isolated graph instances for two users, A and B, with data and thread isolation to prevent data mixing in a system platform." />
</Frame>

Execution threads must remain separate. Each graph run tracks its own execution history and current node. Passing a unique identifier lets the system determine which state belongs to which user and enables safe checkpointing, resumption, and tracing.

Example: minimal pattern for session isolation in LangGraph. Create a small typed state, generate a UUID for the session, compile the graph, and invoke it with the session identifier as the runtime `thread_id`.

```python theme={null}
