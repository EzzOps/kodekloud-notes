# Enable LangSmith tracing for all LangGraph runs
enable_tracing()
```

When tracing is enabled, LangGraph opens a trace session for each run and captures events like node execution, model calls, tool invocations, state updates, and timings. All captured data is sent to LangSmith and stored as an execution trace for later inspection.

> **lightbulb** Initialize tracing before your graph executes. Tracing begins only after `enable_tracing()` is called, so place it at the top of your script, app startup, or notebook cell that runs prior to graph execution.

LangGraph’s tracing is non-invasive: you do not need to modify node functions or change workflow logic. The framework records execution details without altering runtime behavior.

<Frame>
  <img alt="The image outlines what LangSmith automatically tracks, highlighting features like automatic tracking, non-invasive operation, and important placement. Each feature is accompanied by a brief description." />
</Frame>

What LangSmith records (at a glance)

| Layer             | What is captured                          | Why it matters                                |
| ----------------- | ----------------------------------------- | --------------------------------------------- |
| Execution path    | Sequence of nodes executed in the graph   | See exactly which branches ran and why        |
| Model/Chain calls | Model inputs, outputs, prompt versions    | Reproduce responses and audit prompts         |
| Tool usage        | Tool names, arguments, results, API calls | Debug external integrations and failures      |
| Agent decisions   | Intermediate reasoning steps              | Understand decision points and logic flow     |
| Performance       | Latency and per-step timings              | Identify bottlenecks and optimize performance |
| Errors            | Full tracebacks and failure context       | Faster root-cause analysis                    |

In local testing, prints and logs can sometimes be enough. But production workflows typically have branching logic, external calls, stateful memory, and unpredictable user inputs. Two runs with similar inputs may take different execution paths; traces let you compare runs side-by-side.

<Frame>
  <img alt="The image contrasts a simple and insufficient testing approach with the complex and demanding realities of production, highlighting the challenges of debugging in a production environment due to multiple conditional paths, real user input, and memory updates." />
</Frame>

Key investigation tools in LangSmith

| Feature                 | How it helps                                                       |
| ----------------------- | ------------------------------------------------------------------ |
| Visual node traces      | See the path the graph took visually and quickly identify branches |
| Step-by-step breakdowns | Inspect inputs/outputs for each node and tool call                 |
| Prompt version history  | Audit which prompt template or version was used for a given run    |
| Session replay          | Replay previous runs to understand behavior over time              |
| Detailed error context  | View full tracebacks and surrounding state to accelerate fixes     |

<Frame>
  <img alt="The image lists key observability features in LangSmith, including visual node traces, step-by-step breakdowns, prompt version history, session replay, and error context. Each feature includes a short description of its function." />
</Frame>

Best practices for production observability

* Enable tracing for development and staging to detect regressions early.
* Use session tags (user IDs, agent names, experiment IDs) to filter and group traces.
* Attach custom metadata (prompt version, model version, memory size) to correlate configuration with behavior.
* Review traces for subtle issues (unexpected outputs, memory mis-recall), not just explicit errors.
* Configure dashboards and alerts to surface critical signals like latency spikes or recurring failures.

<Frame>
  <img alt="The image presents four best practices for tracing in software environments, including enabling tracing in development and staging, using session tags, logging custom metadata, and reviewing traces for unexpected outputs." />
</Frame>

LangSmith gives you a visual trace of LangGraph execution: which nodes ran, what each step did, and how long each took. If a run fails, inspect the full error context; if it’s slow, identify the slow step. This shifts debugging from speculative to diagnostic.

<Frame>
  <img alt="The image illustrates a &#x22;LangSmith Trace&#x22; analysis with a visual execution flow diagram, highlighting error analysis and performance bottlenecks. It shows a step-by-step process with time durations and emphasizes the importance of transforming debugging from guesswork into diagnosis." />
</Frame>

Troubleshooting and validation use cases

* Answering tough questions: When two similar inputs yield different outputs, traces reveal which nodes executed, the exact prompts sent, and any memory or state accessed.
* Validating changes: After modifying prompts, reducers, or memory logic, use traces to confirm the new behavior before releasing to users.
* Performance tuning: Identify slow tools or model calls and prioritize optimizations based on per-step timings.

<Frame>
  <img alt="The image lists use cases for observability, categorized into &#x22;Answering Tough Questions&#x22; and &#x22;Validating New Changes,&#x22; with specific scenarios for each category." />
</Frame>

Operationalizing observability

* Enrich traces with metadata (user IDs, input types, version tags) for easier filtering and correlation.
* Add monitoring, dashboards, and alerts to detect important signals automatically (latency spikes, frequent retries, long execution chains).
* After updates (prompts, reducers, memory), inspect sample traces across key flows to ensure expected behavior.

<Frame>
  <img alt="The image outlines &#x22;Operational Observability Practices&#x22; with sections on enriching traces with metadata, configuring monitoring and alerts, and reviewing key flows post-update, each with specific steps and diagrams." />
</Frame>

LangGraph enables powerful, stateful agent workflows—and that power brings complexity. As graphs grow, tracing becomes essential to understand actual execution, debug failures, and validate changes. Observability tools like LangSmith help teams build AI systems that are more robust, explainable, and maintainable.

> **warning** Be mindful of sensitive data. Traces can capture user inputs and API responses—sanitize or redact personally identifiable information (PII) and secrets before storing or sharing traces.

For engineers building production agents, LangSmith becomes an essential part of the monitoring and debugging toolkit—turning opaque agent runs into inspectable, repeatable traces.

Links and references

* [LangGraph course on KodeKloud](https://learn.kodekloud.com/user/courses/langgraph)
* [LangChain course on KodeKloud](https://learn.kodekloud.com/user/courses/langchain)
* [LangChain documentation](https://langchain.readthedocs.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/e0cd494a-00a7-4c52-88e9-b3932b03ff9f/lesson/32b29c2b-a9e8-427d-94d5-cded50b77f6a)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/langgraph/module/e0cd494a-00a7-4c52-88e9-b3932b03ff9f/lesson/f8153413-b11a-4e16-9ff0-bfe795bfe05e)


# Leveraging the LangGraph Store

Source: https://notes.kodekloud.com/docs/LangGraph/Long-Term-Memory-and-Stateful-Persistence/Leveraging-the-LangGraph-Store/page

Explains LangGraph's persistent store and checkpointing for agent workflows, enabling durable state, pause and resume, observability, and scalable backend options for production deployments.

The LangGraph store is a built-in persistent storage layer for agent workflows. Instead of creating a custom database or ad-hoc memory system, developers can use LangGraph's storage interface and checkpointing to remember information across runs, share data between concurrent users, and support long-running or interruptible processes.

When combined with checkpointing, the store enables safe pause/resume semantics and recovery from failures — making LangGraph suitable for production deployments where agents manage complex logic, human-in-the-loop events, or multi-step tasks.

Think of the LangGraph store like Ravi’s smart clipboard: it remembers every delivery route, stops made, remaining items, and notes — all in one place. The store holds long-term memories, message history, logs, and per-user context that workflows and agents can read and update over time.

<Frame>
  <img alt="The image is an overview diagram of the LangGraph Store, which is described as a system for managing and persisting graph data. It highlights features like handling state saving, loading, versioning, and concurrent user interactions." />
</Frame>

Key benefits

* Durable conversation and state: agents can maintain knowledge across sessions and users.
* Safe recovery: checkpoint snapshots let workflows resume after failures or interruptions.
* Shared state for scale: multiple workers or services can query and rehydrate the same execution state.
* Observability: checkpoint histories enable auditing, debugging, and reproducibility.

The store works together with LangGraph’s checkpointing system to capture snapshots of the graph state during execution — enabling pause, resume, or recovery. This lets developers query past interactions and track how state changes over time.

<Frame>
  <img alt="The image is a flowchart illustrating the key responsibilities of the LangGraph Store, including memory management, message history, logs and audit trails, and checkpoints." />
</Frame>

Persistence model — three layers

Use the table below to quickly understand how persistence maps to LangGraph workflows.

| Layer                       | What it contains                                                                               | Purpose                                                           |
| --------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Graph state                 | In-memory working state while a graph runs (user inputs, intermediate results, retrieved info) | Short-lived runtime data used by active executions                |
| Runs & checkpoints          | Snapshots saved during execution to pause/resume or recover workflows                          | Durable checkpoints enabling resume, replay, and debugging        |
| Persistent application data | Logs, aggregated summaries, long-term memory stored outside immediate graph state              | Historical records, audit trails, and user-level long-term memory |

These layers together support versioning, debugging, safe recovery, and state migration for long-running agent executions.

Example: persisting LangGraph execution

This concise Python example shows enabling checkpointing with a SQLite checkpointer. It defines an application state schema, creates the checkpointer, compiles a StateGraph with the checkpointer, and invokes the graph using a `thread_id` that becomes the persistent execution identity.

```python theme={null}
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SQLiteSaver
