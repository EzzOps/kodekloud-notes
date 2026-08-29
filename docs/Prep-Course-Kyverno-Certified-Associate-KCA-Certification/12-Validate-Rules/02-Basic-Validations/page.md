# Validate images when a Pod is created directly
- name: validate-pods
  match:
    any:
      - resources:
          kinds:
            - Pod
  validate:
    pattern:
      spec:
        containers:
          - image: "registry.domain.com/*"
```

When targeting controllers that embed Pod templates at `spec.template.spec`, he must create another rule:

```yaml theme={null}
# Validate images for controllers that embed a pod template at spec.template.spec
- name: validate-deployments-statefulsets
  match:
    any:
      - resources:
          kinds:
            - Deployment
            - StatefulSet
            - DaemonSet
            - Job
  validate:
    pattern:
      spec:
        template:
          spec:
            containers:
              - image: "registry.domain.com/*"
```

CronJobs use a different path (`spec.jobTemplate.spec.template.spec`), requiring yet another nearly identical rule:

```yaml theme={null}
# Validate images for CronJobs
- name: validate-cronjobs
  match:
    any:
      - resources:
          kinds:
            - CronJob
  validate:
    pattern:
      spec:
        jobTemplate:
          spec:
            template:
              spec:
                containers:
                  - image: "registry.domain.com/*"
```

Maintaining multiple variants of the same rule quickly becomes tedious. Kyverno’s autogen feature solves this by generating controller-specific rules from a Pod-focused rule.

Autogen: write once, apply everywhere

The core idea: author your policy for the lowest-level resource you care about (Pod). Kyverno will auto-generate the corresponding policies for controllers that create Pods.

<Frame>
  <img alt="The image explains Kyverno's solution to focus on pods, highlighting the principle of focusing on the lowest-level object and writing policies targeting pods. It suggests that Kyverno will handle complex rules automatically." />
</Frame>

Here’s the simplified policy Alex now writes — only targeting Pod objects:

```yaml theme={null}
# Single policy that targets Pods — Kyverno will autogenerate controller-specific rules
- name: validate-registries
  match:
    any:
      - resources:
          kinds:
            - Pod
  validate:
    failureAction: Enforce
    message: "Images may only come from our internal enterprise registry."
    pattern:
      spec:
        containers:
          - image: "registry.domain.com/*"
```

When applied, Kyverno activates autogen and creates equivalent rules for controllers automatically. You can inspect the policy status in-cluster and check `status.autogen.rules` to review what Kyverno generated:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
spec:
  # ... original Pod-only rule ...
status:
  autogen:
    rules:
      - name: autogen-validate-registries
        # ... generated rule for Deployments, StatefulSets, Jobs, DaemonSets, etc. ...
      - name: autogen-cronjob-validate-registries
        # ... generated rule for CronJobs ...
```

Example generated rules

Kyverno wraps your Pod pattern inside controller-specific paths.

Most controllers (Deployment, StatefulSet, DaemonSet, Job, etc.) get rules that place the Pod pattern under `spec.template.spec`:

```yaml theme={null}
# Example generated rule for most controllers
- name: autogen-validate-registries
  match:
    any:
      - resources:
          kinds:
            - Deployment
            - StatefulSet
            - DaemonSet
            - Job
            # ... other common controllers ...
  validate:
    message: "Images may only come from our internal enterprise registry."
    pattern:
      spec:
        template:
          spec:
            containers:
              - image: "registry.domain.com/*"
```

CronJobs receive a separate generated rule because their Pod template is nested at `spec.jobTemplate.spec.template.spec`:

```yaml theme={null}
# Example generated rule for CronJobs
- name: autogen-cronjob-validate-registries
  match:
    any:
      - resources:
          kinds:
            - CronJob
  validate:
    message: "Images may only come from our internal enterprise registry."
    pattern:
      spec:
        jobTemplate:
          spec:
            template:
              spec:
                containers:
                  - image: "registry.domain.com/*"
```

Controlling autogen behavior

If you need fine-grained control over which controllers receive generated rules, Kyverno exposes the `pod-policies.kyverno.io/autogen-controllers` annotation on the policy.

Examples:

```yaml theme={null}
# Generate rules only for Deployment and Job controllers
pod-policies.kyverno.io/autogen-controllers: "Deployment,Job"
```

```yaml theme={null}
# Disable autogen for this policy; only Pod objects will be validated
pod-policies.kyverno.io/autogen-controllers: "none"
```

When autogen is skipped

Autogen is conservative and will skip generation if the original rule is too specific or otherwise cannot be safely translated to parent controller objects. Scenarios that prevent autogen include:

* Matching a Pod by name (controller resource names differ).
* Using label selectors or annotation filters that apply specifically to Pods and cannot be sensibly applied to controllers.
* The rule’s `kinds` list contains resources other than `Pod` (e.g., `ConfigMap`, `Secret`).

<Frame>
  <img alt="The image outlines conditions under which Kyverno autogen is skipped, highlighting issues related to names, selectors, and annotations in Kubernetes." />
</Frame>

To maximize the chances that autogen runs for your rule:

* Target only `Pod` in the `kinds` list.
* Avoid name-based matches, Pod-specific selectors, or predicates that cannot be translated to controllers.

<Frame>
  <img alt="The image explains when autogen is skipped, indicating it works only if the rule's kinds list contains only &#x22;Pod&#x22; and is disabled for lists with other kinds like &#x22;ConfigMap.&#x22;" />
</Frame>

Quick reference table

| Topic                   | Behavior / Example                                                                                       |
| ----------------------- | -------------------------------------------------------------------------------------------------------- |
| Author focus            | Write the rule for `Pod` (lowest-level object).                                                          |
| Autogen default         | Kyverno generates rules for common controllers (Deployment, StatefulSet, DaemonSet, Job, CronJob, etc.). |
| Check generated rules   | Inspect `status.autogen.rules` in the policy object.                                                     |
| Restrict autogen        | Use annotation `pod-policies.kyverno.io/autogen-controllers: "Deployment,Job"`                           |
| Disable autogen         | Use annotation `pod-policies.kyverno.io/autogen-controllers: "none"`                                     |
| When autogen is skipped | Name matches, Pod-only selectors/annotations, or `kinds` includes non-Pod resources.                     |

<Callout icon="lightbulb">
  Autogen simplifies policy management, but always review the generated rules in `status.autogen.rules` to confirm they match your intent — especially when working with custom controllers or operator-managed resources.
</Callout>

Summary

* Problem: Pods are created via many controllers and live at different JSON paths, which used to require multiple, nearly identical rules.
* Solution: Write a single Pod-targeting rule and let Kyverno autogen produce controller-specific rules automatically.
* Customization: Use `pod-policies.kyverno.io/autogen-controllers` annotation to limit or disable autogen.
* Safety: Kyverno skips autogen for rules that are too specific or otherwise cannot be translated to controller resources.

<Frame>
  <img alt="The image illustrates a three-step process titled &#x22;How It Works&#x22; related to creating and adapting policy rules for Kyverno. Each step is numbered and described, focusing on targeting pods, generating necessary rules, and adapting validation paths." />
</Frame>

<Frame>
  <img alt="The image contains a summary and key takeaways, highlighting two points: customization options through annotations for controllers and limitations where autogen is skipped based on certain criteria." />
</Frame>

Further reading and references

* Kyverno Documentation — Policies and Autogen (see Kyverno docs for the latest details).
* Kubernetes API conventions and controller patterns:
  * [Kubernetes Controllers](https://kubernetes.[AWS_SECRET_ACCESS_KEY]/)
  * [Pod Template spec paths](https://kubernetes.io/docs/concepts/workloads/controllers/)

Using autogen will dramatically simplify your policy set and make it more robust and maintainable.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/b33740d9-ee2b-4dbb-868c-a40ce74692ea" />
</CardGroup>


# Basic Validations

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Validate-Rules/Basic-Validations/page

Explains creating a Kyverno ClusterPolicy that enforces that every new Kubernetes Namespace includes the label purpose with value production for cost allocation and governance

In this lesson, you'll learn the most common and fundamental way to validate resources in Kyverno: using a pattern-based validate rule.

Meet Alex, a platform engineer with a simple but important requirement: he must ensure every new Namespace in the cluster is labeled with its intended purpose so cost allocation and governance remain accurate.

<Frame>
  <img alt="The image outlines a goal related to enforcing namespace labels to ensure cost allocation and governance, requiring a label 'purpose' with the value 'production' for new namespaces. It features a character named Alex along with a quotation explaining the goal." />
</Frame>

Goal: enforce that every newly created Namespace must include a label `purpose: production`. This prevents accidental or untracked Namespace creation and is an ideal use case for a Kyverno validate rule.

Below we build a cluster-scoped policy step-by-step to enforce this requirement.

## ClusterPolicy: require-ns-purpose-label

We use `ClusterPolicy` because the rule must apply to all Namespaces regardless of where they are created.

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-ns-purpose-label
spec:
  rules:
  - name: require-ns-purpose-label
    # The `match` block sets the scope. We are targeting any resource of kind "Namespace".
    match:
      any:
      - resources:
          kinds:
          - Namespace

    # The `validate` block defines the check that must pass for matched resources.
    validate:
      message: "Validation error: You must have label `purpose` with value `production` set on all new namespaces."
      pattern:
        metadata:
          labels:
            purpose: production
```

What each section does:

| Field                   | Purpose                                                         | Example / Notes                                            |
| ----------------------- | --------------------------------------------------------------- | ---------------------------------------------------------- |
| `kind: ClusterPolicy`   | Makes the policy cluster-scoped so it applies to all namespaces | Use `Policy` for a namespaced policy instead               |
| `match.resources.kinds` | Targets resources this rule applies to                          | `Namespace` ensures only Namespace creations are validated |
| `validate.message`      | Custom error text shown to users when validation fails          | Helps guide users to fix the request                       |
| `validate.pattern`      | The expected structure/values the incoming resource must match  | Here: `metadata.labels.purpose: production`                |

## How the pattern works

* Kyverno compares the incoming Namespace resource to the `pattern`.
* If the pattern is present and matches (exact `purpose: production`), Kyverno allows the request.
* If the pattern is missing, the label value differs, or the labels block is absent, Kyverno rejects the request with the provided message.

## Compliant example

A Namespace manifest that satisfies the policy:

```yaml theme={null}
apiVersion: v1
kind: Namespace
metadata:
  name: good-namespace
  labels:
    purpose: production
```

Kyverno will find `metadata.labels.purpose: production` and allow the Namespace creation.

## Non-compliant example

A Namespace manifest that fails validation:

```yaml theme={null}
apiVersion: v1
kind: Namespace
metadata:
  name: bad-namespace
  labels:
    purpose: development
```

Because `purpose` is `development` (not `production`), Kyverno will block the request.

<Callout icon="lightbulb">
  If validation fails, users receive immediate feedback when they run `kubectl apply`, preventing misconfigurations before resources are created.
</Callout>

Example kubectl failure output for the non-compliant manifest:

```bash theme={null}
$ kubectl apply -f bad-namespace.yaml
Error from server: admission webhook "validate.kyverno.svc" denied the request:
resource Namespace/bad-namespace was blocked due to the following policies
require-ns-purpose-label:
require-ns-purpose-label: 'Validation error: You must have label `purpose` with value `production` set on all new namespaces.'
```

The error identifies the admission webhook, the blocked resource, the policy that triggered it, and the custom message — giving the user a clear action to resolve the failure.

## Further reading

* Kyverno validation docs: [https://kyverno.io/docs/writing-policies/validate/](https://kyverno.io/docs/writing-policies/validate/)
* Kubernetes Namespaces: [https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

That's it for this lesson — a simple validate pattern can enforce important governance controls like required labels across your cluster.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/f5dd3064-bb37-41e2-8092-362f4cd56c57/lesson/84d27a51-caa8-40d0-8c8a-7e4314ea4685" />
</CardGroup>
