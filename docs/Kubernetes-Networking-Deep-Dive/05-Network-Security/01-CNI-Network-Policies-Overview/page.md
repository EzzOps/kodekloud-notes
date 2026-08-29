# CNI Network Policies Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Network-Security/CNI-Network-Policies-Overview/page

This article provides an overview of CNI network policies in Kubernetes, detailing their benefits, enforcement modes, and examples for traffic control and security.

## Recap of Kubernetes Network Policies

By default, Kubernetes pods communicate without restrictions, which can expose applications to unintended traffic flows. Implementing network policies allows you to explicitly permit or deny traffic between:

* Pod-to-Pod
* Pod-to-Service
* Pod-to-Namespace

> **lightbulb** Network policies enhance cluster security by defining clear ingress and egress rules. Always start with a default deny posture in production.

![The image is a slide titled "Network Policies Recap," summarizing key points about network policies in Kubernetes, including traffic control, communication restrictions, and security enhancements.](https://kodekloud.com/kk-media/image/upload/v1752880384/notes-assets/images/Kubernetes-Networking-Deep-Dive-CNI-Network-Policies-Overview/network-policies-recap-kubernetes-summary.jpg)

## Built-In vs. CNI-Specific Network Policies

Kubernetes ships with basic network policy support, but many CNI plugins extend capabilities with advanced features:

| Feature                        | Built-In Policy | CNI Plugin Extensions               |
| ------------------------------ | --------------- | ----------------------------------- |
| Layer 7 Filtering              | ✖️              | ✅ HTTP, gRPC, Kafka rules           |
| Encryption & Segmentation      | ✖️              | ✅ mTLS, IPsec                       |
| Rate Limiting & Whitelisting   | ✖️              | ✅ IP whitelisting/blacklisting, QoS |
| Traffic Monitoring & Analytics | Limited         | ✅ Real-time metrics & logs          |
| Multi-Cluster Policy Scope     | ✖️              | ✅ Global policy management          |

![The image is an overview of CNI (Container Network Interface) network policies, illustrating a Kubernetes cluster with nodes and an external network, highlighting features like network segmentation, encryption, and enhanced security. It also mentions projects like Calico, Cilium, and Weave Net.](https://kodekloud.com/kk-media/image/upload/v1752880384/notes-assets/images/Kubernetes-Networking-Deep-Dive-CNI-Network-Policies-Overview/cni-network-policies-kubernetes-overview.jpg)

## Key Benefits of CNI Network Policies

| Benefit                  | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| Advanced Traffic Control | Fine-grained L3–L7 rules across pods, nodes, external targets |
| Enhanced Security        | Intrusion detection, IP whitelisting, rate limiting           |
| Performance Optimization | Low-latency, high-throughput networking                       |
| Extended Scope           | Policy enforcement beyond cluster boundaries                  |
| Customization            | Organization-specific rule definitions                        |
| Segmentation & QoS       | Network isolation plus traffic prioritization                 |
| Real-Time Monitoring     | Anomaly detection and live metrics                            |

## Cilium: Our CNI of Choice

Cilium leverages eBPF for efficient enforcement of Layer 3, 4, and 7 policies with minimal performance overhead:

* Layer 7 Visibility (HTTP, gRPC, Kafka)
* Protocol-Aware Filtering (methods, paths, headers)
* Service Mesh Integrations ([Istio](https://istio.io), [Linkerd](https://linkerd.io))
* Multi-Cluster Policy Consistency
* Rich eBPF-Powered Troubleshooting & Metrics

![The image is an informational graphic about Cilium Network Policies, highlighting protocol support (HTTP, gRPC, Kafka), layered controls (L3/L4 and L7), and extensive integrations. It features the Cilium logo.](https://kodekloud.com/kk-media/image/upload/v1752880385/notes-assets/images/Kubernetes-Networking-Deep-Dive-CNI-Network-Policies-Overview/cilium-network-policies-protocols-graphic.jpg)

## Policy Enforcement Modes

Cilium follows a whitelist model. Traffic is dropped by default unless permitted by one of these modes:

* **Ingress Policies:** Allow traffic into pods based on source IPs, ports, or L7 rules
* **Egress Policies:** Allow pods to initiate traffic to specified destinations
* **Default Deny:** Any traffic not explicitly allowed will be blocked

## Rule Structure

Every Cilium policy uses an endpoint selector to target pods via labels:

```yaml theme={null}
endpointSelector:
  matchLabels:
    app: myapp
```

Subsequent rule sections can include:

* `fromEndpoints` / `toEndpoints`: Label selectors for source/destination pods
* `ports` & `protocols`: Restrict to TCP/UDP ports
* Layer 7 rules: HTTP methods, paths, headers
* CIDR blocks: Allow or exclude specific IP ranges

![The image explains two rule basics: "Layer 7 Rules," which define policies based on application layer parameters like HTTP methods and paths, and "CIDR Blocks," which control traffic to/from specific IP ranges for network integration.](https://kodekloud.com/kk-media/image/upload/v1752880386/notes-assets/images/Kubernetes-Networking-Deep-Dive-CNI-Network-Policies-Overview/layer-7-rules-cidr-blocks-explained.jpg)

### Example: Comprehensive CiliumNetworkPolicy (L3–L7)

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "example-policy"
spec:
  endpointSelector:
    matchLabels:
      app: myapp
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
          rules:
            http:
              - method: "GET"
                path: "/public"
  egress:
    - toEndpoints:
        - matchLabels:
            app: database
      toPorts:
        - ports:
            - port: "3306"
              protocol: TCP
```

* **Ingress:** Only HTTP GET on `/public` from pods with `app=frontend`.
* **Egress:** Only TCP port 3306 to pods with `app=database`.

***

## Layer 3 Policies

Layer 3 policies define network-layer connectivity without deep packet inspection:

* **Endpoints-based:** Select pods by labels
* **Entities-based:** Match built-in identities like `host` or `world`
* **DNS-based:** Use runtime-resolved DNS names (honoring TTLs)

![The image shows a list of Layer 3 policies alongside a diagram of the OSI Model layers, highlighting the Network layer.](https://kodekloud.com/kk-media/image/upload/v1752880387/notes-assets/images/Kubernetes-Networking-Deep-Dive-CNI-Network-Policies-Overview/layer-3-policies-osi-model-diagram.jpg)

### Examples

```yaml theme={null}
