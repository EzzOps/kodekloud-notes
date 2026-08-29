# Demo Create AI Agents using AWS MCP Servers In action

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/Creating-AI-Agents-Bring-It-all-together/Demo-Create-AI-Agents-using-AWS-MCP-Servers-In-action/page

Guide demonstrating two-way Slack and KAgent integration using A2A and Slack MCP servers, showing local Slack bot setup, agent deployment, tool configuration, and example workflows

This lesson demonstrates a two-way integration between Slack and KAgent:

* Slack -> KAgent: a user invokes a Slack slash command; the Slack bot forwards the query to a KAgent via the A2A protocol; the agent runs tools and returns results to Slack.
* KAgent -> Slack: the agent proactively posts notifications to a Slack channel using a Slack MCP server.

Below are the key components for this integration.

<Frame>
  <img alt="A screenshot of a code editor (likely VS Code) with a project sidebar on the left and an open text file on the right. The document shows an ASCII-style &#x22;KEY COMPONENTS&#x22; section describing a Slack app, a Python Slack bot, and a kagent agent." />
</Frame>

<Callout icon="lightbulb">
  This article does not cover Slack app creation specifics because that depends on your organization's Slack configuration. At a minimum you will need a bot token and an app token with appropriate scopes (`chat:write` and `commands`) and [Socket Mode](https://api.slack.com/apis/connections/socket-mode) enabled for local development.
</Callout>

## Key components (overview)

| Component               |                                                              Purpose | Example / Notes                                                                                                                                                         |
| ----------------------- | -------------------------------------------------------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Slack App               |            Provides tokens and scopes to interact with the workspace | Create at [api.slack.com/apps](https://api.slack.com/apps) — requires `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `chat:write`, `commands`, Socket Mode for local development |
| Slack Bot (Python Bolt) |         Receives Slack events and forwards queries to KAgent via A2A | Runs locally with `uvicorn main:app --reload`. Listens for `/mykagent` slash command and formats responses as Slack Block Kit                                           |
| KAgent Agent            |                               Executes LLM + tools inside Kubernetes | Deployed in the `kagent` namespace and exposed via A2A                                                                                                                  |
| A2A Protocol            |                       REST API for external systems to invoke agents | Endpoint pattern: `/api/a2a/{namespace}/{agent-name}/` — use backticks when documenting (e.g., `/api/a2a/{namespace}/{agent-name}/`)                                    |
| MCP Servers             | Provide tool integrations to agents (Slack, GitHub, PagerDuty, etc.) | Slack MCP server exposes tools like `slack_post_message`, `slack_get_channel_history`, etc.                                                                             |

Notes:

* Use backticks for endpoints that contain braces (e.g., `/api/a2a/{namespace}/{agent-name}/`).
* This example uses Socket Mode for the local Slack bot with Python Bolt.

## Local connection and setup (development flow)

A typical local development flow:

1. Port-forward the KAgent controller so your local machine can reach the A2A endpoint:

```bash theme={null}
kubectl port-forward -n kagent svc/kagent-controller 8083:8083
```

2. Set the A2A URL environment variable (pointing to the agent you will deploy). Use backticks when copying the path:

```bash theme={null}
export KAGENT_A2A_URL="http://127.0.0.1:8083/api/a2a/kagent/my-k8s-agent/"
```

3. Start the Slack bot locally (example for a uvicorn-based app):

```bash theme={null}
uvicorn main:app --reload
```

4. Test from Slack using the configured slash command, e.g.:

```bash theme={null}
/mykagent show me the pods in the cluster
```

## Environment variables (.env example)

Store Slack tokens and the A2A URL in a `.env` file or secret manager:

```bash theme={null}
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-1-...
KAGENT_A2A_URL=http://127.0.0.1:8083/api/a2a/kagent/my-k8s-agent/
```

<Callout icon="warning">
  Do not commit tokens or secrets to source control. Use Kubernetes Secrets or a secret manager for production credentials. Rotate tokens if they are accidentally exposed.
</Callout>

## Slack -> KAgent request flow (high-level)

1. USER (Slack) types a slash command (e.g., `/mykagent "show me pods"`).
2. Slack delivers the command event (via Socket Mode) to the local Slack bot.
3. SLACK BOT (Python Bolt) extracts the query and performs an HTTP POST to the A2A endpoint configured in `KAGENT_A2A_URL`.
4. The A2A request hits the KAgent controller (port-forwarded to localhost).
5. The controller routes the request to the appropriate agent pod.
6. The agent processes the query using its LLM, chooses and executes tools (e.g., Kubernetes resource tools), and crafts a response.
7. The agent returns the response via A2A; the Slack bot posts formatted output back to the Slack channel.

Example HTTP request to A2A (local dev):

```text theme={null}
POST http://127.0.0.1:8083/api/a2a/kagent/my-k8s-agent/
Payload: { "input": "show me pods", ... }
```

## Running the bot and deploying the agent

Start the Slack bot locally:

```bash theme={null}
uvicorn main:app --reload
