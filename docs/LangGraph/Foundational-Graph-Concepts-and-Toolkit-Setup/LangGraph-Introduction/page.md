# If running in a clean environment, uncomment and run:
# pip install --upgrade openai langgraph
```

Set your environment variable:

* `OPENAI_API_KEY` — required
* `OPENAI_MODEL` — optional (defaults to `gpt-4` in the examples below)

You can set `OPENAI_API_KEY` in your shell or let the script prompt for it at runtime.

| Item             | Purpose                              | Example / Notes                 |
| ---------------- | ------------------------------------ | ------------------------------- |
| Packages         | Provides SDKs for OpenAI + LangGraph | `pip install openai langgraph`  |
| `OPENAI_API_KEY` | Auth for OpenAI API                  | set in env or prompt at runtime |
| `OPENAI_MODEL`   | Model selection                      | `gpt-4` (default)               |

<Callout icon="warning">
  Protect your `OPENAI_API_KEY`. Using LLMs incurs cost — monitor usage and model selection (`OPENAI_MODEL`) to control billing.
</Callout>

## Initialize the client and constants

The example below creates an OpenAI client (reading `OPENAI_API_KEY` from the environment) and sets a default `MODEL`. The helper will prompt for the key if it is not already set.

```python theme={null}
import os
import getpass
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from openai import OpenAI

# Helper to prompt for the API key if not set in the environment
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}:")

_set_env("OPENAI_API_KEY")

# Create OpenAI client (expects OPENAI_API_KEY in env)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Choose a model (adjust as needed for your org/account)
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4")
```

## Define a typed state

LangGraph operates on structured, typed states instead of raw strings. Define the state shape with `TypedDict`. This example uses a two-field state: `question` (input) and `answer` (output).

```python theme={null}
class QAState(TypedDict):
    question: str
    answer: str
```

Using a typed state makes data flow explicit, enables validation, and improves readability when graphs grow larger.

## Node: call the Responses API

Each node receives the current typed state and returns a partial update (a dictionary with only the fields it produced). Here is a single node, `answer_question`, which calls the OpenAI Responses API using the `question` and returns only the `answer` field.

```python theme={null}
def answer_question(state: QAState) -> dict:
    """Call OpenAI Responses API and return the answer as a partial state update."""
    resp = client.responses.create(
        model=MODEL,
        input=state["question"],
    )
    # Use the SDK's convenience property for text output
    return {"answer": resp.output_text}
```

Note: nodes should return partial state updates rather than replacing the entire state. LangGraph merges these updates into the global state — this composability enables building larger orchestrations from small, focused nodes.

## Build the StateGraph and set the entry point

Register the node in a `StateGraph`, set the entry point, then compile the graph into a callable `app`.

```python theme={null}
builder = StateGraph(QAState)
builder.add_node("qa", answer_question)
builder.set_entry_point("qa")
app = builder.compile()
```

## Invoke the graph

Invoke the compiled graph with an initial state that provides the `question`. LangGraph runs the entry node, merges the returned partial update, and returns the final state that includes both the original input and the generated `answer`.

```python theme={null}
result = app.invoke({"question": "In one sentence, what is LangGraph used for?"})
print(result["answer"])
```

Example final state:

```python theme={null}
{
  "question": "In one sentence, what is LangGraph used for?",
  "answer": "LangGraph is used for creating and visualizing complex language processing workflows with multiple models and functions."
}
```

## Why this pattern matters

* Typed state: makes data flow explicit and type-safe across nodes.
* Nodes return partial updates: enables small, composable units of work that can be merged by the orchestrator.
* Graph defines orchestration: lets you add routing, tool-calling, validation, retries, or memory without changing node internals.

This pattern scales cleanly to agentic workflows. You can add routing nodes, tool-call nodes, validation or critique steps, and memory writes while preserving the same execution model.

## Next steps and extensions

From here you can extend the basic graph with:

* Branching and routing (conditional node execution)
* Tool integration (external APIs, search, databases)
* Retries and error handling
* Observability and metrics for each node
* Persistent memory for multi-step dialogs

Each extension is implemented by adding nodes or orchestration logic — you do not need to rewrite core node implementations.

## Links and references

* LangGraph: [https://github.com/langgraph/langgraph](https://github.com/langgraph/langgraph)
* OpenAI Responses API: [https://platform.openai.com/docs/api-reference/responses](https://platform.openai.com/docs/api-reference/responses)
* OpenAI Python client: [https://github.com/openai/openai-python](https://github.com/openai/openai-python)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-6ddf-41fa-9043-b5ed2c4e66d6/lesson/1fe2b2d1-2d71-4bb3-8078-49d514b6dac9" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.[SECRET_REDACTED]-6ddf-41fa-9043-b5ed2c4e66d6/lesson/c890ba0e-262b-4deb-ab58-69bf6f25d269" />
</CardGroup>


# LangGraph Introduction

Source: https://notes.kodekloud.com/docs/LangGraph/Foundational-Graph-Concepts-and-Toolkit-Setup/LangGraph-Introduction/page

Introduction to LangGraph, a visual declarative state-machine framework built on LangChain for organizing multi-step AI agent workflows with persistent state, branching, retries, and human-in-the-loop support

Welcome — this guide introduces LangGraph by building intuition first, then showing how the library maps complex agent behavior into a clear, visual state machine. If you build multi-step AI agents, document pipelines, or human-in-the-loop assistants, LangGraph gives you an explicit roadmap to manage flow, state, and retries while integrating familiar LangChain components.

Why start with a story? Practical analogies make the need for explicit control flow easier to grasp.

There was once a messenger named Ravi who was excellent at reading letters and talking to people. Everyone trusted him to handle important messages. But Ravi had one problem: the town he worked in was huge and confusing. Some days he forgot which house he had already visited. Some days he mixed up the order of deliveries. If someone stopped him midway to add a new instruction, he got completely lost. And if two people gave him tasks at the same time, he didn't know which one to handle first.

<Frame>
  <img alt="The image shows a character asking &#x22;Which first?&#x22; with a flowchart directing tasks A and B to Person A and Person B respectively." />
</Frame>

Ravi was capable — his problem was lack of a persistent plan. One day the mayor gave him a detailed map showing the route, fallback actions for closed houses, where to pause for checks, and the next-step rules. With that map, Ravi’s deliveries became smooth and predictable: no repeats, no skips, and no panic when plans changed. He still did the thinking and talking — the map simply kept everything organized.

<Frame>
  <img alt="The image shows a cartoon character with a speech bubble saying &#x22;Yes, I needed this,&#x22; alongside a map with options: &#x22;Clear route,&#x22; &#x22;Next step,&#x22; and &#x22;Fallback actions.&#x22;" />
</Frame>

That map is what LangGraph provides for AI. Large language models are powerful, but multi-step tasks can confuse them. LangGraph supplies the structure, flow, and persistent state so the AI always knows what to do next.

<Frame>
  <img alt="The image shows a map with a delivery route and an illustration of a person holding a package, accompanied by features such as &#x22;Reads letter,&#x22; &#x22;Talks to people,&#x22; and route optimization indicators like &#x22;No repeated houses&#x22; and &#x22;No skipped stops.&#x22;" />
</Frame>

Why LangGraph?

LangGraph addresses a common gap: libraries like LangChain provide LLMs, tools, chains, and memory blocks — but not a visual, declarative way to organize multi-step interactions. LangGraph models agent workflows as a graph (a finite state machine) so you can design explicit, maintainable flows with deterministic transitions and conditional branching.

<Frame>
  <img alt="The image presents a graphical explanation of LangGraph, highlighting its capability to manage complex, multi-step AI agent workflows effectively." />
</Frame>

How it works (high level)

A graph model gives you:

* A clear roadmap for the agent.
* Traffic rules that determine how and when to move between steps.
* Persistent state the agent carries and updates.
  LangGraph is built on top of LangChain, letting you reuse LLMs, memory, tools, and chains while organizing them declaratively in a state-machine-style graph.

<Frame>
  <img alt="The image explains the concept of LangGraph using a graph-based state machine model with states A, B, and C, connected to an agent, and highlights features like branching logic, retries, looping, and conditional steps." />
</Frame>

Core building blocks

* Node: a logical unit of work (an LLM call, tool execution, or data transformation).
* Edge: a connection that defines the next node based on conditions or outputs.
* State: the persistent context carried between nodes (memory, inputs, outputs, user data).

To extend the Ravi analogy:

* A node is a single action (pick up letters, deliver a letter, request signature).
* An edge is the path or conditional rule (if house locked → try next house).
* The state is what Ravi remembers and updates (delivered list, locked houses, notes).

<Frame>
  <img alt="The image is a flowchart titled &#x22;Node,&#x22; depicting a logical unit that functions as a mini-program and connects to LLM calls and tool execution." />
</Frame>

State and persistence

LangGraph persists and updates the state as the graph runs. The state schema becomes the shared input/output contract across nodes and edges so each part of the graph can read and write expected fields.

<Frame>
  <img alt="The image shows a diagram about the &#x22;State&#x22; as the agent's working context, highlighting elements like memory, input/output values, and user data." />
</Frame>

<Frame>
  <img alt="The image shows a list of tasks related to mail delivery, such as checking which letters are delivered and which houses were locked, alongside an illustration of a person holding envelopes." />
</Frame>

State schema example (Python)

Define a typed state schema so nodes and transitions can rely on a consistent context shape:

```python theme={null}
from typing import TypedDict

class State(TypedDict):
    graph_state: str
    delivered: list[str]
    current_target: str | None
```

This TypedDict ensures the graph and nodes agree on the shared context structure (inputs and outputs), improving type-safety and clarity.

Core building blocks — quick reference

| Component | Purpose                                                                      | Example / Notes                                                           |
| --------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Node      | Encapsulates one unit of work — LLM call, tool execution, or processing task | `LLM -> summarize -> update state`                                        |
| Edge      | Defines transitions between nodes, conditional or deterministic              | `if state["delivered"] contains target -> go to summary_node`             |
| State     | Persistent working context shared across nodes and edges                     | `{"graph_state": "in_progress", "delivered": [], "current_target": None}` |

Key LangGraph features

* Looping & branching: model conditional paths, retries, and loops without tangled if/else code.
* State persistence: pause and resume workflows with persisted state snapshots.
* Human-in-the-loop: add review gates where a person inspects or edits state before continuing.
* Streaming outputs: stream LLM responses for responsive UIs and progressive feedback.
* LangChain integration: reuse LangChain LLMs, memory, tools, chains, and expressions.

<Frame>
  <img alt="The image is an infographic titled &#x22;LangGraph – Key Features,&#x22; highlighting features like state persistence, human-in-the-loop support, streaming outputs, looping & branching, and LangChain integration." />
</Frame>

<Callout icon="lightbulb">
  LangGraph provides a declarative, visual state machine you can build on top of familiar LangChain components — giving you structure and control for complex agent workflows.
</Callout>

Real-world use cases

* Multi-agent systems: separate planning and execution agents coordinate via shared state and transitions.
* Approval workflows: generate artifacts and pause for human review before continuing.
* Resilient chains: implement fallback strategies (e.g., try GPT-4, then fallback to a smaller model) with branching and retries.
* Dynamic document processing: scan documents, summarize, route to reviewers, and store final results using a single graph for orchestration.

<Frame>
  <img alt="The image outlines four example use cases: Multi-Agent Systems, Approval Workflows, Resilient Chains, and Dynamic Document Processing, each with a brief description and an icon." />
</Frame>

These scenarios show where LangGraph is already helping teams build production-ready, resilient AI flows.

Wrap up

LangGraph blends the explicit control of a state machine with LangChain’s composable AI building blocks. You get built-in handling for looping, pausing, retries, streaming, and human interaction while keeping workflows declarative, visual, and maintainable. Engineers and product teams can use LangGraph to construct interactive, fault-tolerant AI systems faster and with fewer surprises.

Get started by defining a small graph: list nodes for each logical step, define the state schema, and wire edges for your expected transitions. Iteratively add retries, checkpoints, and fallbacks as you mature the flow.

<Frame>
  <img alt="The image is a summary slide highlighting key features and future steps for LangGraph, including its flexibility, support for various functionalities, and accessibility for builders." />
</Frame>

Links and references

* LangChain: [https://learn.kodekloud.com/user/courses/langchain](https://learn.kodekloud.com/user/courses/langchain)
* Python TypedDict docs: [https://docs.python.org/3/library/typing.html#typing.TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)

Further reading and next steps

* Define your state schema early — it’s the contract across nodes.
* Start small: model one happy path first, then add branches and retries.
* Use human review nodes for safety-critical decisions.
* Reuse LangChain components (LLMs, tools, memory) inside LangGraph nodes for faster development.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-6ddf-41fa-9043-b5ed2c4e66d6/lesson/9cd71629-d144-4ab6-a82f-730486f4049f" />
</CardGroup>
