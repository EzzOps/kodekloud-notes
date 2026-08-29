# Check the Deployment replicas
kubectl get deployments
# Output example:
# NAME            READY   UP-TO-DATE   AVAILABLE   AGE
# Find the LoadBalancer’s public IP
kubectl get service
# NAME            TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)         AGE
# kodekloudapp    LoadBalancer   10.0.199.121    20.247.251.108  80:30895/TCP    73m
# kubernetes      ClusterIP      10.0.0.1        <none>          443/TCP         124m
```

***

## 2. Scale to 5 replicas

Increase your Deployment to five pods:

```bash theme={null}
kubectl scale deployment kodekloudapp --replicas=5
kubectl get deployment kodekloudapp
# NAME            READY   UP-TO-DATE   AVAILABLE   AGE
# kodekloudapp    5/5     5            5           76m
```

### Validate load balancing

Open three incognito browser windows and navigate to your Service’s public IP. You should see traffic routed to different pods:

![The image shows three browser windows displaying the "KodeKloudApp" homepage with a welcome message, system name, and IP address highlighted in yellow. Each window has a different system name and IP address.](https://kodekloud.com/kk-media/image/upload/v1752869529/notes-assets/images/Azure-Kubernetes-Service-Scaling-the-Deployment-using-kubectl/kodekloudapp-homepage-browser-windows.jpg)

***

## 3. Scale to the pod limit (30 replicas)

When you created the AKS cluster, you configured Azure CNI with a maximum of 30 pods per node. Let’s push the Deployment to that limit:

```bash theme={null}
kubectl scale deployment kodekloudapp --replicas=30
kubectl get deployment kodekloudapp
# NAME            READY   UP-TO-DATE   AVAILABLE   AGE
# kodekloudapp    16/30   30           16          78m
```

Only 16 pods are running; the rest remain `Pending`:

```bash theme={null}
kubectl get pods
# NAME                           READY   STATUS    RESTARTS   AGE
# kodekloudapp-677fc758c5-5k92g  0/1     Pending   0          57s
# kodekloudapp-677fc758c5-bbp84  0/1     Pending   0          57s
# ...
```

### Filter non-running pods

List pods that aren’t in the `Running` phase:

```bash theme={null}
kubectl get pods --field-selector=status.phase!=Running
```

### Inspect pod scheduling events

Describe one pending pod to see why it isn’t scheduled:

```bash theme={null}
kubectl describe pod kodekloudapp-677fc758c5-5k92g
```

In the **Events** section you’ll find:

```text theme={null}
Warning  FailedScheduling   2m     default-scheduler   0/1 nodes are available: 1 Too many pods.
Normal   NotTriggerScaleUp  110s   cluster-autoscaler  max node group size reached
```

***

## 4. Namespaces and system pods

AKS uses several namespaces to isolate workloads. System pods in `kube-system` count toward your per-node limit.

```bash theme={null}
kubectl get namespaces
# NAME              STATUS   AGE
# default           Active   129m
# kube-node-lease   Active   129m
# kube-public       Active   129m
# kube-system       Active   129m
```

### Namespace overview

| Namespace       | Purpose                     | Pod Count |
| --------------- | --------------------------- | --------- |
| default         | User applications           | 16        |
| kube-node-lease | Node heartbeat leases       | 0         |
| kube-public     | Public config and resources | 0         |
| kube-system     | Core cluster services       | 12+       |

```bash theme={null}
kubectl get pods --namespace kube-system
# NAME                                               READY   STATUS    RESTARTS   AGE
# ama-logs-rs-7f8bcb7c6f-5dlqq                       1/1     Running   0          131m
# coredns-59b6bf8b4f-lwt4c                           1/1     Running   0          131m
# metrics-server-7d74d8758-wfsdd                     2/2     Running   0          130m
# ...
```

> **triangle-alert** Azure CNI assigns IPs from your VNet based on the `--max-pods` setting at cluster creation. **You cannot change this limit post-creation**.

***

## Next steps

To work around the per-node pod limit, consider:

* Deploying multiple node pools with different `--max-pods` settings
* Switching to Kubenet or Azure CNI Overlay networks
* Splitting workloads across separate namespaces and node pools

***

## Links and References

* [Kubernetes Scaling Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#scaling-a-deployment)
* [AKS Networking Concepts](https://learn.microsoft.com/azure/aks/concepts-network)
* [Azure CNI IP Management](https://learn.microsoft.com/azure/aks/configure-azure-cni)

- [Watch Video](https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/2e4891fe-2f53-4239-9ab9-8b15ba4c6369/lesson/9448e603-60d1-4b69-9175-3ae44984a0d8)


# Scaling the Nodes using Azure CLI

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Working-with-AKS/Scaling-the-Nodes-using-Azure-CLI/page

This article explains how to scale Azure Kubernetes Service nodes using Azure CLI and discusses autoscaling components.

Our Azure Kubernetes Service (AKS) cluster is configured to support up to 30 pods, but only 16 are currently running. Before we scale the nodes manually, let’s review how AKS autoscaling works and when you might need to intervene.

## AKS Autoscaling Components

AKS provides two core autoscaler types to ensure your workloads have the right resources:

| Autoscaler                      | Purpose                                                                | Scope                       |
| ------------------------------- | ---------------------------------------------------------------------- | --------------------------- |
| Cluster Autoscaler              | Adds or removes nodes based on unschedulable pods and node utilization | Node pool level             |
| Horizontal Pod Autoscaler (HPA) | Adjusts pod replica count based on real-time CPU/memory metrics        | Deployment/ReplicaSet level |

### Cluster Autoscaler

The Cluster Autoscaler watches for pending pods that cannot be scheduled due to insufficient node capacity. When required, it scales out the node pool by adding new VMs. Conversely, when nodes are underutilized, it can remove nodes after cordoning and draining them.

> **triangle-alert** If you set both the minimum and maximum node count to the same value, the Cluster Autoscaler cannot expand or shrink your node pool.

### Horizontal Pod Autoscaler (HPA)

The HPA relies on the Kubernetes Metrics Server to monitor pod resource usage (CPU, memory, custom metrics, etc.). When usage crosses user-defined thresholds, HPA automatically increases or decreases the number of pod replicas.

#### How HPA Works

1. Polls metrics every 60 seconds by default.
2. Retrieves current resource usage from the Metrics Server.
3. Compares usage against your target thresholds.
4. Adjusts the replica count via the deployment controller.

![The image illustrates the process of a Cluster Autoscaler using a Horizontal Pod Autoscaler (HPA) in an Azure Kubernetes Service (AKS) cluster, detailing how it adjusts pod replicas based on resource metrics and user-specified thresholds.](https://kodekloud.com/kk-media/image/upload/v1752869530/notes-assets/images/Azure-Kubernetes-Service-Scaling-the-Nodes-using-Azure-CLI/cluster-autoscaler-hpa-aks-process.jpg)

> **lightbulb** You can customize the HPA polling interval and thresholds in your `HorizontalPodAutoscaler` manifest.

## Manually Scaling the AKS Node Pool

Since our Cluster Autoscaler is locked to a fixed node count (1–1), we’ll use Azure CLI to increase the pool to two nodes.

### 1. Verify System Pods

Run the following commands to confirm that system components are healthy:

```bash theme={null}
kubectl get pods --namespace kube-node-lease
kubectl get pods --namespace kube-public
kubectl get pods --namespace kube-system
```

Example output:

```bash theme={null}
NAME                                      READY   STATUS    RESTARTS   AGE
coredns-596bbf8b84-lwt4c                  1/1     Running   0          131m
metrics-server-7d7ad478s-wfdd             2/2     Running   0          130m
kube-proxy-dx4s4                          1/1     Running   0          131m
...
```

### 2. Scale the Node Pool

Use `az aks scale` to adjust the node count:

```bash theme={null}
az aks scale \
  --resource-group RG1-KodeKloud-AKS \
  --name AKS1-KodeKloudApp \
  --node-count 2
```

This command will provision a second VM in your AKS node pool. Provisioning may take a few minutes.

### 3. Confirm Two Ready Nodes

After scaling, verify the node count:

```bash theme={null}
kubectl get nodes
```

You should see two nodes, both in the `Ready` state.

### 4. Verify Pod Scheduling

Finally, ensure all pods are scheduled across the nodes:

```bash theme={null}
kubectl get pods --all-namespaces
```

Pending pods should now be distributed on the new node.

## Scaling Down

When you reduce your workload (for example, scaling your deployment replicas down to two), you may want to shrink the node pool back to one. Since our Cluster Autoscaler remains disabled, we need to scale down manually:

```bash theme={null}
az aks scale \
  --resource-group RG1-KodeKloud-AKS \
  --name AKS1-KodeKloudApp \
  --node-count 1
```

This command will cordon and drain the extra node, then remove it from the pool.

## Links and References

* [AKS Cluster Autoscaler Documentation](https://docs.microsoft.com/azure/aks/cluster-autoscaler)
* [Horizontal Pod Autoscaler (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
* [Azure CLI `az aks scale`](https://docs.microsoft.com/cli/azure/aks#az_aks_scale)
* [Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)

- [Watch Video](https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/2e4891fe-2f53-4239-9ab9-8b15ba4c6369/lesson/f3613b23-8e96-4f3a-8e24-56028569b74c)
