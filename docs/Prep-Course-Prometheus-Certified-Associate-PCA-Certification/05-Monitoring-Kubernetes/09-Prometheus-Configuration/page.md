# Show all cluster resources
kubectl get all

# List StatefulSets and inspect Prometheus StatefulSet
kubectl get statefulset
kubectl describe statefulset prometheus-prometheus-kube-prometheus-prometheus

# Dump generated Prometheus config secret to file
kubectl get secret prometheus-prometheus-kube-prometheus -o jsonpath="{.data.prometheus\.yaml\.gz}" | base64 --decode > prometheus.yaml.gz
gunzip prometheus.yaml.gz

# Dump rule ConfigMap to file
kubectl describe configmap prometheus-prometheus-kube-prometheus-prometheus-rulefiles-0 > rulefile.yaml

# Inspect operator deployment
kubectl describe deployment prometheus-kube-prometheus-operator > operator-deployment.txt

# View node-exporter daemonset
kubectl get daemonset prometheus-prometheus-node-exporter -o wide
```

***

## Useful links and references

* Prometheus Operator docs: [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
* Prometheus Operator runbooks and rules: [https://prometheus-operator.dev/](https://prometheus-operator.dev/)
* Kubernetes kubectl docs: [https://kubernetes.io/docs/reference/kubectl/overview/](https://kubernetes.io/docs/reference/kubectl/overview/)

***

If you'd like, I can:

* Show an example `PrometheusRule` manifest and walk you through adding an alert, or
* Provide a sample `ServiceMonitor` to scrape a custom app and demonstrate how the operator renders the config.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/cabca690-195e-4e68-8785-938fd09a887b" />
</CardGroup>


# Prometheus Configuration

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Prometheus-Configuration/page

Explains Helm installed Prometheus configuration, Kubernetes service discovery roles, and relabeling rules used to select scrape targets and configure TLS and authorization.

Now that you can connect to your Prometheus server, this article inspects the default configuration the Helm chart installs and explains how Kubernetes service discovery (SD) is used to dynamically discover scrape targets.

Kubernetes exposes multiple SD roles that Prometheus can use to discover targets. Each role returns different metadata that you can filter using relabeling rules.

| SD Role   | What it discovers                                 | Typical metadata / use                                                                                                                 |
| --------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| node      | All nodes in the cluster                          | Node name, IP, labels — useful for node-exporter or kubelet scraping                                                                   |
| service   | Kubernetes Services and their ports               | Service name, labels, ports — useful for Service-level targeting                                                                       |
| pod       | Pods directly                                     | Pod name, labels, pod IP — useful to target a pod's metrics endpoint                                                                   |
| endpoints | Individual endpoints (IP + port) backing Services | Most flexible: enumerates every IP:port in the cluster (Pods, Nodes, external endpoints) and exposes endpoint + service + pod metadata |

<Callout icon="lightbulb">
  The Helm charts commonly use the `endpoints` role for Kubernetes SD. Because `endpoints` enumerates IP:port pairs for Services, Pods, and Nodes, relabeling rules then narrow that large set to the exact targets you want to scrape.
</Callout>

<Frame>
  <img alt="The image is a screenshot of a webpage or document describing Kubernetes SD (service discovery) configurations, detailing node, service, and pod roles with associated meta labels for retrieving targets from the Kubernetes REST API." />
</Frame>

Inspecting the generated configuration

* In the Prometheus web UI go to Status → Configuration to view the generated `prometheus.yml`.
* The important section is `scrape_configs` — this is where SD and relabeling determine which endpoints Prometheus scrapes.
* Helm-generated configs typically create many `scrape_configs` (one per ServiceMonitor/PodMonitor, or per built-in component), each using `kubernetes_sd_configs` with `role: endpoints`.

Representative scrape config (cleaned) that a Helm chart uses to find Alertmanager endpoints. Notice `kubernetes_sd_configs` with `role: endpoints` and relabel rules that keep only the Alertmanager Service and its `web` port:

```yaml theme={null}
scrape_configs:
  - job_name: "serviceMonitor/default/prometheus-kube-prometheus-alertmanager"
    honor_labels: true
    metrics_path: /metrics
    scrape_interval: 30s
    scrape_timeout: 10s
    scheme: http
    follow_redirects: true
    kubernetes_sd_configs:
      - role: endpoints
        kubeconfig_file: ""
        follow_redirects: true
        enable_http2: true
    relabel_configs:
      - source_labels: [__meta_kubernetes_service_name]
        separator: ;
        regex: prometheus-kube-prometheus-alertmanager
        action: keep
      - source_labels: [__meta_kubernetes_endpoint_port_name]
        separator: ;
        regex: web
        action: keep
```

How relabeling restricts what Prometheus scrapes

* Kubernetes SD returns a broad set of endpoint entries. Prometheus relies on relabeling rules to include or exclude targets by matching metadata exposed by the SD.
* Common metadata keys you’ll see in relabeling rules:
  * `__meta_kubernetes_service_name`
  * `__meta_kubernetes_endpoint_port_name`
  * `__meta_kubernetes_service_label_<label>`
  * `__meta_kubernetes_endpoint_address_target_*` (for pod/node backing info)

Example relabel rules that filter by service labels and endpoint port:

```yaml theme={null}
relabel_configs:
  - source_labels: [__meta_kubernetes_service_label_app, __meta_kubernetes_service_labelpresent_app]
    separator: ;
    regex: (kube-prometheus-stack-alertmanager);true
    replacement: $1
    action: keep

  - source_labels: [__meta_kubernetes_service_label_release, __meta_kubernetes_service_labelpresent_release]
    separator: ;
    regex: (prometheus);true
    replacement: $1
    action: keep

  - source_labels: [__meta_kubernetes_service_label_self_monitor, __meta_kubernetes_service_labelpresent_self_monitor]
    separator: ;
    regex: (true);true
    replacement: $1
    action: keep

  - source_labels: [__meta_kubernetes_endpoint_port_name]
    separator: ;
    regex: http-web
    replacement: $1
    action: keep
```

Common relabel operations and patterns

| Operation                                | Purpose                                                             | Example                                                                    |
| ---------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Keep by service name / label / port      | Restrict the discovered endpoints to only those you want            | `action: keep` with `__meta_kubernetes_service_name`                       |
| Replace/copy metadata into target labels | Populate Prometheus target labels like `container` or `job`         | Use `target_label:` and `replacement:`                                     |
| Extract backing resource names           | Set labels based on whether the endpoint is backed by a Pod or Node | Use `__meta_kubernetes_endpoint_address_target_kind` and `..._target_name` |

Example replacements that convert metadata into Prometheus target labels:

```yaml theme={null}
relabel_configs:
  - source_labels: [__meta_kubernetes_service_name]
    regex: (.+)
    target_label: container
    replacement: $1
    action: replace

  - source_labels: [__address__]
    regex: (.+)
    target_label: endpoint
    replacement: https://$1
    action: replace
```

TLS and authorization for cluster components

* Components such as the Kubernetes API server or kubelet require HTTPS and authentication.
* Even when using `kubernetes_sd_configs` to locate endpoints, the corresponding `scrape_configs` will include `scheme: https`, `tls_config`, and `authorization` blocks so Prometheus can authenticate and validate TLS.

```yaml theme={null}
- job_name: "serviceMonitor/default/prometheus-kube-prometheus-apiserver"
  scheme: https
  metrics_path: /
  authorization:
    credentials_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    server_name: kubernetes
    insecure_skip_verify: false
  kubernetes_sd_configs:
    - role: endpoints
      follow_redirects: true
```

<Callout icon="warning">
  When scrape configs reference in-cluster secrets (for `credentials_file` or `ca_file`), ensure Prometheus has appropriate RBAC access and the service account tokens/CA files are mounted at the expected paths. Misconfigured RBAC or missing files will result in scrape failures (DOWN targets).
</Callout>

What you should verify in the Prometheus UI

* Status → Configuration: review the generated `scrape_configs` and relabel rules.
* Status → Targets: inspect discovered endpoints, `UP`/`DOWN` states, labels, and latest scrape durations.

<Frame>
  <img alt="The image shows a Prometheus web interface displaying the status of various monitored targets, all of which are currently in &#x22;UP&#x22; state, along with their endpoints, labels, and scrape durations." />
</Frame>

Summary

* Helm charts commonly use Kubernetes SD with `role: endpoints` to discover nearly all cluster targets.
* Relabel rules narrow the broad set of discovered endpoints to the exact targets you want to scrape (by service name, service labels, endpoint port name, etc.).
* Components that require TLS/auth include `tls_config` and `authorization` settings in their scrape configs.
* Use Status → Configuration and Status → Targets to inspect generated configs and validate scrapes.

Links and References

* [Prometheus: Service discovery](https://prometheus.[AWS_SECRET_ACCESS_KEY]configuration/#kubernetes_sd_config)
* [Kubernetes: Services, Endpoints and Pods](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Prometheus relabeling guide](https://prometheus.[AWS_SECRET_ACCESS_KEY]relabel_config/)
* [Helm charts (kube-prometheus-stack)](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/1f206fab-608b-4e75-a2a2-2808265c2341" />
</CardGroup>
