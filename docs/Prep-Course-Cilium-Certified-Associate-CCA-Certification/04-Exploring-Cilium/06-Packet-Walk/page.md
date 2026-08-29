# Delete the ConfigMap as well to avoid kube-proxy being reinstalled during a kubeadm upgrade
kubectl -n kube-system delete cm kube-proxy
```

Also ensure you clean up any leftover iptables or ipvs rules created by kube-proxy to avoid conflicts with Cilium.

> **warning** Before removing kube-proxy, ensure you understand how control-plane and API-server access will be handled. Removing kube-proxy without configuring Cilium to communicate with the API server can lead to control-plane connectivity issues.

2. Configure Cilium to replace kube-proxy
   When Cilium replaces kube-proxy, it must be able to contact the Kubernetes API server directly (since the kube-proxy Service IP may no longer exist). Provide explicit API server host and port in Cilium's configuration and enable kubeProxyReplacement:

```yaml theme={null}
kubeProxyReplacement: "true"
k8sServiceHost: "host-ip-control-plane"
k8sServicePort: "6443"
```

> **lightbulb** Setting k8sServiceHost and k8sServicePort avoids a bootstrap problem: with kube-proxy removed, Cilium needs explicit connectivity information to the API server to initialize service discovery and control-plane interactions.

Apply the Cilium manifest or Helm chart with these settings and ensure Cilium DaemonSet/Pods restart with the new configuration.

3. Verify kube-proxy replacement is active
   After deploying Cilium with kubeProxyReplacement enabled, validate the agent status:

```bash theme={null}
kubectl -n kube-system exec ds/cilium -- cilium-dbg status | grep KubeProxyReplacement
```

For more verbose diagnostics:

```bash theme={null}
kubectl -n kube-system exec ds/cilium -- cilium-dbg status --verbose | grep KubeProxyReplacement
```

A successful replacement shows `KubeProxyReplacement: true`, indicating Cilium is handling service routing/load balancing via eBPF.

Operational notes and caveats

* Remove all kube-proxy artifacts (DaemonSet, ConfigMap) and clear iptables/ipvs rules to avoid conflicts.
* Ensure k8sServiceHost and k8sServicePort are correct so Cilium can reach the API server.
* Test pod-to-pod, pod-to-service, and control-plane connectivity after enabling replacement.
* Monitor Cilium logs and use Cilium diagnostics (cilium-dbg, Hubble) to validate traffic flows and troubleshoot.

Helpful links and references

* Cilium Documentation: [https://cilium.io/](https://cilium.io/)
* Kubernetes Service Networking: [https://kubernetes.io/docs/concepts/services-networking/](https://kubernetes.io/docs/concepts/services-networking/)
* eBPF Overview: [https://ebpf.io/](https://ebpf.io/)

For more on configuring Cilium via Helm or manifests, see the official Cilium docs and Helm chart examples.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/0807e400-fd1b-4f25-bba5-d0fdb0f4e3f2/lesson/1580f9e9-3811-40f1-bfc7-64577c58ffc8)


# Packet Walk

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Exploring-Cilium/Packet-Walk/page

Explains high level packet traversal in a Cilium Kubernetes cluster showing eBPF attachments, service DNAT, conntrack, BPF maps and VXLAN encapsulation for pod to pod traffic.

In this lesson we step through the network interfaces created by Cilium and then perform a packet walk: as packets traverse a node and the cluster network, we explain the routing decisions and where eBPF is involved. This is a high-level conceptual overview to show the big picture — it does not dive into eBPF implementation details.

> **lightbulb** This article simplifies many details for clarity. The exact behaviour may vary with Cilium versions and configuration (for example: kube-proxy replacement, encapsulation mode, or network policy settings).

## Node interfaces and pod addressing

Assume a two-node Kubernetes cluster with Cilium installed. On a node (Node1) the relevant host interfaces might look like:

```bash theme={null}
