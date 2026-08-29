# OpenTelemetry Collector Deployment Modes in Kubernetes

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-in-Kubernetes/OpenTelemetry-Collector-Deployment-Modes-in-Kubernetes/page

Comparing OpenTelemetry Collector deployment modes in Kubernetes, including DaemonSet, Deployment gateway, Sidecar, and StatefulSet with patterns, trade-offs, and example configurations.

When deploying the OpenTelemetry Collector in Kubernetes, you can choose multiple deployment modes depending on coverage, scalability, persistence, and routing requirements. This guide explains the common patterns, trade-offs, and example configurations for each mode so you can pick the best architecture for your observability pipeline.

## DaemonSet

Running the collector as a DaemonSet launches one collector pod on every node, ensuring full node coverage. This is ideal for collecting node-local telemetry such as kubelet stats, host metrics, cAdvisor data, container and host logs, and workload telemetry that originates on the same node.

<Frame>
  <img alt="The image illustrates a Kubernetes cluster architecture with DaemonSet collectors on each node, gathering metrics and logs from app pods and forwarding them to a deployment collector, which then sends them to the backend." />
</Frame>

DaemonSet collectors typically:

* Collect node-local telemetry (container logs, pod/container metrics, kubelet stats, host metrics, disk and memory usage).
* Receive workload telemetry locally from applications on the same node (reducing network hops).
* Enrich telemetry with Kubernetes metadata (namespace, pod name, node name).
* Buffer and retry locally to improve resilience against transient network or next-hop failures.

<Frame>
  <img alt="The image is an informational slide about a DaemonSet Collector per node, detailing its functions such as running one collector pod per node, collecting node-local telemetry, receiving workload telemetry locally, enriching telemetry with Kubernetes metadata, and ensuring resilience." />
</Frame>

Operational patterns:

* DaemonSet -> Gateway: DaemonSet collectors commonly forward to a centralized Deployment (gateway) collector for centralized processing (sampling, aggregation, redaction).
* DaemonSet -> Backend: You can also configure DaemonSet collectors to export directly to external backends if per-node processing is sufficient.

Example: OpenTelemetryCollector CR (operator-managed) for DaemonSet mode:

```yaml theme={null}
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: otel-daemonset
spec:
  mode: daemonset
  config: |
    receivers:
      otlp: {}
      hostmetrics: {}
    exporters:
      logging: {}
    service:
      pipelines:
        metrics:
          receivers: [hostmetrics]
          exporters: [logging]
```

## Deployment (Gateway)

A Deployment-mode collector (often called a gateway) acts as a shared, stateless cluster endpoint. It aggregates telemetry from many workloads and is typically fronted by a Kubernetes Service so traffic can be load-balanced across replicas.

* Receives cluster-wide telemetry (via receivers or forwarded from DaemonSets/sidecars).
* Stateless and horizontally scalable—run multiple replicas and load-balance via a Service.
* Common use cases: batching, sampling, transformation, PII redaction, centralized buffering.

<Frame>
  <img alt="The image illustrates a stateless and multiple replica architecture with Kubernetes clusters containing app pods. It shows a gateway collector aggregating and exporting telemetry data to a backend through load-balanced Otelcol components." />
</Frame>

DaemonSet collectors frequently forward to a load-balanced gateway service for more advanced processing and to provide a single logical export endpoint.

<Frame>
  <img alt="The image is a diagram illustrating &#x22;DaemonSet Collectors – Forwarding to Gateway Deployment&#x22; in a Kubernetes cluster. It shows app pods on three nodes forwarding data to collectors, which then send data to a load-balanced service and ultimately to a backend." />
</Frame>

Configure a Deployment-mode collector by setting `mode: deployment` in the OpenTelemetryCollector resource. The configuration (receivers/processors/exporters) is shared across replicas and reachable through the Service DNS.

<Frame>
  <img alt="The image describes the features and functions of a Deployment/Gateway Collector, highlighting its centralized service role, cluster-wide telemetry collection, gateway endpoint function, and its ability to export telemetry to external observability platforms." />
</Frame>

## Sidecar

The sidecar pattern runs the collector in the same pod as the application container. This eliminates network hops between app and collector and isolates telemetry collection to the application instance level.

<Frame>
  <img alt="The image illustrates two modes of running agents in a Kubernetes cluster: per pod using a sidecar container and per node using a DaemonSet, both sending data to a backend." />
</Frame>

A typical sidecar pod spec includes both the app container and the otel collector container:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  containers:
    - name: my-app
      image: my-app:latest
      # app container config
    - name: otel-collector
      image: otel/opentelemetry-collector:latest
      args: ["--config", "/conf/collector-config.yaml"]
      # collector container config and volume mounts
```

When to use sidecars:

* You want per-application isolation and minimal hop telemetry collection.
* You need collector configuration tailored specifically for a single application.
* You may opt to export data directly from sidecars or forward to a central gateway.

## StatefulSet

Use StatefulSets when collectors require stable network identity and persistent storage (PVC). This is useful for Prometheus-style scraping (to keep target assignment consistent) and for tail-based sampling where traces must consistently arrive at the same collector.

<Frame>
  <img alt="The image illustrates a Kubernetes cluster setup using StatefulSets for stable collectors linked to application pods with persistent volume claims (PVC). It emphasizes the use of stable DNS through a headless service." />
</Frame>

StatefulSet collectors provide:

* Stable DNS and identity per pod.
* A dedicated PVC per pod for durable storage or queue persistence.
* Predictable mapping between collectors and targets for scraping and sticky routing.

Example OpenTelemetryCollector in StatefulSet mode with a volume claim template:

```yaml theme={null}
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: otel-stateful
spec:
  mode: statefulset
  volumeClaimTemplates:
    - metadata:
        name: otel-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
  config: |
    receivers:
      otlp: {}
    exporters:
      logging: {}
```

## TargetAllocator (operator feature)

The TargetAllocator decouples service discovery from scraping so both can scale independently. It generates Prometheus receiver configs and assigns scrape targets across collector pods. Combined with StatefulSets (stable identities), the TargetAllocator can assign a fixed subset of targets to each collector to prevent duplicate scraping and balance load.

<Frame>
  <img alt="The image illustrates a Kubernetes cluster setup for balanced Prometheus target allocation, featuring app pods linked to collector pods using persistent volume claims (PVC) and stable DNS via a headless service." />
</Frame>

For tail-based sampling, traces must be routed consistently to the same collector instance (sticky routing). StatefulSet collectors with stable identities are ideal because routing can remain consistent by trace ID.

<Frame>
  <img alt="The image is a diagram titled &#x22;StatefulSet Routing for Tail-Based Sampling,&#x22; illustrating the flow of spans from applications through an OpenTelemetry Collector to StatefulSet collectors, ensuring sticky routing by trace ID, and ending at a monitoring interface." />
</Frame>

## Comparison at-a-glance

| Mode                 | Best for                                                | Key characteristics                                                  |
| -------------------- | ------------------------------------------------------- | -------------------------------------------------------------------- |
| DaemonSet            | Node-local telemetry (kubelet, host metrics, node logs) | One collector per node, local buffering, enriched with node metadata |
| Deployment (Gateway) | Centralized processing, high availability               | Stateless, load-balanced via Service, scalable replicas              |
| Sidecar              | Per-application isolation, minimal hop                  | Collector in same pod as app, dedicated config per app               |
| StatefulSet          | Prometheus scraping, tail-based sampling                | Stable pod identity & DNS, PVCs for persistence, sticky routing      |

## Recap

* Deployment (gateway): central, stateless, load-balanced, cluster-wide aggregation and processing.
* DaemonSet: one collector per node—ideal for kubelet stats, host metrics, and node-local logs.
* Sidecar: collector in the same pod as the application—ideal for per-application isolation and minimal network hops.
* StatefulSet: collectors with stable identity and persistent storage—ideal for consistent scraping assignments and tail-based sampling.

<Frame>
  <img alt="The image illustrates different OpenTelemetry Collector deployment modes within a Kubernetes cluster, including Deployment, DaemonSet, Sidecar, and StatefulSet, each connecting to a backend." />
</Frame>

<Callout icon="lightbulb">
  Choose the deployment mode based on the telemetry type (node vs pod vs cluster-wide), the need for persistent storage or sticky routing, and your scalability/availability goals. Hybrid architectures (e.g., DaemonSet + gateway Deployment or sidecars with a central gateway) are common and provide a good balance between locality and centralized processing.
</Callout>

Links and References

* [OpenTelemetry Collector (official)](https://opentelemetry.io/docs/collector/)
* [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator)
* [Kubernetes DaemonSet Documentation](https://kubernetes.io/docs/[AWS_SECRET_ACCESS_KEY]/)
* [Kubernetes StatefulSet Documentation](https://kubernetes.[SECRET_REDACTED]/)
* [Prometheus Target Allocation Patterns](https://prometheus.[AWS_SECRET_ACCESS_KEY]configuration/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/09e46ae9-895f-4e3f-98dd-c7be94303a09/lesson/0caf0713-b2cc-4703-8b45-eb32430de424" />
</CardGroup>
