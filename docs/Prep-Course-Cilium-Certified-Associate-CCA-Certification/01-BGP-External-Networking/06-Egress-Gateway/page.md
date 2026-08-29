# Egress Gateway

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/BGP-External-Networking/Egress-Gateway/page

Describes using Cilium egress gateway to route selected pod outbound traffic through designated nodes, SNATing to fixed egress IPs for compliance and centralized logging

In this lesson we explain how egress gateway changes Kubernetes' default behavior for outbound pod traffic, why you would use it, and how to enable and validate it with Cilium.

By default, when a pod sends traffic to an external IP (for example 8.8.8.8), the node that forwards the packet performs source NAT (SNAT). The external service therefore sees the node's IP as the source, not the pod IP. The node tracks the connection so it can reverse NAT (DNAT) responses back to the originating pod.

<Frame>
  <img alt="A diagram titled &#x22;Kubernetes Source NAT&#x22; showing a cluster with three nodes and pods (10.0.0.1–10.0.0.3). It illustrates a pod on Node1 sending a request to external IP 8.8.8.8 that is source-NATed to the node IP 192.168.1.1." />
</Frame>

The important point: by default external services always see traffic originating from node IPs (because nodes perform SNAT).

Egress gateway changes this default by routing selected pod traffic through a designated egress node (or nodes). Matching traffic is routed—typically encapsulated over the cluster overlay (VXLAN, Geneve, etc.)—to the chosen egress node. That node then SNATs to a configured egress IP and sends the traffic to the external destination. Responses return to the egress node and are reverse-translated and forwarded back to the source pod.

<Frame>
  <img alt="A diagram titled &#x22;Egress Gateway&#x22; showing a Kubernetes cluster with three nodes and pods (10.0.0.1–10.0.0.3) and node IPs 192.168.1.1–.3. It illustrates pod traffic (e.g., 10.0.0.2) going to external IP 8.8.8.8 routed through an EgressGateway on Node3." />
</Frame>

Common use cases for an egress gateway:

* Enforce outbound traffic routing through a fixed public IP for compliance or firewall whitelisting.
* Centralize audit or logging for outbound connections.
* Apply consistent network policy or inspection at a single egress point.

You can select which node(s) act as gateway(s) and choose the SNAT IP used by the egress node. The egress IP must be configured on an interface of the selected node (it does not have to be the default external interface, but it must exist on the node).

<Frame>
  <img alt="A diagram titled &#x22;Egress Gateway Configuration&#x22; showing a Kubernetes cluster with three nodes (192.168.1.1, 192.168.1.2, 192.168.1.3) containing two pods (10.0.0.1 labeled app1 and 10.0.0.2 labeled app2). Two external egress gateways (4.1.1.1 and 5.1.1.1) are illustrated above the cluster." />
</Frame>

## Enabling Egress Gateway (Cilium)

To use egress gateway with Cilium, enable the required features in your Cilium configuration (Helm values or cilium-config) and then restart the operator and agents.

Required settings:

* bpf.masquerade: true — enables SNAT support.
* kubeProxyReplacement: true — egress gateway requires Cilium’s kube-proxy replacement.
* egressGateway.enabled: true — turns on the egress gateway feature.

Example Helm/values YAML:

```yaml theme={null}
bpf:
  masquerade: true

kubeProxyReplacement: true

egressGateway:
  # Enables egress gateway to redirect and SNAT traffic that leaves the cluster.
  enabled: true
```

> **lightbulb** After changing Cilium configuration, restart the Cilium operator and agents so the new settings are applied cluster-wide.

> **warning** The egressIP you configure in a CiliumEgressGatewayPolicy must exist on an interface of the egress node. If the IP is not present, SNAT will fail and outbound traffic will not be translated correctly.

## Creating a Cilium Egress Gateway Policy

A CiliumEgressGatewayPolicy specifies:

* Which pods are affected (selectors).
* Which destination CIDRs should be routed via the egress gateway.
* Which node(s) will act as gateways.
* The egress IP used for SNAT on the gateway node.

Example policy: pods labeled app: app1 will use node3 as the egress and be SNATed to 192.168.1.3 for destinations in 4.0.0.0/8.

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumEgressGatewayPolicy
metadata:
  name: egress-sample
spec:
  selectors:
    - podSelector:
        matchLabels:
          app: app1
  destinationCIDRs:
    - "4.0.0.0/8"
  egressGateway:
    # Select the node that will act as the gateway for this policy.
    nodeSelector:
      matchLabels:
        node.kubernetes.io/name: node3
    # IP address used to SNAT matched traffic. This IP must exist on the selected node.
    egressIP: 192.168.1.3
```

Notes:

* destinationCIDRs: the outbound destination ranges for which traffic will be forced through the egress node.
* selectors: which source pods (by label) will have their egress affected.
* egressIP: address to SNAT to; must be present on the node.

When applied, app: app1 pods communicating with IPs in 4.0.0.0/8 will be encapsulated to node3, SNATed to 192.168.1.3 on node3, and sent to the external destination. Other pods or destinations use the default per-node SNAT behavior.

## Verifying Egress Gateway Configuration

You can inspect the active egress routing and SNAT mapping using the Cilium debug tool from a Cilium pod (or from a node with cilium-dbg installed):

```bash theme={null}
kubectl -n kube-system exec ds/cilium -- cilium-dbg bpf egress list
```

Sample output:

```text theme={null}
Source IP    Destination CIDR    Egress IP         Gateway IP
10.0.1.93    0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.1.151   0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.1.250   0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.2.23    0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.2.32    0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.2.91    0.0.0.0/0           192.168.44.128    192.168.44.128
```

Column meanings:

| Column           | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| Source IP        | Pod IP that matches an egress policy                       |
| Destination CIDR | The destination range for which the policy applies         |
| Egress IP        | IP address used to SNAT traffic when it leaves the cluster |
| Gateway IP       | Internal IP of the node acting as the egress gateway       |

Note: Egress IP and Gateway IP can be the same or different. The Egress IP is what external services see as the source; Gateway IP identifies the egress node inside the cluster.

## When to use an egress gateway

* You need fixed public IPs for outbound traffic for firewall whitelisting or cloud NAT compatibility.
* You require centralized egress inspection, logging, or compliance controls.
* You want predictable network paths for auditability or troubleshooting.

## Links and References

* [Cilium Egress Gateway Documentation](https://docs.cilium.io/en/stable/policy/egress/)
* [Cilium kube-proxy replacement](https://docs.cilium.io/en/stable/policy/kube-proxy/)
* [Kubernetes Networking Concepts](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
* [Understanding SNAT and DNAT](https://en.wikipedia.org/wiki/Network_address_translation)

If you want to force traffic from selected pods to egress via a particular node (for compliance, fixed public IPs, audit logging, or firewall rules), apply a CiliumEgressGatewayPolicy as shown above.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/867bdf6b-2e01-46bd-844e-a770f3563f60)
