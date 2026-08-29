# Example output:
# NAME             URL
# open-telemetry   https://open-telemetry.github.io/opentelemetry-helm-charts
```

<Frame>
  <img alt="This image shows a webpage from OpenTelemetry's documentation about Kubernetes integration, describing components like the OTLP Receiver, Kubernetes Attributes Processor, and Kubeletstats Receiver. It includes a sidebar menu with documentation sections and a dark theme interface." />
</Frame>

## 1 — Prepare a local values.yaml

Fetch the chart's default values into a local `values.yaml` so you can edit the Collector configuration (mode, image, presets, config):

```bash theme={null}
helm show values open-telemetry/opentelemetry-collector > values.yaml
```

Open `values.yaml` in your editor/IDE and edit the sections you need: `mode`, `image`, `presets`, and `config` (receivers/processors/exporters/pipelines). I prefer editing locally for clarity and versioning.

<Frame>
  <img alt="The image shows a Visual Studio Code workspace with a terminal open, displaying a Kubernetes configuration script related to OpenTelemetry collector settings." />
</Frame>

## 2 — Presets: enable built-in Kubernetes integrations

The Helm chart exposes "presets" that add common Kubernetes-related components (kubernetesAttributes processor, kubeletstats receiver, host metrics, file log collection, etc.). Enabling a preset also adjusts RBAC, volumes, and mounts automatically.

Example minimal preset snippets to include under `presets:` in `values.yaml`:

```yaml theme={null}
presets:
  logsCollection:
    enabled: true
    includeCollectorLogs: false
    storeCheckpoints: false
    maxRecombineLogSize: 102400

  kubernetesAttributes:
    enabled: true
    extractAllPodLabels: false
    extractAllPodAnnotations: false

  kubeletMetrics:
    enabled: true

  hostMetrics:
    enabled: false

  kubernetesEvents:
    enabled: false

mode: daemonset
image:
  repository: otel/opentelemetry-collector-k8s
  pullPolicy: IfNotPresent
```

Enabling `kubernetesAttributes` enriches telemetry with pod, container, and node metadata (pod name, pod UID, node name, labels, etc.), which is highly valuable when troubleshooting or visualizing traces/metrics/logs.

<Frame>
  <img alt="The image shows a webpage from OpenTelemetry documentation, specifically about the Kubernetes Attributes Processor. It includes a table detailing deployment patterns and usability, along with a description of the processor's functionalities." />
</Frame>

There are prebuilt receivers such as `kubeletstats` to collect node/pod/container metrics:

```yaml theme={null}
presets:
  kubeletMetrics:
    enabled: true

# Additional kubelet receiver configuration (if needed)
receivers:
  kubeletstats:
    collection_interval: 10s
    auth_type: serviceAccount
    endpoint: '${env:K8S_NODE_NAME}:10250'
    insecure_skip_verify: true
    metric_groups:
      - node
      - pod
      - container
```

<Frame>
  <img alt="The image displays a webpage from OpenTelemetry documentation, detailing the configuration of Kubernetes receivers for telemetry data collection. It includes sections for &#x22;Kubeletstats Receiver&#x22; and &#x22;Filelog Receiver&#x22; with navigation links on the side." />
</Frame>

## 3 — Mode: daemonset vs deployment (choose the right topology)

A Collector can run as a DaemonSet (node-local), Deployment (centralized), or StatefulSet. Choose based on collection needs, latency, and scaling.

| Mode       | Use Case                                              | Pros                                                                         | Cons                                                              |
| ---------- | ----------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| DaemonSet  | Node-local collection (host metrics, node-local OTLP) | Low network hops, per-node collection, useful for node-local instrumentation | More pods to manage; storage for logs on nodes                    |
| Deployment | Centralized collection and processing                 | Easier to scale collectors, centralized buffering                            | Potential higher latency and network hops, single ingestion point |

> **lightbulb** DaemonSet ensures a collector runs on every node (useful to keep network hops low and to collect host-level metrics). Deployment gives centralized collectors and may be easier to scale for ingestion/backpressure.

For this demo we use `mode: daemonset` so apps can send OTLP to a collector running on the same node.

## 4 — Collector configuration (receivers / processors / exporters / pipelines)

Under `config:` in `values.yaml` define receivers, processors, exporters, extensions, and service pipelines. A simple example enabling OTLP receivers and a debug exporter:

```yaml theme={null}
config:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318

  processors:
    batch: {}
    memory_limiter:
      check_interval: 5s
      limit_percentage: 80
      spike_limit_percentage: 25

  exporters:
    debug: {}

  extensions:
    health_check:
      endpoint: 0.0.0.0:13133

  service:
    telemetry:
      metrics:
        readers:
          - pull:
              exporter:
                prometheus:
                  host: 0.0.0.0
                  port: 8888
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [debug]
      metrics:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [debug]
      logs:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [debug]
```

> **warning** Do not remove the `health_check` extension unless you update the liveness/readiness probes. Removing it can cause the Helm chart's probes to fail and result in CrashLoopBackOff.

## 5 — Install the Collector with Helm

Install the customized chart:

```bash theme={null}
helm install otel-collector open-telemetry/opentelemetry-collector -f values.yaml
```

Helm should report the release is deployed:

```plaintext theme={null}
NAME: otel-collector
LAST DEPLOYED: ...
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES: ...
```

Check the DaemonSet and pods:

```bash theme={null}
kubectl get ds
# NAME                                              DESIRED   CURRENT   READY ...
kubectl get pod
# Pods may initially appear as CrashLoopBackOff while images download or if config errors exist.
```

### Troubleshooting CrashLoopBackOff

If Collector pods crash, inspect logs to find configuration errors:

```bash theme={null}
kubectl logs <collector-pod-name>
```

Common example error when values.yaml contains an invalid key in exporter configuration:

```plaintext theme={null}
Error: failed to get config: cannot unmarshal the configuration: decoding failed due to the following error(s):
'exporters' error reading configuration for 'debug': decoding failed due to the following error(s):
'' has invalid keys: verbosity
```

Fix the config in `values.yaml` and update the release:

```bash theme={null}
helm upgrade otel-collector open-telemetry/opentelemetry-collector -f values.yaml
```

After the upgrade the DaemonSet should converge to the desired number of ready pods:

```bash theme={null}
kubectl get ds
# otel-collector-opentelemetry-collector-agent   2   2   2   ...
kubectl get pod
# Two collector pods, 1/1 Running each
```

## 6 — How the DaemonSet exposes OTLP on node host ports

When using `mode: daemonset`, the chart config maps container ports to host ports (hostPort) so OTLP traffic sent to `http://<node-ip>:4318` or gRPC to `<node-ip>:4317` is delivered to the local collector pod.

Inspect the DaemonSet YAML and node IPs:

```bash theme={null}
kubectl get ds otel-collector-opentelemetry-collector-agent -o yaml > ds.yaml
kubectl get node -o wide
```

Look for port mappings similar to:

```yaml theme={null}
ports:
  - containerPort: 4317
    hostPort: 4317
    name: otlp
    protocol: TCP
  - containerPort: 4318
    hostPort: 4318
    name: otlp-http
    protocol: TCP
```

Now OTLP HTTP to `http://<node-ip>:4318/v1/traces` or OTLP gRPC to `<node-ip>:4317` will reach the node-local collector.

## 7 — Deploy a sample instrumented application

This sample app (`sloppy-networks/traces-py`) periodically generates a trace and exports it via OTLP HTTP to the collector. The app reads the collector host from an environment variable `K8S_NODE_IP` which we populate from the node's IP using a `fieldRef`.

Python tracer configuration excerpt:

```python theme={null}
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import os

print("app starting")
COLLECTOR_HOST = os.getenv('K8S_NODE_IP')
print(COLLECTOR_HOST)

COLLECTOR_URL = f"http://{COLLECTOR_HOST}:4318/v1/traces"

def configure_tracer():
    exporter = OTLPSpanExporter(endpoint=COLLECTOR_URL)
    span_processor = BatchSpanProcessor(exporter)
    resource = Resource.create({
        "service.name": "flight-service"
    })
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
```

Kubernetes Deployment `app-deployment.yaml`:

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
          - name: K8S_NODE_IP
            valueFrom:
              fieldRef:
                apiVersion: v1
                fieldPath: status.hostIP
```

Apply the deployment and check which node the pod lands on:

```bash theme={null}
kubectl apply -f app-deployment.yaml
# deployment.apps/myapp created
kubectl get pod -o wide
# myapp-... 1/1 Running   NODE: kind-worker (for example)
```

Tail the collector logs on the node where the app landed to confirm telemetry arrives and is enriched with Kubernetes attributes:

```bash theme={null}
kubectl logs <collector-pod-on-that-node> -f
# You will see Resource attributes such as k8s.pod.name, k8s.node.name, k8s.deployment.name, etc.
```

Those attributes are supplied by the `kubernetesAttributes` preset enabled earlier.

## 8 — Forward traces to Jaeger (optional)

To visualize traces, deploy Jaeger and configure the Collector to export traces to Jaeger.

Example Jaeger Deployment (all-in-one):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  labels:
    app: jaeger
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
        - name: jaeger
          image: jaegertracing/all-in-one
          ports:
            - containerPort: 16686  # UI
            - containerPort: 4317   # OTLP gRPC
            - containerPort: 4318   # OTLP HTTP ingest
            - containerPort: 14250  # Jaeger gRPC
            - containerPort: 14268  # Jaeger HTTP
```

Internal ClusterIP Service for Jaeger:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: jaeger-internal
  labels:
    app: jaeger
spec:
  selector:
    app: jaeger
  ports:
    - name: otlp-grpc
      port: 4317
      targetPort: 4317
    - name: otlp-http
      port: 4318
      targetPort: 4318
    - name: jaeger-grpc
      port: 14250
      targetPort: 14250
    - name: jaeger-http
      port: 14268
      targetPort: 14268
  type: ClusterIP
```

Optional NodePort for accessing Jaeger UI from outside the cluster:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: jaeger-external
  labels:
    app: jaeger
spec:
  selector:
    app: jaeger
  ports:
    - name: ui
      port: 16686
      targetPort: 16686
      nodePort: 30007
  type: NodePort
```

Apply Jaeger resources:

```bash theme={null}
kubectl apply -f jaeger.yaml
kubectl get svc
# jaeger-internal shown with ports 4317/4318/14250/14268
# jaeger-external NodePort 30007
```

Update `values.yaml` for the Collector to include an exporter pointing to `jaeger-internal:4317` (OTLP gRPC) or `http://jaeger-internal:4318` (OTLP HTTP). Example `config.exporters` and pipeline snippet:

```yaml theme={null}
config:
  exporters:
    otlp/jaeger:
      endpoint: jaeger-internal:4317
      tls:
        insecure: true
  # ... rest of config ...
  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [otlp/jaeger, debug]
```

Upgrade the Helm release so the Collector uses the new exporter:

```bash theme={null}
helm upgrade otel-collector open-telemetry/opentelemetry-collector -f values.yaml
```

Collector pods will restart with the updated configuration. Confirm pods return to Running:

```bash theme={null}
helm list
kubectl get pod
# Collector pods restart and should be Running
```

Access the Jaeger UI via NodePort (example: `http://<node-ip>:30007`) and you should see traces from the instrumented `flight-service`.

## Summary checklist

* Added the OpenTelemetry Helm repository and used `helm show values` to create a local `values.yaml`.
* Enabled presets: `kubernetesAttributes`, `kubeletMetrics`, `logsCollection` to simplify Collector configuration and RBAC.
* Deployed the Collector as a DaemonSet (node-local) with `hostPort` mappings for OTLP (4317/4318).
* Deployed an instrumented Python app that reads the node IP via `status.hostIP` and sends OTLP to `http://<node-ip>:4318/v1/traces`.
* (Optional) Deployed Jaeger and configured the Collector to export traces to a ClusterIP `jaeger-internal` service, then verified traces via Jaeger UI.

This demonstrates a Helm-based flow for deploying an OpenTelemetry Collector on Kubernetes and configuring applications to send telemetry to a node-local collector. For other deployment models and advanced lifecycle management, consider the OpenTelemetry Operator or managed observability backends.

## Links and references

* OpenTelemetry Helm charts: [https://github.com/open-telemetry/opentelemetry-helm-charts](https://github.com/open-telemetry/opentelemetry-helm-charts)
* OpenTelemetry Collector docs: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Jaeger: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/09e46ae9-895f-4e3f-98dd-c7be94303a09/lesson/65f855f2-8928-4f08-ab35-a3d00502f4a8)


# Demo OpenTelemetry Operator Auto Instrumentation

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-in-Kubernetes/Demo-OpenTelemetry-Operator-Auto-Instrumentation/page

Walkthrough to enable automatic OpenTelemetry instrumentation for a Python Flask app in Kubernetes using the OpenTelemetry Operator, Collector, and Jaeger to capture and verify traces.

This walkthrough demonstrates how to enable automatic OpenTelemetry instrumentation for a Python Flask application using the OpenTelemetry Operator and Collector in Kubernetes. The operator can inject language-specific auto-instrumentation into pods so you don't need to modify application code.

What you’ll do:

* Deploy an Instrumentation custom resource (CR) to configure auto-instrumentation.
* Annotate a Deployment to opt the pod into Python auto-instrumentation.
* Generate traffic and verify traces in Jaeger.

Prerequisites:

* A Kubernetes cluster (e.g., kind, GKE, EKS).
* OpenTelemetry Operator and an OpenTelemetry Collector deployed in the cluster.
* A tracing backend such as Jaeger.

For operator installation and examples, see the OpenTelemetry operator docs:
[https://opentelemetry.io/docs/operator/](https://opentelemetry.io/docs/operator/)

<Frame>
  <img alt="This image shows a screenshot of the OpenTelemetry documentation webpage, focusing on the installation and configuration of an OpenTelemetry Operator for Kubernetes. It includes sections on installing the operator, creating a collector, and configuring automatic instrumentation." />
</Frame>

## Sample Flask application (no manual instrumentation)

Save this Flask app as `app.py` (this example contains no OpenTelemetry code):

```python theme={null}
import time
import random
from flask import Flask

app = Flask(__name__)

@app.get("/")
def get_products():
    time.sleep(random.uniform(0.02, 0.08))
    return "Get All Products"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Because the app is uninstrumented, the operator will inject auto-instrumentation at pod startup.

## Verify cluster components

Confirm nodes and that the Collector pod and operator are running:

```bash theme={null}
kubectl get node -o wide
