# Continuous and Declarative Description

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Terminology/Continuous-and-Declarative-Description/page

Explains GitOps concepts like declarative manifests, continuous reconciliation, desired state, drift, state store, feedback loops, and rollbacks for managing infrastructure via Git

Explore essential GitOps terminology and how the concepts fit together.

GitOps is the practice of managing infrastructure and applications using Git as the single source of truth for declarative configuration with automated reconciliation. This article clarifies key GitOps terms and shows how they relate: continuous reconciliation, declarative manifests, desired state, state drift, reconciliation, feedback loops, rollbacks, and the state store.

<Frame>
  <img alt="The image illustrates GitOps concepts with labeled elements like &#x22;Continuous,&#x22; &#x22;Declarative,&#x22; and &#x22;Desired State,&#x22; alongside descriptions of managing infrastructure using Git for declarative configuration." />
</Frame>

## Continuous

In GitOps, reconciliation is continuous — an ongoing loop that ensures the running system matches the declared configuration. Continuous reconciliation reacts to changes (for example, pod crashes or ad-hoc manual edits) and restores the desired state automatically. Think of it like a thermostat: it constantly observes the environment and adjusts until the setpoint is reached.

Continuous reconciliation reduces operational toil and improves resiliency by continuously observing, comparing, and correcting the cluster state.

<Frame>
  <img alt="The image illustrates a continuous integration setup involving a Kubernetes cluster that syncs with desired manifests, incorporating GitHub and an automation bot, alongside a thermostat displaying the number 78." />
</Frame>

## Declarative

Declarative configuration states what you want the system to look like (the desired state), not how to get there. A GitOps operator is responsible for making the cluster match that description.

Imperative commands execute specific API calls and steps; declarative manifests describe the intended outcome.

Imperative example (direct commands):

```bash theme={null}
kubectl create deployment nginx-deployment \
  --image=nginx:latest \
  --replicas=5

kubectl expose deployment nginx-deployment \
  --type=LoadBalancer \
  --port=80 \
  --target-port=80 \
  --name=nginx-service
```

Declarative example (YAML manifests stored in Git):

Service (`service.yml`)

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  labels:
    app: nginx-deployment
spec:
  type: LoadBalancer
  selector:
    app: nginx-deployment
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
```

Deployment (`deployment.yml`)

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx-deployment
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
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
```

A GitOps operator (for example, Flux or Argo CD) watches the repository and applies the YAML manifests to the cluster.

Useful links:

* Flux: [https://learn.kodekloud.com/user/courses/gitops-with-fluxcd](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)
* Argo CD: [https://learn.kodekloud.com/user/courses/gitops-with-argocd](https://learn.kodekloud.com/user/courses/gitops-with-argocd)

> **lightbulb** Keeping the desired state in Git enables code review, CI checks, and an auditable history of configuration changes — essential for collaborative operations and compliance.

## Desired state

The desired state is the canonical description of how your system should behave. A repository commonly contains a directory like `manifests/` with YAML files for Deployments, Services, ConfigMaps, Ingresses, and more. Those files collectively define the desired state of your application and its infrastructure.

Example repository tree:

* `manifests/deployment.yml`
* `manifests/service.yml`
* `manifests/configmap.yml`
* `manifests/ingress.yml`

Why desired state matters:

* It provides a single, reviewable definition of intent.
* Enables reproducible environments across clusters and teams.
* Makes it possible to detect and correct divergences.

<Frame>
  <img alt="The image displays Kubernetes YAML manifest files, including deployment.yml, service.yml, configmap.yml, and ingress.yml, representing different components of a deployment setup. It shows a GitHub logo indicating the source directory for these manifests." />
</Frame>

## State drift

State drift happens when the actual cluster state diverges from the desired state in Git. Drift leads to unexpected behavior, complicates troubleshooting, and can open security or stability gaps.

Example scenario:

* Desired state in Git specifies 5 replicas for a Deployment (declared in `deployment.yml`).
* Someone runs an imperative command that scales the Deployment to 3 replicas.

Deployment (desired in Git)

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
  labels:
    app: nginx-deployment
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
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
```

Imperative change made in cluster

```bash theme={null}
kubectl scale deployment nginx-app --replicas=3
```

Now the cluster has three replicas while Git declares five — that divergence is state drift.

> **warning** Avoid ad-hoc imperative changes in production clusters. They create drift that breaks the one source of truth model and can undermine automated reconciliation.

## State reconciliation

State reconciliation detects drift and brings the actual state back in line with the desired state. Reconciliation is the GitOps control loop: Observe -> Diff -> Act.

* Observe: the operator reads desired manifests from Git and inspects the running cluster.
* Diff: it computes the differences between desired and actual states.
* Act: it applies the needed changes to reconcile the cluster to the declared state.

Using Flux or Argo CD, the operator will detect the replica mismatch and create two additional Nginx pods to return the replica count to five.

Why reconciliation matters:

* Self-healing: automatic correction improves availability.
* Consistency: ensures the running system matches declared configuration.
* Reduced manual intervention: operators fix drift without human action.

<Frame>
  <img alt="The image illustrates a &#x22;State Reconciliation&#x22; process involving a circular flow of &#x22;Observe,&#x22; &#x22;Diff,&#x22; and &#x22;Act&#x22; to align the &#x22;Desired State&#x22; from Git with the &#x22;Actual State&#x22; in a Kubernetes cluster." />
</Frame>

## GitOps-managed software system

A GitOps-managed software system is any system (Kubernetes clusters, applications, or infrastructure) controlled via GitOps principles. The Git repository becomes the single source of truth for namespaces, RBAC, Helm charts, deployments, services, and add-ons (for example Prometheus). All changes are made by editing the repository; a GitOps operator ensures those changes are applied automatically.

<Frame>
  <img alt="The image illustrates a GitOps Managed Software System, showing the flow from Git repositories (with Kubernetes manifests, Helm charts, Terraform, and Ansible files) to a GitOps operator, which then manages deployments across cloud services like Azure, Google Cloud, AWS, and Kubernetes." />
</Frame>

## State store

The state store is the centralized repository holding the definitive desired state—most commonly Git. It contains all configuration and manifests, and acts as the authoritative record of system intent.

Why a state store matters:

* Single source of truth: Git is the authoritative record of system state.
* History and audit: every change is tracked and reviewable.
* Collaboration: teams use pull requests, code review, and branching workflows.

<Frame>
  <img alt="The image illustrates a diagram showing a Git-based single source of truth for managing configurations and code, involving developers, operators, and CI systems like Jenkins, with directories for Kubernetes manifests, Helm charts, Terraform, and Ansible." />
</Frame>

Note: Some GitOps patterns use OCI artifact registries to store declarative artifacts (e.g., OCI images or bundles) and may treat those registries as a form of state store.

## Feedback loop

The feedback loop closes the cycle between deployment and operation. It uses observability signals (metrics, logs, alerts) to inform stakeholders and to trigger fixes or rollbacks in Git.

Typical feedback flow:

1. GitOps operator deploys a new version from Git.
2. Monitoring (Prometheus) detects increased error rates.
3. Visualization (Grafana) surfaces the issue.
4. Alertmanager sends notifications (email, Slack).
5. Teams revert or fix the change in Git, triggering reconciliation back to a healthy state.

<Frame>
  <img alt="The image depicts a feedback loop in a software deployment process, showing interactions between a bot, a version control system, a Kubernetes cluster, and a monitoring stack (Prometheus, Grafana, Alert Manager). It illustrates pulling, deploying, adjusting, and informing stages within this loop." />
</Frame>

Why the feedback loop matters:

* Detect problems early using automated observability.
* Close the loop from runtime signals back to the desired configuration.
* Iterate quickly and safely using operational data.

## Rollback

Rollbacks let you quickly undo problematic changes, either manually via Git or automatically via GitOps tooling.

Common rollback methods:

| Method             | When to use                                                               | Example                                        |
| ------------------ | ------------------------------------------------------------------------- | ---------------------------------------------- |
| Git revert         | Manual, precise undo while preserving history                             | `git revert <commit-hash>`                     |
| Automated rollback | Configure GitOps tool to revert on failed health checks or failed deploys | Argo CD or Flux health/rollback configurations |

Example: revert a bad commit

```bash theme={null}
