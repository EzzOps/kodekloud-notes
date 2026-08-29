# Verify installation
cmctl check api

# Inspect Issuer or Certificate resources
cmctl inspect issuer <name>

# Trigger a certificate renewal
cmctl renew <certificate-name>
```

***

## Let’s Encrypt Overview

Let’s Encrypt is a free, automated, and open certificate authority (CA) that uses the ACME protocol to issue SSL/TLS certificates. It empowers Kubernetes users to secure applications without manual certificate provisioning.

![The image is an overview of Let's Encrypt, highlighting features such as free usage, standard and wildcard certificates valid for 90 days, production and staging usage, and programmatic access.](https://kodekloud.com/kk-media/image/upload/v1752880396/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cert-Manager-and-Lets-Encrypt-Overview/letsencrypt-overview-features-certificates.jpg)

Key points about Let’s Encrypt:

* Certificates are valid for 90 days.
* Offers **Production** and **Staging** endpoints.
* ACME challenges: HTTP-01 or DNS-01.
* Publicly logged for transparency.

Table: Let’s Encrypt Endpoints

| Environment | ACME Endpoint                                                                                                    | Use Case                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Staging     | [https://acme-staging-v02.api.letsencrypt.org/directory](https://acme-staging-v02.api.letsencrypt.org/directory) | Testing automation workflows |
| Production  | [https://acme-v02.api.letsencrypt.org/directory](https://acme-v02.api.letsencrypt.org/directory)                 | Live environments            |

The ACME flow:

1. Client generates a key pair and creates a `CertificateRequest`.
2. Let’s Encrypt returns an HTTP-01 or DNS-01 challenge.
3. Client fulfills the challenge by serving a token or adding a DNS record.
4. After validation, Let’s Encrypt issues the certificate.
5. Client fetches and stores the certificate in Kubernetes.

![The image is a flowchart illustrating the process of how Let's Encrypt works, including steps like client request, challenge, validation, certificate issuance, and renewal. It emphasizes "Public Trust by Transparency."](https://kodekloud.com/kk-media/image/upload/v1752880397/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cert-Manager-and-Lets-Encrypt-Overview/lets-encrypt-flowchart-process-illustration.jpg)

***

## Integrating cert-manager with Let’s Encrypt

To use Let’s Encrypt as your certificate authority, define an Issuer or ClusterIssuer in cert-manager:

![The image is a diagram showing the relationship between Cert-Manager and Let's Encrypt, with two issuers: "letsencrypt-staging" and "letsencrypt-prod," connected to Cert-Manager.](https://kodekloud.com/kk-media/image/upload/v1752880398/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cert-Manager-and-Lets-Encrypt-Overview/cert-manager-letsencrypt-issuers-diagram.jpg)

### Example: Staging Issuer

```yaml theme={null}
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-staging
    solvers:
    - http01:
        ingress:
          class: nginx
```

> **lightbulb** When moving to production, update the `server` URL to the production ACME endpoint and rename secrets accordingly.

***

### Configuring Kubernetes Ingress

Annotate your Ingress resource to reference the Issuer and specify TLS settings:

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    cert-manager.io/issuer: letsencrypt-staging
spec:
  tls:
    - hosts:
        - example.com
      secretName: web-tls
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 80
```

When this Ingress is applied, cert-manager handles ACME challenges, retrieves the certificate, and stores it in the `web-tls` Secret. Certificates are renewed automatically before expiration.

***

## Links and References

* [cert-manager Documentation](https://cert-manager.io/docs/)
* [Let’s Encrypt ACME Protocol](https://letsencrypt.org/docs/)
* [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* [ACME RFC (RFC 8555)](https://datatracker.ietf.org/doc/html/rfc8555)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-networking/module/5a70ab6c-2094-4bf2-9f49-e441919fc8c2/lesson/c8cd2c23-8d3f-4497-99c1-710836bebaf2)


# Cilium Hubble Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Networking-Deep-Dive/Network-Security/Cilium-Hubble-Overview/page

Cilium Hubble enhances network observability, troubleshooting, and security for Kubernetes clusters through eBPF, offering metrics, UI/CLI tools, and integrations with Prometheus and Grafana.

Cilium Hubble extends Cilium’s eBPF datapath to deliver unparalleled network observability, troubleshooting, and security enforcement for Kubernetes clusters. In this guide, we’ll cover Hubble’s architecture, built-in metrics, UI/CLI tools, and how to integrate with Prometheus and Grafana.

Hubble components:

* **eBPF datapath** on each node for flow and event capture
* **Relay** to aggregate data across nodes
* **Integrations** with Prometheus (metrics), Grafana (dashboards, service maps), and Hubble UI/CLI for interactive inspection

![The image is a diagram explaining Hubble, a tool built on Cilium (eBPF), highlighting its features like network observation, troubleshooting, and monitoring, with components like Grafana, Prometheus, and Hubble UI/CLI. It shows nodes with pods and integrations for metrics, service maps, and flow inspection.](https://kodekloud.com/kk-media/image/upload/v1752880399/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Hubble-Overview/hubble-cilium-ebpf-diagram-features.jpg)

## Built-in Metrics for Prometheus

Hubble exports metrics in the [Prometheus OpenMetrics format](https://prometheus.io/docs/instrumenting/exposition_formats/), making it simple to monitor network health and trigger alerts on key events:

| Metric Category   | Tracks                                          | Use Case                                    |
| ----------------- | ----------------------------------------------- | ------------------------------------------- |
| dns               | DNS queries, failures, latencies                | Alert on high DNS failure rate              |
| drop              | Packet drops by policy or error                 | Identify unintended policy blocks           |
| tcp               | TCP connections, retransmissions, resets        | Detect connection instability               |
| flow              | Flow counts, throughput, duration               | Baseline traffic trends                     |
| port-distribution | Top port usage across services                  | Spot unexpected open ports                  |
| icmp              | ICMP echo requests and replies                  | Monitor ping flood or unreachable hosts     |
| httpV2            | HTTP/2 metrics with exemplars and label context | Trace request latencies with context labels |

> **lightbulb** Enable only the metrics you need to reduce data volume and improve query performance.

### Enabling Hubble Metrics via Helm

When installing or upgrading Cilium with Helm, you can enable Hubble and Prometheus integration in one step:

```bash theme={null}
helm upgrade cilium cilium/cilium --version CILIUM_VERSION \
  --namespace kube-system \
  --reuse-values \
  --set hubble.enabled=true \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true \
  --set hubble.metrics.enableOpenMetrics=true \
  --set prometheus.enabled=true \
  --set operator.prometheus.enabled=true \
  --set hubble.metrics.enabled="{dns,drop,tcp,flow,port-distribution,icmp,httpV2:exemplar=true;labelsContext=source_ip\,source_namespace\,source_workload\,destination_ip\,destination_namespace\,destination_workload\,traffic_direction}"
```

## Hubble UI and CLI

Hubble offers both a web-based UI and a scriptable CLI, providing deep visibility into service interactions, network flows, and security policy verdicts.

![The image outlines Hubble's offerings, including Built-in Metrics for Prometheus, Hubble UI, and Hubble CLI, each with specific features related to metrics, service dependencies, network flows, protocols, filtering, and security information.](https://kodekloud.com/kk-media/image/upload/v1752880400/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Hubble-Overview/hubble-offerings-metrics-ui-cli.jpg)

### Hubble UI

The Hubble UI delivers interactive dashboards and service maps:

* **Service Dependency Map**\
  Visualize inter-service communication to spot bottlenecks or misconfigurations.
* **Flow Table**\
  Inspect individual network flows with source/destination, protocol details, performance metrics, and policy verdicts.
* **Security Events**\
  Review blocked connections, policy violations, and external access attempts.

Example service dependency graph:

![The image is a diagram from the Hubble UI showing a network of interconnected services, including "recruiter," "jobposting," "crawler," "coreapi," "loader," "elasticsearch," "kafka," and "zookeeper." Each service is represented with its respective ports and protocols.](https://kodekloud.com/kk-media/image/upload/v1752880401/notes-assets/images/Kubernetes-Networking-Deep-Dive-Cilium-Hubble-Overview/hubble-ui-network-services-diagram.jpg)

> **triangle-alert** Avoid exposing the Hubble UI publicly without proper authentication. Use port-forwarding or an ingress with strong access controls.

#### Launching Hubble UI Locally

Forward the UI port to your workstation:

```bash theme={null}
cilium hubble ui
