# Prometheus Configuration

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Cloud-Native-Observability/Prometheus-Configuration/page

This guide explains how to configure a Prometheus server to scrape metrics from one or multiple nodes.

This guide explains how to configure a Prometheus server to scrape metrics from one or multiple nodes. After installing Prometheus and setting up your nodes with Node Exporters to expose metrics, you must explicitly configure Prometheus to discover and scrape these targets using its pull-based model.

The configuration is maintained in the prometheus.yaml file, typically found in the /etc/prometheus directory.

Below is a basic Prometheus configuration example:

```yaml theme={null}
