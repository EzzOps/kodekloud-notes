# Example tool imports (implementations below)
from tools.helpdesk_tools import (
    lookup_user_impl,
    check_service_status_impl,
    create_ticket_impl,
)

# Register function tools
lookup_user_tool = FunctionTool(func=lookup_user_impl)
check_service_status_tool = FunctionTool(func=check_service_status_impl)
create_ticket_tool = FunctionTool(func=create_ticket_impl)
```

Tool examples and expected structured outputs

| Tool name                    | Success payload (typical)                                        | Error payload (typical)                                                       |
| ---------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| create\_ticket\_impl         | status: "success", ticket:                                       | status: "error", error\_message: "..."                                        |
| check\_service\_status\_impl | status: "success", service: "email", status\_text: "operational" | status: "error", error\_message: "Unknown service '...'. Known services: ..." |
| lookup\_user\_impl           | status: "success", user:                                         | status: "error", error\_message: "No user found for email '...'."             |

Example: create\_ticket\_impl (structured success return)

```python theme={null}
from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel

class CreateTicketArgs(BaseModel):
    summary: str
    service: str
    user_email: str
    severity: str
    department: str

class Ticket(BaseModel):
    summary: str
    service: str
    user_email: str
    severity: str
    status: str
    department: str
    created_at: datetime

def create_ticket_impl(args: CreateTicketArgs) -> Dict[str, Any]:
    ticket = Ticket(
        summary=args.summary,
        service=args.service.lower(),
        user_email=args.user_email.lower(),
        severity=args.severity,
        status="open",
        department=args.department,
        created_at=datetime.utcnow(),
    )

    return {
        "status": "success",
        "ticket": ticket.model_dump(),  # pydantic v2 model_dump()
    }
```

Example: check\_service\_status\_impl with defensive handling

* Normalize the input, check a status store, and on unexpected errors return a structured error with a friendly message and a concise technical hint.

```python theme={null}
from typing import Dict, Any

_FAKE_SERVICE_STATUS: Dict[str, str] = {
    "email": "operational",
    "gitlab": "degraded",
    "vpn": "operational",
    "wifi": "down",
}

def check_service_status_impl(service_name: str) -> Dict[str, Any]:
    try:
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
    except Exception as exc:
        # User-facing message with a short technical hint (exception type)
        return {
            "status": "error",
            "error_message": (
                "Internal error while checking service status: "
                "Please try again later or contact IT. "
                f"(Technical details: {type(exc).__name__})"
            ),
        }
```

Example: lookup\_user\_impl returning structured error/success

```python theme={null}
from typing import Dict, Any

_FAKE_USER_DIRECTORY: Dict[str, Dict[str, Any]] = {
    "alice@example.com": {"name": "Alice", "department": "IT", "status": "active"},
    "bob@example.com": {"name": "Bob", "department": "HR", "status": "active"},
}

def lookup_user_impl(email: str) -> Dict[str, Any]:
    user = _FAKE_USER_DIRECTORY.get(email.lower())
    if not user:
        return {
            "status": "error",
            "error_message": f"No user found for email '{email}'.",
        }

    return {
        "status": "success",
        "user": {
            "email": email.lower(),
            "name": user["name"],
            "department": user["department"],
            "status": user["status"],
        },
    }
```

Important: do not expose full stack traces to end users

> **warning** Avoid returning raw stack traces or long technical dumps to users. Return a short user-facing error\_message and, if needed, a brief technical hint (exception type). Store full traces in logs/tracing for debugging.

How the LLM handles structured failures

* Tools return a structured "status": "error" and a clear "error\_message" so the LLM can:
  * Produce a concise natural-language explanation (user-facing).
  * Offer an actionable next step (suggest valid service names, propose opening a ticket, etc.).
* The agent session stays active; the LLM translates structured errors into helpful suggestions rather than crashing or exposing raw exceptions.

Example console run (trimmed and corrected)

```bash theme={null}
(.venv) jeremy@MACSTUDIO ticketpro % adk run helpdesk_agent
Log setup complete: /tmp/agents_log/agent.latest.log
Running agent helpdesk_root_agent, type exit to exit.
[user]: is the 'cause_internal_error' service having issues?
[helpdesk_root_agent]: I can't find a service called 'cause_internal_error'. I can check the status of 'email', 'gitlab', 'vpn', and 'wifi'.
[user]:
```

* In this example the tool returned an error indicating an unknown service 'cause\_internal\_error'. The LLM examined that structured response and produced a helpful message listing available services and suggesting the user check for typos or try one of the known services.

Inspecting traces in the ADK web UI

* The ADK web UI traces each function invocation and its structured response. Use the trace tab to inspect the functionResponse and see the exact status and error\_message returned by the tool.

Example trace snippet (YAML-like representation from the trace tab)

```yaml theme={null}
content:
  parts:
    0:
      functionResponse:
        id: "adk-52a2bfc0-d054-48b5-a206-d695933905ca"
        name: "check_service_status_impl"
        response:
          status: "error"
          error_message: "Unknown service 'cause_internal_error'. Known services: email, gitlab, vpn, wifi."
        role: "user"
        invocationId: "e-29b4c468-60e7-4389-9981-405bff665ccc"
        author: "helpdesk_root_agent"
        id: "88f15d67-ee05-4666-855c-d231bba9269d"
        timestamp: 1765835965.212065
        title: "functionResponse:check_service_status_impl"
```

Summary — best practices

* Convert unexpected exceptions into structured error responses (status + payload or error\_message).
* Provide a short user-facing message and an optional brief technical hint (exception type).
* Keep tool responses consistent across your toolset so the LLM always has predictable signals.
* Log full traces and technical details to your tracing/log system (e.g., ADK traces) rather than returning them to the user.

Next steps

* Add a lightweight evaluation loop to verify critical flows automatically (for example: tool returns for common inputs and handling for intentionally injected failures).
* Apply the same defensive pattern to all function tools so the agent always receives predictable, structured signals about success and failure.

References

* ADK traces and tooling in the ADK web UI.
* pydantic documentation: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
* Follow structured error patterns to improve LLM-agent resiliency and user experience.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/672589ad-758d-4e70-8408-bd4bd4409388/lesson/0ac61c4a-988d-4d4e-ae5a-e66272191e60)


# Evaluations

Source: https://notes.kodekloud.com/docs/Google-ADK/Deploying-and-Operating-ADK-Agents/Evaluations/page

Describes a lightweight, event-driven evaluation workflow for ADK agents measuring tool trajectory and response similarity using captured golden sessions via UI or CLI

<Frame>
  <img alt="A presentation slide showing the word &#x22;Evaluations&#x22; on the left and a large dark curved shape on the right with the word &#x22;Demo&#x22; in blue. Small &#x22;© Copyright KodeKloud&#x22; text appears in the bottom-left corner." />
</Frame>

This lesson demonstrates a lightweight, event-driven evaluation loop for ADK agents. The goal is a minimum viable evaluation setup that lets you:

* Capture golden-path sessions in the web UI,
* Configure simple metrics (tool trajectory vs. response similarity),
* Run evaluations from the UI and CLI,
* Iterate on prompts and tools to improve scores.

Two core signals ADK encourages you to measure:

1. Tool trajectory (tool usage and order): Did the agent call the right tools in the right order?
2. Final response similarity: Is the final agent message close to the reference/expected response?

Both signals are important: correct tool usage AND a correct final message.

Quick links

* [Python Basics](https://learn.kodekloud.com/user/courses/python-basics) — minimal imports and local test data referenced below.

Overview of the evaluation flow

1. Record golden-path sessions in the ADK web UI.
2. Group sessions into an eval set (e.g., `helpdesk_core_flows`).
3. Configure threshold criteria (JSON file).
4. Run the evaluation (UI or `adk eval`).
5. Review per-case metrics and iterate on prompts, tool definitions, or expected responses.

Local test data and minimal imports

```python theme={null}
from typing import Dict, Any
from datetime import datetime
import uuid

from google.adk.tools import FunctionTool
from pydantic import BaseModel, Field

from schemas.ticket import Ticket
