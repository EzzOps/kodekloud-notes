# Kube Scheduler

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Core-Concepts/Kube-Scheduler/page

This article provides a comprehensive overview of the Kube Schedulers role in pod placement within Kubernetes.

Welcome to this comprehensive lesson on the Kube Scheduler, a core component of Kubernetes. In this guide, we delve into the scheduler’s role in determining on which node a pod should be placed. It is important to note that while the scheduler makes the placement decision, the actual creation of the pod on the selected node is carried out by the Kubelet.

## Scheduler Process Overview

The primary responsibility of the Kubernetes scheduler is to assign pods to nodes based on a series of criteria. This ensures that the selected node has sufficient resources and meets any specific requirements. For instance, different nodes may be designated for certain applications or come with varied resource capacities. When multiple pods and nodes are involved, the scheduler assesses each pod against the available nodes through a two-phase process: filtering and ranking.

### 1. Filtering Phase

In the filtering phase, the scheduler eliminates nodes that do not meet the pod's resource requirements. For example, nodes that lack sufficient CPU or memory are immediately excluded.

![The image illustrates a Kubernetes scheduler filtering nodes based on CPU availability, showing nodes with 4, 12, and 16 CPUs, and a container requiring 10 CPUs.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869723/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kube-Scheduler/frame_110.jpg)

As depicted above, the diagram demonstrates the elimination of nodes with insufficient resources, leaving only the candidate nodes that can accommodate the pod's needs.

### 2. Ranking Phase

After filtering, the scheduler enters the ranking phase. Here, it uses a priority function to score and compare the remaining nodes on a scale from 0 to 10, ultimately selecting the best match. For instance, if placing a pod on one node would leave six free CPUs (four more than an alternative node), that node is assigned a higher score and is chosen.

![The image illustrates the Kube-Scheduler process, showing node filtering and ranking, with nodes labeled by CPU capacity.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869724/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kube-Scheduler/frame_160.jpg)

This high-level overview outlines how Kubernetes efficiently filters and ranks nodes for optimal pod placement. The scheduler’s design is highly customizable, allowing you to develop your own scheduler if the need arises. For more advanced scheduling configurations—such as resource limits, taints and tolerations, node selectors, and affinity rules—refer to the [Kubernetes Documentation](https://kubernetes.io/docs/).

> **lightbulb** Customizing the scheduling process can help tailor your Kubernetes environment to meet specific workloads and performance requirements.

## Installing and Running the Kube Scheduler

To install the kube-scheduler, download the binary from the Kubernetes release page. Once downloaded and extracted, you can run it as a service by specifying the scheduler configuration file. Below is a sample command for downloading the binary and an example systemd service configuration:

```bash theme={null}
wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kube-scheduler
```

Below is an example of the systemd service configuration for the kube-scheduler:

```bash theme={null}
