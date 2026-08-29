# Expected output:
# alertmanagerconfig.monitoring.coreos.com/alert-config created
```

Verify the resource exists:

```bash theme={null}
kubectl get alertmanagerconfig
# NAME          AGE
# alert-config  17s
```

## Verify the Alertmanager configuration in the UI

Port-forward to the Alertmanager service and inspect the configuration via the status page:

1. Find the Alertmanager service (commonly `alertmanager-operated`):

```bash theme={null}
kubectl get svc
```

2. Port-forward to 9093:

```bash theme={null}
kubectl port-forward service/alertmanager-operated 9093:9093
```

3. Open [http://localhost:9093/](http://localhost:9093/) in your browser and inspect the “Status -> Configuration” page. You should see your webhook receiver and routing as part of the Alertmanager configuration generated from your AlertmanagerConfig CRD.

## Troubleshooting tips

* If you see no AlertmanagerConfig objects in the Alertmanager UI but they exist in Kubernetes, re-check that:
  * The Helm chart `alertmanagerConfigSelector` matches the labels on your AlertmanagerConfig objects.
  * If you used namespace selectors, ensure `alertmanagerConfigNamespaceSelector` is set appropriately.
* Use `kubectl get alertmanagers.monitoring.coreos.com -o yaml` to inspect the Alertmanager CRD instance spec and verify selectors.
* Review the operator logs (Prometheus Operator) for errors about parsing AlertmanagerConfig objects.

Useful references:

* kube-prometheus-stack Helm chart: [https://github.com/prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts)
* Prometheus Operator AlertmanagerConfig CRD: [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
* Kubernetes basics: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/3310a7e3-7f20-47ef-a2cc-77babda5196a" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/bb958f66-38c3-41ed-ae2f-7a4ee96c4d66/lesson/0cf3e9ef-4c72-45ec-b382-12275b356795" />
</CardGroup>


# Connecting To Prometheus

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Monitoring-Kubernetes/Connecting-To-Prometheus/page

Guide for accessing and exposing a Prometheus server in Kubernetes, covering service inspection, port-forward, NodePort, LoadBalancer, Ingress, and security best practices.

This guide explains how to access the Prometheus server running inside your Kubernetes cluster, including quick diagnostic commands and common access methods (temporary and production-ready). Follow the sequence below to inspect the service, confirm its configuration, and choose an access strategy.

## Inspect the Prometheus services

Start by listing services in the cluster to find the Prometheus-related services and their types:

```bash theme={null}
kubectl get service
NAME                                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                        AGE
alertmanager-operated                        ClusterIP   None             <none>        9093/TCP,9094/TCP,9094/UDP     11h
kubernetes                                   ClusterIP   10.100.0.1       <none>        443/TCP                        4d5h
prometheus-grafana                           ClusterIP   10.100.235.247   <none>        80/TCP                         11h
prometheus-kube-prometheus-alertmanager      ClusterIP   10.100.53.114    <none>        9093/TCP                       11h
prometheus-kube-prometheus-operator          ClusterIP   10.100.196.32    <none>        443/TCP                        11h
prometheus-kube-prometheus-prometheus        ClusterIP   10.100.54.169    <none>        9090/TCP                       11h
prometheus-kube-state-metrics                ClusterIP   10.100.133.149   <none>        8080/TCP                       11h
prometheus-operated                          ClusterIP   10.100.248.61    <none>        9100/TCP                       11h
prometheus-prometheus-node-exporter          ClusterIP   10.100.249.161   <none>        9100/TCP                       11h
```

Note the `TYPE` column — in this example the Prometheus server is exposed via a `ClusterIP` service (`prometheus-kube-prometheus-prometheus`), which by default is accessible only from within the cluster.

<Callout icon="lightbulb">
  If you are running commands in a specific namespace other than `default`, add `-n <namespace>` to the `kubectl` commands above. For example: `kubectl get service -n monitoring`.
</Callout>

## Inspect the service YAML

Export the service YAML to confirm its configured ports, selectors, and `type`:

```bash theme={null}
kubectl get service prometheus-kube-prometheus-prometheus -o yaml > service.yaml
```

Example excerpt showing the key sections:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  annotations:
    meta.helm.sh/release-name: prometheus
    meta.helm.sh/release-namespace: default
  labels:
    app: kube-prometheus-stack-prometheus
    app.kubernetes.io/instance: prometheus
spec:
  clusterIP: 10.100.54.169
  ports:
    - name: http-web
      port: 9090
      protocol: TCP
      targetPort: 9090
  selector:
    app.kubernetes.io/name: prometheus
    prometheus: prometheus-kube-prometheus-prometheus
  type: ClusterIP
```

The `type: ClusterIP` confirms the service is internal-only.

## How to connect to Prometheus (options)

Choose one of the following access methods depending on your needs. Summary below:

| Method                   | When to use                             | Pros                               | Cons                                              | Example command(s)                                                                                                        |
| ------------------------ | --------------------------------------- | ---------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Port-forward (temporary) | Quick local access for debugging/demos  | Fast, no cluster config changes    | Not suitable for production; single-user          | `kubectl port-forward <pod-name> 9090:9090` or `kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090` |
| NodePort                 | Quick cluster-wide access from node IPs | Simple, exposes on node port       | Requires opening node port; not cloud LB-managed  | `kubectl edit svc prometheus-kube-prometheus-prometheus` → set `type: NodePort`                                           |
| LoadBalancer             | Production-ready in cloud environments  | Cloud LB + external IP             | Depends on cloud provider; may incur cost         | `kubectl edit svc prometheus-kube-prometheus-prometheus` → set `type: LoadBalancer`                                       |
| Ingress                  | Route via domain/host with TLS          | Clean host-based routing and certs | Requires Ingress controller and additional config | Create Ingress resource that targets the service                                                                          |

Links and references:

* Kubernetes Service types: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
* kubectl port-forward: [https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)

<Callout icon="warning">
  Exposing Prometheus directly to the Internet can reveal sensitive metric data. When enabling external access, use authentication, TLS, and network restrictions (Ingress with auth, or firewall rules).
</Callout>

## Quick demo — Port-forward to verify the UI

For a short demo or verification you can port-forward the service (or a pod) to your localhost. This does not change the cluster configuration and is temporary.

1. List pods to find the Prometheus pod name (or use the service name for `kubectl port-forward svc/...`):

```bash theme={null}
kubectl get pods -l app.kubernetes.io/name=prometheus
```

2. Port-forward the Prometheus pod (or service) to localhost 9090:

```bash theme={null}
