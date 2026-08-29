# db-migration-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration-job
spec:
  template:
    spec:
      containers:
      - name: db-migration
        image: alpine:3.12
        command:
        - /bin/sh
        - -c
        - |
          echo 'Running Database Migration...' \
          && sleep 15 \
          && echo 'Database Migration Complete.'
      restartPolicy: Never
  backoffLimit: 2
```

(Note: the cleanup Job in the repository initially had an incomplete annotation; I fixed that and committed the changes.)

Application configuration used to deploy these manifests (example settings):

| Field                 | Value (example)                                                  |
| --------------------- | ---------------------------------------------------------------- |
| Application name      | syncHooks0                                                       |
| Project               | default                                                          |
| Sync policy           | Automatic                                                        |
| Auto-create namespace | Enabled                                                          |
| Repository URL        | (my repo URL)                                                    |
| Path                  | ./synchronization/hooks                                          |
| Destination cluster   | [https://kubernetes.default.svc](https://kubernetes.default.svc) |
| Destination namespace | sync-hooks-0                                                     |

When I created the Application, Argo CD started applying the manifests. Because none of the resources had hook annotations initially, Argo CD applied the three manifests concurrently. The result was that the cleanup Job, the migration Job, and the Nginx deployment were all created at the same time.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the application &#x22;sync-hooks-0&#x22; marked Healthy and Synced, with a resource tree displaying components like nginx, cleanup-job, and db-migration-job. The top toolbar shows actions such as Details, Diff, Sync, History and Rollback." />
</Frame>

Desired ordering for this demo:

1. Run the migration Job first.
2. When the migration Job completes successfully, create the Nginx Deployment.
3. After the Deployment is ready, run the cleanup Job.

To enforce this ordering, add Argo CD hook annotations to the manifests so that Argo CD executes Jobs at the appropriate sync phases (for example, marking the migration Job as PreSync and the cleanup Job as PostSync). Hooks control execution timing and can also be configured with deletion/cleanup policies.

Example annotations you can add to achieve the ordering:

* Mark the migration Job as PreSync:

```yaml theme={null}
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync
```

* Leave the Nginx Deployment as a regular resource (applied during Sync).

* Mark the cleanup Job as PostSync:

```yaml theme={null}
metadata:
  annotations:
    argocd.argoproj.io/hook: PostSync
```

You can also control hook deletion behavior with annotations such as:

```yaml theme={null}
metadata:
  annotations:
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
```

(See the Argo CD docs for other deletion-policy options.)

<Callout icon="lightbulb">
  By default, Argo CD applies resources concurrently. Use hook annotations (for example, `argocd.argoproj.io/hook: PreSync` or `PostSync`) to enforce ordering for tasks like database migrations or cleanup. For full details and advanced hook lifecycle options, refer to the Argo CD Sync Hooks documentation: [https://argo-cd.readthedocs.io/en/stable/user-guide/hooks/](https://argo-cd.readthedocs.io/en/stable/user-guide/hooks/)
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/c4033a0f-7848-4b31-b8fa-7d390035d3df" />
</CardGroup>


# Demo Sync Hook 2

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Sync-Hook-2/page

Guide demonstrating Argo CD hooks to enforce ordered PreSync, Sync, and PostSync jobs, manage sync waves and hook delete policies for migrations, notifications, and cleanup.

This guide continues the Sync Hooks demo and shows how to enforce ordering between jobs and deployments in Argo CD using hook annotations (PreSync, Sync, PostSync), sync waves, and hook-delete-policy. This prevents jobs such as database migrations from running in parallel with deployments and ensures predictable lifecycle and cleanup of hook resources.

Why use hooks?

* Ensure a DB migration runs before application Deployments.
* Run notifications or cleanup only after a successful sync.
* Control whether hook resources are retained or removed.

Key annotation keys (Argo CD hooks)

| Annotation                              | Purpose                                                               | Example                                                |
| --------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------ |
| `argocd.argoproj.io/hook`               | Defines hook phase: `PreSync`, `Sync`, `PostSync`                     | `argocd.argoproj.io/hook: PreSync`                     |
| `argocd.argoproj.io/hook-delete-policy` | Controls cleanup: `HookSucceeded`, `HookFailed`, `BeforeHookCreation` | `argocd.argoproj.io/hook-delete-policy: HookSucceeded` |
| `argocd.argoproj.io/sync-wave`          | Numeric ordering when using sync waves                                | `argocd.argoproj.io/sync-wave: "5"`                    |

For more details see the Argo CD hooks docs:

* [https://argo-cd.readthedocs.io/en/stable/user-guide/hooks/](https://argo-cd.readthedocs.io/en/stable/user-guide/hooks/)
* [https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/)

Open the Git repository and navigate to the synchronization/hooks folder to add the manifests and annotations.

<Frame>
  <img alt="A dark-themed Gitea repository page showing the kk-org/gitops-argocd-capa project with the &#x22;synchronization&#x22; folder open, listing subfolders like hooks, waves, and waves-demo. The left sidebar shows the repo file tree and the main pane shows recent file commits." />
</Frame>

Step 1 — Add a PreSync DB migration Job

* Purpose: run a migration before any application resources are created.
* Desired lifecycle: the job should be removed after it succeeds.

Example manifest (db-migration-job.yaml):

```yaml theme={null}
