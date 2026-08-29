# Kubernetes Networking Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cilium-Overview/Kubernetes-Networking-Overview/page

Explains Kubernetes networking basics, Pod and Service CIDRs, kube-proxy, NetworkPolicy, and the role of CNI plugins like Cilium in providing networking and enforcement.

This article explains how Kubernetes networking works and the expectations the platform places on Container Network Interface (CNI) plugins such as Cilium. Understanding Kubernetes’ networking primitives—Pod CIDR, Service CIDR, kube-proxy, and NetworkPolicy—will make it easier to see what CNIs must provide and how eBPF-based CNIs (like Cilium) can replace or augment kube-proxy behavior.

## Pod IP addressing and the Pod CIDR

When you create a Kubernetes cluster you typically allocate a Pod CIDR (example: 172.16.0.0/16). Kubernetes assigns pod IP addresses from that CIDR so every pod in the cluster has an IP in the shared address space.

Kubernetes assumes a flat pod address space: any pod should be able to reach any other pod using its pod IP, regardless of which node the pods run on or the underlying node network topology. As long as nodes have IP reachability between them, pod-to-pod communication should work without application-level routing changes.

<Frame>
  <img alt="A diagram of the Kubernetes networking model showing a cluster-wide Pod CIDR (172.16.0.0/16) with pods on three nodes/data centers (IPs 172.16.0.1–172.16.0.4) and their routes across underlying networks (192.168.1.0/24 and 192.168.2.0/24). The green arrows show pod-to-pod traffic flowing between nodes." />
</Frame>

Note:

* Pod IPs are ephemeral—pods that restart typically receive new IPs.
* Host processes running directly on a node can also reach pods on that node using pod IPs.

## Services and the Service CIDR

Because pod IPs are ephemeral, Kubernetes provides Services to give stable network identities and load balancing for groups of pods. When you create a cluster you also define a Service CIDR (example: 10.100.0.0/16). Each Service receives a stable ClusterIP from the Service CIDR (for example, 10.100.0.1). Client pods send traffic to that ClusterIP and the Service load-balances traffic to the current backend pod endpoints.

<Frame>
  <img alt="A diagram of the Kubernetes networking model showing a frontend pod and three backend pods (IPs 172.16.0.1, .4, .5, .6) all accessed via a ClusterIP service (10.100.0.1) with POD CIDR 172.16.0.0/16 and Service CIDR 10.100.0.0/16. It also shows kube-proxy, traffic flow to the backend service, and a table mapping the service to the pod IPs." />
</Frame>

How a ClusterIP reaches backend pods in practice:

* kube-proxy runs on every node and watches Service and Endpoint objects.
* kube-proxy programs iptables or IPVS rules so that traffic sent to a Service IP is redirected to one of the backend pod IPs.
* Some CNIs (including eBPF-based ones like Cilium) can replace or augment kube-proxy and implement service handling more efficiently.

## NetworkPolicy: declare who can talk to whom

By default, Kubernetes networking is permissive: any pod can reach any other pod. For production workloads you usually want to restrict traffic between pods and across tiers. Kubernetes NetworkPolicy is the declarative API for expressing these restrictions. Enforcement, however, is performed by the cluster’s CNI implementation.

<Frame>
  <img alt="A slide titled &#x22;Kubernetes Networking Model – Network Policy&#x22; showing frontend and backend pods (IPs 172.16.0.3 and 172.16.0.4) and a database pod (172.16.0.5) with a network policy that permits traffic to the database on port 5436 only from the backend pod." />
</Frame>

<Callout icon="lightbulb">
  Kubernetes defines the NetworkPolicy API, but enforcement depends on the cluster’s CNI plugin. If the CNI does not implement NetworkPolicy semantics, the policies will not be enforced.
</Callout>

## Kubernetes does not ship full data-plane networking

Kubernetes itself does not provide pod IP allocation, overlay routing, or NetworkPolicy enforcement. If you create a cluster without installing a CNI plugin, pods will not receive Pod CIDR IPs and pod-to-pod communication will not function. The only networking component included in upstream Kubernetes is kube-proxy; everything else (IP allocation, routing/overlays, service handling integrations, and policy enforcement) is delivered by a third‑party CNI.

<Frame>
  <img alt="A slide titled &#x22;Kubernetes Networking Model&#x22; showing a central Kubernetes icon labeled &#x22;Kubernetes Limitations&#x22; with three connected teal bars listing &#x22;No IP address assignment,&#x22; &#x22;Communication barriers,&#x22; and &#x22;Non-functional network policies.&#x22;" />
</Frame>

<Callout icon="warning">
  If a cluster is created without a conformant CNI plugin, pods will not get IP addresses from a Pod CIDR and cluster networking (including NetworkPolicy enforcement) will not work.
</Callout>

## Choose a conformant CNI plugin

You don’t need to build networking yourself. Install a conformant CNI plugin to provide:

* Pod IP allocation and routing (overlay or routing-based).
* Service integration or kube-proxy replacement (iptables/IPVS or CNI-native service handling).
* NetworkPolicy enforcement.

Popular CNIs include:

* Cilium — eBPF-based, advanced network and security features: [https://cilium.io/](https://cilium.io/)
* Calico — policy and routing features: [https://projectcalico.org/](https://projectcalico.org/)
* Flannel — simple overlay networking: [https://github.com/flannel-io/flannel](https://github.com/flannel-io/flannel)

<Frame>
  <img alt="A diagram titled &#x22;Kubernetes Networking Model - CNI&#x22; showing a Kubernetes pod on the left connected to a vertical Container Network Interface (CNI) component in the center, which in turn links to several CNI plugins/logos on the right." />
</Frame>

## Quick reference

| Resource / Component | Purpose                                                     | Example / Notes                        |
| -------------------- | ----------------------------------------------------------- | -------------------------------------- |
| Pod CIDR             | IP address pool for pods                                    | 172.16.0.0/16                          |
| Service CIDR         | IP range for ClusterIP services                             | 10.100.0.0/16                          |
| kube-proxy           | Implements Services (iptables/IPVS) on nodes                | Can be replaced/augmented by some CNIs |
| NetworkPolicy        | Declarative access control for pods                         | Enforcement depends on CNI             |
| CNI plugin           | Provides pod IP allocation, routing, and policy enforcement | Cilium, Calico, Flannel                |

## Summary

* Pod CIDR: where pods receive their IP addresses.
* Service CIDR + kube-proxy (or CNI alternatives): provide stable ClusterIPs and load balancing.
* NetworkPolicy: expresses network access control but must be enforced by the CNI.
* Kubernetes requires a conformant CNI plugin to enable pod networking and policy enforcement—choose a plugin (Cilium, Calico, Flannel, etc.) that meets your networking and security requirements.

With this foundation you’ll be better prepared to understand what Cilium implements and which parts of Kubernetes networking it replaces or augments.

## Links and references

* [Kubernetes Networking Concepts](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
* [CNI Project Specification](https://github.com/containernetworking/cni)
* [Cilium — eBPF-powered Networking & Security](https://cilium.io/)
* [Calico](https://projectcalico.org/)
* [Flannel](https://github.com/flannel-io/flannel)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/9c9fa5ec-2721-4654-9383-5cb9b264e8b6/lesson/1dd04108-4f90-43e9-9358-976fec112d91" />
</CardGroup>
