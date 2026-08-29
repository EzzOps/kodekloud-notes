# Adding State to the IT Helpdesk Assistant

Source: https://notes.kodekloud.com/docs/Google-ADK/ADK-Fundamentals/Adding-State-to-the-IT-Helpdesk-Assistant/page

Explains building a stateful IT helpdesk assistant that uses session history and targeted tools to clarify issues, check service and account status, and provide concise troubleshooting steps.

In this lesson we evolve the helpdesk agent to behave like a real IT workflow: it clarifies the issue, requests the right details, calls targeted tools, and converts results into concise, actionable next steps. We accomplish this by tightening the agent instructions and relying on ADK's multi-turn session handling so the agent remembers prior turns and avoids repeating already-answered questions.

> **lightbulb** ADK supplies the full conversation history on each turn. Use that to avoid repeating questions already answered earlier in the session.

## Summary of changes

* The original root agent was replaced with a workflow-aware version that:
  * Runs inside a multi-turn session and receives full conversation history each turn.
  * Follows a repeatable troubleshooting flow for every new issue.
  * Calls tools only when they add value (improves determinism).
  * Returns concise numbered or bulleted next steps based on tool results.
  * Enforces style and safety constraints (calm, practical, and honest).

These updates reduce guesswork about tool usage and make the agent's behavior more predictable and useful.

## At-a-glance: Troubleshooting flow

| Step                   | When to use it                                                           | What to do                                                                                               |
| ---------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| 1. Clarify the problem | If the user is vague or the service is unclear                           | Ask 1–2 short clarifying questions (service, observed behavior). Don’t repeat if already asked.          |
| 2. Gather key details  | When the issue involves an account or a backend service                  | Ask for work email when appropriate; consider calling lookup\_user if an account lookup would help.      |
| 3. Check service state | When the problem relates to an infrastructure service (VPN, email, etc.) | Call check\_service\_status to determine service health before troubleshooting local causes.             |
| 4. Provide next steps  | After collecting data and tool results                                   | Give short numbered steps (reconnect, restart, wait for service restoration), and surface uncertainties. |

## Tools (provided to this agent)

| Tool                   | Use case                                                                     | Example                                    |
| ---------------------- | ---------------------------------------------------------------------------- | ------------------------------------------ |
| lookup\_user           | Verify account status when the user provides an email address                | `lookup_user(email="carol@example.com")`   |
| check\_service\_status | Check whether a named service (VPN, email, Wi‑Fi) is degraded or unavailable | `check_service_status(service_name="vpn")` |

## Root agent: structured prompt and tooling

Below is a consolidated example of the root agent definition and its instruction string. The two tools available to this agent are lookup\_user and check\_service\_status.

```python theme={null}
root_agent = Agent(
    model="gpt-4o-mini-2.7-trash",
    name="helpdesk_root_agent",
    description="Smart IT Helpdesk assistant that troubleshoots common IT issues using clarifying questions and internal tools.",
    instruction=(
        "You are a friendly but efficient IT helpdesk assistant for an internal company.\n\n"
        "You are running inside a multi-turn session. ADK will give you the full conversation history each time, so you should remember what has already been asked and answered.\n\n"
        "=== OVERALL GOAL ===\n"
        "- Help the user troubleshoot issues with email, VPN, GitLab, Wi-Fi and similar services.\n"
        "- When appropriate, look up their account and check the status of backend services.\n"
        "- Explain what you are doing in plain language.\n\n"
        "=== TROUBLESHOOTING FLOW ===\n"
        "Follow this high-level process for each new issue:\n\n"
        "1) Clarify the problem\n"
        " - If the user is vague (e.g., 'something is broken'), ask 1-2 short questions:\n"
        "   * Which service is affected? (email, VPN, GitLab, Wi-Fi, etc.)\n"
        "   * What exactly happens? (errors, disconnects, password rejected, etc.)\n"
        " - If they already provided this earlier in the conversation, do NOT repeat the question.\n\n"
        "2) Gather key details\n"
        " - If the problem clearly involves an account, politely ask for their work email address.\n"
        " - When it adds value, call the lookup_user tool (when you have an email and it would help to know account status).\n"
        " - Call check_service_status when the issue clearly involves a service (e.g., VPN, email).\n\n"
        "3) Use tools sparingly\n"
        " - Only call a tool if it will add value for the current troubleshooting step.\n\n"
        "4) Provide next steps\n"
        " - Give short numbered next steps based on tool results (e.g., reconnect VPN, restart client, try a different network).\n\n"
        "=== STYLE ===\n"
        "- Be calm, practical, and reassuring.\n"
        "- Prefer bullet points or numbered steps when giving instructions.\n"
        "- Keep answers concise but not cryptic.\n"
        "- Never invent real company names or internal ticket IDs; speak generically.\n\n"
        "=== SAFETY & HONESTY ===\n"
        "- Do NOT claim to directly access real systems; you only see the fake tool data provided.\n"
        "- If tools return an error or you are uncertain, say so clearly and suggest talking to IT.\n"
        "- Never reveal private data beyond what the user has already provided.\n"
    ),
    tools=[lookup_user, check_service_status],
)
```

## How the flow behaves: examples

Below are two compact interaction examples illustrating how the agent uses session history and tools to be efficient and deterministic.

1. VPN service degradation example

User reports a VPN that disconnects. The agent checks service status and returns short, actionable steps.

```text theme={null}
[user]: my VPN keeps disconnecting every few minutes

[helpdesk_root_agent]: I understand your VPN keeps disconnecting every few minutes. Let me check the VPN service status for you.

[helpdesk_root_agent]: It looks like the VPN service is currently degraded. This might be causing your disconnections.

Here are a few steps you can try:
1. Reconnect: Disconnect and reconnect to the VPN.
2. Restart your computer: Sometimes a fresh start resolves transient issues.
3. Try a different network (if possible): Connect from another Wi‑Fi network or a mobile hotspot.

We are aware of the degradation and are working on it. You can try again shortly, or contact IT if the issue continues.
```

When the user reports the issue persists on a different network, the agent refers to prior messages (because it receives full session history) rather than re-asking the same questions:

```text theme={null}
[user]: my network is fine, but I am still having problems on a new network

[helpdesk_root_agent]: I understand you're still having trouble even on a different network. Since the VPN service is currently degraded, that could be the root cause.

Have you tried the steps from my previous message?
1. Disconnect and reconnect to the VPN.
2. Restart your computer.

If you've tried those and the issue persists, it's likely related to the ongoing service degradation. Please wait a short while while our team works on restoring service, or contact IT if it becomes urgent.
```

2. Locked email account example

When the user reports a locked account and supplies an email address, the agent calls lookup\_user to confirm account status before advising next steps.

```text theme={null}
[user]: My email account is locked. My email is carol@example.com

[helpdesk_root_agent]: I'm sorry to hear your email account is locked. Let me look up your account status for you.

[helpdesk_root_agent]: According to our records, the account carol@example.com is locked.

To resolve this, please contact the IT department so they can unlock your account. If you'd like, I can provide suggested wording for the IT request.
```

## Why this pattern helps

* Deterministic tool use: The prompt explicitly states when to call lookup\_user and check\_service\_status, reducing incorrect or needless tool calls.
* Session-aware interactions: ADK’s multi-turn state allows the agent to reference previous turns and avoid repeating questions.
* Repeatable flow: A concise, explicit troubleshooting flow yields clearer guidance and is easier to extend (for example, by adding a ticket creation tool and a machine-readable ticket schema).

> **warning** Do NOT claim to access real systems. Always treat tools as limited views of fake or provided data, and surface uncertainties or tool errors clearly to the user.

## Next steps

This lesson introduced a stateful, workflow-driven helpdesk agent. Upcoming lessons will add more structure (for example, a ticket schema and a create-ticket tool) so the agent can produce machine-readable outputs that other systems can consume.

Try the included lab to experiment with the troubleshooting flow and observe how session state influences the agent's questions and tool usage.

## References

* ADK multi-turn session patterns and best practices (see your internal ADK docs)
* General helpdesk and troubleshooting guidance: [https://en.wikipedia.org/wiki/Help\_desk](https://en.wikipedia.org/wiki/Help_desk)

- [Watch Video](https://learn.kodekloud.com/user/courses/google-adk/module/ee2729d1-2b89-4a41-b21d-f245c7372cc9/lesson/fb18c7ae-64de-4c2b-9312-2487b581bf7f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/google-adk/module/ee2729d1-2b89-4a41-b21d-f245c7372cc9/lesson/0950cf35-a73a-4db6-8cc9-52085b4a7cd5)
