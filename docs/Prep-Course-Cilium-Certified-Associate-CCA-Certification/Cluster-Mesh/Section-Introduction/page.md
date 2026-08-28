# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cluster-Mesh/Section-Introduction/page

Guide to using Cluster Mesh for multi-cluster Kubernetes networking, enabling cross-cluster connectivity, load balancing, and inter-cluster network policies with security best practices

In this lesson we'll focus on managing multiple Kubernetes clusters using Cluster Mesh. Cluster Mesh provides multi-cluster networking, cross-cluster connectivity, and consistent security controls across a set of clusters. This enables pods and applications in different clusters to discover, reach, and securely communicate with each other while preserving local autonomy for workloads and policies.

What you'll learn in this lesson:

* What Cluster Mesh is and how it connects clusters.
* How to enable cross-cluster connectivity so pods and applications can communicate across clusters.
* How to load balance traffic across multiple—or all—clusters.
* How to configure inter-cluster network policies to control which clusters (or pods from which clusters) are allowed to talk to which other clusters.

<Frame>
  <img alt="A presentation slide titled &#x22;Agenda&#x22; with a turquoise left panel and three numbered items on the right. The items cover connecting pods/applications across clusters, load-balancing traffic to multiple clusters, and configuring network policies to restrict inter-cluster communication." />
</Frame>

Cluster Mesh supports a range of multi-cluster design patterns depending on your goals:

* Full-mesh connectivity: every pod in every cluster can reach every other pod.
* Hub-and-spoke (or federated) topologies: a subset of clusters act as aggregation points.
* Selective connectivity: only specific clusters, namespaces, or services are permitted to communicate.
* Geo-aware load distribution: direct traffic to nearest or healthiest cluster.

<Callout icon="lightbulb">
  Cluster Mesh lets you treat multiple clusters as a cohesive network domain while still enforcing cluster-local policies. Use selective connectivity to reduce attack surface and control egress/ingress paths between clusters.
</Callout>

Table — Key topics and practical examples

| Topic                          | Purpose                                                           | Practical example                                                                                |
| ------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Cross-cluster connectivity     | Enable pod-to-pod and service-to-service communication            | Expose a central database in Cluster A to app pods in Cluster B using secure tunnels             |
| Load balancing across clusters | Distribute traffic across clusters for resilience and locality    | Route user requests to the nearest healthy cluster or balance traffic evenly across all clusters |
| Inter-cluster network policies | Enforce which clusters/namespaces/services may talk to each other | Restrict a sensitive service so only pods from Cluster X can connect                             |

Security and policy are critical considerations when enabling multi-cluster networking. Misconfigured connectivity can expose sensitive services or cause unintended lateral movement between clusters.

<Callout icon="warning">
  Always enforce least privilege when authorizing inter-cluster traffic. Combine network policies with identity and TLS controls to limit which workloads can communicate across clusters.
</Callout>

Recommended references

* [Kubernetes Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
* [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Cilium Cluster Mesh (multi-cluster) documentation](https://docs.cilium.io/en/stable/gettingstarted/multicluster/)

In the following sections we will step through how Cluster Mesh establishes connections, how service and traffic distribution work across clusters, and how to enforce inter-cluster network policies with concrete configuration examples and patterns.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b8be180f-1719-47ca-b26e-7bf942694abf/lesson/88070f8d-475f-41f1-bbd5-cef9218b1a65" />
</CardGroup>
