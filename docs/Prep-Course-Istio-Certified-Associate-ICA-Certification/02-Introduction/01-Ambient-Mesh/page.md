# Legacy injection
kubectl label namespace myapp istio-injection=enabled

# Revision-based injection (recommended for canary upgrades)
kubectl label namespace myapp istio.io/rev=canary-1
```

Notes:

* After labeling a namespace, existing pods must be restarted so that new sidecars get injected.
* Revision-based labels map namespaces to a specific control plane revision and enable running multiple control planes concurrently.

## Ambient mode (sidecarless) and Waypoint proxies

Ambient mode is Istio’s option for sidecarless security and traffic management:

* In Ambient mode a `ztunnel` runs as a DaemonSet (one `ztunnel` per node) to enforce mTLS and network-level policies without per-pod sidecars.
* If you require Layer 7 features (L7 routing, application-level proxies) at namespace granularity rather than per-workload sidecars, consider deploying Waypoint proxies which provide namespace-level application proxy functionality.

Understand the trade-offs:

* Sidecar mode gives per-workload L7 capabilities and fine-grained routing.
* Ambient mode reduces injection overhead and simplifies some operational aspects at the cost of some L7 control patterns.

## Istio Operator and customization

The Istio Operator (the `IstioOperator` CR) is the canonical way to declaratively customize the control plane.

Workflow:

1. Create or edit an `IstioOperator` resource or Helm values file to express desired control plane configuration.
2. Apply changes with `istioctl` or Helm; the operator reconciles and updates the control plane accordingly.

Example (install a revisioned control plane):

```bash theme={null}
istioctl install --set revision=canary-1 --set profile=default
```

Key points:

* Use the operator to manage profiles, component enablement, and resource sizing.
* Keep your `IstioOperator` or Helm values in source control for reproducibility (ideal for GitOps).

<Callout icon="warning">
  The Istio Operator and revision-based installation workflow are frequently covered in [certification exams](https://learn.kodekloud.com/user/courses/istio-certified-associate). Be comfortable with configuring via IstioOperator, updating values, and applying changes with `istioctl` or Helm.
</Callout>

## Canary (revision) upgrades for the Istio control plane

Canary upgrades let you run a new control plane revision in parallel with the old one, migrate workloads, and then remove the old revision once validated. Typical steps:

1. Install the new control plane with a revision label:

```bash theme={null}
istioctl install --set revision=<new-revision> --set profile=default
```

2. Label target namespaces to use the new revision:

```bash theme={null}
kubectl label namespace <namespace> istio.io/rev=<new-revision>
```

3. Restart workloads (or let rolling updates occur) so pods are recreated and injected with the new proxy. Examples:

```bash theme={null}
kubectl rollout restart deployment/myapp -n <namespace>
# or delete pods to force recreation
kubectl delete pod -l app=myapp -n <namespace>
```

4. Validate application behavior and traffic routing with tests and telemetry (logs, metrics, traces).

5. When stable, uninstall the old control plane revision:

```bash theme={null}
istioctl uninstall --revision=<old-revision>
```

Checklist during canary upgrades:

* Confirm namespace labels target the intended revision.
* Verify sidecar proxies in pods match the new revision.
* Run integration and traffic-shift tests before decommissioning old revisions.

## Quick commands reference

| Purpose                          | Command                                                                |
| -------------------------------- | ---------------------------------------------------------------------- |
| Install default Istio            | `istioctl install`                                                     |
| Install revisioned control plane | `istioctl install --set revision=<new-revision> --set profile=default` |
| Label namespace for injection    | `kubectl label namespace <namespace> istio.io/rev=<revision>`          |
| Legacy injection label           | `kubectl label namespace <namespace> istio-injection=enabled`          |
| Restart deployment               | `kubectl rollout restart deployment/<name> -n <namespace>`             |
| Uninstall revision               | `istioctl uninstall --revision=<revision>`                             |

## Final reminders

* Always verify namespace labels before expecting automatic sidecar injection.
* Know when to use sidecar vs ambient mode and how `ztunnel` and Waypoint proxies differ.
* Use the Istio operator (IstioOperator CR) or Helm values for repeatable configuration; store these artifacts in version control.
* Practice the canary revision upgrade flow: install revision, migrate namespaces, validate traffic, then remove the old revision.

## Links and references

* Istio official docs: [https://istio.io/](https://istio.io/)
* [GitOps with Argo CD](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* [Istio Certified Associate course (exam prep)](https://learn.kodekloud.com/user/courses/istio-certified-associate)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/65ee174b-536e-4657-9b6f-85c90c7612da/lesson/09d3bcf7-365a-4c37-b6e5-f38d8f003f01" />
</CardGroup>


# Ambient Mesh

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Introduction/Ambient-Mesh/page

Explains Istio Ambient Mesh sidecar-less architecture using ztunnel per node and Waypoint per namespace to provide Layer 4 transport and on-demand Layer 7 features.

Istio Ambient Mesh is Istio’s sidecar-less deployment mode. Instead of injecting an Envoy sidecar into every workload pod, Ambient Mesh splits proxy responsibilities across two purpose-built components — reducing per-pod overhead and simplifying proxy management while still providing secure, observable, and controllable traffic.

Key benefits

* Sidecar-less architecture reduces CPU/memory overhead and the number of proxies to manage.
* Transparent Layer 4 controls remain available for all workloads.
* Layer 7 capabilities are provided on-demand using per-namespace Waypoint proxies.

Core components

* ztunnel — a Rust-based transparent proxy deployed as a DaemonSet (one per node). It intercepts inbound and outbound traffic for the node’s workloads and provides mTLS, authentication/authorization checks, and telemetry for pod traffic on that node.
* Waypoint — an Envoy-based proxy deployed as a standalone pod in a namespace when Layer 7 features are required. It handles application-layer routing and policies without being injected as a per-pod sidecar.

<Callout icon="lightbulb">
  ztunnel is a Rust-based transparent proxy running as a DaemonSet (one per node). Waypoint is an Envoy-based proxy deployed as a pod (per-namespace) when L7 features are required.
</Callout>

Layer responsibilities

* ztunnel (Layer 4)
  * Transparent interception of TCP/UDP traffic for all workloads on the node
  * mTLS (encryption/decryption)
  * Node-level authentication/authorization and telemetry
  * Basic routing to healthy endpoints
* Waypoint (Layer 7)
  * Application-level routing (path/header matches, rewrites)
  * Traffic splitting, fault injection, delays, aborts
  * Advanced L7 features where required (deployed per-namespace)

<Frame>
  <img alt="The image provides information about &#x22;Waypoint,&#x22; describing it as a proxy deployed as a pod, a standalone workload, handling Layer 7 policies, deployed per namespace, and not supporting timeouts, retries, or mirroring." />
</Frame>

When to use each component

* If you only need secure transport and basic connectivity controls, ztunnel (Layer 4) covers most use cases with minimal overhead.
* If you need application-layer routing, policy enforcement, header/path-based behavior, or traffic-splitting, deploy Waypoint in the target namespace to enable L7 capabilities for those workloads.

Gateway API and HTTPRoute
Ambient Mesh often relies on Kubernetes-native APIs for expressing Layer 7 routing. The Gateway API — specifically `HTTPRoute` — is a common pattern for L7 routing in ambient deployments, and integrates with Waypoint when application-layer features are required.

Example: HTTPRoute splitting traffic between two service backends

```yaml theme={null}
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: hello-http-route
  namespace: hello
spec:
  parentRefs:
    - group: gateway.networking.k8s.io
      kind: Gateway
      name: mesh-gateway
  rules:
    - backendRefs:
        - name: helloworld-v1
          port: 5000
          weight: 5
        - name: helloworld-v2
          port: 5000
          weight: 95
```

<Callout icon="lightbulb">
  The Gateway API approach differs from Istio’s sidecar-based VirtualService and DestinationRule model. For the Prep Course - Istio Certified Associate (ICA) Certification, installing Ambient mode and labeling namespaces is the primary requirement — in-depth Gateway API and Waypoint configuration is outside the exam scope. For current feature details and roadmap, see the Istio Ambient Mesh docs.
</Callout>

Architecture overview

* Ambient Mesh removes the per-pod sidecar. ztunnels run on each node to handle Layer 4 traffic; Waypoint proxies are deployed per-namespace only when L7 functionality is required. Make sure to label namespaces appropriately so Ambient behavior applies to workloads in those namespaces.

<Frame>
  <img alt="The image depicts a sidecar-less service mesh architecture within a Kubernetes environment, showcasing three nodes with different apps, services, namespaces, and zTunnels connected by Waypoints." />
</Frame>

Feature parity and limitations

* Not all sidecar-mode features are yet available in Ambient Mesh. Some fine-grained timeout/retry/mirroring semantics and specific L7 behaviors may be absent or different in Waypoint.
* The Istio project is actively evolving Ambient Mesh; consult the official docs for the latest information: [https://istio.io/latest/docs/ops/deployment/ambient/](https://istio.io/latest/docs/ops/deployment/ambient/)

Quick comparison

| Component | Layer                 | Deployed as                    | Primary responsibilities                                                                | When to use                                                    |
| --------- | --------------------- | ------------------------------ | --------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| ztunnel   | Layer 4 (transport)   | DaemonSet (one per node)       | Transparent interception, mTLS, node-level authN/authZ, telemetry, routing to endpoints | Default for all workloads to provide secure transport          |
| Waypoint  | Layer 7 (application) | Deployment/Pod (per-namespace) | Path/header routing, traffic splitting, rewrites, fault injection                       | Deploy when application-layer policies or routing are required |

Benefits summary

* Reduced proxy footprint (fewer proxies overall vs. sidecar-per-pod)
* Lower resource usage per node and per-cluster
* Simpler operational model for many deployment patterns

<Frame>
  <img alt="The image highlights a benefit of using Istio Ambient Mesh over traditional Istio Service Mesh, emphasizing fewer proxies to manage, accompanied by a small graphic." />
</Frame>

Closing
Ambient Mesh offers a compelling, sidecar-less alternative to traditional Istio deployments by moving transport concerns to a per-node proxy (ztunnel) and enabling L7 features only when needed (Waypoint). For deployment guidance, configuration examples, and compatibility notes, reference the Istio documentation and the Gateway API project:

* Istio Ambient Mesh docs: [https://istio.io/latest/docs/ops/deployment/ambient/](https://istio.io/latest/docs/ops/deployment/ambient/)
* Gateway API: [https://gateway-api.sigs.k8s.io/](https://gateway-api.sigs.k8s.io/)

Following this introduction, you will find a summary and hands-on configuration and installation tasks to practice Ambient mode setup and namespace labeling.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/da4579eb-7769-4ab9-a0e8-b81f70a12978/lesson/2a577a51-a17d-4e29-a47d-87b4b4e2e46d" />
</CardGroup>
