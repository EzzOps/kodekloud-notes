# If you don't have the alias `k`, use kubectl
kubectl -n argocd get svc
```

Note the NodePort (example: `31148`) or external IP. Then log in with the CLI, replacing `<NODEPORT>` with the correct host:port (e.g., `localhost:31148`):

```bash theme={null}
argocd login localhost:31148
```

The login flow may prompt:

* A TLS certificate verification warning (if the server uses a self-signed cert)
* Username (commonly `admin` unless changed)
* Password

> **warning** If the server uses a self-signed certificate, argocd will warn that the certificate is signed by an unknown authority. You can proceed insecurely by answering `y` to the prompt, but for production environments configure TLS correctly to avoid security risks.

On successful login you should see:

```text theme={null}
'admin:login' logged in successfully
Context 'localhost:31148' updated
```

Now retry:

```bash theme={null}
argocd app list
```

Example output for one existing app:

```text theme={null}
NAME                      CLUSTER                         NAMESPACE          PROJECT  STATUS  HEALTH   SYNCPOLICY  CONDITIONS  REPO                                              PATH       TARGET
argocd/highway-animation  https://kubernetes.default.svc  highway-animation  default  Synced  Healthy  Manual      <none>      http://host.docker.internal:5000/kk-org/capa-demos  ./vanilla  HEAD
```

## 3. Create a new application using the CLI

Create a new application (`app-2`) that points to the same repository and path as the existing app but targets a different namespace (`app-2`):

```bash theme={null}
argocd app create app-2 \
  --repo http://host.docker.internal:5000/kk-org/capa-demos \
  --path ./vanilla \
  --dest-namespace app-2 \
  --dest-server https://kubernetes.default.svc
```

Expected response:

```text theme={null}
application 'app-2' created
```

List applications again:

```bash theme={null}
argocd app list
```

Because the repository path is shared with another application, Argo CD may report shared resources and mark the new app as OutOfSync. Example output:

```text theme={null}
NAME                       CLUSTER                         NAMESPACE  PROJECT  STATUS     HEALTH   SYNCPOLICY   CONDITIONS                      REPO                                              PATH
argocd/app-2               https://kubernetes.default.svc  app-2      default  OutOfSync  Healthy  Manual       SharedResourceWarning(2)         http://host.docker.internal:5000/kk-org/capa-demos  ./vanilla
argocd/highway-animation   https://kubernetes.default.svc  highway-animation  default  Synced  Healthy  Manual   <none>                       http://host.docker.internal:5000/kk-org/capa-demos  ./vanilla  HEAD
```

## 4. Create the destination namespace (if needed)

If the destination namespace `app-2` does not exist, create it with kubectl:

```bash theme={null}
kubectl create ns app-2
# namespace/app-2 created
```

## 5. Synchronize the application

Sync the newly created application to apply the manifests to the cluster:

```bash theme={null}
argocd app sync app-2
```

During sync the CLI prints resource-level events and a summary. Example output:

```text theme={null}
TIMESTAMP                           GROUP   KIND        NAMESPACE  NAME                          STATUS     HEALTH    HOOK  MESSAGE
2025-10-23T10:32:26+00:00           v1      Service     app-2      highway-animation-service      OutOfSync  Healthy
2025-10-23T10:32:26+00:00           apps    Deployment  app-2      highway-animation              OutOfSync  Healthy
2025-10-23T10:32:27+00:00           v1      Service     app-2      highway-animation-service      Synced     Healthy   service/highway-animation-service configured
2025-10-23T10:32:28+00:00           apps    Deployment  app-2      highway-animation              Synced     Healthy   deployment.apps/highway-animation configured

Name:        argocd/app-2
Project:     default
Server:      https://kubernetes.default.svc
Namespace:   app-2
URL:         https://localhost:31148/applications/app-2
Source:
- Repo: http://host.docker.internal:5000/kk-org/capa-demos
  Path: ./vanilla
SyncWindow:  Sync Allowed
Sync Policy: Manual
Sync Status: Synced to (0c48696)
Health Status: Healthy
```

After the sync completes the application should appear as Synced / Healthy. Verify via the UI or with:

```bash theme={null}
argocd app list
```

## Troubleshooting and best practices

* Use unique resource names and namespaces when multiple Argo CD applications reference the same repository to avoid SharedResourceWarning.
* Prefer overlays, separate paths, or separate repositories when deploying distinct environments.
* For production, configure proper TLS certificates rather than accepting self-signed certificates.

> **lightbulb** If multiple Argo CD applications point to the same manifests and overlap resources (same names/namespaces), Argo CD raises SharedResourceWarning. Avoid conflicts by using distinct repository paths, kustomize overlays, or separate namespaces and repositories.

This completes the demo for creating and synchronizing an Argo CD application using the CLI. For more examples and advanced workflows, see the [Argo CD CLI reference](https://argo-cd.readthedocs.io/en/stable/cli_operations/).

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/ea24d846-8c67-457a-88d8-26a0873c94c7)


# Demo Create and Test ArgoCD Project

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Create-and-Test-ArgoCD-Project/page

Creating and testing ArgoCD projects to restrict source repositories destinations Kubernetes kinds, manage roles and tokens, and observe how project-level policies affect application creation and synchronization.

In this lesson you'll create a new ArgoCD Project, restrict what applications in that project may do, and observe how those project-level restrictions affect application creation and synchronization.

What you'll learn

* What an ArgoCD Project is and why it matters
* How to restrict source repositories, cluster destinations, and Kubernetes kinds
* How to create project roles and short-lived tokens
* How to test a restricted project by creating and syncing an application

Relevant links and references

* [Argo CD documentation — Projects](https://argo-cd.readthedocs.io/en/stable/operator-manual/project/)
* [Kubernetes API concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

## What is a Project?

A Project is a logical grouping of applications in ArgoCD. Projects scope what applications in that group are allowed to use — including which Git repos they can pull from, which cluster destinations and namespaces they can deploy to, and which Kubernetes API kinds they may create. Use projects to enforce team boundaries and reduce blast radius (for example, disallow non-operator teams from creating cluster-scoped resources like ClusterRole).

> **warning** ArgoCD ships with a `default` project that is highly permissive (it can pull from any repository, deploy to any destination, and create cluster-level resources). You can modify the `default` project but you cannot delete it.

## Default / Permissive Project Behavior

A very permissive project specification (the typical default after fresh install):

```yaml theme={null}
spec:
  sourceRepos:
  - '*'
  destinations:
  - namespace: '*'
    server: '*'
```

To allow cluster-scoped resources by default, a project can include a cluster resource allow list:

```yaml theme={null}
spec:
  sourceRepos:
  - '*'
  destinations:
  - namespace: '*'
    server: '*'
  clusterResourceWhitelist:
  - group: '*'
    kind: '*'
```

## Key Project Fields (at a glance)

| Field                                               | Purpose                                         | Example                                                           |
| --------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------- |
| sourceRepos                                         | Whitelist/deny repositories the project can use | `- 'https://github.com/example/*'`                                |
| destinations                                        | Allowed server URL and namespace pairs          | `- namespace: 'default' server: 'https://kubernetes.default.svc'` |
| clusterResourceWhitelist / clusterResourceBlacklist | Allow or deny specific cluster-scoped API kinds | `- group: rbac.authorization.k8s.io kind: ClusterRole`            |
| roles                                               | Define project-level roles and policies         | `argocd proj role create`                                         |

## Controlling Allowed and Denied Repositories

You control repository access with `sourceRepos`. Patterns may be negated using a leading `!` to explicitly deny matches.

CLI examples to add/remove repository patterns:

```bash theme={null}
argocd proj add-source <PROJECT> <REPO>
argocd proj remove-source <PROJECT> <REPO>
