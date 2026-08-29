# Additional Scrape Configs

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Additional-Scrape-Configs/page

Explains how to add Prometheus scrape jobs via kube-prometheus-stack additionalScrapeConfigs and recommends using ServiceMonitors as the preferred operator native approach

So we got our application deployed onto Kubernetes:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: api-service
  labels:
    job: node-api
```

Now it's time to make Prometheus aware of these new targets. There are two main approaches:

* The less ideal approach: use the chart's `additionalScrapeConfigs` to append raw Prometheus scrape jobs to the server configuration.
* The preferred approach: use ServiceMonitors, the Prometheus Operator–native, declarative way to add targets.

Below I show the high-level steps for the less-preferred approach, so you understand what to change. It will work, but there are caveats.

<Callout icon="warning">
  Using `additionalScrapeConfigs` means you are appending raw Prometheus scrape configuration. The chart does not validate these entries and upgrades could potentially break if the scrape config is incompatible with future Prometheus changes. Prefer ServiceMonitors for a more robust, operator-friendly solution.
</Callout>

1. Dump the chart's default values so you can edit them:

```bash theme={null}
helm show values prometheus-community/kube-prometheus-stack > values.yaml
```

2. Open `values.yaml` and search for `additionalScrapeConfigs`. This field lets you append Prometheus scrape jobs. The chart will not validate the contents, so ensure the jobs are valid Prometheus configuration blocks.

Here is an example of how you can add additional scrape jobs (this is one valid way to format the jobs; adapt jobs and relabeling rules to your environment):

```yaml theme={null}
additionalScrapeConfigs:
- job_name: kube-etcd
  kubernetes_sd_configs:
  - role: node
  scheme: https
  tls_config:
    ca_file: /etc/prometheus/secrets/etcd-client-cert/etcd-ca
    cert_file: /etc/prometheus/secrets/etcd-client-cert/etcd-client
    key_file: /etc/prometheus/secrets/etcd-client-cert/etcd-client-key
  relabel_configs:
  - action: labelmap
    regex: __meta_kubernetes_node_label_(.+)
  - source_labels: [__address__]
    action: replace
    target_label: __address__
    regex: '([^;]+):(\d+)'
    replacement: '${1}:2379'
