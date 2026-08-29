# Section Overview

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Alternative-Approaches-Operator-SDK-Helm-Operator/Section-Overview/page

Comparing Kubebuilder, Operator SDK, and Helm-based approaches for building Kubernetes operators, highlighting tradeoffs, use cases, tooling, and demos

So far this course has focused on building a Go operator with Kubebuilder—an intentional choice because Kubebuilder exposes the controller-runtime patterns used by many production Go operators.

This lesson expands that view to two common alternative approaches: Operator SDK and Helm-based operators. Both are widely used in production, but they solve different problems and fit different team needs.

<Frame>
  <img alt="The image illustrates the relationship between Kubebuilder and Operator SDK, showing shared elements such as API types, reconcilers, manager setup, manifests, and generated code." />
</Frame>

Operator SDK builds on the same controller-runtime building blocks Kubebuilder uses for Go operators: API types, reconcilers, manager setup, manifests, and generated code. The core reconcile loop and API machinery feel familiar to anyone who has used Kubebuilder.

Where Operator SDK differs is in the surrounding tooling and the operator distribution story. It adds first-class workflows for operator bundles, scorecard checks, OLM packaging, and built-in support for non-Go implementations such as Ansible and Helm-based operators. For teams targeting Operator Lifecycle Manager (OLM) or Red Hat ecosystems, these features can significantly reduce integration and packaging effort.

<Callout icon="lightbulb">
  Operator SDK reuses controller-runtime for reconcile loops and API scaffolding while adding tools for bundles, scorecards, and OLM packaging. It also supports non-Go operator types such as Ansible and Helm.
</Callout>

When evaluating Operator SDK, ask whether your project needs the additional packaging and CI workflows it provides. If you plan to publish an OLM bundle or want standardized operator checks and packaging, Operator SDK can save substantial development and release work.

A different path is the Helm-based operator. Rather than writing custom reconcile logic in Go, a Helm-based operator maps a custom resource (CR) to Helm chart values and lets Helm handle the creation and updates of application resources.

<Frame>
  <img alt="The image compares Kubebuilder and Operator SDK, emphasizing their shared core and Go operator usage, and discusses when to use extra SDK tooling for targeting OLM or the Red Hat ecosystem." />
</Frame>

Helm-based operators are especially attractive when:

* The application already has a mature Helm chart.
* The desired lifecycle fits Helm's install/upgrade/uninstall model.
* You want to avoid writing low-level reconciliation code and reuse Helm release semantics.

With a Helm operator the CR essentially becomes a values.yaml generator: the operator converts CR fields into chart values and invokes Helm to apply the release.

<Frame>
  <img alt="The image depicts a flowchart titled &#x22;The Helm-Based Operator Path,&#x22; illustrating a sequence from &#x22;Custom Resource&#x22; to &#x22;Application Resources&#x22; with intermediate steps of &#x22;Helm-based Operator&#x22; and &#x22;Helm Chart.&#x22;" />
</Frame>

The trade-off between Helm-based and Go operators is speed versus control. Helm operators are faster to create because they reuse existing charts and avoid implementing detailed reconciliation. But if your operator must handle complex runtime behaviors—cross-resource coordination, advanced status aggregation, fine-grained custom status logic, or sophisticated reconciliation strategies—a Go operator provides the necessary control and flexibility.

<Frame>
  <img alt="The image compares Helm-based and Go operators, highlighting that Helm-based operators are faster to create, while Go operators offer more control for complex needs such as complex behaviors and cross-resource decisions. A scale illustrates the tradeoff in control." />
</Frame>

This module includes two demos to make the differences concrete:

* A Go operator scaffolded with Operator SDK, compared side-by-side with a Kubebuilder scaffold to highlight layout, generated artifacts, and packaging differences.
* A Helm-based operator scaffold showing how a CR maps to chart values and how Helm manages the resulting resources.

<Frame>
  <img alt="The image illustrates two demos: one for implementing a Go operator with the Operator SDK, comparing it with Kubebuilder, and another for using a Helm-based operator with custom resources and chart values to manage app resources." />
</Frame>

After finishing this lesson you will be able to:

* Explain the architectural overlap between Kubebuilder and Operator SDK.
* Describe when Operator SDK’s bundling and OLM-focused tooling make it the better choice.
* Evaluate whether a Helm-based operator is suitable when you already have a Helm chart.
* Decide which approach—Kubebuilder, Operator SDK, or Helm—best matches your project constraints.

Comparison summary

| Approach            | Best for                                                                   | Notes                                                                                                               |
| ------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Kubebuilder (Go)    | Operators that require deep control and custom reconciliation              | Full control over reconcilers, status handling, and complex multi-resource workflows.                               |
| Operator SDK        | Teams that want controller-runtime benefits plus packaging and OLM tooling | Reuses controller-runtime; adds bundle generation, scorecards, and multi-language support (Ansible, Helm).          |
| Helm-based operator | Rapid operator development when a Helm chart already exists                | Maps CRs to chart values and relies on Helm for lifecycle; faster to implement but less flexible for complex logic. |

When to choose which approach

* Choose Kubebuilder (Go) if you need fine-grained reconciliation logic, complex cross-resource interactions, or precise status management.
* Choose Operator SDK if you want Kubebuilder-style Go operator code plus integrated packaging, scorecards, and OLM-ready bundles.
* Choose a Helm-based operator if you have a stable Helm chart and need fast delivery without custom reconcile code.

Further reading and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Operator SDK](https://sdk.operatorframework.io/)
* [OLM (Operator Lifecycle Manager)](https://olm.operatorframework.io/)
* [Helm](https://helm.sh/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/d2537d70-4008-4d53-ad04-b7731ca0f7c0/lesson/6aac2156-a088-4a51-9f56-b9f3f85bf7c6" />
</CardGroup>
