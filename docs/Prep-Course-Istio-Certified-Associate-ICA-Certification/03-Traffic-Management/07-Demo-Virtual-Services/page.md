# ... other services and deployments created
```

Check pods. Initially, some pods may show `0/2` while they initialize — those indicate the Envoy sidecar is being injected (1 container for your app + 1 for Envoy):

```bash theme={null}
kubectl get pods
```

Example:

```plaintext theme={null}
NAME                               READY   STATUS            RESTARTS   AGE
details-v1-65599dcf88-56xsj       2/2     Running           0          23s
productpage-v1-9487c9b5b-k91sp    2/2     Running           0          22s
ratings-v1-59b99c644-5shkc        0/2     PodInitializing   0          23s
reviews-v1-598599854-bvf9         0/2     PodInitializing   0          23s
```

***

## 2) Create a non-injected namespace and run a client pod

Create a new namespace `test` (by default it will not have the `istio-injection=enabled` label):

```bash theme={null}
kubectl create ns test
kubectl get ns --show-labels
```

Example output showing `test` is not injected:

```plaintext theme={null}
NAME              STATUS   AGE     LABELS
default           Active   5m11s  istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system      Active   2m40s  kubernetes.io/metadata.name=istio-system
test              Active   8s     kubernetes.io/metadata.name=test
```

Run a simple nginx pod in the `test` namespace (no sidecar will be injected):

```bash theme={null}
kubectl run test --image=nginx -n test
kubectl get pods -n test
```

Example:

```plaintext theme={null}
NAME    READY   STATUS    RESTARTS   AGE
test    1/1     Running   0          12s
```

Exec into the test pod and curl the Bookinfo `productpage` service in the `default` namespace (productpage runs on port 9080):

```bash theme={null}
kubectl exec -ti -n test test -- /bin/bash
# inside pod
curl --head productpage.default.svc.cluster.local:9080
```

You should get an HTTP 200 response proxied through Envoy, indicating the request reached Bookinfo (Envoy is the server in headers):

```plaintext theme={null}
HTTP/1.1 200 OK
content-type: text/html; charset=utf-8
content-length: 1683
server: istio-envoy
x-envoy-upstream-service-time: 27
```

Note: Istio by default allows traffic to flow (so you can adopt policies later without breaking initial connectivity).

***

## 3) Apply PeerAuthentication (mTLS STRICT) in default namespace

Create a `PeerAuthentication` resource to enforce strict mTLS for the `default` namespace:

peer\_auth.yaml

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: STRICT
```

Apply it:

```bash theme={null}
kubectl apply -f peer_auth.yaml
```

Then from your non-injected `test` pod, try to curl `productpage` again:

```bash theme={null}
kubectl exec -ti -n test test -- /bin/bash
# inside pod
curl --head productpage.default.svc.cluster.local:9080
```

You will see a failure like:

```plaintext theme={null}
curl: (56) Recv failure: Connection reset by peer
```

This happens because `default` now requires mTLS. Only traffic routed through an Istio sidecar (Envoy) can satisfy that requirement — and the `test` pod currently has no sidecar.

<Callout icon="warning">
  Applying a `PeerAuthentication` with `mtls: STRICT` enforces mutual TLS for all workloads in the target namespace. Clients without an Envoy sidecar will fail to connect until they are inside an injected namespace or a policy allows plaintext.
</Callout>

***

## 4) Enable injection on the `test` namespace and re-run the client

Label the `test` namespace to enable automatic sidecar injection:

```bash theme={null}
kubectl label namespace test istio-injection=enabled
kubectl get ns --show-labels
```

Example output:

```plaintext theme={null}
NAME      STATUS   AGE     LABELS
test      Active   4m55s   istio-injection=enabled,kubernetes.io/metadata.name=test
default   Active   9m58s   istio-injection=enabled,kubernetes.io/metadata.name=default
```

Delete and recreate the `test` pod (or simply delete it and let the controller recreate it) so the sidecar gets injected:

```bash theme={null}
kubectl delete pod -n test test
kubectl run test --image=nginx -n test
kubectl get pods -n test
```

You should now see `1/2` or `2/2` as the pod becomes injected and ready (1 app container + 1 envoy) — e.g. `1/2` then `2/2`.

Exec into the test pod and curl again:

```bash theme={null}
kubectl exec -ti -n test test -- /bin/bash
# inside pod
curl --head productpage.default.svc.cluster.local:9080
```

Now the request should succeed because the Envoy sidecar on the client pod performs mTLS with the server sidecar.

Example response:

```plaintext theme={null}
HTTP/1.1 200 OK
content-type: text/html; charset=utf-8
content-length: 1683
server: envoy
x-envoy-upstream-service-time: 21
```

***

## 5) Introduce a Sidecar resource to restrict egress

A `Sidecar` resource allows you to restrict egress (outbound) and ingress for sidecars in a namespace or for selected workloads.

Create a Sidecar that restricts egress to itself and the `istio-system` namespace:

sidecar\_default\_namespace.yaml

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: default
  namespace: test
spec:
  egress:
  - hosts:
    - "./*"
    - "istio-system/*"
```

Apply it:

```bash theme={null}
kubectl apply -f sidecar_default_namespace.yaml
```

Now exec into the `test` pod and try curling `productpage` (in `default` namespace):

```bash theme={null}
kubectl exec -ti -n test test -- /bin/bash
# inside pod
curl --head productpage.default.svc:9080
```

You may see:

```plaintext theme={null}
curl: (52) Empty reply from server
```

Why? Because the `Sidecar` resource limited egress to only workloads in the same namespace (`./*`) and `istio-system/*`. The `default` namespace is not allowed, so traffic to `default` is blocked.

### Allow the `default` namespace in the Sidecar

Update the Sidecar to permit `default/*` as well:

sidecar\_default\_namespace.yaml (updated)

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: default
  namespace: test
spec:
  egress:
  - hosts:
    - "./*"
    - "default/*"
    - "istio-system/*"
```

Apply and retry; the curl should return HTTP 200 again.

***

## 6) Restrict only selected workloads via workloadSelector

You can target only specific workloads (pods) in the namespace using `workloadSelector` and labels.

Example: restrict egress for workloads labeled `run=test`:

sidecar\_default\_namespace.yaml (workload-scoped)

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: default
  namespace: test
spec:
  workloadSelector:
    labels:
      run: test
  egress:
  - hosts:
    - "./*"
    - "istio-system/*"
```

Apply this configuration:

```bash theme={null}
kubectl apply -f sidecar_default_namespace.yaml
```

Effect:

* Pods in the `test` namespace with label `run=test` will be limited to `./*` and `istio-system/*` — they cannot access `default/*`.
* Other pods in the same namespace (for example, a pod labeled `run=nginx`) will not be affected and can still access `default/*` (unless another Sidecar matches them).

Demonstration:

* Create another pod in `test` named `nginx` (default label will be `run=nginx`).
* `kubectl exec` into `nginx` and curl productpage — it will succeed.
* `kubectl exec` into the `test` pod (`run=test`) and curl productpage — it will fail with `Empty reply from server`.

This shows how Sidecars with `workloadSelector` allow per-workload egress control.

***

## Sidecar quick reference

| Field                   | Description                                                    | Example                                  |
| ----------------------- | -------------------------------------------------------------- | ---------------------------------------- |
| `metadata.name`         | Name of the Sidecar resource                                   | `default`                                |
| `metadata.namespace`    | Namespace where the Sidecar applies                            | `test`                                   |
| `spec.egress`           | List of allowed egress hosts (namespace/workload)              | `["./*", "default/*", "istio-system/*"]` |
| `spec.workloadSelector` | Optional selector to target specific workloads by labels       | `labels: { run: test }`                  |
| `spec.ingress`          | Optional inbound ports/protocols and `defaultEndpoint` for UDS | See Istio docs                           |

***

## Useful commands summary

```bash theme={null}
# List namespaces and labels
kubectl get ns --show-labels

# Deploy Bookinfo (example)
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.11/samples/bookinfo/platform/kube/bookinfo.yaml

# Create namespace
kubectl create ns test

# Label namespace for injection
kubectl label namespace test istio-injection=enabled

# Create a test pod
kubectl run test --image=nginx -n test

# Exec into pod
kubectl exec -ti -n test test -- /bin/bash

# Curl productpage from pod
curl --head productpage.default.svc.cluster.local:9080

# Apply PeerAuthentication
kubectl apply -f peer_auth.yaml

# Apply Sidecar
kubectl apply -f sidecar_default_namespace.yaml
```

***

## References and further reading

<Callout icon="lightbulb">
  Helpful resources:

  * Istio Sidecar reference: [https://istio.io/latest/docs/reference/config/networking/sidecar/](https://istio.io/latest/docs/reference/config/networking/sidecar/)
  * Istio PeerAuthentication reference: [https://istio.io/latest/docs/reference/config/security/peer\_authentication/](https://istio.io/latest/docs/reference/config/security/peer_authentication/)
</Callout>

***

## Wrap-up

* Applying a `PeerAuthentication` with `mtls: STRICT` enforces mutual TLS and requires clients to use sidecars for encryption.
* Enabling `istio-injection=enabled` on a namespace ensures sidecars are injected into pods and allows them to participate in mTLS.
* `Sidecar` resources allow fine-grained egress and ingress control at namespace or workload level using `egress`, `ingress`, and `workloadSelector`.
* Use the Istio docs to copy Sidecar/PeerAuth examples rather than typing them during troubleshooting or exams.

Next up: VirtualServices and traffic routing.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/22d5c51f-0040-4a81-9b18-e129f8a1d3ba" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/c60cca75-b26e-4899-89b2-38a99c2f8a5a" />
</CardGroup>


# Demo Virtual Services

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Virtual-Services/page

Demonstrates configuring and testing an Istio VirtualService for an httpbin app including routing, namespace sidecar injection effects, port misrouting, and URL rewrite examples

In this demo we configure a simple Istio VirtualService for an httpbin sample app. VirtualServices are a core Istio resource — they control how requests are routed within the mesh and are required by many other features (gateways, retries, rewrites, etc.). This walkthrough covers:

* Verifying Istio injection
* Deploying httpbin
* Creating a test pod in a separate namespace
* Creating and applying a VirtualService
* Demonstrating how namespace injection affects routing
* URL rewrites
* Quick reference of common VirtualService features

***

## 1. Verify Istio injection in namespaces

Check namespace labels to see whether `istio-injection` is enabled:

```bash theme={null}
kubectl get ns --show-labels
```

Example output:

```text theme={null}
NAME              STATUS   AGE   LABELS
default           Active   15m   istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system      Active   12m   kubernetes.io/metadata.name=istio-system
kube-node-lease   Active   15m   kubernetes.io/metadata.name=kube-node-lease
kube-public       Active   15m   kubernetes.io/metadata.name=kube-public
kube-system       Active   15m   kubernetes.io/metadata.name=kube-system
```

***

## 2. Deploy the httpbin sample app

Deploy the httpbin sample from the Istio repository:

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.com/istio/istio/refs/heads/master/samples/httpbin/httpbin.yaml
```

Confirm the `httpbin` pod is running and has a sidecar (2/2 ready):

```bash theme={null}
kubectl get pods
```

Example:

```text theme={null}
NAME                        READY   STATUS    RESTARTS   AGE
httpbin-787cdcc9df-h5q2     2/2     Running   0          7s
```

***

## 3. Create a separate namespace and a test pod

Create a `test` namespace and run a simple `nginx` pod there:

```bash theme={null}
kubectl create ns test
kubectl run test --image=nginx -n test
kubectl get pods -n test
```

Example pod status (without injection):

```text theme={null}
NAME   READY   STATUS    RESTARTS   AGE
test   1/1     Running   0          5s
```

A `1/1` READY means the Istio sidecar is not injected into this pod. We’ll use this to demonstrate how VirtualService behavior depends on sidecar injection.

***

## 4. Test connectivity from the non-injected test pod

Exec into the `test` pod and curl the httpbin service in the `default` namespace:

```bash theme={null}
kubectl exec -ti -n test test -- /bin/bash
