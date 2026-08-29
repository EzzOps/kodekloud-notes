# e.g. /root/istio-1.18.2/bin/istioctl
```

Dump the `demo` profile to a file, edit it, and change the mesh config to `REGISTRY_ONLY`:

```bash theme={null}
istioctl profile dump demo -o yaml > demo.yaml
vim demo.yaml
```

Update `meshConfig.outboundTrafficPolicy.mode` inside `demo.yaml`:

```yaml theme={null}
meshConfig:
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY
  accessLogFile: /dev/stdout
  defaultConfig:
    proxyMetadata: {}
  enablePrometheusMerge: true
```

Install Istio using the modified profile:

```bash theme={null}
istioctl install -f demo.yaml
```

Verify Istio system pods are running:

```bash theme={null}
kubectl get pods -n istio-system
```

> **lightbulb** Be aware: `REGISTRY_ONLY` blocks outbound traffic to external services unless they're registered with Istio (for example, via a ServiceEntry). Use ServiceEntry to explicitly allow specific external hosts when using this policy.

***

## 2) Create a test pod (nginx) and test connectivity before injection

Run a simple test pod. Note: the official `nginx` image may not include `curl`. If `curl` is missing, use a `curl`-enabled image (for example, `curlimages/curl`) or install `curl` in the pod.

Create and exec into the pod:

```bash theme={null}
kubectl run test --image=nginx --restart=Never
kubectl exec -ti test -- /bin/sh
```

From inside the container, test outbound access to Wikipedia (fetch headers only):

```bash theme={null}
curl --head -L http://www.wikipedia.org
```

If the pod is not Istio-injected, you should see an HTTP 301 redirect and then 200 headers:

```text theme={null}
HTTP/1.1 301 Moved Permanently
location: https://www.wikipedia.org
server: HAProxy

HTTP/2 200
server: ATS/9.2.9
content-type: text/html
...
```

Exit the pod shell:

```bash theme={null}
exit
```

***

## 3) Enable automatic sidecar injection for the namespace and re-run the test

Label the `default` namespace for Istio automatic sidecar injection, then recreate the test pod:

```bash theme={null}
kubectl label namespace default istio-injection=enabled
kubectl delete pod test
kubectl run test --image=nginx --restart=Never
kubectl get pods
# test should show 2/2 when the sidecar is injected
kubectl exec -ti test -- /bin/sh
curl --head -L http://www.wikipedia.org
```

With `outboundTrafficPolicy = REGISTRY_ONLY` and no ServiceEntry, the sidecar will block the external request. The sidecar returns a 502 Bad Gateway:

```text theme={null}
HTTP/1.1 502 Bad Gateway
date: ...
server: envoy
```

Exit the pod shell:

```bash theme={null}
exit
```

> **lightbulb** Labeling a namespace with `istio-injection=enabled` enables automatic sidecar injection for new pods in that namespace. Existing pods must be recreated to receive a sidecar.

***

## 4) Create a ServiceEntry for [www.wikipedia.org](http://www.wikipedia.org) to allow egress

Create a ServiceEntry in the same namespace as the test pod (default) to register `www.wikipedia.org` with Istio so sidecars can allow and route traffic.

service\_entry.yaml

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: wikipedia-egress
spec:
  hosts:
  - www.wikipedia.org
  ports:
  - number: 80
    name: http
    protocol: HTTP
  - number: 443
    name: https
    protocol: HTTPS
  resolution: DNS
  location: MESH_EXTERNAL
```

Apply the ServiceEntry:

```bash theme={null}
kubectl apply -f service_entry.yaml
kubectl get serviceentries.networking.istio.io
# Should show wikipedia-egress in default namespace
```

Exec into the test pod and retry the curl. With the ServiceEntry present, you should see 301 → 200 responses:

```bash theme={null}
kubectl exec -ti test -- /bin/sh
curl --head -L http://www.wikipedia.org
# expect 301 -> 200 responses
exit
```

***

## 5) Configure an Egress Gateway, DestinationRule, and VirtualService

To route mesh-originating traffic through an Istio egress gateway, create three resources:

* Gateway that selects the egress gateway pod (selector must match egress pod labels).
* DestinationRule pointing to the egress gateway service/subset.
* VirtualService that routes mesh traffic to the egress gateway and configures how the egress gateway forwards to the external host.

Confirm the egress gateway pod and labels:

```bash theme={null}
kubectl get pods -n istio-system --show-labels
# Look for egress gateway pod labels, e.g. istio=egressgateway or app=istio-egressgateway
```

Create the Gateway selecting the egress gateway (selector must match labels):

gateway.yaml

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: istio-egressgateway
spec:
  selector:
    istio: egressgateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - www.wikipedia.org
```

Apply the Gateway:

```bash theme={null}
kubectl apply -f gateway.yaml
kubectl get gateways.networking.istio.io
```

Create a DestinationRule that points traffic to the egress gateway service from the `default` namespace:

destinationrule.yaml

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: egressgateway-for-wikipedia
  namespace: default
spec:
  host: istio-egressgateway.istio-system.svc.cluster.local
  subsets:
    - name: wikipedia
```

Apply the DestinationRule:

```bash theme={null}
kubectl apply -f destinationrule.yaml
kubectl get destinationrules.networking.istio.io
```

Now create the VirtualService that handles two routing phases:

* mesh-originating requests: match `gateways: [mesh]` and route to the egress gateway service subset.
* gateway-handled requests: match `gateways: [istio-egressgateway]` and forward to the external host.

virtualservice.yaml

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: wikipedia-egress-gateway
spec:
  hosts:
    - www.wikipedia.org
  gateways:
    - istio-egressgateway
    - mesh
  http:
    - match:
        - gateways:
            - mesh
          port: 80
      route:
        - destination:
            host: istio-egressgateway.istio-system.svc.cluster.local
            subset: wikipedia
            port:
              number: 80
          weight: 100
    - match:
        - gateways:
            - istio-egressgateway
          port: 80
      route:
        - destination:
            host: www.wikipedia.org
            port:
              number: 80
          weight: 100
```

Apply the VirtualService:

```bash theme={null}
kubectl apply -f virtualservice.yaml
kubectl get virtualservices.networking.istio.io
# Should list wikipedia-egress-gateway with gateways ["istio-egressgateway","mesh"]
```

***

## 6) Verify traffic flows through the egress gateway and tail logs

Tail logs from the egress gateway deployment in one terminal (replace resource if different):

```bash theme={null}
kubectl logs -f -n istio-system deployment/istio-egressgateway
```

In another terminal, exec into the test pod and perform the request:

```bash theme={null}
kubectl exec -ti test -- /bin/sh
curl --head -L http://www.wikipedia.org
exit
```

Expected results:

* The test pod still sees the normal 301 → 200 responses.
* Egress gateway logs include the forwarded request. Example Envoy log snippet:

```text theme={null}
"HEAD / HTTP/2" 301 - via_upstream ... "www.wikipedia.org" "208.80.153.224:80" outbound|80||www.wikipedia.org ...
```

> **warning** Important: To force mesh-originating traffic through an Istio egress gateway, the VirtualService must include the `mesh` gateway in `gateways` and have a `match` for `gateways: [mesh]`. Without this, sidecar proxies are not instructed to route to the egress gateway and traffic may go directly to the Internet or be blocked by `REGISTRY_ONLY`.

***

## 7) Example: VirtualService without mesh vs with mesh

VirtualService that only lists the egress gateway (no `mesh`) — this handles requests arriving at the egress gateway but does not instruct pods inside the mesh to send requests to the gateway:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: wikipedia-egress-gateway-no-mesh
spec:
  hosts:
    - www.wikipedia.org
  gateways:
    - istio-egressgateway
  http:
    - match:
        - gateways:
            - istio-egressgateway
          port: 80
      route:
        - destination:
            host: www.wikipedia.org
            port:
              number: 80
          weight: 100
```

The VirtualService shown in step 5 (the `virtualservice.yaml`) includes `mesh` and explicitly routes mesh-originating traffic to the egress gateway before the gateway forwards it to the external host.

***

## 8) Notes, exam tips, and quick reference

* ServiceEntry registers external services (DNS hosts, IPs, ranges) with Istio so sidecars will allow and route egress traffic when outbound policy is `REGISTRY_ONLY`.
* Egress gateway pattern typically uses three resources:
  * Gateway: selects the egress proxy pod.
  * DestinationRule: targets the egress gateway service/subset.
  * VirtualService: routes mesh traffic to the gateway and gateway traffic to the external host.
* For exams and real-world tasks: keep templates handy and update `hosts`, `ports`, `resolution`, and `namespaces` quickly.
* Many orgs do not send all Internet traffic through an egress gateway, but doing so enables centralized monitoring, policy enforcement, and security controls.

Resources quick reference:

| Resource        | Purpose                                                     | Example location                                                         |
| --------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------ |
| ServiceEntry    | Register external host(s) so sidecars permit egress         | `default` namespace                                                      |
| Gateway         | Selects egress gateway pod and defines server/host          | `istio-system` (egressgateway)                                           |
| DestinationRule | Directs traffic to egress gateway service/subset            | `default` (targets `istio-egressgateway.istio-system.svc.cluster.local`) |
| VirtualService  | Routes mesh -> egress gateway, and gateway -> external host | `default` namespace                                                      |

***

## 9) Useful ServiceEntry examples

ServiceEntry for multiple HTTPS external hosts:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: external-svc-https
spec:
  hosts:
    - api.dropboxapi.com
    - www.googleapis.com
    - api.facebook.com
  location: MESH_EXTERNAL
  ports:
    - number: 443
      name: https
      protocol: TLS
  resolution: DNS
```

ServiceEntry for external cluster with static endpoints:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: external-svc-mongocluster
spec:
  hosts:
    - mymongodb.somedomain
  addresses:
    - 192.192.192.192/24
  ports:
    - number: 27018
      name: mongod
      protocol: MONGO
  location: MESH_INTERNAL
  resolution: STATIC
  endpoints:
    - address: 2.2.2.2
    - address: 3.3.3.3
```

Wildcard host ServiceEntry:

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: external-svc-wildcard-example
spec:
  hosts:
    - "*.bar.com"
  location: MESH_EXTERNAL
  ports:
    - number: 80
      name: http
      protocol: HTTP
  resolution: NONE
```

***

That wraps up ServiceEntry and egress gateway basics. Practice creating these manifests and verifying behavior by tailing egress gateway logs and testing from pods both with and without sidecar injection.

Links and references:

* [Istio Networking Concepts](https://istio.io/latest/docs/concepts/traffic-management/)
* [Istio ServiceEntry docs](https://istio.io/latest/docs/reference/config/networking/service-entry/)
* [Istio Egress Gateway example](https://istio.io/latest/docs/tasks/traffic-management/egress/egress-gateway/)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/5674ec14-32a4-48c3-bb67-a08d54199396)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/0b5f42c9-6182-4747-8253-554ce30147dc)


# Demo 2 Service Entries

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-2-Service-Entries/page

Demonstrates using Istio ServiceEntry and VirtualService to register and route traffic to an external host and ensure sidecar injection intercepts traffic.

In this lesson we demonstrate how to use an Istio ServiceEntry to register an external workload with the mesh (by static IP) and then route mesh traffic to that external endpoint using a VirtualService. This pattern is useful when you must bring externally-resolved services into the mesh without changing an outbound registry-only policy. It matches a common scenario in the Prep Course - Istio Certified Associate (ICA) Certification.

## What you'll accomplish

* Register an external host (myapp.com) and a static endpoint with a ServiceEntry.
* Configure a VirtualService so the mesh routes HTTP traffic to that external endpoint.
* Verify traffic is intercepted by the Istio sidecar and routed correctly.

## Prerequisites / quick checks

* Istio is already installed and running.
* An external NGINX server is reachable at `myapp.com`. In this lab environment this hostname is mapped to a local IP via `/etc/hosts`.

Recommended verification commands:

```bash theme={null}
kubectl get pods -A
istioctl version
```

Confirm the external web app is resolvable and responding from the control-plane host:

```bash theme={null}
curl myapp.com
```

A successful response will look like the NGINX welcome page (truncated):

```html theme={null}
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and working.</p>
...
</html>
```

Verify the `/etc/hosts` mapping:

```bash theme={null}
cat /etc/hosts
```

Example entry:

```text theme={null}
192.168.121.2 myapp.com
```

## Why use a ServiceEntry?

A ServiceEntry tells Istio how to resolve and route traffic for hosts that are outside the mesh. Use `MESH_EXTERNAL` for workloads outside the cluster and `resolution: STATIC` when you want to bind a fixed IP endpoint to a hostname.

> **lightbulb** We use `MESH_EXTERNAL` because the workload is outside the mesh. Use `resolution: STATIC` for fixed IPs; use `resolution: DNS` for externally resolved hostnames.

## 1) Create a ServiceEntry

Create a file named `se.yaml`. Replace the `address` value with the IP you observed from `/etc/hosts`.

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: myapp-service-entry
spec:
  hosts:
    - myapp.com
  location: MESH_EXTERNAL
  ports:
    - number: 80
      name: http
      protocol: HTTP
  resolution: STATIC
  endpoints:
    - address: 192.168.121.2
```

Apply and verify the ServiceEntry:

```bash theme={null}
kubectl apply -f se.yaml
kubectl get serviceentries.networking.istio.io
```

Expected output:

```text theme={null}
NAME                   HOSTS               LOCATION       RESOLUTION   AGE
myapp-service-entry    ["myapp.com"]       MESH_EXTERNAL  STATIC       30s
```

## 2) Run a test pod and try to curl

Start a simple test pod. The `nginx` image often includes `curl`; if not, use a curl-specific image (e.g., `curlimages/curl`).

```bash theme={null}
kubectl run test --image=nginx --restart=Never
kubectl get pods
```

Exec into the pod and attempt to curl the host:

```bash theme={null}
kubectl exec test -- curl myapp.com -s -S
```

You might see a redirect or unexpected HTML (e.g., `302 Found`). This indicates the ServiceEntry is present but Istio is not yet performing HTTP routing for the host — a VirtualService is required.

## 3) Create a VirtualService

Create `vs.yaml` to capture HTTP traffic for `myapp.com` and forward it to the destination that matches the ServiceEntry.

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: myapp-vs
spec:
  hosts:
    - myapp.com
  http:
    - route:
        - destination:
            host: myapp.com
            port:
              number: 80
```

Apply and check the VirtualService:

```bash theme={null}
kubectl apply -f vs.yaml
kubectl get virtualservices
```

Expected output:

```text theme={null}
NAME       GATEWAYS  HOSTS           AGE
myapp-vs             ["myapp.com"]   4s
```

## 4) Re-test from the test pod

Try curling again from the `test` pod:

```bash theme={null}
kubectl exec test -- curl myapp.com -s -S
```

If the response is still incorrect, confirm whether the test pod has an Istio sidecar. Istio must intercept the pod’s traffic for the ServiceEntry + VirtualService routing to work.

Check pod readiness and namespace labels:

```bash theme={null}
kubectl get pods
kubectl get ns --show-labels
```

Run istioctl analyze for hints:

```bash theme={null}
istioctl analyze
```

Sample analyzer message when namespace injection is disabled:

```text theme={null}
Info [IST0102] (Namespace default) The namespace is not enabled for Istio injection. Run 'kubectl label namespace default istio-injection=enabled' to enable it, or 'kubectl label namespace default istio-injection=disabled' to explicitly mark it as not needing injection.
```

## 5) Enable automatic sidecar injection and recreate the test pod

Label the namespace for injection so new pods receive the Envoy sidecar. Then recreate the test pod.

```bash theme={null}
kubectl label namespace default istio-injection=enabled
kubectl delete pod test
kubectl run test --image=nginx --restart=Never
kubectl get pods
```

The `test` pod should now show `2/2` (application container + sidecar):

```text theme={null}
NAME   READY   STATUS    RESTARTS   AGE
test   2/2     Running   0          30s
```

## Final curl — success

From the injected `test` pod, curl the external host again:

```bash theme={null}
kubectl exec test -- curl myapp.com -s -S
```

You should now receive the expected NGINX default page served from the externally-registered endpoint. This confirms the mesh intercepted the traffic, the VirtualService matched and routed it to the ServiceEntry endpoint.

## Summary / Key takeaways

* ServiceEntry registers external hosts and endpoints with the mesh.
* VirtualService captures and routes HTTP traffic for hosts — including external hosts defined by ServiceEntry.
* Pods must have the Istio sidecar (injected) for the mesh to intercept and route their traffic.
* Label namespaces for automatic injection before creating pods that need to be part of the mesh.

## Quick reference table

| Resource Type   | Purpose                                                    | Example                                                   |
| --------------- | ---------------------------------------------------------- | --------------------------------------------------------- |
| ServiceEntry    | Register external host and endpoints with the mesh         | See `se.yaml` above                                       |
| VirtualService  | Capture and route HTTP traffic for a host to a destination | See `vs.yaml` above                                       |
| Namespace label | Enable automatic sidecar injection for new pods            | `kubectl label namespace default istio-injection=enabled` |

## Links and references

* [Istio Networking Concepts](https://istio.io/latest/docs/concepts/traffic-management/)
* [ServiceEntry API reference](https://istio.io/latest/docs/reference/config/networking/service-entry/)
* [VirtualService API reference](https://istio.io/latest/docs/reference/config/networking/virtual-service/)

Give this a try in the labs to get hands-on experience bringing external workloads into the mesh.

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/68e4e6ad-3398-4e12-a666-5b9f96fda7d2)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/b96f41b7-7bd2-4022-b388-701bec8e39ff)
