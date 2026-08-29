# Demo Setup Argo Rollouts

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Demo-Setup-Argo-Rollouts/page

Guide to installing and configuring Argo Rollouts in Kubernetes, verifying the controller, installing the CLI, and using progressive delivery strategies like canary and blue green deployments.

In this guide you'll install Argo Rollouts in a Kubernetes cluster, verify the controller, and install the CLI so you can experiment with canary and blue-green deployments. Argo Rollouts is a Kubernetes controller plus a set of CRDs that extend the Deployment semantics to enable progressive delivery: fine-grained traffic control, automated analysis, and safe rollbacks.

<Frame>
  <img alt="The image shows a webpage from the Argo Rollouts documentation, explaining its functions as a Kubernetes Progressive Delivery Controller, with a menu on the left and a description of its key features on the right." />
</Frame>

## 1) Cluster permissions

Argo Rollouts requires the controller to run with appropriate RBAC permissions. If your user is not already cluster-admin (common in managed clusters), you can temporarily grant cluster-admin for installation/testing by creating a ClusterRoleBinding — replace `<YOUR_EMAIL>` with your identity:

```bash theme={null}
kubectl create clusterrolebinding YOURNAME-cluster-admin-binding --clusterrole=cluster-admin --user=`<YOUR_EMAIL>`
```

> **warning** Granting `cluster-admin` is powerful. Only create a ClusterRoleBinding in test environments (minikube, kind, or disposable clusters) or when you understand the security implications.

## 2) Install Argo Rollouts

Create the `argo-rollouts` namespace and apply the official install manifest. The manifest sets up CRDs, RBAC, ConfigMap, Service, and the Rollouts controller Deployment.

```bash theme={null}
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

Expected install output (sample):

```bash theme={null}
namespace/argo-rollouts created
customresourcedefinition.apiextensions.k8s.io/analysisruns.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/analysistemplates.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/clusteranalysistemplates.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/experiments.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/rollouts.argoproj.io created
clusterrole.rbac.authorization.k8s.io/argo-rollouts created
clusterrolebinding.rbac.authorization.k8s.io/argo-rollouts created
clusterrole.rbac.authorization.k8s.io/argo-rollouts-aggregate-to-admin created
clusterrole.rbac.authorization.k8s.io/argo-rollouts-aggregate-to-edit created
clusterrole.rbac.authorization.k8s.io/argo-rollouts-aggregate-to-view created
configmap/argo-rollouts-config created
secret/argo-rollouts-notification-secret created
service/argo-rollouts-metrics created
deployment.apps/argo-rollouts created
```

Verify the controller pod, service, and deployment are present and running:

```bash theme={null}
kubectl get all -n argo-rollouts
```

Sample verification output:

```bash theme={null}
NAME                                   READY   STATUS    RESTARTS   AGE
pod/argo-rollouts-64d959676c-m6h4w     1/1     Running   0          2m

NAME                                   TYPE        CLUSTER-IP      PORT(S)    AGE
service/argo-rollouts-metrics          ClusterIP   10.101.96.18    8090/TCP   2m

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/argo-rollouts          1/1     1            1           2m

NAME                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/argo-rollouts-64d959676c       1         1         1       2m
```

Recommended quick reference: resources created by the install manifest

| Resource Type | Purpose                                                    | Example created by manifest     |
| ------------: | ---------------------------------------------------------- | ------------------------------- |
|     Namespace | Logical isolation for Argo Rollouts components             | `argo-rollouts`                 |
|          CRDs | Custom resources for Rollouts, AnalysisRuns, Experiments   | `rollouts.argoproj.io`          |
|    Deployment | Controller process that reconciles Rollout CRs             | `deployment.apps/argo-rollouts` |
|       Service | Metrics endpoint for dashboard/monitoring                  | `service/argo-rollouts-metrics` |
|          RBAC | Permissions for the controller to manage cluster resources | `clusterrole/argo-rollouts`     |

## 3) Install the Argo Rollouts CLI

To manage Argo Rollouts from your workstation, install the kubectl plugin binary (kubectl-argo-rollouts). Download the correct release for your OS/arch from the Argo Rollouts releases page:

* Releases: [https://github.com/argoproj/argo-rollouts/releases](https://github.com/argoproj/argo-rollouts/releases)

Example for Linux AMD64 (version v1.8.3):

<Frame>
  <img alt="This image shows a GitHub repository page for &#x22;argo-rollouts,&#x22; featuring sections for code, issues, and pull requests, with repository statistics like stars and forks." />
</Frame>

```bash theme={null}
wget https://github.com/argoproj/argo-rollouts/releases/download/v1.8.3/kubectl-argo-rollouts-linux-amd64
chmod +x ./kubectl-argo-rollouts-linux-amd64
sudo mv ./kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts
```

After placing the binary on your `PATH` (for example `/usr/local/bin/kubectl-argo-rollouts`), invoke it through `kubectl`:

```bash theme={null}
kubectl argo rollouts version
```

Example output:

```bash theme={null}
kubectl-argo-rollouts: v1.8.3
```

Notes:

* On macOS use the Darwin binary; on Windows use the `.exe` release and add it to your PATH.
* You can also install via package managers or Homebrew where available — check the releases page for options.

## 4) Accessing the Argo Rollouts dashboard

The CLI can start a local web UI for inspecting Rollout resources:

```bash theme={null}
kubectl argo rollouts dashboard
```

When started it will print the local address, for example:

```text theme={null}
INFO[0000] Argo Rollouts Dashboard is now available at http://localhost:3100/rollouts
```

Open `http://localhost:3100/rollouts` in your browser. The dashboard lists Rollout CRs across namespaces you have access to. Initially it will be empty until you create Rollout objects (the Argo Rollouts CRD) in the namespaces you inspect.

Useful links and references

* Argo Rollouts documentation: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)
* GitHub releases: [https://github.com/argoproj/argo-rollouts/releases](https://github.com/argoproj/argo-rollouts/releases)
* Kubernetes concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

That's it — Argo Rollouts is installed and ready. The controller is running, and the CLI + dashboard are available so you can begin testing blue-green and canary deployment strategies.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/444c5850-0e7e-461a-bf4d-861dfa3ed065)
