# cilium-config snippet (example)
routingMode: "native"

# IPv4 CIDR(s) that will use native routing (e.g., your cluster Pod CIDR)
ipv4NativeRoutingCIDR: "10.244.0.0/16"
ipv6NativeRoutingCIDR: ""
```

Notes about these settings:

* ipv4NativeRoutingCIDR defines which IP range(s) Cilium advertises or treats as natively routed.
* Traffic within that CIDR will be forwarded natively by the underlay; traffic outside falls back to encapsulation.
* You can restrict the range (for example, a /17) to mix native and encapsulated traffic across different pod groups.

### Pros and cons of native routing

| Pros                                                            | Cons                                                                       |
| --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| No encapsulation overhead → better throughput and lower latency | Requires underlay routing for pod CIDRs (static routes or dynamic routing) |
| Full visibility into packets (no tunnel headers)                | Adds operational complexity (BGP peering, route management)                |
| No MTU overhead related to encapsulation                        | Less portable where providers restrict route advertisement or BGP          |

> **warning** Native routing requires careful underlay configuration. If your physical network lacks routes for the pod CIDRs (or your cloud provider blocks route advertisement), pod-to-pod traffic can be dropped. Plan route distribution (e.g., BGP) before switching to native routing.

***

## Quick comparison

| Feature                | Encapsulation (Tunnel)                  | Native routing                           |
| ---------------------- | --------------------------------------- | ---------------------------------------- |
| Underlay requirement   | Node-to-node IP reachability only       | Underlay must know pod CIDRs             |
| Overhead               | Yes — tunnel headers (e.g., \~50 bytes) | No                                       |
| MTU impact             | May reduce effective MTU                | No encapsulation-related MTU reduction   |
| Operational complexity | Lower                                   | Higher (routing configuration, BGP)      |
| Portability            | High                                    | Depends on provider/network capabilities |
| Visibility & debugging | Harder (inner packets hidden)           | Easier (packets visible)                 |

***

## Choosing a mode

* Use encapsulation if you need portability and minimal underlay changes (default for many environments).
* Use native routing for maximum performance and visibility if you can reliably distribute pod routes into the underlay (for example with BGP).
* Consider a hybrid approach: advertise only selected CIDRs natively and encapsulate others.

***

## Links and references

* Cilium documentation — Routing and node connectivity: [https://docs.cilium.io/](https://docs.cilium.io/)
* Kubernetes networking concepts: [https://kubernetes.io/docs/concepts/cluster-administration/networking/](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
* VXLAN overview: [https://tools.ietf.org/html/rfc7348](https://tools.ietf.org/html/rfc7348)
* Geneve overview: [https://tools.ietf.org/html/rfc8926](https://tools.ietf.org/html/rfc8926)
* BGP basics: [https://en.wikipedia.org/wiki/Border\_Gateway\_Protocol](https://en.wikipedia.org/wiki/Border_Gateway_Protocol)

Further reading:

* [Cilium BGP integration](https://docs.cilium.io/en/stable/concepts/bgp/)
* [Kubernetes CNI plugins and networking models](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)

***

Summary

* Encapsulation (tunneling) is simpler to deploy and portable, but adds overhead and MTU considerations.
* Native routing removes encapsulation overhead and improves performance but requires route distribution into the physical network (BGP or static routes).
* Cilium supports both modes and allows mixing them by CIDR. Choose based on your underlay capabilities, performance goals, and operational constraints.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/0807e400-fd1b-4f25-bba5-d0fdb0f4e3f2/lesson/4d28cf35-5a75-45be-a5a0-7c709017d8f9)


# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Exploring-Cilium/Section-Introduction/page

Practical guide to Cilium configuration, routing modes, kube-proxy-less performance, terminology, and packet flow for Kubernetes networking production use.

In this lesson we'll cover the essential Cilium configuration options and concepts needed to deploy and operate Cilium in Kubernetes. The goal is to give you a practical understanding of common, high-impact settings, the different routing modes Cilium offers, and how the kube-proxy-less architecture accelerates Kubernetes service handling. You'll also learn Cilium-specific terminology that appears in configuration and observability tools, and finish with a deep packet walk that traces how packets traverse nodes and the cluster network when Cilium is in use.

What you'll learn:

* Configuration options and recommended settings for production and testing
* Routing modes supported by Cilium and when to use each
* How the kube-proxy-less architecture works and why it improves performance
* Important Cilium terminology used in policies and telemetry
* A step-by-step deep packet walk (packet flow through nodes and the cluster)

<Frame>
  <img alt="A presentation agenda slide with a vertical timeline of five numbered colored markers beside the word &#x22;Agenda.&#x22; The items list Cilium topics: configuration options, routing modes, kube-proxy-less architecture, terminology, and understanding packet flow." />
</Frame>

> **lightbulb** This lesson focuses on actionable, production-relevant topics. If you're preparing for Cilium-related certification or improving cluster networking performance, pay close attention to the routing modes and kube-proxy-less sections — they cover common pitfalls and optimization strategies.

Key topics at a glance:

| Topic                        | Why it matters                                        | Where to apply                                      |
| ---------------------------- | ----------------------------------------------------- | --------------------------------------------------- |
| Configuration options        | Affects security, performance, and observability      | Cluster bootstrapping, CI/CD, production clusters   |
| Routing modes                | Determines packet path and load-balancing behavior    | Multi-node clusters, cloud vs bare metal            |
| Kube-proxy-less architecture | Reduces latency and CPU by offloading services to BPF | High-throughput services, latency-sensitive apps    |
| Terminology                  | Understand logs, metrics, and policy rules            | Debugging, writing policies, readouts in dashboards |
| Deep packet walk             | Visualizes actual packet handling to diagnose issues  | Troubleshooting and performance tuning              |

Links and references:

* [Cilium Documentation](https://docs.cilium.io/)
* [Kubernetes Networking Concepts](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
* [eBPF Overview](https://ebpf.io/)

Next, we'll dive into Cilium's configuration options, followed by routing modes and the kube-proxy-less architecture.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/0807e400-fd1b-4f25-bba5-d0fdb0f4e3f2/lesson/8975df5e-e56d-4131-a91d-4780a3564123)
