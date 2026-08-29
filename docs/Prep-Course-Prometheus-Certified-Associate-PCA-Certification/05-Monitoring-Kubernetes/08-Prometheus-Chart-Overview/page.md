# macOS (Homebrew)
brew install helm

# Windows (Chocolatey)
choco install kubernetes-helm

# Windows (Scoop)
scoop install helm
```

For other package managers (APT, YUM, etc.), see the Helm docs linked above.

Verify Helm is installed:

```bash theme={null}
helm version
```

Example output (your version/build info may differ):

```bash theme={null}
version.BuildInfo{Version:"v3.10.2", GitCommit:"50f003e5ee8704ec937a756c646870227d7c8b58", GitTreeState:"clean", GoVersion:"go1.18.8"}
```

## 2) Add the Prometheus Helm repository and update

Add the Prometheus Community chart repository and refresh your local index:

```bash theme={null}
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

Typical update output when the repo already exists:

```bash theme={null}
"prometheus-community" already exists with the same configuration, skipping
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "prometheus-community" chart repository
Update Complete. ⚓Happy Helming!⚓
```

<Callout icon="lightbulb">
  The release name you provide when installing a chart (for example `prometheus` in this guide) is arbitrary. Choose any valid name; just be consistent when running `helm upgrade`, `helm uninstall`, or when querying resources by label.
</Callout>

## 3) Inspect chart values (optional but recommended)

Charts expose many configurable values. To view the kube-prometheus-stack defaults:

```bash theme={null}
helm show values prometheus-community/kube-prometheus-stack
```

Save defaults to a file for customization:

```bash theme={null}
helm show values prometheus-community/kube-prometheus-stack > values.yaml
```

A short illustrative excerpt from `values.yaml`:

```yaml theme={null}
## Provide a name in place of kube-prometheus-stack for `app:` labels
nameOverride: ""

## Override the deployment namespace
namespaceOverride: ""

## Provide a k8s version to auto dashboard import script example: kubeTargetVersionOverride: 1.16.6
kubeTargetVersionOverride: ""

## Labels to apply to all resources
commonLabels: {}
  scmhash: abc123

## Service configuration example
externalTrafficPolicy: Cluster
type: ClusterIP

servicePerReplica:
  enabled: false
  annotations: {}

port: 9093
targetPort: 9093
nodePort: 30904
```

Edit `values.yaml` to adjust namespace, persistence, resource requests/limits, scrape settings, alerting configuration, and dashboard imports.

<Callout icon="lightbulb">
  To deploy with your custom values file, pass it during install or upgrade: `helm install prometheus prometheus-community/kube-prometheus-stack -f values.yaml` (or `helm upgrade --install prometheus ... -f values.yaml`).
</Callout>

## 4) Install the chart

Install the chart with default values:

```bash theme={null}
helm install prometheus prometheus-community/kube-prometheus-stack
```

Or install using your customized values:

```bash theme={null}
helm install prometheus prometheus-community/kube-prometheus-stack -f values.yaml
```

Example installation summary:

```bash theme={null}
NAME: prometheus
LAST DEPLOYED: Mon Nov 21 13:22:39 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
kube-prometheus-stack has been installed. Check its status by running:
  kubectl --namespace default get pods -l "release=prometheus"

Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.
```

Verify pods and other resources created by the release:

```bash theme={null}
kubectl --namespace default get pods -l "release=prometheus"
kubectl --namespace default get svc -l "release=prometheus"
kubectl --namespace default get pvc -l "release=prometheus"
```

## 5) Uninstall the release

Remove the release and associated resources created by the chart:

```bash theme={null}
helm uninstall prometheus
```

If you deployed to a namespace other than `default`, append `--namespace <namespace>` to both install and uninstall commands.

## Quick reference: common commands

| Action                  | Command                                                                                 |
| ----------------------- | --------------------------------------------------------------------------------------- |
| Add repo                | `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts` |
| Update repos            | `helm repo update`                                                                      |
| Inspect values          | `helm show values prometheus-community/kube-prometheus-stack`                           |
| Save values             | `helm show values prometheus-community/kube-prometheus-stack > values.yaml`             |
| Install (defaults)      | `helm install prometheus prometheus-community/kube-prometheus-stack`                    |
| Install (custom)        | `helm install prometheus prometheus-community/kube-prometheus-stack -f values.yaml`     |
| Upgrade (apply changes) | `helm upgrade prometheus prometheus-community/kube-prometheus-stack -f values.yaml`     |
| Uninstall               | `helm uninstall prometheus`                                                             |
| Verify pods             | `kubectl get pods -l "release=prometheus"`                                              |

## Summary

* Install Helm (script or package manager) and verify with `helm version`.
* Add the `prometheus-community` Helm repository and run `helm repo update`.
* Optionally inspect and customize chart defaults with `helm show values` and a `values.yaml` file.
* Install the kube-prometheus-stack chart: `helm install <release-name> prometheus-community/kube-prometheus-stack` (use `-f values.yaml` to apply customizations).
* Verify resources using `kubectl` and remove the release with `helm uninstall <release-name>`.

## Links and references

* [Helm Documentation](https://helm.sh/docs/)
* [Prometheus Community Helm Charts](https://prometheus-community.github.io/helm-charts)
* [kube-prometheus Repository](https://github.com/prometheus-operator/kube-prometheus)

This article will be followed by a deeper look at the Kubernetes resources the kube-prometheus-stack chart creates and how Prometheus, Alertmanager, and the operator are configured.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/601c8a1d-c743-457e-85e5-a39ea757c476" />
</CardGroup>


# Prometheus Chart Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Prometheus-Chart-Overview/page

Guide to inspecting kube-prometheus-stack Helm chart resources, mapping created Kubernetes objects to Prometheus components and extracting generated configuration and rule files

We installed the Prometheus Helm chart (kube-prometheus-stack). Let's inspect what it created and where the important configuration and rule files live. This guide walks through the main resources, how they map to Prometheus components, and the exact commands to inspect and extract configuration for editing.

## Quick summary (what the Helm chart installs)

* StatefulSets: Prometheus server, Alertmanager
* Deployments: Prometheus Operator, kube-state-metrics, Grafana
* ReplicaSets: associated with the Deployments above
* DaemonSet: node-exporter (one pod per node)
* Services: ClusterIP services for internal access
* Secrets / ConfigMaps: generated Prometheus config and rule files

<Callout icon="lightbulb">
  The Helm chart also installs Grafana and configures it to use the Prometheus datasource out of the box. Grafana provides a graphical UI to visualize Prometheus metrics (installed automatically by the chart).
</Callout>

***

## Inspect the cluster resources

Run:

```bash theme={null}
kubectl get all
```

Example output (trimmed for readability):

```text theme={null}
NAME                                               READY   STATUS    RESTARTS   AGE
pod/alertmanager-kube-prometheus-alertmanager-0    2/2     Running   1          158m
pod/prometheus-grafana-d978dcd9-xhvgw              3/3     Running   0          158m
pod/prometheus-prometheus-kube-prometheus-0        2/2     Running   0          158m
pod/prometheus-prometheus-node-exporter-5ptg       1/1     Running   1          158m

NAME                                       TYPE        CLUSTER-IP       PORT(S)
service/prometheus-grafana                 ClusterIP   10.100.235.247   443/TCP
service/prometheus-kube-prometheus        ClusterIP   10.100.53.131    9093/TCP
service/prometheus-kube-state-metrics     ClusterIP   10.100.196.32    9090/TCP

NAME                                                       DESIRED   CURRENT   READY
daemonset.apps/prometheus-prometheus-node-exporter         2         2         2

NAME                                               READY   UP-TO-DATE   AVAILABLE
deployment.apps/prometheus-grafana                 1/1     1            1
deployment.apps/prometheus-kube-prometheus-operator 1/1     1            1
```

### Resource summary table

| Resource Type      | Purpose                                       | Example from chart                                          |
| ------------------ | --------------------------------------------- | ----------------------------------------------------------- |
| StatefulSet        | Runs stateful components (persistent storage) | Prometheus server, Alertmanager                             |
| Deployment         | Managed, scalable pods                        | `prometheus-grafana`, `prometheus-kube-prometheus-operator` |
| ReplicaSet         | Deployment's replica controller               | `prometheus-grafana-<hash>`                                 |
| DaemonSet          | Runs a pod per node                           | `prometheus-prometheus-node-exporter`                       |
| Service            | Internal networking to pods                   | `prometheus-prometheus` (ClusterIP)                         |
| ConfigMap / Secret | Prometheus config and rulefiles               | `prometheus...-rulefiles-0`, `prometheus...` secret         |

***

## StatefulSets (Prometheus & Alertmanager)

Start from the bottom of `kubectl get all` output: the StatefulSets are the Prometheus server and Alertmanager.

List StatefulSets:

```bash theme={null}
kubectl get statefulset
```

Example:

```text theme={null}
NAME                                                     READY   AGE
alertmanager-prometheus-kube-prometheus-alertmanager     1/1     168m
prometheus-prometheus-kube-prometheus-prometheus         1/1     168m
```

Describe the Prometheus StatefulSet to inspect containers, args, mounts, and volumes:

```bash theme={null}
kubectl describe statefulset prometheus-prometheus-kube-prometheus-prometheus
```

You can pipe the full description to a file for easier viewing in an editor:

```bash theme={null}
kubectl describe statefulset prometheus-prometheus-kube-prometheus-prometheus > prometheus-statefulset.txt
```

Key sections you'll see in the StatefulSet description:

* Prometheus container args (web UI, storage path, config file)
* Init container: `prometheus-config-reloader` (creates initial config)
* Sidecar/container: config reloader (watches config changes and triggers Prometheus reload)
* Mounts and Volumes (where Prometheus YAML and rule files come from)

Example container args extracted from the StatefulSet (trimmed):

```yaml theme={null}
containers:
  - name: prometheus
    image: quay.io/prometheus/prometheus:v2.39.1
    ports:
      - containerPort: 9090
    args:
      - --web.console.templates=/etc/prometheus/consoles
      - --web.console.libraries=/etc/prometheus/console_libraries
      - --storage.tsdb.retention.time=10d
      - --config.file=/etc/prometheus/config_out/prometheus.env.yaml
      - --storage.tsdb.path=/prometheus
      - --web.enable-lifecycle
      - --web.external-url=http://prometheus-kube-prometheus-prometheus.default:9090
```

Init container (responsible for initial config):

```yaml theme={null}
initContainers:
  - name: init-config-reloader
    image: quay.io/prometheus-operator/prometheus-config-reloader:v0.60.1
    command:
      - /bin/prometheus-config-reloader
    args:
      - --watch-interval=0
      - --listen-address=:8080
      - --config-file=/etc/prometheus/config/prometheus.yaml.gz
      - --config-envsubst-file=/etc/prometheus/config_out/prometheus.env.yaml
      - --watched-dir=/etc/prometheus/rules/
```

The StatefulSet mounts show where the config, rule files, and web config live:

```yaml theme={null}
mounts:
  - /etc/prometheus/config from config (rw)         # Prometheus YAML (from Secret)
  - /etc/prometheus/config_out from config-out (rw) # generated config
  - /etc/prometheus/rules/... from <rulefiles> (rw) # ConfigMap with rule files
  - /etc/prometheus/web_config/web-config.yaml from web-config (rw)
volumes:
  config:
    type: Secret
    secretName: prometheus-prometheus-kube-prometheus
  prometheus-prometheus-kube-prometheus-prometheus-rulefiles-0:
    type: ConfigMap
    name: prometheus-prometheus-kube-prometheus-rulefiles-0
  web-config:
    type: Secret
    secretName: prometheus-prometheus-kube-prometheus-web-config
```

***

## Deployments and ReplicaSets

Key deployments:

* `prometheus-kube-prometheus-operator` — the Prometheus Operator container that manages Prometheus instances and their lifecycle.
* `prometheus-grafana` — Grafana UI.
* `prometheus-kube-state-metrics` — exposes Kubernetes object metrics (deployments, pods, etc).

Describe the operator deployment:

```bash theme={null}
kubectl describe deployment prometheus-kube-prometheus-operator > operator-deployment.txt
```

Important flags you’ll see for the operator:

```yaml theme={null}
containers:
  - name: kube-prometheus-stack
    image: quay.io/prometheus-operator/prometheus-operator:v0.60.1
    args:
      - --kubelet-service=kube-system/prometheus-kube-prometheus-kubelet
      - --localhost=127.0.0.1
      - --prometheus-config-reloader=quay.io/prometheus-operator/prometheus-config-reloader:v0.60.1
      - --config-reloader-cpu-request=200m
      - --config-reloader-memory-request=50Mi
      - --thanos-default-base-image=quay.io/thanos/thanos:v0.28.1
      - --web.enable-tls=true
      - --web.cert-file=/cert/cert
      - --web.key-file=/cert/key
      - --web.listen-address=:10250
```

The operator primarily watches Kubernetes API objects (Prometheus, ServiceMonitor, PodMonitor, PrometheusRule, etc.) and generates the Prometheus configuration, rule files, and Secrets/ConfigMaps used by the Prometheus StatefulSet.

***

## DaemonSet — node-exporter

The chart creates a DaemonSet called something like `prometheus-prometheus-node-exporter`. DaemonSets ensure one node-exporter pod runs on each cluster node and expose host metrics (CPU, memory, filesystem) for Prometheus to scrape.

Check nodes and daemonset status:

```bash theme={null}
kubectl get nodes
kubectl get daemonset -n default prometheus-prometheus-node-exporter
```

***

## Pods and Services

Pods section shows all pods created (Prometheus, Alertmanager, Grafana, Operator, kube-state-metrics, two node-exporters).

Services created are typically ClusterIP (internal) by default:

```bash theme={null}
kubectl get svc
```

If you want to access Prometheus or Grafana externally you can:

* Create an Ingress
* Change the Service type to `LoadBalancer`
* Use `kubectl port-forward` or `kubectl proxy` for quick local access

***

## Where the Prometheus configuration and rule files live

The Prometheus Operator generates the Prometheus configuration and stores it in a Secret (gzipped `prometheus.yaml.gz`) that is mounted into the Prometheus pod. Rule files are stored in a ConfigMap.

To inspect the Secret containing the generated Prometheus config:

```bash theme={null}
kubectl describe secret prometheus-prometheus-kube-prometheus > prometheus.yaml
```

Example Secret description:

```text theme={null}
Name:         prometheus-prometheus-kube-prometheus
Namespace:    default
Labels:       managed-by=prometheus-operator
Annotations:  generated: true
Type: Opaque

Data
====
prometheus.yaml.gz:  1723 bytes
```

To inspect rule files (ConfigMap with alerting/recording rules):

```bash theme={null}
kubectl describe configmap prometheus-prometheus-kube-prometheus-prometheus-rulefiles-0 > rulefile.yaml
```

A rulefile excerpt will look like:

```yaml theme={null}
groups:
- name: kubernetes-system
  rules:
  - alert: KubeVersionMismatch
    annotations:
      description: There are {{ $value }} different semantic versions of Kubernetes components running.
      summary: Different semantic versions of Kubernetes components running.
    expr: count by (cluster) (count by (git_version, cluster) (label_replace(kubernetes_build_info{job~"kube-dns|coredns"},"git_version","$1","git_version", "(v[0-9]*.[0-9]*).*")) > 1
    for: 15m
    labels:
      severity: warning
```

If you prefer to view the raw generated file locally, dump the secret and extract the gzipped YAML:

```bash theme={null}
kubectl get secret prometheus-prometheus-kube-prometheus -o jsonpath="{.data.prometheus\.yaml\.gz}" | base64 --decode > prometheus.yaml.gz
gunzip prometheus.yaml.gz
less prometheus.yaml
```

<Callout icon="warning">
  Do not manually edit the generated Secret or ConfigMap created by the operator. Changes will be overridden by the operator. Instead, use Kubernetes-native objects supported by the Prometheus Operator (ServiceMonitor, PodMonitor, PrometheusRule, Prometheus CR) to configure scraping and rules.
</Callout>

***

## How the config reload workflow works

* The Prometheus Operator generates `prometheus.yaml` and writes it into a Secret.
* The Prometheus StatefulSet mounts that Secret into `/etc/prometheus/config`.
* An init container (`init-config-reloader`) and a sidecar `prometheus-config-reloader` watch the config/rule mounts (ConfigMap / Secret / EmptyDir).
* When a change is detected, the reloader triggers Prometheus' `/-/reload` endpoint so Prometheus applies the updated configuration without manual restarts.

Reloader config example (from the StatefulSet):

```yaml theme={null}
config-reloader:
  image: quay.io/prometheus-operator/prometheus-config-reloader:v0.60.1
  command:
    - /bin/prometheus-config-reloader
  args:
    - --listen-address=:8080
    - --reload-url=http://127.0.0.1:9090/-/reload
    - --config-file=/etc/prometheus/config/prometheus.yaml.gz
    - --config-envsubst-file=/etc/prometheus/config_out/prometheus.env.yaml
    - --watched-dir=/etc/prometheus/rules/
```

***

## PrometheusRule objects vs editing the generated files

Use Prometheus Operator resources (PrometheusRule) to add or modify alerting and recording rules. The operator will render these into the rule ConfigMap(s) and mount them into Prometheus. This is the recommended pattern — it avoids manual edits to the generated artifacts.

Example: create a `PrometheusRule` manifest and apply with `kubectl apply -f myrule.yaml`. The operator merges it into the rule ConfigMap.

***

## Quick commands cheat-sheet

```bash theme={null}
