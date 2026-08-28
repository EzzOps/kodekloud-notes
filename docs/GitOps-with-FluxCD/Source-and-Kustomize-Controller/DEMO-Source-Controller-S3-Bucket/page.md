# List all registered sources
flux get sources

# Filter for Git sources
flux get sources git
# NAME         REVISION                READY   MESSAGE
# flux-system  main@sha1:edf2288f      True    stored artifact for revision 'main@sha1:edf2288f'
```

```bash theme={null}
# List Kustomizations
flux get kustomizations
# NAME         REVISION                READY   MESSAGE
# flux-system  main@sha1:edf2288f      True    Applied revision: main@sha1:edf2288f
```

## 3. Import and Clone the Demo Application

We’ll use a repository named `bb-app-source` containing both app code and Kubernetes manifests.

1. **Import into your GitHub account**

<Frame>
  ![The image shows a GitHub page for importing a project, with fields for the old repository's clone URL and new repository details, including options for public or private visibility. A "Begin import" button is highlighted.](https://kodekloud.com/kk-media/image/upload/v1752877693/notes-assets/images/GitOps-with-FluxCD-DEMO-Source-Controller-Git-Manifest-in-Flux-Repo/github-import-project-repository-page.jpg)
</Frame>

2. **Clone locally and switch to the demo branch**
   ```bash theme={null}
   git clone https://github.com/your-account/bb-app-source
   cd bb-app-source
   git checkout 1-demo
   ```

<Frame>
  ![The image shows a GitHub page indicating that a new repository import is complete, with a user menu open on the right side.](https://kodekloud.com/kk-media/image/upload/v1752877694/notes-assets/images/GitOps-with-FluxCD-DEMO-Source-Controller-Git-Manifest-in-Flux-Repo/github-repository-import-complete-user-menu.jpg)
</Frame>

## 4. Examine Application Source and Manifests

* **src/**: PHP app reporting its Pod and namespace.
* **manifests/1-demo/**: Contains three YAML definitions:
  * `deployment.yml`
  * `namespace.yml`
  * `service.yml`

<Frame>
  ![The image shows a GitHub repository page with a directory listing for "1-demo" containing three YAML files: deployment.yml, namespace.yml, and service.yml.](https://kodekloud.com/kk-media/image/upload/v1752877695/notes-assets/images/GitOps-with-FluxCD-DEMO-Source-Controller-Git-Manifest-in-Flux-Repo/github-repo-1-demo-yaml-files.jpg)
</Frame>

Here’s the `Deployment` snippet (`manifests/1-demo/deployment.yml`):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: block-buster
  namespace: 1-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: block-buster
      version: "7.1.0"
      env: dev
  template:
    metadata:
      labels:
        app: block-buster
        version: "7.1.0"
        env: dev
    spec:
      containers:
        - name: app
          image: siddharth67/block-buster-dev:7.1.0
          imagePullPolicy: Always
          resources:
            requests:
              memory: "10Mi"
              cpu: "10m"
            limits:
              memory: "20Mi"
              cpu: "50m"
```

## 5. Add Manifests to Your Flux Cluster Repo

Copy the demo manifests into your Flux cluster repository under `flux-clusters/dev-cluster/1-demo`:

```bash theme={null}
cp manifests/1-demo/*.yml \
   ../block-buster/flux-clusters/dev-cluster/1-demo/
cd ../block-buster/flux-clusters/dev-cluster/
git add 1-demo/*.yml
git commit -m "Add 1-demo manifests"
git push
```

Flux will detect these new files and begin applying them automatically.

## 6. Verify the GitOps Deployment

1. **Check Kubernetes namespaces**
   ```bash theme={null}
   kubectl get ns
   # NAME         STATUS   AGE
   # 1-demo       Active   30s
   # default      Active   49m
   # flux-system  Active   42m
   ```
2. **Confirm Flux has the latest revision**
   ```bash theme={null}
   flux get sources git
   flux get kustomizations
   ```

## 7. Inspect the Source Controller Cache

Dive into the Source Controller pod to view the cached repository archive:

```bash theme={null}
kubectl -n flux-system exec -it deploy/source-controller -- sh
cd data/gitrepository/flux-system/flux-system
ls -ltr
# latest.tar.gz -> ...cf1664a0b9...tar.gz
tar -tf latest.tar.gz
# flux-clusters/
# flux-clusters/dev-cluster/1-demo/deployment.yaml
# flux-clusters/dev-cluster/1-demo/namespace.yaml
# flux-clusters/dev-cluster/1-demo/service.yaml
exit
```

## 8. Access the Deployed Application

1. **List resources in the demo namespace**
   ```bash theme={null}
   kubectl -n 1-demo get all
   # pod/block-buster-...      1/1   Running   0   2m
   # service/block-buster-svc  NodePort  10.110.102.187  <none>  80:30001/TCP 2m
   ```
2. **Open the game in your browser**\
   [http://localhost:30001](http://localhost:30001)

<Frame>
  ![The image shows a web-based game interface called "Block Buster" with a notification indicating "Level 1 Completed." It includes game details like pod name, IP, namespace, and app version, with a simple game layout featuring a paddle and ball.](https://kodekloud.com/kk-media/image/upload/v1752877696/notes-assets/images/GitOps-with-FluxCD-DEMO-Source-Controller-Git-Manifest-in-Flux-Repo/block-buster-game-interface-level-1-completed.jpg)
</Frame>

This PHP-based game displays live pod metadata, demonstrating a full GitOps flow with Flux CD.

***

## Links and References

* [Flux CD Source Controller](https://fluxcd.io/docs/components/source/)
* [Flux CD Kustomize Controller](https://fluxcd.io/docs/components/kustomize/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [GitHub Repository Importing](https://docs.github.com/en/repositories/importing-repository-content)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/857e34cf-a086-433b-bf3b-88a5a5096a6f/lesson/d33d485b-ce5e-4b8b-afa2-790d05c9bbd6" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/857e34cf-a086-433b-bf3b-88a5a5096a6f/lesson/12f2f5ac-6a4d-4ad9-ae7f-38ae5ca23e3b" />
</CardGroup>


# DEMO Source Controller S3 Bucket

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Source-and-Kustomize-Controller/DEMO-Source-Controller-S3-Bucket/page

Leverage Flux’s Source Controller to fetch Kubernetes manifests from an S3-compatible store and deploy them via GitOps.

Leverage Flux’s Source Controller to fetch Kubernetes manifests from an S3-compatible store (MinIO) and deploy them via GitOps. In this walkthrough, you will:

* Set up a dedicated Git branch with demo manifests
* Deploy MinIO locally as an S3 replacement
* Create a bucket, upload manifests, and configure Flux sources
* Apply and verify your application in the cluster

***

## 1. Prepare the Demo Branch

Open your terminal in Visual Studio Code and switch to the `4-demo` branch of the `bb-app-source` repo:

```bash theme={null}
root ~/bb-app-source 3-demo
➤ git checkout 4-demo
Branch '4-demo' set up to track remote branch '4-demo' from 'origin'.
Switched to a new branch '4-demo'
root ~/bb-app-source 4-demo
➤
```

In this branch, the `4-demo` directory contains three manifests:

* `namespace.yml`
* `deployment.yml` (version **7.4.0**)
* `service.yml`

Example excerpt from **deployment.yml**:

```yaml theme={null}
env: dev
version: 7.4.0
spec:
  containers:
    - name: app
      image: siddharth67/block-buster-dev:7.4.0
      imagePullPolicy: Always
      resources:
        requests:
          memory: "10Mi"
          cpu: "10m"
        limits:
          memory: "64Mi"
          cpu: "20m"
```

***

## 2. Deploy MinIO as an S3-Compatible Store

Apply the MinIO manifest to create a namespace, pod, and service:

```bash theme={null}
root ~/bb-app-source 4-demo
▶ kubectl apply -f minio/minio-s3.yml
namespace/minio-dev created
pod/minio created
service/minio created
```

Verify the MinIO deployment:

```bash theme={null}
kubectl -n minio-dev get all
```

| NAME      | READY | STATUS  | AGE |
| --------- | ----- | ------- | --- |
| pod/minio | 1/1   | Running | 13s |

| NAME          | TYPE     | PORT(S)                        | AGE |
| ------------- | -------- | ------------------------------ | --- |
| service/minio | NodePort | 9000:30040/TCP, 9000:30041/TCP | 13s |

| Port  | Purpose                  |
| ----- | ------------------------ |
| 30040 | MinIO Web Console (HTTP) |
| 30041 | MinIO S3-compatible API  |

<Callout icon="lightbulb">
  By default, MinIO uses `minio-admin:minio-admin` for S3 authentication. Keep this credential secure in production.
</Callout>

***

## 3. Create a Bucket and Upload Manifests

1. Open the MinIO console at [http://localhost:30040](http://localhost:30040)

2. Authenticate with:
   * **Username:** `minio-admin`
   * **Password:** `minio-admin`

3. Create a bucket named **bucket-bb-app** using all defaults.

<Frame>
  ![The image shows a MinIO Object Store interface where a user is creating a new bucket with options for versioning, object locking, and quota settings. The sidebar includes various menu options like Access Keys, Documentation, and Settings.](https://kodekloud.com/kk-media/image/upload/v1752877697/notes-assets/images/GitOps-with-FluxCD-DEMO-Source-Controller-S3-Bucket/minio-object-store-new-bucket-interface.jpg)
</Frame>

4. In the Object Browser, select **bucket-bb-app**.

<Frame>
  ![The image shows a MinIO Object Store interface with a bucket named "bucket-bb-app" that has no usage or objects. The sidebar includes options like Object Browser, Access Keys, and Settings.](https://kodekloud.com/kk-media/image/upload/v1752877699/notes-assets/images/GitOps-with-FluxCD-DEMO-Source-Controller-S3-Bucket/minio-object-store-bucket-bb-app.jpg)
</Frame>

5. Create a folder called **app740** and upload `namespace.yml`, `deployment.yml`, and `service.yml` from your local `bb-app-source/4-demo` folder.

<Frame>
  ![The image shows a MinIO Object Store interface with an open file explorer window displaying folders on a local drive.](https://kodekloud.com/kk-media/image/upload/v1752877701/notes-assets/images/GitOps-with-FluxCD-DEMO-Source-Controller-S3-Bucket/minio-object-store-file-explorer.jpg)
</Frame>

6. Confirm all three manifests appear under `bucket-bb-app/app740/`.

<Frame>
  ![The image shows a web interface of an object storage browser with a bucket named "bucket-bb-app" containing three YAML files: deployment.yml, namespace.yml, and service.yml. A sidebar on the left displays various menu options, and a download/upload status window is visible on the right.](https://kodekloud.com/kk-media/image/upload/v1752877702/notes-assets/images/GitOps-with-FluxCD-DEMO-Source-Controller-S3-Bucket/object-storage-browser-bucket-bb-app.jpg)
</Frame>

***

## 4. Create a Flux Bucket Source

Instead of Git, Flux will track this S3 bucket via the **Bucket** API. Generate the source manifest and export it to your cluster repo:

```bash theme={null}
flux create source bucket 4-demo-source-minio-s3-bucket-bb-app \
  --bucket-name bucket-bb-app \
  --endpoint minio.minio-dev.svc.cluster.local:9000 \
  --provider generic \
  --secret-ref minio-crds \
  --insecure \
  --interval 1m \
  --export > ../block-buster/flux-clusters/dev-cluster/4-demo-source-minio-s3-bucket-bb-app.yml
```

Generated **Bucket** resource:

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: Bucket
metadata:
  name: 4-demo-source-minio-s3-bucket-bb-app
  namespace: flux-system
spec:
  bucketName: bucket-bb-app
  endpoint: minio.minio-dev.svc.cluster.local:9000
  provider: generic
  insecure: true
  secretRef:
    name: minio-crds
  interval: 1m0s
```

***

## 5. Create a Flux Kustomization

Point your Kustomization at the `app-740` folder in the bucket:

```bash theme={null}
flux create kustomization 4-demo-kustomize-minio-s3-bucket-bb-app \
  --source Bucket/4-demo-source-minio-s3-bucket-bb-app \
  --path ./app-740 \
  --prune=true \
  --target-namespace 4-demo \
  --interval 1m \
  --export > ../block-buster/flux-clusters/dev-cluster/4-demo-kustomization-minio-s3-bucket-bb-app.yml
```

Generated **Kustomization**:

```yaml theme={null}
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: 4-demo-kustomize-minio-s3-bucket-bb-app
  namespace: flux-system
spec:
  sourceRef:
    kind: Bucket
    name: 4-demo-source-minio-s3-bucket-bb-app
  path: ./app-740
  prune: true
  targetNamespace: 4-demo
  interval: 1m0s
```

***

## 6. Create the MinIO Credentials Secret

Flux requires a Kubernetes secret for S3 access. First, confirm Flux sees no secret:

```bash theme={null}
flux get sources bucket
```

Create `minio-crds` in the `flux-system` namespace:

```bash theme={null}
kubectl -n flux-system create secret generic minio-crds \
  --from-literal=accesskey=minioadmin \
  --from-literal=secretkey=minioadmin
```

Reconcile and verify:

```bash theme={null}
flux reconcile source bucket 4-demo-source-minio-s3-bucket-bb-app
flux get sources bucket
