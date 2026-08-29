# Application source/destination (example)
source:
  repoURL: "http://host.docker.internal:5000/kk-org/gitops-argocd-capa"
  targetRevision: "HEAD"
  path: "./nginx-app"
destination:
  server: "https://kubernetes.default.svc"
  namespace: "nginx-app-1"
```

The repository contains a Deployment manifest that initially sets `replicas: 1` and deploys into `nginx-app-1`.

Change the desired state in Git

When you update the manifest in Git (for example, scale to 2 replicas), commit the change. Argo CD will eventually show the application as OutOfSync (desired state: 2 replicas; live cluster: 1 replica).

Example updated Deployment (scale to 2 replicas):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          imagePullPolicy: Always
          ports:
            - containerPort: 80
```

Refresh vs automatic polling

* Manual Refresh: Clicking Refresh in the Argo CD UI re-evaluates the application immediately and shows OutOfSync status.
* Polling: If you don't refresh manually, Argo CD polls repositories based on the reconciliation timeout (default up to 3 minutes). Detection may therefore take up to that interval.

Configure a shorter reconciliation timeout

Add the `timeout.reconciliation` key to the `argocd-cm` ConfigMap to change the polling interval. For example, set it to `60s` to poll about every 60 seconds.

Check whether the key exists:

```bash theme={null}
kubectl -n argocd get configmap argocd-cm -o yaml | grep -i timeout.reconciliation || true
```

If missing, patch the ConfigMap (example sets 60 seconds):

```bash theme={null}
kubectl -n argocd patch configmap argocd-cm --patch '{"data":{"timeout.reconciliation":"60s"}}'
```

Verify the key:

```bash theme={null}
kubectl -n argocd get configmap argocd-cm -o yaml | grep -i timeout.reconciliation
# expected output:
# timeout.reconciliation: 60s
```

How the change takes effect

The repo-server process reads this value as the environment variable ARGOCD\_RECONCILIATION\_TIMEOUT. Updating the ConfigMap does not automatically update the environment of running pods — you must restart the repo-server deployment.

> **lightbulb** After patching `argocd-cm` you need to restart the repo server so it picks up
  the new `timeout.reconciliation` value: kubectl -n argocd rollout restart
  deployment argocd-repo-server

Restart repo-server and watch pods

Restart the deployment:

```bash theme={null}
kubectl -n argocd rollout restart deployment argocd-repo-server
```

Watch the new pods come up:

```bash theme={null}
kubectl -n argocd get pods -w
```

Once the new repo-server pod is Running, Argo CD will use the new reconciliation timeout (for example, \~60s) to poll repositories.

Enable Auto-Sync (optional)

If you want Argo CD to automatically apply changes it detects, enable Auto-Sync for the application (in the UI or via YAML). In the UI, open the Application, edit sync settings and enable Auto-Sync and any additional options (prune, self-heal, etc.).

Example UI screenshot:

<Frame>
  <img
    alt="A screenshot of the Argo CD web UI showing an &#x22;nginx-app-1&#x22; application with
Healthy and Synced status on the left and a sync/options panel on the right
(the &#x22;auto-create namespace&#x22; option is checked). The right panel shows
synchronization settings and available checkboxes for prune, dry run, replace,
etc."
  />
</Frame>

Test the change end-to-end

1. Commit a change in Git (e.g., change replicas to 3).
2. With `timeout.reconciliation: 60s` and repo-server restarted, Argo CD should detect the change and begin synchronization within roughly one minute.
3. Watch pods in the target namespace:

```bash theme={null}
kubectl -n nginx-app-1 get pods -w
```

When sync completes, the live state should match the desired state in Argo CD (pods scaled per the manifest). Example resource view:

<Frame>
  <img
    alt="A screenshot of the Argo CD web UI showing an application named
&#x22;nginx-app-1&#x22; with status indicators (Healthy, Synced to HEAD) and a resource
graph flow from the app to a deployment, replica set, and pod. The left
sidebar shows navigation (Applications, Settings, User Info, Documentation)
and resource
filters."
  />
</Frame>

Quick reference — commands and purpose

| Command                                                                                           | Purpose                                         |
| ------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `kubectl -n argocd get configmap argocd-cm -o yaml \| grep -i timeout.reconciliation`             | Check current reconciliation timeout key        |
| `kubectl -n argocd patch configmap argocd-cm --patch '{"data":{"timeout.reconciliation":"60s"}}'` | Add or update reconciliation timeout to 60s     |
| `kubectl -n argocd rollout restart deployment argocd-repo-server`                                 | Restart repo-server so it reads the new timeout |
| `kubectl -n argocd get pods -w`                                                                   | Watch Argo CD pods during restart               |
| `kubectl -n nginx-app-1 get pods -w`                                                              | Observe app pod scaling as sync occurs          |

Summary

* Default reconciliation/polling interval: up to 3 minutes.
* Shorten polling by adding `timeout.reconciliation` (e.g., `"60s"`) to `argocd-cm`.
* Patch the ConfigMap and restart the `argocd-repo-server` deployment so pods pick up the new setting.
* Enable Auto-Sync to have Argo CD automatically apply detected changes.

Links and references

* [Argo CD Documentation — FAQ](https://argo-cd.readthedocs.io/en/stable/faq/)
* [Argo CD — Application Concepts](https://argo-cd.readthedocs.io/en/stable/user-guide/argo-cd-overview/)
* Kubernetes docs: [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/0b14ab3a-657d-42be-a8ab-b8d78d12a193)


# Demo Sync Hook 1

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Sync-Hook-1/page

Explains using Argo CD sync hooks to order and run Jobs like migrations and cleanup during application synchronization.

Sync hooks control the order and lifecycle of resources applied by Argo CD during a synchronization. They let you run Jobs and other resources at specific points in the synchronization process (for example, to run database migrations before deploying an application or to clean up temporary resources afterward).

Common hook phases:

* PreSync — run before the main sync step.
* Sync — the normal synchronization of non-hooked resources.
* PostSync — run after a successful sync.
* SyncFail — run when a sync fails.
* PreDelete / PostDelete — run during deletion lifecycles.

The typical sync flow looks like this: the operation begins with PreSync; if PreSync succeeds it proceeds to Sync; if Sync fails, SyncFail hooks run; if Sync succeeds it proceeds to PostSync. Hook cleanup lifecycles (how and when hook resources are removed) are configurable and will be covered elsewhere.

| Hook Phase             | When it runs                         | Typical use case                                            |
| ---------------------- | ------------------------------------ | ----------------------------------------------------------- |
| PreSync                | Before regular resources are applied | Run migrations or prepare state required by other resources |
| Sync                   | Regular resource application phase   | Deploy Deployments, Services, etc.                          |
| PostSync               | After a successful sync              | Run cleanup tasks or post-deploy verification               |
| SyncFail               | After a sync failure                 | Rollback-related tasks or notifications                     |
| PreDelete / PostDelete | During resource deletion             | Cleanup external state or revoke credentials                |

<Frame>
  <img alt="A screenshot of an Argo CD documentation page showing a flowchart of sync phases: PreSync -> Sync -> PostSync with success arrows. If Sync fails, an arrow points downward to a red &#x22;SyncFail&#x22; box." />
</Frame>

Example scenario

In my GitOps Argo CD Kappa project I have a repository path synchronization/hooks containing three Kubernetes manifests:

* An Nginx Deployment
* A database migration Job
* A cleanup Job

Below is the db-migration Job manifest used in this demo:

```yaml theme={null}
