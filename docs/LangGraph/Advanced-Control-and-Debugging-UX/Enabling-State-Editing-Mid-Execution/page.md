# Imports used throughout the examples
from typing import TypedDict, List, Dict
import copy
from pprint import pprint
```

Define a compact `TypedDict` to represent the workflow state used in the demo:

```python theme={null}
class WorkflowState(TypedDict):
    input_text: str
    confidence: float
    decision: str
    status: str
```

Next, define the workflow nodes. This tiny workflow has two phases:

1. Evaluate (marks the state as evaluated)
2. Route (chooses a path based on confidence)

```python theme={null}
def evaluate_node(state: WorkflowState) -> WorkflowState:
    return {
        **state,
        "status": "evaluated"
    }

def route_node(state: WorkflowState) -> WorkflowState:
    if state["confidence"] >= 0.7:
        return {
            **state,
            "decision": "main_path",
            "status": "completed"
        }
    return {
        **state,
        "decision": "fallback_path",
        "status": "completed"
    }
```

Build a tiny checkpoint engine to simulate LangGraph's checkpointing. Each checkpoint stores a deep copy of the state in a history list so it can be inspected or restored later.

```python theme={null}
def save_checkpoint(history: List[Dict], step_name: str, state: WorkflowState):
    history.append({
        "step": step_name,
        "state": copy.deepcopy(state)
    })

def run_workflow(initial_state: WorkflowState):
    history: List[Dict] = []
    state = copy.deepcopy(initial_state)

    save_checkpoint(history, "start", state)

    state = evaluate_node(state)
    save_checkpoint(history, "after_evaluate", state)

    state = route_node(state)
    save_checkpoint(history, "after_route", state)

    return state, history
```

Run the workflow once with a low-confidence input so the route chooses the fallback path. We print both the final state and the saved checkpoints for inspection.

```python theme={null}
initial_state: WorkflowState = {
    "input_text": "Classify this request and decide whether to continue automatically.",
    "confidence": 0.4,
    "decision": "",
    "status": "new"
}

final_state, history = run_workflow(initial_state)

print("Final state from first run:")
pprint(final_state)

print("\nCheckpoints:")
for i, checkpoint in enumerate(history):
    print(f"Checkpoint {i}: {checkpoint['step']}")
    pprint(checkpoint["state"])
    print("-" * 60)
```

```plaintext theme={null}
Final state from first run:
{'input_text': 'Classify this request and decide whether to continue automatically.',
 'confidence': 0.4,
 'decision': 'fallback_path',
 'status': 'completed'}

Checkpoints:
Checkpoint 0: start
{'input_text': 'Classify this request and decide whether to continue automatically.',
 'confidence': 0.4,
 'decision': '',
 'status': 'new'}
------------------------------------------------------------
Checkpoint 1: after_evaluate
{'input_text': 'Classify this request and decide whether to continue automatically.',
 'confidence': 0.4,
 'decision': '',
 'status': 'evaluated'}
------------------------------------------------------------
Checkpoint 2: after_route
{'input_text': 'Classify this request and decide whether to continue automatically.',
 'confidence': 0.4,
 'decision': 'fallback_path',
 'status': 'completed'}
------------------------------------------------------------
```

Each saved checkpoint represents a snapshot of execution at a particular step. Time travel means selecting one of those snapshots, changing the state, and continuing from there to observe how the workflow would behave under the modified conditions.

<Callout icon="lightbulb">
  Time travel is useful for debugging and experimentation: instead of rerunning the entire pipeline, you can jump to the step you care about, change a variable, and see what would have happened.
</Callout>

## Inspecting checkpoints

Here’s a concise table that summarizes the checkpoints created in the example:

| Index | Step name        | Description                                                        |
| ----- | ---------------- | ------------------------------------------------------------------ |
| 0     | `start`          | Initial input state before any processing.                         |
| 1     | `after_evaluate` | State after the evaluate node marks the request as `evaluated`.    |
| 2     | `after_route`    | Final state after routing (decision chosen based on `confidence`). |

## Rewind, inject, and resume

Now rewind to the checkpoint saved immediately after evaluation (`after_evaluate`), inject a higher confidence value, and resume routing from that checkpoint so the workflow follows the alternate path.

```python theme={null}
# Choose the checkpoint to rewind to (after_evaluate)
rewind_checkpoint = next(c for c in history if c["step"] == "after_evaluate")
rewind_state: WorkflowState = copy.deepcopy(rewind_checkpoint["state"])

# Inject a modified value
rewind_state["confidence"] = 0.9

print("Injected state (after rewind):")
pprint(rewind_state)

# Continue execution from the rewound checkpoint
continued_state = route_node(rewind_state)

print("\nFinal state after time travel and injection:")
pprint(continued_state)
```

```plaintext theme={null}
Injected state (after rewind):
{'input_text': 'Classify this request and decide whether to continue automatically.',
 'confidence': 0.9,
 'decision': '',
 'status': 'evaluated'}

Final state after time travel and injection:
{'input_text': 'Classify this request and decide whether to continue automatically.',
 'confidence': 0.9,
 'decision': 'main_path',
 'status': 'completed'}
```

Compare the original run outcome with the time-travel outcome:

```python theme={null}
print("Original run outcome:")
pprint(final_state)

print("\nAfter rewind + injection:")
pprint(continued_state)
```

```plaintext theme={null}
Original run outcome:
{'input_text': 'Classify this request and decide whether to continue automatically.',
 'confidence': 0.4,
 'decision': 'fallback_path',
 'status': 'completed'}

After rewind + injection:
{'input_text': 'Classify this request and decide whether to continue automatically.',
 'confidence': 0.9,
 'decision': 'main_path',
 'status': 'completed'}
```

Because we injected a higher confidence before routing, the resumed execution followed the `main_path` instead of the `fallback_path`. This demonstrates how state injection lets you explore alternate outcomes without re-running the entire workflow.

<Callout icon="warning">
  When modifying checkpoints, always work on deep copies (as shown) to avoid mutating historical records. Preserving immutable checkpoints ensures reproducibility and accurate auditing of prior runs.
</Callout>

## When to use time travel with state injection

* Reproduce a bug that occurs only with a specific intermediate value.
* Test how downstream logic responds to different upstream outputs.
* Perform A/B style experiments by changing one variable at a checkpoint and comparing outcomes.

## References and further reading

* Python `TypedDict` and typing: [https://docs.python.org/3/library/typing.html#typing.TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)
* Checkpointing concepts (computing): [https://en.wikipedia.org/wiki/Checkpoint\_(computing)](https://en.wikipedia.org/wiki/Checkpoint_\(computing\))
* LangGraph concepts and docs (search for LangGraph checkpoints and debugging in your project docs)

Key takeaway: State injection (time travel) lets you rewind a workflow to a chosen checkpoint, modify the saved state, and continue execution from there—making debugging, testing, and scenario exploration faster and more targeted.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-cf65-40d3-a3c3-70fdfb767635/lesson/77331c58-962b-4d72-b4b9-8f3454463d05" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.[SECRET_REDACTED]-cf65-40d3-a3c3-70fdfb767635/lesson/3cbdd6a6-88fb-4072-bede-10fc0e692056" />
</CardGroup>


# Enabling State Editing Mid Execution

Source: https://notes.kodekloud.com/docs/LangGraph/Advanced-Control-and-Debugging-UX/Enabling-State-Editing-Mid-Execution/page

How to pause AI workflows to inspect and edit runtime state for debugging, corrections, and supervised overrides with safe interfaces

Why edit state mid-execution?

When building multi-step agents and dynamic workflows, there are times you need to pause execution to inspect, correct, or steer the flow. Enabling mid-execution state editing gives developers and authorized users a controlled way to intervene: change values, validate decisions, and then resume without restarting the whole process.

<Frame>
  <img alt="The image is a flowchart illustrating the concept of mid-execution state editing, showing steps where inspection and correction can occur in a process." />
</Frame>

How it works (high level)

Think of mid-execution editing as a runtime breakpoint for stateful AI logic. In platforms like [LangGraph](https://learn.kodekloud.com/user/courses/langgraph), execution pauses at designated checkpoints, exposes the current state dictionary to an external interface (UI, CLI, or API), and then continues once an updated state is returned. This enables quick fixes, interactive debugging, and supervised overrides without restarting the workflow.

A paused state snapshot might look like this:

```json theme={null}
{
  "status": "paused",
  "step": "2",
  "data": {
    "value": "..."
  }
}
```

Imagine Ravi pauses at a checkpoint, updates the delivery route in his logbook, and then resumes the workflow with the corrected information.

<Frame>
  <img alt="The image shows a diagram titled &#x22;Mid-Execution State Editing&#x22; with checkpoints marked along a line, connected to an illustration of a person leading to a logbook." />
</Frame>

Implementing pauses in LangGraph

There are two common approaches to pause a graph in LangGraph:

* Conditional edge: add a condition that evaluates to a paused state and triggers an external intervention.
* Custom pause node: create a node whose sole responsibility is to halt execution and surface the current state to an external system.

These pause mechanisms are typically paired with an admin dashboard, CLI, or API that allows an operator to inspect and update the state. Once the update is submitted and validated, a signal causes the graph to continue from the same point using the new values.

<Frame>
  <img alt="The image is about enabling editable pauses in LangGraph, showing two approaches: using a custom node or condition to pause, and exposing state to user/admin interface." />
</Frame>

Example: pausing and editing state in a custom node

The example below shows a simple Python pause node that exposes the current state via an interrupt function and resumes when the external editor or API returns an updated state:

```python theme={null}
from langgraph.types import interrupt

def editable_pause_node(state):
    # Pause execution and expose the current state to an external system
    updated_state = interrupt({
        "message": "Edit the state if needed before continuing",
        "state_snapshot": state
    })

    # Resume execution with the updated state
    return updated_state
```

During the pause, a user or automated system can inspect, validate, and modify state values. When the updated state is returned, the graph continues using those new values — effectively acting as a breakpoint for AI workflows.

Use cases for mid-execution editing

* Quick fixes when an agent produces unexpected outputs.
* Human-in-the-loop overrides where a supervisor reroutes or corrects decisions.
* Live tuning and experiment-driven development during testing phases.

<Frame>
  <img alt="The image outlines use cases for mid-execution editing, including quick fixes for unexpected behavior, human-in-the-loop overrides, and live tuning of logic and state during development." />
</Frame>

Front-end and integration options

To make mid-execution editing safe and usable, provide interfaces that let authorized actors view, edit, and validate state. Common integration points:

| Integration point | Description                                                                     | Example / Notes                                                                                    |
| ----------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Admin dashboard   | Browser-based JSON editor with schema validation and audit controls             | Use an embedded JSON editor + `POST /api/state/continue` to submit updates                         |
| CLI tools         | Developer-friendly tools for inspecting and patching state during local testing | `langgraph pause --id <checkpoint-id>` then `langgraph resume --file updated-state.json`           |
| Webhooks / API    | External services submit updates via a secure webhook or REST API               | Webhook payload: `{"checkpoint_id":"123","state": {"route":"A->B->C"}}` (validate before applying) |

Always enforce server-side validation, schema checks, and permission controls before accepting any edited state. Include clear error messaging if validation fails.

<Frame>
  <img alt="The image lists three front-end integration options: 1) Admin dashboards with state editors, 2) CLI tools for developers, 3) Webhooks for external systems." />
</Frame>

<Callout icon="warning">
  Editing state mid-execution is powerful but risky. Always log who changed what and when, enforce validation rules to prevent corrupt state, and restrict this capability in production to admin or trusted roles.
</Callout>

Best practices

* Audit every edit: capture user, timestamp, and before/after snapshots.
* Validate edited state against a schema or business rules before resuming.
* Limit editing to safe checkpoints and authorized roles.
* Use mid-execution editing primarily for debugging, supervised production interventions, and iterative development — avoid ad-hoc edits in critical automated pipelines.

Enabling state editing mid-execution gives teams a flexible, real-time way to manage complex flows. Whether debugging, experimenting, or supervising agent behavior, platforms like [LangGraph](https://learn.kodekloud.com/user/courses/langgraph) make interactive control straightforward when combined with proper interfaces and safeguards.

Links and references

* [LangGraph course and docs](https://learn.kodekloud.com/user/courses/langgraph)
* JSON schema validation: [https://json-schema.org/](https://json-schema.org/)
* Best practices for secure webhooks: [https://owasp.org/www-project-secure-headers/](https://owasp.org/www-project-secure-headers/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-cf65-40d3-a3c3-70fdfb767635/lesson/b6dd0044-d18d-4c7e-8f5b-2d04a729d0ad" />
</CardGroup>
