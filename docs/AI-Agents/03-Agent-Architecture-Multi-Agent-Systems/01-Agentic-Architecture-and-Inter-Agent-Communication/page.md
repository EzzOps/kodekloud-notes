# Agentic Architecture and Inter Agent Communication

Source: https://notes.kodekloud.com/docs/AI-Agents/Agent-Architecture-Multi-Agent-Systems/Agentic-Architecture-and-Inter-Agent-Communication/page

Designing modular agent architectures, inter-agent communication patterns, and deploying scalable multi-agent systems with FastAPI, messaging, memory, and observability

In this lesson we examine agentic architecture and inter-agent communication—core concepts for building flexible, maintainable, and scalable multi-agent systems. We cover agent system layers, modular components, decoupled design benefits, common communication protocols and patterns, practical multi-agent workflows, and how to expose agents with FastAPI for production deployments.

Choosing the right architecture determines how well agents support long-horizon reasoning, persistent memory, tool orchestration, and autonomous operation. Decoupled designs enable independent upgrades, easier debugging, team-based development, and robust scaling. Clear inter-agent protocols let agents delegate, collaborate, and compose complex behaviors across services and runtime environments.

Agentic architecture refers to system designs that let AI agents operate as autonomous, extensible components. Typical subsystems include perception, planning, memory, action, and feedback mechanisms. These subsystems are integrated through modular services to form continuous reasoning loops.

<Frame>
  <img alt="The image illustrates a diagram of agentic architecture, showing a cyclical process involving perception, planning, memory, action, and feedback. Each phase is represented by an icon and connected in a loop." />
</Frame>

## Four core layers of agentic systems

Four key layers commonly found in Agentic AI systems are described below. Each layer is responsible for discrete concerns, which simplifies testing and targeted scaling.

| Layer               | Purpose                                                                               | Examples / Tools                                           |
| ------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Perception Layer    | Converts raw signals into structured observations from text, speech, or vision inputs | NLP pipelines, speech-to-text, OpenCV, ingestion pipelines |
| Cognitive Layer     | Runs models and decision-making frameworks to reason, plan, and generate intents      | LLMs, rule engines, planners, chain-of-thought modules     |
| Action Layer        | Executes effects: tool calls, API interactions, actuators, and feedback integration   | API clients, webhooks, SDKs, robotics controllers          |
| Communication Layer | Manages interactions across agents, services, and humans via well-defined protocols   | REST, WebSockets, pub/sub systems, vector stores           |

These layers let agents perceive, reason, act, and communicate in dynamic environments while keeping responsibilities separated.

## Modular components of an agent runtime

A practical agent system is composed of modular components with clear responsibilities:

* Controller / Planner: decomposes high-level goals into actionable tasks and routes work to agents or tools.
* Tool Executor: manages external API integrations, sandboxed function calls, and runtime tools.
* Memory System: stores and retrieves context and long-term state; often uses vector stores for embeddings and semantic search.
* Interface Layer: exposes agent capabilities to users or other systems via APIs, WebSockets, or SDKs.
* Agent Runtime Orchestrator: coordinates planning, tool invocations, retries, and response synthesis.

Separation of concerns like this improves testability, reuse, and independent scaling. For example, you can upgrade the planner model without modifying memory access or the interface layer.

<Frame>
  <img alt="The image is an infographic titled &#x22;Why Decoupling Matters,&#x22; illustrating four benefits: supporting multi-agent orchestration, aligning with microservice design patterns, easier maintenance and debugging, and enabling independent upgrades of agent parts. Each benefit is visually represented with icons connected by colorful lines." />
</Frame>

## Inter-agent communication methods

Inter-agent communication enables delegation, knowledge sharing, and collaboration. Choose mechanisms based on latency, reliability, and coupling goals:

| Mechanism                | Characteristics                                                   | Use cases                                                 |
| ------------------------ | ----------------------------------------------------------------- | --------------------------------------------------------- |
| REST APIs                | Synchronous HTTP calls; simple, direct                            | Point-to-point requests, short-lived calls                |
| Message queues / Pub‑Sub | Asynchronous, durable, decoupled (Redis Streams, RabbitMQ, Kafka) | Task orchestration, retries, fan-out, resilient workflows |
| Shared stores            | Shared database or vector store for collaborative state           | Shared context, caching, persistent memory across agents  |

<Frame>
  <img alt="The image illustrates three inter-agent communication methods: REST APIs, Message Queues, and Shared Memory. Each method is briefly explained with icons representing their functionality." />
</Frame>

### Communication patterns

Common patterns for composing agent interactions:

* Request–Response: Agent A asks Agent B to perform work and waits for a result.
* Publish–Subscribe: Agents publish events or tasks; multiple subscribers react or process work.
* Supervisor–Worker: A coordinating agent delegates tasks to worker agents and aggregates results.

These patterns support collaboration, specialization, fault tolerance, and scalable execution.

> **lightbulb** Choose communication patterns based on latency, reliability, and coupling requirements. Use REST for simple synchronous calls, message queues for decoupled and resilient workflows, and shared stores for collaborative memory and caching.

## Conversable and collaborative agent capabilities

Key capabilities that enable agents to work together and interact with users:

* Agent customization: personalize agents with domain-specific tools, personas, plugins, or scripts.
* Multi-agent conversations: agents exchange messages for joint reasoning, handoffs, or validation.
* Flexible conversation patterns: support joint chat (a shared channel where all agents contribute) and hierarchical chat (a lead agent delegates to sub-agents).

<Frame>
  <img alt="The image illustrates three agent communication models: &#x22;Request-response,&#x22; &#x22;Supervisor-worker,&#x22; and &#x22;Publish-subscribe,&#x22; each depicted with labeled triangles." />
</Frame>

<Frame>
  <img alt="The image illustrates two models of agent communication: multi-agent customization and flexible conversation patterns, which include joint chat and hierarchical chat." />
</Frame>

## Practical multi-agent workflows

Common real-world workflows for multi-agent systems:

* Role-based teams: specialized agents (researcher, writer, fact-checker) collaborate to complete complex tasks.
* Escalation flows: when an agent cannot proceed, it calls a helper or supervisor agent.
* Negotiation: agents propose and score options, exchanging proposals until consensus.
* Pipeline chaining: one agent handles preprocessing and passes results to downstream agents (summarizer → verifier → publisher).

Agent collaboration models human team dynamics but requires well-defined messaging protocols, observability, and fault handling.

## FastAPI for exposing agent capabilities

[FastAPI](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi) is a modern, high-performance Python framework ideal for exposing agent capabilities. Reasons to use FastAPI:

* Asynchronous endpoints to integrate with async LLM calls and background tasks.
* Automatic OpenAPI / Swagger documentation generation.
* Strong input validation with [Pydantic](https://docs.pydantic.dev/).
* Easy dependency injection for authentication, policy checks, and observability.

A typical access-control workflow in a containerized environment follows these steps:

1. Client (user, web app, or another agent) sends a request to the FastAPI service.
2. FastAPI validates the request body with Pydantic models.
3. The application queries an external policy engine (HTTP or SDK) with inputs such as principal, action, and resource.
4. The policy engine returns allow/deny decisions; the application enforces the decision.
5. The decision and relevant metadata are logged for auditing.

This flow commonly runs inside a Docker container to ensure consistent runtime and dependency management.

<Frame>
  <img alt="The image is a diagram providing an overview of the FastAPI framework, showing its interaction with requests, policies, and logging within a Docker container environment. It illustrates the flow from making a request to evaluating policies and generating logs." />
</Frame>

### Example FastAPI endpoint (agent interface)

Below is a minimal FastAPI example demonstrating a Pydantic request model, async handler, and a placeholder policy check. Use this pattern to validate inputs and gate agent execution behind policy decisions.

```python theme={null}
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class AgentRequest(BaseModel):
    user_id: str
    prompt: str
    metadata: Dict[str, str] = {}

async def check_policy(user_id: str, action: str) -> bool:
    # Replace with a real policy engine call or SDK
    # e.g., policy_client.evaluate({"principal": user_id, "action": action})
    return True

@app.post("/agent/run")
async def run_agent(req: AgentRequest):
    allowed = await check_policy(req.user_id, "run_agent")
    if not allowed:
        raise HTTPException(status_code=403, detail="policy denied")
    # Invoke planner, memory lookup, and tool executor here (async)
    result = {"status": "ok", "output": "agent result goes here"}
    return result
```

<Frame>
  <img alt="The image illustrates how FastAPI works, showing a flow from a client request to a FastAPI endpoint, through agent core logic, and ending with a JSON response." />
</Frame>

### How FastAPI fits into agent architectures

Typical integration points and deployment patterns:

* Client sends requests: frontends or other agents call REST endpoints.
* FastAPI endpoints receive validated payloads via Pydantic schemas.
* Agent logic executes: planners, memory lookups, tool executors, and LLM calls run—often asynchronously or via background tasks.
* Response returned: structured JSON responses; auto-generated docs help developer onboarding.

FastAPI integrates well with microservice patterns—each agent role (planner, memory store, tool executor) can be containerized and scaled independently.

## Deployment and scaling strategies

Common deployment and scaling approaches for agent systems:

* Horizontal scaling: multiple worker instances behind a load balancer for stateless agents.
* Service separation: isolate planner, memory, and tool executors into separate services for targeted scaling.
* Async task queues: use Celery, RQ, or cloud-native job queues for long-running or retryable tasks.
* Observability: structured logging, distributed tracing, and metrics for debugging and performance tuning.
* Security and policy enforcement: centralize access control policies, use mTLS, API gateways, and rate limiting.

These patterns help create production-grade, maintainable, and observable agent deployments.

> **warning** Security and observability are critical. Enforce least-privilege access, validate inputs thoroughly, log decisions for audits, and instrument distributed traces to troubleshoot inter-agent workflows.

## Quick reference: communication selection guide

| Goal                          | Recommended approach                                     |
| ----------------------------- | -------------------------------------------------------- |
| Low-latency sync call         | REST / gRPC                                              |
| Decoupled, resilient pipeline | Message queue / Pub‑Sub (Kafka, RabbitMQ, Redis Streams) |
| Shared context or memory      | Shared database / vector store                           |
| Fan-out to many workers       | Pub‑Sub with consumer groups                             |

## Links and references

* [FastAPI docs and tutorials](https://learn.kodekloud.com/user/courses/python-api-development-with-fastapi)
* [Pydantic documentation](https://docs.pydantic.dev/)
* [Redis Streams](https://redis.io/docs/latest/streams/)
* [RabbitMQ](https://www.rabbitmq.com/)
* [Kafka event streaming course](https://learn.kodekloud.com/user/courses/event-streaming-with-kafka)
* [Kubernetes basics](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial)
* [Docker primer](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner)

Together, these architectural principles, communication patterns, and deployment practices enable scalable, adaptable multi-agent systems able to solve complex, multi-step tasks in production environments.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-agents/module/2e110716-1967-4e6f-a995-9138c54fb38c/lesson/1c72afc9-6b60-48e5-9dbd-3a3418b013c8)
