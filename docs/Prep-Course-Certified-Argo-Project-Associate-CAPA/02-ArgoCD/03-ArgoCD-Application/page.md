# ArgoCD Application

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/ArgoCD-Application/page

Overview of the Argo CD Application resource, creation methods, manifest fields, sync policies and best practices for implementing GitOps deployments to Kubernetes clusters.

Understanding the Argo CD Application resource is essential for implementing GitOps workflows with Argo CD. An Application is a Kubernetes custom resource (CR) that describes a deployed software instance — the desired state (manifests, charts, kustomize overlays, etc.) and where to apply it. Argo CD then continuously reconciles the live cluster to match this desired state.

Key concepts:

* GitOps: store desired state in Git and let Argo CD sync it to clusters.
* Application: the CR that binds a source (Git/Helm/Plugins) to a destination (cluster + namespace).
* Sync Policy: controls automated sync, pruning, and self-healing behavior.

## How to create an Argo CD Application

You can create an Application using:

* argocd CLI
* a Kubernetes YAML manifest applied with kubectl
* the Argo CD web UI

Example: create an application from a Git repository using the CLI

```bash theme={null}
argocd app create color-app \
  --repo https://github.com/sid/app-1.git \
  --path team-a/color-app \
  --dest-namespace color \
  --dest-server https://kubernetes.default.svc
```

After creation, Argo CD can automatically synchronize manifests from the Git repository to the configured destination cluster and namespace.

## Example Application manifest

This YAML corresponds to the CLI example above. It shows common fields and an automated sync policy.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: color-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/sid/app-1.git'
    targetRevision: HEAD
    path: team-a/color-app
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: color
  syncPolicy:
    automated:
      prune: false
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Manifest fields (reference)

| Field                              | Purpose                                       | Notes / Example                                 |
| ---------------------------------- | --------------------------------------------- | ----------------------------------------------- |
| metadata.name                      | Name of the Application resource              | e.g., `color-app`                               |
| metadata.namespace                 | Namespace where Argo CD is installed          | commonly `argocd`                               |
| spec.project                       | The Argo CD Project that owns the Application | Projects can enforce allowed repos/destinations |
| spec.source.repoURL                | Git repository containing manifests           | e.g., `https://github.com/sid/app-1.git`        |
| spec.source.targetRevision         | Git branch/tag/commit to use                  | e.g., `HEAD`, `main`, `v1.0.0`                  |
| spec.source.path                   | Path in repo to manifests or chart            | e.g., `team-a/color-app`                        |
| spec.destination.server            | Kubernetes API server to deploy to            | `https://kubernetes.default.svc` for in-cluster |
| spec.destination.namespace         | Target namespace in destination cluster       | e.g., `color`                                   |
| spec.syncPolicy.automated.selfHeal | Auto-rollback manual changes in cluster       | `true` to enforce Git state                     |
| spec.syncPolicy.automated.prune    | Remove resources not in Git during sync       | `true` to enable pruning                        |
| spec.syncPolicy.syncOptions        | Extra sync options                            | e.g., `CreateNamespace=true`                    |

## Source vs Destination

* Source: where Argo CD reads the desired state from — can be plain YAML, Helm charts, Kustomize overlays, Jsonnet, or custom plugins. The Application's source block points Argo CD to the correct repo/path/revision and triggers rendering as needed.
* Destination: the Kubernetes cluster and namespace where resources are applied. The destination.server can reference the in-cluster API (`https://kubernetes.default.svc`) or an external cluster registered in Argo CD.

## Sync policies and options

* Automated sync: instructs Argo CD to apply changes in Git automatically.
* Self-heal: when enabled, Argo CD will revert out-of-band (manual) changes on cluster resources to match Git.
* Prune: if enabled, resources that no longer exist in the Git source will be deleted from the cluster on sync.
* CreateNamespace: a syncOption that tells Argo CD to create the target namespace if missing (requires proper RBAC).

<Callout icon="lightbulb">
  When using automated sync and CreateNamespace, ensure Argo CD's ServiceAccount has sufficient RBAC permissions to create namespaces and manage the required resource types in the destination cluster. For multi-cluster setups, confirm projects restrict allowed destinations to avoid accidental deployments.
</Callout>

## Best practices and cautions

* Use Argo CD Projects to limit the repositories and clusters an Application can target.
* Test automated sync and pruning in non-production environments before enabling in production.
* Use branch/tag commit pins (targetRevision) for predictable deployments.
* Ensure secrets and credentials (to clusters, registries) are stored securely and referenced via Argo CD mechanisms (Secrets, SSO integrations, or external secret stores).

<Callout icon="warning">
  Be cautious with automated sync and pruning in production clusters. Misconfigured paths, overly permissive projects, or insufficient RBAC checks can lead to unintended deletions or rollbacks.
</Callout>

## Links and references

* Argo CD official docs: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/) or [https://argo-cd.readthedocs.io/en/stable/](https://argo-cd.readthedocs.io/en/stable/)
* Kubernetes concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* GitOps principles: [https://www.gitops.tech/](https://www.gitops.tech/)

This overview should help you create and manage Argo CD Application resources safely, with clear expectations for sync behavior and RBAC requirements.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/1c65a0f9-525f-4713-a804-5123eddb5d03" />
</CardGroup>
