# priority-class.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for mission critical pods"
globalDefault: true

# pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  containers:
    - name: nginx
      image: nginx
      ports:
        - containerPort: 8080
  priorityClassName: high-priority
```

## Pod Priority and Preemption

Consider a scenario where there are two workloads waiting to be scheduled: a critical application with a priority of 7 and a job with a priority of 5. With available resources, the higher priority critical application is scheduled first. If resources remain, the lower priority job is also scheduled.

<Frame>
  ![The image illustrates the concept of pod priority, showing a comparison between "Jobs" with priority 5 and "Critical Apps" with priority 7, distributed across three servers.](https://kodekloud.com/kk-media/image/upload/v1752869898/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Priority-Classes/pod-priority-comparison-jobs-apps.jpg)
</Frame>

Now, suppose a new job with a priority of 6 is submitted when no extra resources are available. Whether this new Pod preempts (or evicts) an existing lower priority Pod depends on the preemption policy defined in its priority class. By default, Kubernetes applies the `PreemptLowerPriority` policy, meaning the scheduler will evict lower priority Pods to free up resources for higher priority ones.

The following YAML snippet demonstrates setting the preemption policy to `PreemptLowerPriority`:

```yaml theme={null}
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for mission critical pods"
preemptionPolicy: PreemptLowerPriority
```

If you prefer that a higher priority Pod waits for resources rather than preempting lower priority Pods, set the `preemptionPolicy` to `Never`. This change ensures the Pod remains in the scheduling queue without evicting any existing Pods:

```yaml theme={null}
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for mission critical pods"
preemptionPolicy: Never
```

:::note Additional Information
For more details on Kubernetes scheduling and priority, refer to the [Kubernetes documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/).
:::

This concludes the discussion on priority classes. You can now implement these concepts to better manage workload priorities in your Kubernetes cluster.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/d2a37ba9-458c-4f68-843e-28a83a851176" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/f5299818-5c75-429b-b751-154cefa82109" />
</CardGroup>


# Scheduling Section Introduction

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/Scheduling-Section-Introduction/page

This article provides a comprehensive lesson on Kubernetes scheduling concepts and techniques for managing pods and workloads effectively.

Hello, my name is Mumshad Mannambeth, and I welcome you to this comprehensive lesson on scheduling in Kubernetes. In this module, you will explore essential scheduling concepts and techniques that empower you to manage pods and workloads effectively. Previously, we briefly introduced the installation and configuration of the Kubernetes scheduler. Now, we will dive deeper into the various customization options that influence scheduler behavior through a series of practical, hands-on labs.

## Overview

In this lesson, you will learn about the following topics:

* **Manual Scheduling:** Understand how to manually schedule pods to specific nodes.
* **DaemonSets:** Discover how to run a copy of a pod on each node in your cluster.
* **Labels and Selectors:** Learn how to use labels and selectors to manage and target specific groups of pods.
* **Resource Requests and Limits:** See how resource constraints affect scheduling decisions.
* **Multiple Schedulers:** Explore configuration strategies for running multiple schedulers within a cluster.
* **Viewing Scheduler Events:** Learn how to monitor and troubleshoot scheduler events for optimal performance.

<Callout icon="lightbulb">
  Each section of this lesson is complemented by hands-on labs designed to reinforce your understanding and give you real-world experience with Kubernetes scheduling.
</Callout>

Let's get started with the first topic—Manual Scheduling—and progressively build your expertise in Kubernetes scheduling.

<Frame>
  ![The image lists course objectives, including core concepts, scheduling, logging, application lifecycle management, cluster maintenance, security, storage, networking, installation, and troubleshooting.](https://kodekloud.com/kk-media/image/upload/v1752869904/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Scheduling-Section-Introduction/frame_50.jpg)
</Frame>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/cd124bdf-9911-4cc1-8177-f2d8b6dfd2a0/lesson/5e3dfca7-9f2f-41ea-bc35-0be1e71da107" />
</CardGroup>
