# Example job for a Kubernetes service (adapt service name/port labels to your cluster)
- job_name: api-service
  kubernetes_sd_configs:
  - role: endpoints
  relabel_configs:
  - source_labels: [__meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
    action: keep
    regex: 'api-service;http'
```

Notes about the example:

* The `kubernetes_sd_configs` and `relabel_configs` entries follow Prometheus server configuration syntax.
* You must ensure the configuration is valid YAML and valid Prometheus config; the chart will not validate it for you.
* Replace the service/port names and relabel rules to match how your application is exposed in Kubernetes.

3. Apply the updated values by upgrading the Helm release:

```bash theme={null}
helm upgrade prometheus prometheus-community/kube-prometheus-stack -f values.yaml
```

After the upgrade completes, Prometheus should reload with the appended scrape jobs and begin scraping the newly added targets.

> **lightbulb** ServiceMonitors provide a declarative, Operator-native way to add targets to Prometheus and are generally the recommended approach.

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/c0644cd7-27af-4637-853b-61f7cb946ca8)


# Alertmanager Rules

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Alertmanager-Rules/page

Guide for creating AlertmanagerConfig CRDs, configuring Helm selectors so Alertmanager discovers them, converting alertmanager.yml to CRD syntax, applying examples and troubleshooting

The Prometheus Operator exposes an AlertmanagerConfig CRD to register Alertmanager routes and receivers from Kubernetes. This guide shows how to create AlertmanagerConfig objects, ensure Alertmanager discovers them, and how to configure the Helm chart so the Alertmanager picks them up.

> **lightbulb** AlertmanagerConfig objects defined in Kubernetes follow the Prometheus Operator CRD schema and are mapped to Alertmanager configuration. They are not automatically discovered unless Alertmanager's `alertmanagerConfigSelector` (and optionally `alertmanagerConfigNamespaceSelector`) are configured to match your labels.

## Basic AlertmanagerConfig example

This is a minimal AlertmanagerConfig CRD that routes grouped alerts to a webhook receiver:

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1alpha1
kind: AlertmanagerConfig
metadata:
  name: alert-config
  labels:
    resource: prometheus
spec:
  route:
    groupBy: ["severity"]
    groupWait: 30s
    groupInterval: 5m
    repeatInterval: 12h
    receiver: "webhook"
  receivers:
    - name: "webhook"
      webhookConfigs:
        - url: "http://example.com/"
```

Key parts:

* `metadata.labels` — used to match this object to Alertmanager instances (via `alertmanagerConfigSelector`).
* `spec.route` — route behavior (grouping and timing).
* `spec.receivers` — one or more receivers (here: webhook).

## Why Alertmanager might not pick up your AlertmanagerConfig

When installed via the kube-prometheus-stack Helm chart, the Alertmanager StatefulSet/Deployment includes two fields in its spec:

```yaml theme={null}
spec:
  alertmanagerConfigNamespaceSelector: {}
  alertmanagerConfigSelector: {}
```

By default these are empty, meaning Alertmanager will not match any AlertmanagerConfig objects. You must set `alertmanagerConfigSelector` (and optionally `alertmanagerConfigNamespaceSelector`) in the chart values so Alertmanager can discover AlertmanagerConfig objects by label.

> **warning** If you do not configure a selector in the Helm chart values, Alertmanager will ignore AlertmanagerConfig objects even if they exist in the cluster.

## Important syntax differences: alertmanager.yml vs AlertmanagerConfig CRD

When converting an `alertmanager.yml` (standalone Alertmanager config) to an `AlertmanagerConfig` CRD, note two common differences:

* Property naming: standalone `alertmanager.yml` uses snake\_case (e.g., `group_wait`), while the CRD uses camelCase (e.g., `groupWait`).
* Label matchers: in `alertmanager.yml` you can write `job: kubernetes`. In the CRD matchers must be objects with `name` and `value`.

Comparison:

| Feature         | alertmanager.yml (standalone)                   | AlertmanagerConfig CRD                                                 |
| --------------- | ----------------------------------------------- | ---------------------------------------------------------------------- |
| Grouping/timing | `group_wait: 30s`                               | `groupWait: 30s`                                                       |
| Group by        | `group_by: ['severity']`                        | `groupBy: ["severity"]`                                                |
| Matcher example | `routes:\n  - matchers:\n      job: kubernetes` | `routes:\n  - matchers:\n      - name: job\n        value: kubernetes` |

Example pair:

alertmanager.yml

```yaml theme={null}
route:
  receiver: staff
  group_by: ['severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 12h
routes:
  - matchers:
      job: kubernetes
    receiver: infra
    group_by: ['severity']
```

AlertmanagerConfig CRD (equivalent)

```yaml theme={null}
spec:
  route:
    groupBy: ["alertname"]
    groupWait: 30s
    groupInterval: 5m
    repeatInterval: 12h
    receiver: "webhook"
  routes:
    - matchers:
        - name: job
          value: kubernetes
      receiver: "infra"
      groupBy: ["severity"]
```

## Configure the Helm chart so Alertmanager finds AlertmanagerConfig objects

1. Retrieve the default values for the kube-prometheus-stack chart:

```bash theme={null}
helm show values prometheus-community/kube-prometheus-stack > values.yaml
```

2. Edit `values.yaml` and set `alertmanagerConfigSelector` to match the labels you will use on AlertmanagerConfig objects. For example, to match `resource: prometheus`:

```yaml theme={null}
alertmanagerConfigSelector:
  matchLabels:
    resource: prometheus
```

You can choose any label key/value pair; just use the same one on your AlertmanagerConfig objects.

3. Upgrade the Helm release using the modified values file:

```bash theme={null}
helm upgrade prometheus prometheus-community/kube-prometheus-stack -f values.yaml
```

After the upgrade, the Alertmanager resource in the cluster should include the selector configuration:

```yaml theme={null}
spec:
  alertmanagerConfigNamespaceSelector: {}
  alertmanagerConfigSelector:
    matchLabels:
      resource: prometheus
```

## Create and apply an AlertmanagerConfig

Create a file `alert.yaml` with the same example CRD (note `metadata.labels` matches the Helm selector):

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1alpha1
kind: AlertmanagerConfig
metadata:
  name: alert-config
  labels:
    resource: prometheus
spec:
  route:
    groupBy: ["severity"]
    groupWait: 30s
    groupInterval: 5m
    repeatInterval: 12h
    receiver: "webhook"
  receivers:
    - name: "webhook"
      webhookConfigs:
        - url: "http://example.com/"
```

Apply it:

```bash theme={null}
kubectl apply -f alert.yaml
