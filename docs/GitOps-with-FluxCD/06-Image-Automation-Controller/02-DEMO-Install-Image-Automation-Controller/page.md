# Enter your Docker ID and password or access token
# Username: <your-dockerhub-username>
# Password: <your-password-or-access-token>
# Login Succeeded
```

> **lightbulb** For security, use a Docker Hub [access token](https://docs.docker.com/docker-hub/access-tokens/) instead of your account password.

***

## 2. Pull the Base Image

Fetch the pre-built Block Buster image from the original repository:

```bash theme={null}
docker pull siddharth67/block-buster-dev:7.8.0
# 7.8.0: Pulling from siddharth67/block-buster-dev
# Digest: sha256:cf54e2a9efad47898d8ae12a3956b2ce7dbc69f239a22804ee78f691
# Status: Image is up to date for docker.io/siddharth67/block-buster-dev:7.8.0
```

***

## 3. Retag and Push to Your Docker Hub

Tag the image under your own namespace and push:

```bash theme={null}
docker tag \
  siddharth67/block-buster-dev:7.8.0 \
  <your-username>/bb-app-flex-demo:7.8.0

docker push <your-username>/bb-app-flex-demo:7.8.0
# Pushing layers to <your-username>/bb-app-flex-demo
# latest: digest: sha256:cfc54e2a396562b2ce7dbc69f239a22804e78f691 size: 3662
```

> **triangle-alert** Replace `<your-username>` consistently. Never commit credentials or tokens into Git repositories.

After a successful push, confirm that the `bb-app-flex-demo` repository with tag `7.8.0` appears in your Docker Hub account.

***

## 4. Update the Kubernetes Deployment Manifest

Switch to the `8-demo` branch and edit the deployment to reference your image:

```bash theme={null}
cd ../bb-app-source/
git checkout 8-demo
```

Open `deployment.yaml` and update the container image:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blockbuster
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: blockbuster
  template:
    metadata:
      labels:
        app: blockbuster
    spec:
      containers:
        - name: app
          image: <your-username>/bb-app-flex-demo:7.8.0
          imagePullPolicy: Always
          resources:
            requests:
              memory: "10Mi"
              cpu:    "100m"
```

Commit and push your change:

```bash theme={null}
git add deployment.yaml
git commit -m "chore: update image to <your-username>/bb-app-flex-demo:7.8.0"
git push origin 8-demo
```

***

## 5. Deploy with Flux

In your Flux cluster repository, create a GitRepository source and Kustomization:

```bash theme={null}
cd ../block-buster/flux-clusters/dev-cluster

# Define the Git source tracking the 8-demo branch
flux create source git bb-app-source \
  --url https://github.com/sidd-harth-2/bb-app-source \
  --branch 8-demo \
  --interval 1m \
  --export > bb-app-source.yaml

# Create a Kustomization to apply manifests from the source
flux create kustomization bb-app-kustomize \
  --source GitRepository/bb-app-source \
  --path ./manifests \
  --prune true \
  --interval 1m \
  --target-namespace dev \
  --export > bb-app-kustomize.yaml

# Apply the Flux resources
kubectl apply -f bb-app-source.yaml
kubectl apply -f bb-app-kustomize.yaml
```

Trigger an immediate reconciliation and verify:

```bash theme={null}
flux reconcile source git flux-system
flux reconcile kustomization flux-system

kubectl get ns
# NAME           STATUS   AGE
# dev            Active   1m
kubectl -n dev get all
# Confirm the blockbuster Deployment, Service, Pod, etc.
```

***

## 6. Verify the Application

Point your browser to the NodePort (e.g., `localhost:30008`) and confirm the high score persistence in version 7.8.0:

![The image shows a screenshot of a block-breaking game called "Block Buster" with a "Game Over" message. The game interface includes colorful blocks, a paddle, and a ball, along with game information like score and lives.](https://kodekloud.com/kk-media/image/upload/v1752877642/notes-assets/images/GitOps-with-FluxCD-DEMO-Initialize-DockerHub/block-buster-game-over-screenshot.jpg)

***

You’ve now integrated Docker Hub with Kubernetes and automated your deployment using Flux GitOps. Next up: creating a `FluxRepository` to track image updates and automate version bumps.

## Links and References

* [Docker Hub Documentation](https://docs.docker.com/)
* [Flux GitOps](https://fluxcd.io/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/e4076c7b-6728-412c-b4d7-9316fc346fc5/lesson/8b4c829a-b3d6-4291-98ff-51fc8b52e6bf)


# DEMO Install Image Automation Controller

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Image-Automation-Controller/DEMO-Install-Image-Automation-Controller/page

This guide explains how to upgrade an existing Flux CD installation to include Image Reflector and Image Automation Controllers.

In this guide, you’ll upgrade an existing Flux CD installation to include both the **Image Reflector Controller** and the **Image Automation Controller**. By the end, you’ll verify new deployments, CRDs, and see the updated Git manifests.

***

## 1. Verify Existing Flux Controllers

Ensure you’re working in the `flux-system` namespace and list deployed controllers:

```bash theme={null}
kubectl -n flux-system get deployment
```

Expected output:

```plaintext theme={null}
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
helm-controller         1/1     1            1           18h
kustomize-controller    1/1     1            1           18h
notification-controller 1/1     1            1           18h
source-controller       1/1     1            1           18h
```

> **lightbulb** No image controllers appear yet. You’ll add them in Step 3.

***

## 2. List All Flux Sources

Check which source types are defined in your cluster:

```bash theme={null}
flux get sources all
```

Sample output:

```plaintext theme={null}
NAME                                           SUSPENDED  READY  MESSAGE
ocirepository/7-demo-source-oci-bb-app         False      True   stored artifact
bucket/4-demo-source-minio-s3-bucket-bb-app    False      False  bucket not found
gitrepository/2-demo-source-git-bb-app         False      True   stored artifact
gitrepository/3-demo-source-git-bb-app         False      True   stored artifact
gitrepository/5-demo-source-git-helm-bb-app    False      True   stored artifact
gitrepository/flux-system                      False      True   stored artifact
gitrepository/infra-source-git                 False      True   stored artifact
helmrepository/6-demo-source-helm-bb-app       False      True   stored artifact
```

This confirms you have all standard source types: **Git**, **Helm**, **OCI**, and **Bucket**.

***

## 3. Upgrade Flux to Include Image Controllers

Re-run the Flux bootstrap command with the `--components-extra` flag:

```bash theme={null}
flux bootstrap github \
  --owner=sidd-harth-2 \
  --repository=block-buster \
  --path=flux-clusters/dev-cluster \
  --personal=true \
  --private=false \
  --components-extra="image-reflector-controller,image-automation-controller"
```

> **triangle-alert** When prompted, paste your GitHub Personal Access Token.\
  Never share your token publicly or commit it to Git.

Flux will detect existing components and automatically upgrade to add the image controllers.

***

## 4. Confirm New Deployments and CRDs

### 4.1 Check Pods & Deployments

```bash theme={null}
kubectl -n flux-system get pod,deploy
```

Expected snippet:

```plaintext theme={null}
pod/image-automation-controller-xxxxx    1/1   Running   0   30s
pod/image-reflector-controller-xxxxx     1/1   Running   0   30s
...
deployment.apps/image-automation-controller  1/1  1  1  30s
deployment.apps/image-reflector-controller  1/1  1  1  30s
```

### 4.2 List Image CRDs

```bash theme={null}
kubectl get crds | grep image
```

```plaintext theme={null}
imagepolicies.image.toolkit.fluxcd.io
imagerepositories.image.toolkit.fluxcd.io
imageupdateautomations.images.toolkit.fluxcd.io
```

| CRD                                             | Description                           |
| ----------------------------------------------- | ------------------------------------- |
| imagepolicies.image.toolkit.fluxcd.io           | Define rules for selecting new images |
| imagerepositories.image.toolkit.fluxcd.io       | Specify external container registries |
| imageupdateautomations.images.toolkit.fluxcd.io | Automate updates based on policies    |

***

## 5. Review the Updated Flux Component Manifest

Open the generated manifest at `flux-clusters/dev-cluster/flux-components.yaml` and confirm the new controllers are included:

```yaml theme={null}
