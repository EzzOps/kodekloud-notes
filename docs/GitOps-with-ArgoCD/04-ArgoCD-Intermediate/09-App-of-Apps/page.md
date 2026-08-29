# App of Apps

Source: https://notes.kodekloud.com/docs/GitOps-with-ArgoCD/ArgoCD-Intermediate/App-of-Apps/page

This article explores the App-of-Apps pattern in ArgoCD for managing multiple applications through a single root configuration.

In this article, we dive into the App-of-Apps pattern in ArgoCD—a declarative approach that streamlines the creation and management of ArgoCD applications. Instead of manually deploying each application, the App-of-Apps pattern programmatically generates and manages multiple ArgoCD applications from a single root configuration.

The core idea is to create a root ArgoCD application whose source points to a folder containing YAML definition files for each microservice or application. Each YAML file specifies a path to a directory containing the relevant Kubernetes manifests. Once all these configuration files are committed to a Git repository, ArgoCD automatically detects and deploys the defined applications.

> **lightbulb** The root application acts as an orchestrator. It cues ArgoCD to traverse the specified directory, reading every YAML file to instantiate the associated applications. This ensures that updates in your Git repository trigger automatic synchronization with your Kubernetes cluster.

## Repository Structure Example

Assume your Git repository is organized so that each directory holds the necessary files for a specific application. The following example reviews the root ArgoCD application's YAML file, which is placed within a multi-application directory. This root application points to the "app-of-apps" directory, prompting ArgoCD to create all the child applications as defined in that folder.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-of-apps
spec:
  project: default
  source:
    repoURL: https://github.com/sidd-harth/test-cd.git
    targetRevision: HEAD
    path: ./declarative/app-of-apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

In this example, three ArgoCD application YAML files are defined within the specified directory. ArgoCD reads these definitions and automatically creates the corresponding applications.

## Detailed Look: Circle App YAML

Let’s examine the Circle App YAML file as an example. Every application YAML includes a source field that refers to its specific manifest directory. In the Circle App, ArgoCD uses the provided details to create or update the deployment and service in the Kubernetes cluster.

```yaml theme={null}
