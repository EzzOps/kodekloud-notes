# HPA Architecture

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Horizontal-Pod-Autoscaler-HPA/HPA-Architecture/page

Explains Kubernetes Horizontal Pod Autoscaler architecture, metric sources, adapters, control loop, and examples for resource custom and external metrics to enable automated pod scaling.

In this lesson we continue exploring the Horizontal Pod Autoscaler (HPA) by breaking down its architecture and the runtime workflow that takes metrics from various sources and turns them into scaling decisions. This guide focuses on how HPA consumes metrics (resource, custom, and external), how adapters expose those metrics to Kubernetes, and how the HPA control loop reconciles replica counts.

At a high level the HPA:

* Automatically adjusts the number of pod replicas for a target workload (Deployment, StatefulSet, ReplicaSet, etc.).
* Can use resource metrics (CPU/memory), custom in-cluster metrics, or external metrics from third-party monitoring/APM systems.
* Requires metric adapters or a Metrics Server to expose non-native metric sources through the Kubernetes Metrics APIs.

Primary HPA components

* HPA resource definition: YAML manifest that designates the target workload, minimum/maximum replicas, and the metric targets.
* Metrics API availability & collection sources: the Kubernetes metric API endpoints that the HPA controller queries.
* Metrics adapters: bridge external or custom metric sources into Kubernetes via `custom.metrics.k8s.io` or `external.metrics.k8s.io`.

<Frame>
  <img alt="A slide titled &#x22;HPA Architecture Framework&#x22; showing a diagram with a central HPA box above a dashed boundary containing four colored component boxes labeled &#x22;HPA Resource Definition,&#x22; &#x22;Metrics API Availability,&#x22; &#x22;Metrics Collection Source,&#x22; and &#x22;Metrics Adapters.&#x22; The image visually represents the components of a Horizontal Pod Autoscaler architecture." />
</Frame>

HPA resource definition example (CPU utilization)

* This HPA keeps average CPU utilization across pods at 50%, with a minimum of 2 replicas and a maximum of 10.

```yaml theme={null}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-deployment-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

How metrics flow into HPA

* HPA queries the Metrics APIs through the kube-apiserver.
* Metrics may come from the built-in Metrics Server (resource metrics), from in-cluster sources exposed via a custom metrics adapter, or from external systems via an external metrics adapter.
* Adapters translate or proxy metrics so the HPA controller sees them through Kubernetes-standard API groups.

Resource metrics (native)

* The Metrics Server exposes CPU and memory metrics under `metrics.k8s.io`. HPA reads these via the kube-apiserver and uses them for resource-based scaling.

<Frame>
  <img alt="A slide titled &#x22;Metrics Collection – Resource&#x22; showing a Kubernetes cluster diagram. It depicts the Metrics Server sending CPU/memory metrics via the Kube API to the HPA (HPA Definition), which adjusts Workload (Deployment) scaling accordingly." />
</Frame>

Custom metrics (in-cluster application metrics)

* Custom metrics are application-generated metrics exposed inside the cluster and surfaced to Kubernetes via `custom.metrics.k8s.io`.
* A custom metrics adapter scrapes or fetches metrics from application endpoints, Prometheus, or other in-cluster sources and exposes them to the custom metrics API.
* HPA can target these metrics to scale based on application-specific indicators such as requests per second, queue length, or active users.

Example HPA using a pods-level custom metric `http_requests_per_second`:

* This HPA targets an average of `100` requests per second across pods.

```yaml theme={null}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
```

<Frame>
  <img alt="A diagram of custom metrics collection in a Kubernetes cluster showing HPA Definition and the Kube API interacting with a Custom Metrics Adaptor and a Workload (Deployment). It illustrates scraping application metrics (e.g., number of users, active orders) and adjusting workloads based on those metrics." />
</Frame>

External metrics (outside the cluster)

* External metrics originate outside the Kubernetes cluster (cloud provider metrics, external APMs like New Relic, Datadog, Dynatrace).
* An external metrics adapter runs in-cluster and bridges those external sources into `external.metrics.k8s.io`.
* HPA queries these metrics through the kube-apiserver to make scaling decisions.

Example HPA using an external metric `newrelic.app.response_time`:

* If the external metric value exceeds `500`, the HPA will factor that into scaling behavior.

```yaml theme={null}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: External
      external:
        metric:
          name: newrelic.app.response_time
        target:
          type: Value
          value: "500"
```

<Frame>
  <img alt="A diagram titled &#x22;Metrics Collection – External&#x22; showing a Kubernetes cluster flow where an HPA definition and the Kube API interact with an External Adaptor and External Data Source. Arrows indicate the adaptor fetching metrics from the metrics server/external source and the Kube API adjusting the workload (Deployment) based on the HPA." />
</Frame>

Metrics API overview

* `metrics.k8s.io` — resource metrics (CPU, memory) from Metrics Server.
* `custom.metrics.k8s.io` — application-generated metrics exposed via a custom metrics adapter.
* `external.metrics.k8s.io` — externally generated metrics surfaced via an external metrics adapter.

| Metrics API               | Typical Source                          | Use Case / Examples                                                        |
| ------------------------- | --------------------------------------- | -------------------------------------------------------------------------- |
| `metrics.k8s.io`          | Metrics Server                          | CPU and memory resource metrics for pods/nodes                             |
| `custom.metrics.k8s.io`   | Prometheus, App endpoints (via adapter) | `http_requests_per_second`, queue depth, per-pod custom KPIs               |
| `external.metrics.k8s.io` | Cloud provider APIs, APMs (via adapter) | `newrelic.app.response_time`, Datadog metrics, cloud load balancer metrics |

<Frame>
  <img alt="A slide titled &#x22;Metrics API&#x22; showing two panels: custom.metrics.k8s.io (left) and external.metrics.k8s.io (right). The left panel notes application-generated metrics that originate within the cluster, while the right panel notes external-generated metrics that originate outside the cluster." />
</Frame>

Adapters and common implementations

* Prometheus Adapter: exposes Prometheus metrics as `custom.metrics.k8s.io` — common for Prometheus-based stacks.
* Cloud/Third-party adapters: Datadog, New Relic, and other providers supply external metric adapters to surface APM data into Kubernetes.

> **lightbulb** Make sure a Metrics Server (or equivalent) and the required metric adapters are installed and functioning. Without them, HPA cannot retrieve the metrics it needs to make scaling decisions.

HPA control loop and operation flow

* The HPA controller runs a periodic control loop (sync period configurable via controller manager flags). Each iteration:
  1. Retrieves metrics from the Metrics APIs.
  2. Evaluates current values against configured targets.
  3. Calculates the desired replica count when thresholds are breached.
  4. Updates the target workload (Deployment/StatefulSet) with the new replica count, subject to scale policies.

<Frame>
  <img alt="A colorful infographic titled &#x22;HPA Operation Flow&#x22; showing four connected stages: Metrics Retrieval, Evaluation, Scaling Calculation, and Update Deployment. Each stage is represented by a colored circular icon and curved arrows with simple line illustrations (chart, checklist, calculator, deployment)." />
</Frame>

Additional considerations and best practices

* Deploying Metrics Server: Some distributions omit it by default. Confirm `metrics-server` is running and reachable.
* Scaling policy tuning: Use multiple metrics and configure scale-up/scale-down policies and stabilization windows to prevent oscillation.
* Aggressiveness: Determine how aggressive scaling should be based on your cost, latency and SLA requirements.
* Testing and observability: Validate HPA behavior with load tests and monitor HPA events (`kubectl describe hpa <name>`) and adapter logs.

<Frame>
  <img alt="A presentation slide titled &#x22;HPA Considerations&#x22; showing three columns with icons labeled &#x22;Metrics Server,&#x22; &#x22;Metrics Evaluation,&#x22; and &#x22;Scaling Behavior.&#x22; The slide also lists metric types like &#x22;Custom&#x22; and &#x22;External&#x22; and includes a KodeKloud copyright." />
</Frame>

Next steps and references

* Hands-on: install Metrics Server and a Prometheus Adapter, create sample applications that expose custom metrics, and apply HPAs to observe autoscaling behavior.
* Read more:
  * [Kubernetes HPA documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
  * [Metrics Server](https://github.com/kubernetes-sigs/metrics-server)
  * [Prometheus Adapter for Kubernetes Metrics APIs](https://github.com/kubernetes-sigs/prometheus-adapter)
  * Your cloud provider or APM documentation for their external metric adapters (e.g., Datadog, New Relic)

This completes the HPA architecture overview and the metric flow paths used for autoscaling. Use the examples above as templates when authoring HPA manifests and ensure your Metrics Server and adapters are properly configured for reliable automatic scaling.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/245fe895-fa01-4adf-b796-ce7f28666043/lesson/5d8bfc51-788e-4d32-be9a-95a1e1149a49)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/245fe895-fa01-4adf-b796-ce7f28666043/lesson/1ecc250a-8b72-4da9-aaca-5b75bd17417d)
