# CNI in Kubernetes

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Container-Orchestration-Networking/CNI-in-Kubernetes/page

This article explains how Kubernetes uses the Container Network Interface to configure network plugins for containers.

Welcome to this lesson on how Kubernetes uses the Container Network Interface (CNI) to configure network plugins for containers. In earlier lessons, we covered the fundamentals of network namespaces, Docker networking, and the emergence of CNI along with its plugins.

![The image lists prerequisites for a topic, including network namespaces in Linux, Docker networking, Container Network Interface (CNI), and CNI plugins.](https://kodekloud.com/kk-media/image/upload/v1752880564/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-CNI-in-Kubernetes/frame_20.jpg)

In this article, you'll learn how Kubernetes is configured to utilize these network plugins. CNI defines the responsibilities for container runtimes, and in this context, Kubernetes creates container network namespaces and links them to the appropriate network plugins. A dedicated component within Kubernetes first creates the containers and then invokes the specified CNI plugin based on the configuration.

![The image outlines key points about Container Network Interface, including network namespace creation, network attachment, plugin invocation, and JSON configuration, alongside a Kubernetes logo.](https://kodekloud.com/kk-media/image/upload/v1752880566/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-CNI-in-Kubernetes/frame_50.jpg)

## Kubelet Configuration for CNI

The kubelet service on each node is the key component for configuring the CNI plugin. Within the kubelet service file, the network plugin is set to CNI and options are provided that specify the directories for both CNI plugins and configuration files. Here is an example snippet from a kubelet service file:

```plaintext theme={null}
ExecStart=/usr/local/bin/kubelet \
    --config=/var/lib/kubelet/kubelet-config.yaml \
    --container-runtime=remote \
    --container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \
    --image-pull-progress-deadline=2m \
    --kubeconfig=/var/lib/kubelet/kubeconfig \
    --network-plugin=cni \
    --cni-bin-dir=/opt/cni/bin \
    --cni-conf-dir=/etc/cni/net.d \
    --register-node=true \
    --v=2
```

When you inspect the running kubelet process with a command like:

```bash theme={null}
ps -aux | grep kubelet
```

You will see that the network plugin is set to CNI along with additional options, such as:

* The CNI binaries directory (`/opt/cni/bin`), which contains executables for supported plugins (e.g., bridge, DHCP, flannel).
* The CNI configuration directory (`/etc/cni/net.d`), where the kubelet reads configuration files to determine which plugin to use.

For example, you can list the contents of these directories with the following commands:

```bash theme={null}
