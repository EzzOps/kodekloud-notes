# See rollout status
kubectl rollout status deployment/my-app

# Roll back to the previous revision
kubectl rollout undo deployment/my-app
```

> **lightbulb** RollingUpdate is the Kubernetes default strategy. It provides continuous availability during upgrades and is well-suited to stateless services or stateful apps that rely on external persistence.

## Recreate

The Recreate strategy deletes all existing pods before creating any new pods. This is a simpler lifecycle but it introduces downtime while the new pods start. Use Recreate when the application cannot safely run multiple versions simultaneously (no coexistence) or when short downtime is acceptable.

Example Deployment (Recreate):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:1.0
```

How Recreate typically works in a GitOps flow:

1. Update the image tag in the Git manifest.
2. GitOps operator applies the manifest to the cluster.
3. Kubernetes deletes all current pods for the Deployment.
4. Kubernetes creates the new pods for the updated version.
5. The service is unavailable between pod deletion and the new pods becoming ready.

Comparing RollingUpdate vs Recreate

* RollingUpdate: minimal downtime, allows coexistence of old and new pods during rollout. Best when continuous availability is required.
* Recreate: simple lifecycle with downtime while pods are replaced. Best when version coexistence is unsafe.

Comparison table

| Strategy        | Downtime               | Coexistence of versions | When to use                                                                                 |
| --------------- | ---------------------- | ----------------------- | ------------------------------------------------------------------------------------------- |
| `RollingUpdate` | Minimal (configurable) | Yes                     | Stateless apps or stateful apps with external persistence; continuous availability required |
| `Recreate`      | Temporary downtime     | No                      | When concurrency between versions causes problems, or when brief downtime is acceptable     |

## Next steps

Once you're comfortable with RollingUpdate and Recreate, explore blue–green deployments and canary releases for more controlled traffic shifting and progressive rollouts. These patterns often require traffic management tooling such as an Ingress controller, a service mesh (e.g., Istio), or external load balancers, together with observability and automation to safely promote or rollback releases.

Links and references

* [GitOps with ArgoCD](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* [Istio Service Mesh](https://learn.kodekloud.com/user/courses/istio-service-mesh)
* Kubernetes docs — Deployments: [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/6835080d-68dc-4c5e-aaab-cd8ec0323f72)


# GitOps Reconciler Types In Cluster and External

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/GitOps-Reconciler-Types-In-Cluster-and-External/page

Explains in-cluster versus external GitOps reconcilers, trade-offs, flows, Argo CD roles, and credential and network considerations for managing Kubernetes clusters.

GitOps relies on a reconciler to converge a Kubernetes cluster's live state to the desired state defined in Git. There are two primary deployment patterns for reconciler components: in-cluster and external. This guide explains both patterns, their operational trade-offs, typical flows, and how Argo CD fits into each model.

## What a reconciler does (high level)

A reconciler continuously compares the desired state (from Git) with the cluster's live state and applies changes until they match. Where the reconciler runs (inside the target cluster or outside it) determines the operational model and affects security, network requirements, and credential management.

## In-cluster reconcilers

In-cluster reconcilers run inside the Kubernetes cluster they manage.

* Behavior: The reconciler pulls manifests from Git and applies changes using the cluster’s local Kubernetes API.
* Examples: Argo CD (when deployed inside the target cluster), Flux CD (as an operator).
* Benefits:
  * No need to expose cluster credentials outside the cluster.
  * Reduced network exposure because reconciliation is performed locally.
  * Simpler authentication: reconciler uses in-cluster service account credentials.
* Typical flow:
  1. Reconciler (running inside the cluster) pulls manifests from Git.
  2. It compares manifests to the cluster’s live state using the local API server.
  3. It applies changes by creating/updating Kubernetes resources locally.

> **lightbulb** In-cluster reconcilers follow a pull model: they fetch desired state from Git and apply it via the cluster’s local API, minimizing external credential handling and network exposure.

## External reconcilers

External reconcilers run outside the target Kubernetes cluster. Common examples include CI/CD runners, management VMs, or controllers in a separate management cluster.

* Behavior: The reconciler either pulls desired state from Git or receives artifacts from a pipeline, then connects over the network to the target cluster’s API server and applies changes.
* Example deployments: a Jenkins pipeline that applies manifests to production clusters, or a central management cluster that controls multiple tenant clusters.
* Trade-offs:
  * Requires storing and managing cluster credentials outside the target cluster (e.g., `kubeconfig`, service account tokens), which increases operational complexity and attack surface.
  * Requires network access to the target clusters’ API servers.
* Typical flow:
  1. External reconciler obtains manifests (pulls from Git or receives them from a pipeline).
  2. It uses externally stored credentials to call the target cluster’s API server.
  3. It applies changes remotely.

> **warning** External reconcilers require externally stored Kubernetes credentials and network access to the API server. Protect and rotate credentials (e.g., `kubeconfig`, tokens) and restrict API access to minimize risk.

## How Argo CD fits in

Argo CD is primarily deployed as an in-cluster reconciler: its components (including the Application Controller) normally run inside a Kubernetes cluster. However, Argo CD is built to manage applications across multiple clusters.

* When Argo CD manages a remote (external) cluster, the Argo CD instance runs in its own cluster (the "management" cluster). For each registered external cluster, Argo CD stores credentials (for example, `kubeconfig` or a service account token) and uses them to connect to that cluster’s API server.
* In other words:
  * Argo CD is an in-cluster reconciler in the cluster where it is deployed.
  * Relative to any external target cluster it manages, Argo CD behaves like an external reconciler because it connects remotely to that cluster’s API to apply changes.
* Key point: Reconciliation is centralized in Argo CD’s controllers, but applying manifests to remote clusters requires Argo CD to hold and use credentials for those clusters—so credential handling and API connectivity are necessary for multi-cluster management.

## Comparison summary

|               Pattern | Runs where                 | Credential handling                                        | Network requirements                           | Operational considerations                                                                      |
| --------------------: | -------------------------- | ---------------------------------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| In-cluster reconciler | Inside the target cluster  | Uses in-cluster service accounts / no external kubeconfigs | Local API access only — lower network exposure | Simpler security model; ideal when controllers can be hosted in each target cluster             |
|   External reconciler | Outside the target cluster | Requires stored `kubeconfig` or tokens outside the cluster | Must reach API server over the network         | Centralized control possible; requires secure credential storage and robust API access controls |

## Choosing a pattern: key factors

Consider these when selecting a reconciler deployment model:

* Security posture for managing cluster credentials (local service accounts vs. external `kubeconfig`).
* Network topology and API server accessibility (firewalls, NAT, private clusters).
* Operational preferences: decentralized (deploy controllers in each cluster) vs. centralized management (single management cluster or CI system).
* Scale and multi-tenancy: central management may simplify operations across many clusters, but increases credential management overhead.

## Final notes

Both patterns are valid and commonly used in GitOps workflows. In-cluster reconcilers reduce credential sprawl and network exposure, while external reconcilers allow centralized pipelines and cross-cluster control. Argo CD supports both scenarios by running as an in-cluster controller and connecting remotely to registered clusters when needed.

## Links and references

* [GitOps with ArgoCD](https://learn.kodekloud.com/user/courses/gitops-with-argocd)

* [GitOps with FluxCD](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)

* [Jenkins course example](https://learn.kodekloud.com/user/courses/jenkins)

* Kubernetes concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)

* Best practice: store and rotate external credentials (`kubeconfig`, tokens) and restrict API server access using network policies and firewall rules.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/24542572-7734-447c-b135-86921b45a18b)
