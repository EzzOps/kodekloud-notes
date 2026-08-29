# schemas/ticket.py
from typing import Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Ticket(BaseModel):
    """Schema for an IT helpdesk ticket."""
    ticket_id: str = Field(
        description="Human-readable ID for the ticket, e.g. IT-1A2B3C4D."
    )
    summary: str = Field(
        description="Short summary of the user's issue."
    )
    service: str = Field(
        description="The affected service, e.g. 'email', 'vpn', 'gitlab', 'wifi'."
    )
    user_email: str = Field(
        description="The user's work email address related to this ticket."
    )
    severity: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Severity of the issue based on impact and urgency.",
    )
    status: Literal["open", "in_progress", "resolved"] = Field(
        default="open",
        description="Current status of the ticket in the helpdesk workflow.",
    )
    department: Optional[str] = Field(
        default=None,
        description="User's department, if known.",
    )
    created_at: datetime = Field(
        description="When the ticket was created (UTC).",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="When the ticket was last updated (UTC).",
    )
```

References:

* Pydantic docs: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

## 2) Typed tool input: CreateTicketArgs

Define a typed input model for the create-ticket tool. This ensures the tool receives validated input and makes intent explicit.

Example `CreateTicketArgs` (place this inside `tools/helpdesk_tools.py` or a shared module):

```python theme={null}
from pydantic import BaseModel, Field
from typing import Optional, Literal

class CreateTicketArgs(BaseModel):
    summary: str = Field(description="Concise summary of the issue in the agent's words.")
    description: Optional[str] = Field(default=None, description="Longer description from the user, if provided.")
    service: str = Field(description="Affected service, e.g., 'email', 'vpn', 'gitlab', 'wifi'.")
    user_email: Optional[str] = Field(default=None, description="User's email address, if known.")
    severity: Literal["low", "medium", "high"] = Field(default="medium", description="Impact-based severity.")
    department: Optional[str] = Field(default=None, description="User's department, if known.")
```

## 3) Tool implementations (lookup, service status, create ticket)

Move domain logic into `tools/helpdesk_tools.py`. For the demo we use simple in-memory backends and return structured dicts indicating "status" plus result payload or error message.

Example excerpts for `tools/helpdesk_tools.py`:

```python theme={null}
# tools/helpdesk_tools.py
from typing import Dict, Any
from datetime import datetime
import uuid

from pydantic import BaseModel
from ..schemas.ticket import Ticket  # relative import when tools/ and schemas/ are sibling packages
from .helpdesk_tools import CreateTicketArgs  # if CreateTicketArgs is in this module, adjust accordingly

# Fake backends (demo)
_FAKE_USER_DIRECTORY: Dict[str, Dict[str, Any]] = {
    "alice@example.com": {"email": "alice@example.com", "name": "Alice", "status": "active", "department": "Engineering"},
    # add more as needed
}

_FAKE_SERVICE_STATUS: Dict[str, str] = {
    "vpn": "degraded",
    "email": "operational",
    "gitlab": "outage",
    "wifi": "operational",
}

def lookup_user_impl(email: str) -> Dict[str, Any]:
    """Look up a user in the internal directory.

    Returns:
        dict: { "status": "success" | "error", "user": {...}, "error_message": "..." }
    """
    if not email:
        return {"status": "error", "error_message": "No email provided."}

    user = _FAKE_USER_DIRECTORY.get(email.lower())
    if not user:
        return {
            "status": "error",
            "error_message": f"No user found for email '{email}'.",
        }
    return {"status": "success", "user": user}

def check_service_status_impl(service_name: str) -> Dict[str, Any]:
    """Check the known fake service status map.

    Returns:
        dict: {
            "status": "success" | "error",
            "service": normalized_name,
            "status_text": "operational" | "degraded" | "outage",
            "error_message": "..."
        }
    """
    if not service_name:
        return {"status": "error", "error_message": "No service name provided."}

    normalized = service_name.strip().lower()
    status = _FAKE_SERVICE_STATUS.get(normalized)
    if not status:
        return {
            "status": "error",
            "error_message": (
                f"Unknown service '{service_name}'. "
                f"Known services: {', '.join(sorted(_FAKE_SERVICE_STATUS.keys()))}."
            ),
        }
    return {
        "status": "success",
        "service": normalized,
        "status_text": status,
    }

def create_ticket_impl(args: CreateTicketArgs) -> Dict[str, Any]:
    """Create a validated Ticket object and return it as a dict."""
    ticket_id = f"IT-{uuid.uuid4().hex[:8].upper()}"
    ticket = Ticket(
        ticket_id=ticket_id,
        summary=args.summary,
        service=args.service.lower(),
        user_email=(args.user_email or "").lower(),
        severity=args.severity,
        status="open",
        department=args.department,
        created_at=datetime.utcnow(),
        updated_at=None,
    )
    # Use model_dump() for Pydantic v2 compatibility; .dict() for v1.
    return {"status": "success", "ticket": ticket.model_dump()}
```

Notes:

* These implementations always return a small structured dict with a `status` field. This makes it easy for the agent to branch on success vs error.
* In a real system, replace fake backends with database calls, API clients, or ticketing system integrations.

## 4) Wrapping tools for the agent

In your agent module you wrap these functions with FunctionTool so the agent can call them. The agent keeps instruction and orchestration logic, while tools encapsulate domain behavior and validation.

Example `agent.py` excerpt:

```python theme={null}
# agent.py (excerpt)
from google.adk.tools import FunctionTool
from tools.helpdesk_tools import (
    lookup_user_impl,
    check_service_status_impl,
    create_ticket_impl,
)

lookup_user_tool = FunctionTool(func=lookup_user_impl, name="lookup_user")
check_service_status_tool = FunctionTool(func=check_service_status_impl, name="check_service_status")
create_ticket_tool = FunctionTool(func=create_ticket_impl, name="create_ticket")

root_agent = Agent(
    model='gemini-2.5-flash',
    name="helpdesk_root_agent",
    description=(
        "Smart IT Helpdesk assistant that troubleshoots common IT issues "
        "using clarifying questions and internal tools."
    ),
    instruction=(
        "You are a friendly but efficient IT helpdesk assistant for an internal company.\n"
        "\n"
        "You are running inside a multi-turn session. ADK will provide tools you can call.\n"
        "1) Use tools when it adds value:\n"
        "   - Call 'lookup_user' when you have an email and it would help to know account status.\n"
        "   - Call 'check_service_status' when the issue involves a known service (email, vpn, gitlab, wifi).\n"
        "2) Decide whether to create a ticket:\n"
        "   - Create a ticket if the issue is severe, troubleshooting didn't resolve it, or the user asks.\n"
        "   - If creating a ticket, call 'create_ticket' with the fields: summary, service, user_email, severity.\n"
        "3) Give next steps: concise numbered steps or suggestions based on tool results.\n"
    ),
    tools=[lookup_user_tool, check_service_status_tool, create_ticket_tool],
)
```

<Callout icon="lightbulb">
  Using tool-level structured outputs (tools return validated dicts produced from Pydantic models) provides strong guarantees about data shape while still letting the LLM decide when and how to call those tools.
</Callout>

## 5) Example run (console)

A typical session shows the agent calling tools, receiving structured outputs, and creating a ticket:

```console theme={null}
(.venv) jeremy@MACSTUDIO ticketpro % ADK run helpdesk_agent
Running agent helpdesk_root_agent, type exit to exit.
[user]: I've been completely unable to connect to the VPN all morning, and our whole team is blocked. My email is alice@example.com
[helpdesk_root_agent]: Thanks, Alice. I've checked into this, and it looks like the VPN service is currently degraded. This means it's experiencing issues, which is likely why you and your team are blocked.

I'm creating a high-priority ticket for this so our IT team can investigate further and work on a resolution.

I've opened a ticket for you: IT-811464F0.

Summary: Your team is unable to connect to the VPN because the service is currently degraded.
Service: VPN
Severity: High

Next Steps:
1. Our IT team is aware of the degraded VPN service and is actively working on it.
2. Please monitor company announcements for updates on the VPN status.
3. You can try connecting to the VPN again periodically.
[user]:
```

Behind the scenes

* The agent called `check_service_status` and received a structured response: `{status: "success", service: "vpn", status_text: "degraded"}`.
* Given the impact, the agent built a `CreateTicketArgs` payload and invoked `create_ticket`.
* `create_ticket_impl` instantiated the `Ticket` Pydantic model, validated it, and returned `ticket.model_dump()` as a structured result.
* The resulting dict can be logged, stored in a database, or sent to a ticketing API.

Summary

* Refactored the demo into `schemas/` and `tools/`.
* Added a Pydantic `Ticket` model and a typed create-ticket tool that returns a validated ticket dictionary.
* Moved domain logic into tools and left the agent focused on orchestration and instructions.
* This pattern—tool-level structured outputs + typed inputs—maintains LLM flexibility while guaranteeing reliable data shapes for downstream systems.

Next steps

* Add grounding sources (internal IT policies, runbooks) so the agent consults authoritative documentation.
* Integrate a real user directory and ticketing API to replace demo backends.
* Add telemetry and audit logging for ticket creation and tool calls.

Links and references

* Pydantic: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
* Python datetime docs: [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
* Python uuid docs: [https://docs.python.org/3/library/uuid.html](https://docs.python.org/3/library/uuid.html)
* (ADK) Consult your ADK provider docs for FunctionTool and agent runtime specifics.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-adk/module/672589ad-758d-4e70-8408-bd4bd4409388/lesson/a642dd26-c60e-41c7-a1d7-0782775d86b5" />
</CardGroup>


# Why Structured Outputs Matter and How ADK Handles Them

Source: https://notes.kodekloud.com/docs/Google-ADK/Deploying-and-Operating-ADK-Agents/Why-Structured-Outputs-Matter-and-How-ADK-Handles-Them/page

Explains why structured outputs are important and how ADK uses agent schemas and tool-level structured results for reliable help desk ticketing workflows.

Most large language models (LLMs) produce free-form text by default. While natural for conversation, unstructured responses are brittle when you need machine-readable results. Common problems include:

* Difficulty reliably extracting structured fields (IDs, statuses, severities).
* Inconsistent severity labels (low/medium/high) across responses.
* Unpredictable formats that break downstream integrations (databases, APIs, analytics).

These are exactly the issues we face in our help desk ticketing workflow: model replies are stochastic and freeform, so we can’t dependably populate ticket fields.

<Frame>
  <img alt="A presentation slide titled &#x22;Free-Text vs Structured Output&#x22; showing three numbered panels. Each panel lists a use case where free-text is weak: extracting tickets from text, standardizing severity levels, and producing API-ready structured fields." />
</Frame>

ADK provides two primary ways to get structured outputs instead of raw text:

1. Agent-level schemas (input and output models).
2. Tool-level structured results (tools that return typed objects).

This guide compares both approaches and shows why we’ll use tool-level structured outputs for our help desk assistant.

<Frame>
  <img alt="A dark-themed slide titled &#x22;ADK's Structured Output Options&#x22; showing two circular icons and labels: &#x22;Agent-Level Schemas&#x22; (database icon) with the caption &#x22;Facilitate structured agent interactions,&#x22; and &#x22;Tool-Level Structured Results&#x22; (toolbox icon) with the caption &#x22;Ensure organized and interpretable output.&#x22;" />
</Frame>

|                      Approach | Best for                                                                  | Key tradeoffs                                                            |
| ----------------------------: | ------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
|           Agent-level schemas | Single-step, deterministic lookups or function-like agents                | Strongly typed outputs but limited tool use and orchestration            |
| Tool-level structured results | Multi-step workflows that call tools, use RAG, or integrate with services | Flexible orchestration; requires each tool to guarantee its return shape |

## Agent-level schemas (typed agents)

Agent-level schemas let you give an ADK agent explicit input and output models (for example, Pydantic classes). This makes the agent behave like a typed function: it accepts structured inputs and is guided to return a fixed JSON shape.

<Frame>
  <img alt="A presentation slide titled &#x22;Agent-Level Structured Outputs&#x22; showing two colorful cards labeled &#x22;input_schema&#x22; (teal) and &#x22;output_schema&#x22; (orange), which describe Pydantic models for what an agent expects and should return." />
</Frame>

Example — an agent that returns the capital of a country. We define a small Pydantic model for the output and pass it as the agent's `output_schema`. ADK steers the model to emit JSON matching that schema so the system reliably receives a `capital` field instead of a paragraph.

```python theme={null}
from pydantic import BaseModel, Field
from google.adk.agents import Agent

class CapitalOutput(BaseModel):
    capital: str = Field(description="The capital of the country.")

capital_agent = Agent(
    name="capital_agent",
    model="gemini-2.5-flash",
    instruction="Return the capital of the requested country.",
    output_schema=CapitalOutput,
)
```

There is an important limitation: agent-level output schemas are intended for single-step, reply-style agents. Agents constrained by an output schema often cannot:

* invoke tools,
* perform retrieval-augmented generation (RAG),
* or hand off to other agents.

That makes agent-level schemas great for pure lookups or deterministic functions, but unsuitable for workflows needing tool calls or orchestration.

<Frame>
  <img alt="A slide titled &#x22;Important Caveat&#x22; showing a two-column table with a green check for &#x22;Only reply&#x22; and a red X listing &#x22;No functional tools, No RAG, No agent transfer.&#x22; A footer notes this is fine for pure-function agents but not suitable for a tool-driven helpdesk." />
</Frame>

<Callout icon="lightbulb">
  Agent-level output schemas are excellent when your agent should behave like a deterministic function and return a fixed schema. If your workflow requires calling tools or RAG, prefer structured tool outputs instead.
</Callout>

## Tool-level structured outputs (recommended for help desk)

The second approach is to make each tool return a strictly structured object (dict or Pydantic model). ADK can generate schemas from type hints and docstrings so the LLM sees tools as reliable, JSON-shaped building blocks. This is the pattern we’ll use for ticket creation.

Benefits:

* Tools guarantee the return shape (e.g., ticket fields), making downstream integration deterministic.
* Agents remain free to orchestrate multiple tools, call external services, and perform RAG.
* Easier to log, persist, and analyze outputs because the shape is standardized.

For a help desk, the create\_ticket tool should return a ticket object with fields like `ticket_id`, `summary`, `severity`, `service`, `user_email`, and `status`. Once that contract is enforced, other systems (databases, dashboards, external platforms) can consume tickets without extra parsing.

<Frame>
  <img alt="A slide titled &#x22;Ticket Object Structure&#x22; showing fields for a create_ticket tool, with labeled boxes for ticket_id, summary, severity, service, user_email, and status." />
</Frame>

Because the ticket is a well-defined object, integration is straightforward: log it, write it to the DB, push it to an external helpdesk, or feed it to analytics and dashboards.

We want a smart IT help desk assistant that:

* decides whether a ticket is needed,
* calls the `create_ticket` tool when appropriate,
* receives a structured ticket object back, and
* responds to the user with a clear confirmation such as: "I've created ticket IT-1234 with severity high for the VPN outage."

That structured ticket is the bridge between conversation and operations.

<Frame>
  <img alt="A presentation slide titled &#x22;Why This Matters&#x22; that outlines a four-step helpdesk assistant + tickets workflow: Decide, Call Tool, Get Structure, Respond. Each step is shown as a colored stacked block with a brief action description (e.g., call create_ticket and tell the user &#x22;I've created ticket IT-1234...&#x22;)." />
</Frame>

## Implementation plan — concrete next steps

To move from concept to working ADK code, we’ll:

* define the ticket Pydantic schema,
* implement the `create_ticket` function tool that returns a typed ticket object,
* register and wire that tool into the help desk agent flow so the agent can open tickets when needed,
* log and persist tickets (DB / external API / analytics).

This refactor makes our assistant both intelligent and reliably integrated.

<Frame>
  <img alt="A presentation slide titled &#x22;Next Steps&#x22; showing four numbered items: refactor the project, define a ticket schema, implement a create_ticket function tool, and wire it into the helpdesk flow. The design uses teal circular number icons and thin horizontal lines on a dark background." />
</Frame>

## References and further reading

* [Large language model — Wikipedia](https://en.wikipedia.org/wiki/Large_language_model)
* [Pydantic documentation](https://docs.pydantic.dev/latest/)
* [Retrieval-augmented generation (RAG) — Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
* [Kubernetes Documentation (for related orchestration patterns)](https://kubernetes.io/docs/)

<Callout icon="warning">
  When you choose agent-level schemas, remember you trade off orchestration and tool calls. For help desk workflows that must interact with services or perform multi-step logic, use tool-level structured outputs.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/google-adk/module/672589ad-758d-4e70-8408-bd4bd4409388/lesson/fed1683d-d6f3-43d9-bb54-237ecbc8a9c3" />
</CardGroup>
