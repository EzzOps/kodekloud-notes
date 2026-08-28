# check namespaces and labels
kubectl get ns --show-labels
```

Example output:

```text theme={null}
NAME              STATUS   AGE   LABELS
default           Active   21m   istio-injection=enabled,kubernetes.io/metadata.name=default
istio-system      Active   51s   kubernetes.io/metadata.name=istio-system
kube-node-lease   Active   21m   kubernetes.io/metadata.name=kube-node-lease
kube-public       Active   21m   kubernetes.io/metadata.name=kube-public
kube-system       Active   21m   kubernetes.io/metadata.name=kube-system
```

2. Deploy the helloworld sample application

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.[SECRET_REDACTED].yaml
```

Expected response:

```text theme={null}
service/helloworld created
deployment.apps/helloworld-v1 created
deployment.apps/helloworld-v2 created
```

3. Create a test pod (use an image with `curl` available)

```bash theme={null}
kubectl run test --image=curlimages/curl --restart=Never --command -- sleep 3600
kubectl get pods
```

Example pod list:

```text theme={null}
NAME                            READY   STATUS    RESTARTS   AGE
helloworld-v1-7459d7b54b-lqtl6  2/2     Running   0          25s
helloworld-v2-654d97458-7vpz4   2/2     Running   0          25s
test                            1/1     Running   0          5s
```

4. Confirm the helloworld service

```bash theme={null}
kubectl get svc
```

Example output:

```text theme={null}
NAME        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
helloworld  ClusterIP   10.111.116.180   <none>        5000/TCP       37s
kubernetes  ClusterIP   10.96.0.1        <none>        443/TCP        22m
```

5. Smoke test the application from the test pod

```bash theme={null}
kubectl exec -ti test -- curl http://helloworld:5000/hello
```

Sample responses (the service load-balances between v1 and v2):

```text theme={null}
Hello version: v2, instance: helloworld-v2-654d97458-7vpz4
Hello version: v1, instance: helloworld-v1-7459d7b54b-lqtl6
```

At this point the app is functioning normally. Circuit-breaking and connection-level controls are configured in DestinationRule resources (if present) — these are separate from VirtualService fault injection.

6. Verify there are no existing VirtualServices or DestinationRules in the namespace

```bash theme={null}
kubectl get vs
kubectl get destinationrules.networking.istio.io
# No resources found in default namespace.
```

Quick reference: common fault types

| Fault Type | Description                                               | When to use                                          |
| ---------- | --------------------------------------------------------- | ---------------------------------------------------- |
| Delay      | Adds latency to selected requests (e.g. `fixedDelay: 5s`) | Simulate slow downstream services or network latency |
| Abort      | Returns an HTTP error (e.g. `httpStatus: 500`)            | Simulate service failures or server errors           |

<Callout icon="warning">
  Do not apply fault injections in production clusters or against production services unless you have explicit permission and proper safeguards. Fault injection will deliberately break or delay traffic.
</Callout>

7. Inject a fixed 5s delay for 100% of traffic

Save the following VirtualService as `vs-delay.yaml`:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: hello-world-vs
spec:
  hosts:
    - helloworld
  http:
    - fault:
        delay:
          percentage:
            value: 100.0
          fixedDelay: 5s
      route:
        - destination:
            host: helloworld
            port:
              number: 5000
```

Apply and verify:

```bash theme={null}
kubectl apply -f vs-delay.yaml
kubectl get vs
```

Example output:

```text theme={null}
virtualservice.networking.istio.io/hello-world-vs configured

NAME             GATEWAYS   HOSTS           AGE
hello-world-vs   []         ["helloworld"]  5s
```

Test the injected delay:

```bash theme={null}
kubectl exec -ti test -- curl http://helloworld:5000/hello
# (response appears after ~5s)
```

Expected behavior: every request to `helloworld:5000` is delayed by approximately 5 seconds.

8. Change the fault to an abort (inject HTTP error responses)

Save this VirtualService as `vs-abort-500.yaml` to abort 100% of requests with HTTP 500:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: hello-world-vs
spec:
  hosts:
    - helloworld
  http:
    - fault:
        abort:
          percentage:
            value: 100.0
          httpStatus: 500
      route:
        - destination:
            host: helloworld
            port:
              number: 5000
```

Apply and test:

```bash theme={null}
kubectl apply -f vs-abort-500.yaml
kubectl exec -ti test -- curl http://helloworld:5000/hello
```

You will see an Envoy fault filter message similar to:

```text theme={null}
fault filter abort
```

To see the injected status code in the HTTP response headers:

```bash theme={null}
kubectl exec -ti test -- curl --head http://helloworld:5000/hello
```

Example headers:

```text theme={null}
HTTP/1.1 500 Internal Server Error
content-length: 18
content-type: text/plain
date: Tue, 15 Apr 2025 15:58:03 GMT
server: envoy
```

Tip: Change `httpStatus` to `404`, `503`, etc., to simulate different server responses.

9. Inject a 50% abort (random failures)

Save this VirtualService (e.g. `vs-abort-50.yaml`) to abort 50% of requests with HTTP 404:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: hello-world-vs
spec:
  hosts:
    - helloworld
  http:
    - fault:
        abort:
          percentage:
            value: 50.0
          httpStatus: 404
      route:
        - destination:
            host: helloworld
            port:
              number: 5000
```

Apply and run multiple requests to observe the distribution:

```bash theme={null}
kubectl apply -f vs-abort-50.yaml

# Run 10 requests and show headers to observe 200 vs 404 responses
kubectl exec -ti test -- /bin/sh -c 'for i in $(seq 1 10); do curl --head http://helloworld.default.svc:5000/hello; echo "---"; done'
```

Expected result: roughly half of the responses return `HTTP/1.1 200 OK` and half `HTTP/1.1 404 Not Found` (randomness and sample size affect exact counts). The same pattern can be used for percentage-based delays.

10. Conditional fault injection (by header match)

You can scope faults to requests that match particular conditions (for example, a specific header). The Istio docs show an example where a 7s delay is injected only for requests with the `end-user` header equal to `jason`:

```yaml theme={null}
hosts:
  - ratings
http:
  - fault:
      delay:
        fixedDelay: 7s
        percentage:
          value: 100
    match:
      - headers:
          end-user:
            exact: jason
    route:
      - destination:
          host: ratings
          subset: v1
```

This injects a 7s delay only for requests where `end-user: jason` is present.

<Callout icon="lightbulb">
  Fault injection in Istio is configured on VirtualService resources. Circuit-breaking and connection-level controls belong in DestinationRule resources — make sure to use the correct resource for each purpose.
</Callout>

11. References and next steps

* Istio VirtualService reference: [https://istio.io[AWS_SECRET_ACCESS_KEY]/virtual-service/](https://istio.io[AWS_SECRET_ACCESS_KEY]/virtual-service/)
* Fault injection task guide: [https://istio.io/latest/docs/tasks/traffic-management/fault-injection/](https://istio.io/latest/docs/tasks/traffic-management/fault-injection/)
* Next steps: configure client-side retries and timeouts in Istio to make your clients resilient to transient faults.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/3216232f-aca0-45ff-812a-35b9253cb0b4" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/f3f5ca4b-b8d6-4788-9553-9ed765709933/lesson/4b560f64-c293-4ed4-8c86-497a50ef68df" />
</CardGroup>


# Demo Request Timeouts Retries

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Traffic-Management/Demo-Request-Timeouts-Retries/page

Configuring Istio VirtualService timeouts and retries using an httpbin demo, deploying test pods, observing proxy behavior and testing delay and status endpoints.

In this lesson you'll learn how to configure request timeouts and retries using Istio VirtualService resources. We'll deploy the sample httpbin application and a simple test pod, then demonstrate how to enforce timeouts and retries and observe their effect via requests and proxy logs.

## Prepare the cluster and deploy httpbin

1. Confirm your current namespace (showing labels is optional):

```bash theme={null}
kubectl get ns --show-labels
```

2. Deploy httpbin and create a test pod with curl installed (image: `curlimages/curl`):

```bash theme={null}
kubectl apply -f https://raw.githubusercontent.com/istio[AWS_SECRET_ACCESS_KEY]/httpbin.yaml
kubectl run test --image=curlimages/curl --restart=Never --command -- sleep 1d
```

3. Verify pods are running:

```bash theme={null}
kubectl get pods
```

Example output (trimmed):

```text theme={null}
NAME                         READY   STATUS      RESTARTS   AGE
httpbin-787cdcc9df-xx9gd     2/2     Running     0          1m
test                         1/1     Running     0          30s
```

4. Confirm the httpbin service exists:

```bash theme={null}
kubectl get svc
```

Example output:

```text theme={null}
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
httpbin      ClusterIP   10.108.160.240  <none>        8000/TCP   1m
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    10m
```

5. From the test pod, verify a basic request works:

```bash theme={null}
kubectl exec -ti test -- curl --head http://httpbin:8000
```

You should see a `200 OK` response header.

## Implementing a request timeout

Create a VirtualService that enforces a 2 second timeout for HTTP requests to the httpbin service.

vs-timeout.yaml:

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

Apply the VirtualService and confirm it exists:

```bash theme={null}
kubectl apply -f vs-timeout.yaml
kubectl get virtualservice
```

Test the behavior using httpbin's delay endpoint:

* A 1 second delay is within the 2s timeout and should succeed:

```bash theme={null}
kubectl exec -ti test -- curl http://httpbin:8000/delay/1
```

Example JSON response:

```json theme={null}
{
  "args": {},
  "headers": {
    "Host": "httpbin:8000",
    "User-Agent": ["curl/7.88.1"],
    "X-Envoy-Attempt-Count": ["1"]
  },
  "method": "GET",
  "origin": "127.0.0.1:4017",
  "url": "http://httpbin:8000/delay/1"
}
```

* A 2 second delay equals the configured timeout and will be terminated by the proxy:

```bash theme={null}
kubectl exec -ti test -- curl http://httpbin:8000/delay/2
```

Typical result:

```text theme={null}
upstream request timeout
```

Explanation: the VirtualService `timeout` causes the Envoy proxy to abort the request if the upstream service does not respond within the configured period (2s). Increase the timeout if you expect longer upstream processing (for example, try `timeout: 5s` and `/delay/3` to confirm).

## Implementing retries

First, remove the timeout VirtualService:

```bash theme={null}
kubectl delete -f vs-timeout.yaml
```

Create a VirtualService that enables retries:

vs-retries.yaml:

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

Apply the new VirtualService:

```bash theme={null}
kubectl apply -f vs-retries.yaml
```

What this configuration means:

* `attempts`: number of retry attempts (3)
* `perTryTimeout`: timeout for each individual attempt (1s)
* `retryOn`: which error classes trigger retries (here `5xx` server errors)

### Test retries using httpbin's status endpoint

httpbin exposes `/status/<code>` to return arbitrary HTTP status codes.

1. Confirm a normal GET works:

```bash theme={null}
kubectl exec -ti test -- curl --head http://httpbin:8000/get
```

You should see `HTTP/1.1 200 OK`.

2. Generate a 500 and observe the response and proxy behavior:

```bash theme={null}
kubectl exec -ti test -- curl --head http://httpbin:8000/status/500
```

You will receive `HTTP/1.1 500 Internal Server Error` as the final response to the client.

3. To observe retries, tail the httpbin pod's proxy logs (the `istio-proxy` container). First get the httpbin pod name and then tail logs:

```bash theme={null}
kubectl get pods -l app=httpbin
kubectl logs -f <httpbin-pod-name> -c istio-proxy
