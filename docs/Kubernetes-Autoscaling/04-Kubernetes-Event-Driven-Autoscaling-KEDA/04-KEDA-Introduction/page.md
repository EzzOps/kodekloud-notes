# KEDA Introduction

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Kubernetes-Event-Driven-Autoscaling-KEDA/KEDA-Introduction/page

Explains KEDA, an event-driven Kubernetes autoscaler, its architecture, components, benefits, and comparisons to HPA VPA CPA, highlighting fast event-based scaling and scale-to-zero support.

Welcome to this lesson on Kubernetes Event-Driven Autoscaling (KEDA). This guide explains what KEDA is, how it works, and why it’s a strong choice for modern applications that must scale quickly and efficiently in response to external events.

First, a quick recap of the autoscaling landscape so you can see where KEDA fits.

We have several ways to autoscale in Kubernetes:

* [Horizontal Pod Autoscaling (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/): adjusts the number of pod replicas for a Deployment based on CPU, memory, custom metrics, or external metrics.
* Vertical Pod Autoscaling (VPA): adjusts CPU/memory requests and limits for existing pods.
* Cluster Proportional Autoscaling (CPA): adjusts system-component replicas (e.g., DNS, proxies) proportionally to cluster size (nodes or cores).

<Frame>
  <img alt="A presentation slide titled &#x22;A Recap&#x22; summarizing autoscaling options in Kubernetes Event-Driven Autoscaling (KEDA). It shows three cards listing Horizontal Pod Autoscaling (HPA), Vertical Pod Autoscaling (VPA), and Cluster Proportional Autoscaling (CPA)." />
</Frame>

Below is a focused review of each autoscaling option — strengths, limitations, and the scenarios where they shine — so you can see why KEDA is often the best fit for event-driven workloads.

## Horizontal Pod Autoscaler (HPA)

HPA automatically adjusts the number of pod replicas in a workload based on metrics such as CPU, memory, custom metrics, or external metrics exposed to Kubernetes.

<Frame>
  <img alt="A presentation slide titled &#x22;Horizontal Pod Autoscaling (HPA)&#x22; with a boxed definition explaining that HPA automatically adjusts the number of Kubernetes pod replicas based on CPU, memory, or custom metrics to ensure efficient resource utilization. The slide is © KodeKloud." />
</Frame>

Advantages:

* Native Kubernetes feature and simple to enable for CPU/memory scaling.
* Smooth replica adjustments with minimal disruption.
* Extendable to custom or external metrics via adapters.

Limitations:

* Built-in triggers are limited — event-driven triggers (queue depth, webhook events) need additional adapters or custom metrics pipelines.
* Uses periodic polling (controller sync intervals), so it reacts on a timer rather than directly to events.
* Requires predefined thresholds and at least one running pod; HPA cannot scale workloads to zero.

<Callout icon="warning">
  HPA cannot scale a workload down to zero replicas. If you need scale-to-zero behavior for cost savings during idle periods, you’ll need an event-driven scaler like KEDA.
</Callout>

## Vertical Pod Autoscaler (VPA)

VPA adjusts CPU and memory requests/limits for existing pods; it does not change replica counts.

<Frame>
  <img alt="A presentation slide titled &#x22;Vertical Pod Autoscaling (VPA)&#x22; with a rounded callout explaining that VPA automatically adjusts CPU and memory for containers to optimize resources within existing pods, unlike HPA which scales pod numbers." />
</Frame>

Advantages:

* Automatically right-sizes container CPU/memory requests and limits based on actual usage.
* Reduces the need for manual resource estimation and tuning.
* Ideal for workloads where changing pod resources is preferable to horizontal scaling.

Limitations:

* Resource adjustments often require pod restarts, which can cause brief downtime — risky for stateful or latency-sensitive services.
* VPA does not provide horizontal scaling; combining VPA and HPA needs careful coordination to avoid controller conflicts.
* May react slower to sudden spikes because of restart/re-provision cycles.

<Callout icon="warning">
  VPA adjustments typically restart pods. For latency-sensitive or stateful workloads, plan carefully or avoid automatic restarts without testing.
</Callout>

## Cluster Proportional Autoscaler (CPA)

CPA scales system components (e.g., CoreDNS, kube-proxy) proportionally to cluster size (nodes or cores), not based on application workload.

<Frame>
  <img alt="A presentation slide titled &#x22;Cluster Proportional Autoscaling (CPA)&#x22;. A centered note explains that CPA scales system components (e.g., DNS or network proxies) proportionally to cluster size, unlike HPA or VPA which scale based on pod resource usage." />
</Frame>

Notes:

* Keeps cluster-level infrastructure components aligned with cluster growth or shrink.
* Useful alongside DaemonSets when you need different proportional ratios for system pods.
* Not driven by application workload, so it doesn’t help scale application replicas in response to user traffic.

Limitations:

* Infrastructure-focused and does not react to per-application demand.
* Less precise for workload tuning compared with HPA or KEDA.

## Quick comparison

| Autoscaler | Primary Use Case                                            |                           Reactivity | Scale-to-zero | Notes                                                             |
| ---------- | ----------------------------------------------------------- | -----------------------------------: | :-----------: | ----------------------------------------------------------------- |
| HPA        | Adjust replicas based on CPU/memory/custom metrics          |              High (polling interval) |       No      | Native; needs adapters for event-based metrics                    |
| VPA        | Adjust pod CPU/memory requests/limits                       |    Medium (changes require restarts) |      N/A      | Good for right-sizing, not horizontal scaling                     |
| CPA        | Scale system components with cluster size                   |                                  Low |       No      | Infrastructure-focused                                            |
| KEDA       | Event-driven scaling (queues, HTTP counters, cloud metrics) | Very high (reacts to events/metrics) |      Yes      | Integrates with HPA via metrics adapter; supports scaling to zero |

## Why KEDA?

Imagine an HTTP public API that sees sudden bursts of traffic followed by long idle periods. Requirements might include:

* Rapid scale-up based on request volume or a request counter metric.
* Scale-down-to-zero when idle to save cost.
* Minimal complexity without custom adapters or heavy configuration.

<Frame>
  <img alt="A slide titled &#x22;Scaling HTTP Workload&#x22; showing a central API gear icon with spokes. Three callouts note sudden bursts of traffic, scaling down to zero during idle periods to save costs, and scaling up based on incoming HTTP requests." />
</Frame>

HPA may not be ideal here (cannot scale to zero and may lag on CPU-based signals). VPA changes pod sizing and can cause restarts. CPA does not observe HTTP load. KEDA fills this gap with event-driven autoscaling that integrates with Kubernetes and supports many external scalers:

* Scales workloads based on event sources or external metrics: message queues, HTTP counters, [Prometheus](https://prometheus.io/) metrics, cloud provider metrics, and more.
* Ships many built-in scalers (Kafka, Azure Service Bus, AWS SQS, Prometheus, HTTP, and others).
* Reacts quickly to metric changes and supports scaling down to zero when demand is zero.
* Uses Kubernetes CRDs like ScaledObject and ScaledJob to define scaling behavior with minimal extra infrastructure.

<Callout icon="lightbulb">
  KEDA enables event-driven autoscaling, including scaling to zero, for any metric or event source that a supported scaler can access or that you can expose.
</Callout>

## KEDA architecture and components

KEDA is composed of several cooperating components that enable event-driven autoscaling in Kubernetes:

* KEDA Operator (control plane): Reconciles CRDs (ScaledObjects and ScaledJobs), watches event sources, and requests scaling actions from the Kubernetes API.
* Metrics adapter / Metrics server: Exposes external metrics to Kubernetes’ External Metrics API so the HPA or other controllers can consume them.
* Admission Webhook: Validates and optionally mutates KEDA resources at admission time to ensure correct configurations.
* TriggerAuthentication: A CRD to securely store credentials for external systems so secrets are not embedded in ScaledObjects.
* Scaler: Component-specific implementations that fetch metrics or observe events from external sources and determine scale-up/scale-down decisions.
* ScaledObject / ScaledJob: CRDs that link a Deployment or Job to a scaler and define scaling behavior (thresholds, min/max replicas, cooldowns).

<Frame>
  <img alt="An infographic titled &#x22;KEDA Components&#x22; showing the KEDA logo in the center surrounded by six numbered bubbles. Each bubble names and briefly describes components like Keda Operator, Metrics Server, Admission Webhooks, Trigger Authentication, Scaler, and ScaledObject." />
</Frame>

### Component details

Operator

* Acts as KEDA’s control plane: watches ScaledObjects and ScaledJobs, reconciles their desired state, and requests scaling changes via the Kubernetes API.

Metrics adapter

* Aggregates external metrics and exposes them through the External Metrics API. This lets Kubernetes-native controllers (like HPA when configured) consume event-based metrics seamlessly. See Kubernetes HPA metrics support: [https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-metrics-apis](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-metrics-apis)

Admission Webhook

* Validates and mutates KEDA-related resources during admission to the API server. This prevents invalid or insecure configurations from being persisted.

TriggerAuthentication

* Stores credentials and secrets that scalers need to access external systems (for example, cloud queues or APIs) so you avoid embedding secrets directly in ScaledObject definitions.

<Frame>
  <img alt="A presentation slide titled &#x22;KEDA – Trigger Authentication&#x22; featuring a green circular shield icon with a user and checkmark and a panel listing key responsibilities: &#x22;External authentication&#x22; and &#x22;Secure sensitive information.&#x22; The slide shows a small © Copyright KodeKloud note at the bottom." />
</Frame>

Scaler

* Implements the platform-specific logic to fetch metrics or observe events (e.g., from Prometheus, cloud provider APIs, or messaging systems). A scaler interprets thresholds and signals when the operator should scale a target workload, and it supplies metrics to the metrics adapter.

<Frame>
  <img alt="A presentation slide titled &#x22;KEDA – Scaler&#x22; showing a green circular icon labeled &#x22;Scaler&#x22; beside a &#x22;Key Responsibilities&#x22; box that lists &#x22;Fetch external metrics.&#x22; The slide has a clean white background with a © Copyright KodeKloud note at the bottom left." />
</Frame>

ScaledObject (and ScaledJob)

* The ScaledObject CRD attaches to a Deployment (or other supported workload) and defines:
  * Which scaler to use (the event source or metric source).
  * Metric queries, thresholds, and behavior parameters.
  * Scaling policy: min/max replicas, cooldown periods, polling intervals.
* ScaledJob is the equivalent for Jobs: it triggers Kubernetes Jobs based on event messages or metrics.

## Putting it together

KEDA’s pieces work together to provide flexible, efficient event-driven scaling:

* ScaledObjects define the scaler, thresholds, and min/max bounds.
* TriggerAuthentication keeps secrets out of ScaledObjects.
* Scalers fetch metrics and interpret when to scale.
* The Operator reconciles desired state and issues scaling requests.
* The metrics adapter surfaces metrics to Kubernetes APIs.
* The admission webhook validates configurations on create/update.

This architecture makes KEDA an excellent choice when you need:

* Fast reaction to event-driven workloads (message queues, HTTP counters, webhooks).
* Fine-grained control over scaling thresholds and behavior.
* The ability to scale to zero to save cost during idle periods.
* Native Kubernetes integration while supporting many external sources and cloud providers.

## Additional resources

* KEDA project: [https://keda.sh/](https://keda.sh/)
* Kubernetes HPA documentation: [https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Cluster Autoscaler (useful when autoscaling nodes): [https://github.[SECRET_REDACTED]-autoscaler](https://github.[SECRET_REDACTED]-autoscaler)

Thanks for reading this lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/c218f836-7d7e-425b-a8b7-0148914eb040/lesson/1b14abfc-5f0a-41ce-8bb4-4b9908578d76" />
</CardGroup>
