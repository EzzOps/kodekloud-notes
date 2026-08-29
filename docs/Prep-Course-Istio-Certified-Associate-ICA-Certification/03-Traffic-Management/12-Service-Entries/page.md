# Service Entries

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Service-Entries/page

Explains Istio ServiceEntry and outbound traffic policies, registering external services for egress control, security, observability, and different resolution methods

We assume familiarity with the Istio service mesh basics: workloads communicate through Envoy sidecars (e.g., Service 1 → Service 3 → Service 2). Controlling how Envoy handles outbound traffic is done via the mesh-wide outbound traffic policy mode, which you configure when installing Istio (for example, using the IstioOperator).

Outbound traffic policy modes

* ALLOW\_ANY (default): Envoy will pass through requests to external services that are not in Istio’s internal service registry.
* REGISTRY\_ONLY: Envoy will only allow outbound traffic to services registered in Istio’s internal service registry (typically via a ServiceEntry). Any attempt to reach unknown external services will be dropped.

> **lightbulb** By default Istio runs in permissive mode (`ALLOW_ANY`), so workloads can reach external services without a `ServiceEntry`. However, Istio will not apply traffic management, observability, or security features to those external flows unless the external services are added to the registry.

Why ServiceEntry?
A ServiceEntry adds an external service (for example, an external PostgreSQL database) to Istio’s internal service registry. This enables Envoy to route to that service and allows Istio to enforce traffic policies, telemetry collection, and mTLS for egress traffic.

<Frame>
  <img alt="The image is a diagram illustrating how a service entry in Istio adds external PostgreSQL services to Istio's registry for routing and access, involving nodes, namespaces, and Envoy proxies." />
</Frame>

Comparing ALLOW\_ANY vs REGISTRY\_ONLY

| Mode            | Behavior                                                                                                                                     | When to use                                                                                                       |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `ALLOW_ANY`     | Envoy allows outbound traffic to unknown external hosts (no `ServiceEntry` required). Istio does not apply advanced controls to those flows. | Useful for default permissive setups or during initial development.                                               |
| `REGISTRY_ONLY` | Envoy only permits outbound traffic to services present in Istio's registry (e.g., via `ServiceEntry`). Unknown external traffic is dropped. | Use when you require strict control over egress traffic, observability, or egress security (mTLS, authorization). |

Enforcing REGISTRY\_ONLY with the Istio operator
To force Envoy to only allow registry-listed services, set `meshConfig.outboundTrafficPolicy.mode` to `REGISTRY_ONLY` in your IstioOperator manifest:

```yaml theme={null}
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  components:
    base:
      enabled: true
    cni:
      enabled: false
    egressGateways:
      - enabled: false
        name: istio-egressgateway
    ingressGateways:
      - enabled: true
        name: istio-ingressgateway
    istiodRemote:
      enabled: false
    pilot:
      enabled: true
  hub: docker.io/istio
  meshConfig:
    outboundTrafficPolicy:
      mode: REGISTRY_ONLY
  defaultConfig:
    proxyMetadata: {}
```

With `REGISTRY_ONLY`, any external destination not represented in Istio’s registry will be blocked. In `ALLOW_ANY` mode, external destinations are reachable but not managed by Istio.

ServiceEntry example — external PostgreSQL
Below is a minimal `ServiceEntry` that registers an external PostgreSQL server. Note: `resolution` is at the same level as `ports` inside `spec`, and this resource is namespaced.

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: postgres-db
  namespace: frontend
spec:
  hosts:
    - db.example.com
  ports:
    - number: 5432
      name: tcp-db
      protocol: TCP
  resolution: DNS
```

Scoping and visibility

* `ServiceEntry` is a namespaced resource. By default, a `ServiceEntry` created in namespace `frontend` is visible only to sidecars and workloads in `frontend`.
* To make a `ServiceEntry` available to other namespaces, use the `exportTo` field (or create the resource in a namespace that is visible to others).

> **warning** If your mesh is configured with `REGISTRY_ONLY`, you must ensure any external dependency is registered in the namespace(s) that require access (or exported). Failing to do so will result in blocked egress traffic.

Common reasons to declare external services with ServiceEntry

* Centralized management of external dependencies for routing and troubleshooting.
* Apply Istio traffic management features to egress (retries, timeouts, circuit breaking).
* Enforce security policies (mTLS, authorization) for outbound traffic.
* Enable observability/telemetry for external calls through Envoy.

Resolution methods overview
The `resolution` field controls how Envoy discovers endpoints for the declared host. The slide below summarizes common resolution options:

<Frame>
  <img alt="The image is a slide titled &#x22;Service Entry Options&#x22; featuring definitions and explanations for terms like &#x22;ServiceEntry&#x22;, &#x22;Location&#x22;, and &#x22;Resolution&#x22;, with a focus on how network endpoints are resolved in a proxy. The slide includes detailed tables describing resolution methods such as NONE, STATIC, DNS, and DNS_ROUND_ROBIN." />
</Frame>

Resolution quick-reference

|        Resolution | Description                                                                                                                       |
| ----------------: | --------------------------------------------------------------------------------------------------------------------------------- |
|            `NONE` | No endpoints are provided by the `ServiceEntry`; it's used for DNS-only scenarios where sidecars rely on DNS to resolve the host. |
|             `DNS` | Envoy uses DNS lookup to discover endpoints for the host (typical for external services).                                         |
| `DNS_ROUND_ROBIN` | Envoy resolves the host via DNS and load-balances across returned addresses (round-robin behavior).                               |
|          `STATIC` | Endpoints are supplied directly in the `ServiceEntry` using the `addresses`/`endpoints` fields.                                   |

References and further reading

* [Istio ServiceEntry reference](https://istio.io/latest/docs/reference/config/networking/service-entry/)
* [Istio outbound traffic policy (meshConfig)](https://istio.io/latest/docs/ops/configuration/traffic-management/outbound/#outbound-traffic-policy)
* [Istio Certified Associate (ICA) course](https://learn.kodekloud.com/user/courses/istio-service-mesh)

Summary

* ALLOW\_ANY vs REGISTRY\_ONLY determines whether Envoy allows unknown external egress.
* Use `ServiceEntry` to register external dependencies when you need Istio-managed egress (routing, security, telemetry).
* `ServiceEntry` resources are namespaced — use `exportTo` when cross-namespace visibility is required.
* Practice creating `ServiceEntry` objects and toggling `outboundTrafficPolicy` to observe differences in connectivity and telemetry.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/12622866-bfdc-4071-8286-720c135f1124)
