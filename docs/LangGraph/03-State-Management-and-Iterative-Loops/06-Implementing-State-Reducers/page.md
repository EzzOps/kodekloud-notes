# Implementing State Reducers

Source: https://notes.kodekloud.com/docs/LangGraph/State-Management-and-Iterative-Loops/Implementing-State-Reducers/page

Explains how LangGraph uses state reducers to control merging, accumulation, and cleanup of shared graph state.

State reducers in LangGraph are the gatekeepers for your shared graph state. They define exactly how the global state should change in response to node outputs, ensuring predictable, consistent updates across the graph.

Why it matters: without reducers, nodes can overwrite or duplicate data, resulting in an unreliable state and hard-to-debug behavior.

<Frame>
  <img alt="The image illustrates the concept of using state reducers by showing a shared state connected to three nodes (A, B, and C) with issues like &#x22;Overwrite&#x22; and &#x22;Duplicate&#x22; indicated." />
</Frame>

## How reducers introduce discipline

A reducer is a simple function that receives the current state and a node's output, then returns the updated state. This is the place to enforce rules like:

* Only add a field if it doesn't already exist.
* Append results to a list instead of replacing the list.
* Prune temporary or sensitive values before they persist.

Think of the reducer as an editor: it inspects node outputs and applies business rules before those outputs are committed.

<Frame>
  <img alt="The image explains a &#x22;State Reducer&#x22; function, highlighting its roles: adding a field only if it doesn't exist and adding to a list without overwriting." />
</Frame>

LangGraph uses the reducer after each node runs to decide what actually becomes part of the global state. This keeps node implementations simple—nodes return outputs, and reducers control how those outputs are merged into the graph.

<Frame>
  <img alt="The image explains &#x22;What is a State Reducer?&#x22; with a diagram showing nodes A, B, and C, each connected to a state. It illustrates how a &#x22;State Reducer&#x22; edits and commits state after each node in the LangGraph system." />
</Frame>

## Field-level reducers (custom merging)

By default, LangGraph performs a shallow merge when a node returns a field. For many workflows—chat history, tool logs, or aggregated analytics—you want accumulation instead of replacement. Field-level reducers let you define exactly how a single key is merged.

Example: annotate a `messages` field with a reducer that appends new messages rather than replacing the list.

```python theme={null}
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
```

Why use field-level reducers? They enable granular control: treat some keys as accumulators (history, logs) and others as unique values (intent, status).

<Frame>
  <img alt="The image explains state merging in LangGraph, highlighting that data should be merged intelligently rather than overwritten. It describes actions based on node output, such as updating intent or appending messages." />
</Frame>

## Example: custom merge for tool results

Below is a concrete reducer example that accumulates tool results instead of overwriting them, plus a sample node that returns the `tool_results` field.

```python theme={null}
from typing_extensions import TypedDict, Annotated

def merge_tool_results(old, new):
    # Accumulate results instead of overwriting
    return (old or []) + (new or [])

class GraphState(TypedDict):
    question: str
    tool_results: Annotated[list, merge_tool_results]

def search_web(state: GraphState) -> dict:
    # Example implementation: call a search tool and return its results for the
    # "tool_results" field. Replace tavily.search with your own tool invocation.
    results = tavily.search(query=state["question"], max_results=3)["results"]
    return {"tool_results": results}
