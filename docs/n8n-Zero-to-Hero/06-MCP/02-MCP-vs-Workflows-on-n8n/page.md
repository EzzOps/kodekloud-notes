# MCP vs Workflows on n8n

Source: https://notes.kodekloud.com/docs/n8n-Zero-to-Hero/MCP/MCP-vs-Workflows-on-n8n/page

Comparison of MCPs versus sub-workflows in n8n, explaining tradeoffs in exposure, latency, cost, modularity, and when to use each for integrations and AI agent access

This article clarifies the practical differences between MCPs (Modular Connector/Capability Providers) and sub-workflows in n8n, and helps you choose the right pattern for integrating tools, automations, or external AI agents.

MCPs are a convenient way to expose a group of apps or tools to an AI agent or other external clients. A common architecture looks like this: an AI agent calls a "news" MCP client, which in turn routes to several research app nodes, or it calls an "email" MCP client that connects to one or more Gmail/email account nodes.

<Frame>
  <img alt="The image shows a workflow editor interface in n8n, featuring nodes connected to create automation processes. It includes tools like an AI Agent, OpenAI Chat Model, and various MCP clients and servers." />
</Frame>

At a high level both MCPs and sub-workflows let an orchestrator route requests to distinct toolsets or logic chains. Functionally you can often implement equivalent behavior either by calling an external MCP endpoint or by wiring sub-workflows together inside n8n. The differences show up in scope, invocation, latency, operational cost, and maintainability.

Comparison at a glance

| Dimension          |                                                                                               MCP (external endpoint) | Sub-workflow (internal)                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------- |
| Scope / Exposure   | Exposes an endpoint external systems (including AI agents) can call. Great for external integrations and formal APIs. | Lives inside n8n runtime. Only callable by other workflows or nodes within the same n8n instance.             |
| Invocation         |                                                                     HTTP/agent call; can be invoked from outside n8n. | Invoked internally by workflow nodes (`Execute Workflow` / sub-workflow nodes).                               |
| Latency & Hops     |                                    Typically introduces network hops and potentially extra agent runs — more latency. | Runs inside n8n process — lower network overhead and typically faster.                                        |
| Operational cost   |        May increase run counts if an external orchestrator calls multiple MCP endpoints (possible "double-handling"). | May still count as separate executions depending on hosting/billing model, but avoids external network calls. |
| Modularity & Reuse |                               Clean external surface for third-party use, useful when you need a stable API contract. | Fast to develop and refactor inside n8n; ideal for internal modularization.                                   |
| Best fit           |                      When you need a public or cross-system API (e.g., to expose capabilities to external AI agents). | When you want lightweight internal modularity and lower orchestration overhead.                               |

Key considerations

* Scope and exposure
  * MCP: Designed to expose callable endpoints. Use MCPs when you want third-party systems or external AI agents to directly invoke capabilities inside n8n.
  * Sub-workflow: Stays inside n8n and is only invoked by other workflows or nodes in the same environment.

* Operational overhead and cost
  * External agent + MCP calls can create effectively a two-step flow — an agent decides which MCP endpoint to call, leading to extra runs, more latency, and additional cost.
  * Internal sub-workflows avoid external network hops. Note: billing models vary — some n8n hosting counts each invoked workflow as a separate execution. Check your plan’s execution/pricing rules.

* Modularity and developer speed
  * Sub-workflows are quick to create, refactor, and maintain within n8n.
  * MCPs formalize the integration boundary and are better when you want a stable, discoverable API surface that other teams or systems will use.

Best-practice example: exposing an email flow via MCP

A common MCP use case is an email MCP server that exposes an endpoint like `/email/send`. External clients (for example, an AI agent) can send requests to that endpoint and trigger email flows inside n8n. When you implement this pattern, consider authentication for the MCP endpoint, payload validation, idempotency, and monitoring.

Example: calling an email MCP endpoint (simple curl example)

```bash theme={null}
curl -X POST "https://mcp.example.com/email/send" \
  -H "Authorization: Bearer <YOUR_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"to":"alice@example.com","subject":"Hello","body":"Hi Alice"}'
```

<Frame>
  <img alt="The image shows a software interface for setting up an Email MCP Server with options for MCP URL, authentication, and path, and a button to execute a test step. The output section is currently empty, prompting to execute the node or set mock data." />
</Frame>

Operational checklist when choosing MCP vs sub-workflow

* Do you need an external-facing API? → Choose MCP.
* Is minimal latency and fewer network hops important? → Prefer sub-workflows.
* Will other teams or external agents call this capability? → Prefer MCP with authentication and versioning.
* Is rapid iteration and internal refactoring more important? → Use sub-workflows.

> **lightbulb** Choose sub-workflows for fast internal modularization and lower orchestration overhead. Choose MCPs when you need to expose functionality outside n8n (for example, to external AI agents or third-party services).

Summary

* MCPs are the right choice when you need a well-defined, external-facing API surface for agents or third-party systems.
* Sub-workflows are best for internal modularity, faster iteration, and reduced network overhead.
* Both approaches are production-ready in n8n today. The correct pattern depends on your architecture, performance requirements, cost model, and who will be calling the automation.

Links and references

* [n8n Documentation](https://docs.n8n.io/)
* [Designing APIs for integrations — general guidance](https://developer.mozilla.org/)
* Consider reviewing your n8n hosting/billing docs to confirm how internal workflow invocations are counted.

- [Watch Video](https://learn.kodekloud.com/user/courses/n8n-zero-to-hero/module/e2e9ccd6-d35a-4a9e-b758-7918221eedc3/lesson/2ac5b9fb-cb2e-4dc9-ac7e-37039c658180)
