# OpenTelemetry Kubernetes Operator

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-in-Kubernetes/OpenTelemetry-Kubernetes-Operator/page

Guide to the OpenTelemetry Kubernetes Operator that automates deploying and managing the OpenTelemetry Collector and automatic instrumentation in clusters, including installation and lifecycle management.

The OpenTelemetry Kubernetes Operator automates the deployment and lifecycle of the OpenTelemetry Collector and the auto-instrumentation layer inside a Kubernetes cluster. This guide explains how the operator works, what it manages, and how to get started with a minimal deployment.

At a high level, the operator runs inside your cluster and manages two primary concerns:

* The OpenTelemetry Collector (deployed as a Deployment, DaemonSet, or sidecar).
* Automatic instrumentation injection that enables workloads to emit telemetry without changing application code.

When auto-instrumentation is enabled across namespaces, instrumented workloads start sending telemetry to the operator-managed collector. The collector then receives and routes that telemetry to your observability backend.

<Frame>
  <img alt="The image illustrates how the OpenTelemetry Operator manages observability in Kubernetes, showing the flow and components like namespaces, auto-instrumentation, and the OTel Collector within a Kubernetes cluster." />
</Frame>

## Getting started: install the operator

There are two common installation methods:

* Helm (recommended for most users): simple, configurable, and integrates well with CI/CD.
* Apply YAML manifests directly: useful for air-gapped or tightly controlled clusters.

Before installing, ensure a certificate manager is available in the cluster. The operator requires webhook TLS certificates to perform automatic injection and manage CRD webhooks.

<Callout icon="lightbulb">
  `cert-manager` (or an equivalent certificate manager) must be present in the cluster before installing the operator because the operator creates webhook certificates automatically. See the cert-manager documentation for installation steps.
</Callout>

### Helm installation example

Add the official Helm repository, update, and install the operator into its own namespace:

```bash theme={null}
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm install opentelemetry-operator open-telemetry/opentelemetry-operator --namespace opentelemetry-operator --create-namespace
```

### Apply manifests directly

If you prefer not to use Helm, the operator repository provides YAML manifests that you can apply with `kubectl apply -f`. See the operator repo for the canonical manifests and instructions.

<Frame>
  <img alt="The image provides instructions for installing an operator, recommending installation via Helm chart, applying YAML directly, and requiring cert-manager for the operator." />
</Frame>

## Deploy a managed OpenTelemetry Collector

The operator can create and manage an OpenTelemetry Collector for you using the `OpenTelemetryCollector` custom resource. Below is a minimal example that deploys a collector in `deployment` mode with an OTLP receiver and a logging exporter.

Save and apply this YAML after the operator is installed:

```yaml theme={null}
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: my-otel-collector
spec:
  mode: deployment
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
          http:
    exporters:
      logging:
        loglevel: debug
    service:
      pipelines:
        traces:
          receivers: [otlp]
          exporters: [logging]
```

This CR instructs the operator to create a Kubernetes Deployment (or the selected mode) running the configured collector. You can extend the `config` block to add additional receivers, processors, exporters, and pipelines.

## What the operator manages

The OpenTelemetry Operator simplifies observability in Kubernetes by automating many operational tasks. Key responsibilities include:

* Ports & Networking: create Kubernetes Services to expose the collector and manage configured ports.
* Monitoring & Endpoints: register and manage collector endpoints so instrumented workloads can send telemetry across namespaces.
* Upgrades & Lifecycle: handle upgrades, rollouts, restarts, and lifecycle events for operator-managed collectors and instrumentation artifacts.
* Auto-instrumentation: configure and inject SDKs or sidecar instrumentations into workloads via webhooks.

| Capability             | What it does                                                    | Example                                 |
| ---------------------- | --------------------------------------------------------------- | --------------------------------------- |
| Ports & Networking     | Creates Services and exposes configured ports for the collector | `Service` with OTLP port                |
| Monitoring & Endpoints | Manages endpoints and cross-namespace telemetry flow            | Configure OTLP receivers and routing    |
| Upgrades & Lifecycle   | Automates rolling updates and configuration rollouts            | Operator-controlled Deployment updates  |
| Auto-instrumentation   | Performs injection for supported runtimes via webhooks          | JVM/Node auto-instrumentation injection |

<Frame>
  <img alt="The image outlines the key capabilities of the OpenTelemetry Operator, highlighting its roles in Ports & Networking, Monitoring & Endpoints, and Upgrades & Lifecycle." />
</Frame>

Because the operator supports multiple deployment patterns (Deployment, DaemonSet, sidecar), automatic service creation, and webhook certificate management, it removes much of the manual effort required to run telemetry agents or instrument applications in Kubernetes.

## Summary

* The OpenTelemetry Operator simplifies deployment and lifecycle management of the OpenTelemetry Collector and auto-instrumentation for Kubernetes workloads.
* Install via Helm (recommended) or by applying manifests directly. Ensure `cert-manager` (or equivalent) is present to provision webhook TLS certificates.
* The operator automates service/port creation, endpoint management, rollouts, and automatic instrumentation injection.

## Links and references

* OpenTelemetry Operator repository: [https://github.com/open-telemetry/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-operator)
* cert-manager documentation: [https://cert-manager.io/docs/](https://cert-manager.io/docs/)
* OpenTelemetry project: [https://opentelemetry.io/](https://opentelemetry.io/)
* Helm documentation: [https://helm.sh/docs/](https://helm.sh/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/09e46ae9-895f-4e3f-98dd-c7be94303a09/lesson/0bdd2c57-a0b1-479d-8f67-475499c0dc59" />
</CardGroup>
