# root ~/bb-app-source 7-demo [?]
```

***

## 2. Inspect the Infrastructure Branch

All MySQL manifests and namespace definitions reside in the `infrastructure` branch under the `database/` directory:

```bash theme={null}
git checkout infrastructure
ls
# bitnami-sealed-secrets/  cert-manager/  database/  ingress-nginx/  block-buster-helm-app-7.7.1.tgz
```

Inside `database/`, you’ll find:

* `namespace.yaml`
* `configmap.yaml`
* `secret.yaml`
* `deployment.yaml`
* `service.yaml`
* PersistentVolume and PersistentVolumeClaim manifests

```yaml theme={null}
# database/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-mysql
  namespace: database
stringData:
  password: mysql-password-0123456789
```

<Callout icon="triangle-alert">
  Storing passwords in plain text is insecure. Use sealed-secrets or another secret management solution for production environments.
</Callout>

***

## 3. Create a Flux GitRepository Source

Define a `GitRepository` resource in your Flux cluster repo (`flux-clusters/dev-cluster`) to track the `infrastructure` branch:

```yaml theme={null}
# infra-source-git.yml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: infra-source-git
  namespace: flux-system
spec:
  interval: 1m0s
  url: https://github.com/sidd-harth-2/bb-app-source
  ref:
    branch: infrastructure
```

Export it with the Flux CLI:

```bash theme={null}
cd ~/block-buster/flux-clusters/dev-cluster
flux create source git infra-source-git \
  --url https://github.com/sidd-harth-2/bb-app-source \
  --branch infrastructure \
  --timeout 10s \
  --export > infra-source-git.yml
```

***

## 4. Create a Flux Kustomization

Use a Kustomization to apply resources under `database/`:

```yaml theme={null}
# infra-database-kustomize-git-mysql.yml
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: infra-database-kustomize-git-mysql
  namespace: flux-system
spec:
  interval: 1m40s
  path: ./database
  prune: true
  sourceRef:
    kind: GitRepository
    name: infra-source-git
  targetNamespace: database
```

Generate via:

```bash theme={null}
flux create kustomization infra-database-kustomize-git-mysql \
  --source GitRepository/infra-source-git \
  --path ./database \
  --prune true \
  --target-namespace database \
  --interval 100s \
  --export > infra-database-kustomize-git-mysql.yml
```

Commit and push both manifests:

```bash theme={null}
git add infra-source-git.yml infra-database-kustomize-git-mysql.yml
git commit -m "Add MySQL DB source and kustomization"
git push
```

***

## 5. Reconcile and Verify

Force Flux to apply changes immediately:

```bash theme={null}
flux reconcile source git infra-source-git
flux reconcile kustomization infra-database-kustomize-git-mysql
```

Check that the `database` namespace is created:

```bash theme={null}
kubectl get ns
# NAME        STATUS   AGE
# database    Active   <age>
```

Inspect Flux sources and kustomizations:

```bash theme={null}
flux get sources git infra-source-git
flux get kustomizations infra-database-kustomize-git-mysql
```

Verify MySQL resources in `database` namespace:

```bash theme={null}
kubectl -n database get all,cm,secret
# NAME                                READY   STATUS    RESTARTS   AGE
# pod/mysql-xxxxxxxxxx-xxxxx          1/1     Running   0          <age>
# service/mysql                       ClusterIP 10.96.x.x 3306/TCP    <age>
# deployment.apps/mysql               1/1       Available   0        <age>
#
# NAME                             AGE
# configmap/mysql-initdb-config    <age>
# secret/secret-mysql              <age>
```

The MySQL database is now up and running! Next, we’ll pull the PHP application image from an OCI registry and deploy it with Flux.

***

## Flux Resources Overview

| Resource Type | Purpose                                  | Flux CLI Example                                                                                             |
| ------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| GitRepository | Track changes in a Git repo              | `flux create source git infra-source-git --url <repo> --branch infrastructure`                               |
| Kustomization | Apply and manage manifests via Kustomize | `flux create kustomization infra-database --source GitRepository/infra-source-git --path ./database --prune` |

***

## Links and References

* [Flux GitRepository Documentation](https://fluxcd.io/docs/components/source/git/)
* [Flux Kustomization Documentation](https://fluxcd.io/docs/components/kustomize/)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [MySQL Official Docs](https://dev.mysql.com/doc/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/205ec7c7-4cb6-4ecb-9bb5-fa50419f1e68/lesson/938cb579-768a-48b1-8184-3fe116c36db3" />
</CardGroup>


# HELM Controller

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Helm-Controller-and-OCI-Registry/HELM-Controller/page

This guide covers the Flux Helm Controller and its role in managing Helm charts within a GitOps workflow.

In this guide, we’ll dive into the Flux Helm Controller and its interaction with the Source Controller to manage Helm charts in a GitOps workflow. You’ll learn how to fetch Helm artifacts, define `HelmRelease` resources, and understand the responsibilities of the Helm Controller.

## Source Controller: Fetching Helm Charts

The Source Controller in Flux can retrieve Helm charts from multiple source types and package them as tarballs or YAML index files. Common source types include Git repositories, OCI registries, S3 buckets, and Helm repositories (e.g., Bitnami, Artifactory).

| Source Type    | Description                    | Format           | Example Provider          |
| -------------- | ------------------------------ | ---------------- | ------------------------- |
| GitRepository  | Charts stored in Git           | `.tar.gz`        | GitHub, GitLab            |
| HelmRepository | Official Helm chart repos      | YAML index files | Bitnami, Artifactory      |
| OCI Registry   | OCI-compliant chart registry   | OCI artifacts    | GitHub Container Registry |
| S3 Bucket      | Charts in cloud object storage | `.tar.gz`        | AWS S3, MinIO             |

Register your sources using `flux create source`:

```bash theme={null}
