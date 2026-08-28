# Static Pods

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/Static-Pods/page

This lesson details static pods in Kubernetes, their configuration, and behavior in standalone and clustered environments.

In this lesson, we explore static pods in Kubernetes and how they operate independently of control plane components. Previously, we reviewed the Kubernetes architecture and explained the role of the kubelet as a primary component. Typically, the kubelet receives instructions from the kube-apiserver about which pods to run on its node. These decisions, made by the kube-scheduler and stored in the etcd data store, are standard in a clustered environment. But what happens when the kube-apiserver, kube-scheduler, and other control plane components are absent? How does the node function on its own?

Imagine being isolated at sea with no master or other nodes nearby. Can the kubelet still guide the node? The answer is yes. When the kubelet and a container runtime (such as Docker) are installed directly on the host without a Kubernetes cluster, the kubelet can independently manage the node. In this scenario, because there is no API server to provide pod details, you must supply the pod definition files directly to the kubelet.

<Callout icon="lightbulb">
  Static pods are created directly by the kubelet without the intervention of the API server or other control plane components.
</Callout>

The kubelet is configured to monitor a designated directory on the host where pod definition files are stored. The kubelet periodically scans this directory, reads available files, and creates the corresponding pods. It also monitors these pods and ensures they remain running. For example, if an application crashes, the kubelet restarts it; if an updated file is detected, the kubelet recreates the pod to apply the changes; and if a file is removed, the corresponding pod is also deleted. These pods, created solely by the kubelet, are known as static pods.

It's important to note that only pod-level resources can be created this way. Higher-level abstractions such as ReplicaSets, Deployments, or Services depend on other control plane components (e.g., the replication and deployment controllers) and cannot be managed via the static pod definition files.

## Configuring the Static Pods Directory

You can place static pods in any directory on the host. The directory location is provided to the kubelet at startup by using the `--pod-manifest-path` option. Below is an example configuration in the kubelet service file:

```bash theme={null}
ExecStart=/usr/local/bin/kubelet \
  --container-runtime=remote \
  --container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \
  --pod-manifest-path=/etc/kubernetes/manifests \
  --kubeconfig=/var/lib/kubelet/kubeconfig \
  --network-plugin=cni \
  --register-node=true \
  --v=2
```

Alternatively, you can specify a configuration file that includes the manifest directory path. For example:

```bash theme={null}
