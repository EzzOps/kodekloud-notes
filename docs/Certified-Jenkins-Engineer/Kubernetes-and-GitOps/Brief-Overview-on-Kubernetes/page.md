# Brief Overview on Kubernetes

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Kubernetes-and-GitOps/Brief-Overview-on-Kubernetes/page

This article provides an overview of Kubernetes architecture, including its components like Pods, Deployments, Services, and Ingress.

Kubernetes is an open-source container orchestration platform originally developed by Google and now maintained by the [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io). It automates deployment, scaling, and management of containerized applications across clusters of machines—physical or virtual.

## Kubernetes Cluster Architecture

A Kubernetes **cluster** consists of nodes that run containerized workloads. Nodes are classified as:

| Node Type          | Role                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| Control Plane Node | Manages the cluster’s desired state and runs the API server, controller manager, scheduler, etcd |
| Worker Node        | Hosts application workloads and runs kubelet, kube-proxy, and a container runtime                |

### Control Plane Components

* **API Server**\
  The central REST endpoint through which all cluster operations are performed.

* **Controller Manager**\
  Ensures the cluster’s actual state matches the desired state by running built-in controllers (e.g., Node Controller, Replication Controller).

* **Scheduler**\
  Assigns Pods to nodes based on resource requirements, affinity/anti-affinity rules, and other constraints.

* **etcd**\
  A highly available, distributed key-value store that persists all cluster data.

<Callout icon="triangle-alert">
  etcd is the single source of truth for your cluster. Ensure you have regular backups and secure access controls.
</Callout>

## Pods

A **Pod** is the smallest deployable unit in Kubernetes. It encapsulates one or more containers sharing:

* A common network namespace (IP address, port space)
* Shared storage volumes

In most scenarios, a Pod runs a single container. Pods are *ephemeral*: if one is terminated, Kubernetes removes it by default and does **not** recreate it unless managed by a higher-level controller.

<Callout icon="lightbulb">
  Use Deployments or ReplicaSets to ensure Pods are automatically recreated after failures.
</Callout>

Example: Define and create a simple Pod

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: sample-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
```

```bash theme={null}
kubectl apply -f sample-pod.yaml
```

## Deployments

**Deployments** provide declarative updates for Pods and ReplicaSets. You specify the desired state—such as the number of replicas and container images—and Kubernetes continuously works to achieve and maintain that state, handling rolling updates and rollbacks.

Example: Create a Deployment

```bash theme={null}
kubectl create deployment web-server --image=nginx:latest --replicas=3
```

## Services

A **Service** exposes a set of Pods as a network service. It provides stable IPs, DNS names, and load balancing.

| Service Type | Description                                                           | Example Command                                                                                           |
| ------------ | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| ClusterIP    | Internal-only service accessible within the cluster                   | `kubectl expose deployment web-server --port=80 --target-port=80`                                         |
| NodePort     | Exposes the service on each node’s IP at a static port                | `kubectl expose deployment web-server --type=NodePort --port=80`                                          |
| LoadBalancer | Provisions an external load balancer (cloud provider required)        | `kubectl expose deployment web-server --type=LoadBalancer --port=80`                                      |
| ExternalName | Maps the service to an external DNS name via the `externalName` field | See [ExternalName Service](https://kubernetes.io/docs/concepts/services-networking/service/#externalname) |

### LoadBalancer

A **LoadBalancer** service automatically provisions and configures an external load balancer—e.g., [AWS ELB](https://docs.aws.amazon.[SECRET_REDACTED]-is-load-balancer.html) or [GCP Load Balancing](https://cloud.google.com/load-balancing/docs). This simplifies external traffic routing but may incur additional costs for each exposed service.

<Callout icon="triangle-alert">
  LoadBalancer services often incur per-hour or per-GB data processing fees. Review your cloud provider’s pricing before use.
</Callout>

## Ingress

[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) provides HTTP and HTTPS routing into the cluster. It allows you to:

* Expose multiple services under a single IP or domain
* Define host- and path-based routing rules
* Terminate TLS/SSL connections

When using Ingress, Services are typically configured as `ClusterIP` so that the Ingress controller handles all external traffic.

<Frame>
  ![The image is a diagram illustrating the basics of Kubernetes architecture, showing the interaction between controller nodes, worker nodes, and various components like pods, services, and ingress.](https://kodekloud.com/kk-media/image/upload/v1752870879/notes-assets/images/Certified-Jenkins-Engineer-Brief-Overview-on-Kubernetes/kubernetes-architecture-diagram.jpg)
</Frame>

## References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/01d04ab3-0694-4c67-bd1a-c3eaaa8d64d3/lesson/d9f8b01c-c3ea-4fac-9567-b364b63a9fe6" />
</CardGroup>
