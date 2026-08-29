# Inspect the repo-server pod environment to see the ARGOCD_RECONCILIATION_TIMEOUT reference
kubectl -n argocd describe pod -l app.kubernetes.io/name=argocd-repo-server | grep -i "ARGOCD_RECONCILIATION_TIMEOUT:" -B1

# Patch the ConfigMap to set the reconciliation timeout to 300 seconds (5 minutes)
kubectl -n argocd patch configmap argocd-cm --patch='{"data":{"timeout.reconciliation":"300s"}}'

# Example output:
# Restart the repo-server deployment to pick up the new configuration
kubectl -n argocd rollout restart deploy argocd-repo-server

# Example output:
# After the rollout completes, list the repo-server pods and verify the env entry references the configmap key
kubectl -n argocd get pods -l app.kubernetes.io/name=argocd-repo-server
kubectl -n argocd describe pod <argocd-repo-server-pod-name> | grep -i "ARGOCD_RECONCILIATION_TIMEOUT:" -B1
```

> **lightbulb** When setting `timeout.reconciliation`, always include a time unit (for example `300s` or `5m`). Very short polling intervals increase load on your Git provider and Argo CD components — pick an interval that balances responsiveness and resource usage for your environment.

Polling introduces a small delay between a Git push and Argo CD reconciling that change (three minutes by default). If you require near-instant synchronization, configure push-based notifications (webhooks) from your Git provider so Argo CD is notified immediately when commits are pushed.

<Frame>
  <img alt="A diagram titled &#x22;Reconciliation Loop – WebHook&#x22; showing a developer pushing a commit to GitHub which triggers Argo CD components. It depicts argocd-server and argocd-repo-server pods running inside a Kubernetes cluster with Argo CD and Kubernetes icons." />
</Frame>

To use webhooks, create a webhook in your Git provider (for example, [GitHub](https://github.com) or [GitLab](https://gitlab.com)) that targets the Argo CD server webhook endpoint:

/api/webhook

A push event to the repository will notify Argo CD immediately, prompting it to pull the committed changes and reconcile without waiting for the next poll. Ensure the Argo CD API server is reachable from your Git provider (directly or via a secure proxy), and secure the webhook (TLS, secret/signature verification, and network restrictions).

> **warning** Make sure the Argo CD API server endpoint used for webhooks is accessible from your Git provider. Protect webhook traffic using TLS, verify payload signatures or secrets, and restrict network access to reduce risk.

Links and references

* [Argo CD documentation — Configuration](https://argo-cd.readthedocs.io/en/stable/operator-manual/config-management/)
* [Kubernetes kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
* Git provider docs: [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/creating-webhooks), [GitLab Webhooks](https://docs.gitlab.com/ee/user/project/integrations/webhooks/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/197dd1cb-9df3-4352-ada6-e62e5ca364f8)


# Sync Hooks

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Sync-Hooks/page

Explains ArgoCD sync hooks for sequencing Kubernetes resource creation, running pre and post tasks, and policies for cleaning up hook resources.

Sync Hooks let you control the order and lifecycle of Kubernetes resources ArgoCD creates during an application sync. Instead of letting `kubectl apply` (or ArgoCD's default sync) create everything at once—potentially starting your app before its database or ConfigMap exist—you annotate specific resources in your manifests so ArgoCD runs them at well-defined moments in the sync lifecycle.

Use cases for Sync Hooks:

* Run database migrations before deploying the application.
* Create or restore backups prior to changes.
* Run integration tests or notify systems after a successful deployment.
* Clean up temporary resources after syncs.

> **lightbulb** Sync hooks are defined with annotations in your Kubernetes manifests (for example, `argocd.argoproj.io/hook: PreSync`). ArgoCD will create the hook resource (a Job, Pod, etc.) and wait for its completion where applicable, before proceeding to the next phase.

## Sync phases

ArgoCD processes hooks in these primary phases:

| Phase          | When it runs                                                   | Typical use cases                                           |
| -------------- | -------------------------------------------------------------- | ----------------------------------------------------------- |
| PreSync        | Before the main sync is applied                                | db migrations, secrets creation, backups                    |
| Sync (default) | Apply main resources (Deployments, Services, ConfigMaps, etc.) | Primary application rollout; ArgoCD waits for health checks |
| PostSync       | After main sync succeeds and resources are healthy             | Integration tests, notifications, cleanup tasks             |
| SyncFail       | Triggered when main sync fails                                 | Rollbacks, notifications, remedial tasks                    |

<Frame>
  <img alt="A simple flowchart titled &#x22;Sync Hooks&#x22; showing three main steps—PreSync -> Sync -> PostSync on success—with a downward arrow from Sync to SyncFail on failure. The arrows between steps are labeled &#x22;Success&#x22; and the failure path is labeled &#x22;Failure.&#x22;" />
</Frame>

## Example: run DB migration before deployment

Imagine these files in your repo:

```text theme={null}
Synchronization
├─ cleanup-job.yml
├─ deployment.yml
├─ migration-job.yml
├─ configmap.yaml
├─ frontend-deployment.yaml
├─ frontend-service.yml
├─ postgresql-deployment.yaml
└─ postgresql-service.yml

$ kubectl apply -f
```

You want `db-migration` to run first (and succeed) before ArgoCD creates the `my-app` Deployment. Annotate the migration Job with `argocd.argoproj.io/hook: PreSync`. ArgoCD will:

1. Create the Job and wait for it to finish successfully.
2. If the Job succeeds, proceed to apply the main resources (Deployment, Service), waiting for them to become healthy.
3. After the main sync completes and resources are healthy, run any PostSync hooks.

Example manifests:

```yaml theme={null}
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
spec:
  template:
    spec:
      containers:
      - name: migrator
        image: alpine
        command: ["sh", "-c", "echo 'database migration...'"]
      restartPolicy: Never
  backoffLimit: 1
```

```yaml theme={null}
apiVersion: batch/v1
kind: Job
metadata:
  name: clean-up
  annotations:
    argocd.argoproj.io/hook: PostSync
spec:
  template:
    spec:
      containers:
      - name: cleanup
        image: alpine
        command: ["sh", "-c", "echo 'cleaning...'"]
      restartPolicy: Never
  backoffLimit: 1
```

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: webserver
        image: nginx
```

If the migration Job fails, the sync is marked as failed and ArgoCD will not proceed to the main Deployment step. You can use SyncFail hooks to run remediation tasks when this happens.

> **warning** Hooks create real Kubernetes resources (Jobs, Pods, etc.). Without a cleanup strategy, completed or failed hook resources accumulate in the cluster and can cause:

  * Cluster clutter — harder to inspect and manage.
  * Sync failures — a future sync may fail if it attempts to create a resource with the same name as an existing completed hook.

<Frame>
  <img alt="A slide titled &#x22;Sync Hooks – CleanUp&#x22; explaining that without cleanup completed/failed sync hooks pile up, causing &#x22;Cluster Clutter&#x22; (making the cluster noisy and hard to inspect) and &#x22;Sync Failures&#x22; (reused job names blocking subsequent syncs)." />
</Frame>

## Cleaning up hook resources: hook-delete-policy

ArgoCD provides the `argocd.argoproj.io/hook-delete-policy` annotation to automatically remove hook resources according to chosen policies. Two practical policies:

| Policy        | Behavior                                                   | Typical reason                                                |
| ------------- | ---------------------------------------------------------- | ------------------------------------------------------------- |
| HookSucceeded | Delete the hook resource only if it completed successfully | Keep cluster clean while preserving failed runs for debugging |
| HookFailed    | Delete the hook resource only if it failed                 | Keep successful runs as audit evidence; discard failed ones   |

Example: delete the migration Job if it succeeds, but only retain successful runs of the cleanup job (or invert policy depending on your needs):

```yaml theme={null}
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
      - name: migrator
        image: alpine
        command: ["sh", "-c", "echo 'database migration...'"]
      restartPolicy: Never
  backoffLimit: 1
```

```yaml theme={null}
apiVersion: batch/v1
kind: Job
metadata:
  name: clean-up
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookFailed
spec:
  template:
    spec:
      containers:
      - name: cleanup
        image: alpine
        command: ["sh", "-c", "echo 'cleaning...'"]
      restartPolicy: Never
  backoffLimit: 1
```

In this setup:

* The `db-migration` job will be deleted after a successful run (keeps the cluster tidy).
* The `clean-up` job will be retained if it succeeded, or deleted if it failed (useful if you want success records kept for auditing).

## Quick best practices

* Use unique names when necessary, or apply delete policies to avoid collisions.
* Keep prolonged-running hook Jobs to a minimum; they block the sync progress until completion.
* Use PreSync for anything that must exist before the main app; use PostSync for tasks that depend on the full app being healthy.
* Retain failed hook resources (default HookSucceeded behavior) to help with debugging.

## Links and references

* [Argo CD Sync Hooks (official docs)](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-hooks/)
* [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
* [Argo CD Application health and sync](https://argo-cd.readthedocs.io/en/stable/user-guide/health/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/2a5355a9-53a3-4283-a64e-df13c7d39ba5)
