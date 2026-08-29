# Controllers Vs Operators The Key Distinction

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Introduction-to-Operator-Fundamentals/Controllers-Vs-Operators-The-Key-Distinction/page

Explains Kubernetes controllers versus operators, where controllers run reconcile loops and operators add application domain knowledge via custom resources to manage complex lifecycle and automation.

Confusion often comes from two engineers using different words for what looks like the same thing:

One says, “We need a controller.”\
Another replies, “We need an operator.”

Both can be partly correct, but the distinction matters before you design or build anything. This guide explains what a controller does, how an operator extends that mechanism, and when to choose one over the other.

Think of a controller like a home thermostat. You set a desired temperature, the thermostat reads the actual room temperature, and it kicks on the A/C to close the gap.

<Frame>
  <img alt="The image compares a desired temperature of 21°C with an actual temperature of 25°C, indicating that it is &#x22;Too warm.&#x22;" />
</Frame>

At its core, a Kubernetes controller implements an observe-and-fix loop: it constantly watches a resource, compares the actual cluster state to the desired state expressed in YAML, and acts when they don't match.

<Frame>
  <img alt="The image depicts a circular loop labeled &#x22;The Same Loop, in Kubernetes,&#x22; with three stages: &#x22;Observe&#x22; (Read the resource), &#x22;Compare&#x22; (Desired vs actual), and &#x22;Act&#x22; (Fix the gap)." />
</Frame>

Example: the built-in Deployment controller inspects the desired replica count in a Deployment and makes sure that exact number of Pods exist. These built-in controllers are intentionally generic: they need not understand whether your workload is a distributed database or a static website. Their job is to reconcile state (e.g., replica count, pod status, etc.) until actual state matches desired state.

<Frame>
  <img alt="The image illustrates the concept of a built-in deployment controller, showing a process from a desired state of 3 replicas to the creation of 3 actual pods." />
</Frame>

An operator uses the same controller mechanism but adds application-specific domain knowledge. For example, cert-manager understands X.509 certificates: you create a Certificate custom resource, and cert-manager’s controller knows how to request a certificate from a CA, renew it before expiry, and store it in a Secret.

For an application operator, the domain knowledge includes the application’s topology, lifecycle rules, and recovery procedures. A user might declare a custom resource like this:

```yaml theme={null}
kind: WebApp
spec:
  image: nginx
  replicas: 3
```

The operator’s controller translates that WebApp CR into the appropriate Kubernetes resources (Deployment, Service, ConfigMap, etc.) and manages them according to the application’s rules: upgrades, backups, scaling semantics, and failure recovery.

<Frame>
  <img alt="The image explains that an &#x22;Operator&#x22; is the combination of a &#x22;Controller&#x22; and &#x22;Application knowledge,&#x22; using a cert-manager to manage certificates through requesting, renewing, and storing processes." />
</Frame>

Quick rule:

* A controller is the mechanism — the reconcile loop that observes, compares, and acts.
* An operator is a controller that embodies domain or application knowledge, typically exposing that knowledge via a Custom Resource Definition (CRD).

Therefore: every operator is a controller, but not every controller is an operator.

> **lightbulb** Summary: Controllers provide the generic reconcile loop. Operators add domain-specific logic and APIs (CRDs) to manage complex application lifecycle and behavior.

Quick comparison

| Aspect      | Controller                                     | Operator                                          |
| ----------- | ---------------------------------------------- | ------------------------------------------------- |
| Purpose     | Generic reconcile loop to ensure desired state | Reconcile loop + domain-specific automation       |
| API surface | Built-in resources (Deployment, Service, etc.) | Custom resources (via `CustomResourceDefinition`) |
| Knowledge   | Stateless about application internals          | Knows application topology, lifecycle, recovery   |
| Example     | Deployment controller                          | cert-manager, database operator, web-app operator |

References and further reading

* Kubernetes Controllers: [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* Custom Resources & CRDs: [https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* cert-manager: [https://cert-manager.io/](https://cert-manager.io/)

The two main pieces that make an operator are the controller (the reconcile logic) and the custom resource (the API surface provided by a CRD).

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/7d198de7-d651-4c7e-a61d-166023fc1031/lesson/81f29cba-286e-40ac-9791-b77dc615836b)
