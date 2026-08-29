# Pull vs Push Deployment Model

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Pull-vs-Push-Deployment-Model/page

Compares push-based CI/CD and pull-based GitOps deployment models for Kubernetes, highlighting differences in permissions, security, operational ownership, secret management, auditability, benefits and tradeoffs.

This lesson compares the two primary deployment approaches used when delivering application changes to Kubernetes: the push-based model (traditional CI/CD) and the pull-based model (GitOps). Choosing the right model impacts security, operational ownership, CI/CD integration, and auditability.

## Overview

* Push-based: CI/CD pipeline actively pushes changes into the cluster (e.g., runs `kubectl`, Helm, or other deployment tooling).
* Pull-based (GitOps): An in-cluster operator continuously reconciles the desired state from Git or an image registry and pulls changes into the cluster.

Both approaches require artifacts (images, manifests) to be produced by CI, but they differ in where the deployment decision and cluster write permissions reside.

## Push-based model

The push-based model is the pattern used by most traditional pipelines.

How it works:

* CI builds images, runs tests, and — after success — applies manifests or Helm charts directly to the cluster.
* Deployments are executed by the CI system using commands such as `kubectl apply -f` or `helm upgrade --install`.

Permissions and flow:

* CI needs:
  * Read access to the source repo (to fetch code).
  * Write access to the container registry (to push images).
  * Write (cluster) credentials to apply changes in the Kubernetes cluster.
* The cluster needs read access to container registries to pull images.

Benefits:

* Simple to implement using existing CI tools (e.g., [Jenkins](https://learn.kodekloud.com/user/courses/jenkins), GitLab CI, Azure DevOps).
* Pipelines can run arbitrary and complex deployment scripts.
* Direct secret injection from CI can be simpler for some workflows.

Drawbacks:

* CI becomes tightly coupled with deployment logic; migrating CI tools can require rework.
* Storing cluster credentials in CI increases attack surface — a compromised CI runner can modify the cluster.
* Enforcing least-privilege is harder because CI often requires broad cluster permissions.

> **warning** Storing long-lived or overly broad cluster credentials in CI systems is a common attack vector. Prefer short-lived credentials, fine-grained permissions, and dedicated service accounts whenever possible.

## Pull-based model (GitOps)

The pull-based approach underpins GitOps: an operator inside the cluster continuously reconciles declared desired state from Git or an image registry.

How it works:

* CI builds images and pushes them to the container registry.
* The GitOps operator (for example, [Argo CD](https://learn.kodekloud.com/user/courses/gitops-with-argocd) or [Flux](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)) monitors a Git repo (or registry) and pulls manifests or image updates.
* When changes are detected, the operator applies them to the cluster.

Permissions and flow:

* CI typically needs:
  * Write access to the container registry (to publish images).
  * Write access to the Git repository (if CI updates manifests or image tags).
* The cluster operator needs:
  * Read access to Git and registries.
  * In-cluster permissions to create/update Kubernetes objects (scoped to the operator).
* CI does not require direct write access to the Kubernetes cluster.

Advantages:

* Decouples deployment from CI: any CI that can publish images and update Git can trigger deployments.
* Reduces external attack surface: external systems don’t need direct cluster write permissions.
* Single source of truth: Git stores desired state and audit history.
* Better for multi-team and multi-cluster setups: operators can be scoped per repo, directory, or namespace.

<Frame>
  <img alt="The image compares push-based and pull-based deployment approaches, highlighting their processes, access permissions, and advantages or disadvantages." />
</Frame>

Secret management and operational complexity:

* GitOps encourages commit-centric workflows, so secrets should be encrypted before they are stored in Git (e.g., Bitnami Sealed Secrets, Mozilla SOPS, or Vault integrations).
* The operator or an in-cluster decryptor must be capable of decrypting secrets at runtime.
* This adds operational complexity versus injecting secrets from CI, but gives better traceability, reproducibility, and audit trails.

Trade-offs and considerations:

* The operator needs appropriate in-cluster RBAC permissions, but these can be scoped and audited centrally.
* Pull-based workflows favor declarative, auditable pipelines and generally scale better across clusters and teams.
* Push-based workflows still make sense for small teams, legacy systems, or when pipelines require tight control over custom deployment steps.

## Quick comparison

| Aspect                       | Push-based (CI-driven)                                  | Pull-based (GitOps)                                                 |
| ---------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------- |
| Who performs deployment      | CI system (external)                                    | In-cluster operator                                                 |
| Required cluster credentials | CI needs write access                                   | Operator needs scoped in-cluster permissions                        |
| CI cluster permissions       | Often broad                                             | Not required for deploys                                            |
| Audit / traceability         | Pipeline logs; manifests may not be the source of truth | Git is the single source of truth; clear history                    |
| Secret handling              | Injected by CI or external secret managers              | Encrypted in Git + in-cluster decryption (SOPS/SealedSecrets/Vault) |
| Best for                     | Complex scripts, legacy setups                          | Multi-team, multi-cluster, declarative workflows                    |

## Recommended decision guide

* Use Pull-based (GitOps) when:
  * You want declarative, auditable deployments and Git as single source of truth.
  * You operate multiple clusters or many teams.
  * You need a smaller external attack surface and easier policy enforcement.

* Use Push-based when:
  * Your deployment requires complex procedural steps not easily expressed declaratively.
  * You have a simple, single-cluster setup or legacy tooling that expects push-style deployments.
  * You accept the operational cost of securing CI credentials and permissions.

## References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Argo CD GitOps course (KodeKloud)](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* [Flux GitOps course (KodeKloud)](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)
* [Jenkins course (KodeKloud)](https://learn.kodekloud.com/user/courses/jenkins)
* [Bitnami Sealed Secrets (KodeKloud)](https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes)
* [HashiCorp Vault (KodeKloud)](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification)

That's all for now.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/7f25d7ec-c8a1-4db0-b435-6897944f4e25)
