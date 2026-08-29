# replicaset-definition.yml
selector:
  matchLabels:
    tier: front-end

# pod-definition.yml
metadata:
  name: myapp-pod
  labels:
    tier: front-end
```

The ReplicaSet uses its selector to monitor and manage pods with the label `tier: front-end`. This concept of labels and selectors is widely used throughout Kubernetes to maintain order and efficiency.

## Scaling ReplicaSets

Scaling ReplicaSets allows your application to adapt to changing demand. Suppose you started with three replicas and later need to scale up to six. There are multiple approaches:

1. **Edit the Definition File:**\
   Update the `replicas` field in your ReplicaSet definition file to six, then run:

   ```bash theme={null}
   kubectl replace -f replicaset-definition.yml
   ```

2. **Use the Scale Command:**\
   Alternatively, use the `kubectl scale` command:

   ```bash theme={null}
   kubectl scale --replicas=6 -f replicaset-definition.yml
   ```

   Or, if you prefer using the ReplicaSet name:

   ```bash theme={null}
   kubectl scale --replicas=6 replicaset/myapp-replicaset
   ```

> **lightbulb** Remember, if you use the scale command, the changes are updated only in the cluster state. The original definition file will continue to show the previous replica count until it is modified.

There are also advanced options for automatically scaling ReplicaSets based on load; however, that topic is outside the scope of this lesson.

## Summary of Commands

Below is a quick reference for essential kubectl commands used with ReplicaSets:

| Command             | Description                                             | Example                                                   |
| ------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| Create a ReplicaSet | Launch a new ReplicaSet from a definition file          | `kubectl create -f replicaset-definition.yml`             |
| List ReplicaSets    | View all ReplicaSets in your cluster                    | `kubectl get replicaset`                                  |
| List Pods           | Display all pods including those managed by ReplicaSets | `kubectl get pods`                                        |
| Delete a ReplicaSet | Remove a specific ReplicaSet                            | `kubectl delete replicaset myapp-replicaset`              |
| Update a ReplicaSet | Replace an existing ReplicaSet with a new configuration | `kubectl replace -f replicaset-definition.yml`            |
| Scale a ReplicaSet  | Adjust the number of replicas using a file              | `kubectl scale --replicas=6 -f replicaset-definition.yml` |

```bash theme={null}
kubectl create -f replicaset-definition.yml         # Create a ReplicaSet
kubectl get replicaset                                # List all ReplicaSets
kubectl get pods                                      # List pods, including those managed by ReplicaSets
kubectl delete replicaset myapp-replicaset            # Delete a specific ReplicaSet
kubectl replace -f replicaset-definition.yml          # Update a ReplicaSet using a file
kubectl scale --replicas=6 -f replicaset-definition.yml # Scale a ReplicaSet to 6 replicas using a file
```

![The image illustrates load balancing and scaling using Kubernetes, showing users accessing multiple pods managed by a replication controller across two nodes.](https://kodekloud.com/kk-media/image/upload/v1752880683/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-ReplicaSets/frame_110.jpg)

Understanding how labels, selectors, and ReplicaSets interact is crucial to maintain high availability and scalable deployments in your Kubernetes environment. This lesson has covered the fundamentals of replication controllers and ReplicaSets, along with their creation, updating, and scaling procedures.

![The image shows multiple "POD" icons arranged around a central icon, labeled "Labels and Selectors," likely illustrating a Kubernetes concept.](https://kodekloud.com/kk-media/image/upload/v1752880684/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-ReplicaSets/frame_690.jpg)

This concludes our discussion on ReplicaSets. Apply these concepts to ensure robust and scalable deployments in your Kubernetes cluster.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/509501a0-727a-41b9-b9a5-e022735c098e/lesson/6243236b-6a32-4e1e-94fb-e1c49de06fdd)


# Configuring Kubernetes Scheduler Profiles

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Scheduling/Configuring-Kubernetes-Scheduler-Profiles/page

This article explores Kubernetes scheduler profiles and their configuration through practical examples of Pod scheduling in a cluster.

In this article, we explore scheduler profiles and the inner workings of the Kubernetes scheduler using a practical example where a Pod is scheduled to one of four nodes in a Kubernetes cluster.

## Pod Definition Example

Below is an example of a Pod definition file. This Pod requires 10 CPU units and will only be scheduled on a node that meets or exceeds that capacity.

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  priorityClassName: high-priority
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      resources:
        requests:
          memory: "1Gi"
          cpu: 10
```

Each node in the cluster has a defined amount of available CPU. As Pods are created, they enter a scheduling queue where they are arranged based on the priority specified in their configuration. In this scenario, our Pod is assigned a high priority by using a PriorityClass object. Here is an example of how to create such a PriorityClass:

```yaml theme={null}
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "This priority class should be used for XYZ service pods only."
```

> **lightbulb** High-priority settings ensure that Pods with this classification are placed at the front of the scheduling queue.

## Scheduling Phases

The Pod scheduling process comprises three main phases:

1. **Filter Phase:**\
   In this phase, the scheduler eliminates nodes that do not satisfy the Pod’s resource requirements. For instance, if the first two nodes do not have the needed 10 CPU units available, they are filtered out.

2. **Scoring Phase:**\
   Nodes that pass the filter phase are then scored. The scheduler assigns each node a score based on factors such as the remaining CPU after allocating the Pod’s requirements. For example, if one node has 2 CPU units remaining while another has 6, the latter will receive a higher score.

3. **Binding Phase:**\
   In the final phase, the Pod is assigned to the node with the best score during the binding process.

## Key Plugins in the Scheduling Process

Plugins are integral to the Kubernetes scheduling process. Here are some examples:

* **Priority Sort Plugin:**\
  During the scheduling queue phase, this plugin orders Pods based on their assigned priority.

* **Node Resources Fit Plugin:**\
  This plugin is active during the filter phase to exclude nodes lacking sufficient resources. Additionally, during the scoring phase, this plugin re-evaluates nodes based on free resources.

* **Node Unschedulable Plugin:**\
  This plugin ensures that nodes marked as unschedulable do not have Pods assigned. For example, running the command:

  ```bash theme={null}
  controlplane ~ → kubectl describe node controlplane
  Name:               controlplane
  Roles:              control-plane
  CreationTimestamp:  Thu, 06 Oct 2022 06:19:57 -0400
  Taints:             node.kubernetes.io/unschedulable:NoSchedule
  Unschedulable:      true
  Lease:
  ```

  confirms that the node unschedulable plugin prevents Pod scheduling on such nodes.

* **Image Locality Plugin:**\
  This plugin is a soft preference during the scoring phase, favoring nodes that already contain the required container image.

* **Default Binder Plugin:**\
  In the binding phase, this plugin finalizes the Pod-to-node assignment.

Kubernetes' extensible design lets you customize active plugins at each extension point, including pre-filter, filter, post-filter, pre-score, score, reserve, pre-bind, and post-bind. You can also integrate custom plugins to meet specific requirements.

![The image outlines Kubernetes scheduling extension points, including Scheduling Queue, Filtering, Scoring, and Binding, with specific functions like queueSort, preFilter, and bind.](https://kodekloud.com/kk-media/image/upload/v1752880685/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Configuring-Kubernetes-Scheduler-Profiles/frame_380.jpg)

## Using Multiple Scheduling Profiles

Kubernetes’ extensibility is further demonstrated by its support for multiple scheduler profiles within a single scheduler binary. This feature, introduced in Kubernetes 1.18, simplifies process maintenance and reduces race conditions by eliminating the need for separate scheduler binaries (such as default scheduler, my-scheduler, and my-scheduler2).

Consider the following configuration files that define separate scheduler configurations with unique scheduler names:

```yaml theme={null}
