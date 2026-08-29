# SyncWaves

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/SyncWaves/page

Explains Argo CD sync waves and hooks, using numeric annotations to deterministically order resource application within sync phases to avoid race conditions.

Let's talk about Sync Waves in Argo CD.

Sync hooks (PreSync, Sync, PostSync, etc.) define the high-level phases of a sync. When you need fine-grained ordering inside a single phase—for example, ensuring a Namespace exists before creating a Deployment in it—sync waves provide deterministic control.

A sync wave is a numeric annotation on a Kubernetes resource that Argo CD uses to determine the relative ordering inside a sync phase. Lower numbers are applied before higher numbers. Waves can be negative, zero, or positive. Resources with the same wave number are applied in parallel.

By combining hooks (to define phases) and sync waves (to order resources within a phase), you can build reliable rollout plans for complex applications and avoid race conditions.

> **lightbulb** Sync Waves order resources within a given hook/phase (e.g., PreSync or Sync). Wave numbers are only compared among resources in the same phase — a PreSync with wave -1 runs before a Sync with wave -1.

## How sync waves work (quick summary)

* Annotation key: argocd.argoproj.io/sync-wave
* Scope: Compared only among resources in the same hook/phase.
* Order: Lower wave numbers are applied before higher numbers.
* Parallelism: Resources sharing the same wave number are applied in parallel.

## Example scenario

Goal:

* Run database migrations first,
* Create application Namespace,
* Deploy front-end, then database,
* Run a post-deploy cleanup/verification task.

Approach:

* Use PreSync hooks for preparatory jobs (migrations, checks).
* Use the Sync phase with waves to order Namespace → front-end → database.
* Use a PostSync hook for final cleanup or verification.

## Step-by-step sync flow (how Argo CD interprets this)

1. PreSync phase runs first. Within PreSync:
   * wave -2 job runs first (e.g., schema migration).
   * wave -1 job runs next (e.g., data verification).
     If any PreSync hook fails, the entire sync is considered failed.
2. Sync phase begins only after all PreSync hooks succeed. Within Sync:
   * Create the Namespace (wave -1) so it exists before deployments are created.
   * Create the front-end Deployment and Service (both wave 0) in parallel, then wait for them to become healthy.
   * Create the PostgreSQL Deployment and Service (both wave 1) in parallel, then wait for them to become healthy.
3. PostSync phase begins only after all Sync-phase resources are healthy. Run the cleanup job (PostSync hook) — this could run integration tests, send notifications, or perform final cleanup.

## Warning about failure behavior

> **warning** If a hook (for example, a PreSync job) fails, Argo CD will mark the sync as unsuccessful. Make hooks idempotent and configure appropriate timeouts and retries to avoid spurious failures.

## Example manifests (annotations demonstrate hooks and sync-wave usage)

PreSync jobs (migrations)

```yaml theme={null}
apiVersion: batch/v1
kind: Job
metadata:
  name: schema-migration-job
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/sync-wave: '-2'
---
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration-job
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/sync-wave: '-1'
```

Sync-phase resources (namespace → frontend → postgresql)

```yaml theme={null}
apiVersion: v1
kind: Namespace
metadata:
  name: app-namespace
  annotations:
    argocd.argoproj.io/sync-wave: '-1'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  annotations:
    argocd.argoproj.io/sync-wave: '0'
spec:
  # deployment spec omitted for brevity
  replicas: 3
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  annotations:
    argocd.argoproj.io/sync-wave: '0'
spec:
  # service spec omitted for brevity
  ports:
    - port: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
  annotations:
    argocd.argoproj.io/sync-wave: '1'
spec:
  # postgres deployment spec omitted for brevity
  replicas: 1
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql-service
  annotations:
    argocd.argoproj.io/sync-wave: '1'
spec:
  # service spec omitted for brevity
  ports:
    - port: 5432
```

PostSync cleanup/verification job

```yaml theme={null}
apiVersion: batch/v1
kind: Job
metadata:
  name: cleanup-job
  annotations:
    argocd.argoproj.io/hook: PostSync
```

## Best practices

* Make hooks idempotent so retries or re-runs are safe.
* Use negative waves for preparatory resources (e.g., -2, -1), zero for primary resources, and positive waves for resources that should be created last.
* Group unrelated resources that can be applied in parallel with the same wave.
* Add readiness checks (liveness/readiness probes) to Deployments so Argo CD waits for true health before proceeding to the next wave.
* Keep wave numbers sparse enough that you can insert intermediate steps later (e.g., use -10, -5, 0, 5, 10).

## Quick reference table

|       Concept | Use case                                                                  | Example annotation                   |
| ------------: | ------------------------------------------------------------------------- | ------------------------------------ |
|  PreSync hook | Run DB migrations or checks before any resources are created              | `argocd.argoproj.io/hook: PreSync`   |
|    Sync phase | Apply the core resources (Namespace, Deployments, Services)               | `argocd.argoproj.io/sync-wave: '0'`  |
| PostSync hook | Run verification or cleanup after resources are healthy                   | `argocd.argoproj.io/hook: PostSync`  |
|     Sync wave | Order resources inside a phase (lower runs first, equal runs in parallel) | `argocd.argoproj.io/sync-wave: '-1'` |

## Links and references

* Argo CD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* GitOps with Argo CD (course): [https://learn.kodekloud.com/user/courses/gitops-with-argocd/](https://learn.kodekloud.com/user/courses/gitops-with-argocd/)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

## Summary

* Hooks (PreSync, Sync, PostSync) control macro phases of a sync.
* Sync waves control ordering inside those phases: lower numbers run first; identical numbers run together.
* Use PreSync for migrations and checks, Sync waves for ordered resource creation, and PostSync for verification or cleanup.
* Combining hooks and sync waves helps avoid race conditions and ensures reliable application rollouts.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/714862f3-140d-4d24-b8cf-281a07383fa8)
