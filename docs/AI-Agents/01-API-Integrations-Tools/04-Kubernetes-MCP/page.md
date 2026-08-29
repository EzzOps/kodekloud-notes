# Kubernetes MCP

Source: https://notes.kodekloud.com/docs/AI-Agents/API-Integrations-Tools/Kubernetes-MCP/page

Explains Kubernetes Multi-Cluster Proxy (MCP) for securely connecting and routing services across distributed, multi-cluster AI agent infrastructures, covering architecture, deployment, security, and best practices.

Welcome back.

In this lesson we'll cover Kubernetes MCP (Multi-Cluster Proxy) and how it helps connect distributed AI agent infrastructure across clusters, regions, and air-gapped environments.

Topics covered:

* What Kubernetes MCP is and why it matters for AI agent infrastructure
* Core architecture: servers, clients, proxies, and tunnels
* MCP server and client interaction
* How MCP enables distributed AI agents and secures AI workflows across clusters
* Use cases and an MCP vs. traditional load balancer comparison
* Deploying MCP with Helm and Kubernetes
* Best practices for AI agent scaling with MCP
* Limitations and monitoring considerations

As agent-based systems grow in scale and complexity, they often need to operate across multiple clusters, regions, or isolated networks. Kubernetes MCP — Multi-Cluster Proxy — provides secure, tunneled connectivity between clusters, enabling cross-cluster routing and real-time interactions without exposing internal services to the public internet. For teams building large-scale or enterprise AI systems, understanding MCP is essential for secure, scalable, and cost-effective deployments.

<Frame>
  <img alt="The image is an introductory slide about &#x22;Kubernetes MCP&#x22; (Multi-Cluster Proxy), an open-source tool for connecting isolated Kubernetes environments." />
</Frame>

Problem statement: in traditional Kubernetes architectures, clusters are isolated by default. Exposing services across regions or to other clusters typically requires complicated network changes, VPNs, or public endpoints. MCP addresses these challenges by creating persistent, secure tunnels from MCP clients (deployed alongside your services) back to a central MCP server. This avoids redesigning cluster networking and reduces the need to expose internal services publicly — a pattern that fits hybrid cloud, multi-region, and air-gapped use cases.

<Frame>
  <img alt="The image is a slide titled &#x22;Kubernetes MCP – Introduction,&#x22; noting its relevance for enterprises managing certain tasks. It includes a Copyright notice for KodeKloud." />
</Frame>

By acting as a central routing layer, MCP enables services in one cluster to securely access services in another — databases, internal APIs, or LLM inference endpoints — without changing cluster networking. In AI agent ecosystems, components (memory stores, inference services, orchestrators) are often distributed for cost, latency, or compliance reasons. MCP lets these components interoperate across cluster boundaries while preserving security and minimizing operational changes.

<Frame>
  <img alt="The image explains the importance of MCP for AI agent infrastructure, showing how agents from different clusters communicate via MCP without network redesign or public exposure. It includes clusters A, B, and C, each containing an agent connected through MCP." />
</Frame>

This architecture makes it easy to colocate GPU-accelerated inference in one cluster, run orchestration or planning agents in another, and host sensitive data in a locked-down region — all while maintaining low-latency, secure access between them.

<Frame>
  <img alt="The image highlights the importance of MCP for AI agent infrastructure, detailing its roles in managing GPU-based inference and orchestration and control clusters." />
</Frame>

Core architecture overview

| Component            | Role                                                                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| MCP server           | Central routing hub (typically in a hub/central cluster). Maintains registry of available services and active client tunnels.              |
| MCP client (agent)   | Runs in satellite/remote clusters. Opens and maintains a persistent secure tunnel to the MCP server and registers local services to proxy. |
| Service registration | Mechanism for clients to announce which local services (internal APIs, vector DBs, LLM endpoints) are reachable via the tunnel.            |
| Tunnel transport     | Persistent WebSocket connections (wss\://) or similar secure channels used to route traffic bidirectionally.                               |

When a client or external host needs access to a registered service, the MCP server routes the request down the correct tunnel to the target client; responses are returned the same way. This enables cross-cluster communication without exposing internal IPs or creating a full mesh.

<Frame>
  <img alt="The image is a diagram titled &#x22;Core Architecture,&#x22; showing an MCP Server connected via web socket tunnels to MCP Clients, which in turn connect to Internal APIs, Vector Databases, and LLM Endpoints." />
</Frame>

Common deployment pattern

A typical pattern is a client–server model:

* Host application (IDE, agent runtime, or developer tool) runs an MCP client and talks to one or more MCP servers.
* Each MCP server connects to local data sources and may also proxy requests to remote web APIs.
* Hosts pull context or data from multiple clusters in real time, supporting decentralized data integration and task coordination.

<Frame>
  <img alt="The image shows a diagram of a core architecture featuring MCP (Message Control Protocol) servers connecting to local data sources and a remote service via web APIs. It represents the interactions between components on a computer and the internet." />
</Frame>

MCP interactions (high-level flow)

When a client starts:

1. Opens a secure WebSocket tunnel to the MCP server (commonly `wss://`).
2. Authenticates (mTLS, tokens, or platform-specific mechanisms).
3. Registers the services it can proxy.
4. Listens for proxied requests forwarded by the server and routes them to local services.

Requests from other clients or from the server travel via the MCP server and the selected client tunnel to the destination service; responses flow back through the same path. This design provides secure, bidirectional routing across clusters.

<Frame>
  <img alt="The image illustrates the interaction between MCP Clients and an MCP Server via a web socket tunnel, showing how clients register local services and request services." />
</Frame>

Why MCP matters for AI agent systems

Modern AI agent ecosystems are distributed by design:

* Inference often runs on GPU-optimized clusters.
* Memory/knowledge stores may be placed in specific regions for compliance.
* Planners or orchestrators can run in secure zones.

MCP maintains separation of concerns while providing low-latency, secure access between these components. Instead of implementing complex network policies across clusters, MCP handles discovery and routing at the application layer.

Security considerations

* Encrypt all tunnels (wss/TLS).
* Use authentication: mutual TLS (mTLS) or token-based authentication to authorize clients.
* Apply IP allow-listing and RBAC at the MCP server to restrict reachability of registered services.
* Never expose sensitive services directly to the public internet; prefer tunneled access through MCP.

<Callout icon="lightbulb">
  For regulated environments (healthcare, finance, defense), pair MCP with strict certificate lifecycle management, centralized audit logging, and least-privilege service definitions to meet compliance and audit requirements.
</Callout>

Real-world use cases

* Research agents in one region accessing production-only services in a separate region without making those services public.
* Dedicated GPU clusters exposing LLM inference endpoints locally while orchestration agents run in other clusters.
* Edge devices (robots, appliances) creating secure tunnels back to a centralized planner in a hub cluster.

MCP vs. traditional load balancers

| Aspect     | Load Balancer                                   | Kubernetes MCP                                                                 |
| ---------- | ----------------------------------------------- | ------------------------------------------------------------------------------ |
| Scope      | Distributes traffic within a region/VPC/cluster | Cross-cluster service discovery and secure routing                             |
| Use case   | Horizontal scaling, HA within same network      | Tunneling and connecting isolated clusters/air-gapped environments             |
| Exposure   | Often requires public endpoints or VPNs         | Preserves internal-only services via secure tunnels                            |
| Complexity | Well-supported for HTTP/TCP balancing           | Adds tunneling layer and service registry; better for autonomy across clusters |

Use a load balancer for intra-cluster or single-cloud scaling. Use MCP when you need cross-cluster autonomy, secure multi-cluster orchestration, or to connect air-gapped/satellite clusters.

Deploying MCP with Helm (high-level steps)

1. Deploy MCP server into a central/hub cluster.
2. Deploy MCP clients into satellite clusters and configure them to connect to the server.
3. Define which services to expose using Kubernetes-native objects (Service, ConfigMap, or CRDs if provided by the MCP implementation).
4. Verify tunnels and the service registry, then test end-to-end routing.

Example Helm commands (replace placeholders with your values):

```bash theme={null}
