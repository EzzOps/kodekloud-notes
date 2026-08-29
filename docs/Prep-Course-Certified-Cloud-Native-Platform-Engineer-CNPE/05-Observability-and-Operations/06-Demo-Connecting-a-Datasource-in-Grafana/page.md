# Demo Connecting a Datasource in Grafana

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Observability-and-Operations/Demo-Connecting-a-Datasource-in-Grafana/page

Guide showing how to configure Grafana to connect to an in-cluster Prometheus datasource, verify services, save and test the connection, and troubleshoot common issues

Grafana does not store metrics itself; it visualizes metrics collected and stored elsewhere. To visualize metrics in Grafana you must configure a datasource that points to where those metrics live. In this demo we connect Grafana to a Prometheus instance running inside the cluster.

Prerequisites

* A Prometheus stack is installed in the `monitoring` namespace (kube-prometheus-stack or similar).
* Grafana is running and reachable (exposed via NodePort in this environment).
* `kubectl` configured to access the cluster.

Verify pods and services

Run the following to confirm the Prometheus and Grafana components are running:

```bash theme={null}
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

A sample output looks like:

```bash theme={null}
