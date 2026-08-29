# Cilium Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cilium-Overview/Cilium-Overview/page

Overview of Cilium, an eBPF-powered Kubernetes platform providing CNI networking, identity-based security, L7 policies, load balancing, observability via Hubble, and service mesh integrations

In this lesson we introduce Cilium: what it is, the capabilities it provides, and how it integrates into a Kubernetes environment.

Cilium is an open-source, cloud-native networking, security, and observability platform for Kubernetes. Although commonly used as a CNI plugin, Cilium extends far beyond basic pod connectivity—leveraging eBPF to deliver high-performance packet processing, identity-based security, L7-aware policies, and rich traffic visibility.

<Frame>
  <img alt="A slide titled &#x22;Cilium – Introduction&#x22; showing a multicolored hexagonal logo linked by lines to three labeled items: Network Connectivity, Security, and Observability, each with a circular icon. The design uses colored rings and a clean white background." />
</Frame>

Overview: we’ll first cover Cilium’s networking features, then security capabilities, followed by observability (Hubble), how Cilium overlaps with service-mesh functionality, and finally the eBPF foundation that powers it.

## At-a-glance feature matrix

| Feature category       | Primary capabilities                                                         | Examples / integrations                                            |
| ---------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Networking             | Pod networking, L4/L7 load balancing, ingress/gateway, egress, multi-cluster | CNI plugin, Envoy for L7, Cluster Mesh, Gateway API                |
| Security               | L3/L4 NetworkPolicy, L7-aware CiliumNetworkPolicy (CNP), encryption          | IPsec/WireGuard, mTLS, protocol-aware L7 rules (HTTP, Kafka, gRPC) |
| Observability          | Flow visibility, metrics, tracing, troubleshooting                           | Hubble, Prometheus metrics, Grafana dashboards                     |
| Platform & performance | Kernel-accelerated datapath, kube-proxy replacement, QoS                     | eBPF-based datapath, service handling without kube-proxy           |

## Networking features

Cilium can be installed as the cluster CNI to provide pod-to-pod networking. Beyond basic connectivity, Cilium implements additional networking components:

* CNI plugin: manages pod interfaces, routes, and connectivity.
* Load balancing: L4 load balancing plus L7 routing when integrated with an L7 proxy such as Envoy.
* Cluster Mesh: connect multiple Kubernetes clusters and expose global services with cross-cluster load balancing.
* Ingress Controller & API Gateway: Cilium can act as an ingress/gateway implementation (including Gateway API support and Envoy-based datapath), reducing the need for a separate ingress controller.
* Egress gateway: define and control how traffic leaves the cluster (specific node/IPs, NATing rules, egress policies).

<Frame>
  <img alt="A Kubernetes networking diagram showing two clusters with nodes and pods and the underlying CNI layer. The top row highlights networking components like CNI plugin, load balancer, multi-cluster/mesh, ingress controller, and egress gateway." />
</Frame>

Egress gateways let operators guarantee that external traffic exits via a known IP address or node, which is useful for policy, auditing, and upstream firewall rules—unlike default Kubernetes egress behavior.

## Security features

Cilium provides layered security that ranges from IP/port filtering to protocol-aware, application-layer rules:

* Kubernetes NetworkPolicy: L3/L4 enforcement (IP and port-based rules).
* CiliumNetworkPolicy (CNP): a richer CRD that supports L7 policies (HTTP, Kafka, gRPC, etc.) and identity-based rules (service account / labels).
* Encryption: optional pod-to-pod encryption using IPsec or WireGuard tunnels managed by Cilium.
* Identity-based policies: policies based on workload identity rather than ephemeral IP addresses, improving policy resilience and security posture.

<Frame>
  <img alt="A Kubernetes cluster diagram showing Node 1 with Frontend (172.16.0.3) and Backend (172.16.0.4) pods exchanging an HTTP GET /products request, and Node 2 hosting a Database (172.16.0.5). The left side contrasts standard NetworkPolicy (L3/L4) with CiliumNetworkPolicy that adds L7 (HTTP) rules." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Security&#x22; listing NetworkPolicy (L3/L4), CiliumNetworkPolicy + L7, and Encryption. To the right is a Kubernetes cluster diagram showing Frontend (172.16.0.3) and Backend (172.16.0.4) pods on Node 1 and a Database (172.16.0.5) on Node 2 with a dashed connection from the backend to the database." />
</Frame>

Example L7 policy use case: allow only HTTP GET /products from frontend to backend; any POST or non-GET requests are dropped by the L7-aware policy.

> **lightbulb** CiliumNetworkPolicy enables protocol-aware L7 filtering (HTTP, Kafka, gRPC, etc.), allowing precise enforcement based on application semantics rather than just IPs and ports.

Note: runtime security (for example, Tetragon) provides syscall and process-level visibility but is outside the scope of this lesson.

## Observability: Hubble, metrics, and troubleshooting

Cilium’s observability is centered on Hubble, which provides real-time flow visibility and troubleshooting telemetry.

* Hubble: flow-level insights—who communicates with whom, which protocols and endpoints are used, events and errors, and allowed vs dropped flows.
* CLI and GUI: Hubble offers both a CLI and a web UI for interactive exploration and service-dependency graphs.
* Metrics: Cilium exports metrics that Prometheus can scrape; Grafana dashboards visualize these metrics for operational insight.

<Frame>
  <img alt="A slide titled &#x22;Observability&#x22; showing a Kubernetes cluster with two nodes, each running a pod and bidirectional arrows representing network traffic between them. A satellite-like Hubble icon and a developer are shown, with the caption stating Hubble enables real-time traffic flow inspection across the cluster." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Observability&#x22; showing a Kubernetes cluster with two nodes and pods and a Cilium component in the center. Prometheus and Grafana are shown above, with arrows indicating Prometheus collecting metrics from Cilium and Grafana visualizing them." />
</Frame>

Hubble supports common operational questions and troubleshooting workflows:

* Which services are communicating and what HTTP calls are happening?
* Which Kafka topics are used by which services?
* Where are flows being dropped and why?
* Failure diagnosis: DNS resolution issues, interrupted TCP connections, unanswered TCP SYNs, HTTP 4xx/5xx spikes, and latency percentiles.

<Frame>
  <img alt="A presentation slide titled &#x22;Failures and Troubleshooting&#x22; with a wrench-and-screwdriver icon on the left and a list of troubleshooting questions on the right (e.g., Is any network communication failing? Is it DNS? Is it an application or network problem?). The Hubble logo and a KodeKloud copyright are also visible." />
</Frame>

<Frame>
  <img alt="A Hubble slide titled &#x22;Error Events&#x22; with a code-and-warning icon on the left and four monitoring questions on the right about DNS resolution problems, interrupted TCP connections, unanswered TCP SYN requests, and 4xx/5xx HTTP response rates." />
</Frame>

<Frame>
  <img alt="A slide titled &#x22;Latency and Access&#x22; from Hubble with a blue panel and a clock-like icon on the left. On the right are numbered questions (15–19) about 95th/99th percentile latency, latency between services, worst-performing services, blocked connections/access from outside the cluster, and DNS resolution." />
</Frame>

Hubble’s flow telemetry plus Prometheus metrics enable SREs and developers to trace issues from service symptoms down to network-level causes quickly.

## Cilium and service-mesh functionality

Many features provided by service meshes overlap with Cilium capabilities: resilient connectivity, L7 routing, identity-based security, ingress/gateway functionality, and observability/tracing. Cilium can therefore serve as or replace parts of a traditional service mesh by combining an Envoy-based datapath (or other proxies), authentication primitives, and Hubble-based observability.

<Frame>
  <img alt="A diagram titled &#x22;How Does Cilium Work?&#x22; showing layered components: Service Mesh, Observability (Cilium Hubble), Networking (Cilium CNI) and Runtime Security (Tetragon), with icons for related tools (Ingress, Gateway API, spiffe, Prometheus, Grafana, fluentd, OpenTelemetry, etc.). The bottom row shows supported platforms like AWS, Google Cloud, Azure, Alibaba Cloud, Red Hat OpenShift and VMware." />
</Frame>

Grouped capabilities:

* Networking: encryption, load balancing, network policy, IPv4/IPv6, overlays/BGP, multi-cluster, egress gateway.
* Observability: metrics, tracing, service maps, logs.
* Service mesh: ingress, Gateway API, authentication, L7 traffic management.

Note: runtime security components like Tetragon are complementary but not covered in this lesson.

## How Cilium works: eBPF and core concepts

Cilium is built on eBPF (extended Berkeley Packet Filter), which enables in-kernel, sandboxed programs to perform networking, security, and observability tasks with low overhead.

Key properties:

* eBPF-powered datapath for high-performance packet processing.
* Layer 3–7 capabilities: from IP routing to L7 protocol inspection.
* Identity-based policy enforcement (workload identity vs IP addresses).
* Can replace kube-proxy for service handling (kube-proxy replacement).
* Supports bandwidth control and Quality-of-Service (QoS) features.

<Frame>
  <img alt="A slide titled &#x22;How Does Cilium Work?&#x22; listing five key points: built on eBPF; works at Layer 3–7; uses identity-based policies; can replace kube-proxy; supports bandwidth control." />
</Frame>

What is eBPF?

* eBPF lets you run small, verified programs inside the kernel without changing kernel source code or loading kernel modules.
* eBPF programs attach to kernel hooks (networking, tracepoints, syscalls) and can inspect and act on packets, events, and system calls with minimal context switching.
* This in-kernel execution yields lower latency, better throughput, and richer visibility compared to user-space-only solutions.

<Frame>
  <img alt="A simplified eBPF architecture diagram showing user-space apps above syscalls and kernel components (networking, files, memory, process mgmt) with eBPF programs attached. On the right it lists benefits: faster processing, better scaling, and better visibility." />
</Frame>

eBPF enables many of Cilium’s features:

* Kernel-accelerated packet routing and forwarding for the CNI.
* L4 and L7 load balancing with minimal overhead.
* NAT and encapsulation for overlay/underlay networking.
* Multi-cluster connectivity (Cluster Mesh) and cross-cluster service handling.
* mTLS/encryption and secure tunnels between endpoints.
* Enforcement of NetworkPolicy and CiliumNetworkPolicy with protocol-aware inspection.
* Real-time flow visibility, metrics, tracing, and logging.

> **lightbulb** Because eBPF runs inside the kernel, Cilium delivers low-latency, scalable packet processing and deep telemetry without requiring user-space proxies for many datapath operations.

## Summary

Cilium is a comprehensive, eBPF-powered platform for Kubernetes networking, security, and observability:

* Acts as a CNI and provides L4/L7 load balancing, ingress/gateway, egress control, and multi-cluster features.
* Enforces Kubernetes NetworkPolicy and provides CiliumNetworkPolicy for protocol-aware L7 controls.
* Supports pod-to-pod encryption via IPsec or WireGuard.
* Hubble delivers flow-level observability and troubleshooting, integrating with Prometheus and Grafana.
* Built on eBPF for performance, scalability, and rich visibility.
* Can replace kube-proxy and provide many service-mesh capabilities, reducing the need for separate service-mesh layers in some deployments.

By combining eBPF-driven performance with identity-based security and Hubble observability, Cilium offers a modern, unified approach to Kubernetes networking and security.

## Links and references

* Cilium official site: [https://www.cilium.io](https://www.cilium.io)
* Hubble: [https://www.cilium.io/features/hubble/](https://www.cilium.io/features/hubble/)
* eBPF: [https://ebpf.io](https://ebpf.io)
* Envoy proxy: [https://www.envoyproxy.io](https://www.envoyproxy.io)
* Prometheus: [https://prometheus.io](https://prometheus.io)
* Grafana: [https://grafana.com](https://grafana.com)
* Kubernetes NetworkPolicy docs: [https://kubernetes.io/docs/concepts/services-networking/network-policies/](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* WireGuard: [https://www.wireguard.com](https://www.wireguard.com)
* IPsec (Wikipedia): [https://en.wikipedia.org/wiki/IPsec](https://en.wikipedia.org/wiki/IPsec)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/9c9fa5ec-2721-4654-9383-5cb9b264e8b6/lesson/259bc127-2355-4830-b8a8-ae032cd0ca1c)
