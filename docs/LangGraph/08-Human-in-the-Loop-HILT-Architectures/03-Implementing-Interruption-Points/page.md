# Example LangGraph approval node (conceptual)
from typing import TypedDict
from langgraph.types import interrupt

# Step 1: Define the graph state
class State(TypedDict):
    content: str
    approval: str

# Step 2: Pause and collect human approval
def review_node(state: State) -> dict:
    # `interrupt` sends the payload to the UI/human task system and returns the selected option.
    approval = interrupt({
        "question": "Do you approve this content?",
        "content": state["content"],
        "options": ["yes", "edit", "cancel"]
    })
    # Return the update to be merged into the graph state
    return {"approval": approval}

# Step 3: Route based on the human decision
def route_after_review(state: State) -> str:
    if state.get("approval") == "yes":
        return "proceed"
    elif state.get("approval") == "edit":
        return "modify"
    return "cancel"

# `builder` is an existing graph builder instance in your LangGraph setup.
# Map the routing function's outcomes to the next node IDs in the graph.
builder.add_conditional_edges(
    "review",                # node name where review happens
    route_after_review,      # routing function reading state
    {
        "proceed": "proceed",
        "modify": "modify",
        "cancel": "cancel"
    }
)
```

This wiring—pause for input, capture the decision, then route accordingly—makes the workflow interruptible, auditable, and human-aware.

<Callout icon="lightbulb">
  Design the frontend to clearly display the AI-generated content, available actions (approve, request changes, cancel), and contextual metadata (who generated it, timestamps, reason). Clear UI and context reduce friction and errors.
</Callout>

<Frame>
  <img alt="The image is a diagram showing a front-end design for approval, featuring sections for AI output, actionable options like &#x22;Approve&#x22; and &#x22;Request Changes,&#x22; and relevant context details. It emphasizes the importance of a clear UI for effective human-in-the-loop (HILT) interactions." />
</Frame>

When the human responds, the frontend posts the result back into LangGraph and the flow resumes using the defined routing logic.

Use cases

| Use Case                                | Description                                                             |
| --------------------------------------- | ----------------------------------------------------------------------- |
| Sending personalized emails or reports  | Human reviews and approves sensitive or customer-facing communications. |
| Drafting but not finalizing conclusions | Agent prepares a draft; human edits or approves the final version.      |
| Verifying sensitive data changes        | Human confirms updates to critical records before they are applied.     |

<Frame>
  <img alt="The image provides three use cases: sending personalized emails or reports, letting agents draft but not finalize conclusions, and verifying sensitive data modifications." />
</Frame>

Best practices

* Minimize unnecessary friction: require approvals only when risk or uncertainty justifies them.
* Log every decision: capture user ID, timestamp, and context for auditability.
* Design for traceability: keep a clear audit trail to review why specific choices were made.
* Gradually reduce approvals where appropriate: as the system proves reliable, allow trusted users or low-risk items to skip review.

<Frame>
  <img alt="The image illustrates &#x22;Best Practices&#x22; with two arrows, highlighting minimizing friction in UI and logging decisions with timestamps and user IDs." />
</Frame>

Takeaways

Approval nodes empower humans to guide agents responsibly. For legal compliance, brand safety, or operational peace of mind, they act as a safety valve—letting you benefit from automation while maintaining human control.

<Frame>
  <img alt="The image is a slide titled &#x22;Takeaways&#x22; that lists three key points about the importance of approval nodes in guiding agents, acting as a safety valve, and being useful for legal and risk-sensitive workflows." />
</Frame>

In LangGraph, human approval nodes are another flow element—pause, collect human input, and route based on the result—making your workflows safe, auditable, and adaptable.

Links and references

* [LangGraph documentation](https://langgraph.ai/docs)
* [Human-in-the-loop (HITL) design patterns (overview)](https://en.wikipedia.org/wiki/Human-in-the-loop)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/0512078c-4290-4d71-9531-0b12f54f10c6/lesson/33409ca8-8f6c-4388-be5c-b5ffa89bb893" />
</CardGroup>


# Implementing Interruption Points

Source: https://notes.kodekloud.com/docs/LangGraph/Human-in-the-Loop-HILT-Architectures/Implementing-Interruption-Points/page

Explains human-in-the-loop interruption points in LangGraph, pausing workflows for human approval, implementation details, examples, front-end integration, and best practices.

Interruption points (human-in-the-loop gates) let users pause or stop an agent before it completes an action. These checkpoints give humans oversight and control in scenarios with consequences—approving contract clauses, sending emails, or deleting records—so the system behaves cooperatively rather than as an opaque autonomous process.

<Frame>
  <img alt="The image highlights the value of interruption points for oversight and control, specifically in processes like approving a contract clause and sending an email." />
</Frame>

Benefits

* Reduce risk by requiring explicit human approval for sensitive steps.
* Improve collaboration by letting humans inspect, edit, or reject AI-generated outputs.
* Increase trust and compliance for workflows involving legal, financial, or destructive actions.

In LangGraph, an interruption point is modeled as a node that pauses execution and waits for human interaction. Based on that interaction, the graph takes different edges: proceed, retry, or cancel. Think of it as a decision gate—the graph only advances once the user chooses a path.

<Frame>
  <img alt="The image is an overview of interruption points, featuring an interruption node represented by a hexagon and an hourglass, along with a &#x22;Human Input Gate&#x22; where flow pauses until a decision is made." />
</Frame>

Real-world example: delivery confirmation
Robbie pauses before leaving a package—waiting for a signature or an instruction such as “leave it at the back door.” That signature is an interruption point: the delivery workflow halts until a human provides a decision.

<Frame>
  <img alt="The image depicts an overview of interruption points in a delivery process, showing a person with a package, an hourglass, a signature requirement, and a house, with a note about leaving the package by the back door." />
</Frame>

How LangGraph implements interruption points
LangGraph uses conditional edges that check flags in the graph state (for example, `user_confirmed == True`). The execution pauses until a corresponding flag is set. Input can arrive via a UI, webhook, or API event; once received, the graph resumes along the matching edge. This event-driven approach keeps the design clean and auditable.

Implementation workflow (high level)

1. Define the graph state to include fields that store the data needing review.
2. Create an interruption node that represents the human review step.
3. Pause execution using the `interrupt` function—this saves state and emits a payload for the front end.
4. Resume the graph when human input is returned, updating the state and continuing execution.

Steps to implement interruption points

| Step                     | What to do                                                              | Example / Notes                                |
| ------------------------ | ----------------------------------------------------------------------- | ---------------------------------------------- |
| Define graph state       | Store the data that will be presented to a human reviewer.              | `{"some_text": "draft email body"}`            |
| Create interruption node | Add a node that pauses and waits for input.                             | A node named `human_review_node`               |
| Pause with `interrupt`   | Use `interrupt()` to save state and send payloads to UI/webhook.        | See the code example below                     |
| Resume and branch        | On input, update state and choose the next edge (approve/retry/cancel). | Conditional edges: `if approved -> send_email` |

Example node implementation
The following Python example shows a simple interruption node that stops the graph, sends text to a reviewer, and resumes with the revised text.

```python theme={null}
from typing import TypedDict
from langgraph.types import interrupt

class State(TypedDict):
    some_text: str

def human_review_node(state: State) -> State:
    # Pause the graph and send the text to the UI for review.
    revised_text: str = interrupt({
        "text_to_review": state["some_text"]
    })

    # Resume the graph with the revised text.
    return {
        "some_text": revised_text
    }
```

How the pause works

* When `interrupt(...)` executes, the current graph execution stops and the runtime persists the current state.
* A payload is emitted to configured endpoints (UI, API, dashboard, or webhook).
* The external system presents the content to a human for approval, editing, or cancellation.
* Once a response arrives, the runtime resumes execution from the same node and returns the user-provided value.

Front-end integration
When the graph pauses, the front end should present the draft or decision with explicit choices (approve, edit, cancel). The UI sends the result back through an API event or webhook so LangGraph can continue.

<Frame>
  <img alt="The image is a flowchart depicting the process of integrating with a front end, involving LangGraph execution, user actions, and sending API events such as approval, rejection, or feedback." />
</Frame>

Common use cases

* Image generation: let a user approve or refine generated images before publishing.
* Data deletion: require confirmation before wiping records.
* Legal or financial advice: require human sign-off on recommendations.

<Frame>
  <img alt="The image depicts two use cases for interruption: &#x22;Email Generation,&#x22; prompting with &#x22;Do you want to send this?&#x22; and &#x22;Data Detection,&#x22; with &#x22;Confirm before wiping records.&#x22;" />
</Frame>

Best practices

<Frame>
  <img alt="The image lists three best practices with icons: make decision points clear and simple, always allow a safe fallback, and avoid blocking flows unnecessarily." />
</Frame>

<Callout icon="lightbulb">
  When designing interruption points, be explicit in the UI about what each decision means. Provide clear options (approve, edit, cancel), allow safe fallbacks, and avoid pausing the flow for trivial matters. Only interrupt where user input improves safety, trust, or personalization.
</Callout>

Concise best-practice checklist

* Make decision points clear and minimal—only pause for high-value human input.
* Provide safe fallbacks (e.g., “undo”, “retry”, or default timeouts).
* Avoid blocking flows unnecessarily—use timeouts or automated fallbacks when appropriate.
* Log all human interactions for auditability and compliance.

With well-designed interruption points, agents become cooperative partners: they ask before they act and allow humans to steer workflows. In LangGraph, this pattern is straightforward to implement using stateful nodes, conditional edges, and front-end callbacks.

Links and references

* LangGraph course: [https://learn.kodekloud.com/user/courses/langgraph](https://learn.kodekloud.com/user/courses/langgraph)
* Human-in-the-loop design patterns and best practices (general reading)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/langgraph/module/0512078c-4290-4d71-9531-0b12f54f10c6/lesson/aec3961d-bbb5-473b-9c8e-7b56a12ebd25" />
</CardGroup>
