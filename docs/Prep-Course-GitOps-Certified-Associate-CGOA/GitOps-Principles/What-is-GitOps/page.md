# What is GitOps

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Principles/What-is-GitOps/page

GitOps is a Git-centered delivery model using declarative configuration and pull-based operators to continuously reconcile applications and infrastructure, enabling auditability, rollbacks, and automated deployments.

GitOps is a delivery framework that places your Git repository at the center of application and infrastructure delivery. It expresses the desired state of your system—applications, configurations, and infrastructure—as declarative code stored in Git, then uses automation to continuously ensure the running environment matches that desired state.

At a high level, the GitOps workflow looks like this:

1. Developers work in feature branches and collaborate via pull requests.
2. When changes are merged into the main branch, a CI pipeline builds and tests the application, produces artifacts (for example, container images), and pushes them to a registry.
3. The CI process also updates the declarative configuration that represents the desired state (Kubernetes manifests, Helm charts, Kustomize overlays, or Jsonnet) in a Git repository.
4. A GitOps operator (agent/controller) running inside the target cluster continuously watches the Git repository, pulls the updated manifests, computes the diff against the cluster’s actual state, and applies only the required changes to reconcile the cluster with Git.

<Frame>
  <img alt="The image illustrates a GitOps workflow, showing the integration of infrastructure, configuration, and application code with Git, CI/CD processes, and Kubernetes deployment." />
</Frame>

Because the operator pulls the desired state from Git rather than having Git push changes into the cluster, GitOps favors a pull-based delivery model and a continuous reconciliation loop. This approach improves observability, reduces blast radius, and provides a clear separation of concerns between CI (artifact creation and manifest updates) and CD (reconciling the cluster to Git).

Key characteristics of GitOps

| Characteristic                     |                                                               Why it matters | Example                                                                   |
| ---------------------------------- | ---------------------------------------------------------------------------: | ------------------------------------------------------------------------- |
| Git as single source of truth      | All desired state and change history lives in Git for traceability and audit | Store manifests or Helm charts in a repository; use `git log` for history |
| Declarative desired state          |                         Enables automated reconciliation and drift detection | Use YAML manifests, Helm charts, or Jsonnet to describe resources         |
| CI updates artifacts and manifests |    CI builds images and updates the manifests repository with new image tags | CI pipeline writes `image: myapp:sha-abc123` into manifests               |
| Pull-based operator                |        Operator pulls changes from Git and applies only diffs to the cluster | Flux or Argo CD running in-cluster watches Git and reconciles             |
| Continuous reconciliation          |                                        Detects and heals drift automatically | Operator periodically compares Git vs cluster and applies fixes           |

When the CI pipeline builds and pushes a new Docker image, it usually also updates the Kubernetes manifests (or a separate manifests repo) to reference that image. The GitOps operator observes the new commit, fetches the updated manifests, and applies them to the target cluster(s), bringing runtime state in line with the repository.

<Frame>
  <img alt="The image is a GitOps workflow diagram illustrating the process of merging application code, running continuous integration tasks, building and pushing a Docker image, and synchronizing Kubernetes manifests using a GitOps operator." />
</Frame>

Rollbacks and auditability are straightforward in GitOps. Because every desired-state change is committed to Git, reverting to a previous state is as simple as reverting the commit and pushing the change (for example, using `git revert <commit>`). The operator will detect the reverted desired state and reconcile the cluster back to the prior stable configuration. This makes every deployment auditable through standard Git history and enables simple, reliable rollbacks.

Useful links and references

* GitOps overview (Weaveworks): [https://www.weave.works/technologies/gitops/](https://www.weave.works/technologies/gitops/)
* Flux (GitOps operator): [https://fluxcd.io/](https://fluxcd.io/)
* Argo CD (GitOps operator): [https://argo-cd.readthedocs.io/en/stable/](https://argo-cd.readthedocs.io/en/stable/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<Callout icon="lightbulb">
  GitOps combines declarative infrastructure, Git-based versioning, and an automated pull-based operator to provide a provable, auditable, and self-healing delivery model. Git stores the canonical desired state and the operator continuously enforces it in the cluster.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/fba78df5-0d92-4a50-85c9-a766064d7402" />
</CardGroup>
