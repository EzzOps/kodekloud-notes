# OUTPUT
# NAME                                  READY   STATUS    RESTARTS   AGE
# nginx-deployment-7ff69d756-8qdv8      1/1     Running   0          3m
# nginx-deployment-7ff69d756-hccjn      1/1     Running   0          3m
# nginx-deployment-7ff69d756-stpmz      1/1     Running   0          3m
```

***

## 1. ClusterIP (Default)

ClusterIP is the Kubernetes default service type. It allocates a virtual IP reachable only within the cluster.

### 1.1 Service Definition

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: clusterip-svc
  namespace: default
spec:
  type: ClusterIP
  selector:
    role: nginx
  ports:
    - name: http
      port: 80
      targetPort: 80
```

```bash theme={null}
kubectl apply -f clusterip-svc.yaml
kubectl get svc clusterip-svc
# OUTPUT
# NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
# clusterip-svc    ClusterIP   10.102.157.139   <none>        80/TCP    5m
```

### 1.2 Testing Internal Access

Launch a temporary pod to test DNS and HTTP:

```bash theme={null}
kubectl run -i --tty --rm debug --image=curlimages/curl --restart=Never -- sh
```

Inside the debug pod:

```bash theme={null}
nslookup clusterip-svc.default.svc.cluster.local
curl http://clusterip-svc.default.svc.cluster.local
# Should return the NGINX welcome page
```

<Callout icon="lightbulb">
  ClusterIP services are only reachable from within the Kubernetes cluster. Use them for internal microservice communication.
</Callout>

***

## 2. NodePort

NodePort exposes a Service on each Node’s IP at a static port, allowing external traffic.

### 2.1 Service Definition

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: nodeport-svc
  namespace: default
spec:
  type: NodePort
  selector:
    role: nginx
  ports:
    - name: http
      port: 80
      targetPort: 80
      nodePort: 30000
```

```bash theme={null}
kubectl apply -f nodeport-svc.yaml
kubectl get svc nodeport-svc
# OUTPUT
# NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)         AGE
# nodeport-svc     NodePort    10.98.229.84     <none>        80:30000/TCP    5m
```

### 2.2 Access via Node IP

1. Find a node’s IP address:
   ```bash theme={null}
   kubectl get node node01 -o jsonpath='{.status.addresses[?(@.type=="InternalIP")].address}'
   # e.g., 192.168.121.156
   ```
2. From outside the cluster:
   ```bash theme={null}
   curl http://192.168.121.156:30000
   ```
   This should return the NGINX welcome page.

<Callout icon="triangle-alert">
  Ensure that your cloud provider’s firewall or on-premise network allows traffic to the `nodePort` range (default 30000–32767).
</Callout>

### 2.3 Internal DNS Resolution

Within the cluster, you can still resolve the service by DNS:

```bash theme={null}
kubectl run -i --tty --rm debug --image=curlimages/curl --restart=Never -- sh
# Inside the pod:
nslookup nodeport-svc.default.svc.cluster.local
curl http://nodeport-svc.default.svc.cluster.local
```

***

## 3. Headless Service

A headless Service omits the cluster IP (`clusterIP: None`) and returns the IPs of individual pods directly.

### 3.1 Service Definition

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: headless-svc
  namespace: default
spec:
  clusterIP: None
  selector:
    role: nginx
  ports:
    - name: http
      port: 80
      targetPort: 80
```

```bash theme={null}
kubectl apply -f headless-svc.yaml
kubectl get svc headless-svc
# OUTPUT
# NAME            TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# headless-svc    ClusterIP   None         <none>        80/TCP    5m
```

### 3.2 DNS and Direct Pod Access

```bash theme={null}
kubectl run -i --tty --rm debug --image=curlimages/curl --restart=Never -- sh
```

Inside the debug pod:

```bash theme={null}
nslookup headless-svc.default.svc.cluster.local
for ip in $(nslookup headless-svc.default.svc.cluster.local | grep Address | awk '{print $2}'); do
  curl http://$ip
done
```

<Callout icon="lightbulb">
  Headless Services are ideal for stateful applications (e.g., databases) where you need direct pod access for persistent storage or custom load balancing.
</Callout>

***

## 4. ExternalName

ExternalName maps a Service to an external DNS name by returning a CNAME record.

### 4.1 Service Definition

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: externalname-svc
  namespace: default
spec:
  type: ExternalName
  externalName: httpbin.org
```

```bash theme={null}
kubectl apply -f externalname-svc.yaml
kubectl get svc externalname-svc
# OUTPUT
# NAME                 TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# externalname-svc     ExternalName   <none>       <none>        <none>    5m
```

### 4.2 Testing ExternalName

```bash theme={null}
kubectl run -i --tty --rm debug --image=curlimages/curl --restart=Never -- sh
# Inside the pod:
curl http://externalname-svc.default.svc.cluster.local/get
# This request is forwarded to httpbin.org/get
```

<Callout icon="lightbulb">
  ExternalName does not proxy traffic through the cluster—it simply performs a DNS CNAME lookup. Use this to reference external APIs or services.
</Callout>

***

## Further Reading & References

* [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Service Types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)
* [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/00c6db37-72b0-44e1-8c3a-81e22c8d8af6/lesson/a007ca25-61da-47e0-bd8c-d81bd96cfc86" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/00c6db37-72b0-44e1-8c3a-81e22c8d8af6/lesson/a3dadd51-f6ef-4e99-aa01-2f84e56582b4" />
</CardGroup>


# Demo Troubleshooting Internal Networking

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Kubernetes-Services/Demo-Troubleshooting-Internal-Networking/page

This guide teaches diagnosing and resolving internal networking issues in Kubernetes using Cilium CNI and troubleshooting techniques for Pods and Services.

In this step-by-step guide, you’ll learn how to diagnose and resolve internal networking issues in Kubernetes using Cilium CNI, NetworkPolicies, and core troubleshooting techniques for Pods and Services. These best practices help ensure cluster connectivity and reliable application delivery.

## Table of Contents

1. [Verify CNI Pod Health](#1-verify-cni-pod-health)\
   1.1 [Using the Cilium CLI](#11-using-the-cilium-cli)\
   1.2 [Running `cilium-debug`](#12-running-cilium-debug)\
   1.3 [Checking Node Connectivity](#13-checking-node-connectivity)
2. [Inspect Network Policies](#2-inspect-network-policies)\
   2.1 [Testing Egress Connectivity](#21-testing-egress-connectivity)
3. [Troubleshoot Pods and Services](#3-troubleshoot-pods-and-services)\
   3.1 [Checking Pod Status and Logs](#31-checking-pod-status-and-logs)\
   3.2 [Port-Forwarding to the Pod](#32-port-forwarding-to-the-pod)\
   3.3 [Verifying Service Endpoints](#33-verifying-service-endpoints)
4. [Summary](#4-summary)
5. [References](#5-references)

***

## 1. Verify CNI Pod Health

Start by confirming that all Cilium components are running in the `kube-system` namespace:

```bash theme={null}
kubectl get pods -n kube-system
```

Sample output:

```bash theme={null}
NAME                                   READY   STATUS    RESTARTS   AGE
cilium-6xfl8                           1/1     Running   0          3m11s
cilium-9qzr8                           1/1     Running   0          3m11s
cilium-operator-58684c48c9-4rntb       1/1     Running   0          3m11s
coredns-76f75df574-964d                1/1     Running   0          2m54s
```

Cilium consists of:

* A **DaemonSet** (`cilium-<pod>`) on each node
* A single **operator** pod managing cluster-wide CRDs

Inspect operator logs to catch any errors or warnings:

```bash theme={null}
kubectl logs -n kube-system cilium-operator-58684c48c9-4rntb
```

<Frame>
  ![The image shows a log output from a Kubernetes system, detailing operations related to Cilium, including node taints, pod scheduling, and garbage collection processes.](https://kodekloud.com/kk-media/image/upload/v1752880343/notes-assets/images/Kubernetes-Networking-Deep-Dive-Demo-Troubleshooting-Internal-Networking/kubernetes-cilium-log-output-details.jpg)
</Frame>

For agent diagnostics, view a Cilium DaemonSet pod log:

```bash theme={null}
kubectl logs -n kube-system cilium-6xfl8
```

### 1.1 Using the Cilium CLI

If you have the **Cilium CLI** installed, quickly check cluster health:

```bash theme={null}
cilium status
```

Example:

```plaintext theme={null}
Cilium:                OK
Operator:              OK
DaemonSet cilium:      Desired: 2, Ready: 2/2, Available: 2/2
```

### 1.2 Running `cilium-debug`

Run the built-in debug tool to gather component status:

```bash theme={null}
kubectl exec -n kube-system cilium-6xfl8 -- cilium-debug status
```

Key checks include KVStore, API server connectivity, IPAM, and overall cluster health:

```plaintext theme={null}
Kubernetes:              Ok      1.29 (v1.29.0) [linux/amd64]
Cilium:                  Ok      1.15.3
Cluster health:         2/2 reachable (2024-07-21T20:18:25Z)
```

### 1.3 Checking Node Connectivity

Validate inter-node connectivity with `cilium-health`:

```bash theme={null}
kubectl exec -n kube-system cilium-6xfl8 -- cilium-health status
```

```plaintext theme={null}
Kubernetes:         Ok      1.29 (v1.29.0)
Cilium:             Ok      1.15.3
Cilium health:      2/2 reachable (2024-07-21T20:18:25Z)
```

***

## 2. Inspect Network Policies

NetworkPolicies can block unintended traffic flows. List all policies across namespaces:

```bash theme={null}
kubectl get networkpolicies.networking.k8s.io -A
```

| NAMESPACE | NAME                | POD-SELECTOR | AGE   |
| --------- | ------------------- | ------------ | ----- |
| default   | default-deny-egress | \<none>      | 7m12s |

Describe a restrictive policy:

```bash theme={null}
kubectl describe networkpolicies.networking.k8s.io default-deny-egress -n default
```

```plaintext theme={null}
PodSelector: <none>    # Applies to all pods in this namespace
Policy Types: Egress
Egress: <none>         # Denies all egress traffic
```

<Callout icon="triangle-alert">
  Deleting or modifying NetworkPolicies in production can expose workloads. Always validate in a non-production namespace first.
</Callout>

### 2.1 Testing Egress Connectivity

Launch a temporary pod to test outbound access:

```bash theme={null}
kubectl run --rm -i --tty debug \
  --image=curlimages/curl \
  --restart=Never \
  -- curl www.google.com --connect-timeout 2
```

* If the request hangs, the policy is blocking egress.
* To restore connectivity, delete the policy:

```bash theme={null}
kubectl delete networkpolicy default-deny-egress -n default
```

Re-run the curl test to confirm successful egress.

***

## 3. Troubleshoot Pods and Services

### 3.1 Checking Pod Status and Logs

List application pods:

```bash theme={null}
kubectl get pods
```

If a pod is running but not behaving, inspect its details and events:

```bash theme={null}
kubectl describe pod nginx-deployment-56fcf95486-7d2dw
```

<Frame>
  ![The image shows a terminal output displaying Kubernetes pod details, including conditions, volumes, and events related to the deployment and startup of an Nginx container.](https://kodekloud.com/kk-media/image/upload/v1752880344/notes-assets/images/Kubernetes-Networking-Deep-Dive-Demo-Troubleshooting-Internal-Networking/kubernetes-pod-details-nginx-container.jpg)
</Frame>

Follow up by streaming the logs:

```bash theme={null}
kubectl logs -f nginx-deployment-56fcf95486-7d2dw
```

### 3.2 Port-Forwarding to the Pod

Test direct connectivity by forwarding local port 8080 to the pod’s port 80:

```bash theme={null}
kubectl port-forward nginx-deployment-56fcf95486-7d2dw 8080:80
```

Open your browser or use `curl http://localhost:8080` to verify the service response.

### 3.3 Verifying Service Endpoints

Services provide stable access to Pods. If port-forward works on the pod but fails on the Service:

1. Describe the Service:

   ```bash theme={null}
   kubectl describe svc nginx-service
   ```

2. If you see `Endpoints: \<none>`, the selector may not match any Pods.

3. Check the Pod labels:

   ```bash theme={null}
   kubectl get pod nginx-deployment-56fcf95486-7d2dw \
     -o=jsonpath='{.metadata.labels}'
   ```

4. Edit the Service selector to match the Pod labels:

   ```bash theme={null}
   kubectl edit svc nginx-service
   # Update selector from app=nginx-website to app=nginx
   ```

5. Confirm the endpoint appears:

   ```bash theme={null}
   kubectl describe svc nginx-service
   # Endpoints: 10.0.0.247:80
   ```

6. Forward traffic via the Service:

   ```bash theme={null}
   kubectl port-forward svc/nginx-service 8080:80
   ```

***

## 4. Summary

In this tutorial, you learned how to:

* Validate **Cilium CNI** health with pod status, logs, and CLI tools (`cilium status`, `cilium-debug`, `cilium-health`).
* Inspect and test the impact of **NetworkPolicies** on egress traffic.
* Diagnose **Pod** and **Service** connectivity with `kubectl describe`, logs, port-forwarding, and selector verification.

Following these steps will help you quickly identify and resolve internal networking issues in your Kubernetes cluster.

***

## 5. References

* [Cilium Documentation](https://docs.cilium.io/)
* [Kubernetes Networking Concepts](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
* [Kubernetes API Reference: NetworkPolicy](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.29/#networkpolicy-v1-networking-k8s-io)
* [cilium CLI GitHub](https://github.com/cilium/cilium-cli)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/00c6db37-72b0-44e1-8c3a-81e22c8d8af6/lesson/fd0eb557-015f-4090-999d-ee11e7eaa847" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-networking/module/00c6db37-72b0-44e1-8c3a-81e22c8d8af6/lesson/00eed1e5-013f-4b11-82dd-604cb24288d8" />
</CardGroup>
