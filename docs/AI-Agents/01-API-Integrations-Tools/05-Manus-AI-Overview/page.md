# Add chart repo and update
helm repo add mcp https://charts.example.com/mcp
helm repo update

# Install MCP server in a hub cluster
helm install mcp-server mcp/mcp-server --namespace mcp-system --create-namespace

# Install an MCP client in a satellite cluster and point it at the server
helm install mcp-client mcp/mcp-client --namespace mcp-client --create-namespace \
  --set server.url="wss://mcp-server.example.com" \
  --set server.auth.token="YOUR_TOKEN_HERE"
```

After installation, confirm client tunnels and service registrations using kubectl and your MCP server status endpoints:

```bash theme={null}
kubectl get pods -n mcp-system
kubectl get pods -n mcp-client
# Check registered services (implementation-specific)
kubectl get services -A
```

<Frame>
  <img alt="The image outlines steps for deploying MCP with Helm, including installing MCP server, deploying clients, using Helm charts, defining services, and validating tunnels and service registry." />
</Frame>

Best practices for operating MCP at scale

* Separate agents by role and region. Keep memory, inference, and control agents in different clusters based on operational needs.
* Avoid exposing sensitive services directly; always prefer tunneled access via MCP.
* Monitor tunnel health and connection metrics. Latency spikes or dropped tunnels directly affect agent performance.
* Integrate MCP logs and metrics into your observability stack (Prometheus, Grafana, EFK/ELK) to trace cross-cluster requests and speed up debugging. See Learn By Doing: AIOps Foundations - Intelligent Monitoring With Prometheus & Grafana and EFK Stack: Enterprise-Grade Logging and Monitoring.
* Document service ownership per cluster to prevent overlap and ensure predictable routing.

<Frame>
  <img alt="The image provides best practices for scaling AI agents, including monitoring tunnel health, using MCP to manage clusters, integrating logs into pipelines, and tunneling APIs." />
</Frame>

Limitations and monitoring considerations

* Latency: Tunneling adds overhead. For high-frequency, low-latency workloads, measure end-to-end latency and consider colocating tightly-coupled components.
* Tunnel health: If a WebSocket tunnel drops, agent communication fails. Implement robust reconnection logic and active health checks.
* Debugging complexity: Cross-cluster flows are multi-hop. Centralize logs and traces to reconstruct interactions across clusters.
* Autoscaling: Many MCP implementations don’t auto-scale proxies out-of-the-box. Integrate with existing orchestration/autoscaling tools to handle load surges.

<Callout icon="warning">
  Monitor tunnel availability and end-to-end latency closely. For latency-sensitive inference, evaluate colocating inference components or using dedicated low-latency links rather than relying solely on cross-cluster tunnels.
</Callout>

<Frame>
  <img alt="The image outlines four limitations and monitoring considerations for a system, including latency overhead, tunnel health monitoring, debugging complexity, and integration of logs into the observability stack." />
</Frame>

Wrap-up

Kubernetes MCP is a practical solution for connecting distributed AI agents across clusters and network boundaries while preserving security, modularity, and deployment autonomy. With proper observability, authentication, and deployment hygiene, MCP simplifies multi-cluster AI architectures and enables teams to place services where they are most effective. For production-grade setups, combine MCP with strong certificate management, centralized logging/tracing, and an automation strategy for scaling and failover.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/d2a91525-d4e7-4c2a-866a-e7a9d34b538c/lesson/c21d81e4-9aa5-437e-8d6b-a3e5e171049c" />
</CardGroup>


# Manus AI Overview

Source: https://notes.kodekloud.com/docs/AI-Agents/API-Integrations-Tools/Manus-AI-Overview/page

Overview of Manus AI, an open source agent operating system for building persistent, long‑horizon agents with world models, durable memory, planning, tool integration, and observability

This lesson explains Manus AI — an open-source framework and operating-model for building persistent, long-horizon AI agents. Key topics covered:

* What Manus AI is and its core mission
* How Manus is architected and its main components
* Feature set and agent capabilities
* Manus as an AI operating system (OS) for long-running agents
* Interoperability with LLMs and external tools
* Developer experience, observability, and example configuration
* Practical use cases and real-world applications
* How Manus compares to other agent platforms
* Limitations, risks, and future directions

Manus represents a conceptual shift: treat agents as long-running, process-driven entities with persistent memory, planning loops, and explicit world-state models. It exposes system-level APIs that mirror operating-system patterns for coordinating resources — useful for developers building adaptive, persistent AI services rather than one-off prompt pipelines.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Manus AI – Signaling the Future of Agent Operating Systems,&#x22; highlighting four features: enabling long-horizon agents, world modeling, serving as an OS for orchestration, and promoting open, modular architecture." />
</Frame>

## What is Manus?

Manus is a full-stack, open-source framework tailored to build intelligent, persistent agents — not just another orchestrator or prompt wrapper. It behaves like an operating system for agents, designed for continuous adaptation and long-horizon planning.

The design draws inspiration from cognitive cycles: reflect → remember → act → adapt. Manus agents run over extended timeframes (hours to weeks) by using:

* persistent, vector-backed memories,
* structured planners and execution graphs,
* evolving world models.

This approach departs from reactive prompt-chaining toward agents that can reflect on prior actions, replan, and change behavior over time.

<Frame>
  <img alt="The image is an introduction slide for Manus AI, featuring text that states &#x22;Manus supports evolving agents grounded in persistent memory,&#x22; alongside an illustration of a person interacting with a digital representation of a brain and AI elements." />
</Frame>

## Mission: world modeling and persistent cognition

Manus reframes agents as thinking systems rather than stateless tools. Agents maintain internal world models that are continuously updated as conditions change. Core design goals include:

* Long-running persistence across sessions
* Durable memory that survives restarts
* Primitives for constructing and evolving world models
* Structured autonomy via tool selection and API calls

These capabilities make Manus suitable for applications that need continuous context, historical awareness, and goal-directed autonomy.

<Frame>
  <img alt="The image outlines a core design and mission emphasizing world modeling, memory, and flexible tool use to support long-running, persistent agents, aiming to enable general intelligence through structured autonomy." />
</Frame>

## Architecture and core components

Manus is modular around a central execution graph that models agent behavior as a network of planned steps and decision points. The canonical Manus cycle is: observe → plan → act → reflect. Main components include:

* Execution graph (planner + execution + verification)
* Persistent memory (vector-backed long-term store)
* Tool integration layer (abstracted external actions)
* World-state manager (evolving internal model)
* Observability/tracing components

A typical multi-agent pattern separates responsibilities:

* Planner agent: decomposes goals into tasks
* Execution agent: performs actions and calls tools
* Verification agent: checks outcomes and triggers corrections

This separation enables automated feedback loops and continuous improvement.

<Frame>
  <img alt="The image is a flowchart illustrating how Manus AI works using a multi-agent architecture, with components labeled as Planner Agent, Execution Agent, and Verification Agent, interacting to process requests and complete tasks." />
</Frame>

## Key features — what Manus provides

Manus elevates agents beyond single-shot generation by providing:

* World modeling: persistent, evolving internal representations of environments and entities
* Memory abstraction: retrievable long-term context that endures restarts
* Embodied planning: decisions that combine objectives, memory, and environment state
* Time-aware planning: schedule-aware reasoning over hours, days, or weeks

These primitives enable durable workflows, adaptive behavior, and richer automation patterns.

<Frame>
  <img alt="The image highlights four key features: time-aware planning, embodied planning, world modeling, and memory abstraction, each represented within a segmented circular diagram." />
</Frame>

## Manus as an AI operating system

Manus treats agents as first-class processes: pause, resume, delegate, and hand off tasks across agents or services. At a system level, Manus exposes APIs to:

* Manage agent lifecycle and state
* Read/write persistent memory
* Register and call tools or external APIs
* Trace execution and observe agent decisions

This OS-like approach supports delegation, concurrency, lifecycle management, and event-driven behavior — useful for building interoperable, long-lived AI services.

<Frame>
  <img alt="The image describes &#x22;Manus as an AI OS,&#x22; highlighting its system-level APIs for managing agents in state, memory, tool usage, and external interaction, with a note on its structured, long-running AI app capability." />
</Frame>

## Interoperability with LLMs and external tools

Manus is model-agnostic and separates reasoning from tool execution. Typical setup:

* LLMs (e.g., Claude, GPT-4, Mistral, LLaMA) provide inference and planning guidance
* Tools (APIs, browser automations, local plugins) are abstracted into callable modules
* Runtime selects tools dynamically based on planner decisions

This reduces brittle prompt engineering and enables composable workflows where LLMs focus on reasoning and the Manus runtime handles execution and integration.

<Frame>
  <img alt="The image showcases interoperability with large language models (LLMs) and tools, listing models like Claude, OpenAI's ChatGPT 4.0, Mistral AI, and LLaMA by Meta. It mentions the capability to call external APIs, tools, or local plugins." />
</Frame>

## Developer experience, observability, and example configuration

Manus provides a Python implementation and is distributed under an open-source license. Developers declare agents with declarative configuration files to improve reproducibility and version control. Observability features include logging, state tracing, and debugging tools that fit typical DevOps workflows.

Example minimal agent declaration (YAML):

```yaml theme={null}
agent:
  id: research-assistant
  roles:
    - planner
    - executor
  memory:
    backend: vector_db
    vector_store: weaviate
  tools:
    - name: web_search
      type: api
      endpoint: "https://api.example-search.com/v1/query"
  schedule:
    run_interval: "1h"
```

<Callout icon="lightbulb">
  Use declarative agent configs for reproducibility. Store them in Git and pair with CI/CD to control agent versions and rollout.
</Callout>

Observability and telemetry help monitor agent health, trace decision paths, and audit tool usage — essential for production deployments.

## Typical use cases

Manus excels in scenarios that require sustained planning and memory:

* Research assistants that replan experiments over time
* Product/design agents that track decisions across a project lifecycle
* Autonomous QA agents that adapt testing strategies as the codebase evolves
* AI DevOps agents that monitor infrastructure, schedule interventions, and collaborate with other agents

Other applications: data extraction, travel planning, comparative analysis, supplier sourcing, e-commerce optimization, financial reporting, education tools, and market research.

<Frame>
  <img alt="The image is a diagram showing use cases for AI agent systems, including data extraction, travel planning, and comparative analysis powered by Manus AI." />
</Frame>

## Manus vs. other agent frameworks

The table below summarizes differences between Manus and typical prompt-chain frameworks (example: LangChain).

| Area          | Manus                                               | Stateless/Prompt-chain Frameworks      |
| ------------- | --------------------------------------------------- | -------------------------------------- |
| Primary focus | Persistent autonomy, world models, execution graphs | Rapid prototyping, stateless chains    |
| Memory        | Vector-backed, durable memory primitives            | Often session-scoped or ephemeral      |
| Architecture  | Execution graph + multi-agent roles                 | Linear or DAG prompt flows             |
| Observability | Built-in tracing & lifecycle APIs                   | Varies by implementation               |
| Extensibility | Tool abstraction + plugin model                     | Tools via connectors, but often ad-hoc |

For a broader introduction to prompt-chain tools, see [LangChain docs](https://learn.kodekloud.com/user/courses/langchain).

## Limitations, risks, and operational considerations

Manus is powerful but early-stage. Key concerns when adopting Manus:

* Engineering complexity: stateful services, distributed components
* Infrastructure cost: vector DBs, persistent stores, monitoring
* Security and governance: access control, data privacy, and auditing
* Safety: guardrails to prevent runaway or unsafe automation

<Callout icon="warning">
  Manus enables powerful, long-running agents, but with that power comes responsibility: design for observability, resource limits, access controls, and safe failover behavior to avoid runaway automation or data leakage.
</Callout>

## Future outlook and ecosystem

The Manus open-source ecosystem is maturing: contributions, plugins, and integrations are expanding. Roadmap directions include:

* Tighter simulation and robotics integration
* Symbolic reasoning modules and hybrid approaches
* Tooling for self-improving agents and automated fine-tuning
* Richer UI and management tooling for multi-agent orchestration

Over time, Manus may become a backend OS for multi-agent systems powering long-living AI assistants, real-time robotics, and complex automation platforms.

<Frame>
  <img alt="The image is a slide titled &#x22;Future Outlook and Ecosystem,&#x22; highlighting key points such as rapid open-source growth, potential for multi-agent systems, integrating symbolic reasoning, and a focus on general AI." />
</Frame>

## Conclusion

Manus is a foundational framework for building agents that think, persist, and coordinate over time. For teams building adaptive, stateful agents, Manus offers primitives and architectural patterns that support long-term autonomy, observability, and modular reasoning. Adopting Manus requires investment in stateful infrastructure and governance, but it unlocks capabilities beyond short-lived prompt workflows.

## Links and references

* [LangChain documentation (example)](https://learn.kodekloud.com/user/courses/langchain)
* Vector DBs and memory stores: Weaviate, Pinecone, Milvus, Faiss
* Open-source agent frameworks and research papers (search for "long-horizon agents", "world modeling", "agent operating system")

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents/module/d2a91525-d4e7-4c2a-866a-e7a9d34b538c/lesson/882a7371-4ee8-4975-b49d-6466fda0a8c1" />
</CardGroup>
