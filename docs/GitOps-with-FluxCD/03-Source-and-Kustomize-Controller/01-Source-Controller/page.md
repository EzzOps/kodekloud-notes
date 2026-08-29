# Source Controller

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Source-and-Kustomize-Controller/Source-Controller/page

Flux’s Source Controller fetches artifacts from external sources and makes them available within your cluster for other controllers to consume.

Flux’s **Source Controller** provides a unified interface for fetching artifacts from external sources—such as Git repositories, OCI registries, object storage buckets, and Helm chart repositories—and making them available within your cluster for other controllers to consume.

## Supported Source Types

| Source Type     | Use Case                             | Flux Resource    |
| --------------- | ------------------------------------ | ---------------- |
| Git             | Kubernetes manifests and Helm charts | `GitRepository`  |
| OCI registry    | OCI artifacts (images, charts)       | `OCIRepository`  |
| Object storage  | Artifacts in S3/Azure/GCS buckets    | `Bucket`         |
| Helm chart repo | Helm charts                          | `HelmRepository` |

When you bootstrap Flux, it creates (or connects to) a `GitRepository` in the `flux-system` namespace to store Flux’s own configuration in a GitOps style. To list all configured Git sources:

```bash theme={null}
flux get sources git
```

***

## 1. Creating a GitRepository Source

Assume you have a GitHub repository `sidd-harth/app1` containing two manifest files at commit `1b31558`. To have Flux fetch these manifests every 10 seconds, run:

```bash theme={null}
flux create source git source-app1 \
  --url https://github.com/sidd-harth/app1 \
  --branch main \
  --interval 10s \
  --export > source-app1.yaml
```

This generates **source-app1.yaml**:

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: source-app1
  namespace: flux-system
spec:
  url: https://github.com/sidd-harth/app1
  ref:
    branch: main
  interval: 10s
```

Apply it to your cluster:

```bash theme={null}
kubectl apply -f source-app1.yaml
```

> **triangle-alert** If your repository is private, create a Kubernetes `Secret` with authentication credentials and reference it in the `spec.secretRef` field of the `GitRepository`.

***

## 2. Verifying the Source

After a short interval, Flux will clone the repo and store its contents as an artifact. Check status with:

```bash theme={null}
flux get sources git
```

Example output:

```text theme={null}
NAME          REVISION        SUSPENDED  READY  MESSAGE
flux-system   main/7e35678     False      True   stored artifact revision 'main/7e35678...'
source-app1   main/1b31558     False      True   stored artifact revision 'main/1b31558...'
```

* **REVISION**: Git reference and commit hash
* **READY**: Indicates whether the artifact is successfully stored

***

## 3. Inspecting Fetched Artifacts

Flux stores fetched artifacts under the Source Controller’s data directory. Exec into the Source Controller pod:

```bash theme={null}
kubectl -n flux-system exec -it deployment/source-controller -- sh
cd data/gitrepository/flux-system/source-app1
ls
```

You should see a `latest.tar.gz` file containing your manifests at the most recent revision.

To list its contents:

```bash theme={null}
tar -tf latest.tar.gz
