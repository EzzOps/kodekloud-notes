# or using the short flag
kyverno apply policy.yaml --resource pod.yaml -p
```

Example `PolicyReport` output:

```yaml theme={null}
apiVersion: wgpolicyk8s.io/v1alpha2
kind: PolicyReport
metadata:
  # ...
results:
- policy: require-purpose-label
  rule: require-purpose-label
  resource:
    kind: Pod
    name: my-app-pod
    namespace: default
  result: fail
  message: "You must have label `purpose` with value `production`."
# ...
summary:
  error: 0
  fail: 1
  pass: 0
  skip: 0
  warn: 0
```

Save the report as an artifact for later analysis:

```bash theme={null}
kyverno apply policy.yaml --resource pod.yaml -p > policy-report.yaml
```

Testing policies against a live cluster

To evaluate a local policy against resources already running in your Kubernetes cluster, use `--cluster` (short `-c`). The CLI connects to the API server using your current `kubeconfig` context, fetches matching resources, and evaluates them without needing the Kyverno controller deployed.

```bash theme={null}
kyverno apply policy.yaml --cluster
# with a PolicyReport
kyverno apply policy.yaml --cluster -p
```

> **lightbulb** When using `--cluster`, the CLI queries the cluster for matching resources. Note that local `--resource` files and `--cluster` mode are mutually exclusive — choose one workflow per run.

Testing PolicyExceptions locally

If you author `PolicyException` manifests, validate them locally before applying to the cluster. The CLI accepts exceptions with `--exception` (short `-e`). Provide the exception manifest alongside your policy and resource to ensure the exception logic behaves as expected.

Example test set:

* `policy.yaml` — enforces a `team` label
* `pod.yaml` — a Pod without the label
* `exception.yaml` — a `PolicyException` that exempts this Pod

<Frame>
  <img alt="The image outlines a test case for testing policy exceptions, showing a sequence of a policy, resource, and exception in YAML files related to team labels." />
</Frame>

Run the CLI with all three files; the rule result should be `skip` instead of `fail` when the exception applies:

```bash theme={null}
kyverno apply policy.yaml --resource pod.yaml --exception exception.yaml
Applying 3 policy rule(s) to 1 resource(s) with 1 exception(s)...
pass: 0, fail: 0, warn: 0, error: 0, skip: 1
```

Providing external context with Values files

Policies often reference external objects—for example, `namespaceSelector` that depends on namespace labels. When you test a single `Pod` file locally, the CLI lacks cluster context for the namespace, so evaluation can be incomplete.

Policy example using `namespaceSelector`:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: enforce-pod-name
spec:
  rules:
  - match:
      any:
      - resources:
          kinds:
          - Pod
    namespaceSelector:
      matchExpressions:
      - key: foo.com/managed-state
        operator: In
        values:
        - managed
```

Supply the missing namespace or other contextual facts using a Values file (`--values-file` or `-f`). The Values manifest has `apiVersion: cli.kyverno.io/v1alpha1` and `kind: Values`. Declare namespaced facts such as namespace labels so the CLI can evaluate selectors accurately.

Example `values.yaml`:

```yaml theme={null}
apiVersion: cli.kyverno.io/v1alpha1
kind: Values
namespaceSelector:
  - name: test1
    labels:
      foo.com/managed-state: managed
```

Then run:

```bash theme={null}
kyverno apply policy.yaml --resource pod.yaml --values-file values.yaml
# short flags
kyverno apply policy.yaml --resource pod.yaml -f values.yaml
```

This tells the CLI that the `test1` namespace has the `foo.com/managed-state: managed` label, enabling correct evaluation of `namespaceSelector` conditions during local tests.

> **warning** Ensure your Values file uses the correct API version and structure (`apiVersion: cli.kyverno.io/v1alpha1`, `kind: Values`) and accurately models the namespace labels or other objects referenced by your policy; otherwise selectors may evaluate incorrectly.

Quick reference: common `kyverno apply` flags

| Flag                    | Purpose                                                                       | Example                                                                    |
| ----------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `-p`, `--policy-report` | Emit a `PolicyReport` YAML to stdout (CI-friendly)                            | `kyverno apply policy.yaml --resource pod.yaml -p`                         |
| `-c`, `--cluster`       | Evaluate policy against resources fetched from the current kubeconfig context | `kyverno apply policy.yaml --cluster`                                      |
| `-e`, `--exception`     | Provide one or more `PolicyException` manifests for evaluation                | `kyverno apply policy.yaml --resource pod.yaml --exception exception.yaml` |
| `-f`, `--values-file`   | Supply external context (namespaces, labels, etc.) via a `Values` manifest    | `kyverno apply policy.yaml --resource pod.yaml -f values.yaml`             |

Recap

* Use `-p` / `--policy-report` to produce structured `PolicyReport` output for CI and tooling.
* Use `-c` / `--cluster` to evaluate policies against live cluster resources via your current kubeconfig.
* Use `-e` / `--exception` to validate `PolicyException` behavior in local tests.
* Use `-f` / `--values-file` to provide external context (namespace labels, etc.) required by selectors and other cross-object checks.

<Frame>
  <img alt="The image is a summary list highlighting four steps related to policy evaluation: generating reports, testing live clusters, testing exceptions, and providing context. Each step is numbered and includes a brief description." />
</Frame>

Next steps

In upcoming lessons we'll cover how the CLI evaluates other rule types (mutate, validate, generate) and show how to author automated unit tests for policies.

Links and references

* Kyverno CLI docs: [https://kyverno.io/docs/kyverno-cli/](https://kyverno.io/docs/kyverno-cli/)
* Kyverno PolicyReport: [https://kyverno.io/docs/writing-policies/policy-report/](https://kyverno.io/docs/writing-policies/policy-report/)
* Kubernetes API concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f4ceb35e-5c8e-4601-856b-997a26924a4a/lesson/39a0c661-56f3-4f8c-be9d-8ef0bb6246ff)


# apply Command Part 3

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-CLI/apply-Command-Part-3/page

Using the Kyverno CLI apply to preview and save mutate and generate policy effects, including handling target resources and common flags

Earlier we looked at how the Kyverno `apply` command validates resources with a clear pass/fail result. In this lesson we’ll focus on how the Kyverno CLI previews the exact effects of `mutate` and `generate` rules so you can see the concrete changes Kyverno would perform in a real cluster.

## Previewing mutate rules

Start with a mutate policy that injects default resource requests into containers that lack them:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-resources
spec:
  rules:
    - name: add-default-requests
      match:
        any:
          - resources:
              kinds:
                - Pod
      mutate:
        foreach:
          - list: "spec.containers[]"
            patchStrategicMerge:
              spec:
                containers:
                  - (name): "{{ element.name }}"
                    resources:
                      requests:
                        +(memory): "100Mi"
                        +(cpu): "100m"
```

This policy uses `foreach` to iterate over each container in a Pod. The `+(memory)` and `+(cpu)` anchors indicate "add only if not present" — existing `resources.requests` remain untouched.

Here’s a simple NGINX Pod manifest that lacks a `resources` block:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx-demo
spec:
  containers:
    - name: nginx
      image: nginx:1.14.2
```

When Kyverno runs in a cluster this policy will mutate the Pod prior to creation so the container receives the default requests. Locally, the Kyverno CLI can render exactly that mutated YAML so you can inspect changes before applying them.

Run:

```bash theme={null}
kyverno apply policy.yaml --resource pod.yaml
```

Example CLI output (truncated for clarity):

```bash theme={null}
$ kyverno apply policy.yaml --resource pod.yaml
Applying 1 policy rule(s) to 1 resource(s)...
policy add-default-resources applied to default/Pod/nginx-demo:
apiVersion: v1
kind: Pod
metadata:
  name: nginx-demo
  namespace: default
spec:
  containers:
    - name: nginx
      image: nginx:1.14.2
      resources:
        requests:
          cpu: 100m
          memory: 100Mi
---
Mutation:
Mutation has been applied successfully.
pass: 1, fail: 0, warn: 0, error: 0, skip: 0
```

To save the mutated manifest to a file (handy for testing, CI, or debugging), add `--output` (or `-o`):

```bash theme={null}
kyverno apply policy.yaml --resource pod.yaml --output mutated-pod.yaml
```

## Advanced mutate: target vs trigger resources

Some policies are evaluated against one resource (the trigger) but mutate another resource (the target). For example, a policy that reacts to a `ConfigMap` create event and mutates an existing `Secret`. In this case provide both manifests to the CLI so Kyverno can compute the mutation.

Example policy (watches `ConfigMap`, mutates an existing `Secret`):

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: mutate-existing-secret
spec:
  rules:
    - name: mutate-secret-on-configmap-create
      match:
        any:
          - resources:
              kinds:
                - ConfigMap
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              foo: bar
        targets:
          - apiVersion: v1
            kind: Secret
            name: secret-1
            namespace: staging
```

When testing locally:

* Use `--resource` to pass the trigger (the `ConfigMap` manifest).
* Use `--target-resource` to pass the current state of the `Secret` that Kyverno should mutate.

Example CLI invocation:

```bash theme={null}
kyverno apply mutate-secret-policy.yaml --resource trigger-configmap.yaml --target-resource secret-1.yaml
```

> **lightbulb** Use `--target-resource` when the object to be mutated is not the same as the trigger resource. This lets the CLI load the target’s current state and show the exact mutation that would be performed.

## Previewing generate rules

Generate rules create new resources (for example, a `NetworkPolicy` when a `Namespace` is created). To preview a generate rule, pass the generate policy and the triggering resource with `--resource`. Kyverno CLI will print the full YAML of the generated resource (not a modified version of the trigger). This output helps you verify template variable substitution, metadata, and the final manifest. You can also save the generated YAML using `--output`.

## Quick reference: common kyverno apply flags

| Flag                | Purpose                                                                                        | Example                           |
| ------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------- |
| `--resource`        | Pass the trigger resource manifest to evaluate policies against                                | `--resource pod.yaml`             |
| `--target-resource` | Provide the current state of the object to be mutated when the target differs from the trigger | `--target-resource secret-1.yaml` |
| `--output`, `-o`    | Save the mutated or generated manifest to a file                                               | `--output mutated-pod.yaml`       |

## Recap

* The Kyverno CLI previews the exact outcome of `mutate` policies by rendering the full mutated resource YAML.
* For `generate` rules the CLI prints the generated resource YAML so you can validate the final manifest.
* Use `--output` (or `-o`) to write results to a file for testing or pipelines.
* When the mutated object differs from the trigger, pass its current state with `--target-resource` so the CLI can compute the mutation precisely.

<Frame>
  <img alt="The image is a summary with a gradient background, detailing four points related to CLI operations: preview mutations, preview generations, save results, and test mutate existing. Each point includes a brief description and is numbered with colorful labels." />
</Frame>

This is it for this lesson.

- [Watch Video](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f4ceb35e-5c8e-4601-856b-997a26924a4a/lesson/8a72365e-c791-4f2d-a0b8-5a8e56d90e4c)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f4ceb35e-5c8e-4601-856b-997a26924a4a/lesson/f80c24c6-7690-4ca3-bee8-c0e3238afbb1)
