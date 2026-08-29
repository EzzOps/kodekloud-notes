# OpenTelemetry in Kubernetes

Source: https://notes.kodekloud.com/docs/Prep-Course-OpenTelemetry-Certified-Associate-OTCA-Certification/OpenTelemetry-in-Kubernetes/OpenTelemetry-in-Kubernetes/page

Guide to applying OpenTelemetry in Kubernetes, covering Collector and Operator deployment patterns, metadata enrichment, auto-instrumentation, and best practices for observing ephemeral containerized workloads

Having covered the OpenTelemetry fundamentals, this article explains how OpenTelemetry is applied in Kubernetes.

OpenTelemetry is the open standard for collecting traces, metrics, and logs. Kubernetes hosts many modern applications, and observability is critical in this dynamic environment. This guide explains why observability matters in Kubernetes, how telemetry in Kubernetes differs from traditional VM or bare-metal deployments, and the roles the OpenTelemetry Collector and Operator play in making observability at scale practical.

In Kubernetes, workloads are distributed across many pods and nodes. Pods are ephemeral — they can be created, destroyed, or rescheduled at any time — and workloads scale up and down frequently. Because of this dynamic nature, traditional monitoring approaches designed for static servers do not provide a complete picture. Observability in Kubernetes must follow workloads as they move and scale, and it must attach the right metadata so signals can be correlated back to the originating workloads.

> **lightbulb** In Kubernetes, telemetry must carry rich metadata (for example, pod name, namespace, labels, and node) so you can correlate traces/metrics/logs to the correct workload as containers are created and destroyed.

<Frame>
  <img alt="The image illustrates the importance of observability in Kubernetes with a diagram showing nodes and containers, highlighting how observability helps manage ephemeral pods, dynamic scaling, and complex networking." />
</Frame>

## Kubernetes telemetry vs. VMs / bare metal

Telemetry on VMs or bare-metal hosts is often simpler because hosts and processes tend to be long-lived and relatively static. You can rely on stable identifiers and persistent instrumentation. Kubernetes is different: applications run in containers inside pods, across many nodes, and identities are ephemeral. To make telemetry useful in this environment, each signal (trace span, metric, log) should include Kubernetes-specific attributes such as:

* pod name and UID
* namespace
* labels and annotations
* deployment, ReplicaSet, or StatefulSet name
* node name and node metadata

These attributes enable you to group, filter, and correlate telemetry across the cluster even as pods are created and destroyed.

<Frame>
  <img alt="The image compares Kubernetes telemetry with VM or bare-metal, highlighting that VMs or physical servers are static with fixed processes, while Kubernetes is dynamic with multiple nodes, pods, and containers, requiring metadata like pod name, namespace, labels, and node information." />
</Frame>

> **warning** If Kubernetes metadata is not attached to telemetry, observability systems cannot reliably attribute signals to the correct workloads—this leads to noisy dashboards, poor alerting, and harder troubleshooting.

## Key OpenTelemetry components and patterns for Kubernetes

To collect, enrich, and export telemetry in Kubernetes, OpenTelemetry provides components and deployment patterns tailored for dynamic environments:

* OpenTelemetry Collector — a vendor-agnostic telemetry pipeline that receives, processes, and exports traces, metrics, and logs. The Collector can be deployed in multiple ways in Kubernetes:
  * sidecar (deployed in the same pod as the application),
  * daemonset/agent (one per node to collect from all pods on that node),
  * gateway/central instance (centralized processing and exporting).
* OpenTelemetry Operator — a Kubernetes operator that simplifies deploying and managing Collector instances through CustomResourceDefinitions (CRDs) and can assist with auto-instrumentation workflows by injecting or managing instrumentation-related resources.
* Auto-instrumentation — language-specific agents or SDKs that automatically capture traces/metrics/logs with minimal code changes. The Operator can help install and configure auto-instrumentation for supported runtimes.

These components let you capture telemetry that preserves context and includes Kubernetes metadata, enabling accurate mapping of signals back to the correct service or workload. The Operator handles lifecycle and configuration of Collectors, and can integrate with pod injection mechanisms so telemetry from new pods is collected automatically.

<Frame>
  <img alt="The image is a diagram explaining the architecture of an OpenTelemetry Operator within a Kubernetes cluster, showing auto-instrumentation and the OTel Collector sending data to an observability backend." />
</Frame>

## Collector deployment patterns (summary)

Below is a concise reference for common Collector deployment patterns, their use cases, and examples.

| Deployment pattern          | Use case                                                                          | Example / notes                                                                                             |
| --------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Sidecar                     | Low-latency, per-pod processing; ensures telemetry stays local to the application | Use when you need request-level context or local buffering; inject a Collector container into the pod spec. |
| DaemonSet / Agent           | One Collector per node to aggregate telemetry from all pods on that node          | Good for minimizing resource duplication across pods; use a DaemonSet and host-level receivers.             |
| Gateway / Central Collector | Centralized processing, advanced batching, and exporting                          | Deploy as a Service/Deployment to centralize processing and route to backend exporters.                     |

Typical commands and resources you might use:

* Install Operator: `kubectl apply -f <operator-manifest.yaml>`
* Deploy a Collector CR: `kubectl apply -f collector-cr.yaml`
* View pods: `kubectl get pods -n <namespace>`

## Operator, CRDs, and auto-instrumentation

The OpenTelemetry Operator provides CRDs for defining Collector instances and configurations, simplifying lifecycle management:

* Collector CRD — declare Collector instances, configuration, and deployment type (sidecar/daemonset/gateway).
* Instrumentation CRD — (where supported) instructs the Operator to enable auto-instrumentation for specific runtimes by injecting agents or setting environment variables.

Using the Operator allows teams to standardize telemetry pipelines across clusters, manage upgrades, and ensure consistent enrichment of telemetry with Kubernetes metadata.

## Practical tips

* Always ensure your telemetry pipeline includes a Kubernetes resource detector or metadata processor so traces, metrics, and logs are enriched before export.
* Choose sidecars for strict per-pod isolation and low-latency needs; use DaemonSets for node-level aggregation to reduce per-pod overhead.
* Use the Operator to manage Collector lifecycle, CRDs, and to automate instrumentation where possible.

## Links and references

* OpenTelemetry Collector: [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)
* OpenTelemetry Operator: [https://github.com/open-telemetry/opentelemetry-operator](https://github.com/open-telemetry/opentelemetry-operator)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* OpenTelemetry auto-instrumentation: [https://opentelemetry.io/docs/instrumentation/](https://opentelemetry.io/docs/instrumentation/)

Subsequent sections will examine concrete Collector deployment examples (sidecar vs agent vs gateway), show Operator CRD examples for managing Collectors and instrumentation, and provide configuration snippets to ensure telemetry is enriched with Kubernetes metadata before export.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-opentelemetry-certified-associate-certification-otca/module/09e46ae9-895f-4e3f-98dd-c7be94303a09/lesson/949d4584-36b4-4f84-8cd3-4ee61fca9edc)
