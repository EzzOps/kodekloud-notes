# Example fragments you may see in exam questions
principals: ["admin", "dev"]
namespaces: ["prod", "test"]
notIpBlocks: ["203.0.113.4"]
```

<Callout icon="warning">
  Exam tip: Understand how `from`, `to`, and `when` combine (OR vs AND), know the difference between L3/L4 NetworkPolicy and L7 AuthorizationPolicy, and be familiar with matching by `selector`, `principals`, and JWT claim keys such as `request.auth.claims[iss]`.
</Callout>

Authorization policies are more expressive than peer authentication (mTLS) alone—invest time in hands-on practice and review the [Istio AuthorizationPolicy reference](https://istio.io/latest/docs/reference/config/security/authorization-policy/) for all available fields.

## Links and references

* [Istio AuthorizationPolicy reference](https://istio.io/latest/docs/reference/config/security/authorization-policy/)
* [Kubernetes NetworkPolicy concepts](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
* [Envoy proxy docs](https://www.envoyproxy.io/docs/)

That's the theory — next up: a hands-on demo configuring policies and testing enforcement.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/17ba1cac-61f4-48b6-b354-c2c735f5791d/lesson/bb5f68af-8211-48ed-b2fe-a89b5e9cf123" />
</CardGroup>


# Demo Ambient Mode Securing Workloads

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Securing-Workloads/Demo-Ambient-Mode-Securing-Workloads/page

A hands on demo showing Istio Ambient mode security, enforcing mTLS, waypoint based L7 authorization, and how to configure AuthorizationPolicy and namespaces for secure workload communication

This lesson demonstrates how Istio Ambient mode interacts with workload security (mTLS via PeerAuthentication and L3/L4 vs L7 AuthorizationPolicy enforcement). Ambient mode behavior is similar to traditional sidecar-mode flows but introduces important differences—most notably the waypoint proxy that enforces L7 policies. This guide is a hands-on demo for learning and experimentation.

Prerequisites: a running Kubernetes cluster with Istio installed and Ambient mode enabled.

Table of contents

* Verify Istio control plane and ztunnel
* Create a test curl pod
* Deploy HelloWorld into the `hello` namespace
* Enforce mTLS globally with PeerAuthentication
* AuthorizationPolicy differences: L3/L4 vs L7 in Ambient mode
* Configure the waypoint proxy for the `hello` namespace
* AuthorizationPolicy for Ambient mode (targetRefs + principals)
* Validate with a non-allowed namespace
* Notes about service accounts and principals
* Cleanup
* Summary
* Links and references

## Verify Istio control-plane and ztunnel

Confirm Istio control-plane components are running (ztunnel, istiod, CNI):

```bash theme={null}
kubectl get pods -n istio-system
