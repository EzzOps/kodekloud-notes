# Tuning

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Optimization/Tuning/page

Practical guidance to tune Cilium for improved throughput and latency by using netdev datapath, host routing bypass, and BIG TCP with deployment and testing considerations

In this lesson we cover practical Cilium performance enhancements you can enable to improve throughput and latency. These knobs are commonly used in production and are useful for understanding how Cilium forwards packets at scale. The explanations remain tied to the accompanying diagrams so you can visualize how traffic flows through the host and pod network stacks.

Architecture reminder

* Each Kubernetes node has a host network namespace (with the main interface to the outside world).
* Each Pod runs in its own network namespace.
* Pods and the host are typically connected via a veth pair; many of the tunables below replace or bypass parts of that path to reduce host-side processing and latency.

Key tuning areas covered:

* netdev datapath (replace veth with the AF\_XDP-based datapath)
* host routing (bypass host iptables/netfilter for selected flows)
* BIG TCP (coalesce TCP segments to reduce packet rate)

Netdev datapath (replace veth)
Cilium can replace the veth pair between host and pod with a kernel/AF\_XDP-based datapath (netdev). This reduces host-side overhead and gives better throughput and lower latency compared to the traditional veth path because fewer context switches and less software processing are involved.

<Frame>
  <img alt="A simple diagram titled &#x22;Netkit Devices&#x22; showing a Host Namespace (with eth0 and a netkit device) connected via a netkit link to a netkit device inside a Pod. The caption notes &#x22;Improved throughput and latency.&#x22;" />
</Frame>

To enable netdev at install time, set Cilium's routing mode to native, select the netdev datapath, enable masquerading if you need SNAT, and turn on kube-proxy replacement. Example Helm install:

```bash theme={null}
helm install cilium cilium/cilium --version 1.17.4 \
  --namespace kube-system \
  --set routingMode=native \
  --set bpf.datapathMode=netdev \
  --set bpf.masquerade=true \
  --set kubeProxyReplacement=true
```

Important flags explained:

* routingMode=native — use native eBPF-based routing instead of proxy-based routing.
* bpf.datapathMode=netdev — use the netdev (AF\_XDP) datapath rather than veth.
* bpf.masquerade=true — enables eBPF-based masquerading (SNAT) when required.
* kubeProxyReplacement=true — replaces kube-proxy with Cilium’s eBPF-based proxy implementation.

Host routing (bypass the host netfilter/iptables path)
By default, pod traffic may traverse the host network stack and be processed by netfilter/iptables. Host routing lets Cilium bypass parts of the host stack for selectable flows, which reduces overhead and improves forwarding efficiency.

<Frame>
  <img alt="A simplified &#x22;Host‑Routing&#x22; diagram showing the host interface (eth0) connected to both an upper host network stack (iptables/NetFilter) and a Pod. Arrows indicate traffic flow between eth0, the host stack, and the Pod." />
</Frame>

To enable host routing–related optimizations, ensure Cilium’s eBPF masquerade and kube-proxy replacement are enabled. A minimal install or upgrade to enable these features:

```bash theme={null}
helm install cilium cilium/cilium --version 1.17.4 \
  --namespace kube-system \
  --set bpf.masquerade=true \
  --set kubeProxyReplacement=true
```

Notes:

* In many deployments you will combine these settings with the netdev datapath.
* Host routing behavior depends on cluster topology and whether nodes are directly routed or behind NAT/load balancers.

BIG TCP (reduce packet processing by coalescing TCP segments)
On high-speed links (100 Gbps+), the sender can generate millions of packets per second for small MTUs. Kernel offloads (GSO/GRO/LRO/TCP segmentation offload) allow coalescing many segments into larger aggregated packets, drastically reducing the packet processing rate and CPU overhead. Cilium supports enabling BIG TCP to allow much larger aggregated TCP segments (for example, up to \~1 MiB), which can reduce pps from millions to tens of thousands for equivalent throughput.

BIG TCP requires kernel and NIC driver support for large GSO/GRO and correct hardware offload behavior. When enabled, you can selectively enable BIG TCP for IPv4 and/or IPv6.

<Callout icon="lightbulb">
  BIG TCP requires kernel and NIC driver support. Test carefully on staging before enabling in production. Incorrect assumptions about offloads or driver behavior can cause performance issues or packet corruption.
</Callout>

Example Helm install enabling BIG TCP for both IPv4 and IPv6:

```bash theme={null}
helm install cilium cilium/cilium --version 1.17.4 \
  --namespace kube-system \
  --set routingMode=native \
  --set bpf.masquerade=true \
  --set ipv6.enabled=true \
  --set enableIPv4BIGTCP=true \
  --set enableIPv6BIGTCP=true \
  --set kubeProxyReplacement=true
```

Flag summary:

* enableIPv4BIGTCP=true — enable BIG TCP for IPv4.
* enableIPv6BIGTCP=true — enable BIG TCP for IPv6.
* ipv6.enabled=true — required when enabling IPv6-specific features.

Configuration quick reference

| Tuning area               | Primary effect                                                        | Key Helm settings                                                                           |
| ------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| netdev datapath (AF\_XDP) | Replaces veth, reduces host processing, improves throughput & latency | routingMode=native, bpf.datapathMode=netdev, bpf.masquerade=true, kubeProxyReplacement=true |
| Host routing              | Bypasses iptables/netfilter for flows, reduces forwarding overhead    | bpf.masquerade=true, kubeProxyReplacement=true (often combined with netdev)                 |
| BIG TCP                   | Coalesces TCP segments to reduce pps and CPU usage                    | enableIPv4BIGTCP=true, enableIPv6BIGTCP=true, ipv6.enabled=true                             |

Deployment checklist before rolling out tuning changes

* Validate kernel version and NIC driver support for AF\_XDP and large GSO/GRO.
* Test netdev and BIG TCP in a staging environment using realistic traffic patterns.
* Monitor CPU, packet rates (pps), and error counters (e.g., XDP drops, checksum errors) after enabling changes.
* Confirm compatibility with your CNI configuration, routing topology, and upstream load balancers.

Further reading and references

* Cilium official docs: [https://docs.cilium.io/](https://docs.cilium.io/)
* AF\_XDP / XDP overview: [https://www.kernel.org/doc/html/latest/networking/index.html#xdp](https://www.kernel.org/doc/html/latest/networking/index.html#xdp)
* Linux network offloads (GSO/GRO/TCP segmentation offload): [https://www.kernel.org/doc/Documentation/networking/](https://www.kernel.org/doc/Documentation/networking/)

<Callout icon="warning">
  Always test these optimizations (netdev datapath, host routing, and BIG TCP) in a non-production environment first. Hardware and driver incompatibilities or misconfigured offloads can cause degraded performance or packet corruption.
</Callout>

Wrap-up
Using the netdev datapath to replace veth, enabling host routing to bypass the host netfilter stack, and enabling BIG TCP to reduce packet processing are common levers to improve Cilium throughput and latency. Validate kernel and NIC driver compatibility and run staged tests before broad rollout.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/282722e0-2670-40d1-b2c5-87638e579e49/lesson/0a1730d8-92c1-4663-bed2-ecd2afaac905" />
</CardGroup>
