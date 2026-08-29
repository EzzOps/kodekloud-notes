# What Is A Kubernetes Operator

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Introduction-to-Operator-Fundamentals/What-Is-A-Kubernetes-Operator/page

Explains Kubernetes operators that automate application lifecycle by using custom resources and controllers to create and maintain Deployments, Services, and ConfigMaps.

Imagine this situation:

You want to give your team a simple way to run an application on Kubernetes — not a folder full of YAML that everyone must parse, edit, and babysit. Instead, a developer should be able to hand a tiny request:

```yaml theme={null}
image: my-app
copies: 3
```

At first glance, that might look like a job for a [Helm chart](https://helm.sh/) or a [kustomize overlay](https://kustomize.io/). Both are excellent for generating and templating Kubernetes manifests. But an operator solves a different, deeper problem: maintaining the application over time, not just creating it once.

<Frame>
  <img alt="The image illustrates a process flow between &#x22;Day 1 - Create&#x22; using Helm/Kustomize to create manifests, and &#x22;Day 2+ - Keep running,&#x22; with a question mark indicating uncertainty in maintaining the system's health over time." />
</Frame>

The important question is not only: can we create the initial objects? The bigger one is: who looks after the application after it is running?

To make this concrete, in this lesson you'll build a small tool called the WebApp Operator. Its custom resource is intentionally minimal: the user supplies only an image and a replica count. The moment a developer applies that single, simple object, the operator’s controller goes to work. It automatically generates, wires up, and manages the entire stack for them — a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) to run the containers, a [Service](https://kubernetes.io/docs/concepts/services-networking/service/) to route traffic, and a [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) for configuration. The operator keeps these resources in sync over time.

<Frame>
  <img alt="The image illustrates a Kubernetes architecture stack, showing a &#x22;WebApp&#x22; with interconnected components: Deployment, Service, and ConfigMap, all kept synchronized." />
</Frame>

If an exhausted engineer accidentally deletes the underlying [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) at two a.m., the operator will detect the difference during its next reconciliation loop and recreate what’s missing. That is the operational value an operator provides.

Think of how an operator works like ordering at a restaurant. The customer places an order; they don't run the oven, assign the cook, or plate the food. The manager knows the recipe and the steps needed to fulfill the order and watches for problems — a missing ingredient, a stalled table, a food-safety issue — and fixes them so the customer gets the expected result. The operator plays the manager’s role for applications on Kubernetes.

<Frame>
  <img alt="The image illustrates a process flow resembling ordering at a restaurant, with arrows connecting a customer to a manager and related tasks like oven, cook, plating, and tables." />
</Frame>

In this lesson, the WebApp object is the order. The operator is the part that knows how to turn that order

<Frame>
  <img alt="The image illustrates a Kubernetes concept comparing the &#x22;order&#x22; to a &#x22;WebApp object&#x22; and the &#x22;manager&#x22; to &#x22;the operator,&#x22; suggesting an analogy in roles or functions." />
</Frame>

into running Kubernetes behavior and how to keep it there.

What should you expect to learn?

* The mental model: why an operator is more than a one-time manifest generator.
* How Kubernetes learns about new application-shaped objects (Custom Resources).
* How controller code watches those objects and reconciles the cluster to match the desired state.
* How the operator creates and maintains the resources your app needs, and how it reports status back to users.

<Frame>
  <img alt="The image contrasts two mental models: &#x22;Static manifests,&#x22; which apply once and do nothing afterward, and &#x22;An operator,&#x22; which continuously watches and converges." />
</Frame>

An operator becomes useful when the application involves rules, decisions, repairs, or lifecycle steps that people would otherwise do by hand. Instead of keeping that operational knowledge in a runbook, you encode it in software that watches the cluster and acts automatically.

You may already have used this pattern without calling it an operator. For example, [cert-manager](https://cert-manager.io/) lets you request a certificate and then automatically handles renewal: you declare a Certificate, cert-manager watches it, and it renews and updates the cluster so your certs remain valid.

<Frame>
  <img alt="The image illustrates a process flow involving a certificate management system, where a &#x22;cert-manager&#x22; automatically watches and renews certificates to ensure they remain valid. It includes labels such as &#x22;Certificate,&#x22; &#x22;cert-manager,&#x22; &#x22;Watches and renews,&#x22; and &#x22;Valid cert, always.&#x22;" />
</Frame>

A template (Helm or kustomize) helps you create objects once; an operator continuously watches application-shaped objects and drives the cluster toward the state those objects declare.

Quick comparison

| Tool                         | Primary Purpose                                                    | When to use                                                                         |
| ---------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Helm / Kustomize             | Generate and template Kubernetes manifests                         | Use when you need repeatable manifest generation, deployment packaging, or overlays |
| Operators (controller + CRD) | Continuously reconcile cluster state to match higher-level intents | Use when the app needs automated lifecycle, repairs, or domain-specific logic       |
| Kubernetes native resources  | Standard primitives like Deployment, Service, ConfigMap            | Use to run and expose workloads; often managed by Helm or an operator               |

> **lightbulb** Prerequisites: Familiarity with `kubectl`, basic YAML, and the concept of Pods and Deployments in Kubernetes is sufficient. You don’t need a Kubernetes certification or to be a Go expert — basic programming comfort with functions and structs is enough. When a Go or Kubernetes detail matters, this lesson will explain it.

> **warning** Operators are not a replacement for good architecture or security practices. Design your CRD behaviors carefully and consider RBAC, validation, and testing before deploying operators to production.

Next in this series, you will build the WebApp operator step-by-step: defining the Custom Resource, writing the controller’s reconcile logic, and wiring it to create the Deployment, Service, and ConfigMap. By the end you’ll understand the pattern and have a small, practical example you can adapt.

That was all for this lesson. We'll also clarify two words people often mix.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/7d198de7-d651-4c7e-a61d-166023fc1031/lesson/714f02ee-a0d6-4672-9d95-d4b5cb2a2234)
