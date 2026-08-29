# Add the chart repository to Argo CD (if not already added)
argocd repo add https://charts.bitnami.com/bitnami --type helm

# Create an application using the nginx chart from that repo
argocd app create nginx \
  --repo https://charts.bitnami.com/bitnami \
  --helm-chart nginx \
  --revision 12.0.3 \
  --values values.yaml \
  --dest-namespace default \
  --dest-server https://kubernetes.default.svc
```

## Manage deployments via the Argo CD UI

* The Argo CD web UI provides forms to create and manage applications, including Helm chart options and value overrides.
* UI supports repository connections using SSH, HTTPS, and GitHub App authentication.
* Whether created via CLI or UI, Argo CD continuously monitors the desired state in Git (or the chart repo) and reconciles changes to the cluster.

> **lightbulb** Once Argo CD deploys and manages a Helm chart, Argo CD becomes the source of truth for that application's lifecycle. Use the Argo CD CLI or the UI to inspect, sync, and manage the application state rather than local Helm client commands.

## Important: Helm CLI vs Argo CD-managed apps

When Argo CD deploys Helm charts, Argo CD renders the manifests and applies them to the cluster using its reconciliation engine. Argo CD does not create Helm release records in cluster storage the way a local Helm CLI install does. As a result:

* `helm list` typically will not show applications managed by Argo CD.
* Use Argo CD commands and the Argo CD UI for authoritative application metadata and status.

To inspect an Argo CD-managed application:

```bash theme={null}
# See Argo CD-managed application metadata and status
argocd app get random-shapes
```

Example: `helm ls` output may be empty for Argo CD-managed apps:

```text theme={null}
$ helm ls

NAME    NAMESPACE   REVISION    UPDATED STATUS  CHART   APP VERSION
```

> **warning** Do not rely on `helm list` to determine the state of applications managed by Argo CD. Always use `argocd app get` or the Argo CD UI for authoritative application status and metadata.

## Quick reference — Argo CD + Helm

| Source Type           | How to reference in Argo CD                                                             | Example                                                          |
| --------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Git repository        | Use `--repo` and `--path` to point at chart directory inside the repo                   | `argocd app create myapp --repo https://... --path helm-chart`   |
| Helm chart repository | Add the repo with `argocd repo add --type helm` and use `--helm-chart` (+ `--revision`) | `argocd repo add https://charts.bitnami.com/bitnami --type helm` |

## Links and references

* [Argo CD Documentation](https://argo-cd.readthedocs.io/)
* [Helm Documentation](https://helm.sh/)
* [Helm chart repositories](https://helm.sh/docs/topics/chart_repository/)
* [Bitnami Charts](https://charts.bitnami.com/bitnami)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/d6e2a380-2f64-465c-ab84-97ae6a8cf39e)


# GitOps Principles

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/GitOps-Principles/page

Explains GitOps principles using Git as the single source of truth for declarative configuration with continuous reconciliation, drift detection, feedback loops and rollback for Kubernetes and cloud infrastructure.

Let's review core GitOps terminology and how the pieces fit together.

GitOps uses Git as the single source of truth for declarative configuration, combined with automated reconciliation, to manage infrastructure and applications. Below we explain the key concepts you see on the screen and show practical examples.

<Frame>
  <img alt="A diagram titled &#x22;GitOps&#x22; showing colored labels for concepts like Continuous, Declarative, Desired State, State Drift, State Reconciliation, State Store, Feedback Loop, Rollback, and GitOps Managed System. A caption explains managing infrastructure and applications using Git as the single source of truth for declarative configuration with automated reconciliation." />
</Frame>

## 1. Continuous (Reconciliation)

In GitOps the reconciliation process is continuous — it runs constantly rather than executing once. Continuous reconciliation ensures the running system continuously converges toward the desired state declared in Git. This always-on loop detects deviations (e.g., a pod crash or a manual change) and automatically attempts to correct them.

Think of it like a thermostat: it continuously checks the temperature and adjusts heating or cooling to maintain the setpoint.

<Frame>
  <img alt="A slide showing a continuous deployment loop: a bot continuously compares a GitHub repo and syncs desired manifests to a Kubernetes cluster. To the right is a thermostat-style control showing 78° with a hand pressing a green button." />
</Frame>

> **lightbulb** Continuous reconciliation reduces manual toil and improves reliability by keeping the actual system in sync with the state declared in Git.

## 2. Declarative

Declarative configuration describes the end state you want, not the exact sequence of commands to reach it. In imperative workflows you run kubectl commands directly; in declarative workflows you store YAML manifests in Git and let the GitOps operator apply them.

Imperative example (creating resources via kubectl):

```bash theme={null}
kubectl create deployment nginx-deployment \
  --image=nginx:latest \
  --replicas=5 \
  --port=80

kubectl expose deployment nginx-deployment \
  --type=LoadBalancer \
  --port=80 \
  --target-port=80 \
  --name=nginx-service
```

Declarative example (store these manifests in Git under .k8s/manifests):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  labels:
    app: nginx-deployment
  name: nginx-service
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx-deployment
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx-deployment
  name: nginx-deployment
spec:
  replicas: 5
  selector:
    matchLabels:
      app: nginx-deployment
  template:
    metadata:
      labels:
        app: nginx-deployment
    spec:
      containers:
      - image: nginx:latest
        name: nginx
        ports:
        - containerPort: 80
```

Why declarative matters:

* Easier to understand the system intent.
* The operator chooses how to apply changes and adapt to the environment.
* Git provides versioning and an audit trail for every change.

## 3. Desired State

Desired state is the canonical configuration stored in your state store (typically Git). It is the plan GitOps aims to realize in the running system.

Example repository layout:

* .k8s/manifests/service.yaml
* .k8s/manifests/deployment.yaml
* .k8s/manifests/configmap.yaml
* .k8s/manifests/ingress.yaml

Each file (Deployment, Service, ConfigMap, Ingress) together represents the desired state for that application or cluster. A well-defined desired state lets you measure success, reproduce environments, and collaborate through Git workflows.

## 4. State Drift

State drift occurs when the actual system state diverges from the desired state declared in Git. Drift can be caused by manual kubectl edits, failed deployments, or unauthorized changes.

Why state drift is a problem:

* Causes unexpected behavior and instability.
* Makes troubleshooting harder if there's no single source of truth.
* Can introduce untracked or insecure configurations.

Example scenario:

* Desired state (Git): deployment with 5 replicas.
* Actual state (cluster): someone ran kubectl scale to reduce replicas to 3 — this is drift.

## 5. State Reconciliation

State reconciliation is the automated process of detecting drift and bringing the actual state back into alignment with the desired state. GitOps operators (observe → diff → act) implement reconciliation continuously.

Reconcile loop diagram:

<Frame>
  <img alt="A &#x22;State Reconciliation&#x22; diagram showing a circular reconcile loop with arrows labeled Observe, Diff, and Act around a central &#x22;Reconcile Loop.&#x22; To the right are two colored boxes labeled Desired State (Git) and Actual State (Kubernetes Cluster)." />
</Frame>

Reconciliation example (drift correction):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx-deployment
  name: nginx-app
spec:
  replicas: 5
  selector:
    matchLabels:
      app: nginx-deployment
  template:
    metadata:
      labels:
        app: nginx-deployment
    spec:
      containers:
      - image: nginx:latest
        name: nginx
        ports:
        - containerPort: 80
```

If someone manually scales the deployment:

```bash theme={null}
kubectl scale deploy nginx-app --replicas=3
```

A GitOps operator like FluxCD or ArgoCD will detect the diff and reconcile the cluster back to 5 replicas automatically.

Why reconciliation matters:

* Provides self-healing and resilience.
* Guarantees consistency with declared configuration.
* Reduces manual intervention and operational risk.

## 6. GitOps Managed Systems

A GitOps-managed system is any application or infrastructure component controlled via GitOps — most commonly Kubernetes clusters, but also cloud resources via tools like Terraform stored in Git. Everything needed to run and manage the system lives in the Git repository: namespaces, RBAC, deployments, services, monitoring stacks, etc.

<Frame>
  <img alt="Diagram of a GitOps-managed software system. It shows Kubernetes manifests, Helm charts and Terraform/Ansible files in a Git repo feeding a GitOps operator that deploys to Kubernetes and cloud providers (Azure, Google Cloud, AWS)." />
</Frame>

## 7. State Store

The state store is the centralized repository holding the desired state. Git is the most common state store because it provides:

* A single source of truth
* Immutable history and audit trails
* Branching, pull requests, and code review workflows for collaboration

Other systems can be used, but Git’s workflows and tooling make it ideal for teams.

## 8. Feedback Loop

A feedback loop closes the cycle between deployment and operation: metrics, logs, and alerts inform adjustments to the desired state and reconciliation behavior. Monitoring and alerting tools detect problems in the running system and feed that information back to teams to trigger fixes or rollbacks.

Example workflow:

* GitOps operator deploys a new version.
* Prometheus detects increased error rates.
* Grafana dashboards visualize the issue; Alertmanager notifies the on-call team.
* Team reverts or patches the manifest in Git → reconciliation applies the fix.

Useful links:

* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Grafana: [https://grafana.com/](https://grafana.com/)
* Alertmanager: [https://prometheus.io/docs/alerting/alertmanager/](https://prometheus.io/docs/alerting/alertmanager/)

Why feedback loops matter:

* Detect issues early in production.
* Improve desired-state definitions based on real-world behavior.
* Allow iterative improvements driven by telemetry.

## 9. Rollback

Rollbacks are fast recovery mechanisms to revert problematic changes. In GitOps, rollbacks are typically done by reverting commits in Git or by letting GitOps tools perform automatic rollbacks when they detect failures.

Methods:

* Git revert: create a new commit that undoes a previous change (preserves history).

```bash theme={null}
