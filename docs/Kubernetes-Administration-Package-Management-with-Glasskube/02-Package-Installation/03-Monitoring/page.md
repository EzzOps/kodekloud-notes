# Monitoring

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Installation/Monitoring/page

Installing Kubetail and kube-prometheus-stack via Glasskube to enable real-time log streaming, Prometheus metrics, Grafana dashboards, and Alertmanager alerting for Kubernetes clusters

This article demonstrates how to use Glasskube to install two observability packages for Kubernetes: Kubetail (real-time log streaming) and the kube-prometheus-stack (Prometheus + Alertmanager + Grafana). We install Kubetail first to get immediate access to pod logs, then deploy the kube-prometheus-stack for metrics, dashboards, and alerting.

## What you'll get

* Real-time, web-based log streaming across pods and containers with Kubetail
* A full metrics & alerting stack with Prometheus, Alertmanager, Grafana, and exporters via kube-prometheus-stack
* Pre-configured dashboards and alerting rules that work out of the box

Learn more:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [kube-prometheus (Prometheus Operator)](https://github.com/prometheus-operator/kube-prometheus)
* [Grafana documentation](https://grafana.com/docs/)

***

## Kubetail: real-time log viewer

Kubetail (as packaged by Glasskube) provides a web UI for streaming and filtering logs across your cluster in real time. It’s particularly helpful for troubleshooting multi-pod, multi-container applications.

<Frame>
  <img alt="The image shows a dashboard interface of &#x22;Kubetail&#x22; displaying log entries with timestamps, sources, regions, and HTTP request details. It features filtering options on the left and log data on the right." />
</Frame>

Package characteristics (Kubetail)

| Field        | Value             |
| ------------ | ----------------- |
| Scope        | cluster-scoped    |
| Values       | none              |
| Entrypoint   | yes (frontend UI) |
| Dependencies | none              |

Kubetail in the Glasskube UI:

<Frame>
  <img alt="The image shows a webpage for installing &#x22;kubetail,&#x22; a web-based log viewer for Kubernetes clusters. It includes version details and an option to enable auto updates." />
</Frame>

Quickly list available packages and installation state with the Glasskube CLI:

```plaintext theme={null}
→ ~ glasskube list
PACKAGENAME   NAMESPACE   NAME                       VERSION   AUTO-UPDATE   REPOSITORY   STATUS
---------------------------------------------------------------------------------------------
quickwit      glasskube   -                          -         -             -             Not installed
...
kubetail                   glasskube   -         -                  Not installed
kube-prometheus-stack      glasskube   -         -                  Not installed
...
```

Install Kubetail via the Glasskube CLI:

```bash theme={null}
glasskube install kubetail
```

Example interactive prompts you may see:

```plaintext theme={null}
