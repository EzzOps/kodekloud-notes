# imports
from typing import TypedDict
from dataclasses import dataclass
import copy
```

Define the workflow state type:

```python theme={null}
class ReviewState(TypedDict):
    content: str
    approval: str
    status: str
```

Next, define a simple `InterruptRequest` dataclass to represent a pause/interrupt. In a real runtime, invoking an interrupt would hand control back to the host with a payload describing what needs review.

```python theme={null}
@dataclass
class InterruptRequest:
    payload: dict

    @staticmethod
    def interrupt(payload: dict) -> "InterruptRequest":
        """Create an interrupt request with the given payload."""
        return InterruptRequest(payload=payload)
```

## Workflow nodes: generate, interrupt, resume

Below are the three main nodes in this simulated workflow: content generation, issuing an interrupt, and resuming based on a decision.

```python theme={null}
def generate_content(state: ReviewState) -> ReviewState:
    state = copy.deepcopy(state)
    state["content"] = "Draft: This is the generated content that requires review."
    state["status"] = "needs_review"
    return state


def request_review(state: ReviewState) -> InterruptRequest:
    """Simulate a node issuing an interrupt for human review."""
    payload = {
        "content": state["content"],
        "reason": "Please approve or request changes."
    }
    return InterruptRequest.interrupt(payload=payload)


def resume_workflow(state: ReviewState, approval: str) -> ReviewState:
    """Continue workflow based on the approval decision."""
    state = copy.deepcopy(state)
    state["approval"] = approval
    if approval.lower() in ("approved", "approve", "yes"):
        state["status"] = "approved"
    else:
        state["status"] = "changes_requested"
    return state
```

## State and function summary

Use the following table to quickly understand the state fields and the purpose of each function in this demo.

| Item                               | Description                                                | Example / Notes                                                    |
| ---------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------ |
| `ReviewState` fields               | State passed between workflow nodes                        | `{"content": "", "approval": "", "status": "started"}`             |
| `content`                          | The generated draft or artifact requiring review           | `"Draft: This is the generated content that requires review."`     |
| `approval`                         | Decision returned by the reviewer                          | `"approved"` or `"changes_requested"`                              |
| `status`                           | Current lifecycle status of the state                      | `"started"`, `"needs_review"`, `"approved"`, `"changes_requested"` |
| `generate_content(state)`          | Produces initial content and sets status to `needs_review` | Returns updated `ReviewState`                                      |
| `request_review(state)`            | Emits an `InterruptRequest` with review payload            | Simulates a runtime interrupt                                      |
| `resume_workflow(state, approval)` | Reconciles the decision and updates status                 | Returns updated `ReviewState`                                      |

## Example run (end-to-end)

This block shows the full flow: initialize state, generate content, request review (interrupt), then resume after a simulated reviewer decision.

```python theme={null}
# initial state
state: ReviewState = {
    "content": "",
    "approval": "",
    "status": "started"
}

# Step 1: generate content
state = generate_content(state)
print("After generation:", state)
# Step 2: interrupt for review
interrupt = request_review(state)
print("Interrupt payload:", interrupt.payload)
# (External human reviews the payload and returns a decision.)
# Simulate a reviewer decision:
decision = "approved"  # or "changes_requested"

# Step 3: resume workflow with the decision
state = resume_workflow(state, decision)
print("After resume:", state)
# After resume: {'content': 'Draft: This is the generated content that requires review.', 'approval': 'approved', 'status': 'approved'}
```

## How this maps to workflow runtimes

* The `InterruptRequest` models the runtime interrupt object you would encounter when a node pauses for external input in a workflow system.
* The `payload` contains only the minimal necessary data for a human reviewer; in production this can be extended with metadata, links to artifacts, or audit IDs.
* When the external decision returns, the workflow runtime or controller reconciles state and resumes processing from the same logical point, preserving idempotency and traceability.
* This pattern enables manual checks, approvals, gated deployments, or other human approvals within otherwise automated processes.

<Callout icon="lightbulb">
  In production systems, interrupts are typically implemented as runtime primitives that persist state, emit events/notifications, and secure the review channel. Use this pattern to model human review gates while keeping your core workflow logic deterministic and resumable.
</Callout>

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Workflow Patterns and Best Practices](https://martinfowler.com/articles/workflow-patterns.html)
* [Designing Human-in-the-Loop Systems — Research and Guidelines](https://www.microsoft.com/en-us/research/publication/human-in-the-loop/)

This pattern is a practical approach to integrating manual approvals into automated workflows while maintaining clarity, auditability, and the ability to resume execution from a known state.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-4290-4d71-9531-0b12f54f10c6/lesson/aca8613b-e199-4adc-8d6e-668daecdd6be" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.[SECRET_REDACTED]-4290-4d71-9531-0b12f54f10c6/lesson/5c16785f-b42f-4856-bd6c-ef1845fa1881" />
</CardGroup>


# Designing Human Approval Nodes

Source: https://notes.kodekloud.com/docs/LangGraph/Human-in-the-Loop-HILT-Architectures/Designing-Human-Approval-Nodes/page

Designing human approval nodes that pause automated workflows for human review, capture decisions, and route actions to ensure safe, auditable, and controllable automation

Human approval nodes are essential when you need explicit human oversight before an agent takes an action—examples include sending sensitive emails, updating critical records, or confirming recommendations in production systems. These nodes improve trust, control, and compliance by pausing an automated flow until a person verifies or modifies the output.

<Frame>
  <img alt="The image is a diagram explaining why human approval nodes matter, highlighting tasks like sending sensitive emails, updating records, and confirming recommendations." />
</Frame>

At a high level, a human approval node gives the user the final say before the agent proceeds. That final check reduces risk and enables safe automation in professional environments.

<Frame>
  <img alt="The image is a flowchart explaining the importance of &#x22;Human Approval Nodes,&#x22; depicting a sequence from &#x22;Agent&#x22; to &#x22;Action Executes,&#x22; highlighting trustworthiness and control." />
</Frame>

What is a human approval node?

A human approval node is a custom LangGraph node that interrupts the graph execution, sends the generated payload to a frontend or human tasking system, waits for the reviewer’s decision, and then resumes the graph with routing based on that decision.

<Frame>
  <img alt="The image illustrates an overview of a &#x22;Human Approval Node&#x22; process, showing a connection between a LangGraph node and a human waiting for a response." />
</Frame>

The reviewer can confirm the agent’s output, request edits, or cancel the flow. After the response is recorded, the graph routes to different branches (e.g., proceed, modify, cancel)—similar to verifying a fragile delivery address before dropping off a package.

<Frame>
  <img alt="The image is an illustration labeled &#x22;Human Approval Node – Overview,&#x22; showing a person requesting confirmation of a drop-off location with text and icons representing a fragile package and a user." />
</Frame>

Common implementation pattern (interrupt + resume)

In LangGraph, human approval nodes typically follow an interruption pattern:

* Pause at a node and send a payload (question, content, options) to the frontend or tasking system.
* Wait for the human to respond.
* Resume the graph and route according to the recorded decision.

This pattern is widely used where outputs must not be executed without human review—for example, client-facing summaries, legal or financial changes, and other sensitive operations.

Three main steps (concise example)

* Step 1 — Define the state\
  Store the content to be reviewed and the approval decision in the graph state.

* Step 2 — Pause and collect human approval\
  The approval node triggers an interrupt to the UI/human task system and waits for a response.

* Step 3 — Route based on the decision\
  A routing function reads the updated state and chooses the next edge in the graph.

Example (conceptual LangGraph approval node):

```python theme={null}
