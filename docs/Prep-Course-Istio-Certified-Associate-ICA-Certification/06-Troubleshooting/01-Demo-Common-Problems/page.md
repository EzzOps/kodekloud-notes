# Demo Common Problems

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Troubleshooting/Demo-Common-Problems/page

Troubleshooting guide for common Istio issues including sidecar injection, mTLS, VirtualService routing, and Gateway configuration with symptoms, diagnosis steps, root causes, and fixes.

This article walks through common Istio troubleshooting scenarios you may encounter on exams or in production. For each scenario you'll find the symptom, step-by-step investigation, root cause analysis, and the recommended fix. Examples use a cluster with these namespaces: `alpha`, `beta`, `charlie`, `delta`, and `istio-system`.

Quick navigation:

* Scenario 1 — Cross-namespace call failing with connection reset (mTLS / sidecar injection)
* Scenario 2 — Pod in an injection-enabled namespace is missing sidecar
* Scenario 3 — VirtualService routes to wrong host/port causing 503
* Scenario 4 — Gateway / External access issues (selector mismatch and missing gateway/hosts in VirtualService)

Summary checklist (use this as a quick reference when troubleshooting Istio):

| Area                      | Common symptoms                         | Quick validation                                                                      |
| ------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------- |
| Sidecar injection         | Pods 1/1 (missing istio-proxy)          | `kubectl get pods -n <ns>` and `kubectl get ns --show-labels`                         |
| mTLS / PeerAuthentication | Connection reset / TLS handshake errors | `kubectl get peerauthentications.security.istio.io -n istio-system -o yaml`           |
| VirtualService routing    | 503 from Envoy                          | `kubectl get virtualservice -n <ns> -o yaml` and verify service FQDN and port         |
| Gateway / Ingress         | Connection refused or 404 from external | `kubectl get gateway -n <ns> -o yaml` and match `spec.selector` to ingress pod labels |

References:

* [Istio Documentation](https://istio.io/latest/docs/)
* [Istioctl analyze](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/)

***

## Scenario 1 — Cross-namespace call failing with connection reset (mTLS / sidecar injection)

Symptom: A pod in namespace `charlie` fails to curl `helloworld` in `alpha` and receives a connection reset:

```bash theme={null}
