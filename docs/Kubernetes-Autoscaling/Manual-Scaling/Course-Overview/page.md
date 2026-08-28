# Course Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Manual-Scaling/Course-Overview/page

Overview of Kubernetes autoscaling covering HPA VPA Cluster Autoscaler CPA and KEDA, with practical patterns, hands-on examples, and best practices for resilient scalable workloads

Welcome.

This lesson covers Kubernetes autoscaling — how to automatically adjust application and cluster capacity so your workloads remain resilient and responsive as traffic changes. You’ll learn when to scale, which autoscaler to use, and practical patterns to avoid common pitfalls.

Imagine you run an online store and traffic spikes during a flash sale. If capacity doesn’t increase quickly enough, pages slow or become unavailable and users abandon their carts. Autoscaling prevents that by increasing resources when demand rises and decreasing them when demand falls, keeping costs under control while preserving performance.

<Frame>
  <img alt="A presentation slide titled &#x22;Identifying the Need for Scaling&#x22; showing an illustrated online store on a large monitor with customers shopping. On the right it lists problems to scale for: &#x22;Website slows down&#x22; and &#x22;Customers can't access.&#x22;" />
</Frame>

Autoscaling behaves like a thermostat for your infrastructure: it observes load (metrics or events) and adjusts capacity so applications meet their service levels. In Kubernetes this can mean scaling application replica counts, resizing container resource requests/limits, or adding and removing nodes.

At a high level:

* Your applications run inside Pods on worker nodes.
* The control plane schedules Pods onto nodes.
* When load increases, you may need more Pod replicas and/or more nodes to host them.
* Different autoscalers handle these responsibilities: some scale Pods, others right-size resources, and others manage the underlying node pool.

<Frame>
  <img alt="A diagram titled &#x22;K8s Autoscaling&#x22; showing a Kubernetes cluster with multiple worker-node pods (some highlighted) arranged inside the cluster. Arrows from a green &#x22;Traffic&#x22; circle point to the cluster, illustrating incoming traffic and autoscaling." />
</Frame>

What we'll cover in this course

* Definitions and scaling goals: when to scale horizontally vs vertically, and how to measure success.
* Horizontal Pod Autoscaler (HPA): scale replicas using CPU, memory, custom, or external metrics.
* Vertical Pod Autoscaler (VPA): recommend or apply container resource requests/limits to right-size Pods.
* Cluster Proportional Autoscaler (CPA): scale cluster-level or add-on replicas proportionally to node count.
* Cluster Autoscaler (and alternatives like Karpenter): add/remove nodes based on pending Pods and scheduling constraints.
* KEDA (Kubernetes Event-Driven Autoscaler): scale based on event sources (message queues, streams) and enable scale-to-zero patterns.
* Hands-on examples and recommended patterns to avoid conflicts and instability.

<Frame>
  <img alt="A slide titled &#x22;Course Content&#x22; showing a colorful roadmap of Kubernetes autoscaling topics with connected circular icons and arrows. The items listed are Introduction to Scaling, Horizontal Pod Autoscaler, Vertical Pod Autoscaler, Cluster Proportional Autoscaler, and Kubernetes Event-Driven Autoscaling (KEDA) Scaling." />
</Frame>

Autoscaler summary

| Autoscaler                            |                                             What it changes | Typical use case                                                                    | Docs / Notes                                                                                 |
| ------------------------------------- | ----------------------------------------------------------: | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Horizontal Pod Autoscaler (HPA)       |       Replica count of Deployments/ReplicaSets/StatefulSets | Scale application instances based on metrics (CPU/memory/custom/external)           | [HPA docs](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)       |
| Vertical Pod Autoscaler (VPA)         |                          Container resource requests/limits | Right-size container resources for stable workloads (not for sudden replica bursts) | [VPA overview](https://github.[SECRET_REDACTED]-pod-autoscaler) |
| Cluster Proportional Autoscaler (CPA) |                    Replica counts for cluster-level add-ons | Scale DNS, monitoring, or other control-plane add-ons relative to node count        | Useful for system components                                                                 |
| Cluster Autoscaler                    |                           Node pool size (add/remove nodes) | Ensure pending Pods can be scheduled by adjusting node count                        | [Cluster Autoscaler](https://cluster-autoscaler.kubernetes.io/)                              |
| KEDA                                  | Triggers for scaling (integrates with HPA or ScaledObjects) | Event-driven scaling based on queue/message lengths or custom event sources         | [KEDA](https://keda.sh/)                                                                     |

A few clarifying points

* HPA adjusts the number of Pod replicas for Deployments, ReplicaSets, and StatefulSets and supports built-in (CPU/memory), custom, and external metrics.
* VPA adjusts container resource requests and/or limits to right-size Pods. VPA does not increase replica counts — use HPA for replica-based scale-out.
* CPA targets cluster-level services and scales their replicas relative to node count (helpful for DNS, logging, and monitoring add-ons).
* Cluster Autoscaler (and alternatives like Karpenter on AWS) changes node count based on unschedulable Pods and cloud-provider scaling policies.
* KEDA connects to external event sources (Kafka, SQS, Azure Queue, Prometheus, etc.) and exposes metrics or triggers that drive scaling, including scale-to-zero.

<Callout icon="warning">
  Avoid uncontrolled interaction between HPA and VPA: if both modify the same resource targets (for example, container CPU requests), they can create oscillations. Use recommended patterns—like VPA in "recommend" mode with HPA controlling replica count—or split responsibilities by workload type.
</Callout>

We’ll include hands-on examples for manual and automated scaling, plus practical tips to avoid common issues (metric selection, cooldowns, target utilization, and resource fragmentation). Follow along to learn when to use HPA, VPA, CPA, Cluster Autoscaler, and KEDA so your applications remain available during spikes and efficient during low load.

<Callout icon="lightbulb">
  By the end of this course you'll understand how these autoscalers interact, which to use for different problems, and implementation best practices so applications stay available under changing load.
</Callout>

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Cluster Autoscaler](https://cluster-autoscaler.kubernetes.io/)
* [Karpenter (AWS alternative)](https://karpenter.sh/)
* [KEDA — Event-Driven Autoscaling](https://keda.sh/)
* [Vertical Pod Autoscaler (VPA) repo](https://github.[SECRET_REDACTED]-pod-autoscaler)

Ready to get started with the first hands-on lesson?

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/66710f67-c094-4a4c-b718-4a031d1ddebe/lesson/7605b2e1-8fbb-4b8c-849e-8f6a8c02f064" />
</CardGroup>
