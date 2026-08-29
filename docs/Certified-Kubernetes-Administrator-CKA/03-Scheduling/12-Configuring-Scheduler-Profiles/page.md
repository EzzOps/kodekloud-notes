# Configuring Scheduler Profiles

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/Configuring-Scheduler-Profiles/page

This article explains configuring scheduler profiles in Kubernetes to customize scheduling behavior and manage multiple profiles within a single scheduler binary.

In this lesson, we dive into the concept of scheduler profiles and their configuration in Kubernetes. We will start with a refresher on how the Kubernetes scheduler functions, illustrated by a simple example where a pod is scheduled to one of several available nodes.

## How Scheduling Works

When a pod is defined, it enters a scheduling queue along with other pending pods. Consider a pod that requires 10 CPU; it will only be scheduled on nodes with at least 10 available CPUs. Additionally, pods with higher priorities are placed at the beginning of the queue. For instance, the following pod definition uses a high-priority class:

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

Before using this priority, you must create a priority class with a specific name and a priority value. Assigning a value like 1,000,000, for example, grants a very high priority. This ensures that pods with higher priorities are scheduled ahead of those with lower ones.

## Scheduling Phases

After being queued, pods progress through several phases:

1. **Filter Phase:** Nodes that cannot meet the pod's resource requirements (e.g., nodes lacking 10 CPUs) are filtered out.
2. **Scoring Phase:** Remaining nodes are scored based on resource availability after reserving the required CPU. For example, a node with 6 CPUs left scores higher than one with only 2.
3. **Binding Phase:** The pod is assigned to the node with the highest score.

### Key Scheduler Plugins

Several scheduler plugins play critical roles during these phases:

* **Priority Sort Plugin:** Sorts pods in the scheduling queue according to their priority.

* **Node Resources Fit Plugin:** Filters out nodes that do not have the needed resources.

* **Node Name Plugin:** Checks for a specific node name in the pod specification and filters nodes accordingly.

* **Node Unschedulable Plugin:** Excludes nodes marked as unschedulable. For instance, running commands like drain or cordon will set the unschedulable flag. An example node description is:

  ```bash theme={null}
  controlplane ~ → kubectl describe node controlplane
  Name:               controlplane
  Roles:              control-plane
  CreationTimestamp:  Thu, 06 Oct 2022 06:19:57 -0400
  Taints:             node.kubernetes.io/unschedulable:NoSchedule
  Unschedulable:      true
  Lease:
  ```

* **Scoring Plugins:** During the scoring phase, plugins (such as the Node Resources Fit and Image Locality plugins) assess each node's suitability. They assign scores rather than outright rejecting nodes.

* **Default Binder Plugin:** Finalizes the scheduling process by binding the pod to the selected node.

> **lightbulb** Kubernetes emphasizes extensibility, allowing you to modify the scheduling process via extension points at stages such as queueing, filtering, scoring, and binding.

The following image outlines the various extension points of the Kubernetes scheduler, including processes like the scheduling queue, filtering, scoring, and binding phases:

![The image outlines Kubernetes scheduler extension points: Scheduling Queue, Filtering, Scoring, and Binding, with specific functions like queueSort, preFilter, and bind.](../../../../images/kodekloud.com/kk-media/image/upload/v1752869885/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Configuring-Scheduler-Profiles/frame_380.jpg)

## Customizing Scheduler Behavior with Profiles

Rather than running separate scheduler binaries (like default scheduler, MyScheduler, and MyScheduler2) with distinct configuration files, Kubernetes 1.18 introduced support for multiple scheduling profiles within a single scheduler binary. This approach minimizes operational overhead and prevents potential race conditions that can arise when multiple processes schedule workloads on the same node.

### Profile Configuration

Each scheduler profile is defined within the scheduler configuration file and behaves like an independent scheduler. For example, here are several configuration snippets:

```yaml theme={null}
