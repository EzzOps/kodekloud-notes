# Introduction to Gateway API 2025 Updates

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Networking/Introduction-to-Gateway-API-2025-Updates/page

This article introduces the Gateway API and its updates, addressing Ingress limitations and enhancing traffic management capabilities in Kubernetes.

In this article, we introduce the Gateway API and explain how it addresses the challenges posed by the traditional Ingress resource. Previously, when using Ingress, multiple teams or organizations sharing a single Ingress resource faced coordination challenges. For instance, if team A manages a web service and team B manages a video service, they would need to coordinate their changes on one Ingress resource. This multi-tenancy issue is a significant limitation of Ingress, which can only be managed by one team at a time.

## Limitations of Ingress

Consider the basic Ingress configuration below, which routes traffic based on host names:

```yaml theme={null}
