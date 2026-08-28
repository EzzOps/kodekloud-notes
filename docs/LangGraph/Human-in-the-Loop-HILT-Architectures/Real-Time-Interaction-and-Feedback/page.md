# Real Time Interaction and Feedback

Source: https://notes.kodekloud.com/docs/LangGraph/Human-in-the-Loop-HILT-Architectures/Real-Time-Interaction-and-Feedback/page

Describes LangGraph human-in-the-loop real time interaction patterns like pause nodes streaming and escape hatches enabling users to guide approve and provide feedback for safer interactive AI workflows

Real-time interaction lets users shape agent behavior as it happens. This capability is critical in high-stakes, safety-sensitive, or creative workflows where user intent can change quickly. Whether refining a draft, validating a medical suggestion, or steering a research assistant, immediate feedback improves trust, engagement, and final output quality.

Human-in-the-loop (HITL) treats the user as an active collaborator throughout the workflow — not only at the start or finish. In LangGraph, that can mean pausing execution for approval, waiting for clarifying input, or asking for an edit before continuing. The runtime supports conditional edges, streaming interfaces, and custom input gates so agents and humans can collaborate in real time.

<Frame>
  <img alt="The image is a flowchart illustrating the &#x22;Human-in-the-Loop&#x22; (HILT) process, showing how tasks are managed with human intervention for clarification and approval." />
</Frame>

Use case metaphor: imagine Ravi delivering a package. He knocks and waits. The recipient instructs, "Leave it by the garage." Ravi adapts in real time. Similarly, LangGraph workflows can pause and accept instructions from users mid-execution.

Common real-time HITL patterns

* Pause nodes that wait for user confirmation, edits, or approvals.
* Streaming tokens that reveal generation as it happens so users can react mid-stream.
* Escape hatches to cancel, reroute, or change execution flow.

| Pattern          | When to use                                           | Example behavior                                                           |
| ---------------- | ----------------------------------------------------- | -------------------------------------------------------------------------- |
| Pause nodes      | Need explicit human approval or edits                 | Halt execution until the user confirms or modifies content                 |
| Streaming tokens | Low-latency feedback and mid-generation interventions | Emit tokens incrementally to create a typing effect and allow cancellation |
| Escape hatches   | Safety, rerouting, or corrective flows                | Abort the current plan and follow an alternate branch                      |

<Frame>
  <img alt="The image outlines &#x22;Real-Time Feedback Patterns,&#x22; featuring a circular diagram with sections on pause nodes for user interaction, streaming tokens for mid-generation response, and escape hatches for execution control." />
</Frame>

Pausing execution for human input
LangGraph’s runtime provides an interrupt mechanism to pause a graph, persist state, surface a payload to an external UI or API, and then resume once the human responds. The payload displayed to the user can include a question, editable text, or UI controls. When the human replies, the runtime resumes the same node and returns the response as the result of the interrupt call.

Example: a simple interrupt node in Python

```python theme={null}
from typing import TypedDict
from langgraph.types import interrupt

class State(TypedDict):
    message: str

def human_input_node(state: State) -> dict:
    # Pause the graph and ask the human for input
    user_reply = interrupt({
        "question": "What would you like to change?"
    })

    # Execution resumes here once the human responds
    return {
        "message": user_reply
    }
```

How it works

* Hitting `interrupt` stops graph execution and persists the current node’s state.
* The runtime surfaces the interrupt payload to the UI or API.
* When the human responds, the graph resumes from the same node and the `interrupt` call returns the human response.
* Use cases: clarification requests, manual approvals, content edits, or safety checks.

Streaming model responses
Most LLM calls return a complete response after generation finishes. Streaming changes that: the model emits tokens incrementally, which reduces perceived latency and enables mid-generation interactions (like cancelling or adjusting prompts). Streaming is especially valuable for long outputs or interactive scenarios.

Example: enabling streaming with a typing-effect and accumulating the final answer

```python theme={null}
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(streaming=True)

def stream_response(state):
    response = ""
    for chunk in llm.stream(state["messages"]):
        # Print each incoming token immediately for a typing effect
        print(chunk.content, end="", flush=True)
        response += chunk.content

    # Append the completed response back into the conversation history
    return {"messages": state["messages"] + [response]}
```

Why streaming matters

* Users see progress as it happens instead of waiting for the full reply.
* Long responses feel faster and more interactive.
* Enables mid-generation interaction: users can interrupt, accept partial results, or steer the completion.

Collecting and recording user feedback
Feedback gathered during a LangGraph workflow can be treated as regular state and persisted for analytics, fine-tuning, or adaptive behavior. Use the same interrupt pattern to ask for feedback and then log or process it downstream.

Example: collect feedback then log it

```python theme={null}
from typing import TypedDict
from langgraph.types import interrupt

class State(TypedDict):
    messages: list
    feedback: str

def collect_feedback(state: State) -> dict:
    # Ask the user whether the response was helpful and pause execution
    feedback = interrupt({
        "question": "Was this response helpful?"
    })

    return {
        "feedback": feedback
    }

def log_feedback(state: State) -> dict:
    print("User feedback:", state["feedback"])
    return state
```

Design best practices for human-in-the-loop interfaces

* Set clear expectations: show when and why a user will be asked to act.
* Keep interactions focused: present one decision or edit at a time.
* Offer undo and retry flows so users can explore alternatives safely.
* Surface enough context for users to make informed decisions (previous messages, provenance, or rationale).
* Log interactions and metadata for auditing, analytics, and model improvement.

<Frame>
  <img alt="The image showcases three best practices for real-time user experience: setting clear expectations, avoiding overwhelming users with options, and allowing undo and retry flows. Each point is accompanied by an icon and a brief description." />
</Frame>

<Callout icon="lightbulb">
  When designing human-in-the-loop steps, avoid surprising users. Explain what control they have, what will happen next, and how they can undo or retry actions.
</Callout>

Conclusion
Human-in-the-loop is a deliberate collaboration strategy, not a fallback. By combining pause points, streaming, escape hatches, and feedback collection, LangGraph enables interactive workflows where humans actively correct, guide, and validate agent behavior. These primitives help teams build safer, more transparent, and more effective AI-powered experiences.

Links and references

* LangGraph concepts and runtime: [https://langgraph.example/docs](https://langgraph.example/docs)
* Streaming LLMs: [https://platform.openai.com/docs/guides/streaming](https://platform.openai.com/docs/guides/streaming)
* Human-in-the-loop design patterns: [https://www.usability.gov/ux-basics/ux-methods/human-in-the-loop.html](https://www.usability.gov/ux-basics/ux-methods/human-in-the-loop.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-4290-4d71-9531-0b12f54f10c6/lesson/1b0ad5b3-1be2-4f6a-8e28-2944e69d9c6a" />
</CardGroup>
