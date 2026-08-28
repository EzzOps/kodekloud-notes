# Connect to a local service in the default namespace
mysql.connect("db-service")
```

To reach a service in another namespace—say `dev`—use the fully qualified domain name:

```python theme={null}
mysql.connect("db-service.dev.svc.cluster.local")
```

Kubernetes automatically provisions DNS entries in the format:

```text theme={null}
<service>.<namespace>.svc.cluster.local
```

* `svc` is the services subdomain
* `cluster.local` is the default cluster domain

<Callout icon="lightbulb">
  You can customize the cluster domain via the `--cluster-domain` flag in kubelet and kube-apiserver configurations.
</Callout>

## Working with Namespaces in kubectl

### 1. Listing Resources

```bash theme={null}
# Pods in the current namespace (default)
kubectl get pods

# Pods in kube-system
kubectl get pods --namespace=kube-system

# All pods across all namespaces
kubectl get pods --all-namespaces
```

### 2. Creating a Pod in a Specific Namespace

Given `pod-definition.yml`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
    tier: frontend
spec:
  containers:
    - name: nginx
      image: nginx:latest
```

Create in the `default` namespace:

```bash theme={null}
kubectl create -f pod-definition.yml
```

Or in `dev`:

```bash theme={null}
kubectl create -f pod-definition.yml --namespace=dev
```

To bake the namespace into your manifest:

```yaml theme={null}
metadata:
  name: myapp-pod
  namespace: dev
```

### 3. Defining a Namespace

Option A: A YAML manifest (`namespace-dev.yml`):

```yaml theme={null}
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

```bash theme={null}
kubectl apply -f namespace-dev.yml
```

Option B: One-liner:

```bash theme={null}
kubectl create namespace dev
```

### 4. Switching Context Namespace

Rather than appending `--namespace=`, set a default in your current context:

```bash theme={null}
kubectl config set-context --current --namespace=dev
```

<Callout icon="triangle-alert">
  Switching contexts affects all future `kubectl` commands in your shell. Confirm with `kubectl config view --minify`.
</Callout>

## Resource Quotas

Limit CPU, memory, and object counts to prevent a single namespace from monopolizing cluster resources:

```yaml theme={null}
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "10"
    limits.memory: 10Gi
```

Apply with:

```bash theme={null}
kubectl apply -f compute-quota.yaml
```

## References

* [Kubernetes Namespace Documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
* [Kubernetes Service DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

Practice creating, configuring, and managing namespaces to master multi-tenant Kubernetes clusters!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/2a7326ae-573b-4f39-b961-5604903fdc26" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/893b87ac-1758-4ac5-9f51-36641dde56ac" />
</CardGroup>


# Isolation and Segmentation Resource Quotas Limits

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Isolation-and-Segmentation-Resource-Quotas-Limits/page

This article covers Kubernetes resource management, including defining requests and limits for CPU and memory, and enforcing resource quotas across namespaces.

In this lesson, we dive deep into Kubernetes resource management. You’ll learn how to define requests and limits for CPU and memory, enforce defaults with LimitRange, and cap overall consumption with ResourceQuota to ensure fair usage across namespaces.

## Resource Scheduling in Kubernetes Clusters

A Kubernetes scheduler assigns pods to nodes based on available CPU and memory. For instance, in a three-node cluster, if you submit a pod requesting 2 CPUs and 1 Gi of memory, the scheduler will place it on the first node that meets these requirements (node-2 in this example). Pods remain in the Pending state if no node has sufficient resources. You can verify this by running:

```bash theme={null}
kubectl describe pod <pod-name>
```

and checking for scheduling errors.

<Frame>
  ![The image shows a Kubernetes scheduling error message indicating insufficient CPU resources, with a visual representation of CPU and memory usage across three nodes.](https://kodekloud.com/kk-media/image/upload/v1752880785/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Isolation-and-Segmentation-Resource-Quotas-Limits/kubernetes-scheduling-error-cpu-usage.jpg)
</Frame>

## Defining Resource Requests

A resource request specifies the minimum CPU or memory a container needs. The scheduler uses these values to make placement decisions.

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  containers:
  - name: simple-webapp-color
    image: simple-webapp-color
    ports:
    - containerPort: 8080
    resources:
      requests:
        memory: "4Gi"
        cpu: "2"
```

CPU requests can be specified in cores (e.g., `"2"`) or millicores (e.g., `"200m"` = 0.2 CPU). The smallest unit is `1m`.

<Callout icon="lightbulb">
  One Kubernetes CPU core maps to one AWS vCPU, one GCP core, one Azure core, or one hyperthread.
</Callout>

<Frame>
  ![The image is a slide titled "Resource - CPU," showing a diagram of a CPU with a list detailing equivalences: 1 AWS vCPU, 1 GCP Core, 1 Azure Core, and 1 Hyperthread.](https://kodekloud.com/kk-media/image/upload/v1752880786/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Isolation-and-Segmentation-Resource-Quotas-Limits/resource-cpu-diagram-equivalences.jpg)
</Frame>

## Memory Units and Conversions

Memory can be defined using SI (e.g., `G`, `M`) or binary suffixes (e.g., `Gi`, `Mi`):

* `G`  = 10⁹ bytes
* `Gi` = 2³⁰ bytes
* `M`  = 10⁶ bytes
* `Mi` = 2²⁰ bytes

<Frame>
  ![The image is a slide titled "Resource - Memory" showing a diagram labeled "MEM" with "1G" and a list of byte conversions for gigabytes, megabytes, kilobytes, gibibytes, mebibytes, and kibibytes.](https://kodekloud.com/kk-media/image/upload/v1752880788/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Isolation-and-Segmentation-Resource-Quotas-Limits/resource-memory-diagram-byte-conversions.jpg)
</Frame>

## Setting Resource Limits

By default, containers have no resource caps and can consume all available CPU and memory. To prevent extreme usage, define both `requests` and `limits`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  containers:
  - name: simple-webapp-color
    image: simple-webapp-color
    ports:
    - containerPort: 8080
    resources:
      requests:
        memory: "1Gi"
        cpu: "1"
      limits:
        memory: "2Gi"
        cpu: "2"
```

* Exceeding the CPU limit results in throttling (slower CPU cycles).
* Exceeding the memory limit triggers an OOM kill, terminating the container.

<Callout icon="triangle-alert">
  If a container exceeds its memory `limits`, Kubernetes will kill it with `OOMKilled`. Always set realistic memory limits to avoid unexpected terminations.
</Callout>

<Frame>
  ![The image illustrates the concept of exceeding resource limits, showing a diagram with CPU and memory constraints, and indicating actions like "THROTTLE" and "TERMINATE" when limits are surpassed, leading to "OOM (Out Of Memory)."](https://kodekloud.com/kk-media/image/upload/v1752880789/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Isolation-and-Segmentation-Resource-Quotas-Limits/resource-limits-cpu-memory-diagram.jpg)
</Frame>

## Default Behavior and Best Practices

Without explicit settings, pods may compete unpredictably for node resources. Below is a summary of CPU allocation behaviors under different configurations:

| Configuration           | Behavior                                                                  | Use Case                                  |
| ----------------------- | ------------------------------------------------------------------------- | ----------------------------------------- |
| No requests, no limits  | A single pod can saturate all CPU resources.                              | Testing or non-critical workloads.        |
| No requests, limits     | The `request` defaults to the `limit`, guaranteeing the capped CPU share. | Enforcing a strict CPU ceiling.           |
| Requests and limits set | Guarantees `requests` and allows bursting up to `limits`.                 | Balanced workloads with predictable load. |
| Requests set, no limits | Guarantees `requests` and allows bursting (throttled by other pods).      | Flexible, bursty workloads.               |

<Frame>
  ![The image illustrates different CPU behavior scenarios with varying configurations of requests and limits, using bar graphs to show resource allocation. It compares cases with no requests or limits, requests with limits, and requests without limits.](https://kodekloud.com/kk-media/image/upload/v1752880790/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Isolation-and-Segmentation-Resource-Quotas-Limits/cpu-behavior-scenarios-bar-graphs.jpg)
</Frame>

Memory allocation follows similar patterns, except bursting beyond the limit always results in an immediate OOM kill.

<Frame>
  ![The image is a diagram illustrating memory behavior with different scenarios of requests and limits, using colored blocks to represent memory allocation.](https://kodekloud.com/kk-media/image/upload/v1752880791/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Isolation-and-Segmentation-Resource-Quotas-Limits/memory-behavior-diagram-requests-limits.jpg)
</Frame>

## Enforcing Defaults with LimitRange

To automatically apply default `requests` and `limits` within a namespace, create a LimitRange. This helps maintain consistency and prevents pods from deploying without resource settings.

```yaml theme={null}
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-defaults
spec:
  limits:
  - type: Container
    min:
      cpu: "100m"
      memory: "500Mi"
    max:
      cpu: "1"
      memory: "1Gi"
    defaultRequest:
      cpu: "500m"
      memory: "1Gi"
    default:
      cpu: "500m"
      memory: "1Gi"
```

<Callout icon="lightbulb">
  `LimitRange` only affects pods created after the object is applied. Existing pods retain their original settings.
</Callout>

## Namespace-Wide Quotas with ResourceQuota

When you need to cap total resource consumption per namespace, use ResourceQuota. This object restricts the aggregate of `requests` and `limits` across all pods in the namespace:

```yaml theme={null}
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "4Gi"
    limits.cpu: "10"
    limits.memory: "10Gi"
```

This ensures no single team or namespace can exceed its allocated share.

<Frame>
  ![The image contains a list of documentation references related to managing memory, CPU, and API resources in Kubernetes, with URLs for further reading.](https://kodekloud.com/kk-media/image/upload/v1752880792/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Isolation-and-Segmentation-Resource-Quotas-Limits/kubernetes-memory-cpu-api-docs.jpg)
</Frame>

## Links and References

* [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-container/)
* [LimitRange Documentation](https://kubernetes.io/docs/concepts/policy/limit-range/)
* [ResourceQuota Documentation](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
* [Kubernetes Official Docs](https://kubernetes.io/docs/)

Complete the hands-on labs to reinforce these concepts. Happy clustering!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/b9af56d3-b4cb-4a43-b8e7-d47ad8ed06e0" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/8e27c03a-c53e-45c3-a0bc-decf1e4e7a50" />
</CardGroup>
