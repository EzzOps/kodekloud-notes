# empty. now what?
```

```bash theme={null}
$ kubebuilder version                           # verify CLI is installed
$ go version                                    # verify Go toolchain
$ kubebuilder init --domain kodekloud.com --repo github.com/kodekloud/webapp-operator
$ kubebuilder create api --group apps --version v1 --kind WebApp
```

> **lightbulb** Ensure [`go`](https://go.dev) and [`kubebuilder`](https://book.kubebuilder.io) are in your PATH. The `--domain` you pass to `kubebuilder init` becomes the DNS domain for your CRD API group (for example: `apps.kodekloud.com/v1`).

After generation, inspect the code layout. Key files you will interact with:

* `api/v1/webapp_types.go` — the Go structs that define the WebApp spec and status.
* `controllers/webapp_controller.go` — the Reconciler that runs when WebApp resources change.
* `main.go` — wires the manager, controllers, and sets up leader election, metrics, etc.
* `Makefile` — contains common targets: `make` build, `make run`, `make docker-build`, `make install` (CRDs), `make deploy`.

The reconciler implements the Reconcile method: read desired state (the resource), compare with actual cluster state, and make changes to converge. The generated skeleton leaves an empty `Reconcile` where you add the operator logic.

<Frame>
  <img alt="The image is a diagram illustrating a tour of generated code, showing two sections: one for Go structs in api/v1/webapp_types.go and one for the reconciler in internal/controller/, with a flow from &#x22;What you want&#x22; to &#x22;What you have.&#x22;" />
</Frame>

controller-gen and markers

Kubebuilder uses controller-tools (`controller-gen`) to generate CRD manifests and RBAC rules from annotated comments (markers) in your Go types and controller code. Markers are straightforward and drive automation.

Example RBAC marker:

```go theme={null}
// +kubebuilder:rbac:groups=apps.kodekloud.com,resources=webapps,verbs=get;list;watch;create;update;patch;delete
```

These markers will be turned into RBAC YAML in `config/rbac/` and CRD YAML in `config/crd/bases/` after you run the generator targets (for example: `make generate` and `make manifests`, depending on your Makefile).

> **warning** Always verify generated RBAC rules and CRD group/version names before applying to a cluster. Incorrect RBAC or API group names can prevent your controller from watching or acting on resources.

Multiple APIs in one repo

A single Kubebuilder project can hold multiple API groups, versions, and kinds. Use `kubebuilder create api` repeatedly to add new groups/versions/kinds; the scaffold keeps APIs and controllers organized under `api/` and `controllers/`, and `PROJECT` records your layout.

Wrap-up

After completing this section you will have:

* A compiling operator project.
* Generated CRD YAML to install into a cluster.
* An empty `Reconcile` method ready for your business logic.
* An understanding of how markers drive CRD and RBAC generation and where to add additional APIs.

Links and references

* [Kubebuilder Book](https://book.kubebuilder.io)
* [controller-runtime on GitHub](https://github.com/kubernetes-sigs/controller-runtime)
* [Operator SDK](https://sdk.operatorframework.io)
* [controller-tools / controller-gen](https://github.com/kubernetes-sigs/controller-tools)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/20a4ec01-fde8-466d-83c7-2f74f6def1f0/lesson/ce641d8c-df2f-40d4-87a2-0e29b2f51c42)


# A Brief Look At OLM

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Packaging-And-Distribution/A-Brief-Look-At-OLM/page

Overview of Operator Lifecycle Manager explaining operator packaging, catalogs, bundles, CSVs, subscriptions, install plans, and when to use OLM versus raw manifests.

You may already know the direct deployment path for an operator: build the controller image, push it to a registry, and apply the manifests that install the operator. The Operator Lifecycle Manager (OLM) provides an alternative, catalog-driven distribution model. OLM packages an operator into a bundle that a cluster can discover, install, and upgrade from a catalog — similar to how a package manager distributes software.

<Frame>
  <img alt="This image illustrates two methods for deploying an operator: a &#x22;Direct path&#x22; involving build, push, and apply steps, and an &#x22;OLM&#x22; method involving discovery and installation." />
</Frame>

Think of raw manifests as handing someone a box of parts plus assembly instructions. OLM acts more like a package manager for operators: the operator package (bundle) still contains CRDs, RBAC, Deployments, and other runtime resources, but it also includes metadata that describes versions, channels, permissions, and upgrade behavior.

<Frame>
  <img alt="The image illustrates a package manager for operators, showing a flow where raw manifests containing CRD, RBAC, and Deployment data are enhanced with metadata before being processed by OLM." />
</Frame>

Important: OLM is about distribution and lifecycle management — not a change to your operator's runtime or reconciliation logic. The controller image you build still runs the operator; OLM defines how that operator is presented, installed, and upgraded on a cluster.

> **lightbulb** OLM provides discovery, install-time metadata, upgrade channels, and a managed approval workflow — it does not change how your reconcile loop works.

Vocabulary (simple sequence)

* Bundle\
  A bundle is the package for one version of the operator. It contains the files OLM needs: CRDs, metadata, and a `ClusterServiceVersion` (`CSV`). A bundle represents a single packaged version of your operator.

<Frame>
  <img alt="The image is an illustration labeled &#x22;Bundle: One Packaged Version,&#x22; showing a green box with &#x22;BUNDLE&#x22; written on it, accompanied by a list that includes &#x22;CRDs,&#x22; &#x22;Metadata,&#x22; and &#x22;CSV.&#x22;" />
</Frame>

* Controller image\
  The controller image is the container image with your operator code. The bundle references this image and includes the metadata that tells OLM how to deploy it.

* ClusterServiceVersion (`CSV`)\
  The `CSV` is the versioned manifest inside the bundle. It describes the APIs the operator owns, the install strategy (for example, the deployment spec), required RBAC permissions, and UI-facing metadata such as description and version.

<Frame>
  <img alt="The image describes &#x22;CSV: The Versioned Label&#x22; with a focus on ClusterServiceVersion elements like Owned APIs, Install strategy, and Permissions, alongside an illustration of an open box labeled &#x22;BUNDLE.&#x22;" />
</Frame>

If the bundle is a box, the `CSV` is the version label that tells OLM and users what’s inside.

* Catalog and `CatalogSource`\
  A `CatalogSource` tells OLM where to look for operator packages (for example, a public registry, vendor catalog, or private catalog). Clusters can use multiple catalogs; catalogs are how OLM discovers available operators and their versions.

* `Subscription`\
  A `Subscription` is a user or platform request to install a package and follow a given channel over time. It names the package, the channel (for example, `stable` or `beta`), the catalog source, and the approval behavior (`Automatic` or `Manual`). OLM watches `Subscription` objects and decides which version should be installed now and which upgrades to consider later.

<Frame>
  <img alt="The image outlines an &#x22;Install Request&#x22; process involving a subscription, detailing package, channel, source, and approval settings, with OLM (Operator Lifecycle Manager) monitoring it. Context tabs are shown above, highlighting stages like Bundle, CSV, and Subscription." />
</Frame>

* `InstallPlan`\
  An `InstallPlan` is the concrete list of steps OLM generates from a `Subscription`. It enumerates the resources OLM intends to install or upgrade (bundles, CSVs, CRDs, and other manifests). Based on the `Subscription` approval mode, OLM may apply the `InstallPlan` automatically or wait for human approval. This gating lets platform teams control when upgrades are applied.

> **warning** If a `Subscription` uses manual approval, OLM will pause at the `InstallPlan` stage until an operator or platform engineer approves the plan. This prevents unintended upgrades in production clusters.

* `OperatorGroup`\
  An `OperatorGroup` defines the scope of the operator — which namespaces it should target. Operators can be namespace-scoped (watch a single namespace) or cluster-scoped (watch the entire cluster). `OperatorGroup` tells OLM the intended installation scope.

Quick comparison: When to use OLM

* Choose raw manifests, `Kustomize`, or `Helm` when:
  * You want a simple, transparent install for a small internal operator.
  * You prefer straightforward YAML that you apply directly.
* Choose OLM when you need:
  * Catalog-driven discovery and distribution.
  * Channel-based upgrades and version metadata.
  * Dependency resolution and a managed approval workflow.
  * A consistent operator marketplace experience (common on platforms like OpenShift).

<Frame>
  <img alt="The image is a comparison of when OLM fits versus when it doesn't, listing benefits like catalog-driven install and channel-based upgrades. It suggests raw manifests for small internal scenarios." />
</Frame>

Summary table of OLM components

|   Resource Type | Purpose                                 | Key fields / notes                                                     |
| --------------: | --------------------------------------- | ---------------------------------------------------------------------- |
|          Bundle | One packaged version of an operator     | Contains CRDs, `CSV`, metadata                                         |
|           `CSV` | Versioned descriptor for the bundle     | `spec.installStrategy`, owned APIs, permissions                        |
| `CatalogSource` | Where OLM discovers packages            | Points to a registry or index image                                    |
|  `Subscription` | Request to install and follow a channel | `spec.name`, `spec.channel`, `spec.source`, `spec.installPlanApproval` |
|   `InstallPlan` | Concrete steps OLM will apply           | Lists manifests and their order; may require approval                  |
| `OperatorGroup` | Defines operator install scope          | Namespace-scoped or cluster-scoped behavior                            |

Further reading and references

* Operator Lifecycle Manager (OLM) docs: [https://olm.operatorframework.io/docs/](https://olm.operatorframework.io/docs/)
* OpenShift Operators and OperatorHub: [https://docs.openshift.com/](https://docs.openshift.com/)
* When to use Helm, Kustomize, or raw manifests: compare in your platform-specific docs

Takeaway: Not every operator needs OLM. Think of distribution as levels: raw manifests are direct and transparent; OLM adds package metadata, catalogs, channels, `InstallPlan`s, and a gated workflow. When you hear "bundle", `CSV`, `CatalogSource`, `Subscription`, `InstallPlan`, and `OperatorGroup`, treat them as the parts of a package manager story for Kubernetes operators.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/5a9bfe56-bc26-4325-b659-06027d4e815f/lesson/81dde39b-6011-46ad-8cf3-5be074ba996e)
