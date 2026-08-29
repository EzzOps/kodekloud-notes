# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Introduction/page

Guide to monitoring Kubernetes with Prometheus, using Helm and kube-prometheus-stack including Prometheus Operator, ServiceMonitor, PodMonitor, kube-state-metrics and Node Exporter

In this lesson we'll cover how to monitor applications and the Kubernetes cluster itself using Prometheus. Kubernetes exposes a wide range of infrastructure metrics (control plane, nodes, pods, deployments, etc.), and Prometheus can scrape both application-level and cluster-level metrics.

Running Prometheus inside the cluster you are monitoring is typically recommended for two main reasons:

* Prometheus should run as close to its scrape targets as possible for reliability and performance.
* You can reuse existing Kubernetes infrastructure instead of managing a separate VM or external host.

<Frame>
  <img alt="The image is a diagram of a Kubernetes cluster, showing a control plane with components like API and c-m, nodes with kubelet, and suggestions to deploy close to targets and use existing infrastructure." />
</Frame>

There are two primary monitoring categories in Kubernetes:

1. Application monitoring — web apps, services, databases, custom application metrics.
2. Cluster monitoring — API server, scheduler, kubelets, node OS metrics, and Kubernetes object state.

Below are the typical sources you will collect cluster-level metrics from:

* API Server, kube-scheduler, CoreDNS, and other control-plane components.
* kubelet (exposes cAdvisor-style container metrics).
* `kube-state-metrics` (converts Kubernetes API objects into Prometheus metrics).
* Node Exporter on each node to collect OS-level metrics (CPU, memory, disk, network).

<Frame>
  <img alt="The image is a slide discussing monitoring applications on Kubernetes infrastructure, detailing the components and metrics involved." />
</Frame>

kube-state-metrics

* Kubernetes does not expose higher-level cluster objects (Deployments, ReplicaSets, Services, etc.) as Prometheus metrics by default. `kube-state-metrics` watches the Kubernetes API and exposes metrics derived from those objects for Prometheus to scrape. It runs as a normal Pod in the cluster and is the standard way to gather cluster state.

Node-level metrics

* For OS-level metrics, run a Node Exporter on each host. In Kubernetes, the recommended pattern is to deploy Node Exporter as a DaemonSet so a pod runs on every node (including new nodes as they join).

<Frame>
  <img alt="The image describes the setup of a Node Exporter in a Kubernetes Cluster, suggesting the use of a daemonSet for efficiency. It includes a diagram of a cluster with three nodes." />
</Frame>

Service discovery and scraping

* Prometheus integrates with Kubernetes Service Discovery: it queries the Kubernetes API to discover scrape targets (control-plane endpoints, kubelet/node-exporters, `kube-state-metrics`, application Services, etc.). This removes the need for manually maintaining endpoint lists.

<Frame>
  <img alt="The image illustrates a service discovery process involving Kubernetes API and Prometheus, connecting to Kube components, node exporters, and Kube state metrics." />
</Frame>

Manual Prometheus deployments on Kubernetes

* You can deploy Prometheus manually by creating Deployments, StatefulSets, Services, ConfigMaps, and Secrets, but this approach is verbose, repetitive, and error-prone for production-grade setups.

<Frame>
  <img alt="The image illustrates the complexity of manually deploying Prometheus on Kubernetes, highlighting the need for configuring deployments, services, configMaps, and secrets. It notes the process is complex and not the simplest solution." />
</Frame>

Use Helm + kube-prometheus-stack for simplicity

* Helm is the de facto package manager for Kubernetes that packages manifests, templates, and configuration into charts.
* The Prometheus Community chart `kube-prometheus-stack` packages a complete, production-ready Prometheus stack tuned for Kubernetes.

Quick install example:

```bash theme={null}
$ helm install prometheus prometheus-community/kube-prometheus-stack
```

Charts allow parameterized deployments and hide the low-level manifest details, making upgrades and maintenance simpler.

<Frame>
  <img alt="The image is a slide titled &#x22;Helm Charts&#x22; explaining that a helm chart is a collection of template and YAML files converting into Kubernetes manifest files, and that helm charts can be shared by uploading to a repository." />
</Frame>

What kube-prometheus-stack provides

* The chart deploys a complete monitoring stack for Kubernetes: Prometheus Server, Alertmanager, Pushgateway, Grafana (optional), and the Prometheus Operator that manages lifecycle and configuration.

A Kubernetes Operator is an application-specific controller that extends Kubernetes with Custom Resource Definitions (CRDs) to create and manage complex applications. The Prometheus Operator provides high-level CRDs tailored for Prometheus-based monitoring.

<Frame>
  <img alt="The image describes the Kube-Prometheus-stack chart, which utilizes the Prometheus Operator to create, configure, and manage instances of complex applications using the Kubernetes API." />
</Frame>

Why use the Prometheus Operator?

* The operator handles lifecycle tasks: installation, configuration, upgrades, rolling restarts on config changes, and resource ownership.
* Using the operator replaces the need to manage multiple low-level objects by offering higher-level CRs such as `Prometheus`, `ServiceMonitor`, `PodMonitor`, `PrometheusRule`, and `Alertmanager`.

<Frame>
  <img alt="The image explains that the Kube-Prometheus-stack chart utilizes the Prometheus Operator to manage complex applications in Kubernetes. It includes a link to the Prometheus Operator GitHub page." />
</Frame>

Example: Prometheus custom resource

* Instead of creating StatefulSets or Deployments directly, you declare a `Prometheus` custom resource that the operator translates into the required Kubernetes primitives.

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  annotations:
    meta.helm.sh/release-name: prometheus
    meta.helm.sh/release-namespace: default
  creationTimestamp: "2022-11-18T01:19:29Z"
  generation: 1
  labels:
    app: kube-prometheus-stack-prometheus
    name: prometheus-kube-prometheus-prometheus
spec:
  alerting:
    alertmanagers:
      - apiVersion: v2
        name: prometheus-kube-prometheus-alertmanager
        namespace: default
        pathPrefix: /
        port: http-web
```

Prometheus Operator CRDs — summary table

| CRD                  | Purpose                                       | Typical use                                                  |
| -------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| `Prometheus`         | Defines a Prometheus server instance and spec | Deploy and configure Prometheus replicas, retention, storage |
| `Alertmanager`       | Deploys/configures Alertmanager cluster       | High-availability Alertmanager setup                         |
| `PrometheusRule`     | Recording and alerting rules                  | Store alerting rules consumed by Prometheus                  |
| `ServiceMonitor`     | Discover Service endpoints to scrape          | Tell Prometheus which Services to scrape                     |
| `PodMonitor`         | Discover Pod endpoints to scrape              | Scrape metrics exposed directly by Pods                      |
| `AlertmanagerConfig` | Alertmanager receiver config                  | Fine-grained routing and notification configs                |

ServiceMonitor and PodMonitor

* Use `ServiceMonitor` and `PodMonitor` objects to declare scrape targets in a Kubernetes-native way. This avoids editing Prometheus config directly and integrates cleanly with Kubernetes RBAC and namespaces.

<Callout icon="lightbulb">
  Using the kube-prometheus-stack chart plus the Prometheus Operator provides a Kubernetes-native, declarative approach to deploy and manage Prometheus, Alertmanager, and related resources with far less manual YAML and maintenance overhead.
</Callout>

Further reading and references

* Prometheus Operator — [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
* kube-prometheus-stack chart — [https://github.com/prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts)
* Kubernetes documentation — [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* kube-state-metrics — [https://github.com/kubernetes/kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
* Helm documentation — [https://helm.sh/docs/](https://helm.sh/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/69a0ec52-6238-4e25-8ab3-d24bfe735b1d" />
</CardGroup>
