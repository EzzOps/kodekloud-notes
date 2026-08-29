# python
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AgentMessage(BaseModel):
    sender: str
    recipient: str
    kind: str
    payload: dict

# Example per-agent API keys
API_KEYS = {"agent-a": "secret-token-a", "agent-b": "secret-token-b"}

def verify_api_key(x_api_key: str):
    # Validate that the provided API key matches a known agent key
    if x_api_key not in API_KEYS.values():
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.post("/message")
def receive_message(msg: AgentMessage, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    # Additional authorization checks here (see authorize() below)
    return {"status": "accepted", "sender": msg.sender, "recipient": msg.recipient}
```

Role-based authorization example

```python theme={null}
# python
def authorize(agent_id: str, action: str) -> bool:
    role_permissions = {
        "writer": {"write_document", "read_context"},
        "planner": {"create_plan", "read_context"},
    }
    role = get_role_for_agent(agent_id)  # implement your lookup
    return action in role_permissions.get(role, set())
```

Operational checklist for secure, ethical MAS

Use this operational checklist as a starting point and tailor it to your domain and compliance requirements.

| Area              | Minimum controls                                                   |
| ----------------- | ------------------------------------------------------------------ |
| Identity & auth   | Per-agent identity, API keys or certs, mutual TLS, signed tokens   |
| Authorization     | RBAC, least privilege, scoped tool access                          |
| Communication     | Encrypted channels, signed messages, schema validation             |
| Memory & data     | Scoped memory, redaction, TTL, session isolation                   |
| Execution         | Sandboxed runtimes, resource limits, tool invocation controls      |
| Monitoring        | Structured logs, alerts, audit trails, behavioral analytics        |
| Ethics & fairness | System-level constraints, bias audits, provenance tracking         |
| Human oversight   | Human-in-the-loop gates, escalation procedures, incident playbooks |

> **lightbulb** This checklist is an operational guide — adapt it to your domain and regulatory needs. For high-impact systems, prioritize human-in-the-loop gates, stronger isolation, and frequent security reviews.

Closing summary

Multi-agent systems deliver powerful distributed intelligence, but they introduce new security and ethical challenges. Map your threat surfaces (communication, shared memory, tool access), enforce agent identity and least privilege, validate and sandbox interactions, and implement system-level ethical constraints. Combine automated defenses with human oversight, monitoring, and structured logs to deploy MAS responsibly and at scale.

<Frame>
  <img alt="The image outlines strategies for securing communication between agents, including using encrypted channels, validating inputs/outputs, preventing injection attacks, and preferring structured data formats." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/2e110716-1967-4e6f-a995-9138c54fb38c/lesson/a1263165-d17d-4000-abc2-a6624ea60216)


# Demo Building a Simple Chatbot

Source: https://notes.kodekloud.com/docs/AI-Agents/Building-AI-Agents/Demo-Building-a-Simple-Chatbot/page

Guide to building a simple interactive chatbot with the OpenAI Agents SDK, covering agent configuration, typed outputs, async Runner usage, environment variables, and a police sketch artist example.

Welcome back! In this lesson we’ll build a simple interactive chatbot using OpenAI’s Agents model. Before diving into code, take a few minutes to explore the OpenAI Agents SDK repository and docs — understanding where examples and patterns live will speed up development.

<Frame>
  <img alt="The image shows a webpage titled &#x22;OpenAI Agents SDK&#x22;, detailing the features and usage of the SDK, with navigation options on the left and additional content on the right." />
</Frame>

Start with the Quickstart and the Examples folder in the Agents SDK to see common integrations and agent patterns you can reuse. These resources demonstrate how tools, outputs, and agent behaviors are wired together.

<Frame>
  <img alt="The image shows a webpage from the OpenAI Agents SDK documentation, highlighting example implementations and categories such as agent patterns and basic capabilities." />
</Frame>

Use the documentation as your reference for configuring agents, registering tools, and customizing outputs.

Example: typed outputs with Pydantic
Here’s a concise example showing how to define a typed output using Pydantic and create an Agent. Typed outputs make it easier to validate and consume structured results from your agent.

```python theme={null}
from pydantic import BaseModel
from agents import Agent

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent,
)
```

Building the chatbot
Below we’ll create a simple interactive chatbot that:

* Loads environment variables securely (do not hard-code API keys).
* Defines an Agent with clear role-based instructions.
* Uses an asynchronous main loop to run the agent via `Runner.run`.
* Stores and displays a simple chat history.
* Supports the `history`, `exit`, and `quit` commands.

> **lightbulb** Make sure you have a `.env` file with `OPENAI_API_KEY` set, or set the environment variable in another secure way. Do not hard-code API keys in your script.

Complete chatbot script
This consolidated script demonstrates the full flow. It uses `python-dotenv` to load the API key, defines an Agent with instructions, awaits `Runner.run`, and manages conversation memory.

```python theme={null}
