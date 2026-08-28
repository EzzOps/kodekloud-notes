# jaeger.yaml
# Jaeger Helm Values Configuration
# provisionDataStore: Controls whether to provision a data store (Cassandra/Elasticsearch)
# Setting to false means we'll use the built-in storage option
provisionDataStore:
  cassandra: false

# allInOne: Enables the all-in-one deployment mode
# This runs collector, query, and agent in a single pod - ideal for development
allInOne:
  enabled: true

# storage: Configures the storage backend for traces
# Using memory storage for simplicity - traces will be lost on pod restart
storage:
  type: memory

# agent: Jaeger agent component (disabled in all-in-one mode)
agent:
  enabled: false

# collector: Jaeger collector component (disabled in all-in-one mode)
collector:
  enabled: false

# query: Jaeger query component (disabled in all-in-one mode)
query:
  enabled: false
```

Ports and OTEL endpoints to be aware of:

* Jaeger UI (query): port 16686.
* Jaeger collector OTLP: port 4317 (gRPC) and 4318 (HTTP/protobuf). In this lab we point KAgent to the OTLP gRPC endpoint (4317).

Install Jaeger using Helm (example chart version 3.4.1 used in this lab):

```bash theme={null}
# Add the Jaeger Helm repo and install Jaeger with the above values
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update
helm install jaeger jaegertracing/jaeger \
  --namespace jaeger --create-namespace \
  -f jaeger.yaml --version 3.4.1
```

## 2. KAgent values (enable OTEL tracing)

The trimmed KAgent values file below enables a minimal set of agents and configures OTEL tracing to send data to the Jaeger collector via OTLP gRPC. The critical section is `otel.tracing.exporter.otlp.endpoint`.

```yaml theme={null}
# kagent-values.yaml
agents:
  argo-rollouts-agent:
    enabled: false
  cilium-debug-agent:
    enabled: false
  cilium-manager-agent:
    enabled: false
  cilium-policy-agent:
    enabled: false
  helm-agent:
    enabled: false
  istio-agent:
    enabled: false
  k8s-agent:
    enabled: true
  kgateway-agent:
    enabled: false
  observability-agent:
    enabled: false
  promql-agent:
    enabled: false

kmcp:
  enabled: true

kagent-tools:
  enabled: true

tools:
  grafana-mcp:
    enabled: false
  querydoc:
    enabled: false

# OpenTelemetry configuration for distributed tracing
otel:
  tracing:
    enabled: true
    exporter:
      otlp:
        # OTLP gRPC endpoint pointing to Jaeger collector service (host:port, do not include http scheme for gRPC)
        endpoint: jaeger-collector.jaeger.svc.cluster.local:4317
```

Install KAgent with Helm:

```bash theme={null}
helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent \
  --namespace kagent \
  -f /root/kagent-values.yaml
```

CRDs and ModelConfig are assumed to be pre-installed for this lab.

## 3. Patch the KAgent UI service for external (lab) access

In the lab environment we expose the KAgent UI externally by changing the service type to `NodePort` and mapping port `8080` to node port `30080`. The JSON payload contains curly braces and is provided as a code block to avoid MDX parsing issues.

```bash theme={null}
kubectl patch svc kagent-ui -n kagent -p '{
  "spec": {
    "type": "NodePort",
    "ports": [
      {
        "name": "ui",
        "port": 8080,
        "targetPort": 8080,
        "nodePort": 30080
      }
    ]
  }
}'
```

Verify pods are running in the `kagent` namespace:

```bash theme={null}
kubectl get pod -n kagent
```

Example expected output:

```plaintext theme={null}
NAME                                            READY   STATUS              RESTARTS   AGE
k8s-agent-756dcd9c66-dkqtj                      1/1     Running             0          53s
k8s-agent-7784d598cc-xtmqz                      1/1     Running             0          53s
kagent-controller-7864494766-9htkv             1/1     Running             0          53s
kagent-kmcp-controller-manager-76645f577f-9xhts 1/1    Running             0          53s
kagent-tools-56c49d7d4d-2vw4b                   1/1     Running             0          53s
kagent-ui-59d5bbd564-2bjn2                      1/1     Running             0          53s
```

If any pod is not ready, investigate with `kubectl describe` and `kubectl logs`.

## 4. Generate agent traffic and inspect traces in Jaeger

With KAgent exporting OTEL traces to Jaeger, exercise the agent (for example: list pods, query deployments, or perform model calls via the KAgent UI). These activities generate traces that appear in Jaeger.

Steps to inspect traces:

1. Open the KAgent UI and use the built-in link to the Jaeger UI (or open Jaeger at the cluster-exposed query endpoint).
2. In Jaeger:
   * Select the `kagent` service (or `KAgent` depending on naming).
   * Filter by operation (e.g., `openai.chat`) and choose an appropriate time range.
   * Open individual traces to expand spans and view tags.

When viewing a trace you can expect to see:

* Services involved and span hierarchy.
* Start timestamps and durations per span.
* Tags containing LLM prompt content and token usage (e.g., `genai.usage.prompt_tokens`).
* OTEL instrumentation metadata (e.g., `otel.library.name`, `otel.library.version`).

Example system prompt captured in a trace:

```plaintext theme={null}
You are KubeAssist, an advanced AI agent specialized in Kubernetes troubleshooting and operations. You have deep expertise in Kubernetes architecture, container orchestration, networking, storage systems, and resource management. Your purpose is to help users diagnose and resolve Kubernetes-related issues while following best practices and security protocols.

## Core Capabilities

- Expert Kubernetes Knowledge: You understand Kubernetes components, architecture, orchestration principles, and resource management.
- Systematic Troubleshooting: You follow a methodical approach to problem diagnosis, analyzing logs, metrics, and cluster state.
- Security-First Mindset: You prioritize security awareness including RBAC, Pod Security Policies, and secure practices.
- Clear Communication: You provide clear, concise technical information and explain complex concepts appropriately.
```

Example trace metadata snippet showing prompt content, timing, and OTEL library information:

```plaintext theme={null}
kagent: POST /5aac84e
Trace Start December 19 2025, 23:41:33.516  Duration 7.2s  Services 1  Depth 8  Total Spans 95

gen_ai.prompt.11.tool_call_id    call_xBdHWLcmn90kzznydtv7kdnw
gen_ai.prompt.12.content         Get deployment status in kagent namespace
gen_ai.prompt.12.role            user
gen_ai.prompt.13.content         Here is the list of all pods across all namespaces with their status:
Namespace | Pod Name | Ready | Stat

> Process: otel.library.name = opentelemetry.instrumentation.openai.v1 | otel.library.version = 0.47.3
```

Note: token usage tags (`genai.usage.prompt_tokens`, `genai.usage.completion_tokens`, etc.) are useful for cost analysis and assessing how much context is being sent to the model.

<Callout icon="warning">
  This lab uses in-memory Jaeger storage. For production systems, do not use in-memory storage — switch to a persistent backend (e.g., Cassandra, Elasticsearch) or a managed OTEL backend to retain traces and ensure availability.
</Callout>

## 5. Inspect Jaeger services and endpoints

You can validate the services created by the Helm chart to confirm the collector and query endpoints:

| Service          | Type / Ports                                                                                | Notes                                                  |
| ---------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| jaeger-agent     | ClusterIP, Ports: `5775/UDP`, `5778/TCP`, `6831/UDP`, `6832/UDP`                            | Local agent ports for legacy Thrift/UDP                |
| jaeger-collector | ClusterIP, Ports: `9411/TCP`, `14250/TCP`, `14267/TCP`, `14268/TCP`, `4317/TCP`, `4318/TCP` | OTLP gRPC `4317` and HTTP/protobuf `4318` exposed here |
| jaeger-query     | NodePort, ClusterIP `172.20.178.179`, Ports: `16686:31686/TCP`                              | Jaeger UI (query) typically on `16686`                 |

If you need details on any specific service or endpoint:

```bash theme={null}
kubectl describe svc <service> -n jaeger
```

## Wrap-up and recommendations

* This lesson demonstrated configuring Jaeger (all-in-one, in-memory) and KAgent to export OTEL traces to Jaeger.
* Use the KAgent UI and Jaeger UI to inspect agent traces, including LLM prompts and token usage for debugging and cost analysis.
* For production:
  * Replace in-memory Jaeger storage with a persistent backend (Cassandra, Elasticsearch) or a managed OTEL backend.
  * Deploy Jaeger (or OTEL collector) in a highly available configuration.
  * Secure OTLP endpoints with TLS and authentication where supported.

Next steps: run additional agents, increase load, or integrate with a persistent OTEL backend to observe trace retention and scale behavior.

## Links and references

* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* KAgent (KAgent course): [https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes)
* Jaeger Helm charts: [https://jaegertracing.github.io/helm-charts](https://jaegertracing.github.io/helm-charts)

That's it for this lesson — proceed to hands-on exercises to generate traces and explore span details in Jaeger.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/1f59e7e3-e5ab-4b77-b210-8c954216f293/lesson/177d2731-283c-46d8-92bd-d849e3498f8b" />
</CardGroup>


# Cons and Limitations of KAgent

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/Introduction/Cons-and-Limitations-of-KAgent/page

Overview of KAgent limitations, operational requirements, and technical trade-offs for hosting AI agents on Kubernetes, with guidance on suitability and deployment considerations

KAgent is a powerful, Kubernetes-native framework for hosting AI agents, but it is still early in its lifecycle. Below is a concise, structured summary of known constraints, operational trade-offs, and technical considerations to help you assess whether KAgent fits your environment and workloads.

It’s important to note that KAgent is under active development; APIs and features may change between releases. Some capabilities are experimental and might be modified or removed as the project evolves.

<Frame>
  <img alt="A slide titled &#x22;Current Limitations&#x22; that lists six numbered issues: early-stage project, learning curve, resource requirements, limited documentation, provider dependencies, and complexity for simple use cases. Below is a panel labeled &#x22;Early-Stage Project&#x22; noting active development, possible API changes, and some experimental features." />
</Frame>

## Summary of current limitations

* Early-stage project: Active development and API churn are possible.
* Learning curve: Requires Kubernetes expertise (CRDs, controllers, RBAC).
* Resource requirements: Needs a Kubernetes cluster and controller components.
* Documentation: Community-driven, with gaps or outdated examples.
* Provider dependencies: Requires LLM provider API keys and cost management.
* Complexity for simple use cases: Overhead may be high for single-agent needs.

## Learning curve

KAgent is Kubernetes-native and relies on Kubernetes primitives such as CRDs, controllers, and standard tooling patterns. Operating KAgent reliably therefore requires good familiarity with Kubernetes concepts, cluster operations, RBAC, and network policies. Understanding agent design patterns and relevant agent protocols (for example, MCP and other agent standards) will reduce friction when building and integrating agent systems.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Current Limitations&#x22; with six numbered boxes listing issues: Early-stage project, Learning curve, Resource requirements, Limited documentation, and MCP protocol familiarity." />
</Frame>

<Callout icon="lightbulb">
  Kubernetes expertise (CRDs, controllers, RBAC, networking) and familiarity with MCP will reduce operational friction. If you lack Kubernetes experience, expect a steeper ramp-up.
</Callout>

## Resource requirements and documentation

KAgent leverages Kubernetes for scheduling, scaling, and lifecycle management. If you do not already operate a cluster, expect additional operational overhead: provisioning, monitoring, backups, upgrades, and running the KAgent controller and supporting components. This adds baseline resource and maintenance costs compared to a standalone single-process agent.

Documentation is community-driven and continues to improve. You may encounter examples that need updates or limited reference material compared with more mature tooling. Plan for validation and testing when following community examples.

<Frame>
  <img alt="A presentation slide titled &#x22;Current Limitations.&#x22; It shows six numbered boxes listing issues: early-stage project, learning curve, resource requirements, limited documentation, provider dependencies, and complexity for simple use cases." />
</Frame>

## Provider dependencies

KAgent requires credentials for supported large language model (LLM) providers to make API calls. Operators must manage API keys, monitor usage, control rate limits, and implement cost controls.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Current Limitations&#x22; showing six numbered boxes (early-stage project; learning curve; resource requirements; limited documentation; provider dependencies; complex for simple use cases). Below it is a &#x22;Provider Dependencies&#x22; section noting items like requiring LLM provider API keys, API costs, and rate limiting considerations." />
</Frame>

<Callout icon="warning">
  Ensure strict secrets and cost controls. Misconfigured or leaked API keys and unmonitored usage can lead to high costs or security incidents.
</Callout>

## Complexity for simple use cases

For teams that require a single, simple agent or have limited Kubernetes experience, KAgent may introduce more operational overhead than benefit. You will need Kubernetes infrastructure, Helm releases (or similar), CI/CD automation, and observability tooling to manage production deployments. Evaluate whether KAgent’s advantages—scalability, multi-agent orchestration, and built-in observability—justify the investment for your use case.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Current Limitations&#x22; showing six numbered boxes listing issues like &#x22;Early-stage project,&#x22; &#x22;Learning curve,&#x22; &#x22;Resource requirements,&#x22; &#x22;Limited documentation,&#x22; &#x22;Provider dependencies,&#x22; and &#x22;Complex for simple use cases.&#x22; A larger panel below expands on the &#x22;Complex for Simple Use Cases&#x22; limitation." />
</Frame>

## Technical considerations

### API stability

KAgent’s APIs are evolving. Alpha or experimental APIs can be subject to breaking changes, requiring migration work for agents or integrations. While the project is stabilizing with each release, plan for release testing and version upgrade paths in your deployment strategy.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Technical Considerations&#x22; with four numbered boxes: 01 API stability, 02 Performance, 03 Security, and 04 Debugging. Below is a larger panel labeled &#x22;API Stability&#x22; showing subpoints like Alpha APIs, breaking changes possible, and migration path considerations." />
</Frame>

### Performance

KAgent uses a reconciliation-style controller loop to manage agents and their interactions. Controller orchestration adds some overhead and can introduce latency in tool invocation and inter-agent communication. External factors such as LLM API response times and network latency also affect end-to-end performance. Production deployments should include performance testing, tuning, and capacity planning.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Technical Considerations&#x22; with four numbered boxes labeled 01 API stability, 02 Performance, 03 Security, and 04 Debugging. Below is a larger &#x22;Performance&#x22; section listing items like controller reconciliation overhead, network latency for tool calls, and LLM API response times." />
</Frame>

### Security and debugging

KAgent does not replace core operator responsibilities such as secrets lifecycle management, RBAC policies, or network segmentation. You must:

* Enforce least-privilege RBAC for controllers and agents.
* Store API keys in a secure secret store (e.g., Kubernetes Secrets with an external KMS).
* Apply network policies and protocol-level restrictions for tool integrations.

For observability and debugging, distributed tracing (for example, OpenTelemetry) is recommended to trace flows across controllers, agents, and provider calls. Instrumentation and tracing for multi-component systems can be complex and will require design and tooling investment.

## When to use — and when not to use

| Use case                                                   | Recommended? | Notes                                                                      |
| ---------------------------------------------------------- | -----------: | -------------------------------------------------------------------------- |
| Kubernetes-focused organizations                           |          Yes | Best fit when teams already run and operate Kubernetes workloads.          |
| Production-grade AI agent deployments                      |          Yes | Supports multi-agent orchestration, scalability, and observability.        |
| Multi-agent systems (A2A communication)                    |          Yes | Native support for agent-to-agent interactions and standardized protocols. |
| Teams ready to adopt DevOps automation (CI/CD, Helm)       |          Yes | Requires pipelines for reproducible deployments and upgrades.              |
| Non-Kubernetes or legacy on-prem without cluster resources |           No | Lacks the infrastructure KAgent depends on.                                |
| Very simple, single-agent projects                         |           No | Operational overhead may outweigh benefits.                                |
| Teams without capacity for secrets, RBAC, or cost controls |           No | High operational risk without proper governance.                           |

<Frame>
  <img alt="A two-column slide titled &#x22;When to Use&#x22; and &#x22;When Not to Use.&#x22; The left column lists suitable scenarios (Kubernetes-focused organizations, production AI agent deployments, multi-agent systems, DevOps automation) and the right column lists unsuitable scenarios (non-Kubernetes environments, simple use cases, limited resources)." />
</Frame>

## Feature comparison: KAgent vs traditional AI frameworks

| Feature                   |                                KAgent (Kubernetes-native) | Traditional frameworks                                    |
| ------------------------- | --------------------------------------------------------: | --------------------------------------------------------- |
| Deployment model          |             Runs on Kubernetes using CRDs and controllers | Often single-process apps or managed services             |
| Agent declaration         |            YAML-first, declarative agent & tool manifests | Frequently code-first, embedded in app logic              |
| Provider integration      |    Built-in multi-provider support and pluggable adapters | Many frameworks embed provider logic in code              |
| Tooling and protocols     | Emerging agent protocols (MCP, A2A) and adapter ecosystem | Custom adapters or bespoke integration typically required |
| Observability             |      Integrates with OpenTelemetry and cluster-wide tools | Varies widely; may need custom instrumentation            |
| Scalability               |           Scales with Kubernetes capacity and autoscaling | Scaling may require app-level changes or custom ops       |
| Multi-agent communication |                           Native A2A support and patterns | Harder to implement; usually custom messaging             |
| Project status            |              Active open-source project (rapid iteration) | Varies by project; some are more mature/stable            |

kMCP and other open standards used by KAgent are key to interoperability and ecosystem growth.

## Key takeaways

<Frame>
  <img alt="A slide titled &#x22;Key Takeaways&#x22; showing a vertical numbered list of points such as &#x22;Production Ready,&#x22; &#x22;Kubernetes Native,&#x22; &#x22;Comprehensive,&#x22; &#x22;Extensible,&#x22; &#x22;Early Stage,&#x22; and &#x22;Kubernetes Required,&#x22; each with a brief explanatory note." />
</Frame>

* Production-ready and Kubernetes-native: KAgent is designed for Kubernetes environments and is suitable for production when you have cluster and devops practices in place.
* Comprehensive and extensible: It supports providers, tools, and observability integrations and embraces open standards.
* Early-stage and evolving: Active development means APIs can change—plan for migrations and version testing.
* Requires Kubernetes expertise: Deploying and operating KAgent effectively requires Kubernetes, CI/CD, secrets management, and cost governance.

## Next steps

In the following lessons we will examine KAgent components—controller, CRDs, provider integrations, and observability—in depth and show practical deployment patterns, migration strategies, and production hardening tips.

Links and references

* Kubernetes concepts and best practices: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* For community support and the latest project updates, check the KAgent project repository and its contributing guides (see the repository referenced from the project homepage).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/a2bef22f-2221-4587-9f26-3c0bce28059e/lesson/2c62f558-8b9b-4478-bd03-0a01a892af60" />
</CardGroup>
