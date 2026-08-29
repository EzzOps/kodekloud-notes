# clusterpolicy.kyverno.io/restrict-image-registries created
```

Test with an untrusted image from `quay.io`:

File: `test-pod-untrusted.yaml`

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: untrusted-pod
spec:
  containers:
    - name: test
      image: quay.io/prometheus/prometheus:latest
```

Attempt to create the Pod in namespace `team-dev`:

```bash theme={null}
kubectl apply -f test-pod-untrusted.yaml -n team-dev
```

If enforcement is enabled, the admission webhook will deny the request. Example error:

```text theme={null}
Error from server: error when creating "test-pod-untrusted.yaml": admission webhook "validate.kyverno.svc-fail" denied the request:
resource Pod/team-dev/untrusted-pod was blocked due to the following policies
restrict-image-registries:
  validate-registries: 'validation error: Image must be from docker.io. rule validate-registries'
    failed at path /spec/containers/0/image/
```

Now try a trusted image from `docker.io`:

File: `test-pod-trusted.yaml`

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: trusted-pod
spec:
  containers:
    - name: app
      image: docker.io/library/nginx
```

Apply it:

```bash theme={null}
kubectl apply -f test-pod-trusted.yaml -n team-dev
# pod/trusted-pod created
```

The trusted pod is admitted because it matches the policy pattern.

<Callout icon="lightbulb">
  You can switch `validationFailureAction` to `Audit` to collect violations without blocking resources.
</Callout>

## 2) Mutate rule example — auto-inject labels

Use a mutate rule to automatically inject labels into Pods created in the `team-dev` namespace using a strategic merge patch.

File: `mutate-labels.yaml`

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-labels
spec:
  rules:
    - name: add-managed-by
      match:
        any:
          - resources:
              kinds:
                - Pod
              namespaces:
                - team-dev
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              managed-by: kyverno
              environment: dev
```

Apply the policy:

```bash theme={null}
kubectl apply -f mutate-labels.yaml
# clusterpolicy.kyverno.io/add-labels created
```

Create a pod (use a `docker.io` image so the validate policy does not block it):

```bash theme={null}
kubectl run mutation-test --image=docker.io/library/nginx -n team-dev
# pod/mutation-test created
```

Check the labels injected by Kyverno:

```bash theme={null}
kubectl get pod -n team-dev mutation-test --show-labels
```

Example output:

```text theme={null}
NAME            READY   STATUS    RESTARTS   AGE    LABELS
mutation-test   1/1     Running   0          17s   environment=dev,managed-by=kyverno,run=mutation-test
```

The labels `managed-by=kyverno` and `environment=dev` were added automatically by the mutate rule.

## 3) Generate rule example — auto-create NetworkPolicy on Namespace creation

A generate rule can create a default-deny `NetworkPolicy` whenever a `Namespace` is created.

File: `generate-netpol.yaml`

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-networkpolicy
spec:
  rules:
    - name: default-deny
      match:
        any:
          - resources:
              kinds:
                - Namespace
      generate:
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        name: default-deny
        namespace: "{{request.object.metadata.name}}"
        spec:
          podSelector: {}
          policyTypes:
            - Ingress
            - Egress
```

Notes:

* The `namespace` field uses the template `{{request.object.metadata.name}}` so the generated NetworkPolicy is created inside the Namespace that triggered the rule.

Apply the policy:

```bash theme={null}
kubectl apply -f generate-netpol.yaml
# clusterpolicy.kyverno.io/generate-networkpolicy created
```

Create a namespace to trigger generation:

```bash theme={null}
kubectl create namespace auto-np-test
# namespace/auto-np-test created
```

Verify the generated NetworkPolicy:

```bash theme={null}
kubectl get networkpolicy -n auto-np-test
```

Example output:

```text theme={null}
NAME          POD-SELECTOR   AGE
default-deny  <none>         11s
```

Kyverno automatically created `default-deny` in `auto-np-test`.

## 4) Audit mode and PolicyReports

Audit mode allows resources that violate policies to be created while Kyverno records the violations in PolicyReport resources. This is useful for observing policy impact before enforcing.

Patch the `restrict-image-registries` policy to `Audit`:

```bash theme={null}
kubectl patch clusterpolicy restrict-image-registries \
  --type=merge \
  -p '{"spec":{"validationFailureAction":"Audit"}}'
# clusterpolicy.kyverno.io/restrict-image-registries patched
```

Now apply the untrusted pod again:

```bash theme={null}
kubectl apply -f test-pod-untrusted.yaml -n team-dev
# pod/untrusted-pod created
```

The Pod is created (not blocked), and Kyverno records the policy results as PolicyReport resources.

List policy reports in the namespace:

```bash theme={null}
kubectl get policyreport -n team-dev
```

Example output (summary):

```text theme={null}
NAME                                       KIND   PASS   FAIL   WARN   ERROR   SKIP   AGE
579d07e7-742c-4299-9147-8e7584106c30       Pod    1      1      0      0       0     0s
274e0a72-4abc-9fa5-9147-9b4ef95fc68e       Pod    1      0      0      0       0     7m9s
76b686df-cc1a-4e7e-821f-cba9b988d981       Pod    2      0      0      0       0     4m19s
```

Describe a PolicyReport for the untrusted pod to view details:

```bash theme={null}
kubectl describe policyreport 579d07e7-742c-4299-9147-8e7584106c30 -n team-dev
```

Example (truncated) output from the PolicyReport:

```text theme={null}
Results:
  - Message: mutated Pod/untrusted-pod in namespace team-dev
    Policy: add-labels
    Properties:
      Process: background scan
      Result: pass
      Rule: add-managed-by
      Scored: true
      Source: kyverno
    Timestamp: 2026-04-15T18:27:20Z

  - Message: validation error: Image must be from docker.io. rule validate-registries failed at path /spec/containers/0/image/
    Policy: restrict-image-registries
    Properties:
      Process: background scan
      Result: fail
      Rule: validate-registries
      Scored: true
      Source: kyverno
    Timestamp: 2026-04-15T18:27:30Z

Summary:
  Pass: 1
  Fail: 1
  Total: 2
```

This output shows:

* The mutate rule passed and injected labels.
* The validate rule failed (image not from `docker.io`), but because the policy is in Audit mode, the Pod was admitted and the violation was captured for visibility.

<Callout icon="lightbulb">
  Use Audit mode to evaluate policy impact and blast radius. Once you are confident, switch policies back to `Enforce` to block violating resources.
</Callout>

## Summary and best practices

* Kyverno policies are Kubernetes-native YAML — no Rego required.
* Use the three complementary rule types:
  * validate: block or audit resources
  * mutate: change resources at admission (strategic merge, JSON patches, etc.)
  * generate: create resources in response to events (e.g., default-deny NetworkPolicy)
* Start in Audit mode and review PolicyReports to safely roll out policies.
* Combine mutate + validate rules to auto-fix common issues and enforce desired state.

## Links and references

* Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
* Kyverno policy examples: [https://kyverno.io/docs/writing-policies/](https://kyverno.io/docs/writing-policies/)
* OPA Gatekeeper: [https://open-policy-agent.github.io/gatekeeper/](https://open-policy-agent.github.io/gatekeeper/)
* Rego language: [https://www.openpolicyagent.org/docs/latest/policy-language/](https://www.openpolicyagent.org/docs/latest/policy-language/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/a82e67a7-e75e-4ef0-be81-4862c665ef4f" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/11c61a43-720a-4ba7-b400-2bc8580dfd1f" />
</CardGroup>


# Demo mTLS with Istio

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Demo-mTLS-with-Istio/page

Guide demonstrating Istio mTLS setup in Kubernetes, enabling sidecar injection, enforcing strict mutual TLS, applying AuthorizationPolicy to restrict service access, and validating with istioctl and in-cluster tests

RBAC controls who can interact with the Kubernetes API. But intra-cluster service-to-service traffic is unauthenticated and unencrypted by default: a compromised pod can communicate freely with other services. Mutual TLS (mTLS) provides both encryption in transit and identity verification between workloads. Istio implements mTLS transparently via sidecar proxies so your application code does not need to change.

In this guide you'll:

* Verify cluster and namespace state,
* Enable Istio automatic sidecar injection for the demo namespace,
* Observe default mTLS behavior (PERMISSIVE),
* Enforce STRICT mTLS with a PeerAuthentication resource,
* Apply an AuthorizationPolicy to restrict which services may call the payment API,
* Validate the policy via in-cluster curl requests,
* Run `istioctl analyze` for a final diagnostic check.

***

## 1) Check current state

Confirm Istio control plane pods and application pods in the `mesh-demo` namespace. Before enabling injection, application pods run without the sidecar (single container).

Check Istio control plane pods:

```bash theme={null}
kubectl get pods -n istio-system
```

Example output:

```text theme={null}
NAME                                   READY   STATUS    RESTARTS   AGE
istio-egressgateway-8455f4dc86-9xm62   1/1     Running   0          10m
istio-ingressgateway-767bc4085b-t6x9k  1/1     Running   0          10m
istiod-659d96fcd-xrr5n                 1/1     Running   0          12m
```

Check application pods in the demo namespace (no sidecars yet):

```bash theme={null}
kubectl get pods -n mesh-demo
```

Example output:

```text theme={null}
NAME                           READY   STATUS    RESTARTS   AGE
order-api-764fd948dc-7xztj     1/1     Running   0          5m
payment-api-756c646c67-dxmx2   1/1     Running   0          5m
web-frontend-8586897ccf-xvbfm  1/1     Running   0          5m
```

Run an initial analysis (recommended):

```bash theme={null}
istioctl analyze -n mesh-demo
```

Example informational output:

```text theme={null}
Info [IST0102] (Namespace mesh-demo) The namespace is not enabled for Istio injection. Run 'kubectl label namespace mesh-demo istio-injection=enabled' to enable it.
Info [IST0118] (Service mesh-demo/order-api) Port name (port: 80, targetPort: 80) doesn't follow Istio's port naming convention.
...
```

***

## 2) Enable automatic sidecar injection and restart workloads

Label the namespace to enable automatic Istio sidecar injection. Then restart the deployments so new pods are created with the sidecar proxy.

```bash theme={null}
kubectl label namespace mesh-demo istio-injection=enabled
kubectl rollout restart deployment/web-frontend deployment/payment-api deployment/order-api -n mesh-demo
```

After pods restart, each workload should have two containers (application + `istio-proxy`). Verify:

```bash theme={null}
kubectl get pods -n mesh-demo
```

Example output after restart:

```text theme={null}
NAME                                READY   STATUS    RESTARTS   AGE
order-api-764fd948dc-7xztj          2/2     Running   0          1m
payment-api-756c646c67-dxmx2        2/2     Running   0          1m
web-frontend-8586897ccf-xvbfm       2/2     Running   0          1m
```

Inspect a pod to see the effective mTLS mode:

```bash theme={null}
istioctl describe pod -n mesh-demo web-frontend-8586897ccf-xvbfm
```

Look for:

```bash theme={null}
Effective PeerAuthentication:
  Workload mTLS mode: PERMISSIVE
```

<Callout icon="lightbulb">
  Permissive mTLS accepts both plain-text (HTTP) and mTLS connections. It's a safe default during setup because it allows mixed clients while sidecars are being rolled out, but it does not enforce encryption or strongly verify caller identity.
</Callout>

***

## 3) Enforce strict mTLS (PeerAuthentication)

To require encrypted, authenticated connections between workloads in `mesh-demo`, create a PeerAuthentication resource with `mtls.mode: STRICT`.

peer-auth-strict.yaml:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: mesh-demo
spec:
  mtls:
    mode: STRICT
```

Apply it:

```bash theme={null}
kubectl apply -f peer-auth-strict.yaml
```

Verify:

```bash theme={null}
kubectl describe peerauthentications.security.istio.io default -n mesh-demo
```

Expected spec summary:

```YAML theme={null}
Spec:
  mtls:
    Mode: STRICT
```

<Callout icon="warning">
  Applying `PeerAuthentication` with `mode: STRICT` will cause any plain-text (non-mTLS) connections to fail. Ensure all workloads in the namespace have sidecars injected and are up-to-date before applying strict mTLS to avoid service disruption.
</Callout>

***

## 4) Restrict calls with an AuthorizationPolicy

mTLS ensures encrypted, authenticated connections, but it does not restrict which workloads can connect to others. Use an AuthorizationPolicy to enforce a zero-trust pattern: allow only specific principals (service accounts) to call the payment API.

Create this AuthorizationPolicy scoped to the `payment-api` workload:

authz-policy.yaml:

```yaml theme={null}
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: payment-api-policy
  namespace: mesh-demo
spec:
  selector:
    matchLabels:
      app: payment-api
  rules:
    - from:
        - source:
            principals:
              - cluster.local/ns/mesh-demo/sa/web-frontend
      to:
        - operation:
            methods: ["GET", "POST"]
```

Key notes:

* `selector.matchLabels` scopes the policy to pods labeled `app: payment-api`.
* `principals` uses the SPIFFE identity form (here: `cluster.local/ns/mesh-demo/sa/web-frontend`) derived from the caller’s service account.
* `operation.methods` limits allowed HTTP methods. You can also add `paths` or other HTTP attributes.

Apply the policy:

```bash theme={null}
kubectl apply -f authz-policy.yaml
```

Table: Resources created

| Resource Type       | Purpose                                       | Example                 |
| ------------------- | --------------------------------------------- | ----------------------- |
| PeerAuthentication  | Enforce namespace/workload mTLS mode          | `peer-auth-strict.yaml` |
| AuthorizationPolicy | Allow specific principals to call payment-api | `authz-policy.yaml`     |

***

## 5) Validate behavior with in-cluster curl

Test from a pod with an unauthorized identity (order-api). The request should be rejected by Istio (HTTP 403):

```bash theme={null}
kubectl exec -n mesh-demo deployment/order-api -- \
  curl -s -o /dev/null -w "%{http_code}" http://payment-api.mesh-demo.svc.cluster.local/api/pay
```

Expected output:

```text theme={null}
403
```

Test from the allowed principal (web-frontend). The request should be permitted; the upstream service may return `404` if the path is missing, which still indicates the request was authorized and reached the service:

```bash theme={null}
kubectl exec -n mesh-demo deployment/web-frontend -- \
  curl -s -o /dev/null -w "%{http_code}" http://payment-api.mesh-demo.svc.cluster.local/api/pay
```

Expected output (example):

```text theme={null}
404
```

Interpretation:

* `403` from `order-api`: Istio denied the request at the sidecar (authorization failure).
* `404` from `web-frontend`: Policy allowed the request and the call reached the payment-api, but the specific path was not found.

This demonstrates zero-trust networking: connections are both authenticated (mTLS) and authorized (AuthorizationPolicy).

***

## 6) Re-run analysis

Run `istioctl analyze` to surface configuration issues such as namespace injection, port naming, selector mismatches, or other diagnostic hints:

```bash theme={null}
istioctl analyze -n mesh-demo
```

Example informational warnings:

```text theme={null}
Info [IST0118] (Service mesh-demo/payment-api) Port name (port: 80, targetPort: 80) doesn't follow Istio's port naming convention.
Info [IST0118] (Service mesh-demo/web-frontend) Port name (port: 80, targetPort: 80) doesn't follow Istio's port naming convention.
```

Use `istioctl analyze` as a routine pre-deployment check before pushing broader changes to production.

***

Summary

* Enabled Istio sidecar injection for the `mesh-demo` namespace.
* Confirmed PERMISSIVE mTLS initially, then enforced STRICT mTLS using a PeerAuthentication.
* Applied an AuthorizationPolicy to restrict which service account can call the payment API and limited allowed operations.
* Validated enforcement with in-cluster curl tests: unauthorized requests were rejected by Istio, authorized requests reached the service.
* Re-ran `istioctl analyze` to surface configuration warnings to address.

Links and references

* [Istio PeerAuthentication docs](https://istio.[AWS_SECRET_ACCESS_KEY]/peer_authentication/)
* [Istio AuthorizationPolicy docs](https://istio.[AWS_SECRET_ACCESS_KEY]/authorization-policy/)
* [istioctl analyze](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/)
* [SPIFFE and SPIRE](https://spiffe.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/64424caf-3564-4c76-93f1-0d88101072d6" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/caedb06f-ceb3-4c51-9c37-be0a7855e26b" />
</CardGroup>
