# Example log:
# INFO:root:Starting kagent Slack bot
```

Deploy the agent manifest into the cluster:

```bash theme={null}
kubectl apply -f slack-k8s-agent.yaml
# Example output:
# agent.kagent.dev/my-k8s-agent created
```

Check agent status:

```bash theme={null}
kubectl get agent -n kagent
# NAME            TYPE          READY   ACCEPTED
# my-k8s-agent    Declarative   False   True
```

Retrieve the agent card from the A2A controller (validates the path and capabilities):

```bash theme={null}
curl http://127.0.0.1:8083/api/a2a/kagent/my-k8s-agent/.well-known/agent.json
```

Example JSON response (truncated):

```json theme={null}
{
  "name": "my_k8s_agent",
  "description": "My Kubernetes Agent",
  "url": "http://kagent-controller.kagent.svc.cluster.local:8083/api/a2a/kagent/my-k8s-agent/",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "skills": [
    {
      "id": "answer-questions-about-your-cluster",
      "name": "Answer Questions About Your Cluster",
      "description": "Answer questions about your Kubernetes cluster",
      "tags": ["kubernetes"],
      "inputModes": ["text"],
      "outputModes": ["text"]
    }
  ]
}
```

Once the agent shows READY in the KAgent UI, invoke it via Slack.

### Example Slack query -> agent response

User input:

```text theme={null}
/mykagent get the list of pods running in the cluster
```

Agent response (example formatted text):

```text theme={null}
Here are the pods running in the cluster across all namespaces:

Namespace: kagent
- kagent-controller-6f546c65bd-ckk6s
- kagent-grafana-mcp-597df4c7f4-r4fdq
- kagent-kmcp-controller-manager-86b48b656d-l8zdb
- kagent-querydoc-7dc78dc9d7-pqf92
- kagent-tools-6d6695c5-rw7rz
- kagent-ui-5757fccb58-bsbbc
- my-k8s-agent-7b98575b68-kds2f

Namespace: kube-system
- metrics-server-67c9654d97-dc7tm
- metrics-server-67c9654d97-g9crq

All pods listed are in Running status. How can I assist you further?
```

This demonstrates the full round-trip: Slack -> Slack bot -> A2A -> agent -> tools -> response -> Slack.

## KAgent -> Slack (Agent-initiated messages)

Agents can proactively post to Slack channels by calling Slack MCP tools. Typical flow:

1. Agent determines a message/alert should be posted to Slack.
2. Agent calls a Slack MCP tool such as `send_message_to_slack` or `slack_post_message`.
3. The Slack MCP server performs an HTTP POST to Slack API `chat.postMessage`.
4. The message appears in the configured Slack channel.

Schematic:

```text theme={null}
KAGENT AGENT (in Kubernetes)
  -> call send_message_to_slack
SLACK MCP SERVER (in Kubernetes)
  -> POST chat.postMessage to Slack API
SLACK WORKSPACE
  -> message appears in channel
```

## Deploying and configuring the Slack MCP server

A Slack MCP server is an `MCPServer` custom resource. A minimal manifest looks like this:

```yaml theme={null}
apiVersion: kagent.dev/v1alpha1
kind: MCPServer
metadata:
  name: slack-mcp
  namespace: kagent
spec:
  deployment:
    image: "node:latest"
    port: 3000
    cmd: ["npx"]
    args:
      - "-y"
      - "@modelcontextprotocol/server-slack"
  secretRefs:
    # secret references for Slack credentials (see your manifest)
```

Create a Kubernetes Secret containing Slack credentials (bot token, team ID, channel IDs) and apply the manifest:

```bash theme={null}
kubectl apply -f slack-mcp.yaml
kubectl get mcpserver -n kagent
# NAME        READY   AGE
# slack-mcp   True    14s
```

When the Slack MCP server is running, tools such as `slack_post_message`, `slack_get_channel_history`, and `slack_add_reaction` are available to agents. Confirm visibility in the KAgent UI.

<Frame>
  <img alt="A screenshot of a web UI for &#x22;kagent&#x22; (localhost:8080/servers) showing a list of server/integration entries. The expanded item is kagent/slack-mcp with multiple Slack actions listed (e.g., slack_add_reaction, slack_get_channel_history)." />
</Frame>

## Granting the agent Slack posting permissions

Steps to allow agents to post into Slack:

1. Create a Kubernetes Secret with Slack credentials (bot token, team ID, channel IDs).
2. Update your agent manifest to include Slack MCP tools (e.g., `slack_post_message`) in the agent's tool list.
3. Apply the updated agent manifest and wait for KAgent to reconcile. It may take a minute for new tools to become available.

Example:

```bash theme={null}
kubectl apply -f slack-k8s-agent.yaml
# agent.kagent.dev/my-k8s-agent configured
```

Example instruction you can give the agent:

```text theme={null}
Get the list of deployments on the cluster and post it to the Slack channel "cluster-info".
```

Example tools executed:

* `get_resource_information` (fetch deployments)
* `slack_post_message` (post formatted message to Slack channel)

Example channel output:

```text theme={null}
List of deployments on the cluster:

Namespace: kagent
- kagent-controller
- kagent-grafana-mcp
- kagent-kmcp-controller-manager
- kagent-querydoc
- kagent-tools
- kagent-ui
- my-k8s-agent
- slack-mcp

Namespace: kube-system
- metrics-server
```

You can deploy multiple Slack apps / MCP servers to support different teams, channels, or clusters as needed.

## Quick reference commands

| Task                           | Command                                                                         |
| ------------------------------ | ------------------------------------------------------------------------------- |
| Port-forward KAgent controller | `kubectl port-forward -n kagent svc/kagent-controller 8083:8083`                |
| Start Slack bot                | `uvicorn main:app --reload`                                                     |
| Apply agent manifest           | `kubectl apply -f slack-k8s-agent.yaml`                                         |
| Retrieve agent card            | `curl http://127.0.0.1:8083/api/a2a/kagent/my-k8s-agent/.well-known/agent.json` |

## Closing

This lesson covered a two-way integration pattern between Slack and KAgent:

* Slack -> KAgent: Slack commands are forwarded to agents via the A2A protocol; agents execute tools and return results back to Slack.
* KAgent -> Slack: Agents post messages or alerts to Slack by invoking MCP tools exposed by a Slack MCP server.

You can reuse this pattern to integrate agents with other MCP servers (GitHub, PagerDuty, etc.) to extend agent capabilities across platforms.

## Links and references

* [Slack API: chat.postMessage](https://api.slack.com/methods/chat.postMessage)
* [Socket Mode (Slack)](https://api.slack.com/apis/connections/socket-mode)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [KAgent (project docs)](https://kagent.dev/) (check your cluster's docs for KAgent-specific manifests)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/2f536b48-ed92-4812-ba03-cac21e7bc768/lesson/32df4a4a-b558-4697-b5b6-2e73deea9a5b" />
</CardGroup>


# Demo Debugging AI Agents

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/Debugging-AI-Agents/Demo-Debugging-AI-Agents/page

Guide showing how to configure Jaeger and KAgent to export OpenTelemetry traces, generate agent traffic, and inspect AI agent traces and LLM metadata in Jaeger

Welcome — in this lesson you'll learn how to add distributed tracing to AI agents running with KAgent and inspect traces in Jaeger. As agent ecosystems grow, visibility into agent actions and their LLM interactions is essential for debugging, cost analysis, and observability.

Objectives:

* Introduce Jaeger and the minimal configuration used in this lab.
* Install Jaeger (all-in-one, in-memory) and KAgent.
* Configure KAgent to export OpenTelemetry (OTEL) traces to Jaeger.
* Generate agent traffic and inspect the traces in the Jaeger UI.

This lab focuses on integrating KAgent with an OTEL backend; Jaeger is used as a simple example. KAgent supports exporting to any OTEL-compatible backend.

<Callout icon="lightbulb">
  This lesson uses Jaeger in all-in-one (development) mode with in-memory storage. Traces are transient and will be lost if the Jaeger pod restarts.
</Callout>

## 1. Jaeger configuration (all-in-one, in-memory)

The Helm values below run Jaeger in all-in-one mode with in-memory storage — suitable for development and short-lived labs. Because storage is `memory`, traces are not persisted across restarts.

```yaml theme={null}
