# Handling Multiple State Schemas

Source: https://notes.kodekloud.com/docs/LangGraph/State-Management-and-Iterative-Loops/Handling-Multiple-State-Schemas/page

Explains using per‑subgraph state schemas, TypedDicts, adapters, and type guards to make LangGraph workflows modular, reusable, and safe to evolve.

Not every branch or component in a LangGraph needs the same state shape. As graphs grow, reusing components or composing subgraphs with different data requirements becomes essential. Handling multiple state schemas lets each part of the graph declare the fields it requires without forcing a one-size-fits-all global state.

<Frame>
  <img alt="The image is a flowchart titled &#x22;Why Multiple State Schemas?&#x22; showing a process starting from a &#x22;Start&#x22; node, branching into three components (A, B, C) with corresponding states, leading to sub-branches (X, Y), and ending at an &#x22;End&#x22; node." />
</Frame>

For example, a summarization branch might track paragraphs and topic scores, while a QA branch stores citations and tool logs. Forcing all branches to conform to a single schema makes components heavier and harder to reuse. Instead, define the schema that each subgraph or node needs and keep global state optional where components intersect.

<Frame>
  <img alt="The image is a workflow graph illustrating the disadvantages of using a global schema across multiple components, where only Component A benefits, while Components B and C do not." />
</Frame>

Why use multiple schemas? They let you:

* Document assumptions per module.
* Catch schema mismatches early via typing and tests.
* Reason locally about each node’s inputs and outputs.
* Reuse subgraphs across different parent graphs with confidence.

<Frame>
  <img alt="The image is a diagram titled &#x22;What Are Multiple Schemas?&#x22; showing a workflow graph with subgraphs for retrieval and summarizer, connected through state schemas and type state structures." />
</Frame>

Analogy: imagine Ravi carries different forms for deliveries — one for medical items, another for food, another for paperwork — each form contains fields tailored to the task. The same applies to graph state: each subgraph should own the fields it requires.

<Frame>
  <img alt="The image explains &#x22;What Are Multiple Schemas?&#x22; featuring three points: clear assumptions, early error detection, and local reasoning per node." />
</Frame>

When your system handles multiple flows (e.g., summarization and translation), you may share some common fields (like `input` and `response`) while each branch tracks its own specialized fields. Keeping separate TypedDicts for these subgraphs clarifies those differences and makes it safe to reuse branches across other graphs. It also helps agents and routers dynamically adapt to context.

<Frame>
  <img alt="The image is a diagram titled &#x22;What Are Multiple Schemas?&#x22; illustrating two categories: &#x22;Medical Delivery&#x22; and &#x22;Food Delivery,&#x22; each with specific attributes listed below them." />
</Frame>

Practical patterns

* Local schemas: give each subgraph or node its own TypedDict that documents required and optional fields.
* Composed parent state: the parent graph can accept a broader `GraphState` with many `total=False` fields so subgraphs can coexist.
* Adapter (transition) nodes: map one schema to another when composing subgraphs.
* Type guards: verify runtime state before assuming fields are present.

Example typed declarations (useful for IDEs and static checks):

```python theme={null}
from typing import List
from typing_extensions import TypedDict
from langchain.schema import BaseMessage

class SearchState(TypedDict):
    query: str
    search_results: list

class ChatState(TypedDict):
    input: str
    chat_history: List[BaseMessage]

class GraphState(TypedDict, total=False):
    input: str
    response: str
    query: str
    search_results: list
    chat_history: List[BaseMessage]
```

Subgraphs: isolate functionality and preserve contracts
A subgraph is a small, self-contained graph with its own state schema. Use subgraphs to encapsulate search, summarization, validation, or any reusable logic.

```python theme={null}
from typing_extensions import TypedDict, NotRequired
from typing import List
from langchain.schema import BaseMessage
from langraph.graph import StateGraph, START, END

class SearchState(TypedDict):
    query: str
    search_results: NotRequired[List[dict]]

def define_search_subgraph(search_node):
    builder = StateGraph(SearchState)

    builder.add_node("search", search_node)
    builder.add_edge(START, "search")
    builder.add_edge("search", END)

    return builder.compile()
```

This example shows a `SearchState` that requires `query` but treats `search_results` as optional. Compile the subgraph and reuse it inside multiple parent graphs. Subgraphs make it easy to test and swap implementations without touching the outer workflow.

Adapters: translate state between schemas
When composing subgraphs with different schemas, use small adapter nodes to map one shape to another. Adapters perform renames, conversions, enrichments, or cleanup.

```python theme={null}
def map_search_to_chat_state(search_state: dict) -> dict:
    return {
        "input": search_state.get("query", ""),
        "chat_history": [],
    }
```

Register adapters like any other node (e.g., `graph.add_node("adapter", adapter_fn)`) and connect them between subgraphs. Adapters are particularly valuable when integrating components from different teams or when evolving schemas over time.

Runtime vs static checks: use type guards
TypedDicts are development-time tools; at runtime the state is a plain dictionary. Protect nodes that expect specific fields with explicit type guards:

```python theme={null}
def is_search_state(state: dict) -> bool:
    return "query" in state and "search_results" in state
```

Use guards inside routers or nodes to branch safely and avoid KeyError exceptions. You can create stricter guards that check types with `isinstance` or raise informative errors when a state is malformed.

> **lightbulb** Type hints and `TypedDict`s improve clarity and tooling support. Always validate runtime assumptions with explicit guards or adapter nodes when composing independent subgraphs.

Benefits of multiple schemas

<Frame>
  <img alt="The image outlines the benefits of using multiple schemas: local clarity and simplicity, increased reusability, and easier debugging and maintenance." />
</Frame>

* Local clarity: each node/subgraph documents exactly what it needs.
* Reusability: isolate functionality, then reuse across projects.
* Easier debugging: smaller, focused schemas reduce search space for bugs.
* Safe evolution: change a subgraph’s schema without breaking unrelated branches.

Quick reference table

| Pattern                    | Purpose                                        | When to use                                     |
| -------------------------- | ---------------------------------------------- | ----------------------------------------------- |
| TypedDict per subgraph     | Document fields and static assumptions         | For any modular subgraph or node                |
| `GraphState` (total=False) | Compose multiple optional fields in the parent | When multiple subgraphs share a container state |
| Adapter nodes              | Map one schema to another                      | When composing subgraphs with different shapes  |
| Type guards                | Runtime validation of required fields          | Protect critical nodes and routers              |

Further reading and references

* LangChain docs: [https://langchain.readthedocs.io/](https://langchain.readthedocs.io/)
* Python typing: [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)
* typing\_extensions `TypedDict`: [https://pypi.org/project/typing-extensions/](https://pypi.org/project/typing-extensions/)

Summary
Treat schemas as local contracts for subgraphs and nodes. Use `TypedDict` and type hints to improve developer experience, introduce adapters to translate state between modules, and protect runtime behavior with explicit type guards. This approach keeps LangGraph workflows modular, easier to reason about, and safer to evolve over time.

- [Watch Video](https://learn.kodekloud.com/user/courses/langgraph/module/7a80b285-b366-4c4d-95d0-bce0c24aaf58/lesson/344d3bd4-df92-4548-944b-b60b8d7f0516)
