# watches.yaml
- group: example.com
  version: v1alpha1
  kind: MyApp
  chart: helm-charts/myapp
```

In plain language: when the controller sees objects of kind `MyApp` in group `example.com`, manage the `helm-charts/myapp` chart for them.

Under the hood, the operator is still a controller: it runs a manager, watches Kubernetes events, and reconciles desired state against actual state. The difference is where reconciliation logic comes from. A Go-based operator runs custom code you author; a Helm-based operator uses a generic Helm reconciler that converts CR values into a Helm release. That trade-off drives the decision to choose one approach over the other.

A Helm-based operator is a good fit when the workload primarily concerns install/upgrade/delete of Kubernetes objects already expressed by the chart—typical examples include web applications, internal services, and other packaged workloads where the chart is the source of truth.

| When to Choose a Helm-Based Operator                                          | When to Choose a Go-Based Operator                        |
| ----------------------------------------------------------------------------- | --------------------------------------------------------- |
| Chart already captures deployment semantics (image, replicas, service, ports) | Need to call external APIs or run complex workflows       |
| Want a Kubernetes-native CRD API for operators and teams                      | Need to compute complex, application-specific status      |
| Prefer minimal custom controller code — reuse chart templating                | Require multi-step reconciliation, migrations, or backups |
| Quick on-ramp to operator framework using Operator SDK Helm plugin            | Full control over lifecycle and custom business logic     |

<Frame>
  <img alt="The image is a flowchart illustrating the use of Helm for managing Kubernetes objects to install, upgrade, or delete web applications and internal services." />
</Frame>

However, a Helm-based operator is not a good fit when the controller must implement application-specific judgment. For example, if you must call external APIs, coordinate backups, wait for database migrations, compute detailed status from live application behavior, or run multi-step recovery workflows, the generic Helm reconciler lacks the necessary flexibility.

<Frame>
  <img alt="The image lists scenarios where something is &#x22;Not a Good Fit&#x22; and needs custom logic, such as calling an external API, coordinating a backup, waiting for a database migration, computing detailed status from live application behavior, and running a multi-step recovery workflow." />
</Frame>

In those cases, prefer a Go-based operator so you have a place to write application-specific reconciliation logic. Treat a Helm-based operator as an on-ramp—not a universal shortcut. It brings an existing chart into the operator ecosystem and exposes install/upgrade/delete via Kubernetes resources, but it does not replace custom controller development when your lifecycle requires real application reasoning.

> **lightbulb** Use a Helm-based operator when your chart already encodes most deployment semantics and you want a Kubernetes-native API. Choose a Go-based operator when you need custom lifecycle logic or deep runtime reasoning.

Operator SDK scaffolds a Helm-based operator with this layout on disk: a Helm chart, a `watches.yaml` mapping a CRD type to that chart, and a control loop that delegates reconciliation to the Helm reconciler. This pattern makes it fast to expose existing Helm charts through Kubernetes APIs while keeping the chart as the source of manifest truth.

Links and references

* Operator SDK Helm plugin: [https://sdk.operatorframework.io/docs/helm/](https://sdk.operatorframework.io/docs/helm/)
* Helm: [https://helm.sh/](https://helm.sh/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Learn Go (background/readiness): [https://learn.kodekloud.com/user/courses/golang](https://learn.kodekloud.com/user/courses/golang)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/d2537d70-4008-4d53-ad04-b7731ca0f7c0/lesson/27b94e89-16d3-4deb-92c2-a7cd320349b4)


# Operator SDK Its Relationship To Kubebuilder

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Alternative-Approaches-Operator-SDK-Helm-Operator/Operator-SDK-Its-Relationship-To-Kubebuilder/page

Compares KubeBuilder and Operator SDK, explains shared controller-runtime foundation, and advises when to choose SDK for packaging, OLM integration, and Helm or Ansible operator styles.

Operator SDK can look like a new route — but for a Go operator it is mostly the same engine with a larger toolkit around it. The names change — you’ll hear SDK, bundles, scorecard, OperatorHub, OpenShift, and OLM — but the reconcile idea underneath does not start over.

<Frame>
  <img alt="The image depicts a metaphor of a Go Operator car on an &#x22;Operator SDK&#x22; road, with a speech bubble saying &#x22;New road, same engine,&#x22; alongside a larger travel kit containing items like Bundles, Scorecard, and OpenShift." />
</Frame>

Summary: think of KubeBuilder as a tidy workshop for building a Go controller, while Operator SDK is that same workshop with extra shelves for packaging, catalog testing, and alternative operator styles. If you already know managers, reconcilers, the client, and generated CRDs, you’re not entering a different universe — both tools sit on top of controller-runtime.

<Frame>
  <img alt="The image illustrates a comparison between Kubebuilder and Operator SDK, highlighting the additional features of Operator SDK like packaging, catalog testing, and alternative operator styles. Both use the same foundational elements like Manager, Reconciler, Client, and CRDs." />
</Frame>

## The shared control-loop foundation

controller-runtime is the library that provides the patterns demonstrated here. The common control-loop pieces are:

* Manager: starts controller processes and coordinates lifecycles.
* Reconciler: receives reconciliation requests and implements desired-state logic.
* Client: reads and writes Kubernetes objects.
* Watches: notify the manager about object changes and enqueue reconcile requests.

A project scaffolded by Operator SDK still uses that same control-loop shape; for a Go operator the layout and concepts should feel familiar.

<Frame>
  <img alt="The image outlines the relationship between Kubebuilder and Operator SDK, both of which rely on the controller-runtime. It illustrates the components of the control loop process: Manager, Reconciler, Client, and Watches." />
</Frame>

Typical repository layout for a Go operator (scaffolded by either tool) looks like:

```text theme={null}
my-operator/
├── api/
│   └── v1alpha1/
│       └── zz_generated.deepcopy.go
├── config/
│   ├── crd/bases/*.yaml
│   └── manifests/*.yaml
├── internal/
│   └── controller/
│       ├── mycontroller_controller.go
│       ├── mycontroller_controller_test.go
│       └── suite_test.go
├── cmd/
│   └── main.go
├── Makefile
├── Dockerfile
├── PROJECT
└── go.mod
```

## So which tool should you choose?

The right question is not "which tool is the real operator tool?" — it’s: what job around the operator do I need help with?

KubeBuilder is strong when the main job is designing a Go API and writing reconcile logic. Operator SDK becomes attractive when you also need the surrounding lifecycle: packaging, validation, distribution, or support for non-Go operator styles.

<Frame>
  <img alt="The image contains a guide on asking useful questions about using &#x22;Kubebuilder&#x22; for operator tasks, with emphasis on job-related queries. It features a design and reconcile icon along with a question mark over a user icon." />
</Frame>

### Quick comparison

| Focus area                | KubeBuilder                                    | Operator SDK                                                    |
| ------------------------- | ---------------------------------------------- | --------------------------------------------------------------- |
| Go controller scaffolding | Excellent — compact, focused                   | Also supports Go, but adds packaging workflows                  |
| Packaging & distribution  | Minimal — you provide manifests/Kustomize/Helm | Built-in bundle creation, validation, scorecards, OLM workflows |
| Target environments       | Any Kubernetes cluster                         | Especially helpful for OpenShift, OperatorHub / OLM             |
| Non-Go operators          | Not applicable                                 | Scaffolds for Helm and Ansible operators                        |
| Ecosystem tooling         | controller-runtime compatible                  | Operator Framework tooling (scorecard, bundle, etc.)            |

## Operator SDK and OLM / bundles

A bundle is the OLM-facing package for one version of an operator: it includes CRDs, metadata, and a ClusterServiceVersion. Operator SDK provides commands and workflows to:

* scaffold a bundle structure,
* assemble CRDs and manifest fragments,
* run validations and the Operator SDK scorecard,
* test operator installation using OLM.

<Frame>
  <img alt="The image illustrates the OLM Packaging process involving a bundle created using the Operator SDK, validated, and checked with a scorecard. It shows components of the bundle including CRDs, metadata, and cluster service version." />
</Frame>

## Operator SDK supports multiple operator styles

Operator SDK reaches beyond Go: it includes scaffolds and runtime support for Helm-based and Ansible-based operators. Those approaches trade custom Go reconcile code for a higher-level automation style. They’re not universally better — they’re simply different trade-offs that can speed development for certain use cases.

<Frame>
  <img alt="The image illustrates three operator styles for Kubernetes—Go for custom reconcile code, Ansible for automating with playbooks, and Helm for package management—linked by the Operator SDK framework. A note emphasizes &#x22;Different models. Same operator framework.&#x22;" />
</Frame>

## Practical guidance

* Choose KubeBuilder if you want the clearest path to build a Go controller and you will ship raw manifests, Kustomize, Helm, or your own pipeline.
* Choose Operator SDK if you need out-of-the-box packaging for OLM, want to publish to OperatorHub, plan to target OpenShift, require scorecard validation, or prefer Helm/Ansible scaffolds over Go code.

<Frame>
  <img alt="The image compares Kubebuilder and Operator SDK, highlighting their goals, features, and suitable use cases in a table format." />
</Frame>

> **lightbulb** Both tools share the same underlying operator model. Choose KubeBuilder for focused Go controller development; choose Operator SDK when you want out-of-the-box packaging, OLM integration, or non-Go operator styles.

The key reassurance: you are not throwing away what you learned. Operator SDK does not replace the operator mental model — it wraps the familiar Go operator workflow in a broader distribution and ecosystem toolkit.

A demo that scaffolds a web-app operator with Operator SDK and compares it to a KubeBuilder project usually highlights that the underlying control-loop patterns remain the same, not that the tooling is foreign.

<Frame>
  <img alt="The image explains a process reassuring that previous knowledge still applies with a familiar Go operator workflow, enhanced by the Operator SDK in a broader toolkit." />
</Frame>

## Links and references

* controller-runtime: [https://github.com/kubernetes-sigs/controller-runtime](https://github.com/kubernetes-sigs/controller-runtime)
* Kubebuilder: [https://book.kubebuilder.io/](https://book.kubebuilder.io/)
* Operator SDK: [https://sdk.operatorframework.io/](https://sdk.operatorframework.io/)
* OLM (Operator Lifecycle Manager): [https://github.com/operator-framework/operator-lifecycle-manager](https://github.com/operator-framework/operator-lifecycle-manager)
* OperatorHub: [https://operatorhub.io/](https://operatorhub.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/d2537d70-4008-4d53-ad04-b7731ca0f7c0/lesson/e01eada6-71d5-44ae-89cd-f34dc525b7b5)
