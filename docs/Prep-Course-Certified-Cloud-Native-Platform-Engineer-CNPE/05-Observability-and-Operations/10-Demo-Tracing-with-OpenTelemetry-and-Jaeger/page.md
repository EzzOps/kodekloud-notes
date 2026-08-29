# pods
NAME                                                      READY   STATUS    RESTARTS   AGE
kube-prometheus-stack-grafana-84cf9bcd57-9vm7h            2/2     Running   0          12m
kube-prometheus-stack-kube-state-metrics-567d4944f-1fpz   1/1     Running   0          12m
kube-prometheus-stack-operator-5d9b6cb8d-8hqhx             1/1     Running   0          12m
kube-prometheus-stack-prometheus-node-exporter-5r5x7      2/2     Running   0          12m
prometheus-kube-prometheus-stack-prometheus-0              2/2     Running   0          12m

# services
NAME                                                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
kube-prometheus-stack-grafana                               NodePort    172.20.151.255  <none>        80:30080/TCP
kube-prometheus-stack-kube-state-metrics                    ClusterIP   172.20.6.143    <none>        8080/TCP
kube-prometheus-stack-operator                              ClusterIP   172.20.149.171  <none>        443/TCP
kube-prometheus-stack-prometheus                            NodePort    172.20.50.36    <none>        9090:30900/TCP,8080:30392/TCP
kube-prometheus-stack-prometheus-node-exporter              ClusterIP   172.20.93.180   <none>        9100/TCP
prometheus-operated                                         ClusterIP   None            <none>        9090/TCP
```

Quick summary of important endpoints

| Component                | Access pattern                                          | Example                                                        |
| ------------------------ | ------------------------------------------------------- | -------------------------------------------------------------- |
| Prometheus (cluster DNS) | `http://<service>.<namespace>.svc.cluster.local:<port>` | `http://prometheus-operated.monitoring.svc.cluster.local:9090` |
| Prometheus (NodePort)    | Node external access                                    | `NodePort 30900`                                               |
| Grafana (NodePort)       | Node external access                                    | `NodePort 30080`                                               |

Open Grafana and log in
Use the Grafana NodePort (or your configured ingress) to reach the Grafana UI and sign in with the credentials for your setup.

<Frame>
  <img alt="The image shows a Grafana login screen with fields for email or username and password against a gradient background. The &#x22;Log in&#x22; button is prominently displayed below the input fields." />
</Frame>

After login you will arrive at Grafana’s home/dashboard page where you can add data sources and create dashboards.

<Frame>
  <img alt="The image shows the Grafana dashboard interface, featuring a welcome message and options for setting up data sources and creating dashboards. There are also links for help and recent blog updates." />
</Frame>

Add Prometheus as a data source

1. Click Add your first data source (or Add data source).
2. From the list, choose Prometheus.

<Frame>
  <img alt="The image shows a Grafana interface with options to add different data sources, including Prometheus, Graphite, InfluxDB, and others. It is organized under categories like time series databases and logging & document databases." />
</Frame>

Configure the Prometheus connection

* Keep the default Name (or give it a descriptive name such as `prometheus-monitoring`).
* For the URL, point Grafana to the in-cluster Prometheus service. Use the full service DNS name and port (including scheme):

```bash theme={null}
http://prometheus-operated.monitoring.svc.cluster.local:9090
```

This follows the standard in-cluster DNS pattern:
`service-name.namespace.svc.cluster.local:port`

It will work regardless of the namespace where Grafana runs, provided DNS resolves and any network policies allow access.

<Frame>
  <img alt="The image shows the Grafana interface for configuring a Prometheus data source, including fields for connection settings and authentication methods." />
</Frame>

Optional settings

* Toggle “Default” if you want this Prometheus instance to be the default for new dashboards.
* Leave authentication, timeouts, and other advanced settings at their defaults unless you require custom configuration (e.g., TLS, headers, or proxy).

Save and test
Click Save & Test. On success Grafana will show a green confirmation that it was able to query the Prometheus API.

<Frame>
  <img alt="The image shows a Grafana data source configuration screen for Prometheus, with various settings toggles and input fields for performance and connection parameters. There's a notification indicating successful querying of the Prometheus API." />
</Frame>

> **lightbulb** If Save & Test fails, verify the following:

  * The service DNS and port are correct: `http://prometheus-operated.monitoring.svc.cluster.local:9090`.
  * Prometheus pods are running in the `monitoring` namespace: `kubectl get pods -n monitoring`.
  * NetworkPolicies, firewall rules, or cluster network ACLs are not preventing in-cluster requests from Grafana to Prometheus.

Next steps

* Create dashboards and panels that query Prometheus using PromQL.
* Import prebuilt Grafana dashboards for Kubernetes or your applications.
* Secure access to Grafana (authentication, RBAC, and TLS) before exposing it externally.

Links and references

* Grafana documentation: [https://grafana.com/docs/](https://grafana.com/docs/)
* Prometheus documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)
* Kubernetes DNS and Services: [https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/9bd090c8-8d99-4742-b50c-ae63e516e6b9/lesson/b380cd38-72e3-4794-8486-ab7f52739839)


# Demo Tracing with OpenTelemetry and Jaeger

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Observability-and-Operations/Demo-Tracing-with-OpenTelemetry-and-Jaeger/page

Guide to enabling OpenTelemetry tracing for a Kubernetes frontend, exporting traces to Jaeger via OTLP, configuring environment variables, viewing traces, and troubleshooting common issues.

Metrics tell you something is slow. Logs tell you what happened in a single service. But when a request traverses multiple microservices and latency spikes, how do you find the specific service causing the delay? Distributed tracing solves this.

OpenTelemetry (OTel) is the vendor-neutral instrumentation standard that applications use to emit traces. Jaeger is a popular tracing backend that receives, stores, indexes, and visualizes those traces. In short: OpenTelemetry controls how traces are generated and exported; Jaeger handles collection, indexing, and visualization.

In this guide you'll enable tracing for a missing service (the frontend) and inspect traces in the Jaeger UI.

## What to check first: cluster workloads and Jaeger

Confirm Jaeger and your microservices are running:

```bash theme={null}
