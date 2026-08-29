# Referencing existing MCP tools
- type: McpServer
  mcpServer:
    name: kagent-tool-server
    kind: RemoteMCPServer
    toolNames:
      - k8s_get_resources
      - k8s_get_available_api_resources

# Referencing an existing agent as a tool
- type: Agent
  agent:
    ref: promql-agent
```

This pattern enables workflows where agents delegate specialized tasks (e.g., query translation, enrichment, or cloud access) and then aggregate the results.

Agent execution flow
A concise end-to-end agent execution loop in K-Agent:

1. Agent receives a user query.
2. Agent analyzes the query using its instructions and skills.
3. Agent determines which tools to call.
4. Agent executes the selected tools to interact with the environment.
5. Agent processes tool results (often using an LLM to interpret or aggregate responses).
6. Agent returns a consolidated response to the user.

This loop is central to K-Agent’s autonomous behavior and to how tools extend agent capabilities.

<Frame>
  <img alt="A flowchart titled &#x22;Agent Execution Flow&#x22; showing six connected boxes that outline steps an agent takes: receives a user query, analyzes it, determines and executes tools, processes results, and returns a response. Arrows show the sequence between each step." />
</Frame>

Key architecture principles
K-Agent is designed around a few core principles:

* Kubernetes-native: Agents are CRD-based and lifecycle control (pods, controllers) leverages Kubernetes.
* Framework-based: Built on the Google Agent Development Kit (ADK) to provide an extensible agent framework.
* Multiple entry points: Agents are accessible via CLI, dashboard UI, and declarative CRDs.

Tool interaction patterns include built-in tools, MCP-based external tools, and composition where agents are used as tools. Agents are defined by instructions and skills which guide autonomous behavior.

Architecture components
Below is a quick reference for the main architecture components and their responsibilities:

|         Component |  Language | Responsibility                                   |
| ----------------: | :-------: | ------------------------------------------------ |
|        Controller |     Go    | Manages CRDs and agent lifecycle in Kubernetes   |
|      Engine / App |   Python  | Runs agent conversation loops (ADK-based)        |
|               CLI |     Go    | Command-line management interface                |
|    Dashboard / UI |    Web    | Visual management and inspection of agents       |
| Agent definitions | YAML/CRDs | Instructions, skills, and composition for agents |

<Frame>
  <img alt="A slide titled &#x22;Summary&#x22; depicting the kagent architecture with four boxed components: Controller, Engine/App, CLI, and Dashboard/UI. Each box shows language icons (Go, Python) and brief notes about managing agent CRDs/lifecycle, running the agent conversation loop, a CLI for management, and a web UI for visual agent management." />
</Frame>

What makes K-Agent effective
Some of the key features that make K-Agent powerful and extensible:

* Kubernetes-native operation for seamless lifecycle management
* Built on the ADK framework for extensibility
* Support for multiple LLM providers and model integrations
* Agent composition (using agents as tools) to build higher-level behaviors
* Extensibility through MCP to incorporate external services and cloud APIs

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Summary&#x22; with the &#x22;kagent&#x22; logo and a &#x22;Key Features&#x22; section. Five boxed features read: &#x22;Kubernetes-native,&#x22; &#x22;Built on ADK framework,&#x22; &#x22;Supports multiple LLM providers,&#x22; &#x22;Agent composition (agents as tools),&#x22; and &#x22;Extensible through MCP.&#x22;" />
</Frame>

> **lightbulb** K-Agent’s MCP support and agent-composition features let you extend capabilities incrementally: add new external tools via MCP, and compose focused agents to build higher-level behavior without changing core components.

Security and governance (quick note)

> **warning** When exposing external tools or agents, carefully manage credentials and RBAC. Grant least-privilege access to MCP adapters and ensure agents cannot perform unauthorized operations in your cluster or cloud account.

Hands-on exercises are available to practice the concepts above—examples include installing MCP adapters, registering AWS tools, creating a PromQL agent, and composing agents to solve end-to-end tasks.

- [Watch Video](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/434776f7-37e5-432d-94f4-db0754f83a8f)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/45e1f0ac-8ec5-4cb3-8804-9953a96a67b5/lesson/331e8954-80dd-4887-b79f-f7fb1ef54f07)


# Demo Create AI Agents Using AWS MCP Servers In action

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KMCP-Installation-Overview/Demo-Create-AI-Agents-Using-AWS-MCP-Servers-In-action/page

Lab walkthrough to deploy declarative AI agents with AWS MCP servers and KAgent UI to query real-time AWS pricing, attach pricing tools, run queries, and troubleshoot

Welcome to this lab-style walkthrough. We'll extend the previously deployed AWS MCP server by connecting declarative agents to it, then use those agents to query real-time AWS pricing. This guide shows how to:

* Inspect MCP servers and agents in the KAgent UI
* Deploy a declarative LLM-only agent and observe its behavior
* Update the agent to attach AWS Pricing MCP server tools and compare results
* Run simple and complex pricing queries through the agent

This content assumes you have the AWS Pricing MCP server and KAgent UI already running in your cluster.

## Overview — What you'll learn

* How to register an agent that relies only on the LLM (no tools)
* How to attach MCP server tools to the agent so it can call AWS Pricing APIs
* How the agent invokes tools, receives structured pricing JSON, and produces human-friendly responses
* Operational checks and debugging patterns for agents + MCP servers

## Access the KAgent UI

* Open the KAgent UI (top-right in your environment).
* Skip the initial wizard if prompted and go to the main view.

## Inspect running agents

* In the KAgent UI, go to View → Agents to see registered agents.
* At the start of this demo there are no agents registered.

## Deploy an LLM-only agent (no tools)

A declarative agent manifest is provided at `/root/no_tool_aws-price-checker.yaml`. This agent is named `aws-price-check` and declares no tools, so it will rely entirely on the LLM (no live pricing calls).

Example agent manifest (LLM-only)

```yaml theme={null}
apiVersion: kagent.dev/v1alpha2
kind: Agent
metadata:
  name: aws-price-check
  namespace: kagent
spec:
  declarative:
    modelConfig: default-model-config
    stream: true
  systemMessage: |-
    You are an AWS Pricing Expert Agent, designed to help users get accurate and comprehensive AWS pricing information.

    # Core Responsibilities
    - Provide real-time AWS service pricing data using available pricing tools
    - Generate detailed cost reports and analysis
    - Compare pricing across different AWS regions and configurations
    - Help users understand AWS pricing models and cost optimization opportunities

    # Instructions
    - Always use the available AWS pricing tools to get accurate, real-time data
    - If user question is unclear, ask for specific details like service name, region, instance type, or usage patterns
    - Provide pricing in the requested currency and region when specified
    - Include relevant pricing attributes and dimensions in your analysis
    - Always be helpful and provide actionable cost insights
    - If you don't know how to answer, tell the user "Sorry, I don't have that pricing information available" and suggest what details might help

    # Response format:
    - ALWAYS format your response as Markdown
    - Include a summary of pricing queries performed and tools used
    - Present pricing data in clear, easy-to-read tables or lists
    - Provide cost optimization recommendations when relevant
    - Include any assumptions made in pricing calculations
```

Apply the agent manifest and check status

```bash theme={null}
