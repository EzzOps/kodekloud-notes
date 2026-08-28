# Restart Cilium to pick up config changes
kubectl -n kube-system rollout restart daemonset/cilium
kubectl -n kube-system rollout restart deployment/cilium-operator
```

## Load balancer modes: dedicated vs shared

Cilium supports two modes for provisioning external cloud load balancers for Ingress resources. Choose the mode that fits your isolation, cost, and routing needs.

| Mode      | Description                                                                                                                                         | When to use                                                                   |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| dedicated | Each Ingress resource provisions its own external Load Balancer (e.g., AWS ELB/ALB per Ingress).                                                    | Use when you need strict isolation per Ingress or separate public endpoints.  |
| shared    | Multiple Ingress resources share a single external Load Balancer. Cilium programs forwarding rules so a single LB routes traffic to many Ingresses. | Use to minimize cloud LB count and cost; centralize routing and certificates. |

<Callout icon="warning">
  Using dedicated mode increases the number of cloud load balancers (and cost). Use shared mode to consolidate LB resources, and prefer dedicated only when endpoint isolation or separate LB features are required.
</Callout>

You can also control the LB mode per-Ingress with an annotation:

* ingress.cilium.io/loadbalancer-mode: shared
* ingress.cilium.io/loadbalancer-mode: dedicated

## Example: Minimal Ingress manifest

If you set `ingressController.default: true`, Cilium will claim Ingresses without an ingressClassName. Otherwise, you can explicitly set the Cilium ingress class.

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress1
spec:
  ingressClassName: cilium
  rules:
    - host: app1.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app1-svc
                port:
                  number: 80
```

## Behavior examples

Dedicated mode

* Each Ingress provisions an external LB, so `kubectl get ingress` will show unique addresses per Ingress:

```console theme={null}
$ kubectl get ingress
NAME        CLASS   HOSTS              ADDRESS                                                                                   PORTS   AGE
ingress1    cilium  app1.example.com   a3c7be5e725ce4a62ab7b5deefb2bf20-415562864.us-east-1.elb.amazonaws.com               80      22s
ingress2    cilium  app2.example.com   a732aea6d7c9f482aa4d3029753fb5f3-1501246429.us-east-1.elb.amazonaws.com               80      22s
test        cilium  *                  a96165cf1bb584356859b46890b117ac-685623129.us-east-1.elb.amazonaws.com               80      22s
```

Shared mode

* All Ingress resources present the same external address because a single shared LB is used and Cilium programs routing rules to direct traffic to the correct Ingress backend.

## Verification and troubleshooting tips

* Check Cilium pods and operator in the kube-system namespace to confirm the ingress controller is enabled:
  * kubectl -n kube-system get pods | grep cilium
  * kubectl -n kube-system get deployment cilium-operator
* Validate default controller behavior:
  * Create an Ingress without ingressClassName if `ingressController.default: true` and confirm Cilium has claimed it.
* Change mode per-Ingress via annotation: `ingress.cilium.io/loadbalancer-mode: shared` or `dedicated`.
* Inspect the Envoy configuration (when used) in the Cilium-managed Envoy instances for L7 policy issues.
* Consult logs for cilium-agent and cilium-operator when troubleshooting provisioning or LB interactions.

## References

* [Kubernetes Ingress Concepts](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* [Cilium Documentation — Ingress and Load Balancing](https://docs.cilium.io/en/stable/)
* [Gateway API (overview)](https://gateway-api.sigs.k8s.io/)

This concludes the Cilium Ingress overview. Gateway API integration and advanced Envoy configuration are covered in separate Cilium documentation and guides.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/50bb84d0-61e7-4f73-a51b-7da0e8338438/lesson/f3332407-b4cd-41ed-91da-b2567243ae07" />
</CardGroup>


# Cilium Service Mesh vs Others

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Service-Mesh/Cilium-Service-Mesh-vs-Others/page

Comparison of Cilium’s sidecarless eBPF-based service mesh with traditional sidecar proxies, detailing traffic flow, resource and operational trade-offs, and when to prefer each approach

This lesson compares Cilium’s sidecarless service mesh architecture with the common sidecar-based model used by many service meshes (for example, Istio). It explains how each model directs traffic, the operational trade-offs, and when you might prefer one approach over the other.

Most service meshes implement a sidecar-based model. In Kubernetes, the mesh injects a proxy container (sidecar) into every application pod. Each application pod (for example, a Python or Go service) pairs with a local proxy that intercepts and routes all inbound and outbound application traffic.

<Frame>
  <img alt="A diagram titled &#x22;Service Mesh Implementation — Sidecar&#x22; showing two Kubernetes pods (one with a Python service, one with a Go service), each paired with a &#x22;Service Mesh Proxy&#x22; sidecar, with arrows indicating traffic flowing between the proxies." />
</Frame>

Benefits of the sidecar model:

* Services don’t need to implement mesh features themselves; sidecars provide observability, traffic control, mTLS, retries, circuit-breaking, etc.
* Language-agnostic: applications written in any language benefit from the same network features without changing application code.
* Supports immutable or closed-source applications because features are attached via a proxy, not code changes.

<Frame>
  <img alt="A presentation slide titled &#x22;Service Mesh Implementation – Sidecar&#x22; showing three benefit boxes. The boxes state: services don't need to implement mesh functionality; useful for apps in different languages; and supports immutable third-party applications." />
</Frame>

Trade-offs and downsides of sidecar injection:

* Higher resource usage: a proxy instance runs per pod, increasing CPU and memory consumption cluster-wide.
* Operational complexity: operators must manage proxy configuration for each pod (per-pod sidecars).
* Slower lifecycle and startup complexity: pods may wait for sidecar readiness, introducing potential race conditions.
* Extra network hop: each request typically traverses the application → sidecar → network path, adding latency.

Cilium takes a different approach: a sidecarless model. Instead of running a proxy per pod, Cilium offloads much of the network and security logic to eBPF programs executing in the Linux kernel. This reduces per-pod overhead while providing comparable networking and security capabilities.

Key distinctions:

* eBPF in-kernel processing: Cilium programs operate at L3/L4 (network and transport layers) inside the kernel, allowing efficient packet processing without additional proxies.
* L7 functionality via Envoy: for application-layer (L7) features—HTTP routing, L7-aware telemetry, or protocol-specific filtering—Cilium forwards traffic to Envoy. The crucial difference is that Envoy is deployed as a node-local instance (one Envoy per node), not one per pod. That typically means far fewer Envoy instances across the cluster (e.g., two nodes → two Envoy instances).

Traffic flow differences:

* L3/L4 traffic: handled directly by eBPF inside the kernel — no extra proxy hop.
* L7 traffic: intercepted and forwarded to the node-local Envoy proxy for L7 termination or advanced processing — one proxy hop only for L7 paths.

<Frame>
  <img alt="A side-by-side diagram comparing network traffic management: the left shows L3/L4 traffic flow handled by cilium/eBPF, and the right shows L7 terminations where an Envoy/service-mesh proxy intercepts traffic before it exits via eth0." />
</Frame>

Comparison table — Sidecar vs Sidecarless (Cilium)

| Feature                           | Sidecar model (e.g., Istio)                   | Cilium (sidecarless)                                        |
| --------------------------------- | --------------------------------------------- | ----------------------------------------------------------- |
| Proxy placement                   | Per-pod sidecar proxies                       | Node-local Envoy (when L7 needed); eBPF in kernel for L3/L4 |
| L3/L4 handling                    | Sidecar or kernel depending on implementation | eBPF handles L3/L4 in kernel (no proxy hop)                 |
| L7 handling                       | Sidecar handles L7                            | Envoy handles L7 (node-local), invoked for L7 only          |
| Resource consumption              | Higher (proxy per pod)                        | Lower (fewer Envoy instances, eBPF efficiency)              |
| Configuration surface             | Per-pod proxy configs to manage               | Centralized node-level configs + eBPF policies              |
| Startup and lifecycle             | Sidecars add startup complexity               | Pod startup decoupled from sidecar lifecycle                |
| Compatibility with immutable apps | Works well (no code change)                   | Works well; integrates transparently via kernel hooks       |
| Observability & L7 features       | Full L7 via sidecar                           | Full L7 via Envoy; L3/L4 observability via eBPF             |

When to choose which approach:

* Use a sidecar model when you need per-pod L7 controls tightly coupled with the application, or when an existing ecosystem relies on per-pod proxies.
* Choose Cilium (sidecarless) when you want lower per-pod resource overhead, high-performance L3/L4 processing, and a simplified operational model while still supporting L7 functionality through node-local Envoy instances.
* Cilium can integrate with other meshes if you need hybrid setups or incremental migration.

Links and references:

* [Cilium](https://cilium.io) — eBPF-based networking and security for cloud-native environments
* [eBPF](https://ebpf.io) — extended Berkeley Packet Filter: safe kernel-level programs
* [Envoy](https://www.envoyproxy.io) — high-performance edge and service proxy
* [Istio](https://istio.io) — example sidecar-based service mesh

<Callout icon="lightbulb">
  Cilium’s approach reduces per-pod overhead by using eBPF for L3/L4 while still providing L7 capabilities via node-local Envoy instances—combining performance with feature completeness.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/50bb84d0-61e7-4f73-a51b-7da0e8338438/lesson/1da8eb0c-d53a-4aae-a0fa-454991ff41f2" />
</CardGroup>
