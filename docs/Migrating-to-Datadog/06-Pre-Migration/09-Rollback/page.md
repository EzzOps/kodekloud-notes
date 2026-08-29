# Rollback

Source: https://notes.kodekloud.com/docs/Migrating-to-Datadog/Pre-Migration/Rollback/page

Explains rollbacks in DevOps, their importance, Kubernetes and Helm commands, and rollback best practices.

Rollback is a foundational capability in modern DevOps and release engineering: the ability to revert a change and restore a previous, known-good version of a component or environment quickly and reliably.

Definition

* Rollback: the process of reverting a change to its previous version to restore a stable state.

Why rollbacks matter

* Minimize downtime by restoring a known-good release quickly.
* Preserve observability and diagnostic context so teams can investigate incidents.
* Enable safer migrations by keeping older artifacts until integrations are validated.
* Make rollbacks auditable and repeatable when automated through CI/CD and IaC tooling.

Typical rollback scenario

1. You build a new version of a component and the CI/CD pipeline deploys it to a Kubernetes cluster or another environment.
2. After deployment, you detect a problem in the cluster or in application behavior (e.g., increased errors, degraded performance, failed health checks).
3. To recover quickly, you trigger a rollback. The pipeline or operator redeploys the previous stable version.
4. After the rollback completes, the environment should return to the prior working state while you diagnose and fix the root cause.

Rollback in Kubernetes and Helm

Common Kubernetes commands for rollbacks:

```bash theme={null}
