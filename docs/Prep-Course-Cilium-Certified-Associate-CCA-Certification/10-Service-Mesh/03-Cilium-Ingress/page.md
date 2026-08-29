# Cilium Ingress

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Service-Mesh/Cilium-Ingress/page

Cilium's Kubernetes Ingress using eBPF for L3 L4 routing and Envoy for selective L7, with Helm enablement, load balancer modes, Gateway API support and troubleshooting tips.

This article explains how Cilium implements Ingress in Kubernetes, comparing its approach with traditional controllers and showing how to enable and configure Cilium's Ingress features via Helm. Cilium combines eBPF-based kernel integration for high-performance L3/L4 routing with Envoy for selective L7 and policy enforcement. It also supports the Kubernetes Gateway API (overview only; Gateway API specifics are out of scope here).

<Frame>
  <img alt="A slide titled &#x22;Cilium Ingress&#x22; showing a multicolored hexagon cluster on the left funneling to two Kubernetes icons on the right labeled &#x22;gateway api&#x22; and &#x22;Ingress.&#x22; It illustrates Cilium routing or integration with the Gateway API and Ingress." />
</Frame>

Key advantages of Cilium Ingress

* Programs the Linux kernel datapath with eBPF for most routing and load-balancing work, avoiding the need for a separate Ingress-controller pod for L3/L4.
* Uses Envoy only where required: L7 processing, TLS termination (if configured), and policy enforcement.
* Supports both traditional Kubernetes Ingress and the Gateway API for modern traffic routing.

> **lightbulb** When you enable Cilium's ingress controller (ingressController.enabled = true), Cilium automatically configures Envoy where needed. eBPF handles most routing and load-balancing tasks for better performance and lower resource usage.

## Enabling Cilium Ingress (Helm values)

To enable Cilium Ingress in a Helm-managed installation, set up the NodePort service implementation and enable the ingress controller in your values.yaml. You can also make Cilium the default Ingress controller and choose a load balancer mode (dedicated or shared).

values.yaml (example)

```yaml theme={null}
nodePort:
  # Enable the Cilium NodePort service implementation.
  enabled: true

ingressController:
  # Enable cilium ingress controller.
  # This will automatically set enable-envoy-config as well.
  enabled: true

  # Set cilium ingress controller to be the default ingress controller.
  # This will let cilium route Ingress entries without an ingressClassName set.
  default: true

  # Default ingress load balancer mode: "dedicated" or "shared"
  # Can also be set via annotation: ingress.cilium.io/loadbalancer-mode: dedicated
  loadbalancerMode: dedicated
```

Apply and reload Cilium components

```bash theme={null}
helm upgrade cilium cilium/cilium -n kube-system -f values.yaml
