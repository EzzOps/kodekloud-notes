# Demo Authorizaton

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Securing-Workloads/Demo-Authorizaton/page

Demonstrates Istio authorization by enforcing mTLS and using AuthorizationPolicy examples to allow or deny traffic, illustrating scoping, methods and paths, and DENY precedence.

This lesson demonstrates authorization in Istio: after authentication (mTLS) establishes identity, AuthorizationPolicy resources determine what authenticated workloads are allowed to do. We'll walk through a set of hands-on examples that illustrate:

* Enforcing mTLS cluster-wide (PeerAuthentication)
* Creating AuthorizationPolicy resources to ALLOW or DENY traffic
* How rule scope (namespace, selector, methods, paths) affects behavior
* The precedence of DENY over ALLOW

Prerequisites: an Istio-enabled cluster with `istio-system` installed and working control plane.

***

## 1. Deploy example workloads

Apply the httpbin sample used throughout this lesson:

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.com/istio/istio/refs/heads/master/samples/httpbin/httpbin.yaml
