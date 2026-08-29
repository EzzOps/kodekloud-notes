# Adding Rules

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Adding-Rules/page

Using the Prometheus Operator PrometheusRule CRD to define, apply, and troubleshoot Prometheus alerting and recording rules in Kubernetes.

Previously we covered how to add new targets. Now we'll look at adding alerting and recording rules using the Prometheus Operator.

The Prometheus Operator exposes a Kubernetes CRD named `PrometheusRule`. You use this CRD to register Prometheus rule groups and rules in the same format as a normal Prometheus rules file. The structure is effectively identical to the standard Prometheus YAML but wrapped in a Kubernetes resource.

Example PrometheusRule

```yaml theme={null}
yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-rules
  labels:
    release: prometheus
spec:
  groups:
    - name: api
      rules:
        - alert: Down
          expr: up == 0
          for: 0m
          labels:
            severity: critical
          annotations:
            summary: Prometheus target missing {{ $labels.instance }}
```

Key points:

* `metadata.name` identifies the PrometheusRule object in Kubernetes.
* `metadata.labels` are used by the Prometheus instance to discover rules (see `ruleSelector` below).
* `spec.groups` contains one or more rule groups. Each group has a `name` and a `rules` list, matching regular Prometheus rule files.

Table — PrometheusRule core fields

| Field             | Purpose                                                          | Example                    |
| ----------------- | ---------------------------------------------------------------- | -------------------------- |
| `apiVersion`      | CRD API group/version                                            | `monitoring.coreos.com/v1` |
| `kind`            | Resource kind                                                    | `PrometheusRule`           |
| `metadata.name`   | Kubernetes resource name                                         | `api-rules`                |
| `metadata.labels` | Labels used for discovery (match with Prometheus `ruleSelector`) | `release: prometheus`      |
| `spec.groups`     | Rule groups (Prometheus format)                                  | see example above          |

Prometheus discovers PrometheusRule objects using the `ruleSelector` configured on the Prometheus resource. You can inspect this selector with `kubectl`:

```yaml theme={null}
yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
spec:
  ruleSelector:
    matchLabels:
      release: prometheus
```

<Callout icon="lightbulb">
  Make sure your `PrometheusRule` objects include the same label(s) that your Prometheus `ruleSelector` matches (for example, `release: prometheus`). Otherwise Prometheus will not pick up the rules.
</Callout>

Applying rules

1. Create a file (for example `rules.yaml`) containing your `PrometheusRule` resource as shown in the example above.
2. Apply it to the cluster:

```bash theme={null}
bash
kubectl apply -f rules.yaml
```

Successful output:

```bash theme={null}
prometheusrule.monitoring.coreos.com/api-rules created
```

Verify the resource exists:

```bash theme={null}
bash
kubectl get prometheusrule
```

Or describe it for more detail:

```bash theme={null}
bash
kubectl describe prometheusrule api-rules
```

Checking rules in Prometheus UI

* Open your Prometheus UI.
* Navigate to Status → Rules.
* You should see your rule group (for example, `api`) and the rules listed there. If the rule appears and is listed as healthy, it was successfully registered.

Troubleshooting quick commands

| Command                                  | Purpose                                            |
| ---------------------------------------- | -------------------------------------------------- |
| `kubectl get prometheuses -o yaml`       | View Prometheus resources and check `ruleSelector` |
| `kubectl get prometheusrule`             | Confirm rules exist in the cluster                 |
| `kubectl describe prometheusrule <name>` | Inspect a specific PrometheusRule                  |
| `kubectl logs <prometheus-pod>`          | Check Prometheus logs for rule loading errors      |

<Callout icon="warning">
  If Prometheus does not register your rules, first check label matching between the `Prometheus` `ruleSelector` and your `PrometheusRule` `metadata.labels`. Labels must match exactly. Also review Prometheus logs for parsing or evaluation errors.
</Callout>

Examples of additional rules

Below are a couple of additional rule snippets that illustrate typical alerting rules. Place them inside the `spec.groups[].rules` list of a `PrometheusRule` object.

Example: Alertmanager reload failure

```yaml theme={null}
yaml
- alert: AlertmanagerFailedReload
  expr: max_over_time(alertmanager_config_last_reload_successful{job="prometheus-kube-prometheus-alertmanager",namespace="default"}[5m]) == 0
  for: 10m
  labels:
    severity: critical
  annotations:
    description: Configuration has failed to load for {{ $labels.namespace }} / {{ $labels.pod }}.
    runbook_url: https://runbooks.prometheus-operator.[SECRET_REDACTED]
    summary: Reloading an Alertmanager configuration has failed.
```

Example: Alertmanager cluster members inconsistent

```yaml theme={null}
yaml
- alert: AlertmanagerMembersInconsistent
  expr: max_over_time(alertmanager_cluster_members{job="prometheus-kube-prometheus-alertmanager",namespace="default"}[5m]) < on (namespace, service) group_left () count by (namespace, service) (max_over_time(alertmanager_cluster_members{job="prometheus-kube-prometheus-alertmanager",namespace="default"}[5m]))
  for: 15m
  labels: {}
  annotations:
    summary: Alertmanager cluster membership is inconsistent.
```

References

* Prometheus Operator (GitHub): [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
* Prometheus rules documentation: [https://prometheus.[AWS_SECRET_ACCESS_KEY]alerting\_rules/](https://prometheus.[AWS_SECRET_ACCESS_KEY]alerting_rules/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/fa87266e-e72e-4431-b165-c99a30ec1a33" />
</CardGroup>
