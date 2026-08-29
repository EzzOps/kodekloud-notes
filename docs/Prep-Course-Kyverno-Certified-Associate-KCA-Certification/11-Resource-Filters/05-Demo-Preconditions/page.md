# NAME              ADMISSION   BACKGROUND   READY   AGE    MESSAGE
# check-label-env   true        true         true    10s    Ready
```

## Test the policy

1. Create a Pod without labels (expected: rejected, because Pod is matched by the rule):

```bash theme={null}
kubectl run my-pod --image=nginx
```

Example admission webhook response:

```text theme={null}
Error from server: admission webhook "validate.kyverno.svc" denied the request:
resource Pod/default/my-pod was blocked due to the following policies

check-label-env:
  check-label-env: validation error: The label `env` is required. rule check-label-env
```

2. Create a Deployment without the `env` label (expected: rejected):

```bash theme={null}
kubectl create deployment my-deployment --image=nginx
```

Example error:

```text theme={null}
error: failed to create deployment: admission webhook "validate.kyverno.svc" denied the request:
resource Deployment/default/my-deployment was blocked due to the following policies

check-label-env:
  check-label-env: validation error: The label `env` is required. rule check-label-env failed at path /metadata/labels/env/
```

3. Create a Pod with the `env` label (expected: allowed):

```bash theme={null}
kubectl run my-pod --image=nginx --labels=env=dev
# pod/my-pod created
```

These steps confirm the policy enforces the `env` label for the matched kinds.

## Scope the rule to a namespace

You can narrow the `match` block to specific namespaces. The example below restricts enforcement to the `restricted-ns` namespace:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-label-env
spec:
  validationFailureAction: enforce
  rules:
    - name: check-label-env
      match:
        any:
          - resources:
              kinds:
                - Pod
                - Deployment
              namespaces:
                - restricted-ns
      validate:
        message: "The label `env` is required."
        pattern:
          metadata:
            labels:
              env: "?*"
```

Apply the updated policy and create the namespace:

```bash theme={null}
kubectl apply -f check-label.yaml
kubectl create namespace restricted-ns
# namespace/restricted-ns created
```

Test the namespace-scoped behavior:

* Create a Pod in `restricted-ns` without labels (expected: rejected):

```bash theme={null}
kubectl run my-pod --image=nginx -n restricted-ns
```

Example webhook response:

```text theme={null}
Error from server: admission webhook "validate.kyverno.svc" denied the request:
resource Pod/restricted-ns/my-pod was blocked due to the following policies

check-label-env:
  check-label-env: validation error: The label `env` is required. rule check-label-env failed at path /metadata/labels/env/
```

* Create a Pod in the `default` namespace without labels (expected: allowed, because it doesn't match the `namespaces` filter):

```bash theme={null}
kubectl run test-pod --image=nginx
# pod/test-pod created
```

## Quick reference

| Topic              | Behavior                                       | Example command                              |
| ------------------ | ---------------------------------------------- | -------------------------------------------- |
| Match by kind      | Targets resources by kind (Pod, Deployment)    | `match: resources.kinds: - Pod - Deployment` |
| Match by namespace | Further restricts scope to specific namespaces | `namespaces: - restricted-ns`                |
| Validation pattern | Enforces non-empty `env` label                 | `metadata.labels.env: "?*"`                  |
| Apply policy       | Install or update ClusterPolicy                | `kubectl apply -f check-label.yaml`          |

## Summary

* Use the `match` block to control which resources Kyverno evaluates (kinds, namespaces, selectors).
* Use `validate.pattern` to require fields—`?*` ensures a string is present and non-empty.
* Adding `namespaces` to `match` scopes enforcement to specific namespaces (e.g., `restricted-ns`) while leaving other namespaces unaffected.

## Links and references

* [Kyverno Documentation](https://kyverno.io/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/b2e99306-7378-4cf1-93b0-d6f2b3031f2e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/a8ce8906-5078-4c36-9fd2-eb27504c3b04)


# Demo Preconditions

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Resource-Filters/Demo-Preconditions/page

Demonstrates using Kyverno preconditions to validate NodePort Services and enforce externalTrafficPolicy set to Local.

In this lesson we use Kyverno preconditions to make a ClusterPolicy that only runs against Services of type `NodePort`. When the precondition is met, the policy validates that `spec.externalTrafficPolicy` is set to `Local`.

<Frame>
  <img alt="The image features the words &#x22;Preconditions&#x22; and &#x22;Demo&#x22; on a white and blue-green background, with a copyright notice for KodeKloud." />
</Frame>

Goal

* Validate Services only when `spec.type` is `NodePort`.
* Enforce `spec.externalTrafficPolicy: Local` for those NodePort Services.

> **lightbulb** Preconditions are evaluated against the incoming admission request. If preconditions pass, the rule's `validate`/`mutate`/`generate` actions run; otherwise the rule is skipped. Use preconditions to make policies highly selective and avoid unnecessary validation on unrelated resources.

Policy manifest (ClusterPolicy)

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-nodeport-trafficpolicy
spec:
  rules:
    - name: validate-nodeport-trafficpolicy
      match:
        any:
          - resources:
              kinds:
                - Service
      preconditions:
        all:
          - key: "{{ request.object.spec.type }}"
            operator: Equals
            value: NodePort
      validationFailureAction: enforce
      validate:
        message: "All NodePort Services must use an externalTrafficPolicy of Local."
        pattern:
          spec:
            externalTrafficPolicy: Local
```

What this policy does

* `match` narrows targets to Kubernetes `Service` resources.
* `preconditions` further limit execution to Services whose `spec.type` equals `NodePort`.
* When the precondition passes, the `validate` block enforces that `spec.externalTrafficPolicy` is `Local`.
* If the precondition does not pass (for example, a `ClusterIP` Service), the rule is skipped.

Apply the policy

```bash theme={null}
kubectl apply -f validate-nodeport-trafficpolicy.yaml
```

Verify the ClusterPolicy is ready

```bash theme={null}
kubectl get cpol validate-nodeport-trafficpolicy
```

Example output:

```plaintext theme={null}
NAME                             ADMISSION   BACKGROUND   READY   AGE
validate-nodeport-trafficpolicy  true        true         Ready   10s
```

Test cases
We create three Service examples to demonstrate the policy behavior:

| Test case     | Service type | externalTrafficPolicy | Expected outcome                                               |
| ------------- | ------------ | --------------------- | -------------------------------------------------------------- |
| Bad NodePort  | `NodePort`   | `Cluster`             | Blocked by Kyverno; validation fails                           |
| Good NodePort | `NodePort`   | `Local`               | Created successfully                                           |
| ClusterIP     | `ClusterIP`  | n/a                   | Policy precondition fails → Rule skipped; created successfully |

1. Bad NodePort Service (should be rejected)

```bash theme={null}
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: bad-nodeport-service
spec:
  type: NodePort
  selector:
    app: bad-app
  ports:
    - port: 80
      targetPort: 8080
  externalTrafficPolicy: Cluster
EOF
```

Expected admission webhook error:

```plaintext theme={null}
Error from server: error when creating "STDIN": admission webhook "validate.kyverno.svc-fail" denied the request:
resource Service/default/bad-nodeport-service was blocked due to the following policies

validate-nodeport-trafficpolicy:
  validate-nodeport-trafficpolicy: 'validation error: All NodePort Services must use
    an externalTrafficPolicy of Local. rule validate-nodeport-trafficpolicy failed
    at path /spec/externalTrafficPolicy/'
```

> **warning** The admission webhook will block creation when the policy's `validationFailureAction` is `enforce`. Inspect Kyverno logs and events if an expected create is denied.

2. Good NodePort Service (should be accepted)

```bash theme={null}
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: good-nodeport-service
spec:
  type: NodePort
  selector:
    app: good-app
  ports:
    - port: 80
      targetPort: 8080
  externalTrafficPolicy: Local
EOF
```

Expected response:

```plaintext theme={null}
service/good-nodeport-service created
```

3. ClusterIP Service (precondition not met; policy skipped — should be accepted)

```bash theme={null}
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: clusterip-service
spec:
  type: ClusterIP
  selector:
    app: clusterip-app
  ports:
    - port: 80
      targetPort: 8080
EOF
```

Expected response:

```plaintext theme={null}
service/clusterip-service created
```

Summary and references

* Use `match` to restrict resources to specific kinds (here: `Service`).
* Use `preconditions` to further filter requests before running policy logic.
* The `validate` block runs only when preconditions succeed; otherwise the rule is skipped.
* For more details, see the Kyverno documentation:
  * Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)
  * Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/3fd51029-2735-4b64-81c3-a5d8b16584cb)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/65cbd27d-801d-4468-b4c5-47391c833127/lesson/64e85186-86bd-4f80-b9ad-a07807440c96)
