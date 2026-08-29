# Output example:
# NAME       SIZE   ENGINE     AGE
kubectl get db
kubectl describe db orders-db
kubectl delete db orders-db
```

The controller watches `Database` resources and drives the provisioning workflow:

* Create Kubernetes objects (Secrets, StatefulSets, Services) or external resources (cloud DB instances).
* Update the CR `status` with progress and conditions.
* Reconcile changes (scaling, backups, configuration updates).
* Clean up resources when the CR is deleted.

## Takeaways

* CRDs extend Kubernetes without modifying the control plane — they register new types with the API server.
* Custom resources use the same API URL patterns and kubectl tooling as built-in resources.
* OpenAPI v3 validation enforces correctness at the API layer before controller logic runs.
* The lifecycle is simple but powerful: CRD defines the schema, CR is the instance, and the controller implements the actions required to realize the instance.

> **lightbulb** CRDs make your platform concepts first-class Kubernetes resources so platform teams can expose domain-specific APIs that integrate seamlessly with kubectl, RBAC, GitOps, and policy engines — all without building a separate API server.

## Further reading and references

* Kubernetes API concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* kubectl overview: [https://kubernetes.io/docs/reference/kubectl/overview/](https://kubernetes.io/docs/reference/kubectl/overview/)
* RBAC docs: [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* OpenAPI v3 specification: [https://spec.openapis.org/oas/v3.0.3](https://spec.openapis.org/oas/v3.0.3)
* Gatekeeper / OPA: [https://open-policy-agent.github.io/gatekeeper/](https://open-policy-agent.github.io/gatekeeper/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/aae4d782-46cf-4e49-acd3-faf8d0fe71bd)


# Operators Controllers Reconcile Like a Pro

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-APIs-and-Self-Service-Capabilities/Operators-Controllers-Reconcile-Like-a-Pro/page

Explains Kubernetes CRDs and controllers, the reconciliation loop, status and finalizers, and best practices for building reliable operators.

We can define platform APIs with CustomResourceDefinitions (CRDs) so users create custom resources (CRs). That validates YAML with the API server, but validation alone doesn't make things happen. If you create a Database CR today, nothing will be provisioned automatically — the YAML just sits in etcd until a controller acts on it.

Controllers are the missing piece that bridge declared intent to real-world resources. In this lesson we will:

* Explain why CRDs are useful only when paired with controllers.
* Describe the reconciliation loop and its governing principles.
* Describe controller architecture and the typical reconcile function shape.
* Cover status reporting with conditions and observedGeneration.
* Implement finalizers for cleanup on deletion.
* Compare common operator frameworks so you can pick the right one.

<Frame>
  <img alt="The image outlines learning objectives related to CRDs and controller architecture, including understanding CRDs' need for controllers and explaining the reconciliation loop." />
</Frame>

This is a longer lesson because controllers are one of the most fundamental concepts in Kubernetes. Deployments, StatefulSets, Services, and every custom operator all depend on controllers to make the desired state real.

Scenario: a shiny Database CRD

A platform team builds a Database CRD with enum validations, printer columns, and a solid OpenAPI schema. They tell developers: create a database with `kubectl apply`.

<Frame>
  <img alt="The image illustrates a concept where a platform team interacts with a database CRD (Custom Resource Definition) through processes like enum validation, printer columns, and schema management." />
</Frame>

The developer applies a YAML:

<Frame>
  <img alt="The image shows a diagram with a &#x22;Platform Team&#x22; informing &#x22;Developers&#x22; that they can now create databases using kubectl apply." />
</Frame>

```yaml theme={null}
apiVersion: platform.acme.io/v1
kind: Database
metadata:
  name: orders-db
spec:
  size: medium
  engine: postgresql
```

Command:

```bash theme={null}
kubectl apply -f orders-db.yaml
