# inside container
curl httpbin.default.svc:8000/ip
curl httpbin.default.svc:8000/user-agent
exit
```

Example responses:

```json theme={null}
{
  "origin": "127.0.0.6:49657"
}
```

```json theme={null}
{
  "user-agent": "curl/7.88.1"
}
```

Note: By default Istio is permissive — services can communicate across namespaces unless you enable stricter mTLS policies or other restrictions.

> **lightbulb** If a pod's namespace is not labeled for istio-injection, its traffic does not traverse the Envoy sidecar. VirtualService rules apply only when traffic routes through the sidecar.

***

## 5. Create the first VirtualService

Create `vs.yaml` defining a VirtualService that routes `httpbin` traffic to the `httpbin` service on port `8000`:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin
  namespace: default
spec:
  hosts:
    - httpbin
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: httpbin.default.svc.cluster.local
            port:
              number: 8000
```

Apply it:

```bash theme={null}
kubectl apply -f vs.yaml
kubectl get virtualservice
```

Example:

```text theme={null}
NAME     GATEWAYS   HOSTS    AGE
httpbin  ["httpbin"]  10m
```

This VirtualService mirrors the existing Kubernetes service behavior (no changes yet), so requests routed through an Envoy sidecar will hit the service as before.

***

## 6. Break the VirtualService (for demonstration)

Edit the VirtualService and change the destination port to `9000` to intentionally misroute requests:

```yaml theme={null}
# modified vs.yaml - destination port changed to 9000
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin
  namespace: default
spec:
  hosts:
    - httpbin
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: httpbin.default.svc.cluster.local
            port:
              number: 9000
```

Apply the modified VirtualService:

```bash theme={null}
kubectl apply -f vs.yaml
```

If you curl from the `test` pod now you may still see it working — why?

* If the `test` pod's namespace is not Istio-injection-enabled (1/1 Ready), its traffic bypasses Envoy and the VirtualService has no effect. The traffic goes directly to the Kubernetes service which listens on port 8000, so the request succeeds.
* Once the `test` namespace has injection enabled and the pod is re-created with the sidecar (2/2), the VirtualService will intercept the traffic and route it to port 9000 — which the service is not listening on — resulting in a 503 Service Unavailable.

***

## 7. Enable Istio injection for the test namespace and re-create the pod

You can use `istioctl analyze` to get hints and then label the namespace:

```bash theme={null}
istioctl analyze -n test
kubectl label namespace test istio-injection=enabled
```

After labeling, delete the `test` pod so it gets re-created with a sidecar:

```bash theme={null}
kubectl delete pod -n test test
kubectl run test --image=nginx -n test
kubectl get pods -n test
```

You should now see `2/2`:

```text theme={null}
NAME   READY   STATUS    RESTARTS   AGE
test   2/2     Running   0          9s
```

Now exec into the pod and curl the httpbin service:

```bash theme={null}
kubectl exec -ti -n test test -- /bin/bash
curl httpbin.default.svc:8000/ip
curl httpbin.default.svc:8000/user-agent
curl -I httpbin.default.svc:8000/ip
exit
```

With the VirtualService pointing to port 9000 you will see a 503 Service Unavailable. Fix the VirtualService back to port 8000 and apply:

```bash theme={null}
# restore vs.yaml to port 8000 then:
kubectl apply -f vs.yaml
```

Requests should succeed again.

> **warning** When you enable `istio-injection=enabled` on a namespace, existing pods must be re-created (deleted) to get the Envoy sidecar injected. Labeling alone is not sufficient — restart the pods.

***

## 8. URL rewrites with VirtualService

You can add a rewrite rule in the VirtualService. Example: rewrite `/hello` to `/` and route to `httpbin`:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin
  namespace: default
spec:
  hosts:
    - httpbin
  http:
    - match:
        - uri:
            prefix: /hello
      rewrite:
        uri: /
      route:
        - destination:
            host: httpbin.default.svc.cluster.local
            port:
              number: 8000
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: httpbin.default.svc.cluster.local
            port:
              number: 8000
```

Test steps:

1. Before applying the rewrite, `curl httpbin.default.svc:8000/hello` returns `404 page not found` (no `/hello` endpoint).
2. Apply the VirtualService with the rewrite:
   ```bash theme={null}
   kubectl apply -f vs.yaml
   ```
3. After applying, `curl httpbin.default.svc:8000/hello` returns the root endpoint as if you requested `/`.

This shows how VirtualService can transform request URIs before routing to the service.

***

## 9. Quick reference: common VirtualService capabilities

The following table summarizes common VirtualService patterns and short YAML samples.

| Feature       |                                            Use case | Example snippet                                                                                        |
| ------------- | --------------------------------------------------: | ------------------------------------------------------------------------------------------------------ |
| Basic routing |               Route traffic to a specific host/port | See the `httpbin` VirtualService above                                                                 |
| Rewrite       |                  Rewrite request URI before routing | `rewrite: { uri: "/" }` in HTTP route                                                                  |
| Redirect      | Send client-side redirect to another path/authority | `redirect: { uri: "/v1/bookRatings", authority: newRatings.default.svc.cluster.local }`                |
| Header match  |                      Match requests by header value | `match: - headers: end-user: exact: jason`                                                             |
| Timeout       |                               Set per-route timeout | `timeout: 5s` inside an http route                                                                     |
| Retries       |        Configure retry attempts and per-try timeout | `retries: { attempts: 3, perTryTimeout: 2s, retryOn: "gateway-error,connect-failure,refused-stream" }` |

Representative YAML examples:

* DestinationRule with subsets:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: reviews-destination
  namespace: foo
spec:
  host: reviews # interpreted as reviews.foo.svc.cluster.local
  subsets:
  - name: v1
  - name: v2
```

* VirtualService with a timeout:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: my-productpage-rule
  namespace: istio-system
spec:
  hosts:
    - productpage.prod.svc.cluster.local
  http:
    - timeout: 5s
      route:
        - destination:
            host: productpage.prod.svc.cluster.local
```

* ServiceEntry for external hosts:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: external-svc-wikipedia
spec:
  hosts:
    - wikipedia.org
  location: MESH_EXTERNAL
```

* VirtualService with header-based match and URI prefix:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: ratings-route
spec:
  hosts:
    - ratings.prod.svc.cluster.local
  http:
    - match:
        - headers:
            end-user:
              exact: jason
          uri:
            prefix: "/ratings/v2/"
            ignoreUriCase: true
      route:
        - destination:
            host: ratings.prod.svc.cluster.local
```

* VirtualService with retries:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: ratings-route
spec:
  hosts:
    - ratings.prod.svc.cluster.local
  http:
    - route:
        - destination:
            host: ratings.prod.svc.cluster.local
            subset: v1
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: gateway-error,connect-failure,refused-stream
```

***

## 10. Final notes & references

* VirtualServices are foundational: you will use them extensively together with DestinationRules, Gateways, and Policies.
* In exam / production scenarios, copy the YAML snippets from the official docs and adapt them — you are expected to reference documentation rather than memorize every field.
* Always ensure the namespace/pod you are testing from is injection-enabled if you want VirtualService rules to be enforced by the Envoy sidecar.

Useful links:

* Istio Documentation: [https://istio.io/latest/docs/](https://istio.io/latest/docs/)
* Kubernetes: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* istioctl analyze: [https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/)

This concludes the VirtualService demo. Next up: DestinationRules and advanced traffic management.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/4deeb1cf-af2a-40f0-98f1-0f03b8dd2b87)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/f9527147-d6e9-4b09-bf7b-86cf274b6cd5)


# Destination Rules

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Destination-Rules/page

Explains Istio DestinationRules and VirtualServices, how subsets enable traffic splitting and apply per-destination policies like load balancing, connection pools, circuit breaking, and TLS

DestinationRules are as important as VirtualServices in Istio traffic management.

A VirtualService intercepts client traffic destined for a service and applies routing policies (like path/host matching and traffic splitting) to direct that traffic to a target service. DestinationRules complement VirtualServices by defining policies that apply after routing — once traffic arrives at the destination service. In practice, DestinationRules let you map logical subset names to specific pod labels and attach traffic policies (load balancing, connection pools, circuit breaking, TLS, etc.) to those subsets.

Use case example: to split traffic 50/50 between two versions of a workload, define subsets in a DestinationRule and reference those subsets from a VirtualService. The VirtualService performs the routing and weight assignment; the DestinationRule binds subset names to pod labels and configures endpoint-level behaviors.

## How DestinationRules and VirtualServices work together

* VirtualService: decides how traffic is routed (hosts, path/URI matches, weights, headers).
* DestinationRule: applies policies to the concrete destination after routing (per-subset or host-level settings).
* Subsets: logical names in a DestinationRule that map to pods via label selectors. VirtualServices reference these subset names to route to specific workload versions.

## Example: two deployments (v1 & v2), one Service, DestinationRule with subsets, and VirtualService traffic split

Deployments for v1 and v2 (each with 3 replicas):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment-v1
  namespace: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      version: v1
  template:
    metadata:
      labels:
        app: frontend
        version: v1
    spec:
      containers:
        - name: app
          image: app:1.1
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment-v2
  namespace: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
      version: v2
  template:
    metadata:
      labels:
        app: frontend
        version: v2
    spec:
      containers:
        - name: app
          image: app:2.1
```

A single Kubernetes Service selects both versions via the shared `app: frontend` label:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: app-svc
  namespace: frontend
spec:
  ports:
    - port: 80
      name: http
  selector:
    app: frontend
```

DestinationRule that defines subsets (v1 and v2) by matching pod labels:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: app-ds
  namespace: frontend
spec:
  host: app-svc
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

VirtualService that references those subsets and splits traffic 50/50:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: app-vs
  namespace: frontend
spec:
  hosts:
    - app-svc
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: app-svc
            port:
              number: 80
            subset: v1
          weight: 50
        - destination:
            host: app-svc
            port:
              number: 80
            subset: v2
          weight: 50
```

## Resource summary

| Resource Type   | Purpose                                              | Example                                  |
| --------------- | ---------------------------------------------------- | ---------------------------------------- |
| Deployment      | Define workload versions (pods/labels)               | `app-deployment-v1`, `app-deployment-v2` |
| Service         | Single logical service that fronts multiple versions | `app-svc`                                |
| DestinationRule | Map subset names to pod labels, apply policies       | `app-ds`                                 |
| VirtualService  | Route and split traffic to subsets                   | `app-vs`                                 |

## Key points

* DestinationRules are applied after routing decisions are made by VirtualServices.
* Subsets are logical names in a DestinationRule that map to pods via labels; VirtualServices reference these subset names to direct traffic.
* DestinationRules control per-subset or host-level policies:
  * Load balancing algorithms
  * Connection pool sizes
  * Timeouts and retries
  * Circuit breaking
  * Client TLS / mTLS settings
* Create DestinationRules in the same namespace as the targeted workloads. The `host` in the DestinationRule can be the short service name (e.g., `app-svc`) or the full FQDN (e.g., `app-svc.frontend.svc.cluster.local`).
* Ensure subset names used in VirtualServices exactly match the subset names defined in DestinationRules.

> **lightbulb** Ensure the subset names used in the VirtualService match the subset names defined in the DestinationRule, and place the DestinationRule in the same namespace as the service/workloads it targets.

DestinationRules enable resilience and fine-grained control of service-to-service traffic — for example, configuring connection pool sizes, timeouts, retries, circuit breaking, and TLS. See the Istio docs for the full set of options.

References:

* [Istio DestinationRule reference](https://istio.io/latest/docs/reference/config/networking/destination-rule/)
* [Istio VirtualService reference](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
* [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)

<Frame>
  <img alt="The image displays documentation for &#x22;Destination Rules Options&#x22; in a structured format, detailing elements like &#x22;DestinationRule,&#x22; &#x22;LoadBalancerSettings,&#x22; and various fields with descriptions related to network configuration." />
</Frame>

Now, let's proceed to a demo and go over these concepts in practice.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/402decd2-9f64-439c-8fbf-354a76b493ef)
