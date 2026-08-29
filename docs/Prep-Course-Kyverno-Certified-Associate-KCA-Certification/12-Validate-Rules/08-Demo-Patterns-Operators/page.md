# output
# clusterpolicy.kyverno.io/conditional-anchor-dockersock created
```

Compliant Pod (has required label):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: good-pod
  labels:
    allow-docker: "true"
spec:
  containers:
    - name: app
      image: busybox
      command: ["sleep", "3600"]
  volumes:
    - name: docker
      hostPath:
        path: /var/run/docker.sock
```

Create it:

```bash theme={null}
kubectl apply -f good-pod.yaml
# output
# pod/good-pod created
```

Non-compliant Pod (missing label):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: bad-pod
spec:
  containers:
    - name: app
      image: busybox
      command: ["sleep", "3600"]
  volumes:
    - name: docker
      hostPath:
        path: /var/run/docker.sock
```

Attempt to create it:

```bash theme={null}
kubectl apply -f bad-pod.yaml
# output (admission webhook denies the request)
# Error from server: admission webhook "validate.kyverno.svc" denied the request: [conditional-anchor-dockersock] validation error: If a Pod mounts /var/run/docker.sock via hostPath, it must have label allow-docker=true.
```

Because the "if" condition matched and the required label was missing, admission is denied.

<Callout icon="warning">
  Policies with `failureAction: Enforce` will block resource creation on non-compliance. Use `background` and `failureAction` carefully in production clusters.
</Callout>

***

## 2) Equality anchors

Equality anchors use `=` to indicate the existence of an object. If the object exists, equality anchors let you place constraints on its child fields.

Policy intent:

* If a `hostPath` volume object exists in a Pod, then its `path` must not be `/var/run/docker.sock`.

Policy (ClusterPolicy):

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: equality-anchor-no-dockersock
spec:
  background: false
  rules:
    - name: equality-anchor-no-dockersock
      match:
        resources:
          kinds:
            - Pod
      validate:
        failureAction: Enforce
        message: "If a hostPath volume exists, it must not be set to `/var/run/docker.sock`."
        pattern:
          =(spec):
            =(volumes):
              - =(hostPath):
                  path: "!/var/run/docker.sock"
```

How it works:

* `=(spec)` and `=(volumes)` assert that those objects exist; when they do, the child constraint applies.
* `path: "!/var/run/docker.sock"` uses Kyverno's `!` operator to express "not equal".

Apply the policy:

```bash theme={null}
kubectl apply -f equality-anchors.yaml
# output
# clusterpolicy.kyverno.io/equality-anchor-no-dockersock created
```

Non-compliant Pod (disallowed hostPath path):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: bad-dockersock-pod
spec:
  containers:
    - name: app
      image: busybox
      command: ["sleep", "3600"]
  volumes:
    - name: docker
      hostPath:
        path: /var/run/docker.sock
```

Attempt to create it:

```bash theme={null}
kubectl apply -f bad-dockersock-pod.yaml
# output
# Error from server: admission webhook "validate.kyverno.svc" denied the request: [equality-anchor-no-dockersock] validation error: If a hostPath volume exists, it must not be set to `/var/run/docker.sock`.
```

Compliant Pod (different hostPath path):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: good-dockersock-pod
spec:
  containers:
    - name: app
      image: busybox
      command: ["sleep", "3600"]
  volumes:
    - name: somepath
      hostPath:
        path: /var/run/some-other.sock
```

Create it:

```bash theme={null}
kubectl apply -f good-dockersock-pod.yaml
# output
# pod/good-dockersock-pod created
```

Because the `hostPath` existed but its `path` did not match the forbidden value, the Pod passed validation.

***

## 3) Existence anchors

Existence anchors are applied to lists/arrays and assert that at least one element in the list matches a given pattern. This is ideal for requiring a Pod to include a specific sidecar or container image.

Policy intent:

* Verify that at least one container in the Pod uses the `nginx` image.

Behavior:

* The policy iterates the `containers` list and accepts the Pod if any item has `image: nginx`. If none match, validation fails.

Apply the existence-anchor policy (example policy file assumed applied):

```bash theme={null}
kubectl apply -f existence-anchor-nginx.yaml
# output
# clusterpolicy.kyverno.io/existence-anchor-nginx created
```

Non-compliant Pod (no nginx container):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: busybox-only
spec:
  containers:
    - name: busy
      image: busybox
      command: ["sleep", "3600"]
```

Attempt to create it:

```bash theme={null}
kubectl apply -f busybox-only.yaml
# output
# Error from server: admission webhook "validate.kyverno.svc" denied the request: [existence-anchor-nginx] validation error: at least one container must use image 'nginx'
```

Compliant Pod (has an nginx container among others):

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-with-nginx
spec:
  containers:
    - name: app
      image: busybox
      command: ["sleep", "3600"]
    - name: proxy
      image: nginx
```

Create it:

```bash theme={null}
kubectl apply -f multi-container-with-nginx.yaml
# output
# pod/multi-container-with-nginx created
```

Because one of the containers matches the required pattern (`image: nginx`), the policy is satisfied.

***

## Recap

* Conditional anchors `( )` create if-then rules where the "if" is an object pattern and the "then" is a sibling field.
* Equality anchors `=` check for the existence of an object and impose constraints on its children.
* Existence anchors operate on lists and require at least one element to match the provided pattern.

These anchors let you write compact, declarative Kyverno validate patterns for common policy intents without adding extra configuration blocks.

## Links and references

* Kyverno validation patterns: [https://kyverno.io/docs/writing-policies/validation-patterns/](https://kyverno.io/docs/writing-policies/validation-patterns/)
* Kyverno GitHub: [https://github.com/kyverno/kyverno](https://github.com/kyverno/kyverno)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/7e0be25b-ff0d-451f-86c3-c509bdc4a075" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/a0161669-b400-4a56-be96-9830372afa74" />
</CardGroup>


# Demo Patterns Operators

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Demo-Patterns-Operators/page

Explains using Kyverno pattern operators to enforce minimum Deployment replicas and forbid the default namespace via validation ClusterPolicies

In this lesson you'll learn how to use operators in Kyverno validate rules. We'll walk through two practical ClusterPolicy examples:

* Enforce a minimum replica count for Deployments using comparison operators.
* Block Deployments created in the `default` namespace using the not (`!`) operator.

These examples use Kyverno `pattern`-based validation to express flexible constraints without hardcoding exact values.

***

## 1) Enforce minimum replica count

This ClusterPolicy validates Deployments and enforces that `spec.replicas` is greater than or equal to 2. The comparison operator is expressed as a string inside the `pattern` field.

```yaml theme={null}
