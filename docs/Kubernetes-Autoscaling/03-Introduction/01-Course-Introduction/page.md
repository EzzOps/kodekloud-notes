# Course Introduction

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Introduction/Course-Introduction/page

A practical course teaching Kubernetes autoscaling techniques including manual scaling, HPA, VPA, CPA and KEDA with hands on labs and debugging for production readiness

Kubernetes has become the de facto platform for running cloud-native applications and is often referred to as the "Linux of the cloud." As AI services scale, Kubernetes plays a central role powering platforms like Poe, Anthropic's Claude, ChatGPT, and many other AI-driven products. Demand for Kubernetes expertise continues to grow — a 2022 Indeed survey reported Kubernetes as the fastest-growing job search term (173% year-over-year), and that momentum carried through 2023 and 2024.

<Frame>
  <img alt="A slide from an Indeed survey showing ranked tech skills by year-over-year job search growth, with Kubernetes #1 at 173% growth. The list highlights fast-growing cloud and e-commerce skills like Magento, Verilog, Golang and others." />
</Frame>

This course focuses on building practical autoscaling skills for Kubernetes so you can demonstrate credibility and value in production environments. I'm Michael Forrest, and I will guide you through core autoscaling concepts, architectures, and hands-on labs designed to help you experiment, iterate, and learn by doing.

<Callout icon="lightbulb">
  Ensure your `kubectl` is configured to point at a working Kubernetes cluster before attempting the lab commands used in this lesson.
</Callout>

To inspect API server flags (for example, admission-related flags) on a control-plane pod, you can run:

```bash theme={null}
kubectl exec -n kube-system kube-apiserver-controlplane \
  -- kube-apiserver -h | grep enable-admission
```

Course roadmap

* Manual scaling — develop intuition for how workloads react to replica changes and pod lifecycle events.
* Horizontal Pod Autoscaler (HPA) — automation for scaling replicas based on CPU, memory, custom metrics, and external metrics.
* Vertical Pod Autoscaler (VPA) — adjust pod resource requests and limits with recommendations or automated updates.
* Cluster Proportional Autoscaler (CPA) — scale control-plane or infrastructure controller replicas proportionally to cluster size.
* KEDA — event-driven autoscaling for external event sources (queues, cron, Redis, etc.).

Course roadmap (summary table)

| Topic                                 | Purpose                                            | Key concepts / examples                                                          |
| ------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------- |
| Manual scaling                        | Understand pod lifecycle under scale operations    | `kubectl scale`, `kubectl get pods`, readiness/probes                            |
| HPA (Horizontal Pod Autoscaler)       | Autoscale replica counts by metrics                | CPU/memory, custom metrics, external metrics, metrics-server, Prometheus Adapter |
| VPA (Vertical Pod Autoscaler)         | Tune pod resource requests/limits                  | Recommendation vs. update modes (`Off`, `Auto`, `Initial`)                       |
| CPA (Cluster Proportional Autoscaler) | Scale controller replicas with cluster growth      | Node/CPU-based ladders, include/exclude unschedulable nodes                      |
| KEDA                                  | Event-driven autoscaling based on external sources | Redis queue length, cron, Kafka, Azure/AWS integrations                          |

Manual scaling and pods
Manually scaling deployments and inspecting pod status is the first hands-on step. Use `kubectl` to observe how pods are created, initialized, and become ready.

```bash theme={null}
kubectl get pods
