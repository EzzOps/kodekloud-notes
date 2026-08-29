# 1. Add the Kyverno Helm repository (do this once)
helm repo add kyverno https://kyverno.github.io/kyverno/

# 2. Update your local Helm repositories
helm repo update

# 3. Install Kyverno into the 'kyverno' namespace (creates the namespace if needed)
helm install kyverno kyverno/kyverno -n kyverno --create-namespace
```

What the commands do

* `helm repo add kyverno https://kyverno.github.io/kyverno/` adds the official Kyverno Helm repository to your local Helm configuration.
* `helm repo update` refreshes Helm's local chart index so you get the latest chart versions.
* `helm install kyverno kyverno/kyverno -n kyverno --create-namespace` installs the chart with the release name `kyverno` into namespace `kyverno`, creating the namespace if required.

Installation modes comparison

| Mode                   | Use case                                   | Characteristics                                                                             |
| ---------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Standalone             | Learning, development, small test clusters | Single replica per controller, lower resource consumption                                   |
| High availability (HA) | Production clusters                        | Multiple replicas per controller, resilient to failures, recommended for critical workloads |

Verify the installation
After Helm finishes, Kubernetes resources are created by the chart. Check that Kyverno's controllers are deployed and ready:

```bash theme={null}
kubectl get deployments -n kyverno
```

Example output:

```bash theme={null}
NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
kyverno-admission-controller     1/1     1            1           60s
kyverno-background-controller    1/1     1            1           60s
kyverno-cleanup-controller       1/1     1            1           60s
kyverno-reports-controller       1/1     1            1           60s
```

When the deployments report READY and AVAILABLE replicas, Kyverno controllers are running.

Service accounts and RBAC
The Helm chart creates a dedicated service account per controller so each controller can be granted least-privilege access. List the service accounts:

```bash theme={null}
kubectl get serviceaccounts -n kyverno
```

Example output:

```bash theme={null}
NAME                             SECRETS   AGE
default                          1         44s
kyverno-admission-controller     0         44s
kyverno-background-controller    0         44s
kyverno-cleanup-controller       0         44s
kyverno-reports-controller       0         44s
```

Kyverno requires cluster-level visibility and permissions to validate, mutate, and generate resources. The Helm chart creates ClusterRoles and ClusterRoleBindings for admission, background processing, cleanup, reporting, and other controller responsibilities. To inspect Kyverno-related cluster roles:

```bash theme={null}
kubectl get clusterroles | grep -i kyverno
```

Common resources created by the Helm chart

| Resource type                      | Purpose                                                              | Example / command                           |                   |
| ---------------------------------- | -------------------------------------------------------------------- | ------------------------------------------- | ----------------- |
| Deployments                        | Runs controller components (admission, background, cleanup, reports) | `kubectl get deployments -n kyverno`        |                   |
| ServiceAccounts                    | Per-controller identity for RBAC                                     | `kubectl get serviceaccounts -n kyverno`    |                   |
| ClusterRoles / ClusterRoleBindings | Provide cluster-scoped permissions used by controllers               | \`kubectl get clusterroles                  | grep -i kyverno\` |
| ConfigMaps / Secrets               | Configuration and TLS secrets for admission webhook                  | `kubectl get configmaps,secrets -n kyverno` |                   |

At this point, Kyverno is installed, running, and has the permissions required to enforce and manage policies.

<Callout icon="lightbulb">
  To switch to high availability later, update the Helm values to increase replica counts (or use the HA values provided by the chart) and perform a Helm upgrade.
</Callout>

Next steps
We'll cover how to author and apply Kyverno policies to enforce guardrails across your cluster, including examples for validation, mutation, and generation policies.

Links and references

* [Helm — Kubernetes package manager](https://helm.sh/)
* [Kyverno documentation](https://kyverno.io/docs/)
* [Kubernetes RBAC documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/8cf118e1-7ca8-49b6-be5a-af80c331f394/lesson/a181d17f-8c8e-4c38-983e-e407a8f79fb1" />
</CardGroup>


# Kyverno Architecture Part 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Kyverno-Certified-Associate-KCA-Certification/Kyverno-Introduction/Kyverno-Architecture-Part-1/page

Overview of Kyverno's integration with the Kubernetes API server via mutating and validating admission webhooks, request flow, webhook configuration, failure policies, and mutation before validation

In this lesson we'll explore Kyverno's architecture and how it integrates with the Kubernetes API server during admission control. This installment focuses on request flow (authentication → authorization → admission) and where Kyverno plugs into that lifecycle. We will not write policies here — instead, we'll understand how API requests are intercepted, mutated, or validated by Kyverno.

<Callout icon="lightbulb">
  Lesson goal: Understand how the Kubernetes API server routes admission requests to Kyverno webhooks, what webhook configuration controls, and how mutation and validation are ordered during admission.
</Callout>

When a client submits an API request (for example, creating a Pod or Deployment), the Kubernetes API server performs:

1. Authentication — verifies the identity of the caller.
2. Authorization — checks whether the caller is allowed to perform the requested action.
3. Admission — a pluggable phase where requests can be mutated or validated before persistence.

Kyverno participates in the admission phase using admission webhooks. It registers MutatingWebhookConfiguration and ValidatingWebhookConfiguration resources so the API server knows which requests to forward to Kyverno.

<Frame>
  <img alt="The image explains Kyverno's role in admission control, detailing how an API server calls Kyverno using mutating and validating webhooks for changes and checks. It includes a flowchart of the admission controller phases, showing interactions with webhooks during mutating and validating admissions." />
</Frame>

How Kyverno handles a forwarded request:

* The API server sends the request payload to Kyverno’s webhook endpoint.
* Kyverno locates policies that match the resource kind, namespace, and operation.
* For mutating policies, Kyverno computes patches and returns them so the API server applies the mutation.
* For validating policies, Kyverno returns an allow or deny decision.
* The API server proceeds using Kyverno’s response (apply mutation, accept, or reject).

<Frame>
  <img alt="The image outlines Kyverno's role in admission control, showing how the API server interacts with Kyverno via MutatingWebhookConfiguration and ValidatingWebhookConfiguration. It also illustrates the phases of the admission controller process including mutating and validating admissions." />
</Frame>

Webhook configuration essentials

Webhook resources are regular Kubernetes objects. They instruct the API server:

* WHAT to intercept (which resources, operations, API groups/versions).
* WHERE to send the request (the service/endpoint hosting the webhook).
* WHAT IF the webhook does not respond (failure behavior and timeouts).

| Concept                   | Purpose                                                                         | Example field                     |
| ------------------------- | ------------------------------------------------------------------------------- | --------------------------------- |
| WHAT to intercept         | Limit which requests are sent to the webhook (improves performance and scoping) | `rules`                           |
| WHERE to send requests    | Kubernetes Service and path that receives admission calls                       | `clientConfig.service`            |
| WHAT IF it doesn't answer | Decide how the API server behaves on webhook failure or timeout                 | `failurePolicy`, `timeoutSeconds` |

<Frame>
  <img alt="The image explains webhook configuration with three steps: intercepting specific resources and operations, specifying the service endpoint for Kyverno, and handling failures with a failure policy." />
</Frame>

Choosing a failure policy

* `failurePolicy: Fail` — if Kyverno is unavailable, the API server rejects the request (more secure).
* `failurePolicy: Ignore` — if Kyverno doesn't respond, the API server continues without enforcement (more available).

<Callout icon="warning">
  Set `failurePolicy: Fail` only when Kyverno is deployed with sufficient high availability. Using `Fail` in single-replica or unstable Kyverno setups can block legitimate requests during outages.
</Callout>

Ordering: mutation before validation

Admission webhooks run in phases. Mutating webhooks are invoked first (and can change the object), followed by validating webhooks which evaluate the final object state. This ordering ensures validation policies assess the object after all mutations have been applied.

Example scenario:

* Mutating policy: add a label to every new Deployment.
* Validating policy: reject Deployments with more than 2 replicas.

When a Deployment is created, Kyverno will first add the label (mutating phase), then validate the final Deployment object (validating phase). If the replica count exceeds 2, the API server will reject the request.

<Frame>
  <img alt="The image illustrates a workflow for deployment mutation and validation, detailing two policies: one for mutating deployments to add a label and another for validating the replica count. It involves steps using mutating and validating webhook configurations to ensure proper validation." />
</Frame>

Example ValidatingWebhookConfiguration

Below is a simplified `ValidatingWebhookConfiguration` demonstrating the WHAT / WHERE / WHAT IF mapping. Note how `rules` selects requests, `clientConfig` points to the Kyverno service endpoint, and `failurePolicy`/`timeoutSeconds` control error handling.

```yaml theme={null}
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: kyverno-resource-validating-webhook-cfg
webhooks:
  - name: validate.kyverno.svc-fail
    rules: # WHAT to intercept
      - apiGroups: ["apps"]
        apiVersions: ["v1"]
        operations: ["CREATE"]
        resources: ["deployments"]
    clientConfig:  # WHERE to send it
      service:
        name: kyverno-svc
        namespace: kyverno
        path: /validate/fail
        port: 443
    timeoutSeconds: 10  # How long to wait for Kyverno
    failurePolicy: Fail  # WHAT IF it fails (options: Fail, Ignore)
```

Automatic webhook registration by Kyverno

You do not need to create these webhook configurations manually. Kyverno automatically inspects policies you apply and generates or updates the appropriate MutatingWebhookConfiguration and ValidatingWebhookConfiguration objects. When policies are removed, Kyverno cleans up the webhook rules it created.

<Frame>
  <img alt="The image outlines the automatic webhook registration process with four steps: writing a Kyverno policy, examining resource kinds, creating configurations, and instructing the API server." />
</Frame>

References and further reading

* Kubernetes Admission Controllers and Webhooks: [https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/)
* Kyverno documentation: [https://kyverno.io/docs/](https://kyverno.io/docs/)

Summary

* Kyverno integrates with the API server via Mutating and Validating webhooks during the admission phase.
* Webhook configuration controls WHAT is intercepted, WHERE the API server sends requests, and WHAT IF the webhook fails.
* Mutations run before validations, so validation policies evaluate the final mutated object.
* Kyverno automatically manages webhook registration based on the policies you create.

This concludes Part 1 of the Kyverno architecture series.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kyverno-certified-associate/module/8cf118e1-7ca8-49b6-be5a-af80c331f394/lesson/d2114aa0-c62d-4442-b470-31844d46cce9" />
</CardGroup>
