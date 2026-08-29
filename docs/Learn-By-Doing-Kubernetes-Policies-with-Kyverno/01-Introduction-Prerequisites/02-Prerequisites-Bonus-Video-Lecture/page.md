# Prerequisites Bonus Video Lecture

Source: https://notes.kodekloud.com/docs/Learn-By-Doing-Kubernetes-Policies-with-Kyverno/Introduction-Prerequisites/Prerequisites-Bonus-Video-Lecture/page

Introduction to Kyverno, a Kubernetes native policy engine that validates and mutates resources using CRDs to enforce governance and best practices

Hey everyone, it's Srinivas from KodeKloud. In this lesson we’ll learn about Kyverno — a Kubernetes-native policy engine that validates and mutates Kubernetes resources using familiar Kubernetes-style CRDs. Kyverno helps enforce organization policies (labels, image sources, resource limits, replica counts, network policies, etc.) so that resource creation and updates comply with governance and best practices.

We’ll cover:

* What Kyverno is
* How Kyverno works inside the API server admission flow
* Example policies (validation and mutation) and a short demo workflow

<Frame>
  <img alt="The image contains an icon on the left and a list on the right with the headings: &#x22;What is Kyverno?&#x22;, &#x22;How Kyverno Works?&#x22;, and &#x22;Quick Demo: Some Example Policies.&#x22; The background is black." />
</Frame>

## Why use Kyverno?

Consider a simple Deployment manifest you might apply to a cluster:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: nginx
```

When you run `kubectl apply`, Kubernetes validates manifest syntax and authorizations, but it won't enforce organization-specific policies by default. Requiring labels, disallowing public registries, enforcing resource requests/limits, or rejecting `:latest` images manually is error-prone and hard to scale.

Automating policy enforcement with Kyverno ensures consistency, lowers developer feedback latency, and preserves compliance without slowing delivery.

<Frame>
  <img alt="The image depicts a flowchart connecting an organization, a manager or CEO, and a platform team or developers, highlighting concepts like governance, best practices, consistency, lower latency, and agility, with the Kubernetes logo featured prominently." />
</Frame>

## Common policy examples

Below are typical policies organizations enforce via Kyverno:

| Policy intent                                  | Target resource  | Example pattern                                        |
| ---------------------------------------------- | ---------------- | ------------------------------------------------------ |
| Require images from an approved registry       | Pods/Deployments | `kodekloud.io/*`                                       |
| Ensure globally unique Ingress hostnames       | Ingress          | (match host uniqueness via custom logic or validation) |
| Require resource requests/limits on containers | Pods/Deployments | validate `spec.containers[*].resources`                |
| Deny traffic unless allowed by NetworkPolicy   | Pods/Namespaces  | deny when no NetworkPolicy applies                     |

You can adopt these examples to fit your environment (private registry prefix, minimum replicas, allowed namespaces, etc.).

<Frame>
  <img alt="The image lists four requirements: images must be from an approved repository, ingress hostnames must be globally unique, pods must have resource limits, and traffic must be denied without network policies." />
</Frame>

## Where Kyverno integrates with Kubernetes

Incoming API requests pass through authentication and authorization, then the admission controller pipeline. Admission webhooks can mutate or validate requests before objects are persisted to etcd. Kyverno runs as an admission webhook (a third-party policy agent) and can perform mutations and validations in the mutating and validating admission stages.

If a request complies with Kyverno policies, the webhook allows it; otherwise it is denied or logged (depending on policy action).

<Frame>
  <img alt="The image is a flowchart illustrating the process of handling an API request with Kyverno, detailing steps like authentication, admission, and validation before storing in ETCD. It highlights the role of a Policy Agent in the mutating and validating admission stages." />
</Frame>

## Installing Kyverno

Kyverno is distributed via Helm. Installing creates the necessary CustomResourceDefinitions (CRDs) and deploys Kyverno controllers plus the admission webhook.

Add the Helm repo, refresh, and inspect the chart:

```bash theme={null}
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update
helm search repo kyverno -l
```

A straightforward install (adjust replica counts for HA):

```bash theme={null}
helm install kyverno kyverno/kyverno -n kyverno --create-namespace \
  --set admissionController.replicas=3 \
  --set backgroundController.replicas=2 \
  --set cleanupController.replicas=2 \
  --set reportsController.replicas=2
```

Verify the Kyverno CRDs:

```bash theme={null}
kubectl get crd | grep kyverno
```

Kyverno also provides an optional chart that ships pre-configured policies implementing the Kubernetes Pod Security Standards:

```bash theme={null}
helm install kyverno-policies kyverno/kyverno-policies -n kyverno
```

## Policy basics (CRDs and actions)

Kyverno introduces CRDs such as `ClusterPolicy` and `Policy`. Policies can:

* Validate requests (deny or audit violations).
* Mutate requests before admission.
* Generate reports.

Use `validationFailureAction` to control enforcement:

<Callout icon="lightbulb">
  Set `validationFailureAction` to `Enforce` to deny non-compliant requests, or `Audit` to allow requests but record violations for reporting.
</Callout>

### Example 1 — Require a `team` label on Deployments

ClusterPolicy that enforces a non-empty `team` label on Deployments:

```yaml theme={null}
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-deployment-team-label
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-deployment-team-label
      match:
        any:
          - resources:
              kinds:
                - Deployment
      validate:
        message: "You must have label `team` for all deployments"
        pattern:
          metadata:
            labels:
              team: "?*"
```

Key points:

* `match` targets resource kinds (here: `Deployment`).
* `validate.message` is returned when the rule is violated.
* The pattern `team: "?*"` requires a non-empty string for the `team` label.

Apply the policy and verify:

```bash theme={null}
kubectl apply -f label-policy.yaml
kubectl get clusterpolicy
```

Creating a Deployment without the `team` label will be denied by Kyverno’s admission webhook:

```bash theme={null}
kubectl apply -f deployment.yaml
