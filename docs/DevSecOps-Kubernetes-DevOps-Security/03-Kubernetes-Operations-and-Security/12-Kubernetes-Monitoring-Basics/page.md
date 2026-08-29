# Kubernetes Monitoring Basics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Kubernetes-Monitoring-Basics/page

This guide explores essential Kubernetes monitoring concepts, built-in tools, and an advanced stack using Prometheus and Grafana for comprehensive observability.

Kubernetes streamlines container orchestration across clouds, but its abstraction can hide critical insights into cluster health and resource usage. In this guide, we’ll explore essential monitoring concepts, built-in tools, and an advanced open-source stack using Prometheus and Grafana.

## Kubernetes Monitoring Overview

To maintain reliability and performance, monitor:

* **Cluster & Node Metrics**: CPU, memory usage, availability, capacity
* **Deployment & Pod Status**: Desired vs. running replicas, CrashLoopBackOff errors
* **Pod Resource Consumption**: Requests and limits for CPU/memory
* **Application-Level Health**: Latency, throughput, error rates

A major challenge is capturing and storing vast quantities of metrics to enable trend analysis and alerting over time.

> **lightbulb** Without persistent storage, short-lived metrics are lost and you miss critical events that could help diagnose incidents.

## Built-in Monitoring Tools

Kubernetes includes several basic monitoring components:

| Tool                 | Function                                             | Limitation                                      |
| -------------------- | ---------------------------------------------------- | ----------------------------------------------- |
| cAdvisor             | Container resource collector in the kubelet          | No long-term storage, trend analysis, or alerts |
| Metrics Server       | Aggregates CPU/memory from cAdvisor into Metrics API | No built-in dashboards or advanced queries      |
| Kubernetes Dashboard | Web UI for namespaces, workloads, and basic metrics  | Real-time only; no historical trend analysis    |

> **triangle-alert** For production environments requiring SLA guarantees, these out-of-the-box tools are insufficient. Plan for a full monitoring stack.

Retrieve real-time metrics:

```bash theme={null}
