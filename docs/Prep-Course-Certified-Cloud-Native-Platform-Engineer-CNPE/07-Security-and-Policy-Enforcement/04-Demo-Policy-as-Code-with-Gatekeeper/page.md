# Output:
# namespace/pss-baseline labeled
```

3. Create a Pod that violates baseline to see the enforcement behavior

Save this as `privileged-pod.yaml`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: privileged-app
spec:
  hostNetwork: true
  containers:
    - name: app
      image: nginx:alpine
      securityContext:
        privileged: true
```

Apply it into `pss-baseline`:

```bash theme={null}
kubectl apply -f privileged-pod.yaml -n pss-baseline
```

You will see an error because baseline forbids host namespaces and privileged containers:

```bash theme={null}
Error from server (Forbidden): error when creating "privileged-pod.yaml": pods "privileged-app" is forbidden: violates PodSecurity "baseline:latest": host namespaces (hostNetwork=true) are prohibited, privileged (container "app" must not set securityContext.privileged=true)
```

4. Try a standard nginx Pod that baseline will admit but restricted will warn on

Use `kubectl run` for a quick test:

```bash theme={null}
kubectl run baseline-test --image=nginx:alpine -n pss-baseline
```

Admission will allow the Pod but print warnings (because `pss-baseline` has `warn`/`audit` for `restricted`):

```bash theme={null}
Warning: would violate PodSecurity "restricted:latest": 
- allowPrivilegeEscalation != false (container "baseline-test" must set securityContext.allowPrivilegeEscalation=false)
- capabilities not dropped (container "baseline-test" must set securityContext.capabilities.drop=["ALL"])
- runAsNonRoot != true (pod or container "baseline-test" must set securityContext.runAsNonRoot=true)
- seccompProfile not set (pod or container "baseline-test" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
pod/baseline-test created
```

These warnings let you discover which fields to add to meet the stricter profile without blocking workloads.

5. Enforce the `restricted` profile on another namespace and observe rejections

Label `pss-restricted` to enforce:

```bash theme={null}
kubectl label namespace pss-restricted pod-security.kubernetes.io/enforce=restricted
# Output:
# namespace/pss-restricted labeled
```

Try to run the same nginx image there:

```bash theme={null}
kubectl run restricted-test --image=nginx:alpine -n pss-restricted
```

Since `restricted` is in `enforce` mode, creation is blocked and the required corrections are listed:

```bash theme={null}
Error from server (Forbidden): pods "restricted-test" is forbidden: violates PodSecurity "restricted:latest":
- allowPrivilegeEscalation != false (container "restricted-test" must set securityContext.allowPrivilegeEscalation=false)
- capabilities not dropped (container "restricted-test" must set securityContext.capabilities.drop=["ALL"])
- runAsNonRoot != true (pod or container "restricted-test" must set securityContext.runAsNonRoot=true)
- seccompProfile not set (pod or container "restricted-test" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```

6. Example Pod that complies with `restricted`

Save this as `restricted-pod.yaml`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: restricted-app
spec:
  containers:
    - name: app
      image: nginx/nginx-unprivileged:alpine
      securityContext:
        runAsNonRoot: true
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        seccompProfile:
          type: RuntimeDefault
```

Apply it into the restricted namespace:

```bash theme={null}
kubectl apply -f restricted-pod.yaml -n pss-restricted
# Output:
# pod/restricted-app created
```

The image `nginx/nginx-unprivileged:alpine` runs as a non-root user and the `securityContext` fields satisfy the `restricted` checks.

7. Use `warn` mode to discover non-compliant workloads (audit flow)

Create an audit namespace and start in `warn` mode:

```bash theme={null}
kubectl create namespace workload-audit
kubectl label namespace workload-audit pod-security.kubernetes.io/warn=baseline
```

Run a test Pod (baseline is permissive):

```bash theme={null}
kubectl run audit-test --image=nginx:alpine -n workload-audit
kubectl get events -n workload-audit
```

If you then change the warn label to `restricted` and create another Pod, admission prints warnings for restricted violations:

```bash theme={null}
kubectl label namespace workload-audit pod-security.kubernetes.io/warn=restricted --overwrite
kubectl run audit-test-2 --image=nginx:alpine -n workload-audit
```

Admission-time output:

```bash theme={null}
Warning: would violate PodSecurity "restricted:latest":
- allowPrivilegeEscalation != false (container "audit-test-2" must set securityContext.allowPrivilegeEscalation=false)
- capabilities not dropped (container "audit-test-2" must set securityContext.capabilities.drop=["ALL"])
- runAsNonRoot != true (pod or container "audit-test-2" must set securityContext.runAsNonRoot=true)
- seccompProfile not set (pod or container "audit-test-2" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
pod/audit-test-2 created
```

You can inspect events to correlate lifecycle events with admission-time messages:

```bash theme={null}
kubectl get events -n workload-audit
```

## Recommended minimal `securityContext` fields for `restricted`

| Field                      |    Example value | Purpose                                         |
| -------------------------- | ---------------: | ----------------------------------------------- |
| `runAsNonRoot`             |           `true` | Ensure containers don't run as UID 0.           |
| `allowPrivilegeEscalation` |          `false` | Prevent setuid binaries / privilege escalation. |
| `capabilities.drop`        |        `["ALL"]` | Remove Linux capabilities.                      |
| `seccompProfile.type`      | `RuntimeDefault` | Apply a seccomp profile at runtime.             |

Putting these into pod/container specs is the most common way to resolve `restricted` violations.

## Summary

* Start with `warn` and `audit` modes to safely discover issues.
* Fix Pod specs (set `runAsNonRoot`, `allowPrivilegeEscalation=false`, drop capabilities, set `seccompProfile`, avoid host namespaces, etc.) until warnings disappear.
* Switch to `enforce` for the target profile to block non-compliant workloads.
* PSS offers a simple, label-driven approach that is easy to audit and reverse without extra operators.

Further reading:

* [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
* [Kubernetes Pod Security Admission](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#podsecurity)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/0a0c1ba8-a55f-4023-be39-fba7a86f5fa8)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/45b8b593-7312-4acf-b1e5-093d3bc53b62)


# Demo Policy as Code with Gatekeeper

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Security-and-Policy-Enforcement/Demo-Policy-as-Code-with-Gatekeeper/page

Guide demonstrating how to use OPA Gatekeeper to enforce custom Kubernetes admission policies using ConstraintTemplates and Constraints, requiring pod labels and using dryrun, warn, or deny enforcement modes.

In this lesson you'll learn how to enforce custom Kubernetes admission policies using OPA Gatekeeper. Built-in admission controllers (for example, LimitRanger and ResourceQuota) handle resource governance, but they don't cover arbitrary policy requirements such as:

* requiring specific labels on every Pod,
* restricting images to approved registries,
* disallowing the `:latest` image tag.

Gatekeeper extends the admission pipeline with policy-as-code using two primary resources:

* ConstraintTemplate — defines a policy (registers a new CRD and contains Rego logic).
* Constraint — an instance of that policy (sets parameters, scope, and enforcement).

This guide walks through a complete example that enforces the presence of `team` and `environment` labels on Pods.

Important references:

* Gatekeeper documentation: [https://open-policy-agent.github.io/gatekeeper/](https://open-policy-agent.github.io/gatekeeper/)
* OPA/Rego language: [https://www.openpolicyagent.org/docs/latest/policy-language/](https://www.openpolicyagent.org/docs/latest/policy-language/)
* Kubernetes admission controllers: [https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

Check Gatekeeper components are running

```bash theme={null}
kubectl get pods -n gatekeeper-system
```

Example output:

```text theme={null}
NAME                                              READY   STATUS    RESTARTS   AGE
gatekeeper-audit-65f8cb8f99-49x7d                 1/1     Running   0          16m
gatekeeper-controller-manager-59874747568-bz9tr   1/1     Running   0          16m
gatekeeper-controller-manager-59874747568-ksdgp   1/1     Running   0          16m
gatekeeper-controller-manager-59874747568-lmz7s   1/1     Running   0          16m
```

## ConstraintTemplate — define the policy and CRD

Create a ConstraintTemplate that registers a new CRD `RequiredLabels` and embeds the Rego logic to detect missing labels. Save this as `required-labels-template.yaml`:

```yaml theme={null}
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: requiredlabels
spec:
  crd:
    spec:
      names:
        kind: RequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package requiredlabels

        violation[msg] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label = input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("missing required labels: %v", [missing])
        }
```

What this template does

* `spec.crd.spec.names.kind` creates the CRD Kind `RequiredLabels`.
* `openAPIV3Schema` validates the constraint parameters (`labels` must be an array of strings).
* `targets.rego` contains the Rego policy executed during admission; it compares required labels with provided labels and generates violations when labels are missing.

Apply the template:

```bash theme={null}
kubectl apply -f required-labels-template.yaml
```

Expected response:

```text theme={null}
constrainttemplate.templates.gatekeeper.sh/requiredlabels created
```

Verify the CRD exists:

```bash theme={null}
kubectl get crd | grep requiredlabels
```

Example output:

```text theme={null}
requiredlabels.constraints.gatekeeper.sh   2026-04-15T16:11:26Z
```

## Constraint — instantiate the policy

Instantiate the policy by creating a Constraint of kind `RequiredLabels`. This configures parameters, scope, and the enforcement action. Save as `required-labels-constraint.yaml`:

```yaml theme={null}
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: RequiredLabels
metadata:
  name: require-labels
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    labels:
      - team
      - environment
```

Key fields

* `enforcementAction`: `deny`, `dryrun`, or `warn`. Use `deny` to block violating requests.
* `match.kinds`: scopes the constraint to core Pods.
* `parameters.labels`: the required label keys validated by the template schema.

Apply the constraint:

```bash theme={null}
kubectl apply -f required-labels-constraint.yaml
```

Example response:

```text theme={null}
requiredlabels.constraints.gatekeeper.sh/require-labels created
```

Quick reference: Gatekeeper resources

| Resource Type      | Purpose                                         | Example                           |
| ------------------ | ----------------------------------------------- | --------------------------------- |
| ConstraintTemplate | Defines policy logic and registers a CRD        | `required-labels-template.yaml`   |
| Constraint         | Instantiates a policy, sets scope & enforcement | `required-labels-constraint.yaml` |
| Rego policy        | Policy logic executed at admission              | included in `spec.targets.rego`   |

## Test: pod without required labels (expected to be denied)

Create `test-pod-no-labels.yaml`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: unlabeled-pod
  namespace: policy-test
spec:
  containers:
    - name: nginx
      image: docker.io/library/nginx
```

Attempt to apply it:

```bash theme={null}
kubectl apply -f test-pod-no-labels.yaml -n policy-test
```

Expected admission error:

```text theme={null}
Error from server (Forbidden): error when creating "test-pod-no-labels.yaml": admission webhook "validation.gatekeeper.sh" denied the request: [require-labels] missing required labels: ["environment", "team"]
```

## Test: pod with required labels (expected to be admitted)

Create `test-pod-with-labels.yaml`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: labeled-pod
  namespace: policy-test
  labels:
    team: platform
    environment: prod
spec:
  containers:
    - name: nginx
      image: nginx
```

Apply it:

```bash theme={null}
kubectl apply -f test-pod-with-labels.yaml -n policy-test
```

Example response:

```text theme={null}
pod/labeled-pod created
```

## Dry-run mode: audit without breaking workloads

Before enforcing a blocking policy, use `dryrun` to discover existing violations safely. Patch the constraint to `dryrun`:

```bash theme={null}
kubectl patch requiredlabels require-labels \
  --type=merge \
  -p '{"spec":{"enforcementAction":"dryrun"}}'
```

Expected response:

```text theme={null}
requiredlabels.constraints.gatekeeper.sh/require-labels patched
```

Now reapply the previously rejected unlabeled pod — Gatekeeper will allow creation but will record violations:

```bash theme={null}
kubectl apply -f test-pod-no-labels.yaml -n policy-test
```

Example response:

```text theme={null}
pod/unlabeled-pod created
```

List pods in namespace `policy-test`:

```bash theme={null}
kubectl get pods -n policy-test
```

Example output:

```text theme={null}
NAME           READY   STATUS    RESTARTS   AGE
labeled-pod    1/1     Running   0          14s
unlabeled-pod  1/1     Running   0          54s
```

Describe the constraint to inspect recorded violations:

```bash theme={null}
kubectl describe requiredlabels.constraints.gatekeeper.sh require-labels
```

Example excerpt:

```text theme={null}
Total Violations: 13
Violations:
  Enforcement Action: dryrun
  Group:
    Kind: Pod
    Message: missing required labels: {"environment", "team"}
    Name: unlabeled-pod
    Namespace: policy-test
    Version: v1
  Enforcement Action: dryrun
  Group:
    Kind: Pod
    Message: missing required labels: {"environment", "team"}
    Name: kube-scheduler-ctrlplane
    Namespace: kube-system
    Version: v1
  ...
```

Enforcement action options

| Action   | Behavior                                    | Use case                        |
| -------- | ------------------------------------------- | ------------------------------- |
| `deny`   | Blocks requests that violate the constraint | Full enforcement in production  |
| `dryrun` | Allows requests but records violations      | Safe auditing and onboarding    |
| `warn`   | Allows requests and emits warnings          | Non-blocking guidance for users |

> **lightbulb** Start in `dryrun` to discover existing violations, remediate resources where needed, and then switch to `deny` to fully enforce the policy. This staged rollout pattern reduces disruption.

## Summary

* ConstraintTemplate defines a policy: it registers a CRD and contains Rego logic.
* Constraint is a policy instance: it configures parameters, scope, and enforcement mode.
* Use `dryrun` to audit and identify violations before enabling `deny`.
* Gatekeeper is an effective policy-as-code solution for Kubernetes: use it to enforce labels, image registries, tag policies, and other organizational rules.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/4808f9b3-7985-47bf-95e5-d3e2368d1aa5)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/35a7fadb-02d8-4557-a819-2e4dcfa970cc/lesson/ec93bd81-3b25-4469-9194-50fabe8b8a18)
