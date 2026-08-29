# NAME             STATUS   AGE   LABELS
# default          Active   24m   istio-injection=enabled,kubernetes.io/metadata.name=default
# istio-system     Active   71s   kubernetes.io/metadata.name=istio-system
# kube-node-lease  Active   24m   kubernetes.io/metadata.name=kube-node-lease
# kube-public      Active   24m   kubernetes.io/metadata.name=kube-public
# kube-system      Active   24m   kubernetes.io/metadata.name=kube-system
```

If needed, label your namespace:

```bash theme={null}
kubectl label namespace default istio-injection=enabled --overwrite
```

## 2. Deploy the Echo server and Service

Create a Deployment (e.g., `echo_deployment.yaml`) for a simple HTTP echo server that listens on port 80, and expose it via a ClusterIP Service `echo-server`.

Service manifest (`echo_svc.yaml`):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: echo-server
  labels:
    app: echo-server
spec:
  ports:
    - port: 80
      name: http
  selector:
    app: echo-server
```

Apply the manifests and confirm pods and service are ready:

```bash theme={null}
kubectl apply -f echo_deployment.yaml
kubectl apply -f echo_svc.yaml

kubectl get pods
# NAME                               READY   STATUS    RESTARTS   AGE
kubectl get svc
# NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# echo-server   ClusterIP   10.104.144.230  <none>        80/TCP     6s
```

## 3. Deploy Fortio (load tester)

Fortio is a lightweight load tester you can run inside the cluster to generate requests to the echo service.

Deploy Fortio and confirm the pod is running:

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.25/samples/httpbin/sample-client/fortio-deploy.yaml

kubectl get pods
# NAME                               READY   STATUS    RESTARTS   AGE
# fortio-deploy-689bd5969b-l82zv     2/2     Running   0          9s
```

Verify connectivity by curling the echo service from the Fortio container:

```bash theme={null}
kubectl exec fortio-deploy-689bd5969b-l82zv -c fortio -- /usr/bin/fortio curl -quiet http://echo-server | grep -o '"HOSTNAME":"[^"]*"'
# Example output:
# "HOSTNAME":"echo-server-64fb4c5655-vzdh6"
```

Tip: replace the Fortio pod name if it differs in your cluster.

## 4. Create a VirtualService (simple passthrough)

Create a VirtualService that intercepts traffic for `echo-server` and routes to the same Kubernetes Service. This keeps routing explicit and prepares the path for upstream policies.

`vs.yaml`:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: echo-vs
spec:
  hosts:
    - echo-server
  http:
    - route:
      - destination:
          host: echo-server
          port:
            number: 80
```

Apply and verify:

```bash theme={null}
kubectl apply -f vs.yaml
kubectl get vs
# NAME      GATEWAYS   HOSTS           AGE
# echo-vs   <none>     ["echo-server"]  3m
```

The VirtualService itself does not change behavior yet — it simply ensures traffic is routed through Istio.

## 5. Create a DestinationRule to implement circuit breaking

Circuit breaking in Istio is enforced by DestinationRule through `connectionPool` limits and `outlierDetection`. Create a DestinationRule to limit connections and eject unhealthy hosts.

`dr.yaml`:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: echo-dr
spec:
  host: echo-server
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 1
      http:
        http1MaxPendingRequests: 1
        maxRequestsPerConnection: 1
    outlierDetection:
      consecutive5xxErrors: 1
      interval: 5s
      baseEjectionTime: 30s
      maxEjectionPercent: 100
```

Meaning of key fields:

* `connectionPool.tcp.maxConnections: 1` — only 1 concurrent TCP connection to the upstream.
* `http.http1MaxPendingRequests: 1` & `maxRequestsPerConnection: 1` — limited pending and per-connection requests.
* `outlierDetection.consecutive5xxErrors: 1` — a single 5xx can mark a host for ejection.
* `interval`, `baseEjectionTime`, `maxEjectionPercent` — control detection frequency and ejection behavior.

Apply the DestinationRule and verify:

```bash theme={null}
kubectl apply -f dr.yaml

kubectl get destinationrules.networking.istio.io
# NAME      HOST         AGE
# echo-dr   echo-server  7s
```

## 6. Generate load to trigger the circuit breaker

Start with a simple request from Fortio to confirm correct routing:

```bash theme={null}
kubectl exec fortio-deploy-689bd5969b-l82zv -c fortio -- /usr/bin/fortio curl -quiet http://echo-server | grep -o '"HOSTNAME":"[^"]*"'
# "HOSTNAME":"echo-server-64fb4c5655-vzdh6"
```

Run a modest load test (2 concurrent connections, 20 requests):

```bash theme={null}
kubectl exec fortio-deploy-689bd5969b-l82zv -c fortio -- /usr/bin/fortio load -c 2 -qps 0 -n 20 -loglevel Warning http://echo-server
```

Sample summary (abbreviated):

```bash theme={null}
Code 200: 19 (95.0%)
Code 503: 1 (5.0%)
All done 20 calls (plus 0 warmup) ... avg ... qps ...
```

Now increase concurrency to force Envoy to hit the configured connection/pending limits:

```bash theme={null}
kubectl exec fortio-deploy-689bd5969b-l82zv -c fortio -- /usr/bin/fortio load -c 20 -qps 0 -n 80 -loglevel Warning http://echo-server
```

When the circuit breaker is engaged you will see many 503 responses:

```text theme={null}
Code 200: 7 (8.8%)
Code 503: 73 (91.2%)
All done 80 calls ... avg ...
```

Explanation: Envoy enforces `maxConnections` and pending request limits; when those are exceeded, it rejects requests with 503.

## 7. Adjust DestinationRule and observe effect

To allow more concurrent traffic, increase connection and request-per-connection limits in the DestinationRule, reapply, and re-run the load test.

Example changes inside `dr.yaml`:

```yaml theme={null}
    connectionPool:
      tcp:
        maxConnections: 10
      http:
        http1MaxPendingRequests: 1
        maxRequestsPerConnection: 10
```

Apply and test:

```bash theme={null}
kubectl apply -f dr.yaml
kubectl exec fortio-deploy-689bd5969b-l82zv -c fortio -- /usr/bin/fortio load -c 20 -qps 0 -n 80 -loglevel Warning http://echo-server
```

You should see fewer 503s as the proxy allows more concurrent connections/requests. Tune the values to match your upstream application's concurrency characteristics.

<Callout icon="lightbulb">
  When setting connection pools and circuit breakers, align limits with your application's real concurrency and connection behavior. Overly strict limits can cause apparent outages under legitimate load.
</Callout>

## 8. Inspect Envoy proxy stats (pilot-agent)

To view circuit breaker metrics exposed by the sidecar, query the pilot-agent stats endpoint from the pod's `istio-proxy` container. These stats show pending totals and overflow/rejection counters that explain observed 503s.

Example command (filtering for echo-server and pending counters):

```bash theme={null}
kubectl exec fortio-deploy-689bd5969b-l82zv -c istio-proxy -- pilot-agent request GET stats | grep echo-server | grep pending
```

Example fields you might see:

```bash theme={null}
cluster.outbound|80|echo-server.default.svc.cluster.local|circuit_breakers.default.remaining_pending: 1
cluster.outbound|80|echo-server.default.svc.cluster.local|circuit_breakers.default.rq_pending_open: 0
cluster.outbound|80|echo-server.default.svc.cluster.local|upstream_rq_pending_total: 36
cluster.outbound|80|echo-server.default.svc.cluster.local|upstream_rq_pending_overflow: 139
```

* `upstream_rq_pending_total` — total pending requests.
* `upstream_rq_pending_overflow` — number of requests rejected due to pending limits.

<Callout icon="warning">
  Circuit breaking and aggressive rate-limiting can be disruptive. Do not apply global or overly strict DestinationRule policies in production without monitoring, staging, and understanding application behavior.
</Callout>

## 9. DestinationRule options and examples

DestinationRule includes several useful configuration groups for connection management and resilience.

| Feature                          | Description                                                                  | Example fields                                                                              |
| -------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Connection pool (TCP/HTTP/HTTP2) | Limits concurrent connections, pending requests, and per-connection requests | `maxConnections`, `http1MaxPendingRequests`, `http2MaxRequests`, `maxRequestsPerConnection` |
| Outlier detection                | Ejects unhealthy hosts based on error/latency patterns                       | `consecutive5xxErrors`, `interval`, `baseEjectionTime`, `maxEjectionPercent`                |
| TCP keepalive                    | Keepalive timing for upstream TCP connections                                | `tcpKeepalive` (`time`, `interval`)                                                         |
| TLS / mTLS                       | Per-destination TLS settings                                                 | `trafficPolicy.tls`                                                                         |
| Load balancing / subsets         | Per-subset traffic policy and load balancer settings                         | `subsets`, `loadBalancer`                                                                   |

More complete examples:

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
      http:
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 7
      interval: 5m
      baseEjectionTime: 15m
```

TCP keepalive example:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: bookinfo-redis
spec:
  host: myredissrv.prod.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30ms
        tcpKeepalive:
          time: 7200s
          interval: 75s
```

<Frame>
  <img alt="The image shows a webpage from Istio's documentation, specifically detailing configuration options for networking such as maxRequestsPerConnection and idleTimeout. It includes sections on HTTP/2 upgrade policy and connection settings." />
</Frame>

## 10. Summary

* Istio circuit breaking is configured via DestinationRule using `connectionPool` (limits) and `outlierDetection` (host ejection).
* VirtualService routes traffic; DestinationRule enforces proxy behavior on the destination.
* Use Fortio (or similar tools) to generate load and verify how Envoy responds when limits are reached (often 503).
* Inspect sidecar stats (`pilot-agent` / stats endpoint) to diagnose pending/overflow counters.
* Always test and tune connection-pool and outlier settings to match your application's concurrency model before applying policies in production.

Links and references:

* Istio DestinationRule docs: [https://istio.io[AWS_SECRET_ACCESS_KEY]/destination-rule/](https://istio.io[AWS_SECRET_ACCESS_KEY]/destination-rule/)
* Fortio: [https://github.com/fortio/fortio](https://github.com/fortio/fortio)
* Envoy stats and cluster metrics: [https://www.envoyproxy.io/docs/envoy/latest/metrics/overview](https://www.envoyproxy.io/docs/envoy/latest/metrics/overview)

For exam preparation: when you hear "circuit breaking" in Istio, think "DestinationRule" and be familiar with `connectionPool` and `outlierDetection` settings.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/518eba4a-4fda-4d47-97a1-45b616fe8388" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/fe71f163-15e5-48ad-a424-c7b74befa7f9" />
</CardGroup>


# Demo Fault Injection

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Fault-Injection/page

Tutorial demonstrating Istio fault injection using VirtualService to simulate fixed delays and abort errors on a helloworld sample, with deployment and test steps

In this lesson you'll apply two Istio fault-injection scenarios to a simple helloworld app: a fixed delay and an abort (HTTP error). The walkthrough shows how to deploy the sample app, run tests from a pod, and apply VirtualService configurations to observe Envoy-injected faults.

Keywords: Istio fault injection, VirtualService, Envoy fault filter, delay, abort, helloworld sample

Prerequisites:

* A Kubernetes cluster with Istio installed and sidecar injection enabled for your namespace.
* `kubectl` configured to talk to the cluster.

1. Verify the namespace has Istio sidecar injection enabled

```bash theme={null}
