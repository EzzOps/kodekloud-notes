# Network Policies Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Container-Network-InterfaceCNI/Network-Policies-Overview/page

Kubernetes Network Policies define rules for pod communication, enhancing security by controlling traffic between pods, namespaces, and external sources.

Kubernetes pods communicate freely by default, which simplifies development but poses risks in production. Network Policies close this gap by defining fine-grained rules for pod-to-pod, namespace, and external traffic. Think of them as traffic signs in your cluster that explicitly allow or deny connections.

<Frame>
  ![The image illustrates a network policy concept, showing a connection from one pod to a network policy, which blocks access to another pod.](https://kodekloud.com/kk-media/image/upload/v1752880284/notes-assets/images/Kubernetes-Networking-Deep-Dive-Network-Policies-Overview/network-policy-pod-connection-illustration.jpg)
</Frame>

## Key Entity Types

Network Policies match traffic based on three entities:

| Entity Type | Selector Key      | Description                        |
| ----------- | ----------------- | ---------------------------------- |
| Other Pods  | podSelector       | Select pods by labels              |
| Namespaces  | namespaceSelector | Select namespaces by labels        |
| IP Blocks   | ipBlock           | Specify CIDR ranges and exclusions |

<Frame>
  ![The image is a diagram titled "Network Policies" showing three entities: Other Pods (podSelector), Namespaces (namespaceSelector), and IP Blocks (ipBlock).](https://kodekloud.com/kk-media/image/upload/v1752880285/notes-assets/images/Kubernetes-Networking-Deep-Dive-Network-Policies-Overview/network-policies-pod-selector-diagram.jpg)
</Frame>

## Defining a NetworkPolicy

A `NetworkPolicy` is a namespaced resource that applies to pods matching `podSelector`. You must also declare `policyTypes` (Ingress, Egress, or both) and the corresponding rules:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: app1
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              team: frontend
        - podSelector:
            matchLabels:
              app: app2
  egress:
    - to:
        - ipBlock:
            cidr: 10.0.0.0/24
```

<Callout icon="lightbulb">
  Network Policies only take effect when a CNI plugin that supports them is installed (e.g., [Calico](https://projectcalico.org), [Cilium](https://cilium.io)).
</Callout>

### Entity Selectors and IP Blocks

Use label selectors for pods and namespaces:

```yaml theme={null}
