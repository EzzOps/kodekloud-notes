# cluster1 cilium configuration (example)
ipam:
  clusterPoolIPv4PodCIDRList: ["11.0.0.0/8"]
  clusterPoolIPv6PodCIDRList: ["fd00::/104"]

cluster:
  name: cluster1
  id: 1

---
# cluster2 cilium configuration (example)
ipam:
  clusterPoolIPv4PodCIDRList: ["12.0.0.0/8"]
  clusterPoolIPv6PodCIDRList: ["fd01::/104"]

cluster:
  name: cluster2
  id: 2
```

Notes:

* Provide unique IPv4/IPv6 ranges per cluster if IPv6 is enabled.
* Give each cluster a unique name and integer ID.

***

## Enabling Cluster Mesh (Cilium)

After deploying Cilium on each cluster, enable Cluster Mesh with the cilium clustermesh enable command. If your environment cannot automatically provision an appropriate LoadBalancer or service type, you can supply a service type explicitly.

Example: enable Cluster Mesh on two clusters using LoadBalancer service type:

```bash theme={null}
cilium clustermesh enable --context $CLUSTER1 --service-type=LoadBalancer
cilium clustermesh enable --context $CLUSTER2 --service-type=LoadBalancer
```

When enabled, Cilium creates a Cluster Mesh API server service in the kube-system namespace. To verify, list services in that namespace:

```bash theme={null}
kubectl get svc -n kube-system
```

Example output (abridged):

```text theme={null}
NAME                                TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                             AGE
cilium-envoy                        ClusterIP      None           <none>           9964/TCP                            15h
clustermesh-apiserver               LoadBalancer   10.96.97.89    172.19.255.46    2379:32200/TCP                      15h
clustermesh-apiserver-metrics       ClusterIP      None           <none>           9962/TCP,9964/TCP,9963/TCP          15h
```

The LoadBalancer EXTERNAL-IP (when provisioned) is used by remote clusters to reach the Cluster Mesh API server.

***

## Connecting clusters into a mesh

After enabling Cluster Mesh on each cluster, establish mesh connections using cilium clustermesh connect. Provide the source and destination kubeconfig contexts:

```bash theme={null}
cilium clustermesh connect --context $CLUSTER1 --destination-context $CLUSTER2
```

You only need to run the connect command in one direction per pair. For a mesh of three clusters, ensure all pairwise connections exist (for full mesh topology: cluster1→cluster2, cluster1→cluster3, cluster2→cluster3), or use scripts/automation to configure full-mesh connectivity.

Check the Cluster Mesh status with:

```bash theme={null}
cilium clustermesh status
```

Example status output:

```text theme={null}
✅ Service "clustermesh-apiserver" of type "LoadBalancer" found
✅ Cluster access information is available:
 - 172.19.255.46:2379
✅ Deployment clustermesh-apiserver is ready
ℹ️ KVStoreMesh is enabled

✅ All 3 nodes are connected to all clusters [min:1 / avg:1.0 / max:1]
✅ All 1 KVStoreMesh replicas are connected to all clusters [min:1 / avg:1.0 / max:1]

🪄 Cluster Connections:
 - cluster1: 3 configured, 3/3 connected
   KVStoreMesh: 1/1 configured, 1/1 connected

🔁 Global services: [ min:1 / avg:1.0 / max:1 ]
```

Once connections are established, pods across clusters can communicate according to configured services and network policies.

<Frame>
  <img alt="A diagram titled &#x22;Cluster Mesh Setup&#x22; showing three Kubernetes clusters (Cluster 1, Cluster 2, Cluster 3) inside a dashed &#x22;Cluster Mesh&#x22; boundary, each cluster containing a pod icon. It illustrates a multi-cluster pod configuration." />
</Frame>

***

## KVStoreMesh — purpose and design

KVStoreMesh is a design improvement introduced to scale Cluster Mesh. Understanding its role helps when planning and troubleshooting multi-cluster environments.

Original design challenges:

* Each Cilium agent/operator wrote resources (Services, CiliumNodes, identities, endpoints) into the cluster Kubernetes API.
* The Cluster Mesh API server would watch the Kubernetes API and sync that data into a central etcd.
* Remote agents had to watch many remote etcd instances; at scale this caused high synchronization load, increased latency, and heavy etcd pressure.

<Frame>
  <img alt="An architecture diagram showing Cilium agents and an operator interacting with Kubernetes and a clustermesh apiserver (a Go binary and etcd) that list/watches and syncs with multiple remote clusters. A caption at the bottom warns that constant syncing leads to latency and scalability issues." />
</Frame>

KVStoreMesh design:

* Each cluster runs a local KVStoreMesh binary and a local etcd instance containing mesh-wide state.
* Cilium agents sync only with the local KV store.
* KVStoreMesh instances synchronize state between clusters, reducing the number of remote endpoints that each agent must watch.

Benefits:

* Reduced overall etcd usage and pressure.
* More balanced load across cluster KV stores.
* Lower impact from agent restarts, workload churn, or new clusters joining the mesh.

<Frame>
  <img alt="An architecture diagram labeled &#x22;KVStoreMesh&#x22; showing two clusters (Cluster A and Cluster B). It depicts Cilium agent/operator, the K8s API, and per-cluster kvstore components (binary and etcd) with arrows for List/Watch and Sync interactions between the clusters." />
</Frame>

<Frame>
  <img alt="A presentation slide titled &#x22;KVStoreMesh&#x22; with three numbered panels: &#x22;Reduced etcd usage,&#x22; &#x22;Balanced load,&#x22; and &#x22;Minimized churn impact.&#x22; Each panel has brief bullets explaining less pressure on etcd, load shared across clusters, and avoiding mesh-wide disruption during agent restarts, workload churn, and new cluster joins." />
</Frame>

KVStoreMesh is enabled by default in modern Cilium Cluster Mesh deployments.

<Callout icon="lightbulb">
  KVStoreMesh is enabled by default. If you must disable it for compatibility reasons, pass --kvstore-mesh=false when enabling Cluster Mesh.
</Callout>

Examples:

```bash theme={null}
# Enable Cluster Mesh (KVStoreMesh enabled by default)
cilium clustermesh enable --context $CLUSTER1 --service-type=LoadBalancer
```

```bash theme={null}
# Enable Cluster Mesh but disable KVStoreMesh explicitly (compatibility mode)
cilium clustermesh enable --context $CLUSTER1 --service-type=LoadBalancer --kvstore-mesh=false
```

Adjust the command and the context for each cluster you add to the mesh.

***

## Summary

This article covered:

* What Cluster Mesh provides: cross-cluster connectivity, cross-cluster load balancing, and shared network policies.
* Key prerequisites: matching datapath, unique Pod CIDRs, full node connectivity, and unique cluster IDs.
* Example Cilium per-cluster configuration snippets.
* How to enable Cluster Mesh and verify the Cluster Mesh API service.
* How to connect clusters and validate mesh status.
* Why KVStoreMesh improves scalability and how to enable/disable it.

Links and references:

* [Cilium Cluster Mesh documentation](https://docs.cilium.io/en/stable/clustermesh/)
* [Kubernetes networking concepts](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
* [Cilium GitHub repository](https://github.com/cilium/cilium)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b8be180f-1719-47ca-b26e-7bf942694abf/lesson/59b9dc70-9b6f-408c-86ef-a96cc335a930" />
</CardGroup>


# Cluster Mesh Network Policy

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cluster-Mesh/Cluster-Mesh-Network-Policy/page

Explains how Cilium network policies are enforced per cluster in a Cluster Mesh and require per-cluster application to restrict cross-cluster traffic

In this lesson we examine how Cilium network policies behave in a Cluster Mesh. When multiple Kubernetes clusters are joined into a Cilium Cluster Mesh, workloads can communicate across clusters, but policy enforcement remains per-cluster. That means deploying a CiliumNetworkPolicy on one cluster does not automatically propagate that policy to other clusters in the mesh—you must apply the same manifest on each cluster where you want it enforced.

Below is a concrete example: a Cluster Mesh spanning three clusters (cluster1, cluster2, cluster3). Each cluster runs a `frontend` pod and a `backend` pod. The CiliumNetworkPolicy shown is applied on Cluster Two and selects backend endpoints there, allowing ingress only from frontend endpoints that carry a specific origin-cluster label (`io.cilium.k8s.policy.cluster: cluster1`). Effectively, this permits only frontends from cluster1 to connect to backends on cluster2; frontends from cluster2 and cluster3 are denied by this policy.

```yaml theme={null}
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "allow-cross-cluster"
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
        io.cilium.k8s.policy.cluster: cluster1
```

Key points

* Scope: This manifest is applied on Cluster Two and restricts ingress to backend pods in Cluster Two.
* Behavior: Frontend pods from Cluster One (`cluster1`) are allowed to reach backend pods on Cluster Two; frontends in Cluster Two and Cluster Three are denied by this rule.
* Enforcement: To enforce the same restriction on backend pods in Cluster Three (or Cluster One), apply the identical manifest to those clusters as well.

| Topic                          | Explanation                                                                                                                                                   | Example / Command                                              |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Per-cluster enforcement        | CiliumNetworkPolicy is evaluated by the Cilium agent running in each cluster. A policy applied in one cluster does not automatically apply in other clusters. | `kubectl apply -f allow-cross-cluster.yaml --context=cluster2` |
| Matching by origin cluster     | Use the label `io.cilium.k8s.policy.cluster` on endpoints to match traffic originating from a specific member cluster in the Cluster Mesh.                    | `io.cilium.k8s.policy.cluster: cluster1`                       |
| Deploying to multiple clusters | Apply the same manifest to each cluster where you want identical enforcement. Use context switching or automation to distribute policies.                     | See example loop below.                                        |

Example: apply the same manifest to multiple clusters

```bash theme={null}
