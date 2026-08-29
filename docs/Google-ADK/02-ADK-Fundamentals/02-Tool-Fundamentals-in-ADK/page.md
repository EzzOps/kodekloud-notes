# Tool Fundamentals in ADK

Source: https://notes.kodekloud.com/docs/Google-ADK/ADK-Fundamentals/Tool-Fundamentals-in-ADK/page

Explains registering typed tools in ADK so LLM agents can call Python functions, return structured outputs, and integrate utilities for actionable helpdesk tasks and production best practices.

Okay — our help desk agent can talk, but it can't do anything yet. In this lesson we'll turn that conversational assistant into an actionable agent by registering tools the model can call.

<Frame>
  <img alt="A presentation slide titled &#x22;Tool Fundamentals in ADK&#x22; with the word &#x22;Demo&#x22; in large cyan text on a dark curved shape at the right. A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left." />
</Frame>

What is a tool?

* Conceptually, a tool is a function or method: it accepts structured inputs, performs an operation, and returns structured outputs.
* ADK exposes tool signatures to the LLM so the model can decide whether to call them. This is similar to LLM function-calling, but ADK adds richer typing and integration with your Python runtime.

Core idea in brief

* Tools use typed/structured inputs and return structured outputs (commonly small JSON-like dicts).
* ADK registers tool definitions and exposes them to the model; the LLM inspects signatures and decides whether to call a tool.
* When a tool is invoked, ADK runs the Python function and passes the structured result back to the model; the model formats a human-friendly response for the user.

Types of tools

| Resource type         | When to use it                                                         | Notes / examples                                                                                                                             |
| --------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Built-in tools        | Common utilities and managed integrations provided by ADK/GCP          | Examples: Google Search, code execution, BigQuery, Vertex AI RAG. These appear in IDE auto-complete and are available out of the box.        |
| Custom function tools | Business logic, internal APIs, or system calls you implement in Python | Wrap directory lookups, ticket systems, service checks, or password reset flows. ADK can auto-wrap simple functions to expose them as tools. |
| Third-party tools     | External services with OpenAPI or other standardized descriptors       | Connectors for SaaS, monitoring systems, or vendor APIs using OpenAPI/MCP descriptions.                                                      |

> **lightbulb** ADK can auto-wrap simple Python functions and register them as tools when included in an agent's tools list. The LLM will see the function signature and may call it when relevant.

Example — build a simple helpdesk agent with a custom lookup tool

* Goal: create an agent that can check whether a user exists in a directory. The custom function returns a small, typed dictionary the model can consume and present to the user.
* In production, replace the fake directory with your organization’s user directory, handle authentication, and return well-typed responses.

```python theme={null}
from google.adk.agents import Agent
from typing import Dict

def lookup_user(email: str) -> Dict:
    """Look up a user in the fake directory.

    Returns a JSON-like dict with a `status` and either `user` (on success) or `error`.
    """
    # Example implementation (replace with a real directory lookup)
    fake_db = {
        "alice@example.com": {"name": "Alice Smith", "department": "Engineering", "status": "active"},
        "bob@example.com": {"name": "Bob Jones", "department": "Support", "status": "active"},
    }
    user = fake_db.get(email.lower())
    if user:
        return {"status": "success", "user": user}
    else:
        return {"status": "not_found", "error": f"No user found for {email}"}

root_agent = Agent(
    model="gemini-2.5-flash",
    name="helpdesk_root_agent",
    description="Smart IT Helpdesk assistant that helps troubleshoot basic IT issues.",
    instruction=(
        "You are a friendly but efficient IT helpdesk assistant for an internal company.\n\n"
        "Goals:\n"
        "1. Quickly understand the user's problem.\n"
        "2. Ask one or two clarifying questions if needed.\n"
        "3. Give clear, step-by-step instructions they can follow.\n"
        "4. Keep answers concise and practical.\n\n"
        "Constraints for now:\n"
        "- You have access only to tools explicitly registered with the agent (e.g., lookup_user).\n"
        "- Don't claim to check real systems unless a tool's output confirms doing so.\n"
    ),
    tools=[lookup_user],  # Register the custom function tool with the agent
)
```

How the LLM + ADK tool workflow works (step-by-step)

1. User: "My email is broken; can you check my account? My address is [alice@example.com](mailto:alice@example.com)."
2. The LLM reads the agent instruction and inspects available tool signatures.
3. If useful, the model decides to call a tool (e.g., `lookup_user`).
4. ADK executes the Python function: `lookup_user("alice@example.com")`.
5. ADK returns the structured result to the LLM.
6. The LLM uses the tool output to generate a concise, human-facing reply.

Example (simulated) logging for a model call

```text theme={null}
2025-12-03 22:22:08,070 - INFO - _client.py:1740 - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent
2025-12-03 22:22:08,073 - INFO - google_llm.py:216 - Response received from the model.
INFO:      127.0.0.1:62905 - "GET /debug/trace/session/bd8f57aa-5ded-4bd1-b682-b3186756ebb9 HTTP/1.1" 200 OK
```

Best practices for tool design and production readiness

* Type and validate outputs: return small, well-structured dicts (status codes, named fields) so the model can unambiguously interpret results.
* Handle errors explicitly: include clear `status` or `error` fields instead of free-form text.
* Implement authentication and access control for tools that touch sensitive systems.
* Add rate limiting and retry policies where appropriate.
* Log tool calls and model decisions for auditing and debugging.
* In development, use IDE auto-complete to discover built-in ADK tools — but treat IDE hints as convenience, not authoritative runtime state.

Common troubleshooting tips

* If the model seems unaware of a tool, confirm the function was registered in the agent's tools list and that ADK had access to the function at agent creation time.
* Inspect structured tool outputs in logs to confirm the function returned the expected schema.
* Use concise, deterministic tool outputs to reduce hallucination risk (the model is less likely to invent results when the tool provides explicit status fields).

Links and references

* [Vertex AI documentation (Generative AI & RAG)](https://cloud.google.com/vertex-ai/docs/generative-ai/overview)
* [BigQuery documentation](https://cloud.google.com/bigquery)
* [Google Cloud documentation](https://cloud.google.com/docs)

Next steps

* Open agent.py and implement a real `lookup_user` that calls your directory service or database.
* Add additional tools (service checks, ticket lookups, password reset helpers) and iteratively test how the agent chooses and composes tool calls end-to-end.

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/ee2729d1-2b89-4a41-b21d-f245c7372cc9/lesson/67d46a34-ca95-46a7-9fff-8b2795b282a0)
