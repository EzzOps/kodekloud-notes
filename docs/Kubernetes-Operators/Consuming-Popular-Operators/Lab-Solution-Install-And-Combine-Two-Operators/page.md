# Show keys (base64-encoded)
$ kubectl get secret webapp-tls-cert -o yaml

# Decode the certificate
$ kubectl get secret webapp-tls-cert -o jsonpath='{.data.tls\.crt}' | base64 --decode
```

## Quick reference: resources and use cases

| Resource Type              | Purpose                                                                         | Example                              |
| -------------------------- | ------------------------------------------------------------------------------- | ------------------------------------ |
| Issuer / ClusterIssuer     | Defines how certificates are signed (self-signed, ACME, CA, etc.)               | `kubectl apply -f issuer.yaml`       |
| Certificate                | Requests a certificate; tells cert-manager to write a Secret                    | `kubectl apply -f certificate.yaml`  |
| Secret (kubernetes.io/tls) | Stores `tls.crt`, `tls.key`, and optionally `ca.crt` for workloads or Ingresses | `kubectl get secret webapp-tls-cert` |

## What cert-manager automates

* Private key generation
* Creating CertificateRequest objects
* Submitting CSR to the chosen Issuer
* Storing signed certificate and key in a Secret
* Automatic renewal before expiry (operator reconciles resources)

This pattern — "custom resources in, operator-managed result out" — avoids writing controller logic and leverages the operator model in Kubernetes.

## References

* cert-manager documentation: [https://cert-manager.io/docs/](https://cert-manager.io/docs/)
* cert-manager GitHub releases: [https://github.com/cert-manager/cert-manager/releases](https://github.com/cert-manager/cert-manager/releases)
* Learn by Doing: AIOps Foundations - Intelligent Monitoring With Prometheus & Grafana: [https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana](https://learn.kodekloud.com/user/courses/aiops-foundations-intelligent-monitoring-with-prometheus-grafana)

That completes an end-to-end cert-manager flow: Issuer + Certificate in, TLS Secret out, and renewal handled by the operator.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/b5e6237b-c98e-4357-b26a-f18c583af395/lesson/49964cfd-04ff-4cab-aa04-3e357dc1d20f" />
</CardGroup>


# Lab Solution Install And Combine Two Operators

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Consuming-Popular-Operators/Lab-Solution-Install-And-Combine-Two-Operators/page

Explains installing cert-manager and Prometheus Operator in one namespace, creating their CRs, and verifying each operator reconciles only its own resources.

This lesson demonstrates how to run two independent Kubernetes operators in the same namespace without mixing ownership of their custom resources. You will install or verify two controllers, create the custom resources each operator manages, and confirm that each operator reconciles only its own resources.

* cert-manager: manages certificate lifecycle (Issuer, Certificate) and produces TLS Secrets.
* Prometheus Operator: manages monitoring lifecycle (ServiceMonitor, Prometheus) and generates the Prometheus workload.

These cert-manager components work together: the controller reconciles Certificate resources, the webhook validates cert-manager API requests, and cainjector injects CA trust data into Kubernetes resources.

<Callout icon="lightbulb">
  Operators claim ownership only of the custom resources defined by their CRDs. Co-locating resources in the same Kubernetes namespace is useful for visibility, but it does not imply shared ownership or control.
</Callout>

## Prerequisites and overview

1. Confirm cert-manager and Prometheus Operator deployments are running.
2. Create a single namespace `combined` to host the application-facing custom resources (the operators themselves run in their own namespaces).
3. Apply cert-manager resources (Issuer + Certificate) and verify a TLS Secret is produced.
4. Apply Prometheus resources (Deployment, Service, ServiceMonitor, Prometheus) and verify the operator generates the Prometheus StatefulSet.
5. Validate that each operator only reconciles its own resources and verify the label selector match between Prometheus and the ServiceMonitor.

## Verify controllers and create namespace

Confirm both operator deployments are available, then create the `combined` namespace:

```bash theme={null}
