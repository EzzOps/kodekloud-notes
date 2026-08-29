# db-migration-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration-job
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: db-migration
          image: alpine:3.12
          command: ["/bin/sh", "-c", "echo 'Running Database Migration...' && sleep 15 && echo 'Database Migration Complete.'"]
      restartPolicy: Never
  backoffLimit: 2
```

Step 2 — Add a PostSync notification Job (optional)

* Purpose: send a notification after a successful sync.
* Recommended cleanup: delete after success so notifications don't persist.

Example manifest (slack-notification-job.yaml):

```yaml theme={null}
# slack-notification-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: app-slack-notification-
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: slack-notification
          image: curlimages/curl
          command:
            - /bin/sh
            - -c
            - >
              curl -X POST --data-urlencode 'payload={"channel":"#somechannel","username":"hello","text":"App Sync succeeded","icon_emoji":":ghost:","attachments":[{"text":"https://hooks.slack.com/services/..."}]}' https://hooks.slack.com/services/...
      restartPolicy: Never
  backoffLimit: 2
```

<Frame>
  <img alt="A screenshot of an Argo CD documentation page titled &#x22;Hook lifecycle and cleanup,&#x22; showing a table of hook-delete policies and a section called &#x22;How sync waves work?&#x22; with left-side navigation and a right-hand table of contents." />
</Frame>

Step 3 — Optional PostSync cleanup job

* Purpose: run remedial cleanup when a sync completes (e.g., remove temp resources).
* Example policy: delete only on failure to preserve artifacts for troubleshooting.

Example manifest (cleanup-job.yaml):

```yaml theme={null}
# cleanup-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: cleanup-job
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookFailed
spec:
  template:
    spec:
      containers:
        - name: cleanup
          image: alpine:3.12
          command: ["/bin/sh", "-c", "echo 'Running Cleanup Job...' && sleep 10 && echo 'Cleanup Complete.'"]
      restartPolicy: Never
  backoffLimit: 2
```

Commit and push these manifests to your Git repo.

<Frame>
  <img alt="A dark-themed Gitea web interface showing a &#x22;Commit Changes&#x22; form with fields for a commit message and description, options to commit to the main branch or create a new branch, and blue &#x22;Commit Changes&#x22; and red &#x22;Cancel&#x22; buttons. The footer displays &#x22;Powered by Gitea&#x22; and version information." />
</Frame>

<Callout icon="lightbulb">
  Hook phases act like guardrails: a PreSync hook must succeed before Sync proceeds; a failing PreSync stops the synchronization and prevents deployments.
</Callout>

How phases work

* Happy path: PreSync → Sync → PostSync
* If Sync fails, PostSync is typically not executed unless you configure alternative lifecycle behaviors.

<Frame>
  <img alt="A screenshot of the Argo CD documentation page &#x22;How phases work&#x22; with a left navigation pane and table of contents. It includes a flowchart showing PreSync → Sync → PostSync on success, with a failure path from Sync down to a red &#x22;SyncFail&#x22; box." />
</Frame>

Step 4 — Create the Argo CD Application
Create the application pointing to the folder with your hooks:

```bash theme={null}
argocd app create sync-hooks-2 \
  --repo http://host.docker.internal:5000/kk-org/gitops-argocd-capa \
  --path ./synchronization/hooks \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace sync-hooks-2 \
  --project default \
  --revision HEAD \
  --sync-policy auto
```

If the destination namespace does not exist, create it:

```bash theme={null}
kubectl create namespace sync-hooks-2
```

If the app shows OutOfSync or Missing, it may indicate the namespace was absent or a previous sync is in progress. You can terminate a stuck sync and start a fresh manual sync.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the &#x22;sync-hooks-2&#x22; application marked OutOfSync and Missing, with a right-hand synchronize panel displaying sync options and checkboxes." />
</Frame>

What to expect during a sync

* Argo CD creates the PreSync DB migration Job (hook icon shown).
* Argo CD waits for the Job to finish successfully.
* If the Job succeeds, Argo CD proceeds to create normal resources (Deployment, Service, etc.) — the Sync phase.
* If the Sync succeeds, PostSync hooks (cleanup, notifications) execute as configured.
* hook-delete-policy determines whether Jobs remain after success/failure.

During the demo:

* The migration job was created and completed.
* Deployments were created in the Sync phase.
* A cleanup job ran afterwards and, due to the delete policy, the DB migration job was deleted.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the &#x22;sync-hooks-2&#x22; application with a Healthy app health and Synced status. The main pane displays a resource tree/diagram with deployable resources like nginx and a cleanup-job and their pods." />
</Frame>

Recommended patterns

| Pattern                      | When to use                                                         | Notes                                               |
| ---------------------------- | ------------------------------------------------------------------- | --------------------------------------------------- |
| PreSync job + HookSucceeded  | DB migrations or schema changes that must happen before deployments | Clean up after success to avoid clutter             |
| PostSync job + HookSucceeded | Notifications (Slack, PagerDuty)                                    | Use generateName for unique jobs                    |
| PostSync job + HookFailed    | Cleanup only when sync fails                                        | Preserve logs for debugging by keeping failed hooks |

Summary

* Use `argocd.argoproj.io/hook: PreSync` to force jobs to run before your main sync.
* Use `argocd.argoproj.io/hook: PostSync` for notifications/cleanup after successful syncs.
* Use `argocd.argoproj.io/hook-delete-policy` to control retention of hook resources.
* Optionally use `argocd.argoproj.io/sync-wave` for finer-grained numeric ordering across many resources.

Links and References

* Argo CD Hooks — [https://argo-cd.readthedocs.io/en/stable/user-guide/hooks/](https://argo-cd.readthedocs.io/en/stable/user-guide/hooks/)
* Argo CD Sync Waves — [https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/)
* Argo CD CLI docs — [https://argo-cd.readthedocs.io/en/stable/user-guide/commands/](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/abb5d85a-bab5-41cc-810d-8e6c04681233" />
</CardGroup>


# Demo Sync Wave 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Sync-Wave-1/page

Using Argo CD sync waves and hooks to enforce deterministic resource synchronization order for migrations, namespace creation, database and frontend deployment, and cleanup

In this lesson we explain how to use Argo CD sync waves together with sync hooks to control resource synchronization order. You'll learn why hooks alone are not enough when you need strict sequencing (for example, run schema migration → data migration → namespace creation → PostgreSQL → frontend → cleanup) and how to combine hook phases and numeric sync-wave annotations to enforce that order.

The repository contains a folder `waves-demo` under the `synchronization` path. That YAML contains multiple resources in a single manifest: two migration jobs (schema and data), a Namespace, frontend and PostgreSQL deployments and services, and a cleanup job.

<Frame>
  <img alt="A dark-themed Gitea repository page showing the kk-org/gitops-argocd-capa project with the &#x22;synchronization&#x22; folder open, listing subfolders (hooks, waves, waves-demo) and recent commit messages. The left sidebar shows other repository directories like helm-chart, nginx-app, and vault-secrets." />
</Frame>

High-level resource order in the manifest:

* Schema migration job — currently annotated as a PreSync hook.
* Namespace `app-namespace`.
* Data migration job — also a PreSync hook.
* Frontend deployment + frontend service.
* PostgreSQL deployment + PostgreSQL service.
* Cleanup job — annotated as a PostSync hook.

Baseline (trimmed) excerpt: the two jobs, the namespace, and a few deployment/service fragments. Note both migration jobs are PreSync hooks in this baseline, which causes them to run in parallel when Argo CD syncs the app.

```yaml theme={null}
