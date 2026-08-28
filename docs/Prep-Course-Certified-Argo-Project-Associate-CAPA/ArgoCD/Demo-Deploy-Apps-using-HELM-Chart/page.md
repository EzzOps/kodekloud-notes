# To add or remove a denied (negated) source:
argocd proj add-source <PROJECT> !<REPO>
argocd proj remove-source <PROJECT> !<REPO>
```

Example YAML using negation patterns:

```yaml theme={null}
spec:
  sourceRepos:
  # Do not use the test repo in argoproj
  - '!ssh://git@github.com:argoproj/test'
  # Nor any GitLab repo under group/
  - '!https://gitlab.com/group/**'
  # Any other repo is fine though
  - '*'
```

## Controlling Destinations and Namespaces

Destination entries define allowed (or denied) server/namespace pairs. You can negate `namespace` or `server` with a `!` prefix:

```yaml theme={null}
spec:
  destinations:
  # Do not allow any app to be installed in `kube-system`
  - namespace: '!kube-system'
    server: '*'
  # Do not allow any cluster whose server URL matches team1-*
  - namespace: '*'
    server: '!http://team1-*'
  # Any other namespace or server is allowed
  - namespace: '*'
    server: '*'
```

If a project has no allowed destinations configured, application creation will fail with an InvalidSpecError.

## Project Roles and Tokens

Projects can define roles and issue short-lived tokens bound to those roles. Tokens are useful for automation or cross-team access with limited scope.

Typical workflow:

```bash theme={null}
PROJ=myproject
APP=guestbook-default
ROLE=get-role

# Create role
argocd proj role create $PROJ $ROLE

# Create a token for the role, expires in 10 minutes
argocd proj role create-token $PROJ $ROLE -e 10m
# List and inspect role
argocd proj role list $PROJ
argocd proj role get $PROJ $ROLE

# Trying to access the app will fail until the role is granted permissions:
argocd app get $APP --auth-token $JWT

# Grant the role permission to get the specific application
argocd proj role add-policy $PROJ $ROLE --action get --permission allow --object $APP
argocd app get $APP --auth-token $JWT

# Modify policies to use a wildcard (grant access to all apps)
argocd proj role remove-policy $PROJ $ROLE -a get -o $APP
argocd proj role add-policy $PROJ $ROLE -a get --permission allow -o '*'
argocd app get $APP --auth-token $JWT

# Revoke the token when done
argocd proj role delete-token $PROJ $ROLE <token-id>
# The token no longer works:
argocd app get $APP --auth-token $JWT
```

## Sync Windows and Global Project Mapping

Projects can be referenced by selectors and sync windows can be applied globally by mapping applications (by label selectors) to a project.

Example that matches apps labeled `opt: prod` and maps them to `proj-global-test`:

```yaml theme={null}
- labelSelector:
    matchExpressions:
    - key: opt
      operator: In
      values:
      - prod
  projectName: proj-global-test
```

ConfigMap snippet that might be stored in ArgoCD settings:

```yaml theme={null}
data:
  globalProjects: |-
    - labelSelector:
        matchExpressions:
        - key: opt
          operator: In
          values:
          - prod
      projectName: proj-global-test
kind: ConfigMap
```

## UI: Viewing and Editing Projects

In the ArgoCD UI navigate to Settings → Projects to view and edit projects. The UI shows project fields such as allowed source repositories, destinations, cluster resource allow/deny lists, roles, and sync windows.

<Frame>
  <img alt="A web UI screenshot of the Argo CD Projects settings page showing the &#x22;deny&#x22; project summary with general info (name &#x22;deny&#x22;, 0 applications), source repositories set to &#x22;*&#x22; and no scoped repositories. The top has buttons to add roles/sync windows or delete, and a left navigation pane lists Settings, User Info and Documentation." />
</Frame>

<Callout icon="lightbulb">
  The UI in this environment auto-saves project edits, so you may not see an explicit "Save" button after changes.
</Callout>

## Creating a Restricted Project (example)

We'll create a project named `deny` and restrict it so users in that project cannot create ClusterRole resources. This is achieved by adding an entry to the project's cluster resource denial list for kind `ClusterRole` in the `rbac.authorization.k8s.io` API group.

Testing approach

1. Create or update the `deny` project to include a rule that denies ClusterRole.
2. Create an application in the `deny` project whose repository includes a Deployment, Service, and a ClusterRole manifest.
3. Attempt to sync the application and observe the sync failure caused by the denied ClusterRole.

Note: if the project does not allow your desired destination (server/namespace), application creation will fail — update the project's destinations first, then create the app.

### Create the application (CLI example)

```bash theme={null}
argocd app create testing-project \
  --repo http://host.docker.internal:5000/kk-org/pod-metadata \
  --path ./manifests \
  --dest-namespace default \
  --project deny \
  --dest-server https://kubernetes.default.svc
```

Example repository manifest (one file under ./manifests):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
  namespace: highway-animation
spec:
  replicas: 1
  selector:
    matchLabels:
      app: highway-animation
  template:
    metadata:
      labels:
        app: highway-animation
    spec:
      containers:
      - name: highway-animation
        image: siddharth67/highway-animation:blue
        ports:
        - containerPort: 3000
        env:
        - name: POD_COUNT
          value: "1"
```

If the project lacks a matching destination, you'll see an error similar to:

```text theme={null}
{"level":"fatal","msg":"rpc error: code = InvalidArgument desc = application spec for testing-project is invalid: InvalidSpecError: application destination server 'https://kubernetes.default.svc' and namespace 'default' do not match any of the allowed destinations in project 'deny'"}
```

To resolve that, add an appropriate destination entry to the `deny` project (for testing you can allow the cluster/namespace you intend to use) and re-run the `argocd app create` command.

Once the app is created, it will appear in the ArgoCD UI with its sync and health status.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing three application cards (app-2, highway-animation, testing-project) with status badges and Sync/Refresh/Delete buttons. The left sidebar shows navigation and filters for sync and health status." />
</Frame>

## Attempting to Synchronize the Application

Try synchronizing the `testing-project` application. Because the repository contains a ClusterRole manifest and the `deny` project blocks ClusterRole creation, synchronization will fail and the UI will indicate the blocked resource(s).

When you click Synchronize in the UI, the operation will fail and report that the ClusterRole (rbac.authorization.k8s.io) is not permitted by the project's rules.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing an application called &#x22;testing-project&#x22; marked OutOfSync on the left. The right side displays a &#x22;Synchronize&#x22; dialog with various sync options and resource checkboxes." />
</Frame>

The sync failure details clearly show the ClusterRole was blocked by the project's cluster resource denial list.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing an application sync that failed, with the message &#x22;one or more synchronization tasks are not valid.&#x22; The result pane shows an rbac.authorization.k8s.io ClusterRole resource was blocked (not permitted) during the sync." />
</Frame>

Because a disallowed resource prevented synchronization, the application tree will show no resources were successfully applied.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the &#x22;testing-project&#x22; application marked OutOfSync with a &#x22;Sync failed&#x22; status. The application tree on the right lists resources like pod-metadata-service, pod-metadata-deployment, and pod-master." />
</Frame>

## Troubleshooting Tips

* If application creation fails with InvalidSpecError, confirm the project's `destinations` include the requested `server` and `namespace`.
* If sync fails and the UI shows a blocked resource, check the project's [SECRET_REDACTED] for the resource's API group/kind.
* Use `argocd proj role list` and `argocd proj role get` to debug role and policy settings when tokens fail.

## Summary

* Projects let you scope repositories, cluster destinations, and permitted Kubernetes kinds for applications.
* Use projects to enforce team boundaries and reduce blast radius (e.g., prevent non-operators from creating ClusterRole).
* Manage projects via the CLI or UI, create project-level roles and tokens, and define sync windows and selectors for global project mapping.

That's all for now.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/6f0d0dba-4dab-49c1-9f6f-62b480160bae" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/0d4320f9-7a40-42de-971e-121e81468411" />
</CardGroup>


# Demo Deploy Apps using HELM Chart

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Deploy-Apps-using-HELM-Chart/page

Guide to deploying Helm charts with Argo CD, explaining Helm-specific options, values override mechanisms, precedence, and examples using a simple random shapes chart.

In this lesson you'll learn how to deploy Helm charts with Argo CD and how Argo CD exposes Helm-specific options: value files, inline `values`, `valuesObject`, and Helm `parameters`. The examples use a simple Helm chart that renders a ConfigMap and a Deployment from chart defaults in `values.yaml`. You'll also see how Argo CD merges and applies overrides and the defined order of precedence.

## Argo CD Application spec (Helm)

A typical Argo CD Application that references a Helm chart includes Helm-specific fields under `spec.source.helm`. The minimal Application spec looks like this:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  # You'll usually want to add your resources to the argocd namespace.
  namespace: argocd
  # Add this finalizer ONLY if you want these to cascade delete.
  finalizers:
    # The default behaviour is foreground cascading deletion
    - resources-finalizer.argocd.argoproj.io
  labels:
    name: guestbook
spec:
  # The project the application belongs to.
  project: default

  # Source of the application manifests
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD    # If repoURL is a Git repo, this is branch/tag/commit. If repoURL is a Helm repo, this can be the chart version.
    path: guestbook         # Path inside the repo when using a Git source
```

Scroll to `spec.source.helm` to configure Helm-specific behavior. Argo CD accepts multiple ways to pass Helm values and options:

* `valueFiles`: list of values files (relative to `spec.source.path`)
* `values`: inline YAML block
* `valuesObject`: native key/value map (preferred over `values`)
* `parameters`: Helm name/value list (highest precedence)

Below are common Helm source options you'll use.

### Example: valueFiles / values / valuesObject

Use `valueFiles` to reference files in the chart directory (relative to `spec.source.path`). You can also provide `values` as an inline YAML document or `valuesObject` as a native map. `valuesObject` takes precedence over `values`.

```yaml theme={null}
