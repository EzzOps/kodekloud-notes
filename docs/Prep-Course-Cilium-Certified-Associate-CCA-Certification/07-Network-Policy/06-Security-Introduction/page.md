# Set these variables appropriately
CILIUM_NAMESPACE=kube-system
CILIUM_POD=<cilium-agent-pod-name>
ENDPOINT=<endpoint-id>

kubectl -n "$CILIUM_NAMESPACE" exec "$CILIUM_POD" -c cilium-agent -- \
  cilium-dbg endpoint config "$ENDPOINT" PolicyAuditMode=Enabled
```

Inspecting audited flows with Hubble
After enabling audit mode (globally or per-endpoint), use Hubble to observe flows and policy verdicts. Audited (would-be denied) traffic is labeled with a policy verdict of "none" and the text "INGRESS AUDITED". Allowed traffic will show the appropriate allowed verdict and "INGRESS ALLOWED".

Example: frontend -> db (audited, would be denied)

```bash theme={null}
kubectl -n kube-system exec cilium-pvq7s -- hubble observe flows -t policy-verdict --last 1
# Jun  3 06:57:16.456: default/frontend-5f44ddcfd6-lbvlz:35256 (ID:6443) -> default/db-584f4c666-wjfkq:80 (ID:6942) policy-verdict:none INGRESS AUDITED (TCP Flags: SYN)
```

Example: backend -> db (allowed by policy)

```bash theme={null}
kubectl -n kube-system exec cilium-pvq7s -- hubble observe flows -t policy-verdict --last 1
# Jun  3 07:00:52.959: default/backend-7d965dd744-gvpmt:53198 (ID:7661) -> default/db-584f4c666-wjfkq:80 (ID:6942) policy-verdict:L3-Only INGRESS ALLOWED (TCP Flags: SYN)
```

<Callout icon="lightbulb">
  Policy audit mode is ideal for testing and validating network policies safely. Use it to identify unexpected denies and tune your rules before switching to enforcement.
</Callout>

<Callout icon="warning">
  Audit mode does not provide network isolation or enforce security controls. Do not rely on audit mode for protection — enable policy enforcement only after you have validated the behavior.
</Callout>

Links and references

* Cilium Helm chart values: [https://docs.cilium.io/en/stable/gettingstarted/helm/](https://docs.cilium.io/en/stable/gettingstarted/helm/)
* cilium-dbg tool: [https://docs.cilium.io/en/stable/tools/cilium-dbg/](https://docs.cilium.io/en/stable/tools/cilium-dbg/)
* Hubble (observability): [https://docs.cilium.io/en/stable/gettingstarted/hubble/](https://docs.cilium.io/en/stable/gettingstarted/hubble/)
* Cilium documentation: [https://docs.cilium.io/](https://docs.cilium.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/bf652c52-bb30-4bcc-9d18-c703f7b3e88a/lesson/8cb4e165-c24d-4539-b5f3-d76923682758" />
</CardGroup>


# Security Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Network-Policy/Security-Introduction/page

Guide to restricting Kubernetes pod communication using NetworkPolicy and Cilium's eBPF-based identity and L7 policies for least privilege enforcement.

This guide explains how to restrict which workloads can communicate inside a Kubernetes cluster using both the native Kubernetes NetworkPolicy API and Cilium’s enhanced policy primitives. By default, Kubernetes clusters permit pod-to-pod communication across the cluster. To adopt a least-privilege posture you must explicitly express which traffic is allowed — for example, preventing Pod 2 from talking to Pod 6. Cilium builds on Kubernetes NetworkPolicy with eBPF-powered enforcement, richer selectors, and L7 controls to make those restrictions more powerful and observable.

<Frame>
  <img alt="A slide titled &#x22;Security – Introduction&#x22; showing a Kubernetes cluster with two nodes (Node 1 and Node 2), each containing four pods (Pod 1–4 and Pod 5–8). A dashed line between the nodes ends at a red “X,” indicating inter-node communication is blocked or denied." />
</Frame>

What this page covers:

* Kubernetes NetworkPolicy — the native API for expressing allowed traffic between pods, namespaces, and IP blocks.
* Cilium NetworkPolicy (CNP) and Clusterwide CiliumNetworkPolicy (CCNP) — Cilium’s extended, eBPF-based policy types that add identity-based selectors, richer L7 rules, and cluster-scoped enforcement.

<Callout icon="lightbulb">
  Kubernetes NetworkPolicy is opt-in: if no policies select a pod, that pod remains reachable by other pods. When a pod is selected by one or more NetworkPolicy resources, traffic is restricted according to those policies, allowing you to adopt a least-privilege model for the selected pods.
</Callout>

Why use Cilium for network security

* Kernel-level enforcement with eBPF for high performance and precise policy enforcement (including inter-node traffic).
* Identity-based policies using labels (and integrating with external identity providers) rather than relying solely on IP addresses, which improves policy stability as pods move.
* L7 filtering and visibility (HTTP, gRPC, Kafka, DNS, etc.) so you can write policies based on HTTP paths, methods, or Kafka topics, not just ports.
* Both namespace-scoped (`CiliumNetworkPolicy`, CNP) and cluster-scoped (`CiliumClusterwideNetworkPolicy`, CCNP) objects to express either granular or broad policies.

Policy type comparison

| Resource Type                                  | Scope                                   | Use Case                                                                     | Example CLI                           |
| ---------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------- |
| Kubernetes `NetworkPolicy`                     | Namespace-scoped                        | Allow/deny traffic based on pod selectors, namespace selectors, and IPBlocks | `kubectl apply -f networkpolicy.yaml` |
| Cilium `CiliumNetworkPolicy` (CNP)             | Namespace-scoped with Cilium extensions | Identity-based policies, L7 rules, richer match semantics                    | `kubectl apply -f cnp.yaml`           |
| Cilium `CiliumClusterwideNetworkPolicy` (CCNP) | Cluster-scoped                          | Apply consistent policies across namespaces or the whole cluster             | `kubectl apply -f ccnp.yaml`          |

Authoring tips

* Start with a default deny for critical workloads, then add explicit allow rules for required traffic.
* Use label-based selectors (identities) where possible so policies remain correct as IPs change.
* Combine L4 (ports/protocols) and L7 filters (HTTP methods, paths) to enforce intent at the application layer.
* Test policies incrementally in a staging environment and use observability tools (Cilium Hubble, cilium monitor) to validate enforcement.

Next sections (in this guide) show:

* Example `NetworkPolicy` YAML and how it behaves in a cluster.
* Example `CiliumNetworkPolicy` and `CiliumClusterwideNetworkPolicy` demonstrating identity-based and L7 rules.
* How Cilium enforces policies at the eBPF level (including inter-node enforcement as illustrated above).
* Techniques to implement and verify a least-privilege network posture.

Links and references

* [Kubernetes NetworkPolicy documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Cilium Network Policy concepts](https://docs.cilium.io/en/stable/policy/)
* [Cilium Hubble observability](https://docs.cilium.io/en/stable/gettingstarted/hubble/)

<Callout icon="lightbulb">
  Tip: Use `kubectl describe` and Cilium’s `hubble` tools to observe which policy matches traffic during testing. This helps iterate policies without risking production outages.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/bf652c52-bb30-4bcc-9d18-c703f7b3e88a/lesson/f6656d91-c2cc-4aaf-ae72-f6cb30fd1d35" />
</CardGroup>
