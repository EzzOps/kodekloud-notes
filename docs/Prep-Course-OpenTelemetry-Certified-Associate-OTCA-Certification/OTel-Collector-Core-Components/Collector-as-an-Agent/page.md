# Collector as an Agent

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OTel-Collector-Core-Components/Collector-as-an-Agent/page

Explains running the OpenTelemetry Collector as a local agent on hosts, nodes, or sidecars to capture, enrich, and forward telemetry with low latency.

In this lesson, we’ll explore how the OpenTelemetry (OTel) Collector can operate as an agent running close to your workloads—on hosts, VMs, Kubernetes nodes, or inside containers. Running the Collector as an agent gives you low-latency telemetry capture and the ability to enrich data with local resource context (for example, host or pod identifiers) at collection time.

An "agent" is a lightweight process colocated with the application (for example, inside the same VM). By capturing telemetry locally, agents reduce network hops and enable accurate resource enrichment, improving trace/metric attribution and overall reliability.

Key benefits of the agent pattern:

* Low-latency capture of spans, metrics, and logs.
* Accurate enrichment with local metadata (host, pod, container).
* Resilience to transient network failures between workload and upstream collectors.
* Fine-grained local processing (filtering, batching, sampling) before forwarding.

<Frame>
  <img alt="The image depicts a diagram of a &#x22;Collector as an Agent in a VM,&#x22; showing how an app/service in a virtual machine collects spans, traces, logs, and performs resource enrichment using a collector agent. It emphasizes local collection and low latency within the app scope." />
</Frame>

Typical layered deployment when using agents

* Local Collector (per-VM or per-node): collects telemetry, enriches it with local host/pod metadata, and performs lightweight processing (batching, local sampling).
* Team-level Collectors: aggregate telemetry from local collectors and apply team-specific rules such as additional filtering, sampling adjustments, or initial redaction.
* Central multi-tenant Collector: performs global concerns such as TLS termination, cross-team routing, PII redaction, and final aggregation before forwarding to observability backends.

This layered architecture balances low-latency capture at the edge with centralized control for security, routing, and tenant-aware processing.

Deployment patterns summary

| Deployment Type        |                                                       Use Case | Example                                                |
| ---------------------- | -------------------------------------------------------------: | ------------------------------------------------------ |
| Local/VM agent         |             Per-host telemetry capture and resource enrichment | Run a Collector as a systemd service on each VM        |
| Node agent (DaemonSet) |           Capture telemetry from all pods on a Kubernetes node | `kubectl apply -f collector-daemonset.yaml`            |
| Sidecar                | Per-pod isolation and localhost transport (lowest network hop) | Application -> `localhost:4317` (OTLP gRPC) to sidecar |

In Kubernetes, the common agent pattern is to run a node-local Collector via a DaemonSet. The node-local Collector receives telemetry from all pods on the node, gathers node metrics, performs initial processing, and forwards telemetry upstream to team-level or central collectors (which can apply PII redaction and routing).

<Frame>
  <img alt="The image illustrates the flow of workload telemetry and node metrics from app pods in a Kubernetes cluster to a central collector for PII redaction and routing, using a collector as an agent in a Kubernetes node (Daemonset)." />
</Frame>

Sidecar pattern

* The sidecar Collector runs in the same Pod as the application and receives telemetry over localhost. This eliminates cross-pod network hops and improves isolation per application instance.
* Default OTLP gRPC port: `4317`. Configure your SDKs/agents to export to `localhost:4317` when using a sidecar.

<Callout icon="lightbulb">
  Agent deployment variants—choose based on operational constraints and goals:

  * VM agent: per-host Collector for direct host metadata enrichment.
  * Node agent (DaemonSet): scales across Kubernetes nodes to collect all pod telemetry per node.
  * Sidecar: per-pod Collector for strict isolation and localhost transport (`localhost:4317`).
</Callout>

Best practices

* Enrich telemetry at the nearest point possible (agent) to preserve accurate context.
* Use local batching and retry policies in agents to smooth transient network issues.
* Place sensitive redaction and tenant-routing logic in centralized collectors to enforce consistent policies.
* Monitor agent resource usage to ensure lightweight operation on hosts and nodes.

Summary
An agent Collector runs close to the workload (VM host, Kubernetes node, or Pod) to capture and enrich telemetry with low latency. Agents forward to team-level collectors for local enforcement of policies and then to a central collector for tenant-aware processing and final delivery to observability backends.

Links and references

* [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
* [OpenTelemetry Specification](https://opentelemetry.io/docs/reference/specs/)
* [Kubernetes: DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/f6507634-836f-4fe9-b29d-047d84bfcce7/lesson/7c1b7ae6-44ec-4b00-92be-95e3fc3c7015" />
</CardGroup>
