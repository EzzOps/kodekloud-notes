# The Decision Maker Implementing the Conditional Router

Source: https://notes.kodekloud.com/docs/LangGraph/The-Core-Workflow-Nodes-Edges-and-Routing/The-Decision-Maker-Implementing-the-Conditional-Router/page

Explains implementing pure conditional routers in LangGraph that read graph state to route execution based on intent, tool outputs, or signals while keeping decision logic separate from node behavior

Not all conversations or processes follow a straight line. Users can switch from asking a question to making a command mid-conversation. A linear sequence of nodes can't handle that reliably — conditional routing is the solution.

<Frame>
  <img alt="The image is a flowchart illustrating the concept of conditional routing based on user input, which is split into categories of &#x22;Question&#x22; leading to &#x22;Answer&#x22; and &#x22;Command&#x22; leading to &#x22;Confirmation.&#x22;" />
</Frame>

Conditional routing lets your graph branch at runtime. Decisions can be based on user intent, LLM outputs, tool results, or internal state values. With a conditional router, a LangGraph becomes context-aware and adaptable — transforming a linear workflow into a decision engine.

A conditional router is implemented as a specialized edge in LangGraph: instead of blindly going from node A to node B, it inspects the graph state and chooses which node to run next.

<Frame>
  <img alt="The image illustrates a flowchart explaining a conditional router in LangGraph, starting from Node A, evaluating states, and directing to Nodes B, C, or D based on conditions." />
</Frame>

## How it works

1. A node (or nodes) computes values and writes them into the graph `state`.
2. Define a pure routing function that reads that `state` and returns a routing key (for example, `"search"`, `"answer"`, or `"clarify"`).
3. Register conditional edges with a `path_map` that maps routing keys to target node IDs.
4. The router only chooses the path; nodes perform work and update `state`.

This clear separation—decision logic in one place, behavior in separate nodes—keeps graphs modular, easier to test, and simpler to extend.

<Frame>
  <img alt="The image explains a &#x22;Conditional Router in LangGraph,&#x22; depicting a circular diagram with two sections labeled &#x22;Logic&#x22; (Decision Function) and &#x22;Behavior&#x22; (Nodes), emphasizing it's easy to test and extend." />
</Frame>

## Anatomy of conditional routing

You need:

* A graph `state` with explicit keys (for example, `intent`).
* One or more nodes that compute or set values in `state`.
* A pure routing function that reads `state` and returns a route key.
* A conditional edge that maps keys to target node IDs.

Example pattern:

* A "choose action" node runs an LLM or classifier and sets `state["intent"]`.
* A router function reads `state["intent"]` and returns that value.
* The builder registers conditional edges mapping intent values to node IDs.

Example implementation

```python theme={null}
