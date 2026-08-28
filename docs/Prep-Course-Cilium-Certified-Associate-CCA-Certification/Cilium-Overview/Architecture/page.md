# values.yaml (illustrative)
bgp:
  enabled: true
  # Add your BGP neighbors/peers here
  neighbors:
    - peer-address: 10.0.0.1
      peer-as: 65001
      my-as: 65000
loadBalancer:
  ipam:
    # Enable Cilium-managed IP pools for Service.loadBalancerIP
    enabled: true
    # An example pool of IPs to assign to LoadBalancer services
    pools:
      - name: lb-pool
        cidr: 192.0.2.0/28
        # optional: range to restrict the assigned subset
        range: 192.0.2.2-192.0.2.14
```

<Callout icon="warning">
  BGP advertises routes into your network—misconfiguration can cause traffic blackholes or route leaks. Coordinate prefix announcements and AS numbers with your network team before enabling BGP.
</Callout>

## Typical configuration flow

* Install or update Cilium with the desired Helm values (or update a Cilium ConfigMap); examples above are illustrative.
* Ensure network/router side is configured to accept BGP sessions from your cluster nodes (peer IPs, AS numbers, route filters).
* Configure the load-balancer IP pool in Cilium so that Service objects of type LoadBalancer can be assigned IPs from the pool.
* Deploy a sample app and create a Service of type LoadBalancer to test the allocation and BGP announcements.

## Verification checklist and commands

Use these checks in sequence to validate the setup:

1. Verify Cilium agents are running

```bash theme={null}
kubectl get pods -n kube-system -l k8s-app=cilium
kubectl logs -n kube-system -l k8s-app=cilium --tail=100
```

2. Inspect the Service and the assigned external IP

```bash theme={null}
kubectl apply -f samples/sample-loadbalancer-svc.yaml
kubectl get svc -o wide
kubectl describe svc <service-name>
```

3. Confirm the external IP came from your configured pool

* Check the Service's external IP matches an address inside the pool CIDR.

4. Check BGP advertisements and neighbor states

* On your external router(s): verify BGP neighbor is established and that the prefix for the Service IP (or the service/pod CIDR) is being learned.
* Example: Router CLI (platform dependent)
  * Cisco-like: `show ip bgp summary` / `show ip route <prefix>`
  * BIRD: `birdc show status` / `birdc show route for 192.0.2.2`
* On the cluster: review Cilium logs and status for BGP-related messages

```bash theme={null}
kubectl -n kube-system logs -l k8s-app=cilium | grep -i bgp || true
kubectl -n kube-system exec -it <cilium-pod> -- cilium status
```

5. End-to-end connectivity test

* From an external host in the same network, confirm TCP/HTTP reachability to the LoadBalancer IP:

```bash theme={null}
curl -v http://192.0.2.2/    # Replace with actual external IP
# or
telnet 192.0.2.2 80
```

6. Trace traffic flow to confirm it reaches the service endpoint

* Use tcpdump on the node or Cilium endpoints to observe the incoming packets and their forwarding.

```bash theme={null}
# Example: run on a node (requires appropriate access)
sudo tcpdump -i any host 192.0.2.2
```

## References and further reading

* Cilium documentation: [https://docs.cilium.io/](https://docs.cilium.io/)
* Cilium LoadBalancer/IPAM guide: [https://docs.cilium.io/en/stable/loadbalancer/](https://docs.cilium.io/en/stable/loadbalancer/)
* Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
* BGP basics and router configuration: refer to your router vendor documentation (Cisco, Juniper, BIRD, FRR, etc.)

This lesson will expand each bullet above into concrete configuration and verification steps, with example manifests and commands to run. Follow the sections in order to ensure safe rollout and predictable behavior.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/fc66c3e4-b28d-440e-a771-66524646d81e" />
</CardGroup>


# Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cilium-Overview/Architecture/page

Overview of Cilium architecture covering per-node agent, eBPF datapath, operator, Envoy L7 proxy, Hubble observability, kube-proxy replacement, and sidecar versus sidecarless service mesh models

In this lesson we examine the Cilium architecture end-to-end: the per-node agent, the in-kernel datapath powered by eBPF, cluster-wide controller responsibilities, L7 proxying with Envoy, observability with Hubble, kube-proxy integration/replacement, and service-mesh deployment models (sidecar vs sidecarless). Each section explains the component's role, how it integrates with the rest of the system, and the traffic flow implications.

Key components covered

* Cilium agent (per-node daemon)
* eBPF programs (in-kernel datapath)
* Cilium operator (cluster-wide controller)
* Envoy proxy (L7 proxy)
* Hubble (observability)
* kube-proxy (and Cilium's kube-proxy replacement mode)
* Service mesh models: sidecar vs sidecarless

| Component       | Primary role                                           | When it matters                          |
| --------------- | ------------------------------------------------------ | ---------------------------------------- |
| Cilium agent    | Per-node orchestration, loads eBPF, enforces policies  | Always on each node                      |
| eBPF datapath   | High-performance L3/L4 networking, in-kernel LB/policy | East‑west traffic, services              |
| Cilium operator | Cluster-wide state (IPs, services, identities, CRDs)   | Multi-node coordination, IPAM            |
| Envoy           | L7 termination, routing, mTLS, deep observability      | HTTP/gRPC, advanced L7 policies          |
| Hubble          | Flow capture, metrics, CLI/UI integration              | Troubleshooting, monitoring              |
| kube-proxy      | Service programming (iptables/ipvs)                    | Only if Cilium runs alongside kube-proxy |

## Cilium agent

The Cilium agent runs on every node (typically as a DaemonSet). It is responsible for translating Kubernetes cluster state into datapath configuration and ensuring the kernel runs the correct programs.

Primary responsibilities:

* Watch Kubernetes API events (Pods, Services, Endpoints, CRDs) and translate cluster state into datapath configuration.
* Compile, load, and attach eBPF programs to the appropriate kernel hooks and network interfaces.
* Enforce network policies and implement service/load-balancing rules using eBPF.
* Route traffic to Envoy when L7 processing is required.
* Host a local Hubble server for per-node flow capture and metrics.

The agent continuously monitors cluster changes (pod lifecycle events, service updates, endpoint changes, CRD updates) and updates kernel programs and rules on the fly so networking and security remain consistent with the cluster state.

<Frame>
  <img alt="A slide titled &#x22;Architecture&#x22; showing a Cilium Agent hexagonal logo on the left. On the right are feature boxes listing Networking, Load Balancing, Network Policies, and Observability and Monitoring." />
</Frame>

## eBPF datapath

Cilium leverages eBPF to implement the datapath inside the Linux kernel. eBPF programs provide a fast, flexible way to control networking without costly user/kernel context switches.

What eBPF provides for Cilium:

1. L3/L4 ingress and egress packet processing (IP/TCP/UDP).
2. In-kernel, efficient load balancing for Services.
3. Low-overhead enforcement of network and security policies.

Because eBPF runs in-kernel, it reduces context switching and improves throughput and scalability versus equivalent user-space proxies for many L3/L4 operations. The Cilium agent ensures the correct eBPF programs are compiled, loaded, and attached to the right network interfaces and hooks in response to cluster events.

<Frame>
  <img alt="A presentation slide titled &#x22;Architecture&#x22; with a bee logo labeled &#x22;ebpf&#x22; on the left. On the right are three numbered points: control ingress and egress network traffic, load balance traffic efficiently, and enforce security policies with minimal overhead." />
</Frame>

## Cilium operator

The Cilium operator handles cluster-scoped duties that don’t belong to any single node agent. It keeps cluster-wide state synchronized and performs tasks that require global knowledge.

Operator responsibilities:

* Synchronize node IPs and lifecycle between Kubernetes and Cilium.
* Coordinate cluster-wide service information so nodes program consistent service maps.
* Manage IP allocation for services when using Cilium’s eBPF-based load balancer.
* Allocate and synchronize security identities (used by network policies).
* Manage CIDRs, CRDs, and IPAM tasks for cluster-scoped resources.
* Assist Cluster Mesh / multi-cluster configuration and CRD lifecycle.
* Aggregate or coordinate Hubble relays and observability across the cluster.

The operator ensures a consistent, cluster-scoped picture of nodes, services, identities, and CRDs—essential for multi-node and multi-cluster deployments.

<Frame>
  <img alt="A presentation slide titled &#x22;Architecture&#x22; listing twelve numbered cluster/network components. Items include Node Management, Cluster‑Wide Services, Load Balancer, Identity & Security, CIDR/CRD/IPAM management, Cluster Mesh, security identity management, and Hubble relay support." />
</Frame>

## Envoy proxy (L7)

Envoy is used by Cilium to provide Layer‑7 features that cannot be implemented in-kernel. Typical L7 responsibilities include HTTP/gRPC routing, rate limiting, TLS/mTLS termination, and deep request inspection for observability and policy.

Deployment options:

* Embedded in the Cilium agent (in‑agent Envoy).
* Deployed as a single Envoy pod per node (node-level proxy).

When an L7 policy or observability feature is required, Cilium routes that traffic to Envoy for termination and inspection. Envoy handles L7 filtering, routing, TLS termination, and richer telemetry that complements eBPF’s L3/L4 strengths. In Cilium’s sidecarless model, fewer proxies are used (typically one per node), reducing per-pod resource cost.

## Kubernetes CRDs

Cilium installs several Kubernetes CRDs to represent policies, observability settings, and other Cilium-specific configuration. These CRDs provide a Kubernetes-native interface to express Cilium network policies, service mesh configuration, and observability controls across the cluster.

## Hubble: per-node server, relay, CLI, UI

Hubble provides high-performance observability built on eBPF flow capture. Each Cilium agent includes a Hubble server for local flow telemetry.

Hubble components and capabilities:

* Per-node Hubble server that streams eBPF-based flow data with low overhead.
* gRPC API and Prometheus metrics endpoints for integration and monitoring.
* Capture of L3/L4 flows and optional L7 telemetry (when Envoy provides L7 context).
* Visibility into packet drops, DNS queries, policy decisions, and more for debugging.

Hubble relay is optional and aggregates flow data from multiple per-node Hubble servers to present a centralized cluster-wide view. Administrators can query flows via the Hubble CLI or visualize traffic and dependencies in the Hubble UI.

<Frame>
  <img alt="A presentation slide titled &#x22;Architecture&#x22; with a &#x22;Hubble Server&#x22; icon on the left. On the right are four numbered points describing features: eBPF-based visibility, a gRPC service for flows and Prometheus metrics, L3/L4 and L7 flow capture, and visibility into packet drops, DNS queries, and security policies." />
</Frame>

A centralized Hubble relay plus the UI/CLI provides powerful cluster-wide observability for troubleshooting and policy verification.

## kube-proxy and Cilium’s kube-proxy replacement

Kubernetes uses kube-proxy on each node to program iptables/ipvs rules for Services. Cilium can either run alongside kube-proxy or replace it entirely by implementing service handling in eBPF.

Benefits of kube-proxy replacement mode:

* Service load-balancing and routing are programmed directly in the kernel via eBPF.
* Improved performance and scalability compared to iptables/ipvs.
* Reduced complexity by removing the need for kube-proxy in the datapath.

<Callout icon="lightbulb">
  Cilium can run in kube-proxy replacement mode: instead of running kube-proxy, Cilium programs the service datapath using eBPF for more efficient Service traffic handling.
</Callout>

## Service mesh: sidecar vs sidecarless

Service meshes historically required either application libraries or a sidecar proxy per pod to implement features such as load balancing, mTLS, rate limiting, tracing, and observability.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Service Mesh – Features&#x22; showing five numbered feature cards: Resilient Connectivity, L7 Traffic Management, Identity-Based Security, Observability and Tracing, and Transparency. Each card includes a brief description of that feature's purpose." />
</Frame>

### Sidecar model

The sidecar pattern deploys a proxy (commonly Envoy) next to each application container in the pod. The proxy implements mesh features so application code remains unchanged.

Benefits:

* No application changes required; language-agnostic.
* Works for immutable third‑party apps.
* Mesh responsibilities are offloaded to the proxy.

Drawbacks:

* One proxy per pod increases resource usage (CPU/memory).
* Operational complexity for proxy configuration and lifecycle.
* Potential startup and readiness race conditions because proxies must initialize.
* Extra network hop per request increases latency.

<Frame>
  <img alt="A slide titled &#x22;Service Mesh Implementation – Library&#x22; showing a Python app and a Go app exchanging an HTTP request while each embeds a language-specific mesh library. Both sides list features provided by the library: load balancing, rate limiting, mTLS, and tracing/metrics." />
</Frame>

<Frame>
  <img alt="A diagram titled &#x22;Service Mesh Implementation – Sidecar&#x22; showing a Python app on the left communicating through two sidecar proxy boxes (each containing a mesh library) to a Go app on the right. Arrows indicate request flow from the Python app through the sidecars to the Go app." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;Service Mesh Implementation – Sidecar.&#x22; It lists three benefits—services don't need to implement mesh functionality; useful for apps in different languages; and supports immutable third‑party applications—each shown with a simple icon." />
</Frame>

### Sidecarless model (Cilium)

Cilium’s sidecarless approach moves most mesh capabilities into the kernel using eBPF, and uses a smaller number of Envoy proxies for L7 features.

Key characteristics:

* L3/L4 logic (routing, policy enforcement, service load balancing) is handled in-kernel by eBPF.
* L7 features (HTTP/gRPC routing, rate limiting, deep inspection, application-protocol policies) are handled by Envoy.
* Instead of one Envoy per pod, Cilium commonly runs a single Envoy per node (or an Envoy embedded in the agent), drastically reducing per-pod resource overhead.

This approach lowers resource consumption and simplifies deployments while preserving full L7 capabilities when required.

<Frame>
  <img alt="A slide diagram titled &#x22;Service Mesh Implementation – Sidecarless&#x22; showing eBPF running in the kernel inside a pod to handle networking instead of a sidecar. It also shows the protocol stack and notes eBPF supports only Layer 3/4 (IP/TCP/UDP), not Layer 7 (HTTP, gRPC)." />
</Frame>

When L7 policy or observability is required, Cilium routes traffic to the node-level Envoy for L7 termination; otherwise eBPF handles the flow entirely in-kernel.

<Callout icon="warning">
  Sidecarless reduces per-pod resource usage and latency for L3/L4 flows, but advanced L7 features still depend on user‑space proxies (e.g., Envoy). Plan proxy placement and capacity accordingly.
</Callout>

### Traffic flow comparison

* L3/L4-only flow: the application socket sends packets into the kernel where eBPF implements routing, policy, and forwarding (no sidecar hop).
* L7 flow: eBPF detects the need for L7 processing and redirects traffic to the Service Mesh proxy (Envoy) for termination and deep inspection; Envoy then forwards or proxies the request to the destination.

<Frame>
  <img alt="A slide titled &#x22;Network Traffic Management – Layer 3/4 vs Layer 7&#x22; with two side-by-side diagrams showing a pod, kernel, sockets, cilium (Network & Service Mesh) + eBPF, and a service mesh proxy (Envoy) illustrating traffic flow: left shows direct L3/4 path to eth0, right shows traffic redirected to the Layer‑7 proxy for termination." />
</Frame>

Sidecarless advantages:

* Fewer containers per pod and lower aggregate CPU/memory usage.
* Better performance for L3/L4 workloads because eBPF runs in-kernel.
* Reduced complexity from fewer per-pod proxies to manage.
* Compatible with other mesh solutions when needed, enabling hybrid deployments.

Trade-offs:

* L7 features still require an Envoy proxy component; Cilium optimizes this by using fewer proxies (one per node).
* Some advanced L7 capabilities remain necessarily in user-space proxies.

## Summary

* Cilium agent runs on each node and watches the Kubernetes API to convert cluster state into kernel programs and policies.
* eBPF programs implement the high-performance datapath for L3/L4 networking, load balancing, and policy enforcement.
* The Cilium operator handles cluster-wide responsibilities (node, service, identity, IPAM, multi-cluster).
* Envoy provides L7 functionality; Cilium routes L7 flows to Envoy and can embed Envoy in the agent or run a node-level proxy.
* Hubble provides per-node flow capture; Hubble relay aggregates flows cluster-wide; the Hubble CLI and UI expose observability.
* Cilium can operate alongside kube-proxy or replace it by implementing service handling in eBPF.
* For service mesh functionality, the traditional sidecar model runs a proxy per pod; Cilium’s sidecarless approach uses eBPF for L3/L4 and a node-level Envoy for L7, reducing resource use and operational complexity.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; with three numbered points comparing service mesh models. It notes that sidecar-based meshes require a proxy per application and increase complexity, resources, latency and start times, while Cilium uses a sidecarless eBPF-based model for L3/L4 and one Envoy proxy per node for L7." />
</Frame>

## Links and references

* Cilium documentation: [https://cilium.io/docs/](https://cilium.io/docs/)
* eBPF community: [https://ebpf.io/](https://ebpf.io/)
* Envoy proxy: [https://www.envoyproxy.io/](https://www.envoyproxy.io/)
* Hubble concepts: [https://cilium.io/docs/concepts/hubble/](https://cilium.io/docs/concepts/hubble/)
* Kubernetes kube-proxy docs: [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/9c9fa5ec-2721-4654-9383-5cb9b264e8b6/lesson/1d09126e-db65-4cfb-a60d-73d2c5494650" />
</CardGroup>
