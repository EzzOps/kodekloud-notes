# virtualservice.networking.istio.io/book-info-vs created
```

At this point the VirtualService works for internal cluster traffic using the host `productpage`. To expose Bookinfo externally we need a Gateway and then update the VirtualService to reference that Gateway and the external host header.

First, identify the label used by the Istio ingress pod so the Gateway selects the correct ingress proxy. Describe the ingress pod (replace the pod name with yours if different):

```bash theme={null}
kubectl describe pod -n istio-system istio-ingress-6cf77d4858-g2cvz
```

Look at the Labels section. Example labels you may see:

```plaintext theme={null}
Labels:
  app=istio-ingress
  app.kubernetes.io/name=istio-ingress
  service.istio.io/canonical-name=istio-ingress
  sidecar.istio.io/inject=true
```

<Callout icon="lightbulb">
  Make sure your Gateway's selector uses the exact label key/value present on your ingress pods (for example `istio=ingress` or `app=istio-ingress`). If the selector doesn't match, the Gateway will not bind to the ingress proxy.
</Callout>

Create the Gateway in the `default` namespace (so it pairs with the VirtualService). Save this as `gw.yaml`:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: istio-gateway
spec:
  selector:
    app: istio-ingress
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "book.info.com"
```

Apply the Gateway:

```bash theme={null}
kubectl apply -f gw.yaml
# gateway.networking.istio.io/istio-gateway created
```

Now update the VirtualService (`vs.yaml`) so it can be invoked via the external host `book.info.com` and is bound to the Gateway:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: book-info-vs
spec:
  hosts:
    - "book.info.com"
    - productpage
  gateways:
    - istio-gateway
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: productpage.default.svc.cluster.local
            port:
              number: 9080
```

Apply the updated VirtualService:

```bash theme={null}
kubectl apply -f vs.yaml
# virtualservice.networking.istio.io/book-info-vs configured
```

Determine how the ingress is exposed. In some lab environments (kubeadm) Istio's ingress service is a NodePort; in cloud environments it will usually be a LoadBalancer. Inspect the Istio services:

```bash theme={null}
kubectl get svc -n istio-system
```

Note: different Istio installs may use slightly different resource names (for example some use istio-ingress while others use istio-ingressgateway). Use the service name you have in your cluster when determining access details.

Example (kubeadm lab with NodePort):

```plaintext theme={null}
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
istio-egress    ClusterIP   10.98.33.91     <none>        15021/TCP,80/TCP,443/TCP
istio-ingress   NodePort    10.97.88.127    <none>        15021:38117/TCP,80:30992/TCP,443:30171/TCP
istiod          ClusterIP   10.111.147.170  <none>        15010/TCP,15012/TCP,443/TCP,15014/TCP
```

Testing the Gateway

* From within the cluster or a node that can reach ClusterIP, you can curl the ClusterIP directly and set the Host header to `book.info.com`.
* From outside the cluster when using NodePort, use `node-ip:nodePort`.
* From outside the cluster when using LoadBalancer, use the EXTERNAL-IP (or hostname) provided.

Example curl from a node that can reach the ClusterIP (replace IP with your istio-ingress CLUSTER-IP):

```bash theme={null}
curl --head --header "Host: book.info.com" http://10.97.88.127
```

If the VirtualService is still only configured for `productpage` and not the external host, you'll see a 404 Not Found. After updating the VirtualService to include the host and gateway, retry:

```bash theme={null}
curl --head --header "Host: book.info.com" http://10.97.88.127
```

Expected response (after configuration):

```plaintext theme={null}
HTTP/1.1 200 OK
content-type: text/html; charset=utf-8
content-length: 1683
server: istio-envoy
date: Fri, 11 Apr 2025 21:35:57 GMT
x-envoy-upstream-service-time: 21
```

Once configured correctly, requests whose Host header matches `book.info.com` will be accepted by the Gateway on port 80 and routed via the VirtualService to the `productpage` service.

<Callout icon="lightbulb">
  If you are testing from a machine outside the cluster without DNS for book.info.com, pass the Host header with curl (as above) or add a local /etc/hosts entry pointing book.info.com to the load balancer or node IP for convenient testing.
</Callout>

Cloud example: LoadBalancer behavior

If Istio is installed on a cloud provider (EKS, AKS, GKE), the istio-ingressgateway service typically becomes a LoadBalancer with an external IP/hostname. Example after installing Istio in a cloud cluster:

```bash theme={null}
kubectl get svc -n istio-system
```

Example output (LoadBalancer in EKS/AWS):

```plaintext theme={null}
NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP                                                                 AGE
istio-egressgateway     ClusterIP      10.100.13.95    <none>                                                                      84s
istio-ingressgateway    LoadBalancer   10.100.188.237  ab6be537f8134cc084b21378582fc75-477874693.us-east-1.elb.amazonaws.com   84s
istiod                  ClusterIP      10.100.65.152   <none>                                                                      93s
```

You can point a DNS record (e.g., `book.info.com`) to the LoadBalancer's external hostname/IP and then simply curl `http://book.info.com` without manually sending the Host header.

Summary

* Create a VirtualService for the internal service.
* Create a Gateway that selects the Istio ingress pod using the correct label.
* Update the VirtualService to include the external host and reference the Gateway (via `gateways`).
* Test using the appropriate endpoint (ClusterIP for in-cluster tests, nodeIP:nodePort for NodePort from outside, or external LoadBalancer IP/hostname for cloud installations).

Thank you.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/0489a47d-305a-4e60-8a03-5742192bc357" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/8a471175-53e2-4d14-95ce-aa3721c7ef20" />
</CardGroup>


# Demo Mirroring

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Mirroring/page

Configures Istio traffic mirroring to send copies of live requests from primary v1 to secondary v2 for testing, logging, debugging, or canary analysis while preserving client responses.

In this lesson we configure traffic mirroring with Istio. Traffic mirroring lets you send a copy of live requests to a secondary subset (for testing, canary analysis, logging, or debugging) while the primary subset continues to serve real user traffic.

<Callout icon="lightbulb">
  Make sure the namespace where you deploy your workloads has Istio sidecar injection enabled. Istio features (including mirroring) require injection to be active for the namespace.
</Callout>

Overview:

* Primary goal: route 100% of client traffic to `v1` while mirroring copies of those requests to `v2`.
* Components used: Kubernetes Deployments, Service, Istio DestinationRule and VirtualService.
* Key Istio concepts: subsets (DestinationRule), `mirror` and `mirrorPercentage` (VirtualService).

## 1. Verify namespace injection

Confirm which namespaces have Istio sidecar injection enabled:

```bash theme={null}
kubectl get ns --show-labels
```

Sample output:

```bash theme={null}
NAME              STATUS   AGE     LABELS
default           Active   2m38s   istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system      Active   2m6s    kubernetes.io/metadata.name=istio-system
kube-node-lease   Active   2m38s   kubernetes.io/metadata.name=kube-node-lease
kube-public       Active   2m38s   kubernetes.io/metadata.name=kube-public
kube-system       Active   2m38s   kubernetes.io/metadata.name=kube-system
```

If the target namespace is not labeled with `istio-injection=enabled`, enable injection before deploying the workloads.

## 2. Deploy two echo-server versions (v1 and v2)

Create a single YAML containing two Deployments: `echo-server-v1` and `echo-server-v2`. Both share `app: echo-server` but use different `version` labels so Istio can create subsets that map to those versions.

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echo-server-v1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: echo-server
      version: v1
  template:
    metadata:
      labels:
        app: echo-server
        version: v1
    spec:
      containers:
      - name: echo
        image: ealen/echo-server
        ports:
        - containerPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echo-server-v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: echo-server
      version: v2
  template:
    metadata:
      labels:
        app: echo-server
        version: v2
    spec:
      containers:
      - name: echo
        image: ealen/echo-server
        ports:
        - containerPort: 80
```

Apply and verify the pods and labels:

```bash theme={null}
kubectl apply -f echo-deployment.yaml
kubectl get pods --show-labels
```

Sample output (labels show `app=echo-server` and `version`):

```bash theme={null}
NAME                                READY   STATUS    RESTARTS   AGE     LABELS
echo-server-v1-59ff75d58-t4dq6      1/2     Running   0          7s      app=echo-server,pod-template-hash=59ff75d58,version=v1,security.istio.io/tlsMode=is
echo-server-v2-5698db4f99-lm5ss     2/2     Running   0          7s      app=echo-server,pod-template-hash=5698db4f99,version=v2,security.istio.io/tlsMode=is,service.istio.io/canonical-name=echo-server,service.istio.io/canonical-revision=v2
```

## 3. Create a Service for the echo servers

Expose both versions through a ClusterIP Service that selects on `app: echo-server` so client traffic can reach either subset depending on routing rules.

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

Apply and confirm the service:

```bash theme={null}
kubectl apply -f echo-svc.yaml
kubectl get svc --show-labels
```

Sample output:

```bash theme={null}
NAME           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE    LABELS
echo-server    ClusterIP   10.98.188.49   <none>        80/TCP     5s     app=echo-server
kubernetes     ClusterIP   10.96.0.1      <none>        443/TCP    4m28s  component=apiserver,provider=kubernetes
```

## 4. Tail logs for both versions

Open two terminals (or background one process) and stream logs from each pod to observe how mirrored requests appear in the mirror target.

Terminal A (v1):

```bash theme={null}
kubectl logs -f echo-server-v1-59ff75d58-t4dq6
```

Sample v1 log lines:

```json theme={null}
{"name":"echo-server","hostname":"echo-server-v1-59ff75d58-t4dq6","msg":"[GET] - /","time":"2025-04-11T16:26:41.095Z"}
```

Terminal B (v2):

```bash theme={null}
kubectl logs -f echo-server-v2-5698db4f99-lm5ss
```

Sample v2 log lines:

```json theme={null}
{"name":"echo-server","hostname":"echo-server-v2-5698db4f99-lm5ss","msg":"[GET] - /","time":"2025-04-11T16:26:39.998Z"}
```

Keep these logs visible while you generate traffic so you can correlate client requests to backend activity.

## 5. Create a test pod to generate traffic

Run a small pod you can exec into for curl-based testing:

```bash theme={null}
kubectl run test --image=nginx --restart=Never
kubectl exec -it test -- /bin/bash
```

From inside the `test` pod, call the echo service repeatedly and extract the responding pod hostname. The echo server returns JSON with a `hostname` field; use grep and sed to print it cleanly:

```bash theme={null}
curl -s http://echo-server | grep -o '"hostname":"[^"]*"' | sed 's/"hostname":"\(.*\)"/HOSTNAME: \1/'
```

Example outputs will indicate which backend served each request:

```bash theme={null}
HOSTNAME: echo-server-v2-5698db4f99-lm5ss
HOSTNAME: echo-server-v1-59ff75d58-t4dq6
```

Watch the logs from step 4 to see mirrored requests appear in `v2` while responses come from `v1`.

## 6. Define DestinationRule with subsets

Create an Istio DestinationRule that defines `v1` and `v2` subsets based on the `version` pod label. These subsets allow VirtualService routing rules to target specific versions.

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: echo-server
spec:
  host: echo-server
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

Apply and verify:

```bash theme={null}
kubectl apply -f dr.yaml
kubectl get destinationrules.networking.istio.io
```

Sample output:

```bash theme={null}
NAME          HOST          AGE
echo-server   echo-server   3s
```

## 7. Create a VirtualService that mirrors traffic

The VirtualService below routes 100% of production traffic to subset `v1` and mirrors each request to subset `v2`. `mirrorPercentage.value` accepts a float between 0.0 and 100.0 so you can partially mirror traffic if desired.

```yaml theme={null}
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: echo-server
spec:
  hosts:
    - echo-server
  http:
    - route:
        - destination:
            host: echo-server
            subset: v1
          weight: 100
      mirror:
        host: echo-server
        subset: v2
      mirrorPercentage:
        value: 100.0
```

Apply the VirtualService:

```bash theme={null}
kubectl apply -f vs.yaml
```

Tip: to reduce resource usage during testing, set `mirrorPercentage.value` to a lower number (for example `10.0`) to mirror only 10% of requests.

## 8. Test mirrored traffic

From the `test` pod, run repeated curl commands and observe that client responses continue to come from `v1` while `v2` receives mirrored copies (visible in its logs).

Repeat the same curl command:

```bash theme={null}
curl -s http://echo-server | grep -o '"hostname":"[^"]*"' | sed 's/"hostname":"\(.*\)"/HOSTNAME: \1/'
```

Expected client responses (all real responses from v1 when routing is 100% to v1):

```bash theme={null}
HOSTNAME: echo-server-v1-59ff75d58-t4dq6
HOSTNAME: echo-server-v1-59ff75d58-t4dq6
HOSTNAME: echo-server-v1-59ff75d58-t4dq6
```

Meanwhile, check the `v2` logs — you should see similar GET entries for the mirrored requests even though the client never received responses from `v2`. This confirms mirroring is functioning: real traffic is served by `v1`, and duplicates are sent to `v2` for analysis or testing.

Example request log from v1:

```json theme={null}
{
  "name": "echo-server",
  "hostname": "echo-server-v1-59ff75d58-t4dq6",
  "msg": "Fri, 11 Apr 2025 16:29:16 GMT | [GET] - http://echo-server/",
  "time": "2025-04-11T16:29:18.525Z"
}
```

Example mirrored request log in v2:

```json theme={null}
{"name":"echo-server","hostname":"echo-server-v2-5698db4f99-lm5ss","msg":"[GET] - http://echo-server/","time":"2025-04-11T16:26:39.998Z"}
```

## Quick reference table

| Resource Type   | Purpose                  | Example / Command                                |
| --------------- | ------------------------ | ------------------------------------------------ |
| Deployment      | Run app versions         | `echo-server-v1`, `echo-server-v2`               |
| Service         | Expose app internally    | `kubectl apply -f echo-svc.yaml`                 |
| DestinationRule | Define subsets by labels | See `dr.yaml` (subsets `v1` / `v2`)              |
| VirtualService  | Route + mirror traffic   | See `vs.yaml` (mirror -> `v2`, route -> `v1`)    |
| Test pod        | Generate traffic         | `kubectl run test --image=nginx --restart=Never` |

## Notes and references

* Mirroring does not change the client response; it only sends a copy of the request to the mirror target.
* Use `mirrorPercentage` to limit the portion of requests that are mirrored (0.0–100.0).
* Ensure labels in `DestinationRule.subsets` exactly match pod labels (`version: v1` / `version: v2`).
* Mirroring is useful for testing new versions without impacting users: logs, tracing, or metrics from the mirror can validate behavior.

<Callout icon="lightbulb">
  If you need the Gateway API or other CRDs present, ensure any required CRDs are installed before testing; for example, follow upstream installation instructions for the Gateway API when required by your environment.
</Callout>

Links and references:

* [Istio Traffic Management — VirtualService & DestinationRule](https://istio.io[AWS_SECRET_ACCESS_KEY]/)
* [Istio: Traffic Mirroring Documentation](https://istio.io/latest/docs/tasks/traffic-management/mirroring/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

That completes this lesson on Istio traffic mirroring. Try adjusting `mirrorPercentage` and subsets to experiment with partial mirroring and canary analysis in your cluster.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/a0ca9fa0-e282-411f-9894-5fab1d4cdfbb" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/4ca5ae83-9cbc-4f15-a7ef-d977caa61cdd" />
</CardGroup>
