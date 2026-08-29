# Output will indicate Istio core, Istiod, ingress/egress gateways installed, etc.
```

Verify Istio system pods are running:

```bash theme={null}
kubectl get pods -n istio-system
```

> **warning** Setting `outboundTrafficPolicy.mode` to `REGISTRY_ONLY` blocks traffic to any destination not registered in the mesh registry. Apply this carefully in production; it can break external integrations unless those endpoints are explicitly added via ServiceEntry/WorkloadEntry.

## Simulate an external application (nginx on the host)

For this demo we simulate an external workload by running nginx on the control plane host. (In production, this would typically be a VM or cloud instance.)

Install nginx on the host:

```bash theme={null}
apt update -y && apt install nginx -y
```

Verify nginx serves locally:

```bash theme={null}
curl localhost
```

Identify the host network interface used by your CNI (weave in this demo) and note its IP (example: `10.50.0.1`):

```bash theme={null}
ip a
```

You should see the weave interface with an IP like:

```text theme={null}
4: weave: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1376 ...
    inet 10.50.0.1/16 brd 10.50.255.255 scope global weave
```

Confirm the host's nginx is reachable via that IP:

```bash theme={null}
curl http://10.50.0.1
# returns the nginx HTML
```

## Create a test pod inside the cluster (with sidecar injection enabled)

Enable Istio sidecar injection for the namespace (we use `default` here):

```bash theme={null}
kubectl label namespace default istio-injection=enabled --overwrite
```

Run a test pod with an injected sidecar:

```bash theme={null}
kubectl run test --image=nginx
kubectl get pods
# NAME   READY   STATUS    RESTARTS   AGE
# test   2/2     Running   0          10s
```

Attempt to curl the host IP from inside the pod. With `REGISTRY_ONLY` the sidecar blocks traffic to unregistered IPs and typically returns a 502:

```bash theme={null}
kubectl exec -ti test -- curl --head http://10.50.0.1
```

Example response:

```text theme={null}
HTTP/1.1 502 Bad Gateway
date: ...
server: envoy
transfer-encoding: chunked
```

> **lightbulb** Setting `meshConfig.outboundTrafficPolicy.mode` to `REGISTRY_ONLY` requires that any external service you want pods to access must be registered with Istio (via `ServiceEntry` and/or `WorkloadEntry`). Otherwise the sidecar will reject the outbound traffic.

## Register the external workload with WorkloadEntry

Create a WorkloadEntry that represents the host-run nginx. Save the following as `workload-entry.yaml`:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: WorkloadEntry
metadata:
  name: external-app-we
  namespace: default
spec:
  address: 10.50.0.1
  labels:
    app: external
```

Apply it and confirm:

```bash theme={null}
kubectl apply -f workload-entry.yaml
kubectl get we
# NAME               AGE   ADDRESS
# external-app-we    10s   10.50.0.1
```

## Create a ServiceEntry that maps a hostname to the WorkloadEntry

Create `service-entry.yaml` to define a logical hostname and connect it to the WorkloadEntry via a selector:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: external-app-se
  namespace: default
spec:
  hosts:
  - app.internal.com
  ports:
  - number: 80
    name: http
    protocol: HTTP
  resolution: STATIC
  workloadSelector:
    labels:
      app: external
```

Notes:

* `hosts` is the logical hostname clients will use, e.g. `app.internal.com`.
* `resolution: STATIC` is required when the ServiceEntry is paired with WorkloadEntry(s).
* `workloadSelector.labels` picks the WorkloadEntry(s) (or pods) with matching labels.

Apply the ServiceEntry:

```bash theme={null}
kubectl apply -f service-entry.yaml
kubectl get serviceentry
# NAME                HOSTS                 LOCATION   RESOLUTION   AGE
# external-app-se     ["app.internal.com"]             STATIC       3s
```

## Test access from the test pod via the registered hostname

From inside the `test` pod, curl the logical hostname:

```bash theme={null}
kubectl exec -ti test -- curl http://app.internal.com
```

You should receive the nginx HTML from the host because Istio now recognizes `app.internal.com` via the ServiceEntry/WorkloadEntry registration.

## Add an in-cluster pod to the same workload (WorkloadEntry label)

To show that a `WorkloadEntry` can represent multiple endpoints, create an in-cluster pod with the same label as the WorkloadEntry:

```bash theme={null}
kubectl run nginx --image=nginx --labels="app=external"
kubectl get pods
# pod/nginx created
```

Edit the pod's index page to distinguish it from the host nginx:

```bash theme={null}
kubectl exec -ti nginx -- /bin/bash
# inside the pod:
echo "This is an Nginx Pod" > /usr/share/nginx/html/index.html
curl localhost
# Output: This is an Nginx Pod
exit
```

Now requests to `app.internal.com` from the `test` pod may be served by either the external host (WorkloadEntry IP) or the in-cluster nginx pod, since they share the label and are part of the same logical service:

```bash theme={null}
kubectl exec -ti test -- curl http://app.internal.com
# This is an Nginx Pod
kubectl exec -ti test -- curl http://app.internal.com
# This is an Nginx Pod
```

Istio may load-balance traffic across the registered endpoints.

## Quick reference: WorkloadEntry vs ServiceEntry

| Resource      | Purpose                                                                                  | Key fields / notes                                                               | Example snippet                                                        |
| ------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| WorkloadEntry | Represent an external or non-Kubernetes workload (VM, bare metal, other cloud VM, or IP) | `address`, `labels`, `serviceAccount` (for mTLS), `network`, `ports`             | `apiVersion: networking.istio.io/v1beta1` <br /> `kind: WorkloadEntry` |
| ServiceEntry  | Register a service hostname into Istio and describe how to reach it                      | `hosts`, `ports`, `resolution` (`STATIC` with WorkloadEntry), `workloadSelector` | `apiVersion: networking.istio.io/v1beta1` <br /> `kind: ServiceEntry`  |

## Practical notes and reference

* WorkloadEntry lets Istio manage non-Kubernetes endpoints. Use it for VMs, bare metal, and external IPs.
* ServiceEntry maps DNS names into the mesh and describes ports/protocols and resolution. Use `workloadSelector` to attach WorkloadEntry(s).
* Common WorkloadEntry fields: `address` (IP or DNS), `serviceAccount` (if mTLS is required), `network`, `labels`, and `ports`.
* If `location` is not set in a ServiceEntry, the default is `MESH_EXTERNAL`. Use `location: MESH_INTERNAL` when the service should be considered internal to the mesh.
* When using `REGISTRY_ONLY`, ensure every external dependency is added to the registry; otherwise application traffic will be blocked.

Further reading and references:

* Istio: WorkloadEntry reference: [https://istio.io/latest/docs/reference/config/networking/workload-entry/](https://istio.io/latest/docs/reference/config/networking/workload-entry/)
* Istio: ServiceEntry reference: [https://istio.io/latest/docs/reference/config/networking/service-entry/](https://istio.io/latest/docs/reference/config/networking/service-entry/)
* Istio Traffic Management: [https://istio.io/latest/docs/concepts/traffic-management/](https://istio.io/latest/docs/concepts/traffic-management/)

Example concise references (for copy/paste):

WorkloadEntry example:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: WorkloadEntry
metadata:
  name: foo-workloads-cluster-2
spec:
  serviceAccount: foo
  network: cluster-2-network
  labels:
    app: foo
```

ServiceEntry example (MESH\_INTERNAL):

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: details-svc
spec:
  hosts:
  - details.bookinfo.com
  location: MESH_INTERNAL
  ports:
  - number: 80
    name: http
    protocol: HTTP
    targetPort: 8080
  resolution: STATIC
  workloadSelector:
    labels:
      app: details-legacy
```

That concludes the workload-entry demo and how to register external workloads when Istio outbound traffic policy is set to `REGISTRY_ONLY`.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/dc4214b4-5f6b-4481-86f4-4961223f2bf1)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/d93422f1-5d4f-4854-8032-44a3e6d01d56)


# Fault Injection

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Fault-Injection/page

Explains Istio fault injection in VirtualService to simulate delays and aborts for testing microservice resilience, scoping faults, percentages, examples, and best practices.

We previously discussed circuit breaking. Fault injection complements that work by letting you test how your services behave when their dependencies fail or slow down.

Imagine fire drills in an office or school: you run a simulated emergency to make sure people know what to do before a real fire happens. In Istio Service Mesh, fault injection is the same idea for microservices — intentionally introduce delays or errors between services to verify resilience, fallbacks, and observability.

Why use fault injection?

* Test whether your application degrades gracefully under failure.
* Verify fallback logic (for example, returning a cached response, a friendly error, or switching to a backup service).
* Ensure timeouts and retries are implemented correctly so requests don’t hang indefinitely.
* Identify bugs, misconfigurations, or missing error handling before they become live incidents.
* Build confidence that services will operate under real-world failures (Netflix’s Chaos Monkey is a well-known example of this approach).

Fault injection is not a standalone resource — it’s configured inside a VirtualService. The `fault` block sits at the same level as `route` within an HTTP route entry.

Here is a basic VirtualService that injects a delay:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: app-vs
  namespace: frontend
spec:
  hosts:
    - app-svc
  http:
    - fault:
        delay:
          percentage:
            value: 100.0
          fixedDelay: 5s
      route:
        - destination:
            host: app-svc.frontend.svc.cluster.local
            subset: v1
            port:
              number: 80
```

This configuration injects a 5-second delay for 100% of requests to `app-svc`. Use such a policy to observe how your application behaves under sustained latency and to validate timeouts, circuit breakers, and user-facing error handling.

Istio also supports aborting requests — returning an HTTP or gRPC error — as another fault injection type. Example:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: app-vs
  namespace: frontend
spec:
  hosts:
    - app-svc
  http:
    - fault:
        abort:
          percentage:
            value: 50.0
          httpStatus: 400
      route:
        - destination:
            host: app-svc.frontend.svc.cluster.local
            subset: v1
            port:
              number: 80
```

In this example, 50% of matching requests receive an HTTP 400 response. The abort fault also supports `grpcStatus` for gRPC traffic.

Fault-injection options — quick reference

| Fault Type | Key fields                                     | Description                                                                   |
| ---------- | ---------------------------------------------- | ----------------------------------------------------------------------------- |
| Delay      | `fixedDelay` (e.g., `5s`), `percentage.value`  | Injects latency to matching requests (delay duration and percent of traffic). |
| Abort      | `httpStatus`, `grpcStatus`, `percentage.value` | Returns an immediate error response (HTTP or gRPC) for part of the traffic.   |

Correct and consistent use of percentage values

* Istio uses percent values in the range 0.0 to 100.0 (for example, 10% is `value: 10.0`, not `0.1`).

Examples for small-percentage faults (10%)

Abort example (10% of requests get HTTP 400):

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
      fault:
        abort:
          percentage:
            value: 10.0
          httpStatus: 400
```

Delay example (10% of requests have a 5s delay):

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
    - reviews.prod.svc.cluster.local
  http:
    - match:
        - sourceLabels:
            env: prod
      route:
        - destination:
            host: reviews.prod.svc.cluster.local
            subset: v1
      fault:
        delay:
          percentage:
            value: 10.0
          fixedDelay: 5s
```

You can combine `match` conditions (source labels, headers, URIs, etc.) to scope faults to specific callers, namespaces, or environments.

> **lightbulb** Use fault injection carefully in production. Start with low percentages and short delays, validate application behavior, and monitor closely. Run aggressive scenarios in staging or dedicated chaos environments before widening scope in production.

Compact reference showing both Abort and Delay configurations:

```yaml theme={null}
