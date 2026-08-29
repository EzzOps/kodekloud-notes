# Example: a classifier node sets the intent in state
def classify_intent_node(state, context):
    user_message = state.get("user_message", "")
    # (Implementation detail) Use an LLM or classifier here.
    # For demonstration, a simple rule:
    if user_message.lower().startswith("find"):
        state["intent"] = "search"
    elif user_message.endswith("?"):
        state["intent"] = "clarify"
    else:
        state["intent"] = "answer"
    return state
```

```python theme={null}
# Router function and conditional edge registration
def route_by_intent(state):
    # Read the explicit state key and return the routing key
    return state.get("intent", "answer")  # default to "answer" if missing

# Register a conditional edge on the builder
builder.add_conditional_edges(
    "choose_action",            # router node id / edge id
    condition=route_by_intent,  # function that returns a path key
    path_map={                  # map returned keys to node ids
        "search": "search_node",
        "answer": "generate_node",
        "clarify": "clarify_node",
    },
)
```

Important design note: the decision itself should not be made inside the router by calling an LLM or performing side effects. The preceding node(s) should set state (for example, `state["intent"] = "search"`). The router must remain pure and only read state and return a routing key.

<Frame>
  <img alt="The image is a flowchart depicting a decision-making process, starting with a user message, going through an intent classifier node, graph state, and a router that reads the intent before reaching a search node." />
</Frame>

Keeping classifier logic and routing logic separate makes routers reusable: you can plug different classifiers into the same router or reuse routers across different graphs.

In practice, classifier nodes are often implemented with tools like LangChain LLMChains or other classification services. The classifier node writes results into `state`; the router routes on those values.

<Frame>
  <img alt="The image illustrates a flowchart labeled &#x22;Where Does the Decision Happen?&#x22; featuring LangChain and LLMChain, where results are stored in state and routed based on value." />
</Frame>

## What can you route on?

Use conditional routing for a wide range of signals:

| Resource    | Example routing conditions     | Example action                                     |
| ----------- | ------------------------------ | -------------------------------------------------- |
| Intent      | `search`, `answer`, `clarify`  | Route to search or follow-up question node         |
| Tool output | Document found or not          | Route to `generate_node` or `fallback_search_node` |
| LLM quality | Confidence or score thresholds | Route to `re-ask` or `use_alternative_strategy`    |
| User type   | `premium` vs `free`            | Route to advanced features or limited flow         |

You can also implement more advanced behaviors: fallback logic, confidence thresholds, multi-step evaluations — as long as the routing function returns a known key, LangGraph will map it to the correct node.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Decision Patterns, What Can You Route On?&#x22; showing a &#x22;Routing Decision Hub&#x22; with connections to various decision outcomes like &#x22;Intent,&#x22; &#x22;Tool output,&#x22; and &#x22;LLM Response Quality,&#x22; each leading to further actions." />
</Frame>

## Minimal example flow

* A "Choose Action" node sets `state["intent"]` via an LLM or classifier.
* A router reads `state["intent"]` and returns the routing key.
* Execution continues at the node mapped to that key.

You can test the routing locally by setting `state` manually to different intent values and verifying the graph follows different paths.

<Frame>
  <img alt="The image is a flowchart demonstrating a conditional graph for code, starting with a language model determining intent, updating the state, and routing based on state intent to different nodes." />
</Frame>

## Chatbot example

Example runtime flow:

* User: "Can you look up the LangGraph docs?"
* Node 1: Classify intent → sets `state["intent"] = "search"`
* Router: Sends execution to `search_node`
* `search_node`: Calls a search tool and stores results in `state`
* `generate_node`: Summarizes found documents into a response

For `clarify`, the router can direct to a node that prompts the user for more details. This pattern scales: add more intent types and nodes as needed.

<Frame>
  <img alt="The image describes a chatbot intent routing process, highlighting &#x22;answer&#x22; for knowledge-based responses and &#x22;clarify&#x22; to prompt users for more input. It emphasizes the robustness and scalability of the application." />
</Frame>

## Best practices

* Use explicit state keys such as `intent`, `decision`, or `route_choice`.
* Keep routing functions pure: avoid side effects and do not call LLMs inside them.
* Log routing decisions to make flows observable and debuggable.
* Avoid embedding routing logic inside nodes; use `add_conditional_edges` to keep routing separate.
* Design routers as small, pluggable functions so they can be reused across graphs and contexts (role-based routing, language switching, escalation).

<Frame>
  <img alt="The image provides design tips for conditional graphs, including using explicit state keys, keeping routing functions pure, logging routes for visibility, and avoiding embedding routing inside nodes." />
</Frame>

<Callout icon="warning">
  Do not perform side effects or call external services (including LLMs) inside your router function. Put that work in preceding nodes and let the router only read state and return a key.
</Callout>

When routing is mixed into node logic it becomes harder to debug and test. Separating routing with `add_conditional_edges` keeps graphs maintainable and easier to reason about — a must for production systems.

<Frame>
  <img alt="The image is a flowchart depicting a reusable routing pattern using a &#x22;Pluggable Router&#x22; connected to Context A (Graph 1) and Context B (Graph 2), emphasizing logic plug-ins and endpoint swapping or prototyping." />
</Frame>

<Callout icon="lightbulb">
  Design routers as pure, pluggable functions so they can be reused across graphs and contexts — for example, role-based routing, language switching, or escalation flows.
</Callout>

## Summary

The router is the brain of a LangGraph: it decides which work to run next but does not perform the work itself. By learning how to set and read state and return routing keys from small, pure functions, you can build smart branching flows that respond to user needs, tool outputs, and more. Conditional routing adds intelligence without unnecessary complexity and scales to advanced use cases like loops and persistent state.

## Links and references

* [LangChain LLMChain documentation](https://langchain.readthedocs.io/en/latest/modules/chains/index_examples/llm_chain.html)
* LangGraph conditional routing concepts and best practices (internal docs and examples)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-0429-43c9-8ecf-2df222ce0663/lesson/a4054bd2-0a1b-4889-a3a9-da9d04fa34a4" />
</CardGroup>


# The Path Building Simple Non Cyclical Sequences

Source: https://notes.kodekloud.com/docs/LangGraph/The-Core-Workflow-Nodes-Edges-and-Routing/The-Path-Building-Simple-Non-Cyclical-Sequences/page

Guide to building and testing linear non-cyclical LangGraph workflows using shared typed state where nodes return partial updates for deterministic multi-step pipelines

When learning how LangGraph works, start with a simple, linear sequence of steps — a non-cyclical workflow where each node runs exactly once in a defined order. These linear graphs are easy to reason about, test, and debug because data moves in a single direction through a shared state object.

Think of it as an assembly line: one task hands off to the next, no loops, no branches.

<Frame>
  <img alt="The image is a flowchart showing a simple sequence from &#x22;Start&#x22; to &#x22;Output&#x22; through &#x22;Node 1,&#x22; &#x22;Node 2,&#x22; and &#x22;Node 3.&#x22; Below are questions about node interaction, state passing, and output generation." />
</Frame>

Why start with simple sequences?

This pattern is ideal for deterministic pipelines such as staged summarization, a fixed chat-response flow, or multi-step data processing. Mastering linear graphs first gives you a clear mental model for how nodes interact, how state is passed, and how outputs are produced — which makes it easier to add branching or loops later.

<Frame>
  <img alt="The image lists three reasons for starting with simple sequences: summarizing text in stages, responding to chat queries, and performing multi-step data processing." />
</Frame>

Core definition: non-cyclical sequence in LangGraph

In LangGraph, a non-cyclical sequence means:

* Each node receives the full, current shared state.
* Each node returns only the partial state it produces.
* The framework merges those partial updates into the global state.
* No node routes back to a previous node (no cycles).

This model is excellent for static pipelines, deterministic agents, and educational demos because the execution order is predictable and easy to trace.

<Frame>
  <img alt="The image explains the benefits of a non-cyclical sequence in LangGraph, highlighting its suitability for static pipelines, deterministic agents, and educational demos. It mentions that this predictable flow is ideal for learning state transitions." />
</Frame>

Building a sequential LangGraph — high-level steps

1. Create a graph builder.
2. Add nodes (each node is a function, chain, or tool wrapper that transforms part of the state).
3. Connect nodes in sequence (add edges).
4. Define entry and exit nodes.

Quick pseudocode example

```python theme={null}
