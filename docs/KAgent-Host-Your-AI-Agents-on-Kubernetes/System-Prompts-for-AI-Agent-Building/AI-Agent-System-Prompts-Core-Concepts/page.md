# Core MCP server logic and utilities
# Your MCP tool implementations
# Entry point that starts the MCP server
# Built-in test suite for tools
# Used to containerize for Kubernetes
# KMCP config defining how server runs
# Python dependencies and project settings
# Sample environment variables
# Project documentation
```

MCP Go project layout:

```text theme={null}
my-mcp-server/
├─ main.go                           # Entry point for the MCP server
├─ go.mod                            # Go module configuration
├─ go.sum                            # Dependency integrity file
├─ tools/                            # Tool implementations
│  ├─ all_tools.go                   # Registers all tools with the server
│  ├─ echo.go                        # Example tool
│  └─ tool.go                        # Template for creating new tools
├─ Dockerfile                        # Container image definition
├─ kmcp.yaml                         # KMCP project configuration
└─ README.md                         # Project documentation
```

## Framework comparison

|        Framework |                      Best for                     | Strengths                                                                   |
| ---------------: | :-----------------------------------------------: | :-------------------------------------------------------------------------- |
| FastMCP (Python) |   Rapid development, teams with Python expertise  | Lightweight, easy to iterate, many Python libraries for integrations        |
|           MCP Go | High-throughput and performance-critical services | Type-safe tool definitions, lower-latency runtime, strong concurrency model |

<Frame>
  <img alt="A presentation slide titled &#x22;Framework Comparison&#x22; showing a split panel comparing FastMCP Python (left) and MCP Go (right) with bullet points listing best use-cases for each (e.g., quick development and Python developers vs high-throughput services and performance-critical applications)." />
</Frame>

## KMCP core components and CLI

* CLI commands:
  * `kmcp init` — Initialize a new MCP project.
  * `kmcp add-tool` — Add a new tool boilerplate to the project.
  * `kmcp run` — Run the MCP server locally for testing.
  * `kmcp deploy` — Deploy the MCP server to Kubernetes.
* Boilerplate code and example tools follow recommended patterns.
* Containerization: `Dockerfile` included in scaffold.
* Project configuration: `kmcp.yaml` includes environment variables, transport settings, and metadata.

```bash theme={null}
# Common kmcp commands
kmcp init    # Initialize new MCP project
kmcp add-tool  # Add new tool boilerplate
kmcp run     # Run locally for testing
kmcp deploy  # Deploy to Kubernetes
```

## Running KMCP on Kubernetes

KMCP integrates with Kubernetes using Custom Resource Definitions (CRDs) to represent MCP server resources. It supports multiple transport types:

* stdio transport (process-based)
* HTTP transport (configure port, target port, path-based routing)

For HTTP transports you can configure HTTP path, service port, and authorization rules. KMCP supports authorization integrations, including an MCP authorization server and providers like Keycloak.

<Frame>
  <img alt="A teal-themed slide titled &#x22;KMCP in Kubernetes&#x22; showing four top boxes: Transport Types, HTTP Transport Configuration, Authorization, and Lifecycle Management. Below is a panel listing features: MCP authorization server support, Keycloak provider integration, and resource metadata for authentication." />
</Frame>

<Callout icon="warning">
  When deploying to Kubernetes, secure your secrets and authorization settings. KMCP manages secret injection, but you should review RBAC, network policies, and authorization providers (for example, Keycloak) to ensure least-privilege access to sensitive tools and data.
</Callout>

### Lifecycle management

KMCP automates:

* Deployments and updates
* Health checks and status conditions
* Secret management and rotation support
* Scaling and resource metadata injection

## Use cases

|                  Use Case | Description                                                                                                        |
| ------------------------: | :----------------------------------------------------------------------------------------------------------------- |
|   Custom tool development | Expose business logic and internal systems to LLMs via MCP tools.                                                  |
|    Kubernetes integration | Deploy MCP servers as Kubernetes workloads (pods / CRDs), manage secrets and lifecycle, scale like other services. |
| Standardized integrations | Avoid per-tool adapters by using the MCP protocol to maintain consistent integration patterns.                     |

<Frame>
  <img alt="A presentation slide titled &#x22;Use Cases&#x22; with three blue rounded panels labeled &#x22;Custom Tool Development,&#x22; &#x22;Kubernetes Integration,&#x22; and &#x22;Standardized Integrations,&#x22; each showing an icon and brief bullet points. The layout highlights different application scenarios and features for a software platform." />
</Frame>

## Benefits

For developers:

* Rapid iteration via boilerplates and templates.
* Multiple framework support (Python, Go).
* Local testing with the MCP Inspector and integrated examples.

<Frame>
  <img alt="A presentation slide titled &#x22;Benefits&#x22; showing a &#x22;For Developers&#x22; panel and four numbered items: fast development with boilerplates, multiple framework support, local testing with inspector, and best practices built-in. The layout uses teal accents, icons, and a dark left sidebar." />
</Frame>

For operations:

* Kubernetes-native deployment and lifecycle.
* Automatic health-checks and status reporting.
* Secret management and scalable architecture.

<Frame>
  <img alt="A presentation slide titled &#x22;Benefits&#x22; listing three operations items: Kubernetes-native deployment, automatic lifecycle management, and secret management. A dark left panel labeled &#x22;For Operations&#x22; shows a gear icon." />
</Frame>

For organizations:

* A standardized protocol reduces maintenance overhead, simplified scaling, and consistent integration patterns without vendor lock-in.

<Frame>
  <img alt="A slide titled &#x22;Benefits&#x22; showing a numbered list of advantages for organizations: Standardized protocol (MCP), Reduced maintenance overhead, Easier scaling, and Consistent integration patterns. A dark left panel features a building icon and the label &#x22;For Organizations.&#x22;" />
</Frame>

## Summary

KMCP enables you to:

* Rapidly scaffold MCP servers with best-practice templates.
* Develop and test tools locally using the MCP Inspector.
* Deploy and manage MCP servers in Kubernetes with CRDs, health checks, and secret handling.
* Choose the framework that fits your needs: FastMCP for Python or MCP Go for high-throughput services.

## Next steps / Labs

Suggested hands-on labs:

* Deploy MCP servers to Kubernetes (including AWS).
* Integrate LLM-driven agents with an AWS Pricing MCP server.
* Build a custom cryptocurrency-check MCP server to fetch live prices.

References and further reading:

* MCP (Model Context Protocol) — [https://github.com/anthropic/mcp](https://github.com/anthropic/mcp)
* Keycloak — [https://www.keycloak.org](https://www.keycloak.org)

I'm excited to share the labs with you — happy building!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/dacd107b-93e4-497f-b0fa-b872f0300527" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/e50e4420-d5bb-46a9-b9fd-b1e827a675dc/lesson/770747d1-dd16-4c12-b682-2fdb408ed4fe" />
</CardGroup>


# AI Agent System Prompts Core Concepts

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/System-Prompts-for-AI-Agent-Building/AI-Agent-System-Prompts-Core-Concepts/page

Explains core concepts and best practices for designing system prompts that define agent instructions, tool usage, and user query handling to build reliable, safe AI agents

Welcome — this lesson explains the core concepts behind system prompts for declarative AI agents. System prompts are the single most important artifact when defining an agent: they set the agent’s role, behavior, and decision-making style. Good system prompts combined with the right tools and query handling produce reliable, useful agents.

<Callout icon="lightbulb">
  System prompts act like an agent’s job description and personality. Designing them clearly is the key to building predictable, safe, and effective agents.
</Callout>

Prompt engineering for agents is a newer discipline compared with traditional software development. It requires iterative design, testing, and a different mental model—one that treats prompts, tools, and queries as co-evolving pieces of the agent’s behavior.

Core concepts you must consider when writing system prompts:

1. Agent instructions
2. Tools
3. User queries

We’ll define each, show how they combine into an end-to-end workflow, and summarize design priorities and best practices.

## 1 — Agent instructions

Agent instructions are the heart of a system prompt. They tell the LLM:

* The agent’s role and domain expertise (for example: “You are an infrastructure expert.”)
* The agent’s goals and constraints
* Expected behaviors such as safety checks, confirmation steps, and error-handling rules

These instructions are provided alongside the user query to the LLM and influence both natural-language responses and the agent’s decision logic. Think of them as the agent’s personality and job description.

Best practice examples:

* Define the agent’s role explicitly: “You are a Kubernetes troubleshooting assistant.”
* Explicitly state limits: “Do not delete resources without confirmation.”
* Provide examples of desired response style and level of detail.

## 2 — Tools

Tools are the functions, APIs, or capabilities the agent may call to interact with its environment. They are the agent’s “hands and eyes.”

* Examples for a Kubernetes-style agent: `list_resources`, `get_logs`, `describe_service`, `delete_pod`.
* Tools enable actions that go beyond text (query state, make changes, or call external APIs).
* The system prompt should document available tools and any usage constraints.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Core Concepts&#x22; showing a tools icon labeled &#x22;Tools&#x22; with the subtitle &#x22;Functions enabling agent interaction.&#x22; Below is a bordered example box referencing a Kubernetes agent and a grey button labeled &#x22;List pods.&#x22;" />
</Frame>

Tools are provided to the agent by the runtime environment. The agent decides when and which tool to call based on instructions and the user query.

## 3 — User query

The user query is the input that triggers the agent workflow.

* It supplies intent and task details the agent must satisfy.
* Designers have less control over user input, so anticipate likely variations and edge cases.
* Combine robust instructions and a well-chosen toolset to handle noisy or ambiguous queries.

## End-to-end workflow

The agent workflow is the combination of:

* Agent instructions (role and behavior)
* Tools (what actions are available)
* User query (the task to perform)

These three inputs are passed to the LLM. The LLM evaluates the query in the context of the instructions, may call tools to gather state or take action, and returns a final response or result.

<Frame>
  <img alt="A dark-themed flowchart titled &#x22;How They Work Together&#x22; showing an LLM workflow. It shows Agent Instructions combined with Tools and User Input feeding into LLM Processing, which then generates a response." />
</Frame>

## Key relationships

### Agent instructions + Tools

* Instructions define what the agent should be and how it should behave.
* Tools define what actions the agent can take.
* Together they form the agent’s full capability set.

Example:

* Instruction: “You are an infrastructure expert.”
* Tools: `list_resources`, `get_logs`, `describe_service`
* Outcome: The agent understands operational tasks and can perform them programmatically.

<Frame>
  <img alt="A dark presentation slide titled &#x22;Key Relationships&#x22; showing two circular icons labeled &#x22;Agent Instructions&#x22; and &#x22;Tools&#x22; connected by a plus sign. Below is an example saying &#x22;You are a Kubernetes expert&#x22; with a robot icon and tool commands like list_pods, get_logs, and describe_service, plus a highlighted caption about the agent." />
</Frame>

Note: This lesson uses a container orchestration platform (Kubernetes) as a concrete example. The principles apply to other domains (databases, cloud infra, support bots, browsing agents, etc.).

### Agent instructions + User query

* Instructions guide how to interpret and act on queries.
* Queries provide specifics and context for tasks.

Example:

* Instruction: “Always verify before making changes.”
* Query: “Delete resource xyz.”
* Result: The agent checks whether the resource exists and asks for explicit confirmation before deleting.

<Frame>
  <img alt="A presentation slide titled &#x22;Key Relationships&#x22; showing icons for &#x22;Agent Instructions&#x22; and &#x22;User Query&#x22; with a plus sign between them. Below is an example pairing — &#x22;Always verify before making changes&#x22; vs &#x22;Delete pod xyz&#x22; — and a highlighted note: &#x22;Agent verifies the pod exists and confirms before deleting.&#x22;" />
</Frame>

### Tools + User query

* The query indicates which tools to use.
* Tools provide the mechanism to fulfill the request.

Example:

* Query: “Show me the logs for resource xyz.”
* Possible flow: call `list_resources` to locate the target, then `get_logs` to retrieve logs.

## Design considerations (by priority)

Prioritize your design effort where it yields the most control and impact:

| Priority | Focus area         | Why it matters                                                                                             |
| -------: | ------------------ | ---------------------------------------------------------------------------------------------------------- |
|        1 | Agent instructions | You fully control instructions; they steer behavior across diverse queries.                                |
|        2 | Tools              | Tools determine what the agent can actually do—provide functions that match expected tasks.                |
|        3 | User queries       | You can’t fully control inputs; anticipate common variations and design instructions/tools to handle them. |

<Frame>
  <img alt="A presentation slide titled &#x22;Design Considerations&#x22; showing three numbered blue panels with icons. Each panel summarizes instruction-related points: controlling instructions and tools, handling varying user queries, and giving clear instructions to help an agent interpret queries." />
</Frame>

<Callout icon="warning">
  Prioritize writing clear, constrained instructions first. Ambiguous instructions lead to unpredictable tool usage and unsafe actions.
</Callout>

## Best practices for writing system prompts

* Start explicit: state the agent’s role and primary objectives upfront.
* Declare capabilities and limits: enumerate what the agent can and cannot do.
* Describe behaviors: require confirmation flows, safety checks, and error-handling policies.
* Document tools in the prompt: list available tool names (e.g., `list_resources`, `get_logs`) and give usage examples.
* Anticipate user queries: include examples and edge cases the agent should handle.
* Test iteratively: simulate diverse queries and tool-call sequences before production.

Tip: Use short, deterministic rules for critical actions (deletions, credential changes) and keep conversational flexibility for information retrieval and diagnostics.

## Key takeaways

* Agent instructions are the foundation—they define who the agent is and how it behaves.
* Tools are the mechanisms that allow the agent to interact with real systems.
* User queries drive action; they trigger the agent’s internal logic and tool usage.
* The combination of instructions, tools, and query handling produces practical, reliable agents.

<Frame>
  <img alt="A presentation slide titled &#x22;Key Takeaways&#x22; listing four numbered points about agent instructions, tools, the user query, and how the components work together. The layout has a dark left column and light right area with turquoise numbered markers." />
</Frame>

Further reading and references:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Prompt engineering resources and best practices](https://learnprompting.org/)
* Consider runtime/tooling docs for your agent framework (tool registration, schema, and security).

As we’ve established the importance of system prompts, the next lesson will walk through how to build a concrete system prompt and register tools for an agent.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/9516a0aa-00b1-4461-a622-cc60e510c96a/lesson/0793531c-b061-43b0-9e6a-a591341f2408" />
</CardGroup>
