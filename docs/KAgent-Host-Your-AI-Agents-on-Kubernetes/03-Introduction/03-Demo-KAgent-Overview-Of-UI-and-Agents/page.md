# kubectl get pods -n kagent
NAME                                                         READY   STATUS    RESTARTS   AGE
argo-rollouts-conversion-agent-6b75f48f84-skzsc               1/1     Running   0          40s
cilium-debug-agent-5c7798b559-9bbzh                           1/1     Running   0          40s
cilium-manager-agent-5dc4964899-2vkn4                         1/1     Running   0          40s
cilium-policy-agent-595f585896-hsmqb                          1/1     Running   0          39s
helm-agent-66d7fd5fb8-dvbr6                                   1/1     Running   0          40s
istio-agent-557f7c74d9-tcspp                                  1/1     Running   0          39s
k8s-agent-76755c85bd-7wcvt                                    1/1     Running   0          40s
kagent-controller-6886fc4f5c-wn2xm                            1/1     Running   0          97s
kagent-grafana-mcp-5cc85fd598-hw6bk                           1/1     Running   0          97s
kagent-kmcp-controller-manager-76645f577f-n2r5v               1/1     Running   0          97s
kagent-querydoc-5f6fd94c98-64kxn                              1/1     Running   0          97s
kagent-tools-56c49d7d4d-6h8zg                                 1/1     Running   0          97s
kagent-ui-59d5bbd564-r7j5q                                    1/1     Running   0          97s
kgateway-agent-d97c5f7d-5qg2c                                 1/1     Running   0          40s
observability-agent-55d64bd489-987hm                          1/1     Running   0          40s
promql-agent-56c56b98bd-xvlzw                                 1/1     Running   0          39s
```

Once the foundation is ready, the course introduces KMCP and MCP servers. You will install a KMCP control plane and deploy one or more MCP servers (for example, an AWS-hosted MCP), enabling agents to query dynamic data sources or external APIs through the Model Context Protocol (MCP).

<Frame>
  <img alt="A presentation slide titled &#x22;What Is MCP?&#x22; showing a diagram of a Model Context Protocol connecting a Large Language Model (LLM) to data sources, tools, and external APIs. A small circular video inset of a speaker appears in the bottom-right corner." />
</Frame>

You will also build a custom MCP server. Example use case: agents fetch real-time cryptocurrency prices via an MCP endpoint so the agent can make data-driven decisions based on live market data.

Example lab output when starting local components (CLI header):

```bash theme={null}
Welcome to the KodeKloud Hands-On lab

KodeKloud
All rights reserved

controlplane ~ via 🐍 v3.10.12
```

The course covers system prompts and prompt engineering for agents: how to craft system-level prompts, structure instructions for predictable behavior, and manage prompt templates used by multiple agents. You will also learn to declare agents using YAML manifests for reproducible deployments.

Observability and debugging are core topics. We demonstrate tracing and telemetry with Jaeger to analyze end-to-end agent workflows, locate failures, and optimize performance. Example Jaeger Helm values for an all-in-one development deployment:

```yaml theme={null}
# jaeger.yaml - Jaeger Helm values for development (all-in-one)
provisionDataStore:
  cassandra: false

allInOne:
  enabled: true

storage:
  type: memory

agent:
  enabled: false

collector:
  enabled: false

query:
  enabled: false
```

Course structure (high-level):

| Module                    | Topics covered                                        | Outcome                                      |
| ------------------------- | ----------------------------------------------------- | -------------------------------------------- |
| KAgent Overview           | Architecture, dashboard, A2A protocol                 | Understand KAgent components and UI          |
| Installation & Validation | Helm manifests, kubectl checks, runtime pods          | Deploy KAgent to a cluster and validate pods |
| KMCP & MCP Servers        | KMCP control plane, MCP server deployment, custom MCP | Build and connect MCP servers to agents      |
| Agent Development         | YAML manifests, system prompts, integrations          | Create declarative and BYO agents            |
| Observability & Debugging | Jaeger tracing, logs, metrics                         | Trace agent workflows and debug issues       |
| Integrations & Labs       | Slack bot, AWS CloudWatch, LangGraph example          | Connect agents to real tools and services    |

Key components used in labs:

| Component               | Purpose                                             | Notes / Examples                                                           |
| ----------------------- | --------------------------------------------------- | -------------------------------------------------------------------------- |
| SLACK APP               | External integration for notifications and commands | Create at `api.slack.com/apps`; needs `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` |
| SLACK BOT (Python Bolt) | Local development bridge to KAgent                  | Runs `python main.py`, listens for `/mykagent`, formats Block Kit          |
| KAGENT AGENT            | Deployed in Kubernetes cluster                      | Declarative YAML manifests manage agent lifecycle                          |
| MCP Server              | Provides contextual data to agents                  | Can be AWS-hosted or self-hosted; serve model context to LLMs              |
| KMCP                    | Control plane for MCP servers                       | Coordinates MCP discovery and access                                       |

> **warning** Security note: never commit tokens or secrets (for example `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`) into source control. Use Kubernetes Secrets, environment variables at runtime, or a secrets manager.

Example environment variables used in labs:

```bash theme={null}
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-1-..."
export KAGENT_A2A_URL="http://127.0.0.1:8083/api/a2a/kagent/my-k8s-agent/"
```

Final hands-on lab: you will combine KAgent, MCP servers, system prompts, and observability to build a complete, deployable AI agent that integrates with external services like Slack and AWS CloudWatch. The course concludes with short quizzes after each section to reinforce key concepts.

Links and references:

* [LangGraph course](/user/courses/langgraph)
* [AWS CloudWatch course](/user/courses/aws-cloudwatch)
* [Jaeger Tracing](https://www.jaegertracing.io/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

By the end of this course you will be able to design, deploy, and operate AI agents on Kubernetes with KAgent — managing communication, observability, and integrations in production-grade environments.

- [Watch Video](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/a2bef22f-2221-4587-9f26-3c0bce28059e/lesson/e816a0eb-bb1b-4b1c-8d19-a786185f6b3c)


# Demo KAgent Overview Of UI and Agents

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/Introduction/Demo-KAgent-Overview-Of-UI-and-Agents/page

Overview of KAgent web UI showing agents, models, tools, and MCP server integrations for managing AI-driven Kubernetes automation and configuring LLM providers and tool actions

Welcome — this lesson walks through the KAgent web UI and the default configuration that exposes agents, models, tools, and MCP servers. You’ll learn how KAgent maps user queries to tools, where to manage LLM providers and models, and where to add integrations (MCP servers) and tools for richer automation on Kubernetes.

## Home screen and agents (what you’ll see first)

The home screen lists the agents available in your KAgent installation. In this demo, all built-in agents are enabled (Argo Rollouts, Istio, Helm, Kubernetes/k8s, observability, etc.). Note that the exact set of agents depends on the KAgent version and any custom components you installed. For this lesson we’ll use the Kubernetes (k8s) agent as the primary example to interact with a cluster.

From the Agents list you can open an agent, type natural-language queries (for example, “list pods in the `kagent` namespace”), and let the agent evaluate the request. The agent determines the appropriate tool to call, runs it, and returns the result.

<Frame>
  <img alt="A dark-themed screenshot of an AI agent interface where the user asks for the list of pods in the &#x22;kagent&#x22; Kubernetes namespace and a k8s_get_resources tool call is shown as completed. The right sidebar lists various Kubernetes actions and tools available to the agent." />
</Frame>

## How agents choose tools and show results

The right-hand tools panel displays the Kubernetes actions available to that agent. When you ask a question, the agent matches the intent to one or more tools (for example `k8s_get_resources`) and executes them. The result is presented in the chat or a console-style output.

Example output for listing pods:

```text theme={null}
• istio-agent-7b54a0bda-r-m8m1w (Running)
• k8s-agent-dcc57cd87-7vzsg (Running)
• kagent-controller-6f546c65bd-ckk6s (Running)
• kagent-grafana-mcp-597df4c7f4-gvjvf (Running)
• kagent-kmcp-controller-manager-86b48b656d-qz4hl (Running)
• kagent-querydoc-7dc78dc9d7-bcjcz (Running)
• kagent-tools-6d6695c5-7txp7 (Running)
• kagent-ui-5757fccb58-bsbbc (Running)
• kgateway-agent-6fbb9c8d87-dxmd4 (Running)
• observability-agent-749d568fb6-dnxpp (Running)
• promql-agent-5d6c7c76cb-kpqxc (Running)
```

## LLM Providers and Models (configure from the UI)

Each agent can be wired to one or more LLM providers and models. In this demo the configured provider is [OpenAI](https://openai.com), but you can add additional providers and models via the UI or by using configuration code if you prefer.

* Use the Models page to add providers, set model names, and provide authentication (API keys, tokens).
* The Create workflow in the UI lets you create new agents and assign models/providers to them.

<Frame>
  <img alt="A dark-themed web UI titled &#x22;Create New Model&#x22; on a site branded &#x22;kagent,&#x22; showing form fields for name, namespace, provider & model. The page also includes an Authentication section with an API key input." />
</Frame>

## Tools Library (what agents call to act)

Tools are the execution primitives agents call to interact with external systems (Kubernetes API, Helm, Argo, observability backends, etc.). KAgent ships with a default set of tools organized into categories. The Tools Library shows available categories and individual tool actions; these entries are what agents select when handling a query.

* Tools are extendable — you can add custom tools or MCP-based tool servers.
* Typical categories: Kubernetes (k8s), Helm, Argo, Datetime, Networking, Observability, and provider-specific integrations.

<Frame>
  <img alt="A dark-themed web UI showing a &#x22;Tools Library&#x22; for &#x22;kagent&#x22; with a search bar and expandable tool categories (Argo, Cilium, Datetime, Helm, etc.). Individual tool entries like &#x22;datetime_get_current_time&#x22; and &#x22;helm_get_release&#x22; are listed with brief descriptions." />
</Frame>

## MCP Servers (integrations and server endpoints)

MCP Servers are service integrations that provide additional functionality and tool endpoints for agents. The default deployment includes several MCP servers; you can add more (for example, cloud service integrations or custom tool servers) from the MCP Servers page.

* MCP Servers expose new tool capabilities and can host specialized tooling that agents call.
* You can register, configure, and remove MCP server entries in the UI.

<Frame>
  <img alt="A dark-themed kagent dashboard showing an &#x22;MCP Servers&#x22; list. It displays three server entries (kagent-grafana-mcp, kagent-querydoc, kagent-tool-server) and a purple &#x22;Add MCP Server&#x22; button." />
</Frame>

## Quick reference: UI pages and their purposes

| Page          | Purpose                                 | Typical actions                                   |
| ------------- | --------------------------------------- | ------------------------------------------------- |
| Agents        | Manage and interact with agents         | Open an agent, send queries, view tool calls      |
| Models        | Configure LLM providers and models      | Add provider, set model name, add API keys        |
| Tools Library | Inspect available tools and categories  | Search tools, view descriptions, add custom tools |
| MCP Servers   | Register integrations and tool backends | Add MCP server, configure endpoints and auth      |

## Next steps

* Create a new agent and attach a model via the Create workflow.
* Add or configure LLM providers on the Models page.
* Explore the Tools Library and enable or add tools your agents need.
* Register additional MCP servers to extend capabilities (e.g., cloud services, observability).

> **lightbulb** Note: The exact agents, tools, and MCP servers available in your KAgent installation depend on the version and the components you installed. The UI lets you extend and customize these elements.

## Links and references

* [OpenAI](https://openai.com)
* [AWS](https://aws.amazon.com)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

That completes the high-level UI and default configuration overview. In the next lesson we’ll create and configure an agent end-to-end, wire it to a model, and add a custom tool to extend behavior.

- [Watch Video](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/a2bef22f-2221-4587-9f26-3c0bce28059e/lesson/d9cb5a2c-3514-4e80-86a3-01b0d624d945)
