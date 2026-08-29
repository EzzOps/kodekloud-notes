# kube-controller-manager example flags (truncated)
kube-controller-manager \
  --allocate-node-cidrs=true \
  --cluster-cidr=10.244.0.0/16,fd00:10:244::/56 \
  --service-cluster-ip-range=10.96.0.0/16,fd00:10:96::/112 \
  --kubeconfig=/etc/kubernetes/controller-manager.conf \
  --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf \
  --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf \
  --bind-address=127.0.0.1 \
  --client-ca-file=/etc/kubernetes/pki/ca.crt \
  --cluster-name=my-cluster \
  --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt \
  --cluster-signing-key-file=/etc/kubernetes/pki/ca.key \
  --controllers=*,bootstrapsigner,tokencleaner \
  --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt \
  --root-ca-file=/etc/kubernetes/pki/ca.crt \
  --service-account-private-key-file=/etc/kubernetes/pki/sa.key
```

The controller-manager divides the cluster CIDR into node-sized slices (for example /24s) and records the assigned CIDR(s) on the Kubernetes Node resource. A Node will include the assigned podCIDR(s), for example:

```yaml theme={null}
apiVersion: v1
kind: Node
metadata:
  labels:
    kubernetes.io/hostname: my-cluster-worker
    kubernetes.io/os: linux
  name: my-cluster-worker
spec:
  podCIDR: 10.244.2.0/24
  podCIDRs:
    - 10.244.2.0/24
    - fd00:10:244:2::/64
```

When Cilium is configured to use Kubernetes host-scope IPAM, the Cilium agent reads the Node resource to learn the node’s podCIDR(s). Configure Cilium to wait for the Node-provided CIDR(s) and set IPAM mode to "kubernetes":

```yaml theme={null}
ipam:
  # Configure IP Address Management mode.
  # ref: https://docs.cilium.io/en/stable/network/concepts/ipam/
  mode: "kubernetes"

k8s:
  # Wait for Kubernetes to provide the PodCIDR via the Node resource
  requireIPv4PodCIDR: true
  requireIPv6PodCIDR: true
```

With these settings, the Cilium agent will not allocate pod IPs until the Node resource contains the podCIDR(s).

***

## Cluster-scope IPAM (Cilium operator) — default

Cilium’s default IPAM mode is cluster-scope, also referred to as "cluster-pool". In this model the Cilium operator manages a cluster-wide pool of CIDRs and delegates per-node subnets directly (rather than relying on kube-controller-manager).

To enable operator-managed allocation set mode to "cluster-pool" and provide the cluster-wide CIDR lists and per-node mask sizes:

```yaml theme={null}
ipam:
  mode: "cluster-pool"
  operator:
    # IPv4 CIDR list to delegate to nodes for IPAM
    clusterPoolIPv4PodCIDRList: ["10.0.0.0/8"]
    # IPv4 per-node mask size (e.g., 24 -> /24 per node)
    clusterPoolIPv4MaskSize: 24
    # IPv6 CIDR list and per-node mask size (if using IPv6)
    clusterPoolIPv6PodCIDRList: ["fd00::/104"]
    clusterPoolIPv6MaskSize: 120
```

In cluster-pool mode the operator creates or updates a CiliumNode custom resource for each Kubernetes node. The Cilium agent watches its node's CiliumNode resource to learn the delegated podCIDR(s). Example CiliumNode:

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumNode
metadata:
  generation: 4
  labels:
    kubernetes.io/hostname: my-cluster-worker2
  name: my-cluster-worker2
  resourceVersion: "2086"
  uid: c1b72e20-f419-400b-a58e-a5d2dc7c7ee8
spec:
  ipam:
    podCIDRs:
      - 10.0.2.0/24
      - fd00::200/120
```

Once the CiliumNode resource contains podCIDRs, the agent on that node begins allocating addresses for local pods.

To inspect allocations and verify how many addresses are used on a node, run the Cilium status command in the agent pod on that node:

```bash theme={null}
kubectl exec -n kube-system cilium-cfkzf -- cilium-dbg status --all-addresses
```

Sample output showing the node’s IPAM allocation:

```console theme={null}
Kubernetes:               Ok              1.32 (v1.32.2) [linux/amd64]
IPAM:                     IPv4: 5/254 allocated from 10.0.2.0/24
Allocated addresses:
    10.0.2.163 (default/nginx)
    10.0.2.236 (router)
    10.0.2.244 (default/tshoot-66ddfc9f65-4qc7g)
    10.0.2.48  (health)
    10.0.2.74  (default/tshoot-66ddfc9f65-7572f)
```

<Frame>
  <img alt="A diagram titled &#x22;Cluster Scope (Default)&#x22; showing the Kubernetes control plane with a Cilium Operator managing three pod CIDR ranges (10.244.1.0/24, 10.244.2.0/24, 10.244.3.0/24). Each CIDR block contains pod icons with example IPs, illustrating how Cilium handles networking across the cluster." />
</Frame>

***

## Other IPAM modes (summary)

Cilium supports additional IPAM modes for advanced or platform-specific requirements. These modes can enable cloud-native integrations, multi-pool allocations, or external control via CRDs.

| IPAM Mode               | Use Case                                                                       | Notes                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| kubernetes (host-scope) | Let kube-controller-manager allocate per-node CIDRs                            | Simple for clusters that rely on Kubernetes control plane for networking decisions                |
| cluster-pool (default)  | Let Cilium operator manage a cluster CIDR and delegate per-node subnets        | Offers Cilium-managed delegation and is the default for many installations                        |
| multi-pool              | Allocate pod CIDRs from multiple pools and assign workloads to different pools | Useful for multi-tenant or performance-isolated workloads; requires additional annotations/config |
| crd-backed              | External or custom IPAM controllers manage allocations via CRDs                | Allows advanced customizations and operators to control IP allocations                            |

<Frame>
  <img alt="A slide titled &#x22;Other IPAM Modes&#x22; showing a comparison table of four modes (Kubernetes Host Scope, Cluster Scope (default), Multi-Pool, CRD-Backed) and which features they support. Rows include Tunnel Routing, Direct Routing, CIDR configuration, multiple CIDRs per cluster/node, and dynamic CIDR/IP allocation with check and cross icons." />
</Frame>

When selecting an IPAM mode, consult the Cilium IPAM documentation to confirm which network features are supported in that mode (not every feature is available for all modes): [https://docs.cilium.io/en/stable/network/concepts/ipam/](https://docs.cilium.io/en/stable/network/concepts/ipam/)

> **warning** Do not change the IPAM mode of an existing, running cluster. Switching IPAM mode on a live cluster can disrupt networking and cause persistent connectivity issues for running workloads. To change modes safely, deploy a new cluster with the desired IPAM configuration and migrate workloads.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/0807e400-fd1b-4f25-bba5-d0fdb0f4e3f2/lesson/bbf92c1d-8fe5-4f8a-a7dc-50234980b52d)


# Kube Proxy less

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Exploring-Cilium/Kube-Proxy-less/page

Explains replacing kube-proxy with Cilium to implement service routing and load balancing via eBPF, covering benefits, configuration steps, verification, and operational caveats

In this lesson you'll learn how to replace kube-proxy with Cilium so that service routing and load balancing run via eBPF. Cilium can be deployed in two main modes:

* Coexist with kube-proxy: Cilium provides CNI, ingress (e.g., Gateway API) and observability, while kube-proxy continues to perform service routing/load balancing using iptables or ipvs.
* Replace kube-proxy: Cilium implements service routing and load balancing directly with eBPF, removing the need for kube-proxy.

Replacing kube-proxy with an eBPF-based data plane (Cilium) yields measurable performance and scalability benefits compared to the traditional iptables approach. The fundamental difference is how packet lookup is performed.

With kube-proxy in iptables mode, each packet is evaluated against a sequential list of rules. As the number of services and endpoints grows, packet processing may require scanning many rules, and kube-proxy frequently rebuilds iptables rules on service or endpoint changes. This sequential scanning and frequent rebuilding does not scale well in highly dynamic Kubernetes clusters.

<Frame>
  <img alt="A slide titled &#x22;Why Replace iptables With eBPF?&#x22; showing that kube-proxy (iptables) requires a full rebuild when rules change, illustrated by a vertical arrow and five services each paired with lists of backend IP addresses." />
</Frame>

Cilium replaces sequential rule scanning with eBPF maps and per-CPU hash tables. Hash lookups are O(1) on average, so increasing the number of services and endpoints does not proportionally increase packet-processing latency as with iptables. This architecture delivers lower latency, improved scalability, more efficient load balancing, and richer observability and debugging.

<Frame>
  <img alt="A slide diagram titled &#x22;Why Replace iptables With eBPF?&#x22; showing an eBPF-based per-CPU hash table that maps names (John Smith, Lisa Smith, Sandra Dee) to bucket indices and phone-number-like values (e.g., 521-8976, 521-9655). It illustrates keys hashing to the same bucket slots across per-CPU tables." />
</Frame>

Key benefits of replacing kube-proxy with Cilium (eBPF)

* Lower packet-processing latency
* Better scalability for clusters with many services and endpoints
* More efficient and flexible load balancing (including session affinity and L4/L7 options)
* Enhanced observability, tracing, and debugging via Cilium tooling

Summary comparison

| Aspect              | kube-proxy (iptables/ipvs)            | Cilium (eBPF, kube-proxy replacement) |
| ------------------- | ------------------------------------- | ------------------------------------- |
| Packet lookup model | Sequential rule matching (iptables)   | Hash-based eBPF maps (per-CPU)        |
| Scalability         | Degrades with many services/endpoints | Scales well due to O(1) lookups       |
| Rule rebuilds       | Frequent, on service/endpoint change  | Minimal, maps updated efficiently     |
| Observability       | Limited                               | Rich telemetry integrated in Cilium   |
| Load balancing      | iptables/ipvs                         | eBPF-based, more efficient            |

Default Cilium behavior
By default Cilium does not replace kube-proxy; it coexists and delegates service routing to kube-proxy:

```yaml theme={null}
kubeProxyReplacement: "false"
```

You can confirm the current kube-proxy replacement setting from a Cilium agent:

```bash theme={null}
kubectl -n kube-system exec ds/cilium -- cilium-dbg status | grep KubeProxyReplacement
```

If the output shows `KubeProxyReplacement: false`, kube-proxy remains active and continues handling service routing.

When to replace kube-proxy
Consider replacing kube-proxy with Cilium when you need:

* Lower L4 packet latency for high-throughput workloads
* A more scalable service datapath for large clusters
* Integrated observability and easier troubleshooting
* Reduced operational complexity from iptables/ipvs rule churn

Before you proceed, validate control-plane connectivity and cluster-specific networking requirements.

Step-by-step: Replacing kube-proxy with Cilium

1. Remove kube-proxy artifacts
   First, delete the kube-proxy DaemonSet and the associated ConfigMap. Removing the ConfigMap prevents kubeadm from automatically re-installing kube-proxy during control-plane upgrades on supported versions:

```bash theme={null}
kubectl -n kube-system delete ds kube-proxy
