# PrometheusRule group for Argo CD
- name: ArgoCD Rules
  rules:
    - alert: ArgoApplicationOutOfSync
      expr: argocd_app_info{sync_status="OutOfSync"} == 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "'{{ $labels.name }}' Application has synchronization issue"
```

### What each field means

| Field         | Purpose                                                      | Example / Notes                                                |
| ------------- | ------------------------------------------------------------ | -------------------------------------------------------------- |
| `name`        | Group name that organizes related alerts                     | `ArgoCD Rules`                                                 |
| `alert`       | Unique alert identifier shown in Alertmanager and dashboards | `ArgoApplicationOutOfSync`                                     |
| `expr`        | PromQL expression that evaluates the condition               | `argocd_app_info{sync_status="OutOfSync"} == 1`                |
| `for`         | Minimum duration the condition must hold before firing       | `5m` to avoid transient noise                                  |
| `labels`      | Metadata for alert routing and severity                      | `severity: warning` (use `critical` for high priority)         |
| `annotations` | Human-readable descriptions inserted into notifications      | `summary` using `{{ $labels.name }}` to reference the app name |

## Where to add this rule

Add the group into an existing `PrometheusRule` resource managed by the Prometheus Operator (namespace often `monitoring`). Example commands to inspect and edit the PrometheusRule:

```bash theme={null}
kubectl -n monitoring get prometheusrules.monitoring.coreos.com kode-kloud-prometheus-stac-alertmanager.rules -o yaml
kubectl -n monitoring edit prometheusrules.monitoring.coreos.com kode-kloud-prometheus-stac-alertmanager.rules
```

Insert the `ArgoCD Rules` group inside the `spec.groups` array. Example fragment showing the ArgoCD group placed at the top of `spec.groups`:

```yaml theme={null}
spec:
  groups:
  - name: ArgoCD Rules
    rules:
    - alert: ArgoApplicationOutOfSync
      expr: argocd_app_info{sync_status="OutOfSync"} == 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "'{{ $labels.name }}' Application has synchronization issue"
  # ... other groups and rules follow ...
```

After saving, the Prometheus Operator will reconcile the `PrometheusRule`; Prometheus will reload rules automatically, which can take a short moment.

## Test the alert by causing drift

To test the rule, make an Argo CD application go OutOfSync. A simple approach is to modify the live cluster resource so it no longer matches the Git desired state.

Open the Argo CD application UI and select an application to test. You can also directly edit a Deployment to introduce drift.

<Frame>
  <img alt="The image displays the Argo CD application's dashboard, showing the synchronization status and health of the &#x22;highway-animation&#x22; application with its deployment and replica sets visualized." />
</Frame>

Example: edit the live Deployment to change replicas or a container env value:

```bash theme={null}
kubectl -n highway-animation edit deployment highway-animation
```

Example deployment fragment (this was edited live to create drift):

```yaml theme={null}
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:blue
          env:
            - name: POD_COUNT
              value: "8"
          ports:
            - containerPort: 3000
              protocol: TCP
```

Once the application reports `OutOfSync` and the rule evaluates true for `for: 5m`, the alert will fire in Alertmanager. While waiting, Alertmanager may display other currently active alerts.

<Frame>
  <img alt="The image shows a web interface listing alerts for various Kubernetes jobs such as &#x22;kube-controller-manager,&#x22; &#x22;kube-etcd,&#x22; and others, with options to expand groups and silence alerts." />
</Frame>

## Viewing the fired alert

After the `for` window elapses and the alert fires, Alertmanager will show the new alert. The alert details include labels such as `job="argocd-metrics"`, `namespace`, the application name, repository URL, and the `severity` label.

<Frame>
  <img alt="The image shows an Alertmanager interface displaying an alert related to &#x22;argocd-metrics,&#x22; with details like severity, sync status, and other metadata tags." />
</Frame>

## Forwarding alerts (Slack example)

Once the alert appears in Alertmanager you can route it to external receivers (Slack, PagerDuty, email, etc.) by configuring Alertmanager receivers and routes.

> **lightbulb** Ensure the `argocd_app_info` metric is being scraped by Prometheus. Argo CD exposes metrics via the argocd-metrics endpoint; if Prometheus isn't scraping `argocd-metrics`, the rule cannot evaluate true.

Example Alertmanager Slack configuration (in Alertmanager YAML):

```yaml theme={null}
global:
  resolve_timeout: 1m
  slack_api_url: 'https://hooks.slack.com/services/TSUJ1MIHQ/BT7J5TR5/5eZMpDbKk8wk2'
route:
  receiver: 'slack-notifications'
receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#monitoring-instances'
        send_resolved: true
```

Example Slack message template for Alertmanager (use in templates files):

```yaml theme={null}
{{- /* Example Slack message template for Alertmanager */ -}}
text: >
{{ range .Alerts -}}
*Alert:* {{ .Annotations.title }}{{ if .Labels.severity }} - `{{ .Labels.severity }}`{{ end }}

*Description:* {{ .Annotations.description }}

*Details:*
{{ range .Labels.SortedPairs -}}
* {{ .Name }}: `{{ .Value }}`
{{ end }}
{{ end }}
```

<Frame>
  <img alt="The image is a screenshot from a Grafana Labs blog on setting up Slack alerts using Prometheus. It shows steps in Slack to manage apps and search for Incoming WebHooks, alongside a sidebar listing blog contents and a prompt to create a Grafana Cloud account." />
</Frame>

## Notes and next steps

* After confirming the alert works, refine labels and routing in your Alertmanager configuration to match your on-call and escalation workflows.
* Use `severity` labels to differentiate notification channels (e.g., `warning` -> pager muted, `critical` -> paged).
* Integrate Grafana or other visualization tools to display Argo CD metrics and alert status.

Useful references:

* [Prometheus Operator documentation](https://github.com/prometheus-operator/prometheus-operator)
* [Argo CD metrics & monitoring](https://argo-cd.readthedocs.io/en/stable/operator-manual/metrics/)
* [Alertmanager configuration guide](https://prometheus.io/docs/alerting/latest/alertmanager/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Grafana Slack notifications: [https://grafana.com/docs/grafana/latest/alerting/notifications/notification-channels/slack/](https://grafana.com/docs/grafana/latest/alerting/notifications/notification-channels/slack/)

That’s how you create an alert for Argo CD application drift, see it in Alertmanager, and route notifications to external systems like Slack.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/8a7954bf-9255-4fd0-bd62-ce42c48a0012)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/34cc2558-9ccc-46cd-b446-e597de03f41b)


# Interoperability with Notifications Observability and Continuous Integration Tools

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Tooling/Interoperability-with-Notifications-Observability-and-Continuous-Integration-Tools/page

Explains how GitOps interoperates with CI, observability, and notification tools to build a resilient delivery pipeline and improve performance using DORA metrics.

This guide explains how GitOps integrates with continuous integration (CI), observability, and notification systems to form a complete cloud-native delivery pipeline. You’ll also get a concise overview of the DORA metrics that measure delivery performance and reliability.

While GitOps makes Git the single source of truth for desired state, it is most powerful when it interoperates with CI systems that build and test artifacts, and with observability/notification tools that provide runtime feedback and automated responses.

## DORA metrics: key indicators of delivery performance

DORA metrics are industry-standard benchmarks that help teams measure how effectively they deliver and operate software. GitOps naturally encourages practices that improve these metrics.

<Frame>
  <img alt="The image outlines DORA metrics for software delivery performance, including deployment frequency, lead time for changes, change failure rate, and time to restore service." />
</Frame>

| DORA Metric             | What it measures                                         | Why it matters                                                        |
| ----------------------- | -------------------------------------------------------- | --------------------------------------------------------------------- |
| Deployment frequency    | How often new versions are released                      | Higher frequency indicates faster delivery and smaller, safer changes |
| Lead time for changes   | Time from commit to production                           | Shorter lead times increase responsiveness and reduce feedback delay  |
| Change failure rate     | % of deployments causing a failure requiring remediation | Lower rates imply more reliable releases                              |
| Time to restore service | Time to recover after an incident                        | Faster recovery reduces user impact and increases reliability         |

> **lightbulb** DORA metrics are complementary to GitOps: declarative manifests, version control, and automated reconciliation help improve deployment frequency and reduce lead time and failure rates.

## Continuous Integration (CI) and GitOps

A CI system automates building, testing, and packaging code changes. In a GitOps workflow, CI produces immutable artifacts (for example, container images) and updates the declarative manifests in Git that describe how the application should run.

<Frame>
  <img alt="The image is a diagram illustrating continuous integration with Jenkins, showing a workflow that includes automating CI/CD for building, unit testing, linting, dockerizing, security, deployment, and tests." />
</Frame>

Jenkins is a widely used automation server that can orchestrate the pipeline—from unit tests and linting to Docker image builds and security scans—before updating Git with the new desired state.

<Frame>
  <img alt="The image is a diagram showing the benefits of Continuous Integration with Jenkins (CI), highlighting code problem detection, accelerated development, and improved software quality." />
</Frame>

Key roles for CI in GitOps:

* Build and test artifacts (binaries, container images).
* Push immutable artifacts to a registry.
* Update Kubernetes manifests or Helm charts in the GitOps repository with the new image tags or config.

## How GitOps connects CI and the runtime

In a typical GitOps flow, a GitOps operator (e.g., ArgoCD or Flux) continuously compares the Git repository’s desired state to the actual cluster state and reconciles differences.

<Frame>
  <img alt="The image is a flowchart depicting the CI/CD process with GitOps, showing interactions between an application code repository, Kubernetes manifests repository, and a production cluster managed by ArgoCD. It illustrates the steps of continuous integration, version control, and deployment automation." />
</Frame>

Example end-to-end sequence:

1. Developer merges code to the application repository.
2. CI pipeline runs tests, builds an image, and pushes it to a container registry.
3. CI updates the Kubernetes manifest repository (e.g., updates image tag).
4. GitOps operator detects the change in the manifests repo and applies it to the cluster.
5. Operator monitors application health and reports discrepancies.

<Frame>
  <img alt="The image illustrates a CI/CD workflow using GitOps, detailing processes like application code management, continuous integration, and deployment through Kubernetes and ArgoCD. It shows how code is tested, built, and synchronized with production clusters." />
</Frame>

Rollback is straightforward because the desired state is versioned in Git. Reverting a commit or using the GitOps operator’s rollback feature returns the cluster to the previous good state.

> **warning** Automatic rollbacks can speed recovery but must be used with care. Ensure health checks and observability thresholds are well-defined to avoid oscillations or cascading rollbacks.

## Observability and notifications: closing the feedback loop

Observability tools collect runtime metrics and logs that inform the GitOps workflow about the health of deployments. Prometheus and Grafana are common choices for metrics and visualization, and Alertmanager handles routing and delivering alerts.

<Frame>
  <img alt="The image illustrates the process of observability and notification using Prometheus, Grafana, AlertManager, and Slack, with Git and Kubernetes integrated into the workflow for deploying and gathering feedback." />
</Frame>

Typical observability workflow:

* Prometheus scrapes metrics from pods and infrastructure.
* Alertmanager receives alerts based on Prometheus rules.
* Alertmanager routes notifications to channels such as Slack, email, or webhooks.
* On a detected regression, the team is notified and may revert the Git manifest or trigger automated remediation.

<Frame>
  <img alt="The image is an infographic titled &#x22;Observability and Notification: Prometheus, AlertManager, and Slack,&#x22; highlighting benefits such as validating successful deployments, providing operational insights, and enabling rapid incident response." />
</Frame>

An example scenario:

* GitOps operator deploys a new version.
* Prometheus detects increased error rate or latency above thresholds.
* Alertmanager sends a Slack alert to the on-call channel.
* The team reverts the manifest in Git (or relies on an automated rollback), and the GitOps operator restores the previous state.

Benefits of integrating observability and notifications with GitOps:

* Validate deployments automatically.
* Gain operational insight into production behavior.
* Enable faster incident detection and response, improving DORA metrics like time to restore service.

## References and further reading

* Jenkins (CI): [https://learn.kodekloud.com/user/courses/jenkins](https://learn.kodekloud.com/user/courses/jenkins)
* ArgoCD (GitOps operator): [https://learn.kodekloud.com/user/courses/gitops-with-argocd](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* FluxCD (GitOps operator): [https://learn.kodekloud.com/user/courses/gitops-with-fluxcd](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)
* Prometheus & Grafana (Monitoring): [https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana)

This overview ties together CI, GitOps, and observability to form a resilient delivery pipeline that supports rapid, safe deployments and clear feedback loops for continuous improvement.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/6974e6f3-41ee-4563-af84-5a5ef529029d)
