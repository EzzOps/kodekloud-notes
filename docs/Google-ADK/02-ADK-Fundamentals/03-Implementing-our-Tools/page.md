# Implementing our Tools

Source: https://notes.kodekloud.com/docs/Google-ADK/ADK-Fundamentals/Implementing-our-Tools/page

Guide to implementing and registering two typed helpdesk tools that lookup users and check service status for an ADK LLM agent.

All right — now that we understand how tools work and how to create them, let's implement two practical tools for our helpdesk agent: user lookups and checking service status. For clarity and to make the example easy to run, we keep everything in a single file (agent.py). Later, you can break tools into separate modules if you prefer.

<Frame>
  <img alt="A presentation slide with the title &#x22;Implementing our Tools&#x22; and a dark teal curved panel on the right containing the word &#x22;Demo&#x22; in bright blue. A small &#x22;© Copyright KodeKloud&#x22; note appears in the bottom-left." />
</Frame>

Overview

* Build two tiny in-memory services:
  * a fake user directory
  * a fake service-status registry
* Implement two strongly-typed tools that return structured dictionaries so the LLM knows what to expect:
  * lookup\_user(email: str) -> Dict\[str, Any]
  * check\_service\_status(service\_name: str) -> Dict\[str, Any]
* Register these functions with an ADK Agent so the LLM can call them.

> **lightbulb** Comments and docstrings are visible to the LLM and can affect tool usage. Keep them accurate, concise, and machine-friendly.

Tool return schemas
Use clear, predictable return shapes so the agent can consume results without guessing. The table below summarizes the two tools and their expected structured outputs.

| Tool                   | Signature                                                   | Success fields                           | Error fields                    |
| ---------------------- | ----------------------------------------------------------- | ---------------------------------------- | ------------------------------- |
| lookup\_user           | `lookup_user(email: str) -> Dict[str, Any]`                 | status: "success", user:                 | status: "error", error\_message |
| check\_service\_status | `check_service_status(service_name: str) -> Dict[str, Any]` | status: "success", service, status\_text | status: "error", error\_message |

Concise example: agent.py
Below is a corrected, concise implementation that demonstrates typed imports, small in-memory stores, the two tool functions, and the Agent registration exposing the tools to the LLM. Keep this code in a single file for now to simplify running and testing.

```python theme={null}
