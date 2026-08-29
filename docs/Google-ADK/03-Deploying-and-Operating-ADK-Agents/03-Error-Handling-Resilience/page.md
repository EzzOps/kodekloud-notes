# Example: conceptual use of session.state for an ongoing VPN troubleshooting conversation
session.state["issue_type"] = "vpn_connectivity"
session.state["progress"] = {"current_step": "verify_credentials", "attempts": 1}
session.state["user_email"] = "alice@example.com"
```

<Frame>
  <img alt="An infographic titled &#x22;What Should Live in State?&#x22; showing four colored boxes: Task Progress, Flags & Decisions, User Preferences, and Temporary Scratch Data, each with a short explanation of what to store. A footer notes that state stores only what matters for decision-making and continuity across turns." />
</Frame>

## What belongs in state

Store only the small set of values that help the agent make decisions and continue a flow — not a verbatim copy of the transcript.

| Category               | Purpose                                      | Examples                                 |
| ---------------------- | -------------------------------------------- | ---------------------------------------- |
| Task progress          | Where you are in a multi-step process        | `onboarding:step_2`, `asking_email`      |
| Flags & decisions      | Branching or escalation markers              | `requires_escalation: True`              |
| User preferences       | Settings that affect behavior                | `locale: "en-US"`, `theme: "dark"`       |
| Temporary scratch data | Short-lived parsed values used within a step | validation results, extracted entity IDs |

Use state for decision-making and continuity; keep it minimal and purposeful.

## State key prefixes: scoping your data

ADK supports key prefixes to control the lifecycle and scope of state values. Prefixes make it easy to reason about how long values should live and who they apply to.

<Frame>
  <img alt="A presentation slide titled &#x22;State Key Prefixes: Scoping Your Data&#x22; showing four colored panels (user:, app:, No prefix, temp:) with bullet points explaining each prefix’s data scope and lifecycle. It summarizes how prefix-based state keys control data across calls, sessions, users, and the app." />
</Frame>

| Prefix      | Scope                               | Typical lifecycle / use                                  |
| ----------- | ----------------------------------- | -------------------------------------------------------- |
| `user:`     | Per-user, persisted across sessions | Long-lived user preferences and user profile metadata    |
| `app:`      | App-wide, shared across users       | Global configuration or app-wide flags                   |
| (no prefix) | Session-scoped                      | Values that live for the current session only            |
| `temp:`     | Invocation-scoped                   | Ephemeral scratch data used only for a single model call |

Prefixing keys keeps state predictable: use `temp:` for per-invocation scratch, session keys for conversation continuity, `user:` for persistent preferences, and `app:` for global settings.

> **lightbulb** Keep state minimal and purposeful. Start with the smallest set of values that let the agent complete the flow, then expand only when necessary.

## State strategy for our help desk assistant

For a help desk assistant, keep state intentionally small. Track only what you need to run the troubleshooting flow: the current issue type, troubleshooting progress, and any contextual user information that influences decisions. Avoid over-engineering state early; you can expand the schema as needs arise.

<Frame>
  <img alt="A presentation slide titled &#x22;State Strategy for Our Helpdesk Assistant&#x22; that outlines what to track: current issue, troubleshooting progress, and user context. It emphasizes minimal/purposeful storage and future user preferences." />
</Frame>

## Injecting state into agent instructions (dynamic prompts)

A powerful ADK feature is automatic injection of state values into agent instruction templates. Write instruction templates with placeholders (for example, `{topic}` or `{issue_type}`), set `session.state` values, and ADK will replace those placeholders before sending the prompt to the LLM. This keeps templates simple and behavior context-aware without manual prompt assembly.

<Frame>
  <img alt="A three-step diagram titled &#x22;Dynamic Instructions: Injecting State Into LLM Prompts.&#x22; It shows 01 Define Template (create instructions with key placeholders), 02 Set State (update session.state with actual values), and 03 Automatic Injection (ADK replaces placeholders before sending to the LLM)." />
</Frame>

Example: defining an LLM agent with a placeholder

```python theme={null}
from google.adk.agents import LlmAgent

story_generator = LlmAgent(
    name="StoryGenerator",
    model="gemini-2.0-flash",
    instruction="Write a short story about a cat, focusing on the theme: {topic}."
)
```

If you set `session.state["topic"] = "friendship"`, ADK will automatically replace `{topic}` with `"friendship"` before calling the model.

## Automatic state updates: output\_key and state deltas

ADK provides two primary ways to update state from agent runs:

* output\_key — a simple option where the agent’s final response is saved into `session.state` under the provided key.
* state delta / events — an advanced mechanism that emits precise state-change events for fine-grained control over updates (recommended for production workflows that require deterministic state changes).

| Method                | When to use                       | Behavior                                                                  |
| --------------------- | --------------------------------- | ------------------------------------------------------------------------- |
| `output_key`          | Quick and simple persistence      | Saves the agent's final text to `session.state["key"]` automatically      |
| State deltas / events | Production control and validation | Emit explicit state-change events describing exactly what to write/remove |

Example: using `output_key` to capture the last greeting

```python theme={null}
from google.adk.agents import LlmAgent

greeting_agent = LlmAgent(
    name="Greeter",
    model="gemini-2.0-flash",
    instruction="Generate a short, friendly greeting.",
    output_key="last_greeting"  # ADK will save the agent's response into session.state["last_greeting"]
)
```

When this agent runs, ADK automatically stores the final greeting into `session.state["last_greeting"]`. For production systems where you need exact control over what changes and when, use state-delta events instead.

## Putting it together: a multi-step troubleshooting flow

A typical smart IT help desk assistant models a structured flow:

1. Problem clarification — ask focused questions to identify the exact issue.
2. Information gathering — collect required details (email, system ID).
3. Tool execution — call tools to look up user data or check service status.
4. Solution and next steps — present resolution or escalate.

Use `session.state` to track progress across these steps so the agent can pick up where it left off and follow deterministic workflows.

<Frame>
  <img alt="A slide titled &#x22;Applying State to Our Helpdesk Assistant&#x22; showing a state-management flow with three steps: Problem Clarification, Information Gathering, and Tool Execution. Each step is connected to a central timeline with numbered nodes and brief descriptions of the agent actions (ask focused questions, collect user/system details, invoke tools)." />
</Frame>

## What’s next

Next, we'll design a complete troubleshooting flow and address key design choices:

* How many clarifying questions to ask and when to stop
* When and how to invoke tools
* How to author instructions for predictable LLM behavior
* Guardrails and validation to ensure reliable enterprise workflows

You’ll learn how to balance conversational flexibility with structured reliability so the agent maps natural language into structured data requests and returns structured results.

<Frame>
  <img alt="A presentation slide titled &#x22;Next: Designing the Troubleshooting Flow&#x22; that lists five upcoming agenda items about building an end-to-end troubleshooting flow (clarifying questions, invoking tools, structuring LLM instructions, and applying guardrails). The slide has a dark teal background with numbered circular icons down the left and brief descriptions to the right." />
</Frame>

> **warning** Avoid storing sensitive personal data in long-lived state fields. Favor `session`- or `temp`-scoped keys for transient data and ensure you comply with your organization’s privacy and retention policies.

## Links and references

* [Google ADK documentation](https://developers.google.com/ai/adk) — ADK reference and guides
* [Designing stateful conversational agents](https://developers.google.com/ai/adk/guides/state) — patterns and best practices
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) — (general reference for deploying back-end tools)

Use these resources to deepen your understanding of stateful agents and to guide production-ready designs.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/ee2729d1-2b89-4a41-b21d-f245c7372cc9/lesson/bd5202c1-6de5-429b-8e07-63d4e8ba2e6c)


# Error Handling Resilience

Source: https://notes.kodekloud.com/docs/Google-ADK/Deploying-and-Operating-ADK-Agents/Error-Handling-Resilience/page

Guidelines for implementing structured error handling in LLM agents and tools to produce predictable, machine readable failures and helpful user facing messages while keeping sessions resilient

All right — we have an agent running and performing non-trivial tasks. In this lesson we'll add robust error handling so the agent behaves predictably and remains resilient when tools fail.

<Frame>
  <img alt="A presentation slide titled &#x22;Error Handling & Resilience&#x22; with a large &#x22;Demo&#x22; label on a dark curved panel to the right. Small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left." />
</Frame>

Goals for tool and agent behavior

* Tools fail gracefully and return clear, structured error signals.
* The agent does not crash or leave sessions in a broken state.
* Users always receive a helpful next step (for example: “please restart the service”, “check this file”, or “contact IT”).

ADK supplies management for sessions, tools, and traces, but it is our responsibility to ensure tools return consistent, structured success/failure information that the LLM can reliably interpret.

> **lightbulb** Always return structured results from tools so the LLM can interpret failures and produce helpful user-facing messages.

Why structured tool responses matter

* Traditional apps throw exceptions, log them, and show a message. LLM-driven agents need machine-readable failure signals.
* Convert failures into a predictable structured object so the model can:
  * Recognize failure as a structured signal (not a raw stack trace).
  * Produce concise, user-friendly explanations and next steps.
* This reduces hallucinations, keeps sessions alive, and enables consistent user experience.

Note about structured returns

* Instead of letting an exception bubble up as an unstructured Python stack trace, catch exceptions and return a structured object with:
  * status: "success" | "error"
  * payload fields (e.g., "ticket", "service", "status\_text")
  * error\_message: user-facing text and optional short technical hint (exception type or brief details)

Tool registration and basic imports

```python theme={null}
from typing import Dict, Any
from google.adk.tools import FunctionTool
from google.adk.agents.llm_agent import Agent
from google.adk.agents import LlmAgent
