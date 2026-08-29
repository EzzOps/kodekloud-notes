# Switch to cluster2 and create frontend and test pods
kubectx kind-cluster2
kubectl run frontend --image=nicolaka/netshoot -l app=frontend -- sleep infinity
kubectl run test --image=nicolaka/netshoot -l app=test -- sleep infinity
kubectl get pod --show-labels

# Switch to cluster1 and create frontend and test pods
kubectx kind-cluster1
kubectl run frontend --image=nicolaka/netshoot -l app=frontend -- sleep infinity
kubectl run test --image=nicolaka/netshoot -l app=test -- sleep infinity
kubectl get pod --show-labels
```

Check Cilium clustermesh status from one cluster (example: cluster1):

```bash theme={null}
kubectx kind-cluster1
cilium clustermesh status
```

Example (cleaned) output:

```text theme={null}
✅ Service "clustermesh-apiserver" of type "LoadBalancer" found
✅ Cluster access information is available: - 172.19.255.91:2379
✅ Deployment clustermesh-apiserver is ready
ℹ KVStoreMesh is enabled

✅ All 3 nodes are connected to all clusters [min:1 / avg:1.0 / max:1]
✅ All 1 KVStoreMesh replicas are connected to all clusters

Cluster Connections:
- cluster2: 3/3 configured, 3/3 connected - KVStoreMesh: 1/1 configured, 1/1 connected

Global services: [ min:1 / avg:1.0 / max:1 ]
```

Confirm nodes are present in each cluster:

```bash theme={null}
kubectx kind-cluster1
kubectl get node

kubectx kind-cluster2
kubectl get node
```

***

## 2) Deploy myapp and mark the Service as global

Deploy the same Deployment in both clusters using the hashicorp/http-echo image. Set the -text argument differently in each cluster so responses identify which cluster served them.

Deployment (apply in both clusters; change -text accordingly):

```yaml theme={null}
# myapp-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    app: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: hashicorp/http-echo:0.2.3
        args:
          - -listen=:80
          - -text="This is Cluster1"
        ports:
          - containerPort: 80
```

Service manifest (global + local affinity, apply in both clusters):

```yaml theme={null}
# myapp-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  annotations:
    service.cilium.io/global: "true"
    service.cilium.io/affinity: "local"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 80
```

Apply the manifests in both clusters (update -text to "This is Cluster2" for cluster2):

```bash theme={null}
# Example flow (do this in each cluster, adjusting args)
kubectx kind-cluster1
kubectl apply -f myapp-deployment.yaml
kubectl apply -f myapp-service.yaml

kubectx kind-cluster2
# Edit deployment to change -text to "This is Cluster2" then apply
kubectl apply -f myapp-deployment.yaml
kubectl apply -f myapp-service.yaml
```

Verify:

```bash theme={null}
kubectl get pods -o wide
kubectl get svc myapp-service -o yaml
```

You should see:

* myapp pods in each cluster returning different text.
* myapp-service annotated as global with local affinity.

***

## 3) Create a CiliumNetworkPolicy to allow only frontend -> myapp

Goal: only pods labeled app=frontend should be allowed to connect to pods labeled app=myapp.

Policy:

```yaml theme={null}
# network-policy.yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: my-policy
spec:
  endpointSelector:
    matchLabels:
      app: myapp
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
```

Apply this policy just on cluster1 to observe cluster-scoped behavior:

```bash theme={null}
kubectx kind-cluster1
kubectl apply -f network-policy.yaml
kubectl get ciliumnetworkpolicy
```

Test connectivity from pods in cluster1:

```bash theme={null}
# From frontend on cluster1 -> service (expected: succeed)
kubectl exec -it frontend -- curl -sS myapp-service

# From test pod on cluster1 -> service (expected: blocked/hang or fail)
kubectl exec -it test -- curl -sS --max-time 5 myapp-service || echo "request failed/timeout"
```

Expected results:

* frontend on cluster1 can curl myapp-service in cluster1 and receive "This is Cluster1".
* test pod on cluster1 cannot reach myapp pods in cluster1 (policy blocks it).

***

## 4) Cluster-scoped policy behavior in a cluster mesh

Key observations you should take away:

* CiliumNetworkPolicy is enforced only on the cluster where it is applied. A policy applied on cluster1 only affects endpoints in cluster1.
* fromEndpoints matchLabels (e.g., app=frontend) do not include cluster identity by default. This means a frontend pod in cluster2 that has app=frontend will match ingress rules on cluster1 and be allowed to reach myapp pods in cluster1 if that remote policy permits it.

Demonstration steps:

```bash theme={null}
# On cluster2: frontend -> its local service (expected: succeed)
kubectx kind-cluster2
kubectl exec -it frontend -- curl -sS myapp-service   # "This is Cluster2"

# On cluster2: frontend -> cluster1 myapp (may succeed if cluster1 policy allows app=frontend)
# On cluster1: frontend -> its myapp (expected: "This is Cluster1" if allowed)
kubectx kind-cluster1
kubectl exec -it frontend -- curl -sS myapp-service   # "This is Cluster1" when allowed
```

> **lightbulb** CiliumNetworkPolicy is cluster-scoped. To enforce the same network policy across all clusters in a mesh, apply the policy manifest to every cluster that hosts endpoints you want protected.

Table: Policy enforcement examples

| Policy applied on   | Endpoints affected          | Cross-cluster label match                                                                                 |
| ------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------- |
| cluster1 only       | Only myapp pods in cluster1 | Frontend pods in any cluster with label app=frontend may match and be allowed to reach cluster1 endpoints |
| cluster1 + cluster2 | myapp pods in both clusters | Label-based allow applies only where policy is present; both clusters enforce the rule locally            |

***

## 5) Apply the same policy on cluster2

To ensure the same restriction across clusters, apply the same CiliumNetworkPolicy to cluster2:

```bash theme={null}
kubectx kind-cluster2
kubectl apply -f network-policy.yaml
kubectl get ciliumnetworkpolicy
```

After applying cluster2 policy:

* test pods on both clusters will be blocked from talking to local myapp pods.
* frontend pods on either cluster will be allowed to reach local myapp pods (label-based allow), since both clusters now enforce the same rule.

***

## 6) Restrict allowed sources to a specific cluster

If you want to allow only frontend pods from a specific cluster (for example, only frontends running in cluster1), add the special label io.cilium.k8s.policy.cluster with the cluster's configured name to the fromEndpoints matchLabels.

Example policy that allows only frontends from cluster1:

```yaml theme={null}
# network-policy-cluster-restricted.yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: my-policy
spec:
  endpointSelector:
    matchLabels:
      app: myapp
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
        io.cilium.k8s.policy.cluster: cluster1
```

Notes:

* io.cilium.k8s.policy.cluster must match the cluster name configured in Cilium's values.yaml when you installed Cilium. Example:

```yaml theme={null}
cluster:
  name: cluster2
  id: 2
```

* The cluster name is case-sensitive and must match exactly.

Apply the cluster-restricted policy on the cluster that hosts the myapp endpoints (e.g., to restrict access to myapp in cluster2, apply the policy on cluster2):

```bash theme={null}
kubectx kind-cluster2
kubectl apply -f network-policy-cluster-restricted.yaml
```

Behavior after applying:

* Frontend on cluster1 allowed only if io.cilium.k8s.policy.cluster matches cluster1.
* Frontend on cluster2 denied if the policy restricts to cluster1.
* test pods remain denied.

***

## Summary / Best practices

* Cilium network policies are enforced locally in each cluster. In a Cluster Mesh, apply the same policies to every cluster where you want consistent enforcement.
* Label-based fromEndpoints rules (e.g., app=frontend) match across clusters if those pods are visible via the global Service and labels match — unless you restrict by cluster identity.
* To limit allowed sources to a single cluster, use io.cilium.k8s.policy.cluster: \<cluster-name> in the fromEndpoints matchLabels.
* Verify your Cilium cluster name configuration used at install time if you plan to use cluster-scoped label matching.

> **warning** If you use global Services (service.cilium.io/global: "true"), remember: traffic to endpoints on a remote cluster is subject to the policies applied on that remote cluster. Ensure policies are deployed in every cluster you expect to enforce access controls.

## Links and References

* [Cilium Cluster Mesh guide](https://docs.cilium.io/en/stable/gettingstarted/clustermesh/)
* [Cilium policy language docs](https://docs.cilium.io/en/stable/policy/language/)
* [Cilium Helm installation and values.yaml](https://docs.cilium.io/en/stable/gettingstarted/helm/)
* [Kubernetes kubectl documentation](https://kubernetes.io/docs/reference/kubectl/)
* [kubectx repository](https://github.com/ahmetb/kubectx)
* [hashicorp/http-echo image](https://hub.docker.com/r/hashicorp/http-echo)
* [nicolaka/netshoot (debug image)](https://hub.docker.com/r/nicolaka/netshoot)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b8be180f-1719-47ca-b26e-7bf942694abf/lesson/e5f07eb6-ad1f-4d4b-b0b4-af7c3a61fca0)


# Demo Configuring Cluster Mesh

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cluster-Mesh/Demo-Configuring-Cluster-Mesh/page

Guide to configure Cilium Cluster Mesh across two Kubernetes clusters, install Cilium, connect clusters, advertise global services, test service sharing and affinity, and clean up.

In this guide you'll learn how to configure a Cilium Cluster Mesh across two Kubernetes clusters (kind-cluster1 and kind-cluster2). The walkthrough covers:

* Preparing and customizing Cilium Helm values for Cluster Mesh
* Installing Cilium on both clusters
* Enabling the clustermesh-apiserver and connecting clusters
* Deploying a test application and validating global service behavior (shared and affinity modes)
* Cleaning up

This tutorial assumes familiarity with kubectl contexts and Helm. Key prerequisites: unique cluster IDs and non-overlapping pod CIDR ranges for each cluster.

> **lightbulb** Make sure each cluster has a unique cluster ID and non-overlapping pod CIDR ranges before enabling Cluster Mesh.

Table of Cilium annotations used in this guide:

|                   Annotation | Purpose                                                 | Example values                  |
| ---------------------------: | ------------------------------------------------------- | ------------------------------- |
|   `service.cilium.io/global` | Mark a Service as a global (mesh-advertised) service    | `"true"`                        |
|   `service.cilium.io/shared` | Control whether a cluster advertises its local backends | `"true"` or `"false"`           |
| `service.cilium.io/affinity` | Prefer local or remote backends for a global service    | `"local"`, `"remote"`, `"none"` |

Related references:

* [Cilium Cluster Mesh docs](https://docs.cilium.io/en/stable/gettingstarted/clustermesh/)
* [Kubernetes concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

## 1) Verify clusters and node readiness

Confirm your kubectl contexts and verify node status on both clusters. Nodes will show NotReady until a CNI (Cilium) is installed.

```bash theme={null}
