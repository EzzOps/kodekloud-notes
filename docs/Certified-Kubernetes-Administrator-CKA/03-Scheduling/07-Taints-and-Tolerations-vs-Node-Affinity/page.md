# kubelet.service
ExecStart=/usr/local/bin/kubelet \
  --container-runtime=remote \
  --container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \
  --config=kubeconfig.yaml \
  --kubeconfig=/var/lib/kubelet/kubeconfig \
  --network-plugin=cni \
  --register-node=true \
  --v=2
```

```yaml theme={null}
# kubeconfig.yaml
staticPodPath: /etc/kubernetes/manifests
```

Many clusters created using kubeadm adopt this approach. When inspecting an existing cluster, first check for the `--pod-manifest-path` option in the kubelet service file. If it is not present, look for the `--config` option to locate the configuration file and check its `staticPodPath` setting.

You can verify the status of static pods using container runtime commands. For instance, running the Docker command below on a host shows the containers spawned by static pods:

```bash theme={null}
docker ps
CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS               NAMES
8e5d4c4db7b6        busybox                 "sh -c 'echo Hello K…'"  20 seconds ago      Up 20 seconds       k8s_myapp-container_myapp-pod-host01_default_48e37fb432f2e06350e76786bd0bac66_0
f6737e1149cb        k8s.gcr.io/pause:3.1     "/pause"                 24 seconds ago      Up 23 seconds       k8s_POD_myapp-pod-host01_default_48e37fb432f2e06350e76786bd0bac66_0
```

In a standalone scenario, use `docker ps` because the kube-apiserver is not available to process Kubernetes API requests.

## Behavior When Part of a Cluster

When a node is part of a Kubernetes cluster, the kube-apiserver instructs the kubelet to create pods via its HTTP API endpoint. In this mixed mode, the kubelet handles pod definitions provided both from the static pod directory and from the API server. Whenever the kubelet creates a static pod in this configuration, it also creates a mirror object in the kube-apiserver. This mirror object is read-only and can be viewed with `kubectl get pods`, but you cannot modify or delete it through the API. To update a static pod, modify the file in the node’s manifest directory.

For example, running the command below on the master node will display the static pod mirror:

```bash theme={null}
kubectl get pods
NAME                READY   STATUS              RESTARTS   AGE
static-web-node01   0/1     ContainerCreating   0          29s
```

Notice that the pod name includes the node name (e.g., "node01") to indicate its origin.

![The image illustrates the architecture of static pods in Kubernetes, showing components like kube-apiserver, ETCD cluster, kube-scheduler, and kubelet with YAML files for pod configuration.](https://kodekloud.com/kk-media/image/upload/v1752869910/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Static-Pods/frame_340.jpg)

## Static Pods vs. DaemonSets

A common question that arises is how static pods differ from DaemonSets. The table below summarizes the key differences between the two:

| Feature                    | Static Pods                                          | DaemonSets                                                 |
| -------------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| Creation Source            | Directly managed by the kubelet                      | Managed by the DaemonSet controller via the kube-apiserver |
| Control Plane Involvement  | No API server interaction                            | Requires kube-apiserver communication                      |
| Use Case                   | Typically used for critical control plane components | Ensures a copy of a pod runs on every node                 |
| Interaction with Scheduler | Ignored by the kube-scheduler                        | Ignored by the kube-scheduler                              |

Static pods are especially useful for deploying control plane components themselves. Once the kubelet is installed on all master nodes, you can create pod definition files for essential components like the API server and controller manager. By placing these files in the designated manifest folder, the kubelet ensures they are running as pods and restarts them automatically if they fail. When you check the pods in the kube-system namespace, you'll see these control plane components running as pods—a standard configuration in clusters set up using kubeadm.

![The image compares Static PODs and DaemonSets, highlighting their creation sources, deployment purposes, and interaction with the Kube-Scheduler.](https://kodekloud.com/kk-media/image/upload/v1752869911/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Static-Pods/frame_490.jpg)

> **lightbulb** This lesson has detailed the concept of static pods, their configuration, and their behavior both in standalone and clustered environments. Using static pods is a simplified yet powerful method to manage critical workloads without relying on the full Kubernetes control plane.

That concludes this detailed discussion on static pods. Be sure to review and practice working with static pods in your upcoming tests to reinforce these concepts.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/d79e79e4-5561-47aa-8bf3-de3dfb96b8e1)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/c10cee47-7e3e-45ff-a283-9261360cdd4b)


# Taints and Tolerations vs Node Affinity

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/Taints-and-Tolerations-vs-Node-Affinity/page

This article explains controlling pod placement in Kubernetes using taints, tolerations, and node affinity for optimal scheduling and exclusive node usage.

Welcome to this article where we explain how to control pod placement in a Kubernetes cluster by combining taints, tolerations, and node affinity. In our example, we have three nodes and three pods, each identified by a distinct color—blue, red, and green. Our objective is to ensure that each pod is scheduled on the node with the corresponding color while preventing unwanted workloads from running on these dedicated nodes.

> **lightbulb** In Kubernetes, taints and tolerations are primarily used to repel pods from nodes unless they explicitly tolerate the taint, whereas node affinity is used to attract pods to nodes that satisfy specific label criteria.

## Using Taints and Tolerations

To begin, we apply a taint to each node that marks it with its respective color (blue, red, or green). Then, each pod is configured with a corresponding toleration. With this setup, the Kubernetes scheduler places the pods on nodes that accept their tolerations. For instance, the green pod is placed on the green node and the blue pod on the blue node.

![The image illustrates "Taints and Tolerations" with colored icons and server symbols labeled Blue, Red, Green, and Other, likely representing a Kubernetes concept.](https://kodekloud.com/kk-media/image/upload/v1752869912/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Taints-and-Tolerations-vs-Node-Affinity/frame_50.jpg)

However, while taints and tolerations ensure that pods with matching tolerations are admitted by the nodes, they do not guarantee exclusive scheduling. Consequently, a pod (for example, a red pod) might still be scheduled on an untainted node, leading to undesired placements.

## Using Node Affinity

To overcome the limitation of taints and tolerations, we leverage node affinity. This method involves labeling each node with its specific color and then configuring node selectors or advanced affinity rules in the pod specifications. Node affinity ensures a pod lands only on the node with the matching label.

While node affinity directs pods to the correct nodes, it does not restrict other pods from also being scheduled on these nodes. This means that although our desired pods are correctly placed, the nodes might still host pods not meant for them.

## Combining Taints and Tolerations with Node Affinity

For exclusive node usage, combining both strategies is the optimal solution. The integration works as follows:

1. Apply taints on nodes and specify corresponding tolerations in pod configurations to block any pod without the proper toleration.
2. Use node affinity rules to ensure that each pod is only scheduled on a node with a matching label.

This combined approach dedicates the nodes exclusively to the intended pods, assuring correct pod assignments and preventing interference by other workloads.

![The image illustrates "Taints/Tolerations and Node Affinity" with colored boxes and server icons labeled Blue, Red, Green, and Other.](https://kodekloud.com/kk-media/image/upload/v1752869913/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Taints-and-Tolerations-vs-Node-Affinity/frame_130.jpg)

> **lightbulb** In summary, leveraging both taints/tolerations and node affinity in Kubernetes ensures precise pod scheduling. This approach is particularly useful in multi-tenant clusters where exclusive node usage is critical.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/072fadcf-5696-4577-89c4-66900d61b524)
