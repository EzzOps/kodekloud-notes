# python
# Step 1: Define state schema
from typing import TypedDict
from langgraph.graph import StateGraph
import uuid

class GraphState(TypedDict):
    messages: list[str]

# Step 2: Generate a unique session ID
session_id = str(uuid.uuid4())

# Step 3: Build and compile the graph
builder = StateGraph(GraphState)
# builder.add_node(...), add edges, etc.
graph_app = builder.compile()

# Step 4: Pass session ID as thread_id for isolation
config = {"configurable": {"thread_id": session_id}}

# Step 5: Run graph with session-specific execution
graph_app.invoke({"messages": []}, config=config)
```

This UUID identifies a single user session or workflow instance. LangGraph will keep execution history, checkpoints, and runtime state scoped to that `thread_id`, ensuring runs remain isolated from each other.

Session awareness is critical: without it, workflows can mix state, produce incorrect outputs, corrupt history, and become hard to resume or debug.

> **lightbulb** Use a session-aware execution model: tie every graph run to a unique `thread_id`, and include that identifier in logs, traces, and checkpoint keys so workflows are traceable and resumable.

<Frame>
  <img alt="The image contrasts the risks of not using unique session management, such as state leakage and inability to resume flows, with the benefits of session-based execution, including logging progress and supporting multi-tenant environments." />
</Frame>

This approach enables per-session logging, safe checkpoint storage, and large-scale concurrent execution — essential for multi-user or multi-tenant systems that require reliability, repeatability, and auditability.

Imagine a customer support bot serving thousands of users. Each user may follow different conversation paths and pause or resume later. Assign a unique thread ID per user so each conversation run stays isolated, auditable, and resumable despite a shared graph definition.

<Frame>
  <img alt="The image compares use cases of a customer support bot with and without unique session handling, highlighting problems like state leakage and data collisions without unique sessions, and benefits like isolated sessions and auditable user flows with unique sessions." />
</Frame>

Best practices for session management:

* Log the `thread_id` with every execution event, tool call, and trace.
* Avoid storing session information in global variables.
* Pass session context explicitly in graph state, or use scoped storage (databases, Redis, checkpoint stores).

<Frame>
  <img alt="The image displays three best practices related to session management: logging thread IDs, avoiding shared global session state, and passing session context via state or scoped storage." />
</Frame>

Concurrency can be implemented using multiple techniques. LangGraph does not mandate a concurrency model — it enforces per-execution isolation while allowing integration with various architectures.

| Execution Model         | Typical Use Case                                       | Notes                                                    |
| ----------------------- | ------------------------------------------------------ | -------------------------------------------------------- |
| Threads                 | Low-latency, CPU-bound tasks in a single process       | Simple to implement, requires thread-safe state handling |
| Async tasks (asyncio)   | High-concurrency I/O-bound flows (chatbots, API calls) | Efficient for many concurrent connections in one process |
| Job queues (Celery, RQ) | Background processing, retryable jobs                  | Enables horizontal scaling and failure isolation         |
| Serverless functions    | Event-driven, auto-scaled runs                         | Good for bursty traffic; requires external state stores  |

<Frame>
  <img alt="The image illustrates different concurrent execution models: Threads, Async Tasks (asyncio), Job Queues, and Serverless Functions, all leading to isolated state instances." />
</Frame>

Race conditions are a classic systems problem: when multiple executions read or write the same resource concurrently, inconsistent or corrupted data can result. Minimize shared mutable state; where sharing is unavoidable (counters, logs, shared caches), rely on the storage layer's atomic operations, transactions, or explicit locks.

> **warning** Avoid shared mutable global state. When shared resources are necessary, protect them with atomic operations, transactions, or locks to prevent race conditions and data corruption.

<Frame>
  <img alt="The image illustrates avoiding race conditions in concurrency with three panels: &#x22;Race Condition&#x22; for concurrent reads and writes, &#x22;Goal&#x22; to minimize shared mutable state, and &#x22;Solution&#x22; suggesting locks and atomic operations." />
</Frame>

For multi-tenant systems, map each `thread_id` to the user or tenant identity at the application layer so ownership and access control are clear. Because each thread maintains independent checkpoints and state, LangGraph supports personalized workflows (different tools, memory stores, or retrieval sources) while sharing the same graph definition.

Observability: tag all logs, traces, and events with the `thread_id` for each run. This links application logs, LangGraph execution state, and observability tools. Platforms such as LangSmith make it easier to inspect node execution, state transitions, and tool calls per thread, simplifying debugging and monitoring at scale.

References and further reading:

* [Kubernetes Documentation](https://kubernetes.io/docs/) — for container orchestration and scaling
* [Redis Docs](https://redis.io/docs/) — for scoped, atomic operations and locking patterns
* [LangSmith](https://learn.kodekloud.com/user/courses/langsmith) — observability integration examples

<Frame>
  <img alt="The image is a diagram explaining monitoring and observability for three users, detailing how logs, traces, and events relate to debugging, understanding workflow behavior, and tracing failures." />
</Frame>

Concurrency and execution isolation are non-negotiable for production AI agents. LangGraph provides the mechanisms to manage per-execution state, persistence, and checkpoints — but correct system design, session handling, and observability are your responsibility.

<Frame>
  <img alt="The image contains a list of four takeaways about concurrency, thread isolation, and architecture related to production agents and LangGraph tools. It emphasizes the importance of system architecture for isolation, safety, and scalability." />
</Frame>

Key takeaways:

* Assign a unique `thread_id` per graph run to isolate state and enable resumption.
* Keep session context out of global variables; prefer scoped storage or explicit state passing.
* Minimize shared mutable state; protect unavoidable shared resources using atomic ops or locks.
* Instrument all events with `thread_id` for traceability and debugging.

Following these principles lets your LangGraph system scale from prototypes to thousands of concurrent users while preserving correctness, auditability, and observability.

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/e0cd494a-00a7-4c52-88e9-b3932b03ff9f/lesson/99515dd9-9046-41d3-9a0a-9d14a007f870)


# Stateful Persistence Checkpoints

Source: https://notes.kodekloud.com/docs/LangGraph/Long-Term-Memory-and-Stateful-Persistence/Stateful-Persistence-Checkpoints/page

Describes LangGraph's checkpointing to persist workflow runtime state for pause and resume, crash recovery, backend options, security, and production best practices.

LangGraph enables agents to persist runtime state so workflows can pause and resume without losing progress. This capability is critical for real-world automation that spans hours or days, depends on external systems, or requires user input across multiple sessions.

<Frame>
  <img alt="The image explains the importance of stateful persistence, showing a robot managing state during pause and resume states with benefits like long workflows, external dependencies, and multi-session input." />
</Frame>

## What is stateful persistence?

Stateful persistence (checkpointing) saves the full runtime state of a graph—data, counters, flags, loop positions, and execution context—so an agent can be paused and later resumed from the same point. Checkpoints are durable: they live outside process memory in a database or object store, similar to saving a game's progress.

Consider a tax-filing chatbot: if the user goes idle mid-session, checkpointing ensures the assistant resumes from the exact step rather than starting over.

<Frame>
  <img alt="The image illustrates an overview of stateful persistence, showing the process of saving the state of a graph, including data, counters, flags, and loop status, into a stateful persistence vault, followed by a durable checkpoint and storage in a database and file storage." />
</Frame>

## Real-world analogy

Imagine a delivery driver, Ravi. He pauses mid-route for lunch and marks which deliveries remain. When he resumes, he continues from that checkpoint—no need to redo completed deliveries. The same concept applies to workflow checkpoints.

<Frame>
  <img alt="The image is a diagram labeled &#x22;Stateful Persistence – Overview,&#x22; showing a delivery route from an office to multiple houses, with stops for deliveries and lunch. The diagram includes a character named Ravi and a summary of delivery statuses." />
</Frame>

## Why checkpointing matters

Checkpointing enables:

* Crash recovery and process restarts without losing progress.
* Long-running workflows that span sessions or human interactions.
* Pausing while waiting for external triggers (webhooks, API calls) or user confirmations, then resuming exactly where the workflow paused.

<Frame>
  <img alt="The image illustrates &#x22;Checkpointing – Benefits&#x22; with a robot icon leading to &#x22;User Confirmation&#x22; and &#x22;API Response.&#x22;" />
</Frame>

## Quick example — enable checkpointing (in-memory)

Below is a minimal Python example showing how to enable checkpointing with an in-memory checkpointer, compile a graph with persistence, run it (which saves state keyed by a `thread_id`), and later resume with the same `thread_id`.

```python theme={null}
from langgraph.checkpoint.memory import InMemorySaver
