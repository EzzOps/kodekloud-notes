# Example output:
# {'question': 'What is the capital of France?', 'answer': 'Paris'}
```

Quick reference: common StateGraph methods

| Method                   |                             Purpose | Example                                 |
| ------------------------ | ----------------------------------: | --------------------------------------- |
| `add_node(name, fn)`     |            Register a node function | `graph.add_node("qa", answer_question)` |
| `set_entry_point(name)`  |               Set the starting node | `graph.set_entry_point("qa")`           |
| `set_finish_point(name)` |               Set the terminal node | `graph.set_finish_point("qa")`          |
| `compile()`              |           Produce an executable app | `app = graph.compile()`                 |
| `app.invoke(state)`      | Run the graph with an initial state | `app.invoke({"question": "..."})`       |

Scaling your graph
The same pattern — define a state, write nodes that read/update it, and connect nodes into a graph — scales to more advanced workflows:

* Branching and conditional transitions
* Loops and retries
* Persisted memory between runs
* Human-in-the-loop steps or approvals
* Observability and testing of individual nodes

<Frame>
  <img alt="The image illustrates the structure of a minimal StateGraph, showing components like State, Node, and Edge, and includes a process involving a language model." />
</Frame>

Links and references

* LangGraph (project docs / repo)
* OpenAI — [https://openai.com](https://openai.com)
* Anthropic — [https://www.anthropic.com](https://www.anthropic.com)
* LangChain — [https://langchain.dev](https://langchain.dev)

By following this minimal pattern you can build robust, maintainable agent workflows: make state explicit, keep node logic isolated, and compose nodes into clear, testable graphs.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/9ad1c023-6ddf-41fa-9043-b5ed2c4e66d6/lesson/5a345f91-5499-43ab-b22a-46740aaa0260" />
</CardGroup>


# Defining the Graph State Schema

Source: https://notes.kodekloud.com/docs/LangGraph/State-Management-and-Iterative-Loops/Defining-the-Graph-State-Schema/page

Explains designing and typing a shared graph state schema for LangGraph workflows to improve reliability, observability, and collaboration using Python TypedDicts and best practices.

In LangGraph, every node exchanges information through a shared structure called the graph state. A clear schema for that state is essential: it defines what the system knows, how knowledge evolves, and what each node should expect to read or write. Without a schema, nodes can assume fields that are never provided or accidentally overwrite critical data—leading to brittle, hard-to-debug graphs.

<Frame>
  <img alt="The image is a flowchart illustrating the importance of defining a graph state schema, highlighting reliability and explainability. It shows &#x22;Node A&#x22; interacting with a graph state that lacks a schema, which can lead to issues like unprovided summaries and overwritten values." />
</Frame>

Why a schema matters

* Improves reliability by preventing missing keys and type mismatches.
* Increases explainability by making the data surface explicit.
* Enables safer collaboration between nodes and teams.
* Makes observability and debugging easier because tools can inspect well-known fields.

The graph state as a single source of truth
LangGraph’s graph state is a single Python dictionary passed from node to node. Each node receives the state, may read and update it, and then passes the updated state forward. Think of it as a shared document that all nodes can edit: it provides memory, tracks tool usage, and stores intermediate outputs needed to build cross-node context.

<Frame>
  <img alt="The image explains the concept of &#x22;Graph State&#x22; with a diagram showing nodes A, B, and C, state as a Python dictionary, and the idea of a &#x22;single source of truth&#x22;. It emphasizes that each step reads, updates, and passes along the state." />
</Frame>

Typical fields you’ll find in LangGraph workflows
Common state fields include the user input, predicted intent, results returned by tools, chat history, and the final response. You’ll often also store flags, metadata, timestamps, or loop counters—anything that helps guide the execution flow.

<Frame>
  <img alt="The image outlines the common data in a graph state, consisting of four stages: Input (user's original message), Intent (predicted intent of message), Results (output from tools), and Response (final generated answer)." />
</Frame>

Use TypedDict to declare a schema
To make the state explicit and machine-checkable, LangGraph recommends declaring the schema using Python’s `TypedDict` (or `typing_extensions.TypedDict` for older versions). This provides a contract between nodes and allows static type checkers like [mypy](https://mypy-lang.org/) to catch inconsistencies early.

Example TypedDict schema:

```python theme={null}
from typing import List, Dict, Any
from typing_extensions import TypedDict, NotRequired
from langchain.schema import BaseMessage

class GraphState(TypedDict, total=False):
    # required at the start of a run
    input: str

    # optional fields populated as the graph executes
    intent: NotRequired[str]
    chat_history: NotRequired[List[BaseMessage]]
    tool_results: NotRequired[Dict[str, Any]]
    final_response: NotRequired[str]
    loop_count: NotRequired[int]
```

Notes about this pattern

* Using `total=False` makes keys optional by default. Alternatively, use `total=True` and mark selective keys with `NotRequired` (see [PEP 655](https://peps.python.org/pep-0655/))—choose the pattern that best fits your project.
* `chat_history` is typed as `List[BaseMessage]` (LangChain message types) to preserve conversational context.
* `tool_results` is a flexible `Dict[str, Any]` because outputs differ between integrations.

Why typing helps

* Static typing and `TypedDict` let tools verify nodes read/write the correct keys and types.
* Observability systems can record which fields exist at each node execution to simplify debugging and audits.
* A typed schema clarifies expectations across teams and over time, improving maintainability.

Field-by-field breakdown

| Field            | Type                | Purpose                                                                                                               |
| ---------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `input`          | `str`               | The user’s original message or command; present at the start of a run.                                                |
| `intent`         | `str`               | Typically set by an intent-classification node to indicate user intent (question, command, tool request, etc.).       |
| `chat_history`   | `List[BaseMessage]` | Stores conversation messages (e.g., `HumanMessage`, `AIMessage`, `SystemMessage`) needed for memory or summarization. |
| `tool_results`   | `Dict[str, Any]`    | Outputs from external tools; structure can be dynamic, e.g. `{"openweather": {"temp_f": 55, "condition": "Rain"}}`.   |
| `final_response` | `str`               | The composed answer produced by the final node.                                                                       |
| `loop_count`     | `int`               | Tracks iteration counts in cyclical graphs to help enforce safe exit conditions.                                      |

Example usage pattern

```python theme={null}
state: GraphState = {"input": "What's the weather in Seattle tomorrow?"}
