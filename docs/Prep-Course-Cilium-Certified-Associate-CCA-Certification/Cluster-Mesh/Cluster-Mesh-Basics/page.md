# Cluster Mesh Basics

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cluster-Mesh/Cluster-Mesh-Basics/page

Overview of Cilium Cluster Mesh features, setup steps, prerequisites, and KVStoreMesh scalability

In this lesson we cover Cluster Mesh fundamentals: what Cluster Mesh enables, required cluster prerequisites, how to configure and enable it in Cilium, how to connect clusters into a full mesh, and why KVStoreMesh improves Cluster Mesh scalability.

Cluster Mesh lets multiple Kubernetes clusters behave as a single multi-cluster network fabric by providing:

* Cross-cluster network connectivity (pods can talk across clusters).
* Cross-cluster load balancing (services can balance across backends in other clusters).
* Shared security controls (apply Kubernetes NetworkPolicies across clusters).

<Frame>
  <img alt="A slide titled &#x22;Cluster Mesh – Basics&#x22; showing a central &#x22;Cluster Mesh&#x22; node with arrows pointing to three features: Security, Network Connectivity, and Load Balancing. Each feature is represented by a blue circular icon connected to the central cluster." />
</Frame>

Example: with cluster1, cluster2, and cluster3 joined into a Cluster Mesh, pods in different clusters can communicate by default according to mesh-wide connectivity and network policies.

<Frame>
  <img alt="A slide titled &#x22;Cluster Mesh – Features&#x22; illustrating three Kubernetes clusters (Cluster 1, 2, 3) inside a dashed &#x22;Cluster Mesh&#x22; boundary, each containing frontend and backend pods to show connectivity across clusters." />
</Frame>

Cross-cluster load balancing lets a frontend pod in one cluster send requests that are distributed among backends across multiple clusters — useful for global-scale services and failover.

<Frame>
  <img alt="A slide titled &#x22;Cluster Mesh — Features&#x22; showing load balancing of traffic between three Kubernetes clusters. Each cluster contains frontend and backend pods and a central load balancer routes requests across the clusters." />
</Frame>

You can also enforce fine-grained cross-cluster access using Kubernetes NetworkPolicies. For example, allow frontend pods from cluster1 and cluster2 to reach a backend in cluster2 while blocking requests originating from cluster3.

<Frame>
  <img alt="A diagram titled &#x22;Cluster Mesh – Features&#x22; showing three Kubernetes clusters, each with frontend and backend pods. It illustrates network policies controlling inter-cluster communication, with some pod connections allowed (green) and others blocked (grey with an X)." />
</Frame>

These are the main features covered below: prerequisites, per-cluster configuration, enablement, cluster connections, and KVStoreMesh design.

***

## Prerequisites and requirements

Before joining clusters into a Cluster Mesh, verify the following requirements across all clusters:

| Requirement                       | Why it matters                                                                                                                                 |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Matching datapath mode            | All clusters should use the same datapath (e.g., encapsulation/tunnel or native routing) to avoid connectivity and routing mismatches.         |
| Non-overlapping Pod CIDRs         | Pods in different clusters must use unique IP ranges to prevent address conflicts.                                                             |
| Full node-to-node IP connectivity | Nodes across clusters must be able to reach each other (or through a suitable networking fabric) for cross-cluster traffic and service access. |
| Unique cluster identifiers        | Each cluster needs a unique cluster name and integer ID in Cilium configuration to avoid collisions.                                           |

When configuring Cilium per-cluster, ensure the Cilium config includes unique Pod CIDR pool entries and a unique cluster name and ID. A representative YAML fragment for two clusters:

```yaml theme={null}
