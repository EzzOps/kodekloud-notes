# from a control plane shell
kubectl exec -n charlie curl -- curl helloworld.alpha.svc.cluster.local:5000/hello
# output
% Total    % Received % Xferd  Average Speed   Time    Time    Time   Current
                                    Dload   Upload   Total   Spent    Left  Speed
0         0         0     --:--:--   --:--:--   --:--:--     0
curl: (56) Recv failure: Connection reset by peer
```

Investigation steps

1. Check pods and services in `alpha`:

```bash theme={null}
kubectl get pods -n alpha
kubectl get svc -n alpha
```

2. Check client pods in `charlie`:

```bash theme={null}
kubectl get pods -n charlie
```

3. Verify namespace labels for sidecar injection:

```bash theme={null}
kubectl get ns --show-labels
```

Example relevant output:

```bash theme={null}
NAME       STATUS   AGE   LABELS
alpha      Active   26m   istio-injection=enabled,kubernetes.io/metadata.name=alpha
charlie    Active   26m   kubernetes.io/metadata.name=charlie
```

4. Inspect global mTLS/PeerAuthentication:

```bash theme={null}
kubectl get peerauthentications.security.istio.io -n istio-system default -o yaml
```

Example (trimmed) YAML:

```yaml theme={null}
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

Root cause

* A global `PeerAuthentication` in `STRICT` mode enforces mutual TLS. The client pod in `charlie` lacked an Istio sidecar because the `charlie` namespace was not labeled for injection, so it could not establish mTLS and the connection was reset.

Fix

1. Use `istioctl analyze` to identify misconfigurations (recommended):

```bash theme={null}
istioctl analyze -n charlie
# Info [IST0102] (Namespace charlie) The namespace is not enabled for Istio injection...
```

2. Label the namespace for injection:

```bash theme={null}
kubectl label namespace charlie istio-injection=enabled
```

3. Recreate the client pod so it receives an injected sidecar. Example if you have a manifest `charlie_curl.yaml`:

```bash theme={null}
kubectl delete -f charlie_curl.yaml
kubectl apply -f charlie_curl.yaml
```

4. Confirm the pod is Running with both application and `istio-proxy` containers:

```bash theme={null}
kubectl get pods -n charlie
# NAME   READY   STATUS
# curl   2/2     Running
```

5. Retry the curl:

```bash theme={null}
kubectl exec -n charlie curl -- curl helloworld.alpha.svc.cluster.local:5000/hello
# Hello version: v1, instance: helloworld-v1-...
```

<Callout icon="lightbulb">
  Always verify both that the namespace has the `istio-injection=enabled` label and that pods were recreated after labeling. Labeling a namespace does not retroactively inject sidecars into existing pods.
</Callout>

***

## Scenario 2 — Pod in an injection-enabled namespace is missing sidecar

Symptom: In `beta`, pods show `1/1` containers (no `istio-proxy`) even though the namespace has `istio-injection=enabled`.

Investigation steps

1. Get pods and deployments in `beta` and confirm namespace labels:

```bash theme={null}
kubectl get pods -n beta
kubectl get deployments.apps -n beta
kubectl get ns --show-labels
```

2. Inspect the Deployment or Pod for annotations that may disable injection:

```bash theme={null}
kubectl describe deployment -n beta curl
```

Look for an annotation like:

```yaml theme={null}
metadata:
  annotations:
    sidecar.istio.io/inject: "false"
```

Root cause

* The Deployment annotation `sidecar.istio.io/inject: "false"` explicitly disables sidecar injection for those pods, overriding the namespace-level label.

Fix

* Edit the Deployment to remove or change the annotation to allow injection (remove or set it to `"true"`), then recreate pods (rolling update or delete pods to let them be recreated).

Commands:

```bash theme={null}
kubectl edit deployment -n beta curl
# ensure pods are recreated and become 2/2
kubectl get pods -n beta
# e.g. curl-xxxxx   2/2  Running
```

Verify the pod contains the `istio-proxy`:

```bash theme={null}
kubectl describe pod -n beta <pod-name> | sed -n '/Containers:/,$p'
# Should list both application container and istio-proxy
```

***

## Scenario 3 — VirtualService routes to wrong host/port causing 503 Service Unavailable

Symptom: Requests to `httpbin` in `delta` return a 503 from Envoy:

```bash theme={null}
kubectl exec -n charlie curl -- curl -I httpbin.delta.svc.cluster.local:8000/get
# HTTP/1.1 503 Service Unavailable
server: envoy
```

Investigation steps

1. Validate the Service and Pods in `delta`:

```bash theme={null}
kubectl get svc -n delta
kubectl get pod -n delta
kubectl get ns --show-labels
```

Example service output:

```bash theme={null}
kubectl get svc -n delta
# NAME     TYPE        CLUSTER-IP       PORT(S)
# httpbin  ClusterIP   10.96.153.246    8000/TCP
```

2. Inspect the VirtualService for `httpbin`:

```bash theme={null}
kubectl get virtualservice -n delta httpbin-vs -o yaml
```

Example problematic VirtualService:

```yaml theme={null}
spec:
  hosts:
  - httpbin.delta.svc.cluster.local
  http:
  - route:
    - destination:
        host: httpbin.charlie.svc.cluster.local   # WRONG namespace
        port:
          number: 5000                             # WRONG port
```

Root cause

* The VirtualService routes traffic to `httpbin.charlie.svc.cluster.local:5000`, but the actual service is `httpbin.delta.svc.cluster.local` on port `8000`. Envoy cannot find a valid upstream, resulting in 503.

Fix

* Edit the VirtualService to point to the correct host and port:

```bash theme={null}
kubectl edit virtualservice -n delta httpbin-vs
# change destination.host to httpbin.delta.svc.cluster.local
# change destination.port.number to 8000
```

Verification:

```bash theme={null}
kubectl exec -n charlie curl -- curl -I httpbin.delta.svc.cluster.local:8000/get
# HTTP/1.1 200 OK
```

Tip: Always cross-check the Kubernetes `Service` that backs the workloads and ensure VirtualService destinations match the service FQDN and port.

***

## Scenario 4 — Gateway / External access issues (selector mismatch and missing gateway/hosts in VirtualService)

Symptom: `helloworld` in `alpha` is reachable internally but not via the configured Gateway/Ingress. External requests to the ingress IP return connection refused or 404.

Investigation steps

1. Check the Ingress Gateway service for external IP or LoadBalancer:

```bash theme={null}
kubectl get svc -n istio-system
# look for istio-ingressgateway (LoadBalancer); EXTERNAL-IP may be pending or an IP
```

2. Inspect the Gateway resource in `alpha`:

```bash theme={null}
kubectl get gateway -n alpha hello-gateway -o yaml
```

Problem #1 — Gateway selector mismatch

Example incorrect selector:

```yaml theme={null}
spec:
  selector:
    istio: ingress    # WRONG if the ingress pods are labeled differently
  servers:
  - hosts:
    - hello.kodekloud.com
    port:
      number: 80
      protocol: HTTP
```

* Confirm labels on the ingress pods to determine the correct selector:

```bash theme={null}
kubectl get pods -n istio-system -l app=istio-ingressgateway --show-labels
```

Ingress pods may have labels like `istio=ingressgateway` or `istio-ingressgateway`. The `Gateway.spec.selector` must match the ingress pod labels exactly; otherwise the Gateway is not bound to any ingress workload and cannot accept traffic.

Fix for selector mismatch

* Edit the Gateway to match the actual label on the ingress pods:

```bash theme={null}
kubectl edit gateway -n alpha hello-gateway
# change spec.selector to match ingress pod label, for example:
spec:
  selector:
    istio: ingressgateway
```

After fixing the selector, a previous `Connection refused` might change to `404 Not Found` because the Gateway is now handled by the ingress but the VirtualService still doesn't match external host/gateway configuration.

Problem #2 — VirtualService missing `hosts` and `gateways` for external routing

* Inspect the `helloworld` VirtualService:

```bash theme={null}
kubectl get virtualservice -n alpha helloworld-vs -o yaml
```

Example VirtualService that only contains the internal host:

```yaml theme={null}
spec:
  hosts:
  - helloworld.alpha.svc.cluster.local
  http:
  - route:
    - destination:
        host: helloworld.alpha.svc.cluster.local
        port:
          number: 5000
```

If the VirtualService does not list the external host (for example `hello.kodekloud.com`) and does not reference the Gateway (`gateways`), the Gateway will not route requests targeting the external hostname to this VirtualService, and Envoy will return `404`.

Fix for VirtualService

* Edit the VirtualService to include both `gateways` and the external host:

```bash theme={null}
kubectl edit virtualservice -n alpha helloworld-vs
```

Example corrected spec:

```yaml theme={null}
spec:
  gateways:
  - hello-gateway
  hosts:
  - helloworld.alpha.svc.cluster.local
  - hello.kodekloud.com
  http:
  - route:
    - destination:
        host: helloworld.alpha.svc.cluster.local
        port:
          number: 5000
```

Verification flow

1. Ensure the Gateway `spec.selector` matches the ingress pod labels.
2. Ensure the VirtualService includes `gateways:` and the external host in `hosts:`.
3. Curl the ingress IP using the external host in the `Host` header:

```bash theme={null}
curl --head --header "Host: hello.kodekloud.com" http://<INGRESS-IP>/hello
# or
curl --header "Host: hello.kodekloud.com" http://<INGRESS-IP>/hello
# Expect HTTP/1.1 200 OK and a Hello response body
```

Example successful response:

```text theme={null}
HTTP/1.1 200 OK
server: istio-envoy

Hello version: v2, instance: helloworld-v2-...
```

***

Notes and exam tips

* Use `istioctl analyze` to surface common issues around injection, Gateways, and VirtualServices.
* Troubleshooting priority checklist:
  1. Validate Kubernetes `Service` and Pod status.
  2. Confirm namespace labels for sidecar injection.
  3. Inspect resource-specific configurations: `PeerAuthentication`, `DestinationRule`, `AuthorizationPolicy`, `VirtualService`, `Gateway`, and `Service`.
* Common misconfiguration patterns: selector typos, wrong hostnames, incorrect namespaces, and wrong ports.
* For exams: apply the correct resource changes where necessary — partial corrections may still earn partial credit; avoid leaving answers blank.

<Callout icon="lightbulb">
  When editing resources: after changing a namespace label or Deployment annotation related to sidecar injection, you must recreate the pods to get the sidecar injected. Labeling alone doesn't modify existing pods.
</Callout>

This completes the common troubleshooting scenarios covered in this lesson/article.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/3b1a1d7c-b04a-4a3d-bf30-65da7d5460c3/lesson/23dac211-f39b-4747-a399-fd8b8f686098" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Troubleshooting/Introduction/page

Exam-focused guide to troubleshooting Istio misconfigurations, demo walkthroughs, checklists, and key kubectl and istioctl commands to prepare for the Istio Certified Associate exam.

This short module is focused and practical. In this lesson you'll:

* Review the most common problems that appear on the Istio Certified Associate (ICA) exam.
* Walk through a live demo of representative questions to learn how to troubleshoot them and what to look for during the exam.

We'll finish with concise personal tips and tricks to help you maximize your chances of passing the [ICA](https://learn.kodekloud.com/user/courses/istio-certified-associate).

Short and focused — let’s bring this home.

<Callout icon="lightbulb">
  This lesson prioritizes exam-relevant troubleshooting patterns for Istio. Focus on recurring misconfigurations, expected debugging commands, and how to interpret common error messages — these are high-value skills for the ICA.
</Callout>

## What this lesson covers

| Topic                | Why it matters                                                    | Outcome                                          |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------ |
| Common exam problems | ICA frequently tests the same misconfigurations and failure modes | Know which issues to check first                 |
| Troubleshooting demo | Live walkthrough shows steps and commands in context              | Understand practical, repeatable diagnostic flow |
| Exam tips & tricks   | Time management and targeted verification help on test day        | Improve accuracy and reduce time-to-solution     |

## How we’ll approach troubleshooting

1. Identify the symptom (error message, failed request, or unexpected behavior).
2. Narrow scope with simple verification commands. Focus on the control plane, data plane, and networking layers in that order.
3. Inspect relevant resources (e.g., Gateway, VirtualService, DestinationRule, Sidecar, Envoy config).
4. Validate configuration vs. expected behavior and iterate until resolved.
5. Document the fix and reason for the failure — this helps prevent similar mistakes.

## Quick checklist you can use during the exam

* Is the Istio control plane healthy? Check pods and CRDs.
* Are sidecars injected and running for the affected workloads?
* Is the Gateway bound to the correct service and port?
* Is the VirtualService route matching the host/path properly?
* Are DestinationRules or policy objects interfering (subset selection, TLS modes)?
* Do Envoy logs or `istioctl proxy-config` reveal mismatched clusters/routes?

## Recommended commands (high-value exam commands)

* `kubectl get pods -n istio-system` — verify control plane pods.
* `kubectl describe pod <pod>` — examine pod events and status.
* `kubectl logs <pod> -c istio-proxy` — check Envoy sidecar logs.
* `istioctl proxy-status` — overview of proxy connectivity.
* `istioctl proxy-config routes <pod> --name <listener>` — inspect route configuration.
* `istioctl analyze` — automatically detect common configuration issues.

<Callout icon="lightbulb">
  Tip: Learn a small set of `istioctl` and `kubectl` commands well. During the exam, efficient use of a few reliable commands saves time and reduces guesswork.
</Callout>

## Links and references

* [Istio Documentation](https://istio.io/latest/docs/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [ICA course on KodeKloud](https://learn.kodekloud.com/user/courses/istio-certified-associate)

Good luck — this module is meant to be concise and actionable. Use the checklist and commands above during practice sessions so they become second nature for exam day.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/3b1a1d7c-b04a-4a3d-bf30-65da7d5460c3/lesson/d48654d1-e167-4342-9cc2-958f319132f9" />
</CardGroup>
