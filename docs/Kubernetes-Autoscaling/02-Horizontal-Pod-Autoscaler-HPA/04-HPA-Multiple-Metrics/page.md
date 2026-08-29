# HPA Multiple Metrics

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Horizontal-Pod-Autoscaler-HPA/HPA-Multiple-Metrics/page

How to configure HPA with multiple metrics to scale Kubernetes services using CPU and custom application metrics, including architecture, examples, and best practices

Welcome. In this lesson we’ll cover how to use multiple metrics with the Horizontal Pod Autoscaler (HPA) to build more accurate, reliable autoscaling policies.

Why this matters: a complex microservices application (for example, an e‑commerce platform) can show different load characteristics across services. Scaling only by CPU or memory may not reflect actual application load — you may need to combine resource metrics (CPU) with application-level metrics (request rate, active HTTP requests, queue length) to scale the right component at the right time.

<Frame>
  <img alt="A presentation slide titled &#x22;When Do We Need Multiple Metrics?&#x22; showing an &#x22;E‑Commerce Application&#x22; icon and three colored circles representing stages: Browsing products, Adding to cart, and Processing transactions. The slide includes simple line icons for each stage and a small © Copyright KodeKloud note." />
</Frame>

Consider an e‑commerce stack split into microservices: product-catalog, cart service, and transaction processor. Each service may require different scaling signals—product-catalog might need CPU plus incoming request rate, while transaction processing may need concurrency or queue length. Multiple metrics let HPA satisfy the strictest requirement across the configured metrics.

<Frame>
  <img alt="A slide titled &#x22;When Do We Need Multiple Metrics?&#x22; showing a laptop with a rising chart and the caption &#x22;To efficiently scale the application during peak traffic.&#x22; To the right is an icon of a person linked to multiple documents with the caption &#x22;Scaling requires considering multiple metrics at once.&#x22;" />
</Frame>

Architecture and required components

* Cluster resource metrics: Ensure a working cluster metrics pipeline (metrics-server) to provide resource metrics like CPU and memory.
* Application instrumentation: Expose custom application metrics (e.g., active HTTP requests, requests per second, queue length) via Prometheus or another collector.
* Metrics adapter: Deploy an adapter (for example, Prometheus Adapter) to make custom metrics available through the Kubernetes metrics API so HPA can consume them.

<Frame>
  <img alt="A slide titled &#x22;Multiple Metrics Implementation&#x22; showing step 02 &#x22;Deploy Metrics Adapter&#x22; with a diagram of a metrics adapter (plug icon) connecting a service/metric source on the left to a K8s cluster (Kubernetes logo) on the right." />
</Frame>

How HPA evaluates multiple metrics

* HPA reads all configured metrics (resource and external/custom).
* For each metric, HPA computes the desired replica count required to meet that metric’s target.
* The HPA then scales to the highest of those desired replica counts so that all targets are satisfied.

Example: scale a Deployment named `backend-service` by CPU utilization and a custom per-pod metric `active_http_requests`:

```yaml theme={null}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: active_http_requests
      target:
        type: AverageValue
        averageValue: "100"
```

Notes about the configuration:

* `averageUtilization: 70` targets \~70% CPU utilization across the pods.
* The `Pods` metric type with `AverageValue` targets an average of `100` `active_http_requests` per pod. The adapter must expose `active_http_requests` as a pods-scoped metric.
* HPA evaluates both metrics and scales to the highest computed replica count.

Metric types at a glance

| Metric Type | Scope                    | Best for                                                                   | Example                |
| ----------- | ------------------------ | -------------------------------------------------------------------------- | ---------------------- |
| Resource    | Pod/Container            | CPU & memory-driven scaling                                                | `cpu` utilization      |
| Pods        | Per-pod custom           | Metrics that are naturally measured per pod (concurrency, active requests) | `active_http_requests` |
| External    | Cluster/external service | Metrics external to pods (queue length in external system, cloud metrics)  | `sqs_queue_length`     |

When NOT to use multiple metrics

* Metrics are not correlated to actual service load (e.g., CPU stuck at high value with no request changes).
* The metrics adapter or metric source is unreliable or hard to maintain.
* Metrics have incompatible sampling intervals or units (one metric sampled every second vs another every 10 minutes).
* The added complexity of reconciling multiple metrics outweighs autoscaling benefits.

<Frame>
  <img alt="A presentation slide titled &#x22;Using Multiple Metrics for Scaling – When to Avoid&#x22; showing three colored columns—Non-Correlated Metrics, Complex Adapters Metrics, and Different Sampling Rates—with icons and bullet points describing when not to use multiple metrics. The slide also includes a small © Copyright KodeKloud notice." />
</Frame>

<Callout icon="lightbulb">
  Ensure your cluster has a working metrics pipeline (`metrics-server`) and a compatible adapter (for example, the Prometheus Adapter) before relying on custom metrics for HPA. Verify sampling intervals, metric names, and scope (pods vs. external) to avoid surprising behavior.
</Callout>

Best practices

* Start simple: use a single well-understood metric and validate behavior.
* Use per-pod metrics when the metric is tightly coupled to workload per replica (like concurrent requests).
* Ensure consistent scraping intervals and retention in your monitoring system.
* Test scaling behavior under realistic load patterns and validate that the highest computed replica count is the correct safe option.

Summary
Multiple metrics let you express richer autoscaling policies (e.g., combine CPU and request rate) and help you scale the right microservice at the right time. However, they require reliable instrumentation, a functioning metrics adapter, and careful attention to metric correlation and sampling. Balance complexity against the value added and choose metrics that best reflect real workload characteristics.

Links and references

* Kubernetes Autoscaling (HPA): [https://learn.kodekloud.com/user/courses/kubernetes-autoscaling](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling)
* metrics-server: [https://github.com/kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server)
* Prometheus Adapter: [https://github.com/prometheus-community/prometheus-adapter](https://github.com/prometheus-community/prometheus-adapter)
* Prometheus monitoring course: [https://learn.kodekloud.com/user/courses/youtube-labs-monitoring-kubernetes-with-prometheus](https://learn.kodekloud.com/user/courses/youtube-labs-monitoring-kubernetes-with-prometheus)

We will get hands-on with this setup so you can see it in action.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/245fe895-fa01-4adf-b796-ce7f28666043/lesson/37304e76-3ec9-447e-ba1c-ace3bf95d336" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/245fe895-fa01-4adf-b796-ce7f28666043/lesson/7582ead6-af77-4e82-bf0d-7c12b99adf4a" />
</CardGroup>
