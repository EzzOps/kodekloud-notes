# example of an imperative client action
kubectl apply -f ./manifest.yaml
```

When multiple people make ad-hoc changes—especially during high-pressure incidents—conflicting modifications can be introduced simultaneously. With no single source of truth and no formal change history, teams cannot track who changed what, when, or why.

<Frame>
  <img alt="The image illustrates a flowchart titled &#x22;Deployment Roulette,&#x22; showing three uncoordinated teams (Dev, Ops, SRE) sending conflicting changes to a production cluster." />
</Frame>

Consequences: configuration drift, unpredictable behavior, and prolonged outages

Uncoordinated changes create configuration drift between environments, unpredictable production behavior, and outages caused by incompatible or unintended changes. This makes root cause analysis difficult and puts production stability in the hands of human coordination and memory rather than an auditable system.

<Frame>
  <img alt="The image outlines the concept of &#x22;Deployment Roulette,&#x22; highlighting three issues: configuration drift between environments, unpredictable production behavior, and prolonged outages from incompatible or unintended changes." />
</Frame>

Imperative vs. Declarative

Root cause: the imperative model. Running imperative commands (scale, set image, etc.) immediately changes cluster state and leaves only ephemeral terminal history.

Imperative examples:

```bash theme={null}
# Imperative examples (state-changing commands run ad-hoc)
kubectl scale deployment api --replicas=5
kubectl set image deployment/web web=nginx:1.21
```

There is no integrated version history, no central audit trail, and no automatic detection when the same resource changes later.

By contrast, the declarative model records desired state in files (YAML/JSON) committed to Git. Git automatically provides a versioned history so you can see who changed what, when, and why (when commit messages are used).

Example (declarative snippet):

```yaml theme={null}
spec:
  replicas: 5
  template:
    spec:
      containers:
        - name: nginx
          image: nginx:1.21
```

The key insight: GitOps replaces imperative “do this now” commands with declarative desired state and automation that converges actual cluster state to that declared state.

<Frame>
  <img alt="The image compares imperative commands (before) with declarative commands (after), highlighting a shift from step-by-step instructions to automation and desired state declaration." />
</Frame>

What is GitOps?

GitOps is an operational model where Git repositories store declarative descriptions of infrastructure and applications. Automated controllers running in the cluster ensure the cluster state matches those Git-declared states.

<Frame>
  <img alt="The image illustrates Git as the single source of truth in a GitOps operational model, connecting Git repositories to declarative descriptions in YAML/JSON format." />
</Frame>

The four pillars of GitOps

| Pillar      | What it means                                  | Why it matters                                                                |
| ----------- | ---------------------------------------------- | ----------------------------------------------------------------------------- |
| Declarative | Desired state defined as files (`YAML`/`JSON`) | Describes the intended system rather than individual commands                 |
| Versioned   | All manifests stored in Git                    | Complete commit history, easy rollbacks and audits                            |
| Pull-based  | Agents inside the cluster pull from Git        | No CI with persistent cluster creds; reduces secret sprawl and attack surface |
| Reconciled  | Controllers continuously converge state        | Detects and corrects drift; enables self-healing                              |

<Frame>
  <img alt="The image illustrates four features of Git as a single source of truth: Declarative, Versioned, Pulled, and Reconciled, with brief descriptions of each." />
</Frame>

If it’s not in Git, it does not exist. If it's in Git, it should be in the cluster.

How the reconciliation loop works

The reconciliation loop is the engine of GitOps. Controllers such as Argo CD and Flux operate continuously in three core phases:

* Watch: The controller detects Git changes via polling, webhooks, or provider notifications.
* Compare: It compares the declared desired state in Git against the actual cluster state resource-by-resource.
* Sync: When differences are found, the controller applies the necessary changes (create/update/delete) to align the cluster with Git.

This loop integrates with developer workflows: Code & Push → Detect & Compare → Sync & Deploy → Continuous Watch.

<Frame>
  <img alt="The image depicts &#x22;The Reconciliation Loop,&#x22; a cyclical process involving four steps: Code & Push, Detect & Compare, Sync & Deploy, and Continuous Watch, each with brief descriptions." />
</Frame>

Example: you change a Deployment's image from `1.0` to `2.0` and push the commit. Within the controller's detection window (seconds to minutes), it sees the Git commit, compares the cluster's running `1.0` deployment, and applies the update to `2.0`. The loop is continuous; it’s not a one-time deployment.

Drift detection and self-healing

Drift occurs when the cluster diverges from Git-declared desired state. Controllers handle drift in several ways depending on policy and environment sensitivity.

| Response                 | Behavior                                                                             | Use case                                                       |
| ------------------------ | ------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| Auto-sync (self-healing) | Controller automatically reverts unintended changes to match Git                     | Standard GitOps for most environments                          |
| Alert + manual sync      | Controller alerts team and waits for approval to apply changes                       | Production systems requiring human checks                      |
| Diff + PR workflow       | Controller generates a diff or PR to update Git when cluster changes are intentional | When cluster-initiated changes must be reflected back into Git |

<Frame>
  <img alt="The image outlines a drift detection and self-healing process using GitHub, featuring auto-sync for self-healing and alert and manual sync for human approval." />
</Frame>

Common sources of drift

* Manual `kubectl` edits and ad-hoc changes.
* Autoscalers (HPA/VPA) adjusting replicas or resource requests/limits.
* Other controllers or operators adding annotations/labels or modifying resources.

Principle to follow: Git is authoritative. Either the controller syncs the cluster to Git, or you update Git to reflect an intentional change in the cluster. The cluster is not the source of truth.

<Callout icon="lightbulb">
  Using a pull-based model (agents inside the cluster pulling from Git) reduces secret sprawl. CI/CD systems do not need persistent cluster credentials to apply changes, improving security and auditability.
</Callout>

Recap — core takeaways

* Git is the single source of truth: desired state belongs in version-controlled repositories.
* Prefer declarative manifests over imperative commands: state is described, automation handles convergence.
* Continuous reconciliation prevents unintentional drift: controllers compare and correct constantly.
* Pull-based deployments are more secure and auditable because the cluster pulls from Git and CI/CD systems avoid persistent credentials.

Further reading and references

* Argo CD: [https://argo-cd.readthedocs.io](https://argo-cd.readthedocs.io)
* Flux: [https://fluxcd.io/](https://fluxcd.io/)
* GitOps principles and best practices: [https://www.gitops.tech/](https://www.gitops.tech/)

This concludes the lesson on GitOps, desired state, drift, and reconciliation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/dff5382b-dbe7-4cac-bd2b-d5a47028945e/lesson/c28403c7-4078-4ed2-a273-ec35b204e887" />
</CardGroup>


# GitOps Tool Landscape ArgoCD vs Flux

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/GitOps-and-Continuous-Delivery/GitOps-Tool-Landscape-ArgoCD-vs-Flux/page

Comparing Argo CD and Flux GitOps engines, their architectures, features, tradeoffs, and guidance for choosing based on team preferences, multi cluster strategy, and ecosystem integrations.

You've adopted GitOps: your repository is organized, configurations are parameterized, and now you need an engine — a controller that watches Git and keeps clusters in sync.

Two CNCF-graduated projects dominate this space: [Argo CD](https://argo-cd.readthedocs.io/en/stable/) and [Flux](https://fluxcd.io/). Both are production-ready and implement GitOps principles correctly, but they follow different philosophies and operational models. Choosing the right GitOps engine for your team reduces long-term friction, improves reliability, and aligns with your multi-cluster strategy.

<Frame>
  <img alt="The image lists learning objectives related to GitOps and compares ArgoCD and Flux, highlighting their architectures, features, and models." />
</Frame>

Real-world example

A financial services company initially adopted Flux. The deployment team — primarily junior engineers — found Flux’s CLI-first workflow difficult to use when troubleshooting cluster drift or visualizing resource trees. Their typical command looked like:

```bash theme={null}
$ flux get kustomizations
NAME   REVISION           SUSPENDED   READY   MESSAGE
apps   main@sha256:...    False       Unknown Reconciliation in progress...
```

After six months they migrated to Argo CD to gain a centralized web UI and clearer visibility into application state. The migration required about three months of effort: each Flux Kustomization was converted to an Argo CD Application, webhooks were rewired, and runbooks were updated. This move underscores an important point: Flux wasn’t “wrong” for them — it simply didn’t match their operational needs.

Why the choice matters

When selecting a GitOps engine, evaluate these critical factors:

* Lock-in risk: Migrating between GitOps tools is non-trivial. Resource CRD models, webhooks, RBAC, and integrations typically need changes.
* Team adoption: If your team relies on a visual dashboard for troubleshooting and onboarding, a CLI-only approach introduces friction. Conversely, teams that prefer Git- and CLI-driven workflows may find a UI-heavy tool unnecessary.
* Ecosystem fit: How well the tool integrates with your CI, secret management, policy engines (OPA/Gatekeeper), and observability stack matters for operational efficiency.
* Multi-cluster strategy: The number of clusters, their topology (hub-and-spoke vs independent clusters), and tenancy model will influence the best-fit tool.

<Frame>
  <img alt="The image is about selecting a GitOps tool and highlights factors such as lock-in risk, team adoption, ecosystem fit, and multi-cluster strategies. It emphasizes why the choice of tool matters." />
</Frame>

High-level philosophies

* Argo CD — application-centric: The Application resource is the primary abstraction. It emphasizes a centralized control plane and a rich web UI (hub-and-spoke model).
* Flux — Git-centric: The GitRepository / HelmRepository Source resources are central. Flux is composed of small controllers that typically run in each cluster (decentralized model).

Neither architecture is universally superior; match the tool to your operational model and team preferences.

<Frame>
  <img alt="The image compares ArgoCD and Flux, highlighting their design philosophies, architectures, and user experiences in implementing GitOps. ArgoCD is described as &#x22;application-centric,&#x22; while Flux is &#x22;Git-centric.&#x22;" />
</Frame>

Argo CD — deeper look

Architecture (hub-and-spoke)

* An Argo CD server runs on a management/control cluster and can manage many target clusters.
* Key components:
  * API server: serves the web UI and handles CLI/API requests.
  * Repo server: clones Git repositories and renders manifests from generators like Helm and Kustomize.
  * Controller: reconciles Application resources and drives changes to target clusters.

Core concepts

* Application: maps a Git source to a target cluster and namespace; it is the primary unit of sync.
* Project: groups Applications to enforce RBAC, quotas, and allowed destinations — useful for multi-tenancy.
* ApplicationSet: a generator that creates many Applications (e.g., deploying the same app to numerous clusters).
* Sync policy: controls auto-sync, self-heal, pruning, and hooks.

Argo CD highlights

* Rich web UI and visual diffing of desired vs. live state.
* SSO integrations and project-level RBAC.
* Native support for Helm and Kustomize via the repo server.
* Centralized multi-cluster management with a single control plane.

<Frame>
  <img alt="The image is an overview of ArgoCD's core concepts, including Application, Project, Application Set, and Sync Policy, each with a brief description." />
</Frame>

Flux — deeper look

Architecture (decentralized, controller-based)

* Flux is composed of multiple, focused controllers that typically run inside each cluster, enabling cluster autonomy.
* Common controllers:
  * Source controller: watches `GitRepository` and `HelmRepository` sources.
  * Kustomize controller: applies manifests; the `Kustomization` CRD is Flux’s apply unit.
  * Helm controller: manages `HelmRelease` CRDs.
  * Notification controller: routes alerts and notifications.
  * Image controllers: handle image discovery and automation (`ImageRepository`, `ImagePolicy`, `ImageUpdateAutomation`).

Core concepts

* `GitRepository` / `HelmRepository`: declare sources Flux should watch.
* `Kustomization`: applies manifests from a source to a cluster/namespace.
* `HelmRelease`: manages Helm chart lifecycle declaratively.
* `ImagePolicy` / `ImageUpdateAutomation`: enable image automation workflows and policies.

Flux highlights

* Modular — install only the controllers you need.
* Built-in image automation and policies.
* Strong fit for decentralized, per-cluster operations and Git-centric workflows.
* Interactions are primarily via Git and CLI; no central UI by default.

Comparison summary

<Frame>
  <img alt="The image is a feature comparison chart between ArgoCD and Flux, highlighting aspects such as primary interface, multi-cluster model, image automation, and Helm support. Both tools are noted to be CNCF Graduated, meaning they are production-ready, well-supported, and have active communities." />
</Frame>

Quick reference (high level)

|              Feature |                                   Argo CD                                  |                                       Flux                                      |
| -------------------: | :------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: |
|    Primary interface |                                Web UI + CLI                                |                           Git + CLI (no UI by default)                          |
|  Multi-cluster model |                          Centralized hub-and-spoke                         |                     Decentralized (controllers per cluster)                     |
|     Image automation |                 Supported via `Argo Image Updater` project                 | Built-in image automation (ImageRepository, ImagePolicy, ImageUpdateAutomation) |
|         Helm support |                    Native via repo server + Application                    |                    Via Helm Controller and `HelmRelease` CRD                    |
| Progressive delivery | Integrates with [Argo Rollouts](https://argoproj.github.io/argo-rollouts/) |                 Integrates with [Flagger](https://flagger.dev/)                 |
|             Best fit |           Teams needing visual dashboards and centralized control          |             Teams favoring Git-native workflows and cluster autonomy            |

Both projects are CNCF-graduated, production-ready, and backed by active communities and vendor ecosystems.

Key takeaways

* Both Argo CD and Flux implement GitOps effectively; the decision should be driven by operational fit, not a perceived absolute superiority.
* Argo CD is application- and UI-centric, offering a centralized control plane for multi-cluster management.
* Flux is Git-centric and modular, designed for decentralized installations where each cluster manages itself.
* Evaluate team culture (UI vs CLI/Git), ecosystem integrations (image automation, progressive delivery, CI, secrets), and long-term multi-cluster strategy before committing.

<Frame>
  <img alt="The image presents key takeaways comparing ArgoCD and Flux, highlighting differences in their production readiness, operational models, multi-cluster approaches, and support for tools like Helm and Kustomize." />
</Frame>

<Callout icon="lightbulb">
  Both Argo CD and Flux are mature, production-ready GitOps engines. Choose based on operational model (centralized vs decentralized), team preferences (UI vs Git/CLI), and ecosystem fit (image automation, progressive delivery, CI and secret management).
</Callout>

<Callout icon="warning">
  Plan migrations carefully. Switching GitOps engines often requires converting resource models, updating webhooks, and revising runbooks — expect non-trivial effort and potential downtime windows.
</Callout>

Links and references

* [Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/)
* [Flux Documentation](https://fluxcd.io/)
* [Helm](https://helm.sh/)
* [Kustomize](https://kustomize.io/)
* [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
* [Flagger](https://flagger.dev/)
* [Argo Image Updater](https://argoproj.github.io/argo-image-updater/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/dff5382b-dbe7-4cac-bd2b-d5a47028945e/lesson/0d2408b0-4899-4fe5-b864-be3567f9708d" />
</CardGroup>
