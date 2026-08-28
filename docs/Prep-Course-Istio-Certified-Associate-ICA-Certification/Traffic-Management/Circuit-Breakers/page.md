# ...
```

If you plan to enable L7 features in a namespace, add the labels:

```bash theme={null}
kubectl label namespace hello istio.io/dataplane-mode=ambient istio.io/use-waypoint=waypoint
```

***

## Deploy the HelloWorld app (example)

This demo uses a simple Hello World app with two versions (v1 and v2). The repository contains `helloworld.yaml` which creates two deployments and a catch-all service.

Deploy into the `hello` namespace:

```bash theme={null}
kubectl apply -f helloworld.yaml -n hello
```

Verify deployments and services:

```bash theme={null}
kubectl get deployments.apps -n hello
kubectl get svc -n hello
```

Example output:

```text theme={null}
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
helloworld-v1   1/1     1            1           2m
helloworld-v2   1/1     1            1           2m
waypoint        1/1     1            1           30s

NAME        TYPE        CLUSTER-IP       PORT(S)
helloworld  ClusterIP   10.109.201.209   5000/TCP
waypoint    ClusterIP   10.108.208.214   15021/TCP,15008/TCP
```

***

## Attempt: split traffic using DestinationRule + VirtualService (sidecar-style)

In sidecar-based deployments, you typically split traffic using a `DestinationRule` with subsets and a `VirtualService` with weighted routes.

Example sidecar-style `VirtualService`:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello-world-vs
  namespace: hello
spec:
  hosts:
    - helloworld
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: helloworld.default.svc.cluster.local
            port:
              number: 5000
            subset: v1
          weight: 95
        - destination:
            host: helloworld.default.svc.cluster.local
            port:
              number: 5000
            subset: v2
          weight: 5
```

And matching `DestinationRule`:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: hello-world-dr
  namespace: hello
spec:
  host: helloworld
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

Apply:

```bash theme={null}
kubectl apply -f hello-dr.yaml
kubectl apply -f hello-vs.yaml
```

However, in Ambient Mode this approach does not reliably split traffic. `ztunnel` handles L4 routing and does not support VirtualService subset routing in the same way sidecars do. Results may appear random or not follow the configured weights.

***

## Correct approach for split traffic in Ambient Mode: HTTPRoute + waypoint

To implement weighted HTTP split routing in Ambient Mode, use the Kubernetes Gateway API `HTTPRoute` (gateway.networking.k8s.io/v1) and configure a waypoint proxy that performs L7 processing.

High-level steps:

1. Create a waypoint proxy for the namespace (generates the waypoint Envoy).
2. Remove the sidecar-style `VirtualService`/`DestinationRule`.
3. Create per-version Kubernetes Services and an `HTTPRoute` that references those services with weights.
4. Test traffic distribution via the waypoint proxy.

Step-by-step:

1. Create the waypoint for the `hello` namespace:

```bash theme={null}
istioctl waypoint apply -n hello
```

Verify the waypoint pod is running:

```bash theme={null}
kubectl get pods -n hello
```

2. Remove the sidecar-style rules that do not provide the expected split semantics in Ambient Mode:

```bash theme={null}
kubectl delete -f hello-vs.yaml
kubectl delete -f hello-dr.yaml
```

3. Create an `HTTPRoute` that attaches to the catch-all `helloworld` Service (port 5000) and splits traffic using `backendRefs`. Save as `hello-httproute-split-traffic.yaml`:

```yaml theme={null}
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: hello-http-split-traffic
  namespace: hello
spec:
  parentRefs:
    - group: ""
      kind: Service
      name: helloworld
      port: 5000
  rules:
    - backendRefs:
        - name: helloworld-v1
          port: 5000
          weight: 95
        - name: helloworld-v2
          port: 5000
          weight: 5
```

Apply:

```bash theme={null}
kubectl apply -f hello-httproute-split-traffic.yaml
```

Important: `backendRefs` must reference Kubernetes Services. Create two per-version services (one per deployment) in addition to the catch-all `helloworld` service.

Example per-version Service YAML (can be added to `helloworld.yaml` or a separate file):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: helloworld-v1
  namespace: hello
  labels:
    app: helloworld
    version: v1
spec:
  ports:
    - port: 5000
      name: http
  selector:
    app: helloworld
    version: v1
---
apiVersion: v1
kind: Service
metadata:
  name: helloworld-v2
  namespace: hello
  labels:
    app: helloworld
    version: v2
spec:
  ports:
    - port: 5000
      name: http
  selector:
    app: helloworld
    version: v2
```

Apply the services (and any updated `helloworld` manifests):

```bash theme={null}
kubectl apply -f helloworld.yaml -n hello
```

Now confirm you have the catch-all and the per-version services:

```bash theme={null}
kubectl get svc -n hello
```

Example output:

```text theme={null}
NAME             TYPE        CLUSTER-IP       PORT(S)
helloworld       ClusterIP   10.109.201.209   5000/TCP
helloworld-v1    ClusterIP   10.109.201.210   5000/TCP
helloworld-v2    ClusterIP   10.106.142.114   5000/TCP
waypoint         ClusterIP   10.108.208.214   15021/TCP,15008/TCP
```

4. Test the split behavior from a test pod:

```bash theme={null}
kubectl exec -n test curl -- curl helloworld.hello.svc.cluster.local:5000/hello
```

You should observe routing according to the configured weights (95% → v1, 5% → v2). Small sample sizes can hide the distribution — issue many requests to validate the split.

***

## Notes: features not fully supported (yet)

* Mirroring is not supported in Ambient Mode (as of this writing).
* Some features like certain timeouts and retries may not behave identically under Ambient Mode L7 processing. Always check release notes and the Istio roadmap for current support.
* `HTTPRoute` + waypoint is the recommended Kubernetes-native pattern for L7 behavior (weights) in Ambient Mode.

<Callout icon="warning">
  Ambient Mode behavior is evolving. If a feature behaves differently than sidecar mode, consult the [Istio Ambient Mode documentation](https://istio.io/latest/docs/ops/deployment/ambient/) and [Istio release notes](https://istio.io/latest/news/releases/) for current status and supported APIs.
</Callout>

***

## Example: httpbin with delay and abort fault injection (waypoint + VirtualService)

For L7 fault injection (delay/abort) you can often use `VirtualService` APIs when a waypoint proxy is handling L7. This example deploys `httpbin` into a waypoint-enabled namespace and applies `VirtualService` fault rules.

1. Label the namespace and create a waypoint for `httpbin`:

```bash theme={null}
kubectl label namespace httpbin istio.io/dataplane-mode=ambient istio.io/use-waypoint=waypoint
istioctl waypoint apply -n httpbin
```

2. Deploy `httpbin`:

```bash theme={null}
kubectl apply -f httpbin.yaml -n httpbin
```

Verify pods and services:

```bash theme={null}
kubectl get pods -n httpbin
kubectl get svc -n httpbin
```

3. Test the basic GET route from the test pod:

```bash theme={null}
kubectl exec -n test curl -- curl httpbin.httpbin.svc.cluster.local:8000/get
```

You should receive a normal httpbin JSON response.

4. Inject a delay (VirtualService fault injection). Save as `httpbin-vs-delay.yaml`:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: httpbin-vs-delay
  namespace: httpbin
spec:
  hosts:
    - httpbin.httpbin.svc.cluster.local
  http:
    - fault:
        delay:
          percentage:
            value: 100.0
          fixedDelay: 3s
      route:
        - destination:
            host: httpbin.httpbin.svc.cluster.local
            port:
              number: 8000
```

Apply:

```bash theme={null}
kubectl apply -f httpbin-vs-delay.yaml
```

Test and observe the delay (\~3 seconds):

```bash theme={null}
kubectl exec -n test curl -- curl httpbin.httpbin.svc.cluster.local:8000/get
```

Sample curl timing should show the request takes \~3s.

5. Inject an abort (500). Save as `httpbin-vs-abort.yaml`:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: httpbin-vs-abort
  namespace: httpbin
spec:
  hosts:
    - httpbin.httpbin.svc.cluster.local
  http:
    - fault:
        abort:
          percentage:
            value: 100.0
          httpStatus: 500
      route:
        - destination:
            host: httpbin.httpbin.svc.cluster.local
            port:
              number: 8000
```

Apply and test with a `HEAD` request to inspect the HTTP status:

```bash theme={null}
kubectl apply -f httpbin-vs-abort.yaml
kubectl exec -n test curl -- curl --head httpbin.httpbin.svc.cluster.local:8000/get
```

Expected response header (example):

```text theme={null}
HTTP/1.1 500 Internal Server Error
content-length: 18
content-type: text/plain
server: istio-envoy
x-envoy-decorator-operation: httpbin.httpbin.svc.cluster.local:8000/*
```

You can change `httpStatus` (for example, to `404`) and reapply to modify abort behavior.

***

## Summary / Best practices

* Ambient Mode uses `ztunnel` for L4 routing and a waypoint Envoy proxy for L7 features.
* Sidecar-mode primitives (VirtualService subsets + DestinationRules) do not reliably provide the same split semantics in Ambient Mode.
* For HTTP request splitting in Ambient Mode, prefer the Kubernetes Gateway API `HTTPRoute` attached to the catch-all service, with `backendRef` services (one service per deployment/version).
* For L7 fault injection (delay/abort), the waypoint proxy combined with `VirtualService` often works — but confirm support per Istio release.
* Ambient Mode is evolving; always consult the Istio docs and release notes for current API support and recommended patterns.

Further reading and references:

* [Istio Ambient Mode docs](https://istio.io/latest/docs/ops/deployment/ambient/)
* [Istio Gateway API / HTTPRoute](https://kubernetes-sigs.github.io/gateway-api/)
* [Istio release notes](https://istio.io/latest/news/releases/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/d31069ab-dc8e-47ed-8e31-0fe4f66948da" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/bc7f3e4f-292c-45db-a5d3-fc8cc9b825e6" />
</CardGroup>


# Circuit Breakers

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Circuit-Breakers/page

Explains Istio circuit breaking concepts, benefits and configuration via DestinationRule including connection pool limits and outlier detection with examples and troubleshooting.

Here's your traditional home.

You have a living room, a bathroom, a kitchen, and maybe a couple of bedrooms.

In one room, two siblings might be playing video games while Grandma watches them. She gets a little cold, so she plugs in her heater. Adjacent on the other side of that wall, Mom just finished showering and is drying her hair. Without getting too deep into the electrical details, there is too much current flowing through that circuit, which can cause the wires to overheat and potentially catch fire.

Luckily, your home has a circuit breaker.

A circuit breaker is a safety switch. If a TV, gaming console, heater, and dryer are all drawing power from the same circuit at once, the breaker will trip and cut power to that part of the house to prevent overheating and fire. Circuit breakers literally save homes every day.

Circuit breaking in Istio is analogous to the circuit breaker in your house, but instead of electricity it controls network traffic between services. If one service is slow, overloaded, or failing, circuit breaking helps protect the rest of the system from being dragged down.

<Frame>
  <img alt="The image shows a person sitting on a sofa with a heater, two people playing video games in front of a TV, and a person drying their hair in front of a mirror." />
</Frame>

Consider a simple example: your home hot water system. Hot water is distributed on demand to bathrooms, the kitchen, and the laundry. If every tap requests hot water at once, the water heater may become overwhelmed and start delivering cold water or fail. With a smart system (like Istio), you could enforce a rule: if more than two taps request hot water simultaneously, stop accepting new requests for a short time. This prevents the heater from being overloaded while allowing the system to recover.

Applied to microservices, circuit breaking prevents one struggling component from causing cascading failures across the entire application.

## Bookinfo example

The Bookinfo sample app demonstrates typical service-to-service communication: productpage calls details and reviews. If the details service slows or fails, productpage requests pile up waiting for responses. Circuit breaking lets us fail fast (return an error or fallback) instead of waiting indefinitely, keeping the rest of the system responsive and preventing request queues from growing unbounded.

## Cascading failure example

Imagine three services: homepage, products, and a database. The products service queries the database, and the homepage calls products. If the database becomes slow, the products service waits, times out, and keeps retrying. The homepage then becomes slow as it waits on the products service, causing more requests and eventually a cascading failure.

Circuit breaking stops this chain by tripping when a downstream dependency is unhealthy. Tripping allows callers to quickly receive an error or fallback response so the overall system remains available and the unhealthy component gets isolated for recovery.

## Why use circuit breaking?

* Prevents spread of failures: Stops calls to an unhealthy service before they cause additional failures.
* Keeps the rest of the system running: Gives struggling services breathing room to recover.
* Fails fast for better UX: Returns a quick error or fallback rather than making users wait indefinitely.
* Provides a signal for troubleshooting: A tripped circuit is an obvious indicator that something is wrong.

## Configuration overview

In Istio, circuit breaking is configured inside a DestinationRule's `trafficPolicy`. There is no standalone "CircuitBreaker" top-level resource. Common controls include connection pool limits and outlier detection (which ejects unhealthy hosts).

Example DestinationRule containing both connection pool settings and outlier detection:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: app-ds
  namespace: frontend
spec:
  host: app-svc
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 2
        connectTimeout: 30s
      http:
        http2MaxRequests: 2
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 5s
      baseEjectionTime: 10m
```

### Key fields explained

| Field                                          | Purpose                                                    | Example / Notes          |
| ---------------------------------------------- | ---------------------------------------------------------- | ------------------------ |
| `connectionPool.tcp.maxConnections`            | Limit concurrent TCP connections to the host               | `2` in the example above |
| `connectionPool.tcp.connectTimeout`            | How long to wait for TCP connection establishment          | `30s`                    |
| `connectionPool.http.http2MaxRequests`         | Max concurrent requests per HTTP/2 connection              | `2`                      |
| `connectionPool.http.maxRequestsPerConnection` | Max requests per HTTP/1 connection                         | `10`                     |
| `outlierDetection.consecutive5xxErrors`        | Number of consecutive 5xx responses to mark host unhealthy | `3`                      |
| `outlierDetection.interval`                    | How often to run ejection analysis                         | `5s`                     |
| `outlierDetection.baseEjectionTime`            | How long an ejected host stays out of the pool             | `10m`                    |

All of these options (and more) are documented under DestinationRule connection pool and outlier detection settings. Review the official docs for the complete list of options and real-world examples: [https://istio.io/latest/docs/reference/config/networking/destination-rule/](https://istio.io/latest/docs/reference/config/networking/destination-rule/)

Another example for a reviews service:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: reviews-cb-policy
spec:
  host: reviews.prod.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30s
      http:
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 7
      interval: 5s
      baseEjectionTime: 15m
```

<Callout icon="lightbulb">
  Circuit breaking (connection pool settings and outlier detection) is configured in `DestinationRule`. The exam often asks about these settings—review the DestinationRule documentation and examples: [https://istio.io/latest/docs/reference/config/networking/destination-rule/](https://istio.io/latest/docs/reference/config/networking/destination-rule/).
</Callout>

## Quick troubleshooting checklist

* Verify DestinationRule `host` matches the service FQDN.
* Confirm values are appropriate for traffic patterns (don't set `maxConnections` too low).
* Use metrics and logs (Envoy and Istio telemetry) to see ejection and connection counts.
* Tune `consecutive5xxErrors`, `interval`, and `baseEjectionTime` based on observed failure modes.

That covers the theory of circuit breaking in Istio. A demo will show these configurations in action.

## Links and references

* Istio DestinationRule docs: [https://istio.io/latest/docs/reference/config/networking/destination-rule/](https://istio.io/latest/docs/reference/config/networking/destination-rule/)
* Istio Traffic Management overview: [https://istio.io/latest/docs/concepts/traffic-management/](https://istio.io/latest/docs/concepts/traffic-management/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/52f3e6e1-9552-4fdc-9023-f74f859af972" />
</CardGroup>
