# Example injected env vars in a Pod (illustrative)
env:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://demo-collector:4318"
  - name: OTEL_PROPAGATORS
    value: "tracecontext,baggage"
  - name: OTEL_TRACES_SAMPLER
    value: "parentbased_traceidratio"
  - name: OTEL_TRACES_SAMPLER_ARG
    value: "1"
```

Sampling options

You control sampling behavior from the Instrumentation CR. The snippet below shows sampler configuration and common choices:

```yaml theme={null}
# In the Instrumentation CR
spec:
  sampler:
    type: parentbased_traceidratio
    argument: "1"  # 1 = 100%; 0.25 = 25%; 0 = 0%
```

Common sampler types:

| Sampler type               | Behavior                                                                       |
| -------------------------- | ------------------------------------------------------------------------------ |
| `always_on`                | Sample all traces                                                              |
| `always_off`               | Sample no traces                                                               |
| `traceidratio`             | Sample approximately the fraction set by `argument` (e.g., `"0.2"` = 20%)      |
| `parentbased_traceidratio` | Parent-based sampling; when no parent exists, `argument` controls the fraction |

Enabling auto-instrumentation for workloads

Workloads opt in by adding annotations on the Pod template. Each runtime has a specific annotation key.

Pod template annotations example:

```yaml theme={null}
spec:
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-java: "true"
        instrumentation.opentelemetry.io/inject-python: "true"
        instrumentation.opentelemetry.io/inject-nodejs: "true"
        instrumentation.opentelemetry.io/inject-dotnet: "true"
```

Patch an existing Deployment to enable Python auto-instrumentation:

```bash theme={null}
kubectl -n appns patch deploy web --type merge -p '
{
  "spec": {"template": {"metadata": {"annotations": {
      "instrumentation.opentelemetry.io/inject-python": "true"
  }}}}
}'
```

Annotation values and semantics

| Annotation value | Meaning                                                                     |
| ---------------- | --------------------------------------------------------------------------- |
| `"true"`         | Use the default Instrumentation CR in the same namespace                    |
| `"name"`         | Use an Instrumentation CR in the same namespace by name                     |
| `"ns/name"`      | Use an Instrumentation CR from another namespace (useful for shared config) |
| `"false"`        | Explicitly opt out of injection for this workload                           |

<Frame>
  <img alt="The image titled &#x22;Annotating Workloads&#x22; provides guidelines on using annotations for instrumentation in different namespaces, with a color-coded legend for pods representing true, name, ns/name, and false values." />
</Frame>

Namespace-level opt-in

Instead of annotating individual pod templates, you can annotate a Namespace to enable injection for all pods in that namespace:

```yaml theme={null}
# Opt-in at Namespace level (affects all Pods in the namespace)
apiVersion: v1
kind: Namespace
metadata:
  name: appns
  annotations:
    instrumentation.opentelemetry.io/inject-python: "true"
```

<Callout icon="warning">
  Use namespace-level injection with care. It will affect all pods in the namespace, including system, test, or utility pods that may not need instrumentation.
</Callout>

Supported languages

The Operator supports injecting language-specific agents and setting the appropriate environment variables. Commonly supported runtimes include Java, .NET, Node.js, Python, and Go.

<Frame>
  <img alt="The image lists supported programming languages for OpenTelemetry instrumentation, including Java, .NET, Node.js, Python, and Go, with corresponding URLs." />
</Frame>

Key takeaways

* The OpenTelemetry Operator centralizes observability settings through the Instrumentation custom resource.
* Instrumentation CRs define exporters, propagators, samplers, and other shared configuration to avoid per-deployment duplication.
* Workloads opt in to auto-instrumentation via pod annotations or namespace annotations; annotations can reference Instrumentation CRs across namespaces.
* Apply namespace-level injection carefully to prevent unintentional agent injection.

<Frame>
  <img alt="The image presents key takeaways about Kubernetes observability, highlighting the role of operators and instrumentation in centralizing various components. The design features a gradient background with numbered points." />
</Frame>

Links and references

* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* OpenTelemetry Operator (GitHub): [https://github.com/open-telemetry/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-operator)
* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)

That covers the essentials of OpenTelemetry auto-instrumentation using the Operator.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/09e46ae9-895f-4e3f-98dd-c7be94303a09/lesson/4ac6b8ec-ac71-475f-bb59-b5823a7b89db" />
</CardGroup>


# Demo OpenTelemetry Collector k8s

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-in-Kubernetes/Demo-OpenTelemetry-Collector-k8s/page

Deploying an OpenTelemetry Collector on Kubernetes with Helm, configuring node-local DaemonSet, enabling Kubernetes presets, exposing OTLP host ports, instrumenting an app, and optionally exporting traces to Jaeger

In this guide you'll deploy an OpenTelemetry Collector into a Kubernetes cluster (using Helm) and instrument a sample application so it sends telemetry (traces, metrics, logs) to the collector running in-cluster. This walkthrough uses a Helm-based Collector deployment (DaemonSet in this example) and shows how to:

* fetch and customize the Collector Helm chart values,
* enable Kubernetes-specific presets (attributes, kubelet metrics, logs),
* expose node-local OTLP endpoints via host ports,
* deploy an instrumented application that sends OTLP to the node-local collector,
* optionally forward traces to Jaeger for visualization.

This article demonstrates the direct Helm approach only (OpenTelemetry Operator is out of scope).

## Environment

For this demo I created a local kind cluster with three nodes (one control-plane and two workers). Verify nodes with:

```bash theme={null}
kubectl get node
NAME                 STATUS      ROLES           AGE   VERSION
kind-control-plane   Ready       control-plane   39s   v1.33.1
kind-worker          Ready       <none>          25s   v1.33.1
kind-worker2         Ready       <none>          25s   v1.33.1
```

We use Helm to install the OpenTelemetry Collector chart.

Add and verify the Helm repo:

```bash theme={null}
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo list
