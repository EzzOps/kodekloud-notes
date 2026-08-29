# ConceptsTerminology

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Principles/ConceptsTerminology/page

Overview of Argo CD concepts and terminology for GitOps, covering Applications, sources, projects, sync and health status, reconciliation, and common CLI operations.

In this lesson we cover the foundational Argo CD concepts and terminology you need to use Argo CD effectively. This overview assumes familiarity with Git, Docker, and Kubernetes. If you need a refresher, see these courses:

* [GIT for Beginners](https://learn.kodekloud.com/user/courses/git-for-beginners)
* [Docker Training Course for the Absolute Beginner](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner)
* [Kubernetes for the Absolute Beginners - Hands-on Tutorial](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial)
* [Coursera Labs: Source Control & CI/CD - Hands-On](https://learn.kodekloud.com/user/courses/coursera-source-control-ci-cd-hands-on)
* [GitOps with ArgoCD](https://learn.kodekloud.com/user/courses/gitops-with-argocd)

<Callout icon="lightbulb">
  Argo CD implements GitOps: the Git repository holds the desired (target) state, and Argo CD continuously reconciles the live cluster state to match that target state.
</Callout>

Core concepts at a glance

|                Concept | What it is                                                                                                                                                        | Example / Notes                                                     |
| ---------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
|          `Application` | A Kubernetes custom resource (CR) of kind `Application` that tells Argo CD where to find manifests, which cluster/namespace to deploy to, and how to render them. | Can reference Kustomize overlays, Helm charts, or plain manifests.  |
| Source types / tooling | How manifests are packaged and rendered (renderers/generators).                                                                                                   | Common: Kustomize, Helm, plain YAML. Argo CD also supports plugins. |
|                Project | A grouping and governance layer that limits repositories, clusters, and namespaces for Applications.                                                              | Useful for multi-team boundaries and RBAC policies.                 |

Application (Argo CD Application)

* An Argo CD Application is the main unit Argo CD manages. It is a Kubernetes CR named `Application`.
* The Application CR includes:
  * `source`: repository URL and path to manifests or chart
  * `destination`: cluster and namespace where resources will be applied
  * rendering tool choice (Kustomize, Helm, plain YAML, or a plugin)
  * sync policies, credentials, and other options

Example: minimal `Application` manifest (YAML)

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
spec:
  project: default
  source:
    repoURL: 'https://github.com/example/guestbook'
    path: 'overlays/prod'
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: guestbook
  syncPolicy:
    automated: {}
```

Source types and tooling

* The Application `source` section defines how Argo CD should render and obtain manifests.
* Common renderers:
  * Kustomize — overlay-driven configuration
  * Helm — templated charts and `values.yaml`
  * Plain Kubernetes manifests (YAML)
* Argo CD can be extended with custom generators and plugins for advanced workflows.

Projects

* Projects are a namespace-like control plane within Argo CD to group and govern Applications.
* Use Projects to restrict which Git repos, clusters, and namespaces an Application can target and to enforce RBAC boundaries.

Application states

|        State | Definition                                                                          |
| -----------: | ----------------------------------------------------------------------------------- |
| Target state | The desired configuration stored in Git (manifests, overlays, Helm values).         |
|   Live state | The actual state of resources running in the Kubernetes cluster(s) Argo CD manages. |

Synchronization and reconciliation

* Argo CD continuously compares the target state (Git) to the live state (cluster) and performs a reconciliation loop.
* When differences are detected, Argo CD can perform a sync operation to apply changes so the live state matches the target state.

Sync status vs. operation status

* Sync status (high-level): indicates whether the live resources match Git, for example:
  * `Synced` — cluster matches Git
  * `OutOfSync` — cluster diverges from Git
* Operation status (task-level): describes the progress/outcome of the last sync action, for example:
  * `Running`, `Succeeded`, `Failed`

Common CLI operations

* Sync an Application:
  * `argocd app sync <app-name>`
* Refresh an Application (re-evaluate Git & cluster state):
  * `argocd app refresh <app-name>`
* View Application status:
  * `argocd app get <app-name>`

Refresh

* A refresh forces Argo CD to re-evaluate the repository and live cluster state. If differences are found, a new sync can be initiated (manually or automatically depending on sync policy).

Health status and checks

* Argo CD provides built-in health checks for many Kubernetes resource kinds and reports per-resource and overall Application health.
* Health checks make it easy to see whether individual resources (Pods, Deployments, Services, etc.) are healthy and whether the Application is overall healthy.

<Frame>
  <img alt="The image is a visual guide to ArgoCD concepts and terminology, featuring definitions for terms like &#x22;Application,&#x22; &#x22;Target state,&#x22; and &#x22;Sync status,&#x22; along with relevant logos and icons." />
</Frame>

You may not interact with Argo CD's built-in health checks directly every day, but understanding them clarifies how Argo CD evaluates resources during reconciliation and sync.

Further reading and references

* [Argo CD Documentation](https://argo-cd.readthedocs.io/) — official docs and API reference
* [GitOps Principles](https://www.weave.works/technologies/gitops/) — concepts and best practices
* [Kubernetes Documentation](https://kubernetes.io/docs/) — core Kubernetes concepts and resources

That covers the basic Argo CD concepts and terminology. Use this as a quick reference when designing GitOps workflows with Argo CD.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/33ca3f0b-f15f-410a-bfe0-e573051803f8" />
</CardGroup>
