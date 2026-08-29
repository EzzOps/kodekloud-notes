# External Metrics Mechanisms

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Horizontal-Pod-Autoscaler-HPA/External-Metrics-Mechanisms/page

Explains using external metrics from outside Kubernetes with metrics adapters and monitoring systems to enable HPA autoscaling based on external signals like queue backlogs or external request rates

Welcome. This guide explains how Kubernetes external metrics work with the Horizontal Pod Autoscaler (HPA), why they matter, and how to put them into production.

External metrics differ from native resource metrics (CPU/memory) and application-level custom metrics. They originate outside the cluster (or outside the pod resource model) and are made available to the HPA so scaling decisions can be based on external systems and services.

<Frame>
  <img alt="A slide titled &#x22;HPA External Metrics&#x22; showing an HPA box containing a &#x22;K8s External Metrics&#x22; block. An arrow points from the HPA box to a laptop icon labeled &#x22;External Metrics.&#x22;" />
</Frame>

Why use external metrics?

* Scale based on external systems such as cloud-managed queues, third-party APIs, or external load balancers.
* Make proactive scaling decisions from signals that don’t exist inside pod metrics (for example, queue backlog or external request rate).
* Integrate infrastructure- or business-level signals (billing events, backlog thresholds, SaaS metrics) into Kubernetes autoscaling.

Common examples:

* A cloud-based message queue backlog drives additional consumers.
* An external load balancer’s observed request rate determines replica count.

<Frame>
  <img alt="A presentation slide titled &#x22;HPA External Metrics&#x22; that says external metrics enable scaling based on external factors. It shows two examples: length of a message queue in a cloud service and rate of incoming requests from an external load balancer." />
</Frame>

Architecture and data flow

External metrics rely on a small set of components working together:

* External metric source: the cloud provider, message queue, or third-party service exposing the metric.
* Collection/monitoring system: gathers metrics from the external source (examples: Prometheus, cloud monitoring like Cloud Monitoring / CloudWatch).
* Metrics adapter: translates collected metrics into the Kubernetes External Metrics API so the HPA can query them.
* HPA: requests metrics via the Kubernetes API and uses the returned values to scale workloads.

Think: the monitoring system is the scout that fetches values, and the adapter is the translator exposing them to Kubernetes.

Components summary

| Component              | Purpose                                                                    | Example                                                             |
| ---------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| External metric source | Origin of the metric (outside the cluster)                                 | Cloud queue backlog, external LB request rate                       |
| Collector / monitoring | Pulls or receives external metrics                                         | [Prometheus](https://prometheus.io/), Cloud Monitoring / CloudWatch |
| Metrics adapter        | Implements Kubernetes External Metrics API and bridges collector → K8s API | `prometheus-adapter`, cloud provider adapters                       |
| HPA                    | Queries the External Metrics API and makes scaling decisions               | `HorizontalPodAutoscaler` (autoscaling/v2)                          |

> **lightbulb** The default Kubernetes Metrics Server only serves resource metrics (CPU/memory) and does not expose external metrics. Deploy a metrics adapter that implements the External Metrics API (for example, the [Prometheus Adapter](https://github.com/kubernetes-sigs/prometheus-adapter) or a cloud-specific adapter) to allow the HPA to consume external signals.

Important considerations

* You need a reliable collector/monitoring layer that can fetch external values (via scraping, API polling, or event ingestion).
* An in-cluster metrics adapter must be configured to expose metrics through the Kubernetes External Metrics API.
* The adapter must support querying metrics by name and labels so the HPA can target the correct time series.
* Validate auth, network connectivity, and metric naming between source → collector → adapter → HPA.

<Frame>
  <img alt="A presentation slide titled &#x22;HPA External Metrics – Considerations&#x22; showing three colored icons and labels: &#x22;Metrics server limitation&#x22;, &#x22;Adapter configuration&#x22;, and &#x22;Monitoring systems.&#x22; The slide appears to outline key considerations for external metrics in horizontal pod autoscaling." />
</Frame>

Practical configuration tips

* Choose a monitoring backend that reliably collects your external signal (queue depth, request rate, third-party metric).
* Select an adapter compatible with your metric store (for Prometheus, use the Prometheus Adapter; for cloud metrics, use the cloud provider’s adapter).
* In the HPA spec, reference the external metric by name and supply label selectors if required to match the right series.
* Test the full pipeline (external source → collector → adapter → Kubernetes API → HPA) and validate both metric accuracy and timeliness.

Example: HPA referencing an external metric (autoscaling/v2)

```yaml theme={null}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: example-external-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: External
      external:
        metric:
          name: queue_messages_ready
          selector:
            matchLabels:
              queue: orders
        target:
          type: Value
          value: "100"
```

Testing and observability checklist

* Confirm the collector is scraping/pulling the external metric and exposing it in the monitoring backend.
* Verify the adapter reports the metric through the Kubernetes External Metrics API:
  * `kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1"` (adapter dependent)
* Check HPA events and status:
  * `kubectl describe hpa example-external-hpa`
* Monitor adapter and collector logs/alerts to detect failures or missing series.

> **warning** If the adapter or collector is misconfigured or unavailable, the HPA will not receive external metrics and scaling may not occur. Continuously monitor adapter health and metric endpoints to avoid gaps in autoscaling.

Further reading and references

* Kubernetes Horizontal Pod Autoscaler docs: [External Metrics](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#external-metrics)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Prometheus Adapter (example): [https://github.com/kubernetes-sigs/prometheus-adapter](https://github.com/kubernetes-sigs/prometheus-adapter)

And that's it — use external metrics to incorporate business- and infrastructure-level signals into HPA-driven scaling. Explore adapters that match your monitoring backend and external sources to make autoscaling both reliable and proactive.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/245fe895-fa01-4adf-b796-ce7f28666043/lesson/f0e21343-4242-4359-a321-c77a082ad324)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/245fe895-fa01-4adf-b796-ce7f28666043/lesson/bbb01344-6729-4736-a876-cbbc454998cc)
