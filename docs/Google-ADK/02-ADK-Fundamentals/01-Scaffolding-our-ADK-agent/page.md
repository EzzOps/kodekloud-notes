# agent.py
from typing import Dict, Any
from google.adk.agents.llm_agent import Agent

# Tiny in-memory "directory" of users.
_FAKE_USER_DIRECTORY: Dict[str, Dict[str, Any]] = {
    "alice@example.com": {
        "name": "Alice Johnson",
        "department": "Engineering",
        "status": "active",
    },
    "bob@example.com": {
        "name": "Bob Smith",
        "department": "Finance",
        "status": "active",
    },
    "carol@example.com": {
        "name": "Carol Lee",
        "department": "HR",
        "status": "locked",  # Their account may be locked.
    },
}

# Tiny in-memory "service status" registry.
_FAKE_SERVICE_STATUS: Dict[str, str] = {
    "vpn": "degraded",
    "gitlab": "outage",
    "wifi": "operational",
}


def lookup_user(email: str) -> Dict[str, Any]:
    """
    Look up a user in the fake directory.

    Returns a structured dict:
      - status: "success" or "error"
      - user: { email, name, department, status }  # only on success
      - error_message: str  # only on error
    """
    if not isinstance(email, str) or not email.strip():
        return {"status": "error", "error_message": "Invalid email provided."}

    normalized = email.strip().lower()
    user = _FAKE_USER_DIRECTORY.get(normalized)
    if not user:
        return {
            "status": "error",
            "error_message": f"No user found for email '{email}'.",
        }

    return {
        "status": "success",
        "user": {
            "email": normalized,
            "name": user["name"],
            "department": user["department"],
            "status": user["status"],
        },
    }


def check_service_status(service_name: str) -> Dict[str, Any]:
    """
    Check the status of a named IT service.

    For now this just looks up a value in an in-memory dict.

    Returns a structured dict:
      - status: "success" or "error"
      - service: normalized service name (on success)
      - status_text: operational state like "operational", "degraded", or "outage" (on success)
      - error_message: str (on error)
    """
    if not isinstance(service_name, str) or not service_name.strip():
        return {"status": "error", "error_message": "Invalid service name provided."}

    normalized = service_name.strip().lower()
    status_text = _FAKE_SERVICE_STATUS.get(normalized)
    if not status_text:
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
        "status_text": status_text,
    }


# Register the agent and attach the tools.
root_agent = Agent(
    model="gemini-2.5-flash",
    name="helpdesk_root_agent",
    description="Smart IT Helpdesk assistant that helps troubleshoot basic IT issues.",
    instruction=(
        "You are a friendly but efficient IT helpdesk assistant for an internal company.\n"
        "\n"
        "Goals:\n"
        "1. Quickly understand the user's problem.\n"
        "2. Ask one or two clarifying questions if needed.\n"
        "3. Give clear, step-by-step instructions they can follow.\n"
        "4. Keep answers concise and practical.\n"
        "\n"
        "Constraints:\n"
        "- Use the available tools (lookup_user, check_service_status) when appropriate.\n"
        "- Do not claim to check real systems outside these tools.\n"
        "- When uncertain, use phrases like 'Based on common IT practice...' instead of pretending.\n"
    ),
    tools=[lookup_user, check_service_status],
)
```

Why normalize inputs

* Make lookups case-insensitive and tolerant of leading/trailing whitespace by lower-casing and stripping inputs.
* Returning a clear structure (status + payload or error\_message) prevents the LLM from guessing shapes and reduces hallucinations.

Best practice

* Explicitly list each tool in Agent.tools (e.g., tools=\[lookup\_user, check\_service\_status]) — this keeps tool availability explicit and discoverable by the agent.
* Keep docstrings short, factual, and up-to-date: the LLM relies on these to decide when and how to call a tool.

Running and testing (example terminal session)
Start your agent with the ADK CLI:

```console theme={null}
(.venv) $ adk run helpdesk_root_agent
Running agent helpdesk_root_agent, type exit to exit.
[user]: My email address is bob@example.com. But I have forgotten my name. What is it?
[helpdesk_root_agent]: Your name is Bob Smith.
[user]: My email address is jeremy@example.com, but I have forgotten my name. What is it?
[helpdesk_root_agent]: I couldn't find a user with the email address jeremy@example.com. Could you please double-check the email address for any typos?
[user]: Is there something wrong with the VPN?
[helpdesk_root_agent]: Based on common IT practice, the VPN service is currently degraded. Are you having trouble connecting to the VPN, or are you experiencing slow speeds?
```

Notes about ADK and how the LLM uses tools

* ADK can auto-wrap plain Python functions as callable tools with structured I/O.
* The agent coordinates between the LLM and your functions: the LLM decides which tool to call and prepares inputs; the function returns structured data; the LLM then translates that structured data into natural language for the user.
* Explicit, structured tool outputs help avoid hallucination and allow concrete, checkable responses.

> **warning** Common pitfalls and debugging:

  * NameError or import errors often indicate a missing import or incorrectly registered tool. Verify your imports and that you included tools in Agent.tools.
  * If the agent returns unexpected output, confirm your tool's return schema matches its docstring and the LLM's expectations.

Next steps

* Implement stateful troubleshooting flows so the agent can remember context across multiple turns.
* Add authentication and access controls when you move from fake in-memory stores to real data sources.
* Split tools into modules for larger projects and add unit tests for each tool's structured outputs.

Further reading

* ADK and agent patterns: [https://developers.google.com/ai](https://developers.google.com/ai)
* Python typing docs: [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/ee2729d1-2b89-4a41-b21d-f245c7372cc9/lesson/ac465a22-acff-4bd0-82db-75ad265c38a9)


# Scaffolding our ADK agent

Source: https://notes.kodekloud.com/docs/Google-ADK/ADK-Fundamentals/Scaffolding-our-ADK-agent/page

Guide to scaffold and run a minimal ADK helpdesk agent using Python, Google AI backend, and ADK tools including CLI and web UI

All right — let's get the project started. In this guide you'll go from zero to a running ADK agent: install required tools, scaffold a project, and wire up a simple helpdesk agent that responds in natural language.

Although this demo uses Google Cloud IDE and the Google AI backend, the ADK is model-agnostic. You can swap in other LLM backends (or run locally) later.

## What you'll build

* A minimal ADK "root agent" that runs against an LLM.
* Local development setup (Python virtual environment).
* A scaffolded project containing the agent, package init, and .env.
* A quick run using the ADK runner and the ADK web UI for inspection.

## Prerequisites

* Python 3.8 or newer
* If using the Google AI backend: a Google API key (create one in AI Studio)

Helpful links:

* AI Studio (create an API key): [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
* ADK documentation: [https://github.com/google/adk](https://github.com/google/adk) (or your internal ADK docs)

***

## 1) Create and activate a Python virtual environment

Mac / Linux:

```bash theme={null}
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell theme={null}
python3 -m venv .venv
.venv\Scripts\Activate.ps1
```

Example terminal session:

```bash theme={null}
jeremy@MACSTUDIO ticketpro % python3 -m venv .venv
jeremy@MACSTUDIO ticketpro % source .venv/bin/activate
(.venv) jeremy@MACSTUDIO ticketpro %
```

***

## 2) Install the ADK package

Install the ADK Python package with pip:

```bash theme={null}
pip install google-adk
```

You may see dependency installation output similar to:

```text theme={null}
Collecting google-adk
Installing collected packages: google-auth, protobuf, pydantic, ...
```

***

## 3) Scaffold a new ADK project

Use the ADK CLI to scaffold a new agent project:

```bash theme={null}
adk create helpdesk_agent
```

The CLI will prompt for a model and backend. For this demo choose:

* Model: gemini-2.5-flash
* Backend: Google AI (not Vertex AI)

If you do not yet have an API key, follow the CLI prompt to create one in AI Studio.

Example interactive prompts:

```text theme={null}
Choose a model for the root agent:
1. gemini-2.5-flash
2. Other models (fill later)
Choose model (1, 2): 1
1. Google AI
2. Vertex AI
Choose a backend (1, 2): 1

Don't have API Key? Create one in AI Studio: https://aistudio.google.com/apikey

Enter Google API key:
```

After completion the CLI lists the created files:

```text theme={null}
Agent created in /Users/jeremy/Repos/adkdemos/ticketpro/helpdesk_agent:
- .env
- __init__.py
- agent.py

(.venv) jeremy@MACSTUDIO ticketpro %
```

***

## 4) Inspect the scaffolded files

Here's a quick reference for the files the scaffold creates:

| File        | Purpose                                   | Notes / Example                           |
| ----------- | ----------------------------------------- | ----------------------------------------- |
| .env        | Environment flags and API key placeholder | DO NOT commit real keys to source control |
| **init**.py | Makes the directory a Python package      | Typically imports the agent module        |
| agent.py    | Root agent definition                     | Contains the Agent instance ADK will run  |

Examples and snippets below.

* **init**.py

This file makes the directory a Python package and commonly imports the agent so the ADK runtime can discover it:

```python theme={null}
from . import agent
```

* .env

The scaffold includes an .env file containing a flag for Vertex AI usage and a placeholder for your API key. Replace the placeholder with a secure secret (see callout below).

Example .env (do not commit real keys to source control):

```text theme={null}
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

> **lightbulb** Store real API keys securely — use environment variables, a secret manager, or another safe credential store. Avoid committing keys to source control.

* agent.py

The scaffolded agent is an LLM-only agent. The only required element in an ADK app is a "root agent" instance that the ADK runtime will import and run. A minimal LLM root agent looks like this:

```python theme={null}
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name="helpdesk_root_agent",
    description="Smart IT Helpdesk assistant that helps troubleshoot basic IT issues.",
    instruction=(
        "You are a friendly but efficient IT helpdesk assistant for an internal company.\n"
        "\n"
        "Goals:\n"
        "1. Quickly understand the user's problem.\n"
        "2. Ask one or two clarifying questions if needed.\n"
        "3. Give clear, step-by-step instructions they can follow.\n"
        "4. Keep answers concise and practical.\n"
        "\n"
        "Constraints for now:\n"
        "- You do NOT have access to tools yet.\n"
        "- Don't claim to check real systems.\n"
        "- Use phrases like 'Based on common IT practice...' instead of pretending.\n"
    ),
    tools=[]  # Tools will be added later
)
```

This instruction block guides the LLM's tone, goals, and constraints. We intentionally set tools=\[] for now — tools (e.g., account lookups, ticket creation, status checks) will be added in later lessons.

***

## 5) Run the agent with the ADK runner

Run the agent using the ADK runtime so it can locate and execute the root agent:

```bash theme={null}
adk run helpdesk_root_agent
```

If you omit the agent name the CLI will report a missing argument:

```text theme={null}
usage: adk run [OPTIONS] AGENT
Error: Missing required argument: AGENT
```

Example run output (trimmed):

```text theme={null}
Log setup complete: /tmp/agents_log/agent.latest.log
Running agent helpdesk_root_agent, type exit to exit.
[user]: My VPN disconnects every 5 minutes
[helpdesk_root_agent]: That sounds frustrating! A frequent VPN disconnect can be caused by several issues.

To help narrow it down, could you tell me:
1. Which VPN software are you using (e.g., Cisco AnyConnect, FortiClient, OpenVPN)?
2. Are you connected via Wi-Fi or wired (Ethernet)?
[user]:
```

This is a plain LLM interaction — the same behavior you'd get from sending the same prompt to Gemini directly. The ADK advantage is the structured agent scaffold that’s ready to be extended with tools, traces, sessions, and a web UI.

***

## 6) Web UI

ADK includes a web interface (adk web) to interact with your agent in a browser. Use it to inspect traces, events, state, artifacts, sessions, and evals — very helpful for debugging and iterating quickly.

You can use both the CLI and the web UI concurrently during development.

<Frame>
  <img alt="A dark-themed desktop screenshot of an &#x22;Agent Development Kit&#x22; web app showing a chat/helpdesk interface. The chat pane contains a user message &#x22;My monitor is blank&#x22; and an automated response asking troubleshooting questions." />
</Frame>

***

## Summary checklist

* Created and activated a Python virtual environment.
* Installed the google-adk package.
* Scaffolded a helpdesk ADK project and inspected its files (.env, **init**.py, agent.py).
* Configured the root\_agent with goals, constraints, and a friendly instruction set.
* Ran the agent via `adk run` to interact with the LLM.
* Verified the web UI is available for interactive debugging and traces.

Next steps: add tools to give this agent real "powers" — for example, user account lookups, ticket creation, and system status queries. These will let the agent perform actions instead of only replying with general advice.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/ee2729d1-2b89-4a41-b21d-f245c7372cc9/lesson/f59b071d-1354-4b7b-8cb4-32402671505f)
