# Assuming kubeconfig has contexts: cluster1, cluster2, cluster3
for ctx in cluster1 cluster2 cluster3; do
  kubectl --context="$ctx" apply -f allow-cross-cluster.yaml
done
```

> **lightbulb** Network policies in a Cluster Mesh are enforced per cluster. You can match endpoint traffic by origin using the `io.cilium.k8s.policy.cluster` label, but to enforce a policy across the mesh you must apply the same policy manifest in every cluster where enforcement is required.

Further reading and references

* Cilium Documentation — Network Policies: [https://cilium.io/docs/](https://cilium.io/docs/)
* Kubernetes Networking Concepts: [https://kubernetes.io/docs/concepts/services-networking/network-policies/](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* Cilium Cluster Mesh: [https://cilium.io/blog/2020/10/29/cilium-clustermesh](https://cilium.io/blog/2020/10/29/cilium-clustermesh)

<Frame>
  <img alt="A diagram titled &#x22;Cluster Mesh Network Policy&#x22; showing three Kubernetes clusters, each with frontend and backend pods. Network policy outlines around backend pods and arrows indicate allowed (green) and blocked (grey) cross-cluster traffic." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b8be180f-1719-47ca-b26e-7bf942694abf/lesson/190501c6-3a45-46f4-b57a-47b72e7ad5b0)


# Demo Cluster Mesh Network Policy

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cluster-Mesh/Demo-Cluster-Mesh-Network-Policy/page

Demonstrates Cilium Cluster Mesh network policy behavior across two Kubernetes clusters, showing global services, local enforcement, cross cluster label matching, and restricting allowed sources by cluster label.

This guide demonstrates how Cilium network policies behave in a Cilium Cluster Mesh across two Kubernetes clusters (kind-cluster1 and kind-cluster2). You will:

* Create simple test workloads.
* Expose a Service as a global Service.
* Apply a CiliumNetworkPolicy on one cluster and observe behavior.
* Apply policies cluster-wide and learn how to restrict allowed sources to a specific cluster using the special cluster label.

Key terms: Cilium Cluster Mesh, CiliumNetworkPolicy, global Service, io.cilium.k8s.policy.cluster.

## Prerequisites

| Requirement                                    | Purpose / Notes                                                                                                                                                                                          |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Two clusters connected via Cilium Cluster Mesh | Example contexts: kind-cluster1, kind-cluster2                                                                                                                                                           |
| kubectl and kubectx                            | Switch contexts and run commands: [https://kubernetes.io/docs/reference/kubectl/](https://kubernetes.io/docs/reference/kubectl/), [https://github.com/ahmetb/kubectx](https://github.com/ahmetb/kubectx) |
| Cilium installed in both clusters              | See Cilium docs: [https://docs.cilium.io/en/stable/](https://docs.cilium.io/en/stable/)                                                                                                                  |

References:

* [Cilium Cluster Mesh guide](https://docs.cilium.io/en/stable/gettingstarted/clustermesh/)
* [Cilium policy language](https://docs.cilium.io/en/stable/policy/language/)

***

## 1) Verify cluster mesh and create test frontend/test pods

Create a debug frontend pod (nicolaka/netshoot) and a simple test pod in each cluster. These are used to simulate allowed and denied clients.

Commands:

```bash theme={null}
