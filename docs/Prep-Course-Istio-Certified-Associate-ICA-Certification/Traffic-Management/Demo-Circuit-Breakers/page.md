# Demo Circuit Breakers

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Circuit-Breakers/page

Guide to configuring Istio circuit breakers with DestinationRule and VirtualService, deploying an echo app, using Fortio load tests and inspecting Envoy sidecar stats

In this lesson you'll configure an Istio circuit breaker by deploying a simple echo application, a Fortio load tester, and then applying a VirtualService + DestinationRule that implements connection pool limits and outlier detection. You will generate load to observe how Envoy enforces the circuit breaker and learn how to inspect the sidecar proxy stats.

Key terms: Istio circuit breaker, DestinationRule, connectionPool, outlierDetection, Envoy, Fortio.

## 1. Verify the namespace is Istio-injection enabled

Confirm your target namespace has the `istio-injection=enabled` label. If it is not labeled, add the label and re-deploy your workloads so sidecars are injected.

Example to check labels:

```bash theme={null}
kubectl get ns --show-labels
