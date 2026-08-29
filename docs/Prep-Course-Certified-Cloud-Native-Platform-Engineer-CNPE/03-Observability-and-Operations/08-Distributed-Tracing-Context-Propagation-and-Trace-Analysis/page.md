# Check Jaeger in the observability namespace and application pods in the workloads namespace
kubectl get pods -n observability
kubectl get pods -n workloads
```

Example output (for reference):

```bash theme={null}
controlplane ~ ✗  kubectl get pods -n observability
NAME                                  READY   STATUS    RESTARTS   AGE
jaeger-fd6d64f9-8246c                 1/1     Running   0          2m19s
jaeger-operator-648447789c-c4kqx      2/2     Running   0          2m32s

controlplane ~ ✗  kubectl get pods -n workloads
NAME                                READY   STATUS    RESTARTS   AGE
frontend-svc-69cd76d4fb-ckqlq       1/1     Running   0          2m28s
inventory-svc-84779cd768-jr52m      1/1     Running   0          2m28s
order-svc-54f6b5764d-mb6rs          1/1     Running   0          2m28s
payment-svc-60bd555596-v6267        1/1     Running   0          2m28s
traffic-generator-865f97bfc-kpbkd   1/1     Running   0          2m27s
```

If you open the Jaeger UI you might notice some services (inventory, order, payment) appear in the service dropdown while `frontend-svc` is missing. The frontend pod can be running and receiving traffic but still not appear in Jaeger if it is not configured to emit traces. The application needs OpenTelemetry environment variables to know to produce and export tracing data.

## How tracing is enabled (overview)

You will add OpenTelemetry environment variables to the frontend deployment so the application exports traces to the Jaeger collector using OTLP:

* `OTEL_SERVICE_NAME`: name shown in Jaeger (e.g., `frontend-svc`)
* `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP endpoint for the Jaeger collector (cluster DNS)
* `OTEL_EXPORTER_OTLP_PROTOCOL`: `grpc` (4317) or `http/protobuf` (4318)
* `OTEL_TRACES_EXPORTER`: typically `otlp`

These variables instruct the OpenTelemetry SDK in your app where and how to send traces.

## Verify the Jaeger collector service and its ports

Before patching the deployment, confirm the collector service and exposed OTLP ports in the `observability` namespace:

```bash theme={null}
kubectl get svc -n observability
```

Example output showing the `jaeger-collector` with OTLP ports:

```bash theme={null}
NAME                           TYPE        CLUSTER-IP      PORT(S)
jaeger-agent                   ClusterIP   172.20.204.3    5775/UDP,5778/TCP,6831/UDP,6832/UDP,14271/TCP
jaeger-collector               ClusterIP   172.20.204.3    9411/TCP,14250/TCP,14267/TCP,14268/TCP,14269/TCP,4317/TCP,4318/TCP
jaeger-query                   ClusterIP   172.20.161.35   16686/TCP
jaeger-ui-nodeport             NodePort    172.20.161.35   16686:30086/TCP
```

Quick reference: gRPC uses port `4317`; HTTP/protobuf uses `4318`. Make sure the protocol you set in `OTEL_EXPORTER_OTLP_PROTOCOL` matches the port you target — mismatch is a frequent cause of missing traces.

<Callout icon="lightbulb">
  Ensure the container name you patch matches the container name defined in the deployment. Patching the wrong container leaves the environment variables unapplied and the service will continue not to emit traces.
</Callout>

## Patch the frontend deployment to emit traces

Create or edit a patch that injects the OpenTelemetry environment variables into the frontend container. Example patch snippet (YAML):

```yaml theme={null}
spec:
  template:
    spec:
      containers:
        - name: frontend-svc
          env:
            - name: OTEL_SERVICE_NAME
              value: "frontend-svc"
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://jaeger-collector.observability.svc.cluster.local:4317"
            - name: OTEL_EXPORTER_OTLP_PROTOCOL
              value: "grpc"
            - name: OTEL_TRACES_EXPORTER
              value: "otlp"
```

Apply the patch and wait for the rollout:

```bash theme={null}
# Patch the deployment using a local file named frontend-patch.yaml
kubectl patch deployment frontend-svc -n workloads --patch "$(cat frontend-patch.yaml)"

# Wait for the new pod to roll out
kubectl rollout status deployment/frontend-svc -n workloads
```

Notes:

* If your cluster uses the collector in a different namespace, update the endpoint DNS accordingly (for example, `jaeger-collector.<namespace>.svc.cluster.local`).
* Choose `grpc` and port `4317` together, or `http/protobuf` and port `4318` together.

## Recommended environment variables (table)

| Variable                      | Purpose                                              | Example value                                                  |
| ----------------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| `OTEL_SERVICE_NAME`           | Human-friendly service name in Jaeger                | `frontend-svc`                                                 |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint for the collector (cluster DNS + port) | `http://jaeger-collector.observability.svc.cluster.local:4317` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | Transport protocol for OTLP                          | `grpc` or `http/protobuf`                                      |
| `OTEL_TRACES_EXPORTER`        | Which exporter to use                                | `otlp`                                                         |

## Confirm traces in Jaeger

After the new pod starts with the environment variables applied:

1. Open the Jaeger UI (see Jaeger docs: [https://www.jaegertracing.io/docs/latest/getting-started/](https://www.jaegertracing.io/docs/latest/getting-started/)).
2. Refresh the service dropdown — `frontend-svc` should now be available.
3. Search for traces and inspect any trace to view the waterfall visualization.

<Frame>
  <img alt="The image shows a Jaeger UI trace visualization for a &#x22;GET&#x22; request to &#x22;frontend-svc&#x22; with multiple service calls, depicting the duration and sequence of various service operations over a timeline." />
</Frame>

Interpretation tips:

* The top-level span is the overall request (frontend); nested spans are downstream calls.
* The widest span typically indicates where time is being spent — start investigating there (in the example, `inventory-svc` dominates latency).
* In large systems, the waterfall view quickly highlights the slowest component and the sequence of calls.

## Troubleshooting checklist

* Confirm the four OpenTelemetry environment variables are present in the running pod:
  * `kubectl describe pod <pod-name> -n workloads` or `kubectl exec -n workloads <pod> -- printenv | grep OTEL`
* Verify the OTLP endpoint points to the correct collector service DNS and port.
* Ensure `OTEL_EXPORTER_OTLP_PROTOCOL` matches the endpoint port:
  * `grpc` → port `4317`
  * `http/protobuf` → port `4318`
* Make sure `OTEL_TRACES_EXPORTER` is set to `otlp`.
* Confirm you patched the correct deployment and container name.

<Callout icon="warning">
  If traces do not appear, the most common issues are: incorrect collector endpoint (DNS or port), protocol/port mismatch, or patching the wrong container name. Double-check those first.
</Callout>

## Wrap-up and next steps

This walkthrough showed how to enable OpenTelemetry instrumentation for a Kubernetes-deployed service and visualize distributed traces in Jaeger. Try these steps in a lab or test cluster, and experiment with different OTLP protocols and collector configurations to understand how instrumented services communicate with Jaeger.

Further reading:

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Jaeger Tracing: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/9507aaae-93db-4f66-9d14-017d3e6651d8" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/4da36e12-ad6b-4d91-a8b8-451e1bf4b8fe" />
</CardGroup>


# Distributed Tracing Context Propagation and Trace Analysis

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Observability-and-Operations/Distributed-Tracing-Context-Propagation-and-Trace-Analysis/page

Explains distributed tracing, trace data model and context propagation, configuring OpenTelemetry to export traces to Jaeger, and using traces to locate performance bottlenecks in microservices.

We've already covered metrics and alerting. This lesson focuses on the third observability pillar: distributed tracing.

* Metrics tell you *something* is slow (for example, p99 latency = 1.3s).
* Logs provide context for a specific service (for example, a payment timeout at 1,200ms).
* Traces show the full, end-to-end path of a request so you can pinpoint *where* the bottleneck lives.

By the end of this lesson you'll understand the trace data model, how context propagation works, how to configure OpenTelemetry (OTEL) to export traces to Jaeger, and how to read a trace to find the performance bottleneck.

<Frame>
  <img alt="The image lists five learning objectives related to distributed systems, trace data models, context propagation, OpenTelemetry configuration, and using Jaeger for trace analysis. The objectives are numbered and color-coded." />
</Frame>

Conceptual overview

Think of tracing as package tracking from Cairo to London. Each time the package is scanned (local post office, sorting center, airport, customs, final delivery) you get timestamps for when the package was handled. If delivery took 21 days, the scans reveal which hop caused the delay (for example, Heathrow Customs held it for 18 days). In a distributed system, spans are those scans; a trace is the full journey.

<Frame>
  <img alt="The image illustrates a package delivery process from Cairo to London, highlighting the difference in delay identification between using and not using tracking scans, with emphasis on the role of distributed tracing." />
</Frame>

Why tracing matters

In microservices, a single user request can traverse many services. Imagine six services: five respond in \~25ms each, and one payment service takes 1,200ms. The slow payment service makes the entire request take over a second. Without traces, you would need to query each service to find the culprit. Tracing reveals the slow hop immediately.

<Frame>
  <img alt="The image illustrates a diagram of a user request across various services, highlighting a significant delay in the Payment Service with a response time of 1,200ms. This delay is emphasized as a &#x22;Needle-in-a-Haystack Problem.&#x22;" />
</Frame>

How the three pillars complement each other

| Pillar  | What it answers                                      | Typical use                                            |
| ------- | ---------------------------------------------------- | ------------------------------------------------------ |
| Metrics | "What" — aggregate view (e.g., p99 latency = `1.3s`) | Detect anomalies, set alerts                           |
| Logs    | "Why" — detailed events in a service                 | Debug specific errors or exceptions                    |
| Traces  | "Where" — end-to-end request flow and timing         | Pinpoint which service/span causes latency or failures |

Each pillar narrows the investigation for the next: metrics detect the problem, logs add context, traces show where to focus.

<Frame>
  <img alt="The image illustrates the &#x22;Needle-in-a-Haystack&#x22; problem in monitoring, comparing what metrics, logs, and traces reveal, with a conclusion that tracing shows the full journey of a request across all services." />
</Frame>

Trace building blocks

| Component                 | Purpose                                                                 | Key fields / examples                                                   |
| ------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Trace                     | The full journey for one request across multiple services               | `trace_id` (unique identifier for the trace)                            |
| Span                      | One unit of work within a trace (HTTP call, DB query, etc.)             | `span_id`, start time, duration, attributes/tags, events (logs), status |
| Parent-child relationship | Spans form a tree. A parent span may have many child spans              | Parent span links to child span IDs                                     |
| Context propagation       | Moves trace context (trace ID + span context) across process boundaries | Typically via HTTP headers (e.g., `traceparent`)                        |

<Frame>
  <img alt="The image illustrates the Trace Data Model, detailing three components: Trace, Span, and Context, each with descriptions of their purpose, identity, and contents. It emphasizes the relationship between these components in distributed systems using HTTP headers." />
</Frame>

OpenTelemetry (OTEL) — standardized instrumentation

OpenTelemetry is the CNCF standard for instrumentation and context propagation. It is vendor-neutral: instrument once and export to multiple backends. OTEL supports:

* Auto-instrumentation for HTTP, gRPC, common database clients
* Automatic injection/extraction of trace context on outgoing/incoming requests
* OTLP (OpenTelemetry Protocol) as the common export format for traces and metrics

<Frame>
  <img alt="The image is an infographic about OpenTelemetry, highlighting its features: vendor-neutral instrumentation, auto-instrumentation, and context propagation." />
</Frame>

Configuring OpenTelemetry with environment variables

You typically configure the OTEL SDK via environment variables to identify your service and tell the SDK where to export traces. Common settings:

```bash theme={null}
