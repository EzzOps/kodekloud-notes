# Kubernetes Namespaces

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Kubernetes-Resources/Kubernetes-Namespaces/page

This lesson explains Kubernetes namespaces, their importance in resource management, and how to use them effectively in a cluster environment.

Welcome to this lesson on Kubernetes namespaces. Understanding namespaces is essential for managing resources and policies within a single Kubernetes cluster, especially in production environments. In this article, we use an everyday analogy to clarify the role and importance of namespaces.

Imagine two boys named Mark. Within their own households, family members use only first names. However, outsiders refer to them by their full names (e.g., Mark Smith and Mark Williams) to avoid confusion. Similarly, in Kubernetes, each namespace acts like a separate household with its own rules and resources.

## Default and System Namespaces

So far, you have been creating objects like Pods, Deployments, and Services in a single namespace—the default namespace, which is automatically created when the cluster is set up. In addition, Kubernetes creates several other namespaces at startup:

* **kube-system:** Contains critical Pods and Services (such as networking solutions and DNS) that are isolated from the user to prevent accidental modifications.
* **kube-public:** Contains resources that should be accessible to all users.

For smaller or learning environments, you might continue working in the default namespace. However, in enterprise or production setups, namespaces become crucial. For instance, if you have both development and production environments sharing the same cluster, isolating resources via separate namespaces can prevent accidental interference.

Below is a diagram that illustrates how different namespaces provide isolation:

<Frame>
  ![The image illustrates Kubernetes namespaces for isolation, showing five labeled houses: kube-system, Default, kube-public, Dev, and Prod, each containing a circle, triangle, and square.](https://kodekloud.com/kk-media/image/upload/v1752880676/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Kubernetes-Namespaces/frame_180.jpg)
</Frame>

Each namespace can enforce its own set of policies and resource quotas. The following diagram demonstrates how various environments (Default, Prod, Dev) are allocated resources such as nodes and containers:

<Frame>
  ![The image illustrates Kubernetes namespace resource limits, showing different environments (Default, Prod, Dev) with nodes and containers, highlighting resource allocation and management.](https://kodekloud.com/kk-media/image/upload/v1752880677/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Kubernetes-Namespaces/frame_200.jpg)
</Frame>

## DNS Service Discovery within Namespaces

Within a namespace, Pods and Services can address each other directly by name. For example, if a web application Pod needs to connect to a database service in the same namespace, it can simply use the service’s name. If the service is in a different namespace, the fully qualified DNS name must be used. For example, if a web Pod in the default namespace connects to a DB service in the dev namespace, the DNS name would be:

  DB-service.dev.svc.cluster.local

In this DNS name:

* "cluster.local" is the default domain of the Kubernetes cluster.
* "svc" indicates the service subdomain.
* The namespace and the service name follow.

## Operational Aspects and Kubectl Commands

Let’s explore some operational tasks using `kubectl` commands.

### Connecting to a Service Using DNS

Below is an example Python snippet that connects to a database service by referencing its DNS name:

```python theme={null}
mysql.connect("db-service.dev.svc.cluster.local")
```

### Listing Pods in Specific Namespaces

By default, the command `kubectl get pods` lists Pods in the default namespace. To view Pods in a different namespace (e.g., kube-system), append the `--namespace` option:

```bash theme={null}
kubectl get pods
```

Output:

```text theme={null}
NAME    READY   STATUS    RESTARTS   AGE
Pod-1   1/1     Running   0          3d
Pod-2   1/1     Running   0          3d
```

```bash theme={null}
kubectl get pods --namespace=kube-system
```

Output:

```text theme={null}
NAME                                      READY   STATUS    RESTARTS   AGE
coredns-78fcd6894-92d52                  1/1     Running   7          7d
coredns-78fcd6894-jx25g                   1/1     Running   7          7d
etcd-master                               1/1     Running   7          7d
kube-apiserver-master                     1/1     Running   7          7d
kube-controller-manager-master            1/1     Running   7          7d
kube-flannel-ds-amd64-hz4cf                1/1     Running   14         7d
kube-proxy-48btn                          1/1     Running   7          7d
kube-proxy-98db4                          1/1     Running   7          7d
kube-proxy-jjrsbs                         1/1     Running   7          7d
kube-scheduler-master                     1/1     Running   7          7d
```

<Callout icon="lightbulb">
  Remember, if you want to list Pods across all namespaces, use:

  ```bash theme={null}
  kubectl get pods --all-namespaces
  ```
</Callout>

### Creating Pods in Specific Namespaces

When you create a Pod using a definition file, it will be created in the default namespace unless specified otherwise.

To create a Pod using the definition file in the default namespace:

```bash theme={null}
kubectl create -f pod-definition.yml
```

Output:

```text theme={null}
pod/myapp-pod created
```

To create a Pod in a different namespace (e.g., dev), specify the namespace on the command line:

```bash theme={null}
kubectl create -f pod-definition.yml --namespace=dev
```

Output:

```text theme={null}
pod/myapp-pod created
```

Below is an example of a Pod definition file without a specified namespace:

```yaml theme={null}
