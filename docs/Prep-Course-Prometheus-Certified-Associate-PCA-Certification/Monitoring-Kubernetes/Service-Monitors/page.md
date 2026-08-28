# Service Monitors

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Service-Monitors/page

Explains using ServiceMonitor CRD with Prometheus Operator to declaratively configure Kubernetes scrape targets, selectors, and resulting Prometheus scrape configs and relabeling.

In this lesson we’ll learn how to add scrape targets to Prometheus by using the ServiceMonitor custom resource provided by the Prometheus Operator. ServiceMonitors let you declare Prometheus scrape configuration in Kubernetes objects instead of editing Prometheus config files directly.

The Prometheus Operator installs several Custom Resource Definitions (CRDs) that provide higher-level abstractions for deploying and configuring Prometheus components (Prometheus instances, Alertmanagers, ServiceMonitors, PodMonitors, etc.).

<Frame>
  <img alt="The image contains text explaining that the Prometheus operator includes several custom resource definitions that provide high-level abstraction for deploying and configuring Prometheus." />
</Frame>

List the installed CRDs:

```bash theme={null}
kubectl get crd
```

Example truncated output:

```text theme={null}
NAME                                           CREATED AT
alertmanagerconfigs.monitoring.coreos.com      2022-11-18T01:18:55Z
alertmanagers.monitoring.coreos.com            2022-11-18T01:18:55Z
podmonitors.monitoring.coreos.com              2022-11-18T01:18:56Z
prometheuses.monitoring.coreos.com             2022-11-18T01:18:56Z
prometheusrules.monitoring.coreos.com          2022-11-18T01:18:56Z
servicemonitors.monitoring.coreos.com          2022-11-18T01:18:57Z
thanosrulers.monitoring.coreos.com             2022-11-18T01:18:57Z
```

Key CRDs and their use cases:

| Resource Type  | Use Case                             | Example                                 |
| -------------- | ------------------------------------ | --------------------------------------- |
| Alertmanager   | Manage Alertmanager instances        | `alertmanagers.monitoring.coreos.com`   |
| Prometheus     | Manage Prometheus instances          | `prometheuses.monitoring.coreos.com`    |
| ServiceMonitor | Declare service-level scrape targets | `servicemonitors.monitoring.coreos.com` |
| PodMonitor     | Declare pod-level scrape targets     | `podmonitors.monitoring.coreos.com`     |
| PrometheusRule | Define alerting and recording rules  | `prometheusrules.monitoring.coreos.com` |

What is a ServiceMonitor?

* A ServiceMonitor is a CRD that defines a set of targets for Prometheus to monitor and scrape.
* It expresses scrape configuration (endpoints, path, interval, job label) in Kubernetes objects so you don’t edit Prometheus config files directly.
* The Prometheus Operator translates ServiceMonitor resources into Prometheus `scrape_configs`.

<Frame>
  <img alt="The image explains that service monitors define targets for Prometheus and provide a declarative Kubernetes syntax to avoid direct configuration changes." />
</Frame>

Example flow

1. Deploy your application (Deployment + Service).
2. Create a ServiceMonitor that selects the Service (via labels) and specifies endpoints (port, path, interval).
3. The Prometheus Operator discovers the ServiceMonitor and adds targets to Prometheus’ scrape configuration.

Example manifests

* Service exposes the application on port 3000 with port name `web` and labels `job: node-api` and `app: api`.
* ServiceMonitor selects the Service by `matchLabels`, sets `jobLabel: job` (so the Prometheus job name is taken from the Service `job` label), and configures endpoints (scrape interval and metrics path).

Service manifest (api-service.yaml):

```yaml theme={null}
