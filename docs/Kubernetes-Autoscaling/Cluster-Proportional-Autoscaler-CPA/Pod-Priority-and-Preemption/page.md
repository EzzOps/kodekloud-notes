# Pod Priority and Preemption

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Cluster-Proportional-Autoscaler-CPA/Pod-Priority-and-Preemption/page

Explains Kubernetes Pod Priority and Preemption, using PriorityClass and preemptionPolicy to control scheduling and evictions so critical workloads run when cluster resources are scarce.

Welcome — this lesson explains Pod Priority and Preemption in Kubernetes: how the scheduler decides which workloads get cluster resources when capacity is limited, and how you can control that behavior using PriorityClass and `preemptionPolicy`.

Pod Priority and Preemption are scheduler features that help guarantee critical system components and high-value applications get scheduled and remain running when the cluster is under resource pressure. We'll use a concert-hall analogy to make the ideas easier to visualize.

Imagine a large concert hall where seats are limited. VIPs, regular guests, and staff all arrive over time. Without a clear priority system, staff and VIPs might not get seats, and the event could fail. In Kubernetes, seats are cluster resources (CPU, memory, etc.), and people are Pods; Priority and Preemption ensure important Pods get the resources they need.

<Frame>
  <img alt="A slide titled &#x22;Pod Priority – Introduction&#x22; showing a large screen above rows of stylized pod-shaped seats with small colored head icons. A legend at right labels the colors: green for VIPs, orange for regular guests, and blue for staff members." />
</Frame>

In Kubernetes terms:

* Seats = available cluster capacity (CPU, memory, ephemeral storage)
* People = Pods (workloads)
* Priority = how important a Pod is relative to others
* Preemption = evicting lower-priority Pods so higher-priority Pods can be scheduled

<Frame>
  <img alt="A slide titled &#x22;Kubernetes – Pod Priority&#x22; uses a concert-hall analogy: seats (resources like CPU/storage) on the left map to resources in a K8s cluster on the right, and people map to pods." />
</Frame>

Many clusters run low-priority workloads (batch jobs, dev/test workloads, CI runners). If the cluster fills up, these low-priority Pods can block scheduling of more important Pods. Preemption lets the scheduler evict those lower-priority Pods to free resources for higher-priority Pods.

<Frame>
  <img alt="A presentation slide titled &#x22;Kubernetes – Pod Priority&#x22; showing three numbered categories: K8s System-Critical Pods (Kube-API, DNS, CNI, CSI), Application-Critical Pods (payment processing system), and Low-Priority Pods (batch jobs, background worker)." />
</Frame>

Preemption is like asking a regular guest to vacate their seat so a VIP or staff member can sit. Kubernetes may evict lower-priority Pods to create space for higher-priority Pods when scheduling fails due to resource constraints.

<Frame>
  <img alt="A slide titled &#x22;Kubernetes – Preemption&#x22; showing a K8s cluster with rows of high‑priority and low‑priority pod icons, and several low‑priority pods marked as preempted and moved into a separate area to make room for higher‑priority pods." />
</Frame>

preemptionPolicy options

* Pods can control whether they may preempt lower-priority Pods via the `preemptionPolicy` field in the Pod spec.
* Two allowed values:

| preemptionPolicy       |                                                                              Behavior | Use case                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------ |
| `PreemptLowerPriority` |         (Default) This Pod may cause eviction of lower-priority Pods to be scheduled. | Use for workloads that must be scheduled even under pressure.                                          |
| `Never`                | This Pod will not preempt lower-priority Pods; it will not evict others to make room. | Use for pods that must not evict others (but note: they can still be evicted by higher-priority Pods). |

<Frame>
  <img alt="A presentation slide titled &#x22;Preemption Type&#x22; showing two rounded boxes explaining preemptionPolicy: &#x22;PreemptLowerPriority&#x22; (default, lets pods of that PriorityClass preempt lower-priority pods) and &#x22;Never&#x22; (explicitly set so pods cannot be evicted). The slide includes brief bullet points under each heading." />
</Frame>

<Callout icon="lightbulb">
  Preemption is enabled by default in Kubernetes. Use `preemptionPolicy: Never` only when you must ensure this Pod does not preempt other pods; it does not protect the Pod from being evicted by higher-priority pods.
</Callout>

How priorities are defined

* Kubernetes uses the PriorityClass resource to assign numeric priorities to pods.
* Higher numeric `value` = higher priority.
* Assign a PriorityClass by setting `priorityClassName` on the Pod (or Pod template inside a Deployment/StatefulSet/DaemonSet).

Example PriorityClass manifests:

```yaml theme={null}
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "This priority class is for critical pods."
```

```yaml theme={null}
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 500
globalDefault: false
description: "This priority class is for less critical pods."
```

Assigning priority to Pods and Deployments

Pod example:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: high-priority-pod
spec:
  priorityClassName: high-priority
  containers:
  - name: nginx
    image: nginx:stable
```

Deployment example (priority applied to Pods created by the Deployment):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: high-priority-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      priorityClassName: high-priority
      containers:
      - name: nginx
        image: nginx:stable
```

Kubernetes also includes several built-in PriorityClasses for system-critical components. These built-ins use very large numeric values so system pods outrank user pods.

<Frame>
  <img alt="A slide titled &#x22;Default Priority Class&#x22; showing a table of Kubernetes priority classes (system-node-critical, system-cluster-critical, default) with their priority values, descriptions, and purposes. It also lists the numeric values 2000001000, 2000000000, and 0." />
</Frame>

Quick reference table — typical priority classes

| PriorityClass name        | Typical value | Purpose                                            |
| ------------------------- | ------------: | -------------------------------------------------- |
| `system-node-critical`    |  `2000001000` | Node/system-critical components (reserved)         |
| `system-cluster-critical` |  `2000000000` | Cluster-critical system components                 |
| `default`                 |           `0` | Default for user pods when no PriorityClass is set |

Control preemption per-Pod

* To prevent a Pod from preempting lower-priority Pods, set `preemptionPolicy: Never` in the Pod spec.
* That does not prevent the Pod itself from being evicted by a higher-priority Pod.

Example: a low-priority Pod that will not preempt others:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: non-preemptible-pod
spec:
  priorityClassName: low-priority    # Using a low-priority class
  preemptionPolicy: Never            # This pod will not preempt lower-priority pods
  containers:
  - name: non-preemptible-container
    image: nginx:stable
```

Best practices and operational guidance

* Use PriorityClasses deliberately. Over-assigning high priority reduces scheduler flexibility.
* Reserve the highest numeric values for critical system components.
* Use `preemptionPolicy: Never` sparingly and only when necessary.
* Test preemption behavior in staging before applying critical PriorityClasses in production.
* Combine Priority/Preemption with resource requests/limits and PodDisruptionBudgets (PDBs) for predictable scheduling and resilience.

Summary

* Pod Priority ensures critical workloads are preferred by the scheduler when resources are scarce.
* Preemption frees resources for higher-priority Pods by evicting lower-priority Pods when necessary.
* Priority is defined with PriorityClass resources and assigned via `priorityClassName` in Pod specs.
* Use `preemptionPolicy` to control whether a Pod may evict lower-priority Pods.

Further reading and references

* Kubernetes scheduler concepts: [https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)
* PriorityClass API reference: [https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#priorityclass-v1-scheduling-k8s-io](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#priorityclass-v1-scheduling-k8s-io)
* PodDisruptionBudget: [https://kubernetes.io/docs/concepts/workloads/pods/disruptions/](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)

That concludes this lesson on Pod Priority and Preemption — thanks for learning with us.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/ad35ef0b-c572-4f9e-82e4-0865c98fd502/lesson/36e80af5-e217-461e-aa1a-6e2eb896fd9a" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/ad35ef0b-c572-4f9e-82e4-0865c98fd502/lesson/ff158bc1-0521-4651-bb2f-023a5bd43085" />
</CardGroup>
