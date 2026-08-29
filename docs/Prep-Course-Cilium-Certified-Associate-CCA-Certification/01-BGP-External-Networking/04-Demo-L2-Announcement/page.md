# Upgrade helm release (example)
helm upgrade cilium cilium/cilium --namespace kube-system -f cilium-values.yaml

# Restart Cilium operator and agent
kubectl rollout restart deployment/cilium-operator -n kube-system
kubectl rollout restart daemonset/cilium -n kube-system
```

Create and apply a CiliumEgressGatewayPolicy

* Label the node(s) you want to act as egress gateway(s) and reference that label in the policy nodeSelector.
* Note: label values in YAML matchLabels must be strings. Quote boolean-like values (e.g., "true").

Label the chosen node (example)

```bash theme={null}
user1@control-plane:~$ kubectl label node worker2 egress=true
node/worker2 labeled
```

Confirm the label

```bash theme={null}
user1@control-plane:~$ kubectl get node --show-labels
NAME            STATUS   ROLES           AGE   VERSION   LABELS
control-plane   Ready    control-plane   37d   v1.32.3   ... 
worker1         Ready    <none>          37d   v1.32.3   ... 
worker2         Ready    <none>          37d   v1.32.3   ... egress=true,...
```

Example CiliumEgressGatewayPolicy (egress-gateway.yaml)

* This example selects pods with label app=app1, matches all destinations (0.0.0.0/0), and configures the node labeled egress: "true" to use egress IP 192.168.44.128.

```yaml theme={null}
apiVersion: cilium.io/v2
kind: CiliumEgressGatewayPolicy
metadata:
  name: egress-example
spec:
  selectors:
  - podSelector:
      matchLabels:
        app: app1
    destinationCIDRs:
    - "0.0.0.0/0"
  egressGateway:
    nodeSelector:
      matchLabels:
        egress: "true"
    egressIP: 192.168.44.128
```

Apply the policy

```bash theme={null}
user1@control-plane:~$ kubectl apply -f egress-gateway.yaml
ciliumegressgatewaypolicy.cilium.io/egress-example created
```

> **warning** When authoring CiliumEgressGatewayPolicy YAML, always quote label values (for example: egress: "true") so they are treated as strings. Also ensure your Cilium version supports the egress gateway feature and that kubeProxyReplacement and bpf.masquerade are enabled.

Verify Cilium BPF egress entries

* Check the BPF egress table from a Cilium agent pod to confirm source pods are mapped to the configured egress IP:

```bash theme={null}
user1@control-plane:~$ kubectl -n kube-system exec ds/cilium -- cilium-dbg bpf egress list
Defaulted container "cilium-agent" out of: cilium-agent, config (init), mount-cgroup (init), apply-sysctl-overwrites (init), mount-bpf-fs (init), clean-cilium-state (init), install-cni-binaries (init)
Source IP    Destination CIDR    Egress IP         Gateway IP
10.0.1.40    0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.1.126   0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.1.206   0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.1.234   0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.2.110   0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.2.126   0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.2.174   0.0.0.0/0           192.168.44.128    192.168.44.128
10.0.2.182   0.0.0.0/0           192.168.44.128    192.168.44.128
```

Confirm behavior with packet capture

* Start a capture on your router. To write a pcap file and capture ICMP on all interfaces:

```bash theme={null}
# Capture ICMP on all interfaces and write to file
user1@router:~$ sudo tcpdump -i any icmp -w egress-demo.pcap
# Or preview in terminal on a single interface for a host
user1@router:~$ sudo tcpdump -i ens39 -nnv host 8.8.8.8
```

* From a pod on worker1 (not the egress gateway), ping 8.8.8.8 and stop the capture after a few packets:

```bash theme={null}
user1@control-plane:~$ kubectl exec -it app1-75c78488c4-dq2dw -- bash
app1-75c78488c4-dq2dw:~# ping -c 4 8.8.8.8
...
```

Expected router capture after enabling egress gateway

* Router should now see the configured egress IP (192.168.44.128) as the source for traffic from pods matched by the policy instead of the pod's local node IP.

Example tcpdump showing traffic egressing from the egress node (worker2/egress IP)

```bash theme={null}
user1@router:~$ sudo tcpdump -i ens38 -nnv host 8.8.8.8
tcpdump: listening on ens38, link-type EN10MB (Ethernet), snapshot length 262144 bytes
05:28:32.380252 IP (tos 0x0, ttl 62, id 49930, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.44.128 > 8.8.8.8: ICMP echo request, id 3, seq 18, length 64
05:28:32.394744 IP (tos 0x0, ttl 127, id 3447, offset 0, flags [none], proto ICMP (1), length 84)
    8.8.8.8 > 192.168.44.128: ICMP echo reply, id 3, seq 18, length 64
...
```

Inspecting the packets (VXLAN encapsulation)

* When the source pod is on a different node than the configured egress node, Cilium forwards the packet across nodes using overlay encapsulation (often VXLAN). The outer header shows node→egress-node (physical IPs) and the inner payload contains the original pod→internet packet. The egress node decapsulates, SNATs to the egress IP, and sends the packet to the internet. Replies are received by the egress node and forwarded/decapsulated back to the source node as needed.

Wireshark view example:

<Frame>
  <img alt="A Wireshark packet-capture window showing a list of network packets (TCP, UDP, ICMP, TLS) with columns for source/destination, ports, and info. The lower panes display the selected packet's protocol details and hex/ASCII dump." />
</Frame>

Representative Wireshark decoded summary (illustrative)

```text theme={null}
Frame 39: ... (VXLAN encapsulated)
Ethernet II, Src: worker1-eth, Dst: worker2-eth
Internet Protocol Version 4, Src: 192.168.211.128, Dst: 192.168.44.128   <-- outer headers (node -> egress-node)
User Datagram Protocol, Src Port: 58778, Dst Port: 8472
Virtual eXtensible Local Area Network
  Inner Ethernet II, Src: cilium, Dst: cilium
  Internet Protocol Version 4, Src: 10.0.1.40, Dst: 8.8.8.8   <-- inner headers (pod -> internet)
  ICMP Echo (ping) request
```

Decapsulated packet leaving the egress node:

```text theme={null}
Frame 40: ...
Ethernet II, Src: worker2-eth, Dst: router
Internet Protocol Version 4, Src: 192.168.44.128, Dst: 8.8.8.8   <-- packet sent to internet with SNAT to egress node IP
ICMP Echo (ping) request
```

Reply returned and delivered back to the pod (encapsulated back if required):

```text theme={null}
Frame 42: ... (VXLAN inner packet containing 8.8.8.8 -> 10.0.1.40)
```

Summary and best practices

* Default: each node SNATs pod outbound traffic to its node IP; external servers will see multiple source IPs if pods are distributed across nodes.
* With Cilium egress gateway: you can centralize egress IPs by selecting one or more egress nodes. Matched pod traffic is forwarded (often via VXLAN), SNAT'd at the egress node, and sent to the internet — useful for predictable outbound IPs, firewalling, and auditing.
* Ensure:
  * kubeProxyReplacement is enabled,
  * eBPF masquerade (bpf.masquerade) is enabled,
  * quoting label values (e.g., egress: "true") in YAML to avoid boolean parsing issues.
* For production: consider multiple egress nodes and failover strategies to avoid single points of egress.

Links and references

* [Cilium Egress Gateway Documentation](https://docs.cilium.io/en/stable/policy/egressgateway/)
* [Kubernetes Concepts — What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Cilium Helm Chart](https://artifacthub.io/packages/helm/cilium/cilium)

If you'd like, I can also provide:

* A granular policy example selecting a single destination IP (e.g., "8.8.8.8/32"),
* Steps to configure multiple egress nodes with failover,
* Commands to inspect Cilium policy state and logs for troubleshooting.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/39bdf5f3-64a6-4e1d-8ac6-4484d992500a)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/809ecc9d-097b-45b8-a548-8f33d8ee89a2/lesson/1464469f-605c-4a8e-96da-a3b305e041cb)


# Demo L2 Announcement

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/BGP-External-Networking/Demo-L2-Announcement/page

Demonstrates Cilium L2 announcement to assign external IPs to LoadBalancer services and have nodes answer ARP in a local Kind Kubernetes cluster.

This guide demonstrates Cilium's L2 announcement feature and how it enables nodes to respond to ARP requests for LoadBalancer external IPs in a local Kubernetes cluster (Kind is used in this demo). The goal is to show how to assign external IPs to LoadBalancer services and have nodes announce those IPs on the host subnet so clients can reach services via ARP.

<Frame>
  <img alt="A presentation slide showing the word &#x22;Demo&#x22; on the left and a turquoise curved shape on the right with the text &#x22;L2 Announcement.&#x22; Small copyright text &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

## Overview

* Technologies: Cilium (L2 announcements), Kind (local cluster), Helm, kubectl.
* Goal: Assign external IPs from a node subnet to LoadBalancer services and have selected nodes respond to ARP for those IPs using Cilium L2 announcements.
* Key CRDs used:
  * CiliumLoadBalancerIPPool: allocate external IPs for LoadBalancer services.
  * CiliumL2AnnouncementPolicy: control which nodes/interfaces respond to ARP for which services.

## Prerequisites

* A running Kind cluster and kubectl configured to that cluster.
* Helm installed and access to the Cilium Helm chart (cilium/cilium).
* Docker available if using Kind node containers for debugging.

Useful references:

* Cilium: [https://cilium.io/](https://cilium.io/)
* Kind: [https://kind.sigs.k8s.io/](https://kind.sigs.k8s.io/)
* Helm: [https://helm.sh/](https://helm.sh/)

## 1. Check cluster state and prepare Cilium values

Before installing Cilium, the cluster nodes may appear NotReady because the CNI is missing:

```bash theme={null}
kubectl get node
NAME                             STATUS     ROLES           AGE   VERSION
my-cluster-control-plane         NotReady   control-plane   30s   v1.32.2
my-cluster-worker                NotReady   <none>          19s   v1.32.2
my-cluster-worker2               NotReady   <none>          18s   v1.32.2
```

To enable L2 announcements, enable both the L2 announcement feature and kube-proxy replacement in Cilium. A typical Helm upgrade/install invocation looks like this:

```bash theme={null}
helm upgrade cilium ./cilium \
  --namespace kube-system \
  --reuse-values \
  --set l2announcements.enabled=true \
  --set kubeProxyReplacement=true \
  --set k8sClientRateLimit.qps={QPS} \
  --set k8sClientRateLimit.burst={BURST} \
  --set k8sServiceHost=${API_SERVER_IP} \
  --set k8sServicePort=${API_SERVER_PORT}
```

> **lightbulb** When enabling kube-proxy replacement, provide the API server host and port (k8sServiceHost and k8sServicePort) so Cilium can reach the Kubernetes API. You can also edit the chart values file and set these keys before installing via Helm.

A good workflow is to fetch the default chart values, edit them, and then install:

```bash theme={null}
helm show values cilium/cilium > values.yaml
