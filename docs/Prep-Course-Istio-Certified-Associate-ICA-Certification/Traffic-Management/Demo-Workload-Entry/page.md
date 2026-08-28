# Example:
kubectl logs -f httpbin-787cdcc9df-xx9gd -c istio-proxy
```

Look for repeated `GET /status/500` log entries — these show the proxy making retry attempts. Example (trimmed) log excerpt:

```text theme={null}
[2025-04-15T17:21:14.709Z] "GET /status/500 HTTP/1.1" 500 - via_upstream "-" 0 1 0 "-" "curl/7.88.1" ...
[2025-04-15T17:21:14.726Z] "GET /status/500 HTTP/1.1" 500 - via_upstream "-" 0 1 0 "-" "curl/7.88.1" ...
[2025-04-15T17:21:14.732Z] "GET /status/500 HTTP/1.1" 500 - via_upstream "-" 0 1 0 "-" "curl/7.88.1" ...
```

Those repeated lines indicate the proxy retried the request according to the VirtualService configuration. The client receives the final non-success status (500) unless one of the retries succeeds.

## Key fields reference (VirtualService HTTP route)

| Field                   | Purpose                                                            | Example                              |
| ----------------------- | ------------------------------------------------------------------ | ------------------------------------ |
| `timeout`               | Maximum total duration for the request before Envoy aborts         | `2s`                                 |
| `retries.attempts`      | Number of retry attempts proxy should make                         | `3`                                  |
| `retries.perTryTimeout` | Timeout for each retry attempt                                     | `1s`                                 |
| `retries.retryOn`       | Which error classes trigger retries (e.g., `5xx`, `gateway-error`) | `5xx`                                |
| `route.destination`     | Upstream service and port                                          | `host: httpbin`, `port.number: 8000` |

## Notes and tips

<Callout icon="lightbulb">
  Timeouts and retries are configured on the VirtualService HTTP route. Use timeouts to bound request latency, and use retries to handle transient 5xx errors — but be careful: retries increase load on upstreams. Tune `attempts` and `perTryTimeout` according to your application behavior.
</Callout>

Common guidance:

* Apply a sensible per-request timeout so clients don't wait indefinitely.
* Use limited retries and short `perTryTimeout` values to recover from brief upstream failures without causing excessive upstream load.
* Monitor proxy logs and application metrics to tune the values for your workload.

## Example reference snippets

VirtualService with a timeout:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin-vs
spec:
  hosts:
    - httpbin
  http:
    - timeout: 2s
      route:
        - destination:
            host: httpbin
            port:
              number: 8000
```

VirtualService with retries:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: httpbin-vs
spec:
  hosts:
    - httpbin
  http:
    - route:
        - destination:
            host: httpbin
            port:
              number: 8000
      retries:
        attempts: 3
        perTryTimeout: 1s
        retryOn: 5xx
```

## Links and References

* [Istio VirtualService API reference](https://istio.io[AWS_SECRET_ACCESS_KEY]/virtual-service/)
* [Envoy retry and timeout behavior](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/retry)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

That wraps up this lesson on configuring timeouts and retries with Istio VirtualServices.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/7935d043-5237-44e5-8fbf-33f442e9e765" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/78ec0f28-7be6-422f-953e-117ee5150663" />
</CardGroup>


# Demo Workload Entry

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Workload-Entry/page

Guide to installing Istio with REGISTRY_ONLY outbound policy and registering external workloads using WorkloadEntry and ServiceEntry so in-cluster pods can access a host nginx.

This tutorial demonstrates how to install Istio with a locked-down outbound traffic policy (`REGISTRY_ONLY`) and register an external workload so in-cluster pods can reach it. We'll use a host-run nginx as the external workload and show how `WorkloadEntry` and `ServiceEntry` allow pods to access it when the mesh denies unregistered outbound destinations.

## Prerequisites

* A Kubernetes cluster with kubectl access.
* curl and apt (for the control-plane host demo steps).
* istioctl (we'll download it as part of the demo).

## Verify Kubernetes is running

List all pods across namespaces to confirm your cluster is healthy:

```bash theme={null}
kubectl get pods -A
```

Example (truncated):

```text theme={null}
NAMESPACE     NAME                                      READY   STATUS    RESTARTS   AGE
kube-system   coredns-76f75df574-9pksc                   1/1     Running   0          45m
kube-system   etcd-controlplane                           1/1     Running   1 (45m ago) 45m
kube-system   kube-apiserver-controlplane                 1/1     Running   0          45m
weave-net-zs761                             2/2     Running   1 (45m ago) 45m
```

## Download and install Istio (demo: v1.18.2)

Download Istio and make `istioctl` available:

```bash theme={null}
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.18.2 sh -
export PATH="$PATH:/root/istio-1.18.2/bin"
```

Create a local copy of the `demo` profile so we can modify mesh settings:

```bash theme={null}
istioctl profile dump demo -o yaml > demo.yaml
```

Edit `demo.yaml` to set the mesh outbound traffic policy to `REGISTRY_ONLY`. Add or update the following under `meshConfig`:

```yaml theme={null}
meshConfig:
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY
  accessLogFile: /dev/stdout
  defaultConfig:
    proxyMetadata: {}
  enablePrometheusMerge: true
```

For context, the file should include the hub and the modified meshConfig:

```yaml theme={null}
hub: docker.io/istio
meshConfig:
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY
  accessLogFile: /dev/stdout
  defaultConfig:
    proxyMetadata: {}
  enablePrometheusMerge: true
```

Validate and install the modified profile:

```bash theme={null}
istioctl validate -f demo.yaml
istioctl install -f demo.yaml -y
