# After intent classification
state["intent"] = "weather_query"

# After invoking a weather tool
state["tool_results"] = {"openweather": {"temp_f": 55, "condition": "Rain"}}

# Compose final response and increment loop counter
state["final_response"] = "Expect rain tomorrow with a high near 55°F."
state["loop_count"] = state.get("loop_count", 0) + 1
```

> **lightbulb** Design your schema to be permissive early (optional fields) and grow it intentionally as new nodes or tools are added. This balances development speed with safety and observability.

Practical considerations and best practices

* Define the schema early in the project to reduce ambiguity and accidental overwrites.
* Treat the schema as a living contract: extend it when you add tools, nodes, or new observability needs.
* Use loop counters and explicit success/error flags to make iterative or cyclical graphs safe and auditable.
* Prefer clear, well-documented keys over deep opaque blobs—this improves explainability and cross-team collaboration.
* Leverage static analysis (`mypy`) and runtime checks in critical nodes to catch unexpected types or missing keys early.

When to update the schema

* When you add new nodes or tool integrations that need new fields.
* When data flows change, require additional metadata, or new observability signals.
* As part of routine maintenance: keep the schema aligned with runtime telemetry and logs.

<Frame>
  <img alt="The image lists three situations for updating a schema: when adding new nodes or tools, when data flow changes or expands, and to keep it a living structure." />
</Frame>

Conclusion
A clear graph state schema is the foundation of robust LangGraph workflows. It ensures consistency, transparency, and safety while speeding up debugging and cross-team collaboration. Define the schema early, document it, and evolve it deliberately as your system grows—just like Robbie refining his delivery journal as routes become more complex.

<Frame>
  <img alt="The image contains a layout with takeaways on schema design, emphasizing foundations, consistency, early definition, and evolution as complexity grows. It features numbered points and a dark sidebar labeled &#x22;Takeaways.&#x22;" />
</Frame>

Further reading and references

* Python `TypedDict` docs: [https://docs.python.org/3/library/typing.html#typing.TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)
* PEP 655 (optional keys): [https://peps.python.org/pep-0655/](https://peps.python.org/pep-0655/)
* mypy static type checker: [https://mypy-lang.org/](https://mypy-lang.org/)
* LangChain message types: [https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/)

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/7a80b285-b366-4c4d-95d0-bce0c24aaf58/lesson/da3e22f3-9144-425a-bc83-4715c077857c)


# Understanding State Accumulation and Data Flow

Source: https://notes.kodekloud.com/docs/LangGraph/State-Management-and-Iterative-Loops/Understanding-State-Accumulation-and-Data-Flow/page

Explains how graph-based systems accumulate shared state across nodes to enable contextual reasoning, track execution, support iterative agents, common patterns, and mitigation strategies for state bloat.

State accumulation is how LangGraph (and similar graph-based systems) remembers what happened during execution. The shared graph state acts as an incremental memory: each node can read from it, modify it, and pass the enriched state forward. Without accumulation, a graph is essentially stateless and cannot reason about prior events or maintain coherent multi-step behavior.

<Frame>
  <img alt="The image presents three reasons to focus on state accumulation: enabling contextual reasoning, tracking system evolution over time, and supporting iterative and adaptive behavior." />
</Frame>

Why state accumulation matters

* Enables contextual reasoning across multiple nodes and turns.
* Tracks the system's evolution over time, useful for audits and debugging.
* Supports iterative and adaptive behavior (e.g., agents refining their plan or tools over multiple passes).

How accumulation works (conceptual)

* The graph state is a dictionary/object shared between nodes.
* Each node may add new fields or update existing ones.
* Over time the state becomes a record of inputs, intermediate decisions, tool invocations, and final output.

Example: a simple state evolution

```js theme={null}
// initial state (empty)
state = {}

// After an intent classifier node:
state = {
  chat_history: [{ role: "user", text: "How long does the battery last?" }],
  intent: "battery_query"
}

// After a tool runner:
state.tools_used = [
  { tool: "spec_lookup", tool_response: "Battery lasts ~10 hours" }
]

// At response node:
state.response = "The battery typically lasts about 10 hours under normal usage."
```

<Frame>
  <img alt="The image illustrates a concept of &#x22;State Accumulation&#x22; using a flowchart with nodes A, B, and C, each accumulating more state information as they progress. It shows the evolution of intent and tools used at each node." />
</Frame>

Analogy: delivery journal
Think of the state as a delivery journal. At every stop the courier adds notes—what was delivered, which tool was used, or a customer request—and the journal becomes richer over the route. The graph state similarly accumulates actionable context that later nodes can consult.

State accumulation in chatbots and agents

* Follow-up questions only make sense when prior messages are preserved.
* Tools (search, calculators, external APIs) produce outputs that should be appended to the state so later nodes can reason with them.
* Execution traces (steps\_taken) help debugging, audit, and reproducibility.

<Frame>
  <img alt="The image illustrates &#x22;Accumulation in Chatbots&#x22; with a woman holding a tablet, a chatbot discussing how long a product lasts in a chat interface, and a diagram describing the chatbot's state and user context handling." />
</Frame>

Common accumulation patterns

| Field          | Purpose                                                         | Example                                                    |
| -------------- | --------------------------------------------------------------- | ---------------------------------------------------------- |
| `chat_history` | Preserve conversation turns for context and prompt construction | `[{ role: "user", text: "Where is my order?" }]`           |
| `tools_used`   | Log tool invocations and results for later reasoning or display | `[{ tool: "order_lookup", tool_response: {...} }]`         |
| `steps_taken`  | Execution trace for debugging, replay, or auditing              | `["classify_intent", "call_order_api", "format_response"]` |
| `memory`       | Persistent or summarized facts retained across executions       | `{"preferred_shipping":"overnight"}`                       |

<Frame>
  <img alt="The image illustrates four common accumulated fields: chat_history, tools_used, steps_taken, and memory, each with short descriptions. The text emphasizes that accumulation strategy defines agent adaptation." />
</Frame>

Trade-offs and mitigation
Accumulating everything without control can bloat the state, increase memory use, and slow processing. Common mitigation strategies:

* Cap chat history length (e.g., keep the last N turns).
* Expire or summarize older tool logs.
* Prune or compress `steps_taken` entries for long-running flows.
* Persist only what helps behavior or auditing; drop or archive the rest.

<Frame>
  <img alt="The image lists strategies for avoiding overaccumulation, such as capping chat history length, expiring outdated tool logs, and integrating pruning into graphs, with the reminder that intentional design prevents overload." />
</Frame>

> **lightbulb** Decide what to persist based on the agent's goals. Keep only the state that improves behavior or is required for auditing; summarize or drop the rest to maintain performance.

Further reading and references

* State (computer science): [https://en.wikipedia.org/wiki/State\_(computer\_science)](https://en.wikipedia.org/wiki/State_\(computer_science\))
* For practical designs, search for "conversational memory patterns", "agent tool logging", and "execution tracing best practices" to find implementation examples and community patterns.

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/7a80b285-b366-4c4d-95d0-bce0c24aaf58/lesson/4ed8f20e-852a-442b-b728-7ab22f616b13)
