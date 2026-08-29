# cilium-values.yaml
prometheus:
  enabled: true

operator:
  prometheus:
    enabled: true

hubble:
  # Ensure Hubble is enabled separately if you want flow telemetry
  enabled: true
  metrics:
    enabled:
      - "dns:query;ignoreAAAA"
      - drop
      - tcp
      - flow
      - icmp
      - http
    enableOpenMetrics: true
```

### What these values do

| Helm key                                 | Purpose                                                                                                                       | Notes                                                                                           |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `prometheus.enabled: true`               | Enables ServiceMonitor and related objects created by the Cilium chart so Prometheus Operator can discover Cilium components. | Required when using Prometheus Operator / kube-prometheus-stack.                                |
| `operator.prometheus.enabled: true`      | Exposes Prometheus metrics for the Cilium Operator.                                                                           | Creates a Service and ServiceMonitor for the operator.                                          |
| `hubble.enabled: true`                   | Turns on Hubble to collect flow telemetry.                                                                                    | Only needed if you want flow-level visibility.                                                  |
| `hubble.metrics.enabled`                 | List of Hubble metric families to export.                                                                                     | `"dns:query;ignoreAAAA"` is a single metric spec and must be quoted due to the colon/semicolon. |
| `hubble.metrics.enableOpenMetrics: true` | Export metrics using OpenMetrics format so Prometheus can scrape them.                                                        | Needed for correct scraping and metric exposition.                                              |

> **lightbulb** Check the official Cilium/Hubble metrics documentation for the complete and up-to-date list of metric families and any changes to Helm values: [https://docs.cilium.io/en/stable/observability/metrics/](https://docs.cilium.io/en/stable/observability/metrics/)

## Install or upgrade Cilium with the metrics values

Add the Cilium Helm repository, update it, and apply your values file to install or upgrade Cilium:

```bash theme={null}
helm repo add cilium https://helm.cilium.io/
helm repo update

# Install or upgrade Cilium using the prepared values file
helm upgrade --install cilium cilium/cilium \
  --namespace kube-system \
  --create-namespace \
  -f cilium-values.yaml
```

Kubernetes rolling updates typically handle changes automatically. To ensure the new configuration is picked up immediately, restart the Cilium pods and the operator:

```bash theme={null}
kubectl -n kube-system rollout restart daemonset cilium
kubectl -n kube-system rollout restart deployment cilium-operator
```

## Verify Prometheus discovery and dashboards

Steps to validate metrics collection and visualization:

* Deploy Prometheus and Grafana (for example, via the kube-prometheus-stack) or use an existing Prometheus instance that can discover ServiceMonitors.
* If you use the Prometheus Operator / kube-prometheus-stack, the ServiceMonitors created by the Cilium chart will let Prometheus scrape Cilium, the operator, and Hubble.
* In the Prometheus UI navigate to Status → Targets and look for cilium-\*, cilium-operator, and hubble targets. Confirm they are UP and being scraped.
* Import or create Grafana dashboards to visualize Cilium and Hubble metrics. There are community dashboards and templates for Cilium available that you can adapt.

Helpful troubleshooting checklist:

| Problem                             | Check                                                                                                                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| No cilium targets in Prometheus     | Confirm ServiceMonitor objects exist: `kubectl -n kube-system get servicemonitors` and that Prometheus Operator has appropriate RBAC and label selectors to pick them up. |
| Metrics appear but dashboards empty | Verify metric names in Prometheus (Status → Targets → Metrics) and adapt Grafana queries to the metric families you enabled.                                              |
| Hubble metrics missing              | Ensure `hubble.enabled: true` and `hubble.metrics.enableOpenMetrics: true` are set, and that the Hubble service exists and is selectable by ServiceMonitor.               |

Additional hands-on monitoring resources:

* Learn By Doing: AIOps Foundations - Intelligent Monitoring With Prometheus & Grafana: [https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana)

> **warning** Metric names and Helm values may change across Cilium releases. Always verify keys, supported metric families, and the values schema against the documentation for your specific Cilium version before applying changes in production.

## Links and References

* Cilium observability & metrics: [https://docs.cilium.io/en/stable/observability/metrics/](https://docs.cilium.io/en/stable/observability/metrics/)
* Prometheus documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)
* kube-prometheus-stack (Prometheus Operator): [https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
* Grafana: [https://grafana.com/](https://grafana.com/)
* Helm: [https://helm.sh/](https://helm.sh/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b4c15752-3e42-43af-bedf-4a4c204ef5d8/lesson/a684ca51-0d39-4884-a416-e38c296d6205)


# Section Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Observability/Section-Introduction/page

Guides how to enable and use Cilium Hubble for network observability, inspect flows via CLI and UI, and integrate Cilium metrics with Prometheus for monitoring and alerts

In this lesson we focus on observability for Kubernetes clusters using Cilium. We'll cover:

* What Hubble is and how it provides network-level observability for Cilium-enabled clusters.
* How to inspect and trace traffic flows inside the cluster with Hubble (CLI and UI).
* How to integrate Cilium with Prometheus to scrape metrics for visibility and alerting.

You will learn how to trace individual connections, visualize service-to-service flows, and configure Prometheus to collect and store Cilium telemetry for dashboards and alerts.

> **lightbulb** Before you begin, ensure you have cluster-admin access, the Cilium CLI (optional but recommended), kubectl configured for the target cluster, and Prometheus (or a Prometheus-compatible scraper) available to ingest metrics.

## Why use Hubble + Prometheus?

* Hubble provides packet- and flow-level visibility into L7 and L3/L4 traffic that Cilium enforces.
* Prometheus collects long-term telemetry for dashboards, SLOs, and alerts.
* Together they let you both explore live network flows and monitor trends or anomalies over time.

| Component          | Purpose                                            | Example                                           |
| ------------------ | -------------------------------------------------- | ------------------------------------------------- |
| Hubble (CLI & UI)  | Real-time packet/flow inspection and tracing       | `hubble observe --since 1m`                       |
| Hubble Relay & UI  | Aggregates flow data and provides web UI           | `cilium hubble enable --relay --ui`               |
| Prometheus         | Scrapes and stores metrics for querying & alerting | Custom `scrape_configs` to collect Cilium metrics |
| Grafana (optional) | Visualize Cilium/Prometheus metrics                | Pre-built dashboards or custom panels             |

## Overview of the flow

1. Enable Hubble with Cilium so flows are captured on each node.
2. Use the Hubble CLI or UI to inspect flows and trace connections.
3. Expose the Cilium metrics endpoint and add a Prometheus scrape job to collect metrics.
4. Create alerts (for example, high packet drops, connection failures) and dashboards in Grafana.

***

## Enable Hubble (quick options)

You can enable Hubble at install time or enable it on an existing Cilium deployment.

Option A — Using the Cilium CLI (recommended when available):

* Install Cilium with Hubble enabled:

```bash theme={null}
cilium install \
  --set hubble.enabled=true \
  --set hubble.ui.enabled=true \
  --set hubble.relay.enabled=true
```

* Or enable Hubble on an existing installation:

```bash theme={null}
cilium hubble enable --relay --ui
```

Option B — Helm / YAML install

If you install via Helm or manifests, enable the equivalent values for `hubble.enabled`, `hubble.ui.enabled`, and `hubble.relay.enabled` in your values.yaml or manifests. Consult the Cilium docs for version-specific flags.

Verify Hubble status:

```bash theme={null}
cilium hubble status
```

> **warning** If you enable Hubble relay and UI on production clusters, ensure proper authentication and network access controls are in place (especially for the Hubble UI and relay ports) — these endpoints expose sensitive network telemetry.

***

## Using the Hubble CLI

Start a port-forward to access Hubble Relay (if you prefer not to open service externally):

* Port-forward the relay (replace namespace or service name if different):

```bash theme={null}
kubectl port-forward -n kube-system svc/hubble-relay 4245:4245
```

Common Hubble CLI commands:

* Observe recent flows (human-readable):

```bash theme={null}
hubble observe --since 5m
```

* Observe flows in JSON (for automation or parsing):

```bash theme={null}
hubble observe --since 1m -o json
```

* Trace a connection between two endpoints (by IP/service):

```bash theme={null}
hubble observe --from-pod <pod-name> --to-pod <pod-name> --since 1m
```

* Get Hubble status and connection health:

```text theme={null}
hubble status
```

Tip: Use `-o table` or `-o json` to control output format. Combine `--follow` to stream live flows.

***

## Using the Hubble UI

If you enabled `hubble.ui`, access it through the service or via the relay port-forward from above:

* Start a local port-forward to the UI:

```Expected Output:   theme={null}
bash
kubectl port-forward -n kube-system svc/hubble-ui 8081:80
```

Open your browser and visit:

* [http://localhost:8081](http://localhost:8081)

The UI displays flows, allows filtering by namespace, pod, port, L7 protocol, and shows trace paths across services.

***

## Metrics: Exposing Cilium Prometheus metrics

Cilium exposes Prometheus metrics describing agent health, endpoint stats, BPF programs, packet drops, and more. To collect these metrics you must configure your Prometheus server to scrape the correct targets.

Common places where metrics appear:

* `cilium-agent` pods (per-node metrics).
* A dedicated `cilium-metrics` service (if deployed).
* Relay or exporter endpoints if using a metrics exporter.

Example: verify a metrics endpoint directly:

```bash theme={null}
kubectl -n kube-system port-forward svc/cilium-metrics 9090:9090
curl http://localhost:9090/metrics | head
```

(Replace `cilium-metrics` with your service name; check your installation.)

### Example Prometheus scrape configuration

Below is a template `scrape_config` you can adapt. Update `role`, `namespace`, and service name patterns according to your cluster and Cilium installation.

```yaml theme={null}
scrape_configs:
  - job_name: 'cilium'
    kubernetes_sd_configs:
      - role: endpoints
    relabel_configs:
      # Keep only endpoints in the namespace where Cilium exposes metrics
      - source_labels: [__meta_kubernetes_namespace]
        action: keep
        regex: kube-system|cilium
      # Keep only Cilium-related services (adjust regex to match your service names)
      - source_labels: [__meta_kubernetes_service_name]
        action: keep
        regex: cilium-metrics|cilium-agent
    metrics_path: /metrics
    scheme: http
    # Optional: add basic_auth or bearer token config if your metrics endpoint is secured
```

If your environment uses static service discovery or other SD mechanisms, replace `kubernetes_sd_configs` accordingly.

***

## Useful Cilium metrics & alert ideas

| Metric name (example)                       | What it indicates               | Alert idea                                                                 |
| ------------------------------------------- | ------------------------------- | -------------------------------------------------------------------------- |
| `cilium_endpoint_regenerations_total`       | Endpoint policy/program changes | Alert if regeneration spikes for many endpoints                            |
| `cilium_drop_count_total`                   | Number of dropped packets       | Alert if drops exceed threshold per minute                                 |
| `cilium_policy_denied_count_total`          | Policy-denied connections       | Alert on sustained policy denies                                           |
| `hubble_grpc_connections` (Hubble-specific) | Active Hubble connections       | Alert if Hubble connection count drops to 0 (indicating connectivity loss) |

Example alert rule (conceptual):

```YAML theme={null}
- alert: CiliumHighPacketDrops
  expr: increase(cilium_drop_count_total[5m]) > 100
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High packet drops detected on Cilium"
    description: "More than 100 drops in the last 5 minutes. Check Cilium endpoints and BPF programs."
```

Adjust thresholds to your baseline.

***

## Inspecting flows for debugging

Workflow for a typical troubleshooting session:

1. Reproduce the problematic traffic (from a client pod to a server pod or service).
2. Use `hubble observe` with filters:
   * Filter by source/destination pod, namespace, port, L7 protocol.
   * Use `--since` and `--last` to scope the timeframe.
3. If you need a visual path, open the Hubble UI to follow flow graphs and traces.
4. Cross-reference Hubble flows with Prometheus metrics (drops, policy denies) to determine if a policy, BPF program, or network issue is causing failures.

Example Hubble observe with filters:

```bash theme={null}
hubble observe --from-namespaces default --to-ports 8080 --since 2m
```

***

## Troubleshooting tips

* If `hubble observe` shows no flows:
  * Ensure Hubble is enabled on Cilium and the relay is running.
  * Confirm that traffic actually traverses the datapath (e.g., check hostNetwork pods or egress rules).
* If Prometheus doesn't scrape Cilium metrics:
  * Verify service names and namespaces in `scrape_configs`.
  * Confirm the metrics endpoint responds (use `curl` via port-forward).
  * Check RBAC if Kubernetes SD is failing to discover endpoints.
* For high cardinality metrics, use relabeling to reduce label explosion before retention.

***

## Links and references

* [Cilium Documentation — Hubble](https://cilium.io/learning/hubble/)
* [Cilium GitHub / releases](https://github.com/cilium/cilium)
* [Prometheus Documentation — Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
* [Kubernetes Documentation — Service discovery in Prometheus](https://kubernetes.io/docs/tasks/debug-application-cluster/extend-prometheus/)

> **lightbulb** This guide provides a practical starting point for using Hubble with Prometheus. For cluster-specific details (service names, namespaces, authentication), consult your Cilium installation manifest or Helm values and the official Cilium docs.

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/b4c15752-3e42-43af-bedf-4a4c204ef5d8/lesson/381ba02d-c068-4aab-82c6-9030ffd29730)
