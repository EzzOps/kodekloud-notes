# Enter the config-reloader container of the Prometheus StatefulSet pod (adjust the pod name if different)
kubectl exec -it prometheus-0 -c config-reloader -- /bin/sh

# View the generated Prometheus config
cat /etc/prometheus/config_out/prometheus.env.yaml
```

Note: pod names, container names, and paths can vary by distribution — adjust `prometheus-0`, `config-reloader`, and the file path to match your deployment.

Example snippet from a generated Prometheus config:

```yaml theme={null}
global:
  scrape_interval: 30s
rule_files:
  - /etc/prometheus/rules/prometheus-0/*.yaml
scrape_configs:
  - job_name: serviceMonitor/monitoring/kube-apiserver/0
  - job_name: serviceMonitor/argocd/argocd-server-metrics/0
  - job_name: serviceMonitor/argocd/argocd-repo-server-metrics/0
  - job_name: serviceMonitor/argocd/argocd-metrics/0
  - job_name: serviceMonitor/argocd/argocd-applicationset-controller-metrics/0
```

This shows Prometheus scraping both Kubernetes components and ServiceMonitor-discovered jobs for ArgoCD.

### 2) The Service: how ArgoCD exposes metrics

ArgoCD deploys Services that expose metrics on a named port (commonly `metrics`). Confirm the Service exists and inspect it:

```bash theme={null}
kubectl get svc argocd-server-metrics -n argocd -o yaml
```

Representative Service manifest:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: argocd-server-metrics
  namespace: argocd
spec:
  ports:
    - name: metrics
      port: 8083
      protocol: TCP
      targetPort: 8083
  selector:
    app.kubernetes.io/name: argocd-server
  type: ClusterIP
```

Important:

* The Service must expose the metrics port with a name (e.g., `metrics`).
* The Service should have labels that a ServiceMonitor can match (see next section).
* Ensure the Service’s namespace is within the scope of the Prometheus CR's `namespaceSelector`.

### 3) ServiceMonitor: instruct the operator how to scrape

Create a ServiceMonitor that selects the Service by its labels and references the named metrics port. The Prometheus Operator recognizes ServiceMonitors and will include them if the Prometheus CR selects them.

Example ServiceMonitor (adjust namespace/labels to your setup):

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-server-metrics
  namespace: argocd
  labels:
    release: prometheus-operator
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: argocd-server
  endpoints:
    - port: metrics
      interval: 30s
```

Notes:

* `selector.matchLabels` selects the Service resource by its labels (not the Service's pod selector).
* `endpoints.port` should reference the named port (`metrics`) whenever possible.
* You can configure additional scrape settings inside `endpoints` (path, scheme, honor\_labels, relabeling, etc.).

### 4) Prometheus CR and automatic config reload

The Prometheus CR (managed by the operator) uses label selectors to discover ServiceMonitors. When a matching ServiceMonitor is found:

* The operator generates the appropriate `scrape_configs`.
* The operator writes those configurations into the Prometheus config volume.
* A config-reloader sidecar reloads Prometheus with the new configuration automatically.

Make sure the Prometheus CR’s `namespaceSelector` includes the namespace where the ServiceMonitor is created (common pitfall).

Verify the ServiceMonitor exists:

```bash theme={null}
kubectl get servicemonitor argocd-server-metrics -n argocd -o yaml
```

Re-check the generated Prometheus configuration (as in Step 1) to confirm `job_name` entries for your ServiceMonitors appear.

> **warning** If a ServiceMonitor is created before the Prometheus Operator and its CRDs are installed, the resource may be ignored or not processed. Always install the operator and CRDs first, then apply monitoring CRs.

### 5) Visualize ArgoCD metrics in Grafana

Once Prometheus is scraping ArgoCD metrics, point Grafana at your Prometheus data source and create dashboards or import community dashboards for ArgoCD. Useful metric types include:

* Application sync status and durations
* Application health and reconciliation counts
* Controller queue sizes and reconcile errors

Grafana sources:

* Use the Prometheus URL as the Grafana data source.
* Search for community dashboards (e.g., “ArgoCD”) to import panels and templates.

## Quick reference table

| Resource        | Purpose                                                           | Example/Command                                                                                          |
| --------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Service         | Exposes ArgoCD metrics via a named port                           | `kubectl get svc argocd-server-metrics -n argocd -o yaml`                                                |
| ServiceMonitor  | Instructs Prometheus Operator how to scrape a Service             | See ServiceMonitor manifest above                                                                        |
| Prometheus CR   | Operator-managed Prometheus instance that selects ServiceMonitors | Check Prometheus CR for `namespaceSelector` and label selectors                                          |
| Config reloader | Sidecar that reloads Prometheus when the config is updated        | `kubectl exec -it prometheus-0 -c config-reloader -- cat /etc/prometheus/config_out/prometheus.env.yaml` |

## Troubleshooting tips

* Confirm CRDs are installed: `kubectl get crd | grep servicemonitor` should show `servicemonitors.monitoring.coreos.com`.
* Check operator logs for errors: `kubectl logs -l app=prometheus-operator -n <operator-namespace>`
* Verify labels: `kubectl get svc argocd-server-metrics -n argocd --show-labels`
* Ensure Prometheus `namespaceSelector` includes the namespace where ServiceMonitor lives.

## Links and references

* Prometheus Operator: [https://prometheus-operator.dev/](https://prometheus-operator.dev/)
* ArgoCD (GitOps workshop reference): [https://learn.kodekloud.com/user/courses/bah-gitops-workshop](https://learn.kodekloud.com/user/courses/bah-gitops-workshop)
* Grafana: [https://grafana.com/](https://grafana.com/)

Wrapping up

* ArgoCD exposes metrics via Services with named ports and labels.
* The Prometheus Operator discovers those Services via ServiceMonitor (or PodMonitor) CRs and auto-generates Prometheus configs.
* Ensure correct labels, port names, and namespace selection so the operator picks up your monitoring resources.
* Use Grafana to build dashboards from the scraped ArgoCD metrics.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/241be712-9418-4199-94c1-73f07c0999af)


# Demo Helm

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Tooling/Demo-Helm/page

Explains using Helm charts with values.yaml and Argo CD to manage Kubernetes deployments via GitOps, enabling templated manifests, versioned configuration, and automated cluster reconciliation

[Helm](https://learn.kodekloud.com/user/courses/helm-for-beginners) is the de facto package manager for Kubernetes. Helm charts combine reusable templates and environment-specific `values.yaml` files to generate Kubernetes manifests (Deployments, Services, RBAC, HPAs, etc.), which makes deployments consistent and repeatable across environments.

<Frame>
  <img alt="The image shows a web interface for a Git repository hosted on a local server, displaying a directory structure of a project related to Helm charts with several YAML and TPL files listed." />
</Frame>

## Helm chart anatomy (quick reference)

| File / Directory |                                         Purpose | Example                     |
| ---------------- | ----------------------------------------------: | --------------------------- |
| `Chart.yaml`     |      Chart metadata (name, version, appVersion) | `Chart.yaml`                |
| `values.yaml`    |     Default configuration consumed by templates | `values.yaml`               |
| `templates/`     | Resource templates rendered with Helm functions | `templates/deployment.yaml` |
| `charts/`        |                   Subcharts (dependency charts) | `charts/`                   |

Templates are YAML manifests with Helm template expressions that evaluate at render time. For example, a Deployment template in `templates/deployment.yaml` may look like:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
  labels:
    app: highway-animation
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: highway-animation
  template:
    metadata:
      labels:
        app: highway-animation
    spec:
      containers:
        - name: highway-animation
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.containerPort }}
              protocol: TCP
          env:
            # You can render environment variables from .Values.env (list)
            # e.g., {{- toYaml .Values.env | nindent 12 }}
```

Note: Template expressions such as `{{ .Values.replicaCount }}` are shown inside code blocks to avoid MDX parsing issues.

A matching `values.yaml` supplies defaults consumed by the template. A minimal example for this chart:

```yaml theme={null}
replicaCount: 1

image:
  repository: siddharth67/highway-animation
  pullPolicy: IfNotPresent
  tag: "blue"

service:
  type: NodePort
  port: 3000
  targetPort: 3000

containerPort: 3000

env:
  - name: POD_COUNT
    value: "1"
