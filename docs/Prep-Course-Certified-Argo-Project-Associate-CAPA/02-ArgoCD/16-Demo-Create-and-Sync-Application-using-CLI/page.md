# you should NOT see "highway-animation" until after sync
```

In the Argo CD UI click Diff to see the manifests pulled from Git and the differences versus cluster state. When resources are applied Argo CD adds tracking annotations; the UI shows the manifests as Argo CD will apply them.

Example of the Service and Deployment as Argo CD reads them from the repository (annotations will be added when Argo CD applies them):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  annotations:
    argocd.argoproj.io/tracking-id: highway-animation:/Service:highway-animation/highway-animation-service
  name: highway-animation-service
  namespace: highway-animation
spec:
  ports:
    - nodePort: 32000
      port: 3000
      protocol: TCP
      targetPort: 3000
  selector:
    app: highway-animation
  type: NodePort

apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    argocd.argoproj.io/tracking-id: highway-animation:apps/Deployment:highway-animation/highway-animation
  name: highway-animation
  namespace: highway-animation
spec:
  replicas: 1
  selector:
    matchLabels:
      app: highway-animation
  ...
```

You can also view the Application resource that Argo CD created to represent this app; it encodes source, destination, and sync options:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: highway-animation
spec:
  project: default
  source:
    repoURL: http://host.docker.internal:5000/kk-org/capa-demos
    path: ./vanilla
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: highway-animation
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
```

## Sync the Application (deploy)

Because the Application is OutOfSync, perform a manual Sync from the Argo CD UI:

* Click the Sync button for the Application.
* Confirm and start the sync operation.

During sync Argo CD will:

* Create the `highway-animation` namespace (because CreateNamespace=true)
* Apply the Service and Deployment manifests
* Add tracking annotations to the created resources

After a successful sync verify the deployment:

```bash theme={null}
kubectl get ns highway-animation
kubectl -n highway-animation get deploy,svc
kubectl -n highway-animation get pods
```

## Links and references

* [Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)
* [Kubernetes documentation](https://kubernetes.io/docs/)

> **lightbulb** Tip: If you want continuous deployments, change the Application sync policy to Automatic and configure any required pruning or hooks. For controlled rollouts keep Manual sync and use Argo CD’s health checks and rollout features.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/c175199a-a8f3-4897-a445-de634e21b7b8)


# Demo Create and Sync Application using CLI

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Create-and-Sync-Application-using-CLI/page

Guide to creating and syncing an Argo CD application entirely via the argocd CLI, including installation, login, app creation, namespace setup, synchronization, and troubleshooting

In this guide you'll learn how to create an Argo CD application entirely from the command line and synchronize it to a Kubernetes cluster using the argocd CLI. Follow these steps:

* Install the argocd CLI
* Authenticate (log in) to your Argo CD server
* List existing applications
* Create a new application with the CLI
* Create the target namespace (if necessary)
* Synchronize the application and verify status

For background reading, see the Argo CD documentation: [Argo CD Docs](https://argo-cd.readthedocs.io/) and the Kubernetes docs: [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

## 1. Install the argocd CLI

Choose the installation method that matches your OS. The following table summarizes common options.

|                       Platform | Installation                                |
| -----------------------------: | ------------------------------------------- |
|                     Arch Linux | `pacman -S argocd`                          |
|               macOS (Homebrew) | `brew install argocd`                       |
| Linux (direct download, amd64) | Download and install binary (example below) |
|               Specific release | Download the desired release from GitHub    |

Example direct download (Linux amd64):

```bash theme={null}
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
```

To install a specific release, replace `latest` with the release tag:

```bash theme={null}
VERSION=<TAG> # pick a release tag from https://github.com/argoproj/argo-cd/releases
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/download/$VERSION/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
```

Verify the client version:

```bash theme={null}
argocd version
```

Example client-only output:

```text theme={null}
argocd: v3.1.5+cfed49
BuildDate: 2025-09-10T16:01:20Z
GitCommit: cfed4910542c359f18537a6668d4671abd3813b
GitTreeState: clean
GoVersion: go1.24.6
Compiler: gc
Platform: linux/amd64
```

<Frame>
  <img alt="A dark-themed Visual Studio Code window with the integrated terminal displaying the Argo CD CLI help output (a list of available commands and flags). The Explorer sidebar is visible on the left and a faint Argo CD/VS Code logo appears in the editor area." />
</Frame>

If the CLI cannot reach the Argo CD API server, commands that contact the server (e.g., `argocd app list`) will return a connection error. You must log in before managing applications.

## 2. Log in to the Argo CD server

First, try listing applications. If you're not logged in or the CLI can't reach the server, this will fail:

```bash theme={null}
argocd app list
```

If you get an error such as "Failed to establish connection ... connection refused", confirm the argocd-server service and its NodePort or load balancer address.

Find the argocd server service in the `argocd` namespace:

```bash theme={null}
