# List kubectl contexts
kubectx
# Example output:
# arn:aws:eks:us-east-1:195275640053:cluster/telepresence
# kind-cluster1
# Switch to a cluster and check nodes
kubectx kind-cluster1
kubectl get nodes
# Example output (before CNI is installed):
# NAME                      STATUS     ROLES          AGE   VERSION
# cluster1-control-plane    NotReady   control-plane  34h   v1.32.2
kubectx kind-cluster2
kubectl get nodes
# Example output (before CNI is installed):
# NAME                      STATUS     ROLES          AGE   VERSION
# cluster2-control-plane    NotReady   control-plane  34h   v1.32.2
# cluster2-worker           NotReady   <none>         34h   v1.32.2
```

## 2) Prepare Cilium Helm values for Cluster Mesh

Fetch the default Cilium Helm values and edit them to set a unique cluster name/id and non-overlapping pod CIDR pools.

```bash theme={null}
helm show values cilium/cilium > values.yaml
```

Important fields to set in `values.yaml` (only relevant snippets shown). Each cluster must have a unique `cluster.name` and `cluster.id`, and `operator.clusterPoolIPv4PodCIDRList` (and IPv6 counterpart if used) must not overlap between clusters.

* Example for cluster1:

```yaml theme={null}
cluster:
  name: cluster1
  id: 1

operator:
  clusterPoolIPv4PodCIDRList: ["11.0.0.0/8"]
  clusterPoolIPv4MaskSize: 24
  clusterPoolIPv6PodCIDRList: ["fd00::/104"]
  clusterPoolIPv6MaskSize: 120
```

* Example for cluster2:

```yaml theme={null}
cluster:
  name: cluster2
  id: 2

operator:
  clusterPoolIPv4PodCIDRList: ["12.0.0.0/8"]
  clusterPoolIPv4MaskSize: 24
  clusterPoolIPv6PodCIDRList: ["fd01::/104"]
  clusterPoolIPv6MaskSize: 120
```

Note: Do not reuse any IPv4/IPv6 CIDR ranges across clusters when using Cluster Mesh.

## 3) Install Cilium on each cluster

Add the Cilium Helm repo and install (or upgrade) Cilium on each cluster using the modified `values.yaml`.

```bash theme={null}
# Ensure Helm repo is set
helm repo add cilium https://helm.cilium.io/
helm repo update

# On kind-cluster1 (ensure kubectl context is set)
kubectx kind-cluster1
helm install cilium cilium/cilium -n kube-system -f values.yaml
# or, if already installed:
# helm upgrade --install cilium cilium/cilium -n kube-system -f values.yaml
```

Repeat after updating `values.yaml` for `kind-cluster2` with the cluster2 name/id/CIDR ranges.

After installation, nodes should transition to Ready because Cilium provides the CNI:

```bash theme={null}
kubectx kind-cluster1
kubectl get nodes
# NAME                      STATUS   ROLES           AGE   VERSION
# cluster1-control-plane    Ready    control-plane   34h   v1.32.2
# cluster1-worker           Ready    <none>          34h   v1.32.2
# cluster1-worker2          Ready    <none>          34h   v1.32.2
```

## 4) Enable Cluster Mesh API server on each cluster

Use the Cilium CLI to enable the clustermesh-apiserver on each cluster. On some environments (like kind) the CLI cannot auto-detect Service type; specify `--service-type=LoadBalancer` if you run into auto-detection errors.

```bash theme={null}
# On each cluster:
kubectx kind-cluster1
cilium clustermesh enable --context kind-cluster1 --service-type=LoadBalancer

# Repeat on cluster2:
kubectx kind-cluster2
cilium clustermesh enable --context kind-cluster2 --service-type=LoadBalancer
```

Verify the `clustermesh-apiserver` Service in `kube-system` and note its EXTERNAL-IP (LoadBalancer IP), which will be used for cluster-to-cluster communication:

```bash theme={null}
kubectl get svc -n kube-system
# Example relevant lines:
# clustermesh-apiserver         LoadBalancer   10.96.52.31      172.19.255.91   2379:31802/TCP
# clustermesh-apiserver         LoadBalancer   10.96.68.254     172.19.255.121  2379:31316/TCP
```

## 5) Connect the clusters into the Cluster Mesh

You only need to run the `cilium clustermesh connect` command once from any machine that has access to both kubectl contexts. This configures both sides.

```bash theme={null}
# Connect cluster1 to cluster2:
cilium clustermesh connect --context kind-cluster1 --destination-context kind-cluster2
```

Example diagnostic output (trimmed):

```text theme={null}
✨ Extracting access information of cluster cluster1...
🔑 Extracting secrets from cluster cluster1...
i Found ClusterMesh service IPs: [172.19.255.91]
✨ Extracting access information of cluster cluster2...
🔑 Extracting secrets from cluster cluster2...
i Found ClusterMesh service IPs: [172.19.255.121]
⚠️ Cilium CA certificates do not match between clusters. Multicluster features will be limited!
i Configuring Cilium in cluster kind-cluster1 to connect to cluster kind-cluster2
i Configuring Cilium in cluster kind-cluster2 to connect to cluster kind-cluster1
✅ Connected cluster kind-cluster1 <=> kind-cluster2!
```

Check Cluster Mesh status:

```bash theme={null}
cilium clustermesh status --context kind-cluster1
# Example success summary:
# ✅ Service "clustermesh-apiserver" of type "LoadBalancer" found
# ✅ Cluster access information is available: - 172.19.255.91:2379
# ✅ Deployment clustermesh-apiserver is ready
# ℹ️ KVStoreMesh is enabled
#
# ✅ All 3 nodes are connected to all clusters [min:1 / avg:1.0 / max:1]
# Cluster Connections:
# - cluster2: 3/3 configured, 3/3 connected
# Global services: [ min:0 / avg:0.0 / max:0 ]
```

Once status shows connected, proceed to deploy and test global services.

## 6) Deploy the test application into both clusters

Create a simple HTTP echo deployment and service on both clusters using hashicorp/http-echo. Use the same service name and namespace on both clusters and set the echo text to indicate the cluster identity.

Template file: `deploy-clusterX.yaml` — change the `-text` value per cluster before applying.

```yaml theme={null}
# deploy-clusterX.yaml (change the -text value per cluster before applying)
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
        image: hashicorp/http-echo
        args:
        - -listen=:80
        - -text="This is Cluster1"  # change to "This is Cluster2" for the other cluster
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 80
```

Apply the manifest on each cluster (swap the `-text` value accordingly):

```bash theme={null}
# On cluster1
kubectx kind-cluster1
kubectl apply -f deploy-cluster1.yaml

# On cluster2 (after editing the -text to "This is Cluster2")
kubectx kind-cluster2
kubectl apply -f deploy-cluster2.yaml
```

Create a troubleshooting pod (netshoot) on each cluster to test connectivity from within a pod:

```bash theme={null}
kubectx kind-cluster1
kubectl run test --image=nicolaka/netshoot -- sleep infinity

kubectx kind-cluster2
kubectl run test --image=nicolaka/netshoot -- sleep infinity
```

From outside the cluster you can curl the Service EXTERNAL-IP. From inside the cluster, DNS resolves the service name (e.g., `curl myapp-service`).

## 7) Default behavior (no global service annotation)

By default (no global annotation), services are local-only. A pod querying the service sees only local endpoints.

From a test pod in cluster1:

```bash theme={null}
kubectx kind-cluster1
kubectl exec test -- curl myapp-service
# Output:
# "This is Cluster1"
```

From a test pod in cluster2:

```bash theme={null}
kubectx kind-cluster2
kubectl exec test -- curl myapp-service
# Output:
# "This is Cluster2"
```

This default is expected even with Cluster Mesh enabled — no global advertisement occurs without the annotation.

## 8) Enable a Global Service (shared across clusters)

To advertise a Service globally across the mesh so backends in all clusters are available, annotate the Service with `service.cilium.io/global: "true"`. Apply the updated Service manifest to both clusters using the same name and namespace.

Service snippet (add the annotation under metadata.annotations):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  annotations:
    service.cilium.io/global: "true"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 80
```

Apply on both clusters:

```bash theme={null}
kubectx kind-cluster1
kubectl apply -f deploy-cluster1.yaml  # ensure annotation is present

kubectx kind-cluster2
kubectl apply -f deploy-cluster2.yaml  # ensure annotation is present
```

Verify Cluster Mesh now recognizes the global service:

```bash theme={null}
cilium clustermesh status --context kind-cluster1
# Global services: [ min:1 / avg:1.0 / max:1 ]
```

Behavior: requests to `myapp-service` from any cluster will be load-balanced across pods in both clusters.

```bash theme={null}
kubectx kind-cluster1
kubectl exec test -- curl myapp-service
kubectx kind-cluster2
kubectl exec test -- curl myapp-service
# Output examples: "This is Cluster1" or "This is Cluster2"
```

## 9) Disable sharing on a specific cluster (service.cilium.io/shared)

If you want a cluster to keep its local backends private (not advertised to the mesh), annotate its Service with `service.cilium.io/shared: "false"`. Apply this annotation only on the cluster you want to stop sharing from.

Example:

```yaml theme={null}
metadata:
  name: myapp-service
  annotations:
    service.cilium.io/global: "true"
    service.cilium.io.shared: "false"  # This cluster will NOT share this service to the mesh
```

Key behaviors:

* The cluster that sets `shared: "false"` will not advertise its local endpoints to other clusters.
* Pods in that cluster still use the global service (they can consume remote backends if available) — `shared` controls advertising, not consumption.

## 10) Service affinity: local vs remote

Cilium supports per-cluster affinity to prefer local or remote backends for a global service. Use the annotation `service.cilium.io/affinity` with values:

* `local` — prefer local backends; fallback to remote only if no local backends exist
* `remote` — prefer remote backends; fallback to local only if remote backends are unavailable
* `none` — default global load balancing (no affinity)

Add the annotation together with `service.cilium.io/global: "true"`:

```yaml theme={null}
metadata:
  name: myapp-service
  annotations:
    service.cilium.io/global: "true"
    service.cilium.io/affinity: "local"   # or "remote" or "none"
```

Example scenario for `affinity: "local"`:

1. With local backends present, pods in the cluster will hit local pods.
2. If local backends are scaled to zero, requests automatically fail over to remote cluster backends.

Demonstration (simulate failure by scaling a deployment to zero):

```bash theme={null}
# On cluster2, scale down to simulate failure
kubectx kind-cluster2
kubectl scale deployment myapp-deployment --replicas=0

# From a test pod in cluster2 (with affinity=local applied on the service), curl should fall back to cluster1:
kubectl exec test -- curl myapp-service
# Output:
# "This is Cluster1"
```

`affinity: "remote"` has the inverse preference (prefer remote, fallback to local).

## 11) Clean up

Delete test deployments and troubleshooting pods when finished. If you need to disconnect the Cluster Mesh, use the cilium clustermesh disable command.

```bash theme={null}
# Remove test resources on each cluster
kubectx kind-cluster1
kubectl delete -f deploy-cluster1.yaml
kubectl delete pod test --ignore-not-found

kubectx kind-cluster2
kubectl delete -f deploy-cluster2.yaml
kubectl delete pod test --ignore-not-found

# To disconnect clusters (if required)
# cilium clustermesh disable --context kind-cluster1
# cilium clustermesh disable --context kind-cluster2
```

Callouts and reminders:

> **lightbulb** * Ensure unique cluster IDs (1..255) and unique pod CIDR pools per cluster before enabling Cluster Mesh.
  * When using LoadBalancer service type on kind clusters, a layer that provides an external IP (e.g., a [MetalLB](https://metallb.universe.tf/) deployment) is required to obtain EXTERNAL-IP addresses.

Further reading and references:

* [Cilium Cluster Mesh — Getting Started](https://docs.cilium.io/en/stable/gettingstarted/clustermesh/)
* [Cilium Documentation](https://docs.cilium.io/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [MetalLB Load Balancer for bare-metal Kubernetes](https://metallb.universe.tf/)
* [hashicorp/http-echo image on Docker Hub](https://hub.docker.com/r/hashicorp/http-echo)
* [nicolaka/netshoot image on Docker Hub](https://hub.docker.com/r/nicolaka/netshoot)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b8be180f-1719-47ca-b26e-7bf942694abf/lesson/8b010e05-9973-440f-9e08-7a86e424a1ed)


# Global Service

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Cluster-Mesh/Global-Service/page

Explains using Cilium Cluster Mesh to expose and load balance Kubernetes Services across clusters with global services, sharing controls, and affinity options.

This guide explains how to expose Kubernetes Services across clusters using Cilium's Cluster Mesh and Global Services. It covers default behavior, how to enable a global service, per-cluster sharing control, affinity options, and practical examples.

Overview

* By default, a Kubernetes Service load-balances only to endpoints (Pods) in the same cluster.
* Cilium Cluster Mesh can expose Services across clusters. Enabling a global service allows cross-cluster load balancing and failover.
* To create a global service, deploy identical Service resources (same name, namespace, and ports) in each cluster where the Service should be reachable, and add the global annotation to enable cross-cluster behavior.

> **lightbulb** Ensure the Service resource (name, namespace, ports) is identical on each cluster. Only the annotations differ when you want to control sharing or affinity per-cluster.

## How global services work (high level)

* Each cluster advertises Services via Cluster Mesh when the Service is marked global.
* A Service is considered global only when the same Service (name + namespace + ports) exists across clusters and is annotated appropriately.
* Clients in any cluster can be load-balanced across local and remote endpoints depending on sharing and affinity configuration.
* If local endpoints disappear, traffic will fail over to available remote endpoints that advertise the Service.

## Default behavior (no global service)

When a frontend Pod in cluster A sends traffic to a Service that is not global, the Service routes only to endpoints in cluster A. There is no cross-cluster load balancing by default.

## Enable a global service

To enable cross-cluster load balancing, create the same Service in every cluster where the Service should be reachable and add the global annotation:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: default
  annotations:
    service.cilium.io/global: "true"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 80
```

Behavior:

* Once the Service exists with `service.cilium.io/global: "true"` across the clusters, the Service becomes global.
* A frontend Pod in cluster A will have its traffic load-balanced across back-end Pods in both local and remote clusters.
* If all local endpoints are unavailable, traffic automatically fails over to remote endpoints advertising the Service.

## Per-cluster sharing control (service.cilium.io/shared)

You can control whether a cluster advertises its endpoints to other clusters by setting the `service.cilium.io/shared` annotation on the local Service.

Cluster A (do not advertise endpoints to other clusters):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: default
  annotations:
    service.cilium.io/global: "true"
    service.cilium.io/shared: "false"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 80
```

Cluster B (advertise by default - omit `shared` or set to "true"):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: default
  annotations:
    service.cilium.io/global: "true"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 80
```

Behavior:

* Frontend Pods in cluster A will still observe endpoints from all clusters because cluster A has a local Service marked global (even if cluster A does not share its endpoints).
* Frontend Pods in cluster B will see only endpoints advertised by clusters that set `shared: "true"` (or omitted the annotation). If cluster A set `shared: "false"`, B will not see cluster A’s endpoints.

## Affinity: bias load-balancing to local or remote endpoints

Use `service.cilium.io/affinity` to prefer local or remote endpoints. Preference is soft: traffic fails over if preferred endpoints are unavailable.

Affinity: local (prefer local endpoints, fallback to remote)

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: default
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

Behavior:

* The Service prefers local endpoints for lower latency.
* If no local endpoints are available, traffic will fail over to remote endpoints advertising the Service.

Affinity: remote (prefer remote endpoints, fallback to local)

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: default
  annotations:
    service.cilium.io/global: "true"
    service.cilium.io/affinity: "remote"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 80
```

Behavior:

* The Service prefers remote endpoints.
* If remote endpoints are unavailable, traffic falls back to local endpoints.

## Annotations quick reference

| Annotation                 | Purpose                                                                 | Example value      |
| -------------------------- | ----------------------------------------------------------------------- | ------------------ |
| service.cilium.io/global   | Mark Service as global and advertise it via Cluster Mesh                | "true"             |
| service.cilium.io/shared   | Control whether this cluster advertises its endpoints to other clusters | "true" / "false"   |
| service.cilium.io/affinity | Bias load-balancing to local or remote endpoints                        | "local" / "remote" |

## Practical notes and troubleshooting

* Ensure the Service name, namespace, and ports are identical across clusters; mismatched Service specs prevent global behavior.
* Use `kubectl get svc -n <ns> -o yaml` on each cluster to confirm annotations and spec parity.
* If a cluster’s Service is global but marked `shared: "false"`, that cluster will consume remote endpoints but will not advertise its own endpoints to others.

> **lightbulb** Test global services using simple client Pods in each cluster. Verify endpoint lists and traffic flows with `kubectl describe svc` and by curling the Service from a test Pod to observe cross-cluster responses.

## Summary

* Default: Services route only to endpoints in the same cluster.
* To enable cross-cluster load balancing, add `service.cilium.io/global: "true"` to the identical Service on each cluster that should participate.
* Control advertising of endpoints with `service.cilium.io/shared: "false"`.
* Bias traffic toward local or remote endpoints using `service.cilium.io/affinity: "local"` or `"remote"`, with automatic fallback when preferred endpoints are unavailable.

Links and references

* [Cilium Cluster Mesh documentation](https://docs.cilium.io/en/stable/cluster-mesh/)
* [Kubernetes Services documentation](https://kubernetes.io/docs/concepts/services-networking/service/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b8be180f-1719-47ca-b26e-7bf942694abf/lesson/cb3c3afd-ff1a-4c71-b9ca-11ad8d626275)
