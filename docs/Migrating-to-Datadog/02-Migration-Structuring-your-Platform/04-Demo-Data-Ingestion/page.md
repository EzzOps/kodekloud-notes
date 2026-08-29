# Demo Data Ingestion

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Migration-Structuring-your-Platform/Demo-Data-Ingestion/page

Guide showing how to deploy Datadog to a k3d Kubernetes cluster, configure API key and operator, instrument a Node.js app, generate traffic, and view metrics logs traces

Welcome to the Datadog data ingestion lesson from the Datadog migration course at KodeKloud. This guide explains how Datadog collects and sends telemetry from your environment and applications to the Datadog platform. You’ll see how Datadog components are deployed to a local k3d Kubernetes cluster, how authentication is configured, how to instrument a Node.js app with tracing and logs, and how to generate traffic to observe telemetry in Datadog (metrics, logs, traces, and profiling).

Key topics covered:

* Datadog Kubernetes UI overview
* Local k3d environment (k3s running in Docker)
* Datadog components in Kubernetes (Agent, Cluster Agent, Operator)
* Installing Datadog via Helm and creating the API key secret
* DatadogAgent CR example (operator-based install)
* Instrumenting a Node.js app with dd-trace
* Building the Docker image and deploying the app pod
* Generating traffic with k6 and viewing logs/traces in Datadog

## Datadog Infrastructure → Kubernetes Overview

From the Datadog console (this demo uses the US5 site), the Infrastructure → Kubernetes Overview gives a concise, high-level view of connected clusters. Clicking a cluster updates dashboards to show counts for clusters, namespaces, nodes, deployments, pods, containers, ReplicaSets, and Services.

<Frame>
  <img alt="The image shows a Datadog dashboard with a menu open for infrastructure options and a main screen displaying no matches found for services and issues. Dashboard links and other features are visible on the right." />
</Frame>

The Kubernetes overview shows useful cluster metrics and summary tiles.

<Frame>
  <img alt="The image shows a dashboard for monitoring Kubernetes resources, displaying various metrics like clusters, nodes, pods, and containers. Each section provides insights into the current state and usage of these resources." />
</Frame>

Scrolling in the Kubernetes overview surfaces FinOps insights and application troubleshooting patterns (e.g., deployments with unavailable replicas, pods in symptomatic phases, container restarts, node and volume details).

<Frame>
  <img alt="The image shows a dashboard for troubleshooting patterns in a Kubernetes environment, focusing on deployments with unavailable replicas. It includes a list of deployments, clusters, namespaces, and their current status." />
</Frame>

Resource utilization dashboards help with capacity planning — CPU/memory usage, over-provisioned workloads, unbound volumes, and recommended dashboards.

<Frame>
  <img alt="The image shows a dashboard interface displaying resource utilization metrics for various pod groups, including CPU and memory usage. It includes sections for unbound volumes, over-provisioned workloads, and recommended dashboards." />
</Frame>

## Local lab environment — k3d (k3s in Docker)

This demo uses k3d, a lightweight tool that runs k3s inside Docker. Each k3d node is a Docker container, so `docker ps` (or `k3d docker ps`) shows Kubernetes nodes as containers.

Example k3d help summary:

```bash theme={null}
