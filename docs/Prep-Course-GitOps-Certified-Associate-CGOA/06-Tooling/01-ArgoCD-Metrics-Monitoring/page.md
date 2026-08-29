# ArgoCD Metrics Monitoring

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Tooling/ArgoCD-Metrics-Monitoring/page

How to integrate ArgoCD metrics with Prometheus Operator using ServiceMonitor and PodMonitor to scrape endpoints, generate Prometheus configs, and visualize metrics in Grafana

This guide explains how ArgoCD exposes metrics and how the Prometheus Operator discovers and configures Prometheus to scrape those endpoints using custom resources such as ServiceMonitor and PodMonitor. Follow the sequence below to verify and configure scraping for ArgoCD metrics and to visualize them in Grafana.

Key concepts covered:

* How ArgoCD exposes metrics via Services
* How the Prometheus Operator uses ServiceMonitor/PodMonitor CRs to generate scrape configs
* Verifying the generated Prometheus configuration and troubleshooting common issues
* Visualizing ArgoCD metrics in Grafana

Overview of the flow

1. Install the Prometheus Operator and its CRDs (ServiceMonitor / PodMonitor / Prometheus).
2. ArgoCD exposes metrics through Services that use a named `metrics` port and identifiable labels.
3. Create ServiceMonitor resources that select those Services and define scrape endpoints.
4. The Prometheus CR selects matching ServiceMonitors and the operator generates Prometheus `scrape_configs`.
5. The operator triggers a config-reloader sidecar that updates Prometheus and begins scraping the ArgoCD endpoints.

> **lightbulb** Ensure the Prometheus Operator and its CRDs are installed in the cluster before applying any ServiceMonitor or PodMonitor resources; otherwise these custom resources will not be recognized.

## Step-by-step details

### 1) Inspect the generated Prometheus configuration

The Prometheus Operator writes generated configuration files into the Prometheus pod via a config-reloader sidecar. To inspect the generated config from the config-reloader container:

```bash theme={null}
