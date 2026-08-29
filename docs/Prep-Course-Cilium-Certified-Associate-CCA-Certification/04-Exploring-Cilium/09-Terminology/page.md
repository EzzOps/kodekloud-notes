# Terminology

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Exploring-Cilium/Terminology/page

Explains Cilium networking terms including endpoints and identities and how identity based policies replace brittle IP based policies for Kubernetes Pod security and observability

In this lesson we define key Cilium terms used throughout the architecture and internal operation of Cilium. These definitions are intentionally consistent so you can reliably map concepts (for example, policies and identities) to everyday Kubernetes objects such as Pods.

## Endpoint

An endpoint in Cilium represents a network identity for which Cilium enforces network policy. In Kubernetes, each Pod receives its own IP address, so you can practically treat a Pod as a Cilium endpoint. Cilium generalizes this by stating “every IP address is an endpoint” to support non‑Kubernetes deployments.

Cilium assigns each endpoint a unique numeric ID that the agent uses internally to manage that endpoint (for example, Pod1 → Endpoint ID 100, Pod2 → Endpoint ID 200).

<Frame>
  <img alt="A diagram titled &#x22;Cilium Endpoint&#x22; showing four pods (POD1–POD4) with pod icons, IPs (172.16.1.1, .20, .30, .40), Endpoint buttons and IDs (100, 200, 300, 400). Below them is a long bar labeled &#x22;Cilium Operator.&#x22;" />
</Frame>

To inspect endpoints from a node’s Cilium agent, exec into the Cilium agent Pod and run `cilium endpoint list`:

```bash theme={null}
kubectl exec -n kube-system cilium-cfkzf -- cilium endpoint list
```

Example (trimmed) output:

```bash theme={null}
ENDPOINT   POLICY (ingress)   POLICY (egress)   IDENTITY   LABELS (source:key[=value])                               IPv6       IPv4         STATUS
ENFORCEMENT ENFORCEMENT
659        Disabled          Disabled          589        k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
                                           k8s:io.cilium.k8s.policy.cluster=default
                                           k8s:io.cilium.k8s.policy.serviceaccount=default
                                           k8s:io.kubernetes.pod.namespace=default
                                           k8s:run=nginx                                                      10.0.2.163  ready

1037       Disabled          Disabled          28075      k8s:app=tshoot
                                           k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
                                           k8s:io.cilium.k8s.policy.cluster=default
                                           k8s:io.cilium.k8s.policy.serviceaccount=default
                                           k8s:io.kubernetes.pod.namespace=default                              10.0.2.244  ready
```

This listing shows per-endpoint numeric ID, identity, labels, IP address, and status. In day-to-day Kubernetes troubleshooting you can think of an endpoint as the corresponding Pod.

> **lightbulb** Remember: in Kubernetes, a Pod’s IP ≈ Cilium endpoint for practical policy and observability tasks. Use `cilium endpoint list` to map Pod IPs to Cilium endpoint IDs.

## IP-based policy limitations

Traditional network policies are often IP-based: they allow or deny traffic by matching source/destination IPs. This approach presents operational challenges in dynamic environments (Kubernetes autoscaling, rolling updates, etc.):

* Adding or removing Pods requires updating IP allowlists.
* Rule changes must be propagated to all nodes, which is costly at scale.
* Convergence delays can temporarily block legitimate traffic or allow unintended access.

For example, if backend 172.16.1.100 should only accept traffic from frontend 172.16.1.1, that mapping must be updated whenever frontends or backends change.

<Frame>
  <img alt="A slide titled &#x22;IP-Based Policies – Limitations&#x22; showing two frontend pods (172.16.1.20, 172.16.1.1) and two backend pods (172.16.1.100, 172.16.1.101). It states &#x22;Allow traffic only from the frontend; deny all others&#x22; and includes a table mapping allowed frontend sources to backend destinations." />
</Frame>

## Cilium identities

Cilium addresses IP volatility by decoupling policy from IP addresses: it assigns stable numeric identities to sets of endpoints that share the same semantic labels (for example, role=frontend). Policies are written against these identities rather than raw IPs, so they remain valid when pods scale or move.

<Frame>
  <img alt="A slide titled &#x22;Cilium Identities&#x22; showing three connected blocks — Security, Identity, and Networking (IP) — each with a colored icon and arrows indicating a left-to-right flow." />
</Frame>

Benefits:

* Identities remain stable across Pod lifecycle events.
* Security policies are decoupled from changing network addresses, simplifying enforcement and scaling.

<Frame>
  <img alt="A slide titled &#x22;Cilium Identities&#x22; showing two colored cards. The left card reads &#x22;Consistent & Scalable — Identities stable throughout the pod's lifecycle,&#x22; and the right card reads &#x22;Decouples Security from IPs — No reliance on changing network addresses.&#x22;" />
</Frame>

How identities are derived

* In Kubernetes, identities are derived from Pod labels (and other label sources).
* All Pods that share the same set of labels are mapped to the same numeric identity.
* Policies reference identities like role=frontend or role=backend, not IP addresses.

Example Pod manifests:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  labels:
    role: frontend
spec:
  containers:
    - name: pod1
      image: pod1
```

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: backend
  labels:
    role: backend
spec:
  containers:
    - name: pod1
      image: pod1
```

All Pods labeled role=backend share the same identity; likewise for role=frontend. A policy such as “allow traffic from frontend to backend” targets identities, so it remains unchanged as Pods are created or deleted.

Note: labels may come from Kubernetes, the container runtime, or reserved/internal sources.

## Verifying identities

To list identities known by a Cilium agent:

```bash theme={null}
kubectl exec -n kube-system cilium-cfkzf -- cilium identity list
```

Example output:

```bash theme={null}
18938    k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
         k8s:io.cilium.k8s.policy.cluster=default
         k8s:io.cilium.k8s.policy.serviceaccount=default
         k8s:io.kubernetes.pod.namespace=default
         k8s:role=backend

32563    k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
         k8s:io.cilium.k8s.policy.cluster=default
         k8s:io.cilium.k8s.policy.serviceaccount=default
         k8s:io.kubernetes.pod.namespace=default
         k8s:role=frontend
```

Each identity row shows a numeric ID and the set of labels (the `k8s:` prefix indicates Kubernetes‑origin labels).

You can correlate endpoints to identities using `cilium endpoint list`:

```bash theme={null}
kubectl exec -n kube-system cilium-cfkzf -- cilium endpoint list
```

Trimmed example:

```bash theme={null}
ENDPOINT   POLICY (ingress)   POLICY (egress)   IDENTITY   LABELS (source:key[=value])                               IPv6       IPv4         STATUS
           ENFORCEMENT        ENFORCEMENT
162        Disabled           Disabled           18938      k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
                                                     k8s:io.cilium.k8s.policy.cluster=default
                                                     k8s:io.cilium.k8s.policy.serviceaccount=default
                                                     k8s:io.kubernetes.pod.namespace=default
                                                     k8s:role=backend                                         10.0.2.161   ready

476        Disabled           Disabled           32563      k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
                                                     k8s:io.cilium.k8s.policy.cluster=default
                                                     k8s:io.cilium.k8s.policy.serviceaccount=default
                                                     k8s:io.kubernetes.pod.namespace=default
                                                     k8s:role=frontend                                       10.0.2.76    ready

2757       Disabled           Disabled           32563      k8s:io.cilium.k8s.namespace.labels.kubernetes.io/metadata.name=default
                                                     k8s:io.cilium.k8s.policy.cluster=default
                                                     k8s:io.cilium.k8s.policy.serviceaccount=default
                                                     k8s:io.kubernetes.pod.namespace=default
                                                     k8s:role=frontend                                       10.0.2.195   ready
```

This output shows multiple endpoints (different Pod IPs) sharing the same identity (32563) because they have identical labels (role=frontend). Policies target identities, so scaling the frontend Pods does not require changing policies.

<Frame>
  <img alt="A slide titled &#x22;Verifying Identity&#x22; showing two rounded boxes: one labeled &#x22;container&#x22; with the text &#x22;Labels from the local container runtime&#x22; and the other labeled &#x22;k8s&#x22; with the text &#x22;Labels from Kubernetes.&#x22; A small green &#x22;reserved&#x22; tag and a KodeKloud copyright appear at the bottom." />
</Frame>

## Quick reference table

| Term            | What it means                                                                                                    | Practical example                                            |
| --------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Endpoint        | A network identity Cilium enforces policy for; in Kubernetes, usually a Pod (IP).                                | `cilium endpoint list` shows endpoint IDs mapped to Pod IPs. |
| Identity        | A stable numeric label assigned to a set of endpoints that share labels. Policies reference identities, not IPs. | `cilium identity list` shows identity → labels mappings.     |
| IP-based policy | Traditional approach matching source/destination IPs; brittle in dynamic clusters.                               | Requires updating allowlists as Pods scale or restart.       |

## Links and references

* [Cilium Documentation](https://cilium.io/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Cilium GitHub](https://github.com/cilium/cilium)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/0807e400-fd1b-4f25-bba5-d0fdb0f4e3f2/lesson/ff323637-70bb-4f69-9355-c99fc739505c)
