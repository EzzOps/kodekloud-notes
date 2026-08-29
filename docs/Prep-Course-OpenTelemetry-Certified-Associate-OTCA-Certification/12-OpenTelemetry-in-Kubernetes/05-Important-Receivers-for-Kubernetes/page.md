# edit values.yaml as needed (see TLS/webhook notes below)
helm install my-opentelemetry-operator open-telemetry/opentelemetry-operator -f values.yaml
```

A few top-level values (excerpt):

```yaml theme={null}
# values.yaml (excerpt)
namespaceOverride: ""
replicaCount: 1
revisionHistoryLimit: 10
nameOverride: ""
```

## TLS / Admission webhook certificate options

The operator installs admission webhooks that require a TLS certificate trusted by the API server. You have three main options:

| Option                                         | Use case                                          | Notes / link                                                                                                                                                         |
| ---------------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cert-manager                                   | Production or cluster-wide certificate management | Deploy `cert-manager` and set `admissionWebhooks.certManager.enabled: true`. See `cert-manager` docs: [https://cert-manager.io/docs/](https://cert-manager.io/docs/) |
| Operator auto-generate (recommended for demos) | Quick demos or local clusters                     | Let the operator generate a self-signed cert by enabling `admissionWebhooks.autoGenerateCert.enabled`.                                                               |
| Provide your own cert                          | Advanced / policy-controlled environments         | Supply the webhook certificate from your own PKI and configure the operator accordingly.                                                                             |

<Callout icon="lightbulb">
  If you don't want to install `cert-manager`, set `admissionWebhooks.certManager.enabled` to `false` and `admissionWebhooks.autoGenerateCert.enabled` to `true` so the operator auto-creates a self-signed webhook certificate suitable for demos and local testing.
</Callout>

Use this `values.yaml` snippet to enable the operator's auto-generated certificate:

```yaml theme={null}
admissionWebhooks:
  certManager:
    enabled: false
  autoGenerateCert:
    enabled: true
    recreate: true
    certPeriodDays: 365
```

## Configure operator and collector images

Set the manager and default collector image repositories and tags in `values.yaml` as needed:

```yaml theme={null}
manager:
  image:
    repository: ghcr.io/open-telemetry/opentelemetry-operator/opentelemetry-operator
    tag: ""
    imagePullPolicy: IfNotPresent
  collectorImage:
    repository: ghcr.io/open-telemetry/opentelemetry-collector-releases/opentelemetry-collector-k8s
    tag: 0.137.0
```

Install (or upgrade) the operator with your edited values:

```bash theme={null}
helm install my-opentelemetry-operator open-telemetry/opentelemetry-operator -f values.yaml
```

Example Helm output:

```text theme={null}
NAME: my-opentelemetry-operator
LAST DEPLOYED: Tue Oct 21 22:55:09 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
[WARNING] No resource limits or requests were set. Consider setting resource requests and limits via the `resources` field.

opentelemetry-operator has been installed. Check its status by running:
    kubectl --namespace default get pods -l "app.kubernetes.io/instance=my-opentelemetry-operator"
```

## Verify the operator

Check deployments:

```bash theme={null}
kubectl get deployment
```

Example output:

```bash theme={null}
NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
jaeger                          1/1     1            1           45m
my-opentelemetry-operator       1/1     1            1           15s
```

Note: this deployment is the operator controller — not a collector. The operator will create and reconcile `OpenTelemetryCollector` custom resources for you.

The OpenTelemetry Operator chart documentation describes the webhook/TLS details in depth: [https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-operator)

<Frame>
  <img alt="The image shows a webpage from OpenTelemetry documentation discussing the configuration of the Operator Helm chart with a focus on TLS certificates and cert-manager usage in Kubernetes." />
</Frame>

## Creating a Collector via the Operator

Create a collector by applying an `OpenTelemetryCollector` CR. The CRD accepts the standard collector configuration (receivers, processors, exporters, service pipelines) and operator-specific fields such as `mode` (Deployment or DaemonSet) and upgrade settings.

Example `collector.yaml` — a deployment-mode collector named `my-collector` that accepts OTLP, logs debug output, and forwards traces to an in-cluster Jaeger service:

```yaml theme={null}
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata:
  name: my-collector
spec:
  mode: deployment
  config:
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

    processors:
      memory_limiter:
        check_interval: 1s
        limit_percentage: 75
        spike_limit_percentage: 15
      batch:
        send_batch_size: 10000
        timeout: 10s

    exporters:
      # NOTE: Prior to v0.86.0 use `logging` instead of `debug`.
      debug:
        verbosity: detailed

      otlp/jaeger:
        endpoint: jaeger-internal:4317
        tls:
          insecure: true

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [debug, otlp/jaeger]
```

Apply the collector CR:

```bash theme={null}
kubectl apply -f collector.yaml
```

Expected response:

```bash theme={null}
opentelemetrycollector.opentelemetry.io/my-collector created
```

Check the collector CR, deployments and pods:

```bash theme={null}
kubectl get opentelemetrycollector
kubectl get deployment
kubectl get pod
```

Example outputs:

```bash theme={null}
# CR status (example)
NAME           MODE        VERSION   READY   AGE    IMAGE
my-collector   deployment  0.137.0   1/1     7s     ghcr.io/open-telemetry/opentelemetry-collector-releases/opentelemetry-collector-k8s:0.137.0  managed

# Deployments
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
jaeger                         1/1     1            1           53m
my-collector-collector         1/1     1            1           14s
my-opentelemetry-operator      1/1     1            1           7m54s

# Pods
NAME                                              READY   STATUS    RESTARTS   AGE
jaeger-75f7bdcc4-sr2v6                            1/1     Running   0          46m
my-collector-collector-dd46d98c6-kpg4n            1/1     Running   0          2m
my-opentelemetry-operator-77fcd686bd-54258        2/2     Running   0          9m
```

## Services created by the operator

When the operator deploys a collector in `deployment` mode it creates ClusterIP Services so other pods can reach the collector by DNS (no need to use node IPs).

Example `kubectl get svc` output (collector services highlighted):

```bash theme={null}
kubectl get svc
```

Example output converted to a table for clarity:

| NAME                              | TYPE      | CLUSTER-IP   | PORT(S)                               | AGE   |
| --------------------------------- | --------- | ------------ | ------------------------------------- | ----- |
| jaeger-external                   | NodePort  | 10.96.224.52 | 16686:30007/TCP                       | 54m   |
| jaeger-internal                   | ClusterIP | 10.96.11.34  | 4317/TCP,4318/TCP,14250/TCP,14268/TCP | 54m   |
| kubernetes                        | ClusterIP | 10.96.0.1    | 443/TCP                               | 54m   |
| my-collector-collector            | ClusterIP | 10.96.73.32  | 4317/TCP,4318/TCP                     | 47s   |
| my-collector-collector-headless   | ClusterIP | 10.96.2.111  | 8888/TCP                              | 47s   |
| my-collector-collector-monitoring | ClusterIP | 10.96.92.124 | 8443/TCP,8080/TCP                     | 8m27s |
| my-opentelemetry-operator         | ClusterIP | 10.96.77.7   | 443/TCP                               | 8m27s |

## Deploy an application that sends traces

Point your app at the collector service DNS (e.g. `my-collector-collector`) instead of a node IP. Example Deployment snippet:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: sloppy-networks/traces-py
          env:
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://my-collector-collector:4318"
```

Apply the app and verify pods:

```bash theme={null}
kubectl apply -f app-deployment.yaml
kubectl get pod
```

Example pod listing showing the app starting:

```bash theme={null}
NAME                                               READY   STATUS            RESTARTS   AGE
jaeger-75f7bdcc4-sr2v6                             1/1     Running           0          55m
my-collector-collector-dd46d98c6-kpg4n             1/1     Running           0          119s
my-opentelemetry-operator-77fcd686bd-54258         2/2     Running           0          9m39s
myapp-5d474bf94c-nz8c2                             0/1     ContainerCreating 0          3s
```

Check application logs to confirm spans are being sent and received by the collector. Example `kubectl logs` output from the sample app:

```text theme={null}
Span #1
Trace ID     : 7a13dcaa7590b979b4e88551c960d02d
Parent ID    : 27ff3b347e06fb2
ID           : 2f9d5516fdc33ee
Name         : process flight
Kind         : Internal
Start time   : 2025-10-22 05:05:04.274897701 +0000 UTC
End time     : 2025-10-22 05:05:04.316242576 +0000 UTC
Status code  : Unset
Status message:
Attributes:
  -> source: Str(jfk)
  -> dest: Str(lax)
  -> flight_number: Str(4427)
  -> airline: Str(delta)
```

## Viewing traces in Jaeger

Open the Jaeger UI (NodePort, port-forward, or external URL) and search for your service. The UI should display traces forwarded from your application via the operator-managed collector.

<Frame>
  <img alt="The image shows the Jaeger UI displaying tracing data, with a list of trace results for a &#x22;flight-service&#x22; including their durations and timestamps. It includes a filter section for refining search criteria based on service, operation, and duration." />
</Frame>

## Conclusion

Using the OpenTelemetry Operator makes collectors Kubernetes-first: define an `OpenTelemetryCollector` CR with normal collector configuration, choose deployment mode (DaemonSet or Deployment), and let the operator manage lifecycle, upgrades, and reconciliations. This is especially helpful for cluster-wide auto-instrumentation and centralized collector management.

## Links and references

* OpenTelemetry Operator Helm Chart: [https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-operator)
* cert-manager documentation: [https://cert-manager.io/docs/](https://cert-manager.io/docs/)
* OpenTelemetry Collector releases: [https://github.com/open-telemetry/opentelemetry-collector-releases](https://github.com/open-telemetry/opentelemetry-collector-releases)
* Jaeger project: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/09e46ae9-895f-4e3f-98dd-c7be94303a09/lesson/d4a4c311-382c-44d4-b259-145d79432d16" />
</CardGroup>


# Important Receivers for Kubernetes

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-in-Kubernetes/Important-Receivers-for-Kubernetes/page

Guide to key OpenTelemetry Collector receivers and processors for Kubernetes, explaining their purposes, typical deployment patterns, configuration snippets, and metadata enrichment and scraping considerations.

This guide recaps the most important OpenTelemetry Collector receivers and related processors commonly used in Kubernetes, where they typically run, and short configuration examples. The goal is to visualize which components collect which telemetry, and how they enrich or forward it to the Collector.

## Kubernetes attributes processor

The `k8sattributes` processor enriches incoming telemetry with Kubernetes metadata such as pod name, namespace, labels, annotations, and node information. This processor is commonly used when the Collector runs as a DaemonSet, sidecar, or centralized Collector with appropriate RBAC access so it can attach Kubernetes context to traces, metrics, and logs.

Example configuration:

```yaml theme={null}
processors:
  k8sattributes: {}
```

<Callout icon="lightbulb">
  Kubernetes metadata enrichment requires the Collector to have proper [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) permissions (to read pods, nodes, and endpoints). Ensure your Collector's [ServiceAccount](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) has the required [Role/ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole).
</Callout>

## kubeletstats receiver

The `kubeletstats` receiver scrapes the kubelet summary endpoint on each node to collect node-, pod-, and container-level resource metrics (CPU, memory, filesystem, network). Because it needs local kubelet access, it is typically deployed as a DaemonSet so each Collector pod can reach the local kubelet.

Example configuration:

```yaml theme={null}
receivers:
  kubeletstats: {}
```

Notes:

* The kubelet summary endpoint may require authentication or TLS; configure the receiver to meet your kubelet security configuration.
* Use `kubeletstats` alongside `hostmetrics` and Prometheus scrapes for a complete resource and workload view.

## filelog receiver

The `filelog` receiver tails container log files (commonly `/var/log/containers/*.log`) and forwards container stdout/stderr logs to the Collector for processing and export.

Example configuration:

```yaml theme={null}
receivers:
  filelog:
    include: ["/var/log/containers/*.log"]
```

## Kubernetes cluster and objects receivers

* `kubernetescluster` (cluster receiver) gathers cluster-level metrics and high-level entity events (e.g., cluster resource usage, aggregated signals).
* `k8sobjects` (objects receiver) retrieves Kubernetes object state and events such as Pod, Deployment, and StatefulSet statuses.

Use these receivers to gain visibility into cluster health, topology, and object lifecycle events. Receiver names can vary between Collector distributions—check your distribution’s contrib receivers list for exact names.

<Frame>
  <img alt="The image shows a diagram of a Kubernetes cluster sending cluster metrics and events to a collector, with k8sobjects indicated in the flow." />
</Frame>

## Prometheus receiver

The Prometheus receiver scrapes metrics exposed in the Prometheus exposition format. Use it to scrape instrumented applications and exporters that expose `/metrics`.

Example minimal snippet:

```yaml theme={null}
receivers:
  prometheus: {}
```

<Callout icon="note">
  The Prometheus receiver requires a full `config.scrape_configs` section (service discovery or explicit `scrape_configs`). The example above is minimal—define jobs, targets, and relabeling to avoid misconfigured scrapes.
</Callout>

<Callout icon="warning">
  If multiple Collectors can scrape the same Prometheus targets you will receive duplicate metrics. Coordinate scrapes (for example, partition targets or use a target allocator) to avoid duplication and metric inflation.
</Callout>

## hostmetrics receiver

The `hostmetrics` receiver collects OS-level metrics from nodes, such as CPU, memory, disk, and network usage. When used together with `kubeletstats` and Prometheus scrapes, it helps provide a full observability picture for both nodes and workloads.

<Frame>
  <img alt="The image illustrates data flow diagrams for Prometheus and Hostmetrics receivers, showing how a collector gathers data from service endpoints and nodes." />
</Frame>

## OTLP receiver (application telemetry)

The OTLP receiver accepts traces, metrics, and logs from instrumented applications over gRPC/HTTP in the OTLP format. Use this when your workloads export telemetry directly to the Collector.

Example configuration:

```yaml theme={null}
receivers:
  otlp:
    protocols:
      grpc: {}
      http: {}
```

## Quick reference table

| Receiver / Processor           | Purpose                                          | Typical Deployment                                                   | Example                                               |
| ------------------------------ | ------------------------------------------------ | -------------------------------------------------------------------- | ----------------------------------------------------- |
| k8sattributes (processor)      | Enrich telemetry with pod/node metadata          | DaemonSet, sidecar, centralized Collector with RBAC                  | `k8sattributes: {}`                                   |
| kubeletstats (receiver)        | Node/pod/container resource metrics from kubelet | DaemonSet (local kubelet access)                                     | `kubeletstats: {}`                                    |
| filelog (receiver)             | Tail container stdout/stderr logs                | DaemonSet or sidecar with hostPath mounts                            | `filelog: { include: ["/var/log/containers/*.log"] }` |
| kubernetescluster / k8sobjects | Cluster-level metrics, object state & events     | Centralized Collector or specialized controllers                     | See distribution contrib list                         |
| prometheus (receiver)          | Scrape Prometheus-format endpoints / exporters   | Sidecar, DaemonSet, or centralized Collector (depending on topology) | `prometheus: {}` (add `config.scrape_configs`)        |
| hostmetrics (receiver)         | OS-level node metrics                            | DaemonSet or node-local Collector                                    | `hostmetrics: {}`                                     |
| otlp (receiver)                | Receive OTLP telemetry from instrumented apps    | Centralized Collector or Gateway                                     | `otlp: { protocols: { grpc: {}, http: {} } }`         |

## Summary and deployment choices

* Use the `k8sattributes` processor to attach Kubernetes context to telemetry; ensure RBAC is configured.
* Deploy `kubeletstats` and `hostmetrics` as node-local (DaemonSet) collectors when you need local resource visibility and access to the kubelet.
* Use `filelog` to collect container logs from node file paths or run sidecars that forward logs into the Collector.
* Enable `kubernetescluster` and `k8sobjects` when you need cluster-level visibility and Kubernetes object events; verify exact receiver names for your Collector distribution.
* Use the `prometheus` receiver to scrape Prometheus-format endpoints—always define proper `scrape_configs` and coordinate scrapes to avoid duplicates.
* Use `otlp` to accept telemetry from instrumented workloads directly.

Review and adapt these choices to match your Collector deployment model (DaemonSet, sidecar, or centralized) and to ensure RBAC, network access, and scrape topology are configured correctly.

## Links and references

* [OpenTelemetry Collector documentation](https://opentelemetry.io/docs/collector/)
* [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* [Kubernetes ServiceAccount](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)
* [Kubelet resource usage monitoring](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/)
* [Prometheus exposition formats](https://prometheus.io/docs/instrumenting/exposition_formats/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/09e46ae9-895f-4e3f-98dd-c7be94303a09/lesson/36b80307-ad56-4210-b1f6-b421379e8f8e" />
</CardGroup>
