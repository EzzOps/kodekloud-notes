# View node metrics
kubectl top nodes

# View pod metrics in a namespace
kubectl top pods -n <namespace>
```

## Advanced Open-Source Monitoring with Prometheus and Grafana

For comprehensive observability, combine Prometheus for metrics scraping/storage with Grafana for visualization and alerting.

![The image is a diagram explaining Kubernetes monitoring, detailing the monitoring of clusters, nodes, deployments, pods, and applications, and listing tools like Prometheus and Grafana.](https://kodekloud.com/kk-media/image/upload/v1752873813/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Kubernetes-Monitoring-Basics/kubernetes-monitoring-diagram-prometheus-grafana.jpg)

Follow these steps to deploy:

1. Add and update Helm repos:
   ```bash theme={null}
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

2. Install Prometheus:
   ```bash theme={null}
   helm install prometheus prometheus-community/prometheus \
     --namespace monitoring --create-namespace
   ```

3. Install Grafana:
   ```bash theme={null}
   helm install grafana prometheus-community/kube-grafana \
     --namespace monitoring
   ```

4. Forward ports to access UIs:
   ```bash theme={null}
   # Grafana UI
   kubectl port-forward svc/grafana 3000:80 -n monitoring

   # Prometheus UI
   kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
   ```

> **lightbulb** After first login to Grafana (default credentials `admin/admin`), immediately update the password and configure your data source.

With Prometheus scraping Kubernetes endpoints and Grafana connected:

* Persist historical metrics for capacity planning
* Build custom dashboards to visualize CPU, memory, and application metrics
* Configure alerts in Prometheus Alertmanager to detect anomalies

Thank you for reading this lesson!

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Prometheus Helm Charts](https://github.com/prometheus-community/helm-charts)
* [Grafana Documentation](https://grafana.com/docs/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/ff5071f2-d8f1-47a7-8a8d-746ac865a12b)


# Pod Pod Communication Need for mTLS

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/Kubernetes-Operations-and-Security/Pod-Pod-Communication-Need-for-mTLS/page

This guide explains the risks of unencrypted pod-to-pod traffic and how Istio simplifies end-to-end encryption using mutual TLS.

Securing communication between pods is critical in a microservices architecture. By default, Kubernetes routes traffic in plaintext, exposing sensitive data to network eavesdroppers. This guide explains the risks of unencrypted pod-to-pod traffic and shows how a service mesh—specifically Istio—simplifies end-to-end encryption using mutual TLS (mTLS).

## Table of Contents

* [1. The Risk of Plaintext Pod-to-Pod Traffic](#1-the-risk-of-plaintext-pod-to-pod-traffic)
* [2. Challenges of Embedding TLS in Applications](#2-challenges-of-embedding-tls-in-applications)
* [3. Service Mesh Solution: Istio and mTLS](#3-service-mesh-solution-istio-and-mtls)
* [4. Comparing Approaches](#4-comparing-approaches)
* [5. Next Steps and References](#5-next-steps-and-references)

***

## 1. The Risk of Plaintext Pod-to-Pod Traffic

By default, Pod A sends HTTP requests directly to Pod B over the cluster network. An attacker on the same node—or any compromised network segment—can intercept and read this traffic.

```plaintext theme={null}
Pod A (HTTP)  ───►  Pod B (HTTP)
```

> **triangle-alert** Plaintext HTTP between pods exposes API keys, tokens, and PII to packet sniffers. Always encrypt inter-service traffic in production.

## 2. Challenges of Embedding TLS in Applications

To secure traffic with TLS (HTTPS), every microservice must handle:

* Generating and rotating key pairs
* Securely storing private keys
* Performing TLS handshakes
* Updating certificates upon expiry

This creates significant operational complexity and duplicates effort across teams.

## 3. Service Mesh Solution: Istio and mTLS

A service mesh like Istio offloads TLS responsibilities to sidecar proxies, automating certificate issuance and mTLS handshakes.

### Prerequisites

> **lightbulb** Ensure you have:

  * A running Kubernetes cluster (v1.20+)
  * `kubectl` configured for your cluster
  * Helm (optional) or `istioctl` CLI installed

### Step-by-Step Guide

1. **Install Istio**
   ```bash theme={null}
   istioctl install --set profile=demo -y
   ```

2. **Enable Automatic Sidecar Injection**
   ```bash theme={null}
   kubectl label namespace default istio-injection=enabled
   ```

3. **Deploy Your Applications**\
   Any pod in the `default` namespace now includes an Istio sidecar.

4. **Verify mTLS is Enforced**
   ```bash theme={null}
   istioctl authn tls-check
   ```

When Pod A calls Pod B:

* Pod A’s app → plaintext to Envoy sidecar
* Envoy (Pod A) → performs mTLS handshake → Envoy (Pod B)
* Envoy (Pod B) → decrypts → plaintext to Pod B’s app

![The image illustrates pod-to-pod communication within a Kubernetes node, highlighting security measures and the prevention of an attacker's access.](https://kodekloud.com/kk-media/image/upload/v1752873814/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Pod-Pod-Communication-Need-for-mTLS/kubernetes-pod-communication-security-diagram.jpg)

## 4. Comparing Approaches

| Approach              | TLS Management          | Complexity | Encryption Type |
| --------------------- | ----------------------- | ---------- | --------------- |
| Manual TLS in Service | Developer               | High       | HTTPS           |
| Istio Service Mesh    | Sidecar Proxies (Envoy) | Low        | mTLS            |

## 5. Next Steps and References

We’ll dive deeper into advanced Istio features—custom mTLS policies, certificate rotation, and traffic observability.

## Links and References

* [Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Istio Official Documentation](https://istio.io/latest/docs/)
* [mTLS Explained](https://en.wikipedia.org/wiki/Mutual_authentication)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/fc1733bc-1e9c-4e38-ae86-84e6bd9af04d/lesson/a2729721-3ef1-42ca-835e-d893a744703f)
