# 1. Create a GitRepository source for the Flux 2 manifests
flux create source git monitoring-source-prometheus-stack \
  --url https://github.com/fluxcd/flux2 \
  --branch main \
  --interval 30m \
  --export > monitoring-source-prometheus-stack.yaml

# 2. Create a Kustomization to apply the monitoring directory
flux create kustomization monitoring-kustomization-prometheus-stack \
  --source GitRepository/monitoring-source-prometheus-stack \
  --path "./manifests/monitoring/kube-prometheus-stack" \
  --interval 1h \
  --prune \
  --export > monitoring-kustomization-prometheus-stack.yaml

# Commit and push to your Git repository
git add .
git commit -m "Add Kube Prometheus Stack monitoring with Flux 2"
git push
```

<Callout icon="triangle-alert">
  Make sure the `monitoring` namespace does not already exist or is managed by another tool, as Flux will create it.
</Callout>

| Resource       | Purpose                                           | Flux CLI Example                                               |
| -------------- | ------------------------------------------------- | -------------------------------------------------------------- |
| GitRepository  | Point Flux at a Git repo for manifests            | `flux create source git ...`                                   |
| Kustomization  | Apply resources from a source directory           | `flux create kustomization ...`                                |
| HelmRepository | Download Helm charts from an OCI or HTTP endpoint | Defined in `monitoring/kube-prometheus-stack/helmrepo.yaml`    |
| HelmRelease    | Install and manage a Helm chart                   | Defined in `monitoring/kube-prometheus-stack/helmrelease.yaml` |

## 3. Verify Deployment

After Flux syncs, confirm that the `monitoring` namespace and its resources are created:

```bash theme={null}
kubectl get ns
# ...
monitoring    Active   30s

kubectl get all -n monitoring
# Should list Deployments, StatefulSets, DaemonSets and Services for Prometheus and Grafana
```

## 4. Expose Prometheus and Grafana

By default, both Prometheus and Grafana services use `ClusterIP`. To access them externally, switch to `NodePort`:

```bash theme={null}
kubectl -n monitoring edit svc kube-prometheus-stack-prometheus
kubectl -n monitoring edit svc kube-prometheus-stack-grafana
kubectl -n monitoring get svc
```

Example output:

```bash theme={null}
NAME                             TYPE       CLUSTER-IP      PORT(S)             AGE
kube-prometheus-stack-grafana    NodePort   10.99.232.155   80:31921/TCP        5m
kube-prometheus-stack-prometheus NodePort   10.97.179.234   9090:30753/TCP      5m
# ...
```

## 5. Access the Prometheus UI

Open the Prometheus interface in your browser at `http://<node-ip>:30753`. The dashboard displays service monitor health:

<Frame>
  ![The image shows a Prometheus monitoring dashboard displaying the status of various service monitors, with some endpoints marked as "UP" and one as "DOWN," indicating their health status.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877657/notes-assets/images/GitOps-with-FluxCD-DEMO-Install-Kube-Prometheus-Stack/prometheus-monitoring-dashboard-status.jpg)
</Frame>

## 6. Access the Grafana Dashboard

Visit `http://<node-ip>:31921` and log in with credentials stored in the `kube-prometheus-stack-grafana` secret:

```bash theme={null}
kubectl -n monitoring get secret kube-prometheus-stack-grafana -o yaml
```

Decode the base64 values:

```bash theme={null}
echo <base64-admin-user>          # YWRtaW4= -> admin
echo <base64-admin-password>      # cHJvbS1hZG1pbi1vcGVyYXRvcg== -> prom-admin-operator
```

Initially, no Flux-specific dashboards are available:

<Frame>
  ![The image shows the Grafana dashboard interface, featuring options for creating new dashboards and adding data sources, along with a blog update section.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877659/notes-assets/images/GitOps-with-FluxCD-DEMO-Install-Kube-Prometheus-Stack/grafana-dashboard-interface-options.jpg)
</Frame>

However, you can browse the built-in Kubernetes monitoring dashboards:

<Frame>
  ![The image shows a Grafana dashboard interface with a list of various monitoring dashboards related to Kubernetes and other services. The interface includes options for browsing, filtering, and sorting the dashboards.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877660/notes-assets/images/GitOps-with-FluxCD-DEMO-Install-Kube-Prometheus-Stack/grafana-dashboard-kubernetes-monitoring.jpg)
</Frame>

## 7. Explore Prometheus Targets

Check the Prometheus `/targets` page to see which endpoints are scraped:

<Frame>
  ![The image shows a Prometheus monitoring dashboard displaying a list of service targets, with some services marked as unhealthy in red and others as healthy in blue.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877661/notes-assets/images/GitOps-with-FluxCD-DEMO-Install-Kube-Prometheus-Stack/prometheus-monitoring-dashboard-service-targets.jpg)
</Frame>

## Next Steps

* Configure `ServiceMonitor` resources to scrape Flux controllers.
* Deploy custom Grafana dashboards for Flux metrics.
* Integrate alerts into your incident management workflow.

## References

* [Flux GitRepository Source Documentation](https://fluxcd.io/docs/components/source/gitrepository/)
* [Flux Kustomization Documentation](https://fluxcd.io[AWS_SECRET_ACCESS_KEY]/)
* [Prometheus Community Helm Charts](https://prometheus-community.github.io/helm-charts)
* [Kube Prometheus Stack on Artifact Hub](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/fb9e59dc-9dee-4532-92a8-553d0df1df27/lesson/8402737e-1205-4320-8bf5-453600a08706" />
</CardGroup>


# DEMO Monitor Flux using Prometheus Grafana

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Monitoring-User-Interface/DEMO-Monitor-Flux-using-Prometheus-Grafana/page

This guide explains how to integrate Prometheus with Flux v2 for monitoring and visualizing metrics in Grafana.

In this guide, you’ll learn how to integrate [Prometheus](https://prometheus.io/) with Flux v2 to scrape controller metrics and visualize them in [Grafana](https://grafana.com/). We’ll leverage the `monitoring` folder from the [fluxcd/flux2 GitHub repo](https://github.com/fluxcd/flux2) and deploy a `PodMonitor` CRD and Grafana dashboards via Flux Kustomizations.

## 1. Explore the monitoring directory

Clone or browse the Flux repository and locate the `monitoring` folder:

<Frame>
  ![The image shows a GitHub repository page for "fluxcd/flux2" with a focus on the "monitoring" directory, containing folders like "kube-prometheus-stack" and "loki-stack."](../../../../images/kodekloud.com/kk-media/image/upload/v1752877662/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/github-repo-fluxcd-flux2-monitoring.jpg)
</Frame>

Inside `monitoring/` you’ll find:

* **PodMonitor** YAML for scraping all Flux controllers.
* A `dashboards/` folder with two Grafana JSON files:
  * `cluster.json`
  * `controlplane.json`

<Frame>
  ![The image shows a GitHub repository page for "fluxcd/flux2" with a focus on the "dashboards" directory, displaying JSON files related to monitoring configurations.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877663/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/github-repo-fluxcd-flux2-dashboards-json.jpg)
</Frame>

## 2. Apply the Flux PodMonitor

The `PodMonitor` CRD instructs Prometheus to scrape metrics from Flux controllers in the `flux-system` namespace:

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: flux-system
  namespace: flux-system
  labels:
    app.kubernetes.io/part-of: flux
    app.kubernetes.io/component: monitoring
spec:
  namespaceSelector:
    matchNames:
      - flux-system
  selector:
    matchExpressions:
      - key: app
        operator: In
        values:
          - helm-controller
          - source-controller
          - kustomize-controller
          - notification-controller
          - image-automation-controller
          - image-reflector-controller
  podMetricsEndpoints:
    - port: http-prom
      relabelings: []
```

<Callout icon="lightbulb">
  Ensure the Prometheus Operator and its CRDs (including `PodMonitor`) are installed (for example via the `kube-prometheus-stack`).
</Callout>

Apply it directly or via Flux:

```bash theme={null}
kubectl apply -f monitoring/manifests/monitoring-config/podmonitor.yaml
```

## 3. Create a Flux Kustomization

Automate the deployment by defining a Flux `Kustomization` that points to your Git source:

```yaml theme={null}
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: monitoring-config
  namespace: flux-system
spec:
  dependsOn:
    - name: monitoring-kustomization-prometheus-stack
  interval: 1h0m0s
  path: ./manifests/monitoring/monitoring-config
  prune: true
  sourceRef:
    kind: GitRepository
    name: monitoring-source-prometheus-stack
```

You can export this with the Flux CLI:

```bash theme={null}
flux create kustomization monitoring-config \
  --namespace flux-system \
  --depends-on monitoring-kustomization-prometheus-stack \
  --interval 1h0m0s \
  --path "./manifests/monitoring/monitoring-config" \
  --prune=true \
  --source GitRepository/monitoring-source-prometheus-stack \
  --export > monitoring-config.yaml
```

Commit and push:

```bash theme={null}
git add manifests/monitoring/monitoring-config
git commit -m "Add Flux PodMonitor and Grafana dashboards"
git push
```

Reconcile the Git source and kustomization:

```bash theme={null}
flux reconcile source git flux-system --namespace flux-system
flux reconcile kustomization monitoring-config --namespace flux-system
```

Verify the PodMonitor is ready:

```bash theme={null}
kubectl get podmonitor -n flux-system
```

## 4. Validate in Prometheus

Open your Prometheus UI and go to **Status → Targets**. Within seconds, the Flux controller endpoints should appear as `UP`:

<Frame>
  ![The image shows a Prometheus monitoring dashboard displaying the status of various targets, with endpoints, states, labels, and scrape durations. All listed targets are marked as "UP," indicating they are functioning properly.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877665/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/prometheus-monitoring-dashboard-targets-status.jpg)
</Frame>

### Common `gotk_` Queries

| Query                                                    | Description                                 |
| -------------------------------------------------------- | ------------------------------------------- |
| `gotk_reconcile_condition{type="Ready", status="True"}`  | Count of successful reconciliations         |
| `gotk_reconcile_condition{type="Ready", status="False"}` | Count of failed reconciliations             |
| `gotk_suspend_status`                                    | Suspension state of Git sources/controllers |
| `gotk_reconcile_duration_seconds_bucket`                 | Histogram buckets for reconcile durations   |
| `gotk_reconcile_duration_seconds_sum`                    | Total reconcile duration                    |
| `gotk_reconcile_duration_seconds_count`                  | Number of reconcile operations              |

Run any query in **Graph** view to see real-time metrics:

<Frame>
  ![The image shows a Prometheus monitoring interface displaying query results related to the "gotk\_reconcile\_condition" metric, with details about containers, endpoints, and statuses.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877666/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/prometheus-monitoring-query-results-gotk.jpg)
</Frame>

Switch to **Graph** mode for time-series visualization:

<Frame>
  ![The image shows a Prometheus monitoring dashboard with a graph displaying multiple colored lines representing different metrics over time. A tooltip provides detailed information about a specific data point on the graph.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877667/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/prometheus-monitoring-dashboard-graph-metrics.jpg)
</Frame>

## 5. Explore Grafana Dashboards

After Flux applies the dashboard JSON, refresh Grafana. Two dashboards are now available:

* **Flux Control Plane**
* **Flux Cluster Stats**

### Flux Control Plane

Tracks each controller’s queue lengths, CPU/memory usage, API request rates, and reconciliation durations:

<Frame>
  ![The image shows a dashboard interface displaying metrics for a Flux Control Plane, including controllers, max work queue time, memory usage, API requests, and resource usage graphs for CPU and memory.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877668/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/flux-control-plane-dashboard-metrics.jpg)
</Frame>

<Frame>
  ![The image shows a dashboard with graphs displaying metrics related to a Flux control plane, including successful and failed reconciliations, Git pulls, and Helm stats.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877669/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/flux-control-plane-dashboard-graphs.jpg)
</Frame>

### Flux Cluster Stats

Provides cluster-wide health: counts of reconcilers, failing controllers, manifest source statuses, operation durations, and readiness tables:

<Frame>
  ![The image shows a dashboard interface displaying metrics for a Flux Control Plane, including controllers, max work queue time, memory usage, API requests, and resource usage graphs.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877670/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/flux-control-plane-dashboard-metrics-2.jpg)
</Frame>

<Frame>
  ![The image shows a Flux Cluster Stats dashboard displaying metrics such as cluster reconcilers, failing reconcilers, Kubernetes manifest sources, and their statuses. It includes tables and graphs indicating reconciliation readiness and operation durations.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877671/notes-assets/images/GitOps-with-FluxCD-DEMO-Monitor-Flux-using-Prometheus-Grafana/flux-cluster-stats-dashboard-metrics.jpg)
</Frame>

These dashboards ship out of the box—just apply them to get comprehensive visibility into your Flux GitOps workflows.

***

## Links and References

* [Flux v2 Documentation](https://fluxcd.io/docs/)
* [Prometheus Documentation](https://prometheus.io/docs/)
* [Grafana Dashboards](https://grafana.com/grafana/dashboards)
* [GitOps with Flux](https://fluxcd.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/fb9e59dc-9dee-4532-92a8-553d0df1df27/lesson/64787e16-94e0-41b2-a537-b3f1fcf7023b" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/fb9e59dc-9dee-4532-92a8-553d0df1df27/lesson/ec051c13-205b-4a16-8ceb-e1586ebbe765" />
</CardGroup>
