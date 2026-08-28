# Developers manually applied different manifests directly to the cluster:
kubectl apply -f deployment-v2.9.5.yaml
kubectl apply -f deployment-v3.0.1.yaml
kubectl apply -f deployment-v2.8.4.yaml
kubectl apply -f deployment-v2.8.4.yaml
```

This hybrid approach produced cascading failures across three main areas:

* Security risks: Storing Kubernetes credentials outside the cluster to allow an external CI to push changes — plus more people with powerful access — expanded the attack surface.
* Configuration drift: The cluster’s live state diverged from the intended state in Git, undermining reproducibility.
* Unreliable disaster recovery: Because manual, unrecorded changes existed, applying what’s in Git would not restore the true working system after an outage.

<Callout icon="lightbulb">
  Configuration drift: when manual or out-of-band changes cause the live environment to differ from the version-controlled desired state, making reproducibility and recovery unreliable.
</Callout>

<Callout icon="warning">
  Storing cluster credentials outside the cluster or granting widespread kubectl access increases risk. Prefer in-cluster controllers and limited, auditable access.
</Callout>

It was a ticking time bomb. Dasho’s core problem was a breakdown of trust: there was no single, reliable source of truth. That translated into instability and high operational risk.

<Frame>
  <img alt="A slide titled &#x22;Challenges&#x22; showing three colored cards labeled &#x22;Security risks&#x22;, &#x22;Configuration drift&#x22;, and &#x22;Disaster recovery.&#x22; Each card has a matching white icon: a shield with a warning for security, a gear/controls for configuration drift, and stacked servers with a recovery/fire symbol for disaster recovery." />
</Frame>

How do we solve these problems?

The answer is GitOps.

At its core GitOps uses Git as the source of truth. Changes to infrastructure or application configuration are made in Git. A controller inside the cluster continuously reconciles the cluster’s actual runtime state with the desired state in Git. This approach provides auditability, repeatability, and a clear workflow for changes.

The Argo project is the leading open-source toolset for implementing GitOps and related automation on Kubernetes. Below we summarize how the primary Argo components address Dasho’s issues.

## Argo CD

Argo CD is the continuous delivery engine for GitOps on Kubernetes.

* Runs inside the Kubernetes cluster and implements a pull-based reconciliation loop: it watches Git repositories and ensures the cluster matches the desired state declared in Git.
* Keeps credentials in-cluster (as Kubernetes Secrets), avoiding the need to expose cluster credentials to external CI systems.
* Detects configuration drift and can automatically or manually revert out-of-band changes by reapplying the desired state from Git.
* Supports disaster recovery by re-creating cluster state from manifests, Helm charts, and Kustomize resources stored in Git.

## Argo Workflows

Argo Workflows is a Kubernetes-native workflow engine for orchestrating multi-step jobs as containers.

* Define pipelines as steps or DAGs with containerized tasks.
* Use it for build, test, linting, and other CI tasks that run inside Kubernetes, leveraging cluster scale and resource management.
* Integrates with other Argo tools to create complete CI/CD automation.

## Argo Rollouts

Argo Rollouts provides progressive delivery strategies to reduce release risk.

* Supports canary, blue-green, and other progressive deployment patterns.
* Integrates with monitoring and metrics systems (for example, [Prometheus](https://prometheus.io/)) to perform automated analysis during rollouts.
* On metric regressions (e.g., increased error rates), Argo Rollouts can pause or roll back automatically to protect production.

## Argo Events

Argo Events is an event-driven automation framework that connects external signals to in-cluster automation.

* Listens for events from Git pushes, webhooks, S3, message queues, and more.
* Triggers workflows, notifies systems, or initiates Argo CD syncs and Argo Rollouts.
* Enables end-to-end event-driven CI/CD: e.g., a Git push → Argo Events → Argo Workflows build/test → success triggers Argo CD sync and Argo Rollouts deployment.

<Frame>
  <img alt="A presentation slide titled &#x22;Argo Project&#x22; showing four cards labeled ArgoCD, Argo Workflows, Argo Rollouts, and Argo Events. Each card has a colorful octopus/squid-themed illustration (rocket, swirling squid, cube with arrows, and a calendar-like icon)." />
</Frame>

## Argo components at a glance

| Component      | Primary use case                              | Key benefit                                                    |
| -------------- | --------------------------------------------- | -------------------------------------------------------------- |
| Argo CD        | GitOps continuous delivery and reconciliation | Git as single source of truth; drift detection and remediation |
| Argo Workflows | Container-native CI pipelines and batch jobs  | Run CI within Kubernetes with scalable resource control        |
| Argo Rollouts  | Progressive delivery (canary/blue-green)      | Safer releases with automated metric-driven rollback           |
| Argo Events    | Event-driven triggers and automation          | Connect external events to internal automation pipelines       |

## Putting it all together

For Dasho, adopting the Argo suite resolved the major failures:

* Argo CD restored trust by enforcing Git as the authoritative source and eliminating configuration drift.
* Argo Workflows automated build and test steps inside the cluster.
* Argo Rollouts enabled safe, progressive deliveries with metric analysis and automated rollback.
* Argo Events connected external triggers to internal automation, creating a seamless event-driven pipeline.

The result: a shift from a chaotic, fragile environment to an automated, secure, and resilient cloud-native platform. This journey from chaos to control is exactly why the Argo Project is a foundational toolset for modern software delivery.

<Frame>
  <img alt="A presentation slide titled &#x22;Conclusion&#x22; showing a vertical timeline with four colorful numbered points summarizing Argo: enabled automation, security and resilience; transformed chaos into a controlled environment; shifted to a modern cloud-native platform; and is essential for modern software delivery. The layout has a turquoise left panel and the four short conclusions listed to the right." />
</Frame>

## Links and references

* Argo Project: [https://argoproj.github.io/](https://argoproj.github.io/)
* GitOps principles: [https://www.gitops.tech/](https://www.gitops.tech/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Prometheus (metrics integration): [https://prometheus.io/](https://prometheus.io/)
* Argo CD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Argo Workflows documentation: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Argo Rollouts documentation: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)
* Argo Events documentation: [https://argoproj.github.io/argo-events/](https://argoproj.github.io/argo-events/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/8b9dba71-6748-4303-8dfa-a0b59b1260ed" />
</CardGroup>


# Demo Application Custom Health Check

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Application-Custom-Health-Check/page

Guide to add Argo CD custom Lua health checks for ConfigMap driven demos to mark application health based on ConfigMap values and resolve degraded states

This guide shows how to add a custom health check in Argo CD that validates a ConfigMap and influences the health status of an Argo CD Application. Argo CD includes many built-in health assessments for standard Kubernetes resources, but you can extend these checks by adding small Lua scripts to the Argo CD config (argocd-cm ConfigMap).

<Frame>
  <img alt="A screenshot of the Argo CD documentation web page showing the &#x22;Resource Health&#x22; section with an overview and checks for Kubernetes resources. The page includes a left navigation menu and a right-side table of contents." />
</Frame>

## How Argo CD custom health checks work

Custom health checks are Lua snippets stored in the argocd-cm ConfigMap under keys following a naming convention. Argo CD executes these scripts for matching resources and expects a table with at least a `status` field (e.g., "Healthy", "Degraded", "Progressing") and an optional `message`.

Key naming examples:

| Key format                                          | Applies to                | Example                                                  |
| --------------------------------------------------- | ------------------------- | -------------------------------------------------------- |
| resource.customizations.health.\<apiGroup>\_\<Kind> | Resources in an API group | `resource.customizations.health.argoproj.io_Application` |
| resource.customizations.health.\<Kind>              | Core group resources      | `resource.customizations.health.ConfigMap`               |

Example: a Lua health script for the Argo CD Application resource that reads the Application status if present:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-cm
    app.kubernetes.io/part-of: argocd
data:
  resource.customizations.health.argoproj.io_Application: |
    hs = {}
    hs.status = "Progressing"
    hs.message = ""
    if obj.status ~= nil then
      if obj.status.health ~= nil then
        hs.status = obj.status.health.status
        if obj.status.health.message ~= nil then
          hs.message = obj.status.health.message
        end
      end
    end
    return hs
```

## Demo application overview

This demo repository contains an application named `health-check` that demonstrates a ConfigMap-driven scenario:

* ConfigMap: `moving-shapes-colors` — defines color values for shapes.
* Deployment: `random-shapes` — loads the ConfigMap via `envFrom`.
* Service: exposes the application.

Example ConfigMap used by the application (note the TRIANGLE\_COLOR intentionally set to "white", which we use to trigger a Degraded health state):

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: moving-shapes-colors
data:
  CIRCLE_COLOR: "pink"
  OVAL_COLOR: "lightgreen"
  SQUARE_COLOR: "orange"
  TRIANGLE_COLOR: "white"  # using white will produce a Degraded message in Argo CD
  RECTANGLE_COLOR: "blue"
```

Deployment that consumes the ConfigMap via envFrom:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: random-shapes
spec:
  selector:
    matchLabels:
      app: random-shapes
  replicas: 1
  template:
    metadata:
      labels:
        app: random-shapes
    spec:
      containers:
      - name: random-shapes
        image: siddharth67/php-random-shapes:v1
        imagePullPolicy: Always
        envFrom:
        - configMapRef:
            name: moving-shapes-colors
```

## Create the Argo CD Application

Create an Argo CD Application that points to the `health-check` path in the git repo, targets the namespace `health-check`, and asks Argo CD to create the namespace. If you are not logged in to the argocd server the create command can fail — log in first if necessary.

Attempt to create the app (may fail if not logged in):

```bash theme={null}
argocd app create health-check-app \
  --repo http://host.docker.internal:5000/kk-org/gitops-argocd-capa \
  --path ./health-check \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace health-check \
  --project default \
  --revision HEAD \
  --sync-policy none \
  --sync-option CreateNamespace=true
```

If it fails due to authentication, log in to Argo CD (example):

```bash theme={null}
argocd login localhost:31148 --plaintext --insecure
