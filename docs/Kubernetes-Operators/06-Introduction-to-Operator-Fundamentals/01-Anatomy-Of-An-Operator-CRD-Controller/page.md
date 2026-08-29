# Anatomy Of An Operator CRD Controller

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Introduction-to-Operator-Fundamentals/Anatomy-Of-An-Operator-CRD-Controller/page

Explains Kubernetes operators by comparing CRD as interface and controller as machinery, showing reconcile loop, child resources, RBAC, and practical tips.

When you first open an operator project it can feel like a warehouse full of boxes: Go files, YAML manifests, generated code, RBAC rules, tests, webhooks, and deployment manifests. It’s easy to lose sight of the core components that actually implement the operator.

This guide strips that complexity down to the essentials so you can immediately see where the operator lives and what each piece does.

<Frame>
  <img alt="The image shows the title &#x22;A Warehouse Full of Boxes&#x22; with filenames like main.go, types.go, and deployment.yaml scattered around, and a central question: &#x22;Where's the operator?&#x22;." />
</Frame>

Conceptually, think of an operator as a vending machine.

* The CRD (CustomResourceDefinition) is the front panel: the set of buttons and the display where users make requests.
* The controller is the internal machinery: motors, coils, and control logic that translate button presses into actions.

Buttons without machinery do nothing, and machinery without buttons cannot receive orders. An operator requires both the CRD (the interface) and the controller (the implementation).

<Frame>
  <img alt="The image illustrates the concept of an operator as two components glued together: an interface labeled &#x22;CRD&#x22; for asking and machinery labeled &#x22;controller&#x22; for doing the work." />
</Frame>

What the CRD does

* A CRD teaches Kubernetes a new kind of API object (for example, `WebApp`).
* After the CRD is installed, you can `kubectl create`, `kubectl get`, and `kubectl delete` those custom resources just like built-in types.

Example: a `WebApp` resource introduced into the `webapp.codecloud.com/v1` API group will appear as a first-class Kubernetes resource.

<Frame>
  <img alt="The image illustrates how a Custom Resource Definition (CRD) registers a new kind, &#x22;webapps,&#x22; into the Kubernetes API." />
</Frame>

WebApp resources typically follow the common Kubernetes pattern of separating desired state from observed state:

* `spec` — the desired state the user requests.
* `status` — the observed state the controller reports back.

Example WebApp manifest:

```yaml theme={null}
kind: WebApp
spec:
  image: nginx
  replicas: 3
status:
  ready: true
```

Quick reference: common `WebApp` fields

| Field           | Purpose                       | Example |
| --------------- | ----------------------------- | ------- |
| `spec.image`    | Container image to run        | `nginx` |
| `spec.replicas` | Number of desired replicas    | `3`     |
| `status.ready`  | Controller-reported readiness | `true`  |

What the controller does
The controller is the running program that watches `WebApp` objects and executes a reconcile loop to make reality match the `spec`. Concretely, reconciliation follows this pattern:

1. Read the `spec` (what the user asked for).
2. Inspect the current cluster state (what exists now).
3. Create, update, or delete child resources to move the cluster toward the desired state.
4. Update the `status` field to reflect what was actually achieved.

<Frame>
  <img alt="The image depicts a process involving a controller running a reconcile() function, which includes reading what is asked for and inspecting existing conditions, as part of an operator API workflow." />
</Frame>

Typical child resources created by a WebApp controller

* Deployment — defines the Pod template and replica count.
* Pod — the running container instance(s).
* Service — stable network identity and load-balancing for Pods.
* ConfigMap — configuration data as key/value pairs.

Linking parent and child objects
The controller sets an `ownerReference` on child objects that points back to the parent `WebApp`. With proper `ownerReferences`, Kubernetes’ garbage collector automatically deletes child objects when the parent is removed.

Around the reconcile loop: supporting pieces in an operator project

* Manager — boots and hosts one or more controllers and shared resources.
* Cache / Informers — a local, read-efficient view of cluster objects used by controllers.
* Client — API client for reading and mutating cluster state.
* RBAC — the set of Kubernetes permissions that determine what actions the controller can perform.

> **lightbulb** Keep the vending machine mental model: the CRD is the front interface, the controller is the machinery that performs work, child Kubernetes objects are the items produced, and `status` reports the result back to users and tooling.

<Frame>
  <img alt="The image illustrates a vending machine metaphor for a process, with elements labeled as &#x22;CRD&#x22; (the front), &#x22;Controller&#x22; (the machinery inside), and &#x22;Child objects&#x22; (what comes out), explaining their functions." />
</Frame>

A few practical tips and resources

* Always verify your controller's RBAC rules include permissions for resources it reads and writes (CRs, Deployments, Pods, Services, ConfigMaps, etc.). Missing RBAC permissions are a common source of runtime failures.
* Use `ownerReferences` so Kubernetes can automatically garbage-collect resources you create.
* Prefer the controller-runtime manager and informers to avoid writing low-level watch code.

> **warning** If your controller lacks appropriate RBAC permissions, reconciliation will fail silently or produce events. Always audit the Role/ClusterRole and RoleBinding/ClusterRoleBinding in your operator manifests.

Links and references

* Kubernetes CustomResourceDefinition (CRD) docs: [https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* Controller pattern and reconciliation: [https://kubernetes.io/docs/concepts/architecture/controller/](https://kubernetes.io/docs/concepts/architecture/controller/)
* controller-runtime and operator SDK: [https://github.com/kubernetes-sigs/controller-runtime](https://github.com/kubernetes-sigs/controller-runtime)

Once you internalize this shape—the CRD as the interface and the controller as the reconciler—the larger project layout and generated files become much easier to navigate and reason about.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/7d198de7-d651-4c7e-a61d-166023fc1031/lesson/ffe6bab3-b9b3-45d5-9204-22a7c41c1222)
