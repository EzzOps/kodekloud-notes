# Auto Instrumentation Using the OpenTelemetry Operator

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-in-Kubernetes/Auto-Instrumentation-Using-the-OpenTelemetry-Operator/page

Explains using the OpenTelemetry Operator to auto-instrument Kubernetes workloads, centralizing instrumentation configuration and injecting language agents via Instrumentation custom resources and annotations.

This article explains how auto-instrumentation works with the OpenTelemetry Operator and how it simplifies collecting telemetry from applications running in Kubernetes. While manual instrumentation remains an option, operator-based auto-instrumentation lets you collect traces, metrics, and logs with minimal code changes.

<Callout icon="lightbulb">
  Auto-instrumentation is ideal when you need quick visibility into running workloads or when you want consistent observability settings across many deployments and namespaces.
</Callout>

<Frame>
  <img alt="The image illustrates a comparison between manual instrumentation and auto-instrumentation for telemetry, highlighting that manual requires explicit coding, while auto collects data with minimal setup." />
</Frame>

Why use auto-instrumentation?

* Fast path to visibility when you lack instrumentation in running workloads.
* Centralized configuration reduces duplication and human error.
* Operator ensures consistent agent injection and environment configuration across pods.

What the Operator does

* Injects language-specific instrumentation libraries or agents into targeted pods.
* Sets environment variables and runtime flags required by those agents.
* Routes telemetry to a configured OpenTelemetry Collector or exporter endpoint.

<Frame>
  <img alt="The image is a diagram illustrating the role of an OpenTelemetry Operator within a Kubernetes cluster, involving namespaces for auto-instrumentation and an OpenTelemetry Collector." />
</Frame>

Instrumentation custom resources (CRs)

A Kubernetes Custom Resource Definition (CRD) extends the API with new kinds. The OpenTelemetry Operator defines an Instrumentation custom resource that centralizes shared observability settings—exporter endpoints, propagators, samplers, and more—so you don't repeat them in every Deployment or Pod.

When an Instrumentation CR exists in a namespace, workloads can opt in via annotations. This model is particularly useful at scale (many namespaces or clusters) for enforcing consistent telemetry configuration.

<Frame>
  <img alt="The image illustrates an &#x22;Instrumentation Custom Resource&#x22; process that auto-instruments a pod, explaining its functions such as setting up auto-instrumentation, holding configuration details, and automatic application use without code changes." />
</Frame>

Example Instrumentation CR

This example creates an Instrumentation CR that directs the operator to export OTLP to a collector and configures propagators and sampling:

```yaml theme={null}
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: demo-instrumentation
spec:
  exporter:
    endpoint: http://demo-collector:4318
  propagators:
    - tracecontext
    - baggage
  sampler:
    type: parentbased_traceidratio
    argument: "1"
```

Exam-style recall question
What is the Kubernetes kind that automatically instruments applications in Kubernetes?
Answer: Instrumentation

How the CR maps to injected environment variables

The Operator translates the Instrumentation spec into environment variables and agent-specific settings inside the injected pod. Common mappings include:

* `spec.exporter.endpoint` → `OTEL_EXPORTER_OTLP_ENDPOINT` (or agent-specific equivalent).
* `spec.propagators` → `OTEL_PROPAGATORS` with comma-separated values.
* `spec.sampler` → `OTEL_TRACES_SAMPLER` and `OTEL_TRACES_SAMPLER_ARG` (or similar).

Illustrative example of injected env vars in a Pod:

```yaml theme={null}
