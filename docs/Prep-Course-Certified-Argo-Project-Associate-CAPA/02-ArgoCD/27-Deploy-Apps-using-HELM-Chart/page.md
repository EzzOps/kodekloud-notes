# Output:
deployment.apps/random-shapes scaled
```

Listing pods shows scaled replicas being created:

```bash theme={null}
kubectl -n health-check get pods
# Example output:
NAME                                READY   STATUS              RESTARTS   AGE
random-shapes-9bb6bdfb8-5vpr7       0/1     ContainerCreating   0          26s
random-shapes-9bb6bdfb8-6vf7h       0/1     ContainerCreating   0          24s
random-shapes-9bb6bdfb8-chc6h       1/1     Running             0          18m
random-shapes-9bb6bdfb8-dx4mm       0/1     ContainerCreating   0          26s
random-shapes-9bb6bdfb8-fbs8s       0/1     ContainerCreating   0          25s
random-shapes-9bb6bdfb8-fmkpg       0/1     ContainerCreating   0          25s
random-shapes-9bb6bdfb8-gncmh       1/1     Running             0          26s
random-shapes-9bb6bdfb8-h8qvt       0/1     ContainerCreating   0          25s
random-shapes-9bb6bdfb8-md7rz       1/1     Running             1          65m
random-shapes-9bb6bdfb8-pppj7       0/1     ContainerCreating   0          25s
```

Without ignoreDifferences (or without RespectIgnoreDifferences enabled), Argo CD will detect the replica-count drift and scale the Deployment back to the declared replica count.

## How ignoreDifferences works

ignoreDifferences is a top-level field in the Application spec that tells Argo CD which differences to ignore when computing resource diffs. To ensure those ignored differences are honored during synchronization, enable the RespectIgnoreDifferences sync option.

You can specify the following in ignoreDifferences:

* jsonPointers: JSON Pointer(s) to fields to ignore (e.g., `/spec/replicas`).
* jqPathExpressions: JQ-style expressions to ignore fields (useful for ConfigMap `.data` keys).
* managedFieldsManagers: ignore changes that originate from specified object managers (e.g., `kube-controller-manager`).
* Optional `name` and `namespace` to scope the rule to a single resource.

| Field                 | Purpose                                | Example                     |
| --------------------- | -------------------------------------- | --------------------------- |
| jsonPointers          | Ignore explicit JSON paths             | `/spec/replicas`            |
| jqPathExpressions     | Ignore with JQ-like expressions        | `.data["config.yaml"].auth` |
| managedFieldsManagers | Ignore changes by a particular manager | `kube-controller-manager`   |
| name / namespace      | Scope rule to a single resource        | `name: random-shapes`       |

> **warning** ignoreDifferences only affects how Argo CD computes diffs and whether it treats a difference as actionable during sync. It does not change the live Kubernetes resource or stop other controllers (HPA, operators) from managing those fields.

## Example ignoreDifferences entries

Here are trimmed, relevant examples for common scenarios:

```yaml theme={null}
ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
      - /spec/replicas

  - kind: ConfigMap
    jqPathExpressions:
      - '.data["config.yaml"].auth'

  - group: "*"
    kind: "*"
    managedFieldsManagers:
      - kube-controller-manager
# Optional:
# name: my-deployment
# namespace: my-namespace
```

## Enable RespectIgnoreDifferences

> **lightbulb** To ensure Argo CD honors ignoreDifferences during synchronization, either:

  * Add "RespectIgnoreDifferences=true" to syncPolicy.syncOptions in your Application manifest, or
  * Select the "Respect differences" checkbox in the Argo CD UI sync dialog when performing a manual sync.

## Example: Application manifest snippet for this demo

This manifest shows automated sync with `selfHeal: true` and an ignoreDifferences entry that targets the `random-shapes` Deployment's `/spec/replicas` field. RespectIgnoreDifferences is included in syncOptions so automated syncs will honor the ignore rule.

```yaml theme={null}
project: default
source:
  repoURL: http://host.docker.internal:5000/kk-org/gitops-argocd-capa
  path: ./health-check
  targetRevision: HEAD

destination:
  server: https://kubernetes.default.svc
  namespace: health-check

syncPolicy:
  automated:
    prune: true
    selfHeal: true
    enabled: true
  syncOptions:
    - CreateNamespace=true
    - RespectIgnoreDifferences=true

ignoreDifferences:
  - group: apps
    kind: Deployment
    name: random-shapes
    namespace: health-check
    jsonPointers:
      - /spec/replicas
```

### UI option: Respect differences

When performing a manual synchronization from the Argo CD UI, you can enable "Respect differences" in the sync panel so Argo CD will honor ignoreDifferences rules during that sync.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the &#x22;health-check-app&#x22; with a resource graph and status indicators (App Health: Degraded, Sync Status: Synced). A synchronization panel on the right lists sync options and the selected resources to synchronize." />
</Frame>

## Demonstration: scale after configuring ignoreDifferences

1. Ensure the Application contains the ignoreDifferences entry (as shown above) and RespectIgnoreDifferences is enabled.
2. Scale the Deployment again:

```bash theme={null}
kubectl -n health-check scale deployment random-shapes --replicas=10
# Output:
deployment.apps/random-shapes scaled
```

3. After scaling and either manually syncing (with Respect differences enabled) or after an automated sync completes, Argo CD will not revert the replica count for the targeted Deployment because `/spec/replicas` is ignored for that resource. The pods created by the scale action will remain running.

## Summary

* Use ignoreDifferences to tell Argo CD to ignore specific fields, JQ expressions, or managed-field managers when computing diffs and deciding whether to sync.
* To make Argo CD actually honor those ignore rules during synchronization, enable RespectIgnoreDifferences in syncPolicy.syncOptions or enable "Respect differences" in the UI sync dialog.
* This pattern is useful for fields controlled externally by HPA or operators (replica counts, dynamic config keys, etc.), preventing Argo CD from continuously reverting externally-managed changes.

## Links and references

* [Argo CD Application spec — ignoreDifferences](https://argo-cd.readthedocs.io/en/stable/operator-manual/applications/#ignoredifferences)
* [Kubernetes Horizontal Pod Autoscaler (HPA) documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
* [Argo CD docs — Sync Options](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#sync-options)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/e8de4f85-17f9-46b5-8c5b-386db2e32870)


# Deploy Apps using HELM Chart

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Deploy-Apps-using-HELM-Chart/page

Using Argo CD to deploy and manage Helm charts for GitOps style declarative application delivery, including creating apps from Git or Helm repos and managing via CLI or UI.

In this lesson you'll learn how to deploy Helm charts with Argo CD and how Argo CD integrates with Helm to implement GitOps-style, declarative application delivery.

Helm is the Kubernetes package manager that packages applications as charts and defines them declaratively — a core principle of GitOps. Argo CD can deploy and continuously monitor Helm charts from several sources, including:

* a Git repository where the chart lives under a specific repo path, or
* a Helm chart repository (public or private), such as Bitnami or Artifactory.

For full reference:

* [Argo CD](https://argo-cd.readthedocs.io/)
* [Helm](https://helm.sh/)
* [Helm chart repository concept](https://helm.sh/docs/topics/chart_repository/)

## Typical Helm chart layout

A simple Helm chart directory looks like this:

```text theme={null}
─ helm-chart
  ├─ Chart.yaml
  ├─ templates
  │  ├─ NOTES.txt
  │  ├─ _helpers.tpl
  │  ├─ configmap.yaml
  │  ├─ deployment.yaml
  │  └─ service.yaml
  └─ values.yaml
```

What these files do:

| File / Folder           | Purpose                                                        |
| ----------------------- | -------------------------------------------------------------- |
| Chart.yaml              | Chart metadata (name, version, app version, description)       |
| templates/              | Kubernetes manifest templates rendered with values and helpers |
| templates/NOTES.txt     | Post-installation notes shown by helm CLI                      |
| templates/\_helpers.tpl | Helper template functions used by other templates              |
| values.yaml             | Default configuration values (can be overridden by Argo CD)    |

## How Argo CD consumes Helm charts

Argo CD treats Helm as a manifest generator: it renders chart templates (using provided values) and applies the generated Kubernetes manifests to the target cluster. You can reference Helm charts from:

* Git repository (chart files inside a repo path)
* Helm chart repository (using chart name and optional revision)

Below are step-by-step examples for both approaches.

## Create an Argo CD application from a Git repository

Steps:

1. Point Argo CD at the Git repository URL.
2. Set the repo path that contains the chart.
3. Optionally override chart values using `--helm-set` or a values file.

Example: create an application named `random-shapes` from the repo path `helm-chart`, overriding a few values:

```bash theme={null}
argocd app create random-shapes \
  --repo https://github.com/sidd-harth/test-cd.git \
  --path helm-chart \
  --helm-set replicaCount=2 \
  --helm-set color.circle=pink \
  --helm-set color.square=violet \
  --helm-set service.type=NodePort \
  --dest-namespace default \
  --dest-server https://kubernetes.default.svc
```

Expected CLI response:

```text theme={null}
application 'random-shapes' created
```

## Create an Argo CD application from a Helm chart repository

Steps:

1. Add the Helm chart repository to Argo CD (use `--type helm` for Helm repos).
2. Create an application referencing the chart name in that repo; optionally specify a chart revision and a values file.

Example: add the Bitnami chart repository to Argo CD, then create an application from the `nginx` chart at a specific revision:

```bash theme={null}
