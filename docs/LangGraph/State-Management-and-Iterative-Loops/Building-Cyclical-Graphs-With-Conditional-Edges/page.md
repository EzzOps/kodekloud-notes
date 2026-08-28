# Create a checkpointer and compile the graph with persistence enabled
checkpointer = InMemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Use a thread_id to associate a session with its persisted state
config = {"configurable": {"thread_id": "session-123"}}

# First run: state is automatically checkpointed after each step
result = app.invoke(inputs, config=config)
print("First run result:", result)

# Later: resume using the same thread id and new inputs
resumed_result = app.invoke(new_inputs, config=config)
print("Resumed graph result:", resumed_result)
```

<Callout icon="lightbulb">
  Pick a `thread_id` that uniquely represents the user session or workflow instance. Treat thread IDs like session tokens and protect them with the same care as authentication credentials.
</Callout>

## Production backends and trade-offs

In production, checkpoint storage should be durable and secure. LangGraph supports pluggable checkpointers and common backends:

| Backend              | Best for                                  | Notes / Example                                                           |
| -------------------- | ----------------------------------------- | ------------------------------------------------------------------------- |
| Redis                | Real-time session storage, low-latency    | Very fast; good for ephemeral sessions and quick resume.                  |
| Cloud object storage | Long-term durable storage                 | Use `S3` or equivalent for archived or infrequently accessed checkpoints. |
| Databases            | Auditing, analytics, enterprise workflows | Relational or document DBs can store metadata and support queries.        |
| Custom checkpointers | Integrate with existing infrastructure    | Implement serialization and storage to match your requirements.           |

Be mindful of checkpoint frequency—excessively frequent saves increase overhead. Save at meaningful boundaries: task completion, decision points, or when waiting for user input.

<Frame>
  <img alt="The image illustrates how LangGraph handles persistence, showing a process where a state is bookmarked for later resumption, even after walking away, closing a tab, or shutting down." />
</Frame>

## Common production use cases

* Asynchronous tasks: checkpoint before sending a message or webhook; resume when a callback arrives.
* Human-in-the-loop flows: pause while awaiting user verification and continue once confirmed.
* Crash recovery: reload the most recent checkpoint after an infrastructure failure.

Table: Example use cases and where checkpointing helps

| Use Case                 | When to checkpoint              | Benefit                                        |
| ------------------------ | ------------------------------- | ---------------------------------------------- |
| Webhook-driven process   | Before sending external request | Resume on callback without redoing prior steps |
| Multi-step approval      | After each approval stage       | Continue approval chain across sessions        |
| Long-running computation | At checkpoints between stages   | Recover progress if the process is interrupted |

When a graph is compiled with a checkpointer, LangGraph automatically stores the workflow state after each step, associating it with the configured `thread_id`. To resume, run the graph again with the same `thread_id` and the runtime will restore the last saved state and continue execution.

```python theme={null}
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

# Compile graph with persistence enabled
app = graph.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "user_123"}}

# Run graph - state is automatically checkpointed
app.invoke(state, config=config)

# Later: resume without losing progress
result = app.invoke(new_inputs, config=config)
print("Resumed graph result:", result)
```

<Frame>
  <img alt="The image illustrates a process titled &#x22;Saving a Checkpoint&#x22; for a system named LangGraph, involving serialization, storage, and versioning. It also suggests configuring the checkpointer and using a thread_id to resume." />
</Frame>

## Security & reliability considerations

Production checkpointing systems commonly include:

* Encryption and hashing of persisted states.
* Audit logs and metadata (timestamps, session IDs).
* Versioning and schema evolution support to maintain compatibility.

<Frame>
  <img alt="The image outlines methods for saving a checkpoint in high-availability systems, including encrypting/hashing the state, logging for audit trails, and tagging the state with metadata. It highlights that this method provides a foundation for long-term and persistent AI workflows." />
</Frame>

<Callout icon="warning">
  Persisted state can contain sensitive data (PII, API keys, tokens). Always encrypt persisted checkpoints, restrict access with IAM, and maintain audit trails to meet compliance and security requirements.
</Callout>

## Resuming execution

When resuming, LangGraph:

1. Loads the latest checkpoint associated with the `thread_id`.
2. Reconstructs the runtime graph, including the last executed node and execution context.
3. Continues execution from that saved point.

Because the checkpoint stores both state data and execution context, resuming is deterministic and reliable.

<Frame>
  <img alt="The image outlines a process for &#x22;Resuming Execution&#x22; in a system called LangGraph, detailing steps like loading checkpoints and reconstructing runtime graphs, and explaining why this process works." />
</Frame>

Resume patterns:

<Frame>
  <img alt="The image outlines three methods of resuming execution: user-driven continuation, multi-turn workflows, and external triggers, each with a brief description." />
</Frame>

* User-driven continuation: pause to ask clarifying questions and resume after a response.
* Multi-turn workflows: staged approvals or document reviews across sessions.
* External triggers: webhooks, scheduled jobs, or callbacks resume the workflow.

## Best practices

* Save checkpoints at meaningful boundaries (decision points, task completions).
* Choose a persistence backend aligned with latency, durability, and cost needs.
* Encrypt persisted data and maintain access logs.
* Treat checkpoint storage as critical infrastructure—implement monitoring, backups, and recovery plans.

<Frame>
  <img alt="The image showcases three best practices: strategic timing, data protection, and critical infrastructure, each represented by a colored icon and brief description." />
</Frame>

## Key takeaways

* Checkpointing makes LangGraph agents robust to crashes and restarts.
* Persistence allows workflows to span multiple sessions and actors.
* Checkpoints preserve both workflow state and execution context, enabling precise resumption.
* Design checkpointing with security, durability, and operational controls in mind.

<Frame>
  <img alt="The image lists four key takeaways about persistence in LangGraph agents, highlighting their robustness, session-spanning ability, workflow enablement, and reliability foundation." />
</Frame>

## References

* Redis: [https://redis.io/](https://redis.io/)
* AWS S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-00a7-4c52-88e9-b3932b03ff9f/lesson/61700334-8d53-4e7a-b8a3-23360d19e653" />
</CardGroup>


# Building Cyclical Graphs With Conditional Edges

Source: https://notes.kodekloud.com/docs/LangGraph/State-Management-and-Iterative-Loops/Building-Cyclical-Graphs-With-Conditional-Edges/page

Shows building a LangGraph workflow that uses conditional edges to route between search and direct answer paths, integrate web search and LLMs, and converge results into a final formatter.

In this lesson we show how to build a small, agentic workflow using LangGraph's conditional edges to route between execution paths. The demo is intentionally compact: based on the user's question, the graph will either perform a live web search via Tavily or answer immediately using an LLM. Both routes converge into a final formatting step. You can also generate a visual representation (Mermaid) of the graph to inspect routing and convergence.

Key concepts covered:

* State-driven routing using conditional edges
* Composable nodes that read/write shared typed state
* Converging branches into a single terminal formatter
* Integrating external APIs (OpenAI Responses API and Tavily search)

***

## Setup and imports

Install dependencies if needed (uncomment the pip line in a fresh environment), then initialize clients and environment variables.

```python theme={null}
