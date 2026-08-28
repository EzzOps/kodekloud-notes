# MESSAGE: authentication required
```

<Frame>
  ![The image shows a GitHub repository page with a branch selection dropdown open, displaying various branches like "2-demo" and "9-demo." The page includes options for code management, such as "Compare & pull request" and "Add a README."](https://kodekloud.com/kk-media/image/upload/v1752877634/notes-assets/images/GitOps-with-FluxCD-DEMO-Image-Automation-Controller-Update/github-repo-branch-selection-dropdown.jpg)
</Frame>

Go to your GitHub repository **Settings → Deploy keys**:

<Frame>
  ![The image shows a GitHub repository settings page, specifically the "Deploy keys" section, indicating that there are no deploy keys for the repository.](https://kodekloud.com/kk-media/image/upload/v1752877635/notes-assets/images/GitOps-with-FluxCD-DEMO-Image-Automation-Controller-Update/github-repo-settings-deploy-keys.jpg)
</Frame>

Generate a deploy key secret and apply it:

```bash theme={null}
flux create secret git 8-demo-git-bb-app-auth \
  --url=ssh://git@github.com/sidd-harth-2/bb-app-source.git \
  --ssh-key-algorithm=ecdsa \
  --ssh-ecdsa-curve=p521 \
  --export > 8-demo-git-bb-app-auth-secret.yml

kubectl apply -f 8-demo-git-bb-app-auth-secret.yml -n flux-system
```

Copy the public key from the secret and add it in GitHub as a **write** deploy key. Authenticate if prompted:

<Frame>
  ![The image shows a GitHub "Confirm access" page prompting the user to enter their password to proceed. It includes a password input field, a "Confirm" button, and links for terms, privacy, and security.](https://kodekloud.com/kk-media/image/upload/v1752877636/notes-assets/images/GitOps-with-FluxCD-DEMO-Image-Automation-Controller-Update/github-confirm-access-password-input.jpg)
</Frame>

***

## 6. Reconfigure GitRepository Source to Use SSH

Regenerate the `GitRepository` to reference your SSH URL and secret:

```bash theme={null}
flux create source git 8-demo-source-git-bb-app \
  --url=ssh://git@github.com/sidd-harth-2/bb-app-source.git \
  --branch=8-demo \
  --secret-ref=8-demo-git-bb-app-auth \
  --timeout=10s \
  --export > 8-demo-source-git-bb-app.yml

kubectl apply -f 8-demo-source-git-bb-app.yml
flux reconcile source git 8-demo-source-git-bb-app -n flux-system
```

***

## 7. Final Reconciliation and Verification

Trigger the image update and verify the new tag is committed and deployed:

```bash theme={null}
flux reconcile image update 8-demo-image-update-bb-app -n flux-system
flux get images all
flux get image update
```

Now Flux will commit the updated tag (e.g., `7.8.1`) to your `manifests/deployment.yml`. Confirm on GitHub:

<Frame>
  ![The image shows a GitHub repository page for "bb-app-source" with a focus on the "manifests" directory, displaying files like "deployment.yml," "namespace.yml," and "service.yml." The branch is 16 commits ahead and 1 commit behind the main branch.](https://kodekloud.com/kk-media/image/upload/v1752877637/notes-assets/images/GitOps-with-FluxCD-DEMO-Image-Automation-Controller-Update/github-repo-bb-app-manifests-files.jpg)
</Frame>

Finally, ensure the new image is running in your cluster:

```bash theme={null}
kubectl -n 8-demo get deploy block-buster -o wide
```

Expected output:

```bash theme={null}
block-buster  1/1  1  1  1m  app  docker.io/siddharth67/bb-app-flux-demo:7.8.1
```

<Frame>
  ![The image shows a game interface for "Block Buster" with details like pod name, IP, and app version. It prompts the user to "PRESS START" to begin the game.](https://kodekloud.com/kk-media/image/upload/v1752877639/notes-assets/images/GitOps-with-FluxCD-DEMO-Image-Automation-Controller-Update/block-buster-game-interface-details.jpg)
</Frame>

***

Congratulations! You’ve successfully automated image tag updates with Flux’s ImageUpdateAutomation controller.

## Links and References

* [Flux Image Automation Guide](https://fluxcd.io/docs/guides/image-automation/)
* [Flux CLI Reference](https://fluxcd.io/docs/cmd/flux/)
* [Kubernetes Concepts Overview](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [GitHub Deploy Keys Documentation](https://docs.github.com/en/developers/overview/managing-deploy-keys)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/e4076c7b-6728-412c-b4d7-9316fc346fc5/lesson/d03a07a1-a7f5-481a-bbc7-3fdcbf3768c4" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/e4076c7b-6728-412c-b4d7-9316fc346fc5/lesson/64cfb295-552e-4ad2-8df8-b7ddb02641d0" />
</CardGroup>


# DEMO Flux User Interface

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Monitoring-User-Interface/DEMO-Flux-User-Interface/page

This guide explores two open-source graphical interfaces for managing Flux CD, enhancing observability and workflow efficiency.

In this guide, we’ll explore two open-source graphical interfaces for managing Flux CD:

* **VS Code GitOps Tools for Flux** – a lightweight VS Code extension
* **Weaveworks GitOps UI** – a full-featured web dashboard

Both solutions let you inspect clusters, sources, workloads, and more without manual `kubectl` commands or hand-editing YAML.

## Comparison at a Glance

| Tool                          | Interface Type    | Key Features                                |
| ----------------------------- | ----------------- | ------------------------------------------- |
| VS Code GitOps Tools for Flux | VS Code Extension | Clusters, Sources, Workloads, Docs links    |
| Weaveworks GitOps UI          | Web Dashboard     | Sources, Applications, Runtimes, Automation |

***

## 1. VS Code GitOps Extension for Flux

The **GitOps Tools for Flux** extension brings Flux CD insights directly into Visual Studio Code.

### Install the Extension

1. Open **Extensions** (⇧⌘X or Ctrl+Shift+X).
2. Search for **GitOps Tools for Flux**.
3. Click **Install**.

Once installed, you’ll see a new **GitOps** icon in the Activity Bar:

<Frame>
  ![The image shows a webpage from the Flux ecosystem, detailing open-source projects that offer graphical user interfaces for Flux, including descriptions of Weaveworks tools.](https://kodekloud.com/kk-media/image/upload/v1752877643/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/flux-ecosystem-open-source-gui-tools.jpg)
</Frame>

<Frame>
  ![The image shows the Visual Studio Code interface with the "GitOps Tools for Flux" extension details displayed, including features and ratings. The terminal at the bottom is open, showing a command prompt.](https://kodekloud.com/kk-media/image/upload/v1752877644/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/vscode-gitops-tools-flux-extension-details.jpg)
</Frame>

### Navigating the GitOps Pane

Click the **GitOps** icon to reveal four sections:

* **Clusters** – view all Flux controllers
* **Sources** – inspect GitRepositories, HelmRepositories, Buckets, OCIRepositories
* **Workloads** – check Kustomizations & HelmReleases
* **Documentation** – quick links to Flux docs

#### Clusters

Select your Kubernetes context (e.g., Docker Desktop) to see live YAML for each controller:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: helm-controller
  namespace: flux-system
  labels:
    app.kubernetes.io/part-of: flux
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/component: helm-controller
  template:
    metadata:
      labels:
        control-plane: controller
    spec:
      containers:
        - name: manager
          image: ghcr.io/fluxcd/helm-controller:v0.41.2
```

<Frame>
  ![The image shows a Visual Studio Code interface with the "GitOps Tools for Flux" extension details open, alongside a terminal window at the bottom. The extension is used for managing Kubernetes and cloud-native applications.](https://kodekloud.com/kk-media/image/upload/v1752877645/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/vscode-gitops-tools-flux-extension.jpg)
</Frame>

#### Sources

Browse all configured Sources in the `flux-system` namespace:

* GitRepository
* HelmRepository
* Bucket
* OCIRepository

#### Workloads

Inspect Kustomizations and HelmReleases in one place. For example, clicking a HelmRelease reveals its specification:

```yaml theme={null}
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: 2-demo-kustomize-git-bb-app
  namespace: flux-system
spec:
  sourceRef:
    kind: GitRepository
    name: 2-demo-source-git-bb-app
    targetNamespace: 2-demo
  path: ./manifests
  interval: 10s
  prune: true
  force: false
```

<Frame>
  ![The image shows a Visual Studio Code interface with a GitOps extension displaying a list of Kubernetes workloads in the "flux-system" namespace. A tooltip provides details about a HelmRelease named "sealed-secrets."](https://kodekloud.com/kk-media/image/upload/v1752877646/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/vscode-gitops-kubernetes-flux-system.jpg)
</Frame>

#### Adding New Sources or Kustomizations

Create new Git sources or Kustomizations via an intuitive form:

<Frame>
  ![The image shows a Visual Studio Code interface with a GitOps configuration screen, where a Git repository is being set up with details like repository name, URL, and branch.](https://kodekloud.com/kk-media/image/upload/v1752877647/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/visual-studio-code-gitops-configuration.jpg)
</Frame>

<Callout icon="lightbulb">
  The VS Code extension is ideal for developers who prefer keeping their GitOps workflow within the editor.
</Callout>

***

## 2. Weaveworks GitOps User Interface

The Weaveworks GitOps UI (part of [Weave GitOps](https://www.weave.works/docs/weave-gitops/)) provides a standalone web dashboard for Flux.

### Prerequisites

* Kubernetes cluster with Flux installed
* `kubectl` configured

### Install the Weave GitOps CLI

```bash theme={null}
curl -sSL \
  "https://github.com/weaveworks/weave-gitops/releases/download/v0.20.0/gitops-$(uname -s)-$(uname -m).tar.gz" \
  | tar xz -C /tmp
sudo mv /tmp/gitops /usr/local/bin/gitops
gitops version
```

### Deploy the Dashboard

Generate and apply the dashboard manifest:

```bash theme={null}
export PASSWORD="your-password"
gitops create dashboard ww-gitops \
  --password="$PASSWORD" \
  --export > weave-gitops-dashboard.yaml

kubectl apply -f weave-gitops-dashboard.yaml
```

You should see:

```text theme={null}
Creating GitOps Dashboard objects ...
Generated GitOps Dashboard manifests
Checking for a cluster in the kube config ...
Flux v0.41.2 (flux-system) is already installed
Applying GitOps Dashboard manifests
HelmRepository/flux-system/ww-gitops created
HelmRelease/flux-system/ww-gitops created
GitOps Dashboard ww-gitops is ready
```

<Frame>
  ![The image shows a webpage with instructions for installing Weave GitOps on a cluster, including prerequisites and steps for installing Flux. The page is part of the Weave GitOps documentation site.](https://kodekloud.com/kk-media/image/upload/v1752877648/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/weave-gitops-installation-instructions-flux.jpg)
</Frame>

### Expose & Access the Dashboard

List the GitOps service and pod:

```bash theme={null}
kubectl -n flux-system get po,svc | grep gitops
```

Patch the service to use `NodePort`:

```bash theme={null}
kubectl -n flux-system patch svc www-gitops-weave-gitops \
  -p '{"spec": {"type": "NodePort"}}'
kubectl -n flux-system get svc www-gitops-weave-gitops
```

Forward to localhost or browse directly:

```bash theme={null}
kubectl port-forward svc/www-gitops-weave-gitops -n flux-system 9001:9001
```

Open your browser at:\
[http://localhost:9001](http://localhost:9001)\
Login with **admin** and your password.

<Callout icon="triangle-alert">
  Exposing services via `NodePort` can pose security risks. Ensure proper network policies and firewall rules are in place.
</Callout>

### Dashboard Overview

#### Sources

Monitor all Git and Helm sources, their sync status, intervals, and last reconciliation:

<Frame>
  ![The image shows a dashboard interface from Weave GitOps, displaying a list of sources with details such as name, kind, namespace, status, and messages.](https://kodekloud.com/kk-media/image/upload/v1752877650/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/weave-gitops-dashboard-sources-list.jpg)
</Frame>

<Frame>
  ![The image shows a Weave GitOps interface displaying a list of sources with their status, messages, URLs, and other details. One source is marked "Not Ready" due to a missing bucket, while others are "Ready" with various updates and revisions.](https://kodekloud.com/kk-media/image/upload/v1752877651/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/weave-gitops-interface-sources-status.jpg)
</Frame>

#### Applications

Inspect Kustomizations and HelmReleases along with dependency graphs, events, and raw YAML:

<Frame>
  ![The image shows a dashboard interface for Weave GitOps, displaying a list of applications with details such as name, kind, namespace, source, status, and messages. The applications are mostly in "Ready" status, and the interface includes navigation options on the left.](https://kodekloud.com/kk-media/image/upload/v1752877653/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/weave-gitops-dashboard-applications-interface.jpg)
</Frame>

<Frame>
  ![The image shows a Weave GitOps application interface displaying details of a Kubernetes deployment, including resources like namespaces, deployments, and services, with their statuses and messages.](https://kodekloud.com/kk-media/image/upload/v1752877654/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/weave-gitops-kubernetes-deployment-interface.jpg)
</Frame>

#### Image Automation & Notifications

Manage image repositories, policies, automation events, and notification controllers—all from the UI.

#### Flux Runtime

View the status of all Flux controllers and custom resources in one panel:

<Frame>
  ![The image shows a Flux Runtime dashboard from Weave GitOps, displaying a list of controllers with their status as "Ready" in the "flux-system" namespace.](https://kodekloud.com/kk-media/image/upload/v1752877655/notes-assets/images/GitOps-with-FluxCD-DEMO-Flux-User-Interface/flux-runtime-dashboard-controllers-status.jpg)
</Frame>

***

Whether you embed GitOps directly in VS Code or operate via a standalone dashboard, these tools streamline your Flux workflows and improve observability.

## Links and References

* [Flux CD Documentation](https://fluxcd.io/docs/)
* [Weave GitOps Documentation](https://www.weave.works/docs/weave-gitops/)
* [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
* [VS Code Marketplace: GitOps Tools for Flux](https://marketplace.visualstudio.com/items?itemName=weaveworks.flux)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/fb9e59dc-9dee-4532-92a8-553d0df1df27/lesson/8a49376a-79bc-4910-bd42-07c3de0f57a6" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/fb9e59dc-9dee-4532-92a8-553d0df1df27/lesson/565653b9-da58-4b18-8485-63f9f9416481" />
</CardGroup>
