# service
NAME         TYPE        CLUSTER-IP       PORT(S)    LABELS
helloworld   ClusterIP   10.105.208.216   5000/TCP   app=helloworld,service=helloworld

# pods
helloworld-v1-7459d7b54b-wxfnj   2/2  Running  app=helloworld,version=v1,...
helloworld-v2-654d97458-twmkh    2/2  Running  app=helloworld,version=v2,...
```

## Create a test namespace and test client

Create a separate namespace for testing and enable Istio injection there. VirtualService/DestinationRule behavior depends on whether the communicating namespaces have sidecar injection enabled.

```bash theme={null}
kubectl create ns test
kubectl label namespace test istio-injection=enabled
```

Run a simple test pod in the `test` namespace (a lightweight curl image that stays running so you can exec into it):

```bash theme={null}
kubectl run test --image=curlimages/curl -n test --restart=Never --command -- sleep 3600
kubectl get pods -n test
```

Example:

```text theme={null}
NAME   READY   STATUS    RESTARTS   AGE
test   2/2     Running   0          3s
```

Exec into the test pod (or run a one-off command) to curl the HelloWorld service in the `default` namespace:

```bash theme={null}
kubectl exec -ti -n test test -- curl helloworld.default.svc:5000/hello
```

With no Istio routing yet, responses will be balanced by Kubernetes/Envoy defaults and you should see responses from either v1 or v2.

## Create a DestinationRule (subsets)

DestinationRules declare subsets that map to pod labels. Create a DestinationRule for the `helloworld` host that defines `v1` and `v2` subsets:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: hello-world-dr
  namespace: default
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

Apply the DestinationRule and confirm it's created:

```bash theme={null}
kubectl apply -f dr.yaml
kubectl get destinationrules.networking.istio.io
```

Example output:

```text theme={null}
NAME            HOST        AGE
hello-world-dr  helloworld  5s
```

Note: A DestinationRule alone does not split traffic; subsets simply define targets. You need a VirtualService to route between those subsets.

## Create a VirtualService to split traffic

Create a VirtualService that references the subsets declared in your DestinationRule. This example splits traffic 50/50 between v1 and v2:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello-world-vs
  namespace: default
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
          weight: 50
        - destination:
            host: helloworld.default.svc.cluster.local
            port:
              number: 5000
            subset: v2
          weight: 50
```

Apply the VirtualService and verify it exists:

```bash theme={null}
kubectl apply -f vs.yaml
kubectl get virtualservices.networking.istio.io
```

Example output:

```text theme={null}
NAME             HOSTS         AGE
hello-world-vs   [helloworld]  5s
```

## Test the routing

From the test pod, run several requests to observe traffic being split between v1 and v2:

```bash theme={null}
kubectl exec -ti -n test test -- /bin/sh -c 'for i in 1 2 3 4 5 6 7; do curl -s helloworld.default.svc:5000/hello; echo; done'
```

Example responses:

```text theme={null}
Hello version: v2, instance: helloworld-v2-654d97458-twmkh
Hello version: v1, instance: helloworld-v1-7459d7b54b-wxfnj
Hello version: v2, instance: helloworld-v2-654d97458-twmkh
...
```

## Adjust weights for traffic distribution

To change the split, update the `weight` fields in the VirtualService. For example, to route 95% to v1 and 5% to v2, modify the route section:

```yaml theme={null}
# update vs.yaml with these weights
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

Apply the updated VirtualService:

```bash theme={null}
kubectl apply -f vs.yaml
```

Re-run the curl loop in the test pod; you should observe mostly v1 responses.

View the final resource files for reference:

```bash theme={null}
cat vs.yaml
cat dr.yaml
```

## DestinationRule features (summary)

DestinationRules cover multiple traffic-management concerns. Use the table below as a quick reference.

|                              Feature | Purpose                                                               | Example/Notes                                                         |
| -----------------------------------: | --------------------------------------------------------------------- | --------------------------------------------------------------------- |
|                              Subsets | Define named groups of endpoints (by labels) for fine-grained routing | `subset: v1` selects pods labeled `version: v1`                       |
|                     Connection pools | Control TCP/HTTP connection reuse and limits                          | Set `trafficPolicy.connectionPool` to limit `maxConnections`          |
|                       Load balancing | Choose LB algorithm per host or per subset                            | `simple: LEAST_REQUEST`, `ROUND_ROBIN`, etc.                          |
| Outlier detection / circuit breaking | Eject unhealthy hosts and limit requests                              | `outlierDetection` with `consecutive5xxErrors` and `baseEjectionTime` |
|                           Client TLS | Configure TLS modes between client and destination                    | `tls.mode: MUTUAL`, `SIMPLE`, `DISABLE`, `ISTIO_MUTUAL`               |

## Example DestinationRule snippets

Connection pool example (TCP):

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: bookinfo-redis
spec:
  host: myredisrv.prod.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30ms
        tcpKeepalive:
          time: 7200s
          interval: 75s
```

Load-balancer and subset-specific trafficPolicy:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: bookinfo-ratings
spec:
  host: ratings.prod.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST
  subsets:
    - name: testversion
      labels:
        version: v3
      trafficPolicy:
        loadBalancer:
          simple: ROUND_ROBIN
```

Outlier detection / circuit breaker:

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
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

Client TLS (MUTUAL):

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: db-mtls
spec:
  host: mydbserver.prod.svc.cluster.local
  trafficPolicy:
    tls:
      mode: MUTUAL
      clientCertificate: /etc/certs/myclientcert.pem
      privateKey: /etc/certs/client_private_key.pem
      caCertificates: /etc/certs/rootcacerts.pem
```

Client TLS (SIMPLE):

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: tls-foo
spec:
  host: "*.foo.com"
  trafficPolicy:
    tls:
      mode: SIMPLE
```

Client TLS (Istio mTLS for ratings service):

```yaml theme={null}
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: ratings-istio-mtls
spec:
  host: ratings.prod.svc.cluster.local
  trafficPolicy:
    tls:
      mode: MUTUAL
```

<Frame>
  <img alt="The image shows a webpage from Istio documentation detailing the TLS connection modes, with a table outlining different modes such as DISABLE, SIMPLE, MUTUAL, and ISTIO_MUTUAL alongside their descriptions." />
</Frame>

## Next steps and practice tips

* Practice creating subsets and VirtualServices that reference those subsets to get comfortable with weight-based splitting.
* Experiment with trafficPolicy fields (connectionPool, loadBalancer, outlierDetection) to observe their operational effects.
* Use different TLS modes when securing connections between services and test with mutual TLS where appropriate.

References

* [Istio DestinationRule API](https://istio.io/latest/docs/reference/config/networking/destination-rule/)
* [Istio VirtualService API](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
* [Istio Traffic Management Concepts](https://istio.io/latest/docs/concepts/traffic-management/)

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/d1f9fcf9-1a4b-4eca-a8d7-a0560640d58b)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/cdadeded-56db-477a-b50d-d4598b89a083)


# Demo Gateways

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Gateways/page

Guide to configure an Istio Gateway and VirtualService to expose the Bookinfo app externally, including deployment checks, Gateway selection, routing updates, and testing via NodePort or LoadBalancer.

In this lesson we will configure an Ingress Gateway for the Bookinfo application using Istio. We'll:

* Verify Istio is installed and sidecar injection is enabled for the default namespace.
* Deploy Bookinfo and create an internal VirtualService.
* Create a Gateway resource and update the VirtualService to route external traffic.
* Test access through the Gateway.
* Show how a cloud installation exposes a LoadBalancer for external access.

Verify Istio is installed and the Istio system pods are running:

```bash theme={null}
kubectl get pods -n istio-system
```

Example output:

```plaintext theme={null}
NAME                                  READY   STATUS    RESTARTS   AGE
istio-egress-cfcd9bc96-9vlncl         1/1     Running   0          4m32s
istio-ingress-6cf77d4858-g2cvz        1/1     Running   0          4m31s
istiod-5fcb79676-j9vr9                1/1     Running   0          4m42s
```

Confirm that the default namespace has Istio sidecar injection enabled:

```bash theme={null}
kubectl get ns --show-labels
```

Example output:

```plaintext theme={null}
NAME              STATUS    AGE     LABELS
default           Active    5m29s   istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system      Active    4m51s   kubernetes.io/metadata.name=istio-system
kube-node-lease   Active    5m29s   kubernetes.io/metadata.name=kube-node-lease
kube-public       Active    5m29s   kubernetes.io/metadata.name=kube-public
kube-system       Active    5m29s   kubernetes.io/metadata.name=kube-system
```

Deploy the Bookinfo application (assumed already installed in these steps). Verify Bookinfo pods are running and have two containers (application + sidecar):

```bash theme={null}
kubectl get pods
```

Example output:

```plaintext theme={null}
NAME                                 READY   STATUS    RESTARTS   AGE
details-v1-65599dcf88-m7qpm          2/2     Running   0          4s
productpage-v1-9487c9c5b-qq955       2/2     Running   0          4s
ratings-v1-59b99c644-2gdfs           2/2     Running   0          4s
reviews-v1-5985999854-ntzxh          2/2     Running   0          4s
reviews-v2-866dc668-qqgmj            2/2     Running   0          4s
reviews-v3-dbb5fb5db-p78hv           2/2     Running   0          4s
```

Create an internal VirtualService that routes traffic to the productpage service. Save this as `vs.yaml`:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: book-info-vs
spec:
  hosts:
    - productpage
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

Apply it:

```bash theme={null}
kubectl apply -f vs.yaml
