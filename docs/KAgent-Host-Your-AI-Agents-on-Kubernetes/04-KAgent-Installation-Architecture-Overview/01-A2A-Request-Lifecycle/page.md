# A2A Request Lifecycle

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/KAgent-Installation-Architecture-Overview/A2A-Request-Lifecycle/page

Explains the agent-to-agent request lifecycle, covering discovery, authentication, sendMessage and sendMessageStream for secure interoperable multi-agent communication and streaming task updates.

This document describes the end-to-end agent-to-agent (A2A) request lifecycle. The A2A flow has four principal stages:

* Agent discovery
* Authentication
* sendMessage (request)
* sendMessageStream (streaming updates)

Below is a concise reference table followed by detailed explanations and examples.

| Stage             | Purpose                                                               | Typical endpoint / artifact                                        |
| ----------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Agent discovery   | Locate an agent and retrieve its capabilities and endpoints           | `GET /.well-known/agent-card` (or registry/direct configuration)   |
| Authentication    | Obtain a token (e.g., OpenID Connect) for the agent's security schema | Authorization server `token` endpoint → JWT                        |
| sendMessage       | Submit a request to an agent (synchronous or async task creation)     | `POST /sendMessage` with JWT                                       |
| sendMessageStream | Receive streaming task lifecycle events and artifacts                 | `POST /sendMessageStream` with JWT (server-sent events or similar) |

## Agent discovery

Discovery is the first step: the client finds an agent card that describes the agent’s capabilities, endpoints, and security schema. Discovery can happen in one of three ways:

* Well-known URI: the client requests a predictable path on the agent or controller.
* Curated registry: a central catalog contains agent cards.
* Direct configuration: a client is given an agent card or endpoint manually.

Example (well-known URI):

```text theme={null}
Client -> GET /.well-known/agent-card
Server -> Returns Agent Card (JSON describing capabilities, endpoints, security)
```

The returned agent card typically includes:

* The agent's name and description
* Endpoints (e.g., `sendMessage`, `sendMessageStream`)
* Supported authentication schemes (e.g., OpenID Connect)
* Declared skills and tool metadata

## Authentication

After parsing the agent card, the client inspects the security schema. If the agent uses OpenID Connect (or another OAuth2 flow), the client obtains an access token from the authorization server and presents that token to the agent.

Typical flow:

1. Discover token endpoint from the agent card or identity provider metadata.
2. Authenticate (client credentials / authorization code / other grant).
3. Receive a JWT access token.
4. Use the JWT in `Authorization: Bearer <token>` when calling the agent.

> **warning** Store and transmit JWTs securely. Always use TLS, implement short token lifetimes, validate audience/issuer claims, and follow least-privilege practices.

## sendMessage (request)

With a valid JWT, the client calls the agent’s `sendMessage` endpoint to submit work. The agent processes the incoming message, creates a task, and returns a task response. The exact response depends on the agent implementation — it may return a synchronous result, a task identifier, or a simple acknowledgement indicating the task was queued.

Simple sequence:

```text theme={null}
Client -> POST /sendMessage (Authorization: Bearer <JWT>, body: message)
Agent  -> Returns TaskResponse (e.g., { taskId, status, result? })
```

Key considerations:

* The message payload should match the agent's expected schema (declared in the agent card).
* Responses vary: some agents do full synchronous processing and return results inline; others return a task ID for later polling or streaming.

## sendMessageStream (streaming updates)

When you need real-time updates (task submitted, progress, artifacts, completion), use `sendMessageStream`. The client opens a streaming connection (SSE, WebSocket, or chunked HTTP) and the agent pushes lifecycle events:

* Task submission confirmation
* Task status updates (e.g., "working", "succeeded", "failed")
* Artifact update events (e.g., logs, files, intermediate outputs)
* Final completion event

Example stream sequence:

```text theme={null}
Agent Discovery
Authentication
sendMessage API
sendMessageStream API

Client -> POST /sendMessageStream (with JWT)
Server -> Stream: Task (Submitted)
Server -> Stream: TaskStatusUpdateEvent
Server -> Stream: TaskArtifactUpdateEvent
Server -> Stream: TaskStatusUpdateEvent (Done)
```

Use streaming when you want low-latency progress updates or to receive artifacts as they are produced.

## Real-world examples

## Enterprise agent network

A2A enables agents across departments and organizations to discover and interoperate using the same protocol. Agents advertise their capabilities and endpoints so other agents can call them directly, enabling cross-company collaboration and standardized integrations.

<Frame>
  <img alt="A diagram titled &#x22;Enterprise Agent Networks&#x22; showing two companies (Company A and Company B), each with Department A and Department B boxes containing agent icons labeled Agent A and Agent B. The two company blocks are connected at the bottom by an &#x22;A2A Protocol&#x22; link." />
</Frame>

## Agent composition

Agent composition is the pattern where one agent treats another agent as a tool. Building systems from small, focused agents (each exposing specific skills) makes complex workflows easier to maintain and scale.

<Frame>
  <img alt="A slide titled &#x22;Agent Composition (Interpretation)&#x22; showing two identical cartoon agents on the left and right with horizontal arrows between them indicating bidirectional communication." />
</Frame>

## Distributed systems

Agents may be deployed in different regions or clouds. A2A supports distributed deployment, enabling agents to collaborate over the network and form a resilient, geo-distributed agent infrastructure.

<Frame>
  <img alt="A world map titled &#x22;Distribution Systems (Interpretation)&#x22; with two cartoon agent icons at left and right and location pins in North America and India connected by dotted lines. It illustrates networked distribution between the two agents." />
</Frame>

## Key takeaways: what A2A enables — and what it does not

What A2A provides:

* Cross-company agent collaboration
* Multi-agent coordination and composition
* Secure, standardized communication at the protocol level
* Reduced need for custom integrations when parties follow the same A2A conventions

What A2A is not:

* An agent-building framework (it does not replace frameworks like LangChain)
* A full messaging/control plane (MCP) on its own
* Model-specific (A2A is independent of the underlying model)
* Limited to trivial tools — it supports complex agent-to-agent coordination

| A2A Enables                       | A2A Is Not                  |
| --------------------------------- | --------------------------- |
| Cross-company agent collaboration | An agent-building framework |
| Multi-agent coordination          | A replacement for an MCP    |
| Standardized, secure protocol     | Model-dependent             |
| Reduced integration burden        | Limited to simple tools     |

<Frame>
  <img alt="A split slide titled &#x22;What A2A Enables&#x22; (left) lists cross-company agent collaboration, multi-agent coordination, secure standard communication, and no custom integrations. The right column, &#x22;What A2A Is Not,&#x22; states it's not an agent-building framework, not an MCP replacement, not model-dependent, and not for simple tools." />
</Frame>

## How A2A fits with KAgent

When A2A is enabled in KAgent, KAgent exposes a discoverable endpoint so other agents can find and communicate with it. The well-known URI for a KAgent-managed agent typically follows this pattern:

```text theme={null}
URL Format - kagent-controller:8083/api/a2a/namespace/agent-name
```

> **lightbulb** KAgent exposes each agent's A2A endpoint under the controller's API. Replace `namespace` and `agent-name` with the actual Kubernetes namespace and agent name.

KAgent supports agent-as-tools (composition) and multi-agent workflows. A caller agent can invoke a callee agent for a specific skill and treat the callee as a managed tool within a larger workflow.

<Frame>
  <img alt="A diagram titled &#x22;How Kagent Uses A2A&#x22; showing two cartoon agent robots labeled Agent A and Agent B linked by an &#x22;A2A Protocol&#x22; box. Above them are three labeled blocks: &#x22;Agent A2A Server,&#x22; &#x22;Agent as tool,&#x22; and &#x22;Multi-agent workflow.&#x22;" />
</Frame>

## Example: agent composition in KAgent

The example below shows a flight agent that exposes a `book_flight` skill and a travel-planner agent that calls the flight agent via A2A.

```yaml theme={null}
