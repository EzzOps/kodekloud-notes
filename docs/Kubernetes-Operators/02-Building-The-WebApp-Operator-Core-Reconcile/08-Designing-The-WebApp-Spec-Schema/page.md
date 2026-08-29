# Designing The WebApp Spec Schema

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Designing-The-WebApp-Spec-Schema/page

Designing a minimal WebApp CRD spec with image and replicas and using operator defaults to reconcile Deployment Service and ConfigMap

Before you write controller code, define the shape of the custom resource that users will provide. That shape is the `spec` — think of it as a concise request form that declares the desired state. For this WebApp operator, the first API version keeps the `spec` intentionally small with just two fields.

The first field is `image`. It is a string that tells the Deployment which container image to run.

The second field is `replicas`. It is an `int32` (the conventional small integer type Kubernetes uses for replica counts). `replicas` tells the Deployment how many Pods should exist.

<Frame>
  <img alt="The image explains how to specify the number of pods to keep in Kubernetes using a &#x22;replicas&#x22; field, with a basic request form showing example fields for &#x22;image&#x22; and &#x22;replicas&#x22;. Additionally, it notes that Kubernetes uses the int32 type for replica counts." />
</Frame>

Notice what is deliberately excluded from this first-version `spec`. There is no service type, no custom port, no nested configuration object, and no status field — those are left out so the initial API remains focused and easy to reason about.

<Frame>
  <img alt="The image features a list titled &#x22;Deliberately Left Out – For Now&#x22; with three items: Service type, Custom port, and Nested config object. Each item is accompanied by an icon." />
</Frame>

Even though the `spec` doesn't expose these options yet, the operator will still create a Service and a ConfigMap for the application. The operator uses clear, fixed defaults for those child resources so the reconciliation loop can be validated end to end without extra user configuration.

<Frame>
  <img alt="The image shows a diagram with two labeled components: &#x22;Service&#x22; and &#x22;ConfigMap,&#x22; under the heading &#x22;The Operator Fills In Clear, Fixed Defaults.&#x22;" />
</Frame>

Concretely:

* Service default: `ClusterIP` on port `80`.
* ConfigMap default: a simple static welcome page.

This minimal-first-version approach keeps the user API small while letting you observe the reconcile loop working across Deployment, Service, and ConfigMap. You can add more `spec` fields later (for example `port`), but start small so the first reconciler remains readable and testable.

> **lightbulb** Start with a narrow API surface. Small, opinionated defaults let you validate reconciliation behavior quickly; expand the `spec` only when you need to expose additional user-configurable options.

Example API sketches:

```yaml theme={null}
