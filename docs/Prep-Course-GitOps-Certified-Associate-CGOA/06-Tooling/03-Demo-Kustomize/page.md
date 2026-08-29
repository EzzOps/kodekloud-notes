# Optional resource configuration:
# resources:
#   limits:
#     cpu: 100m
#     memory: 128Mi
#   requests:
#     cpu: 100m
#     memory: 128Mi
```

Using templates + `values.yaml` enables you to:

* Reuse the same chart across environments (dev/staging/prod) by swapping values.
* Maintain a single source of truth for manifests while customizing behavior with values or overrides.
* Keep configuration in Git to satisfy GitOps principles and enable auditability.

Because the chart lives in a Git repository, it aligns with GitOps best practices. Continuous delivery tools like [Argo CD](https://learn.kodekloud.com/user/courses/gitops-with-argocd) or [Flux CD](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd) can render the chart and continuously reconcile the cluster to the desired state.

<Frame>
  <img alt="The image shows the Argo CD dashboard displaying several applications with their health status marked as &#x22;Healthy&#x22; and &#x22;Synced.&#x22; Each application card includes details like project, repository, and last sync time." />
</Frame>

## Deploying a Helm chart with Argo CD

Argo CD can deploy a Helm chart directly from a Git repo. In the Argo CD UI you typically:

1. Create a new Application.
2. Point `repoURL` to your Git repository and `path` to the chart folder (e.g., `manifests/helm/highway-chart`).
3. Choose a target cluster/namespace and optional automated sync policy.
4. Provide `values.yaml` or overrides if you want to change defaults at deploy time.

<Frame>
  <img alt="The image shows a user interface for configuring application settings in Argo CD, including options for sync policy and other settings." />
</Frame>

Argo CD recognizes the Helm chart and prompts for values files or overrides. Point it at the chart’s `values.yaml` or supply a custom override file to change runtime configuration.

<Frame>
  <img alt="The image shows the Argo CD interface, displaying a form for creating or managing applications, with details about the Git repository and destination cluster URL." />
</Frame>

Once created, Argo CD renders the Helm chart and creates the Kubernetes resources — e.g., Deployment, Service, and Pods configured by `values.yaml`. With the example above (replicaCount: 1) you will initially see a single pod.

<Frame>
  <img alt="The image shows an Argo CD web interface displaying the details of a synced application, including its health and sync status, within a graphical resource tree view." />
</Frame>

## Updating configuration: Git vs UI overrides

You can change chart configuration in two common ways:

* Edit `values.yaml` in the Git repository and let Argo CD pick up the change via GitOps sync, or
* Provide overrides in the Argo CD Application (UI or Application manifest), which are useful for temporary or environment-specific changes.

Example Argo CD Application manifest that references a Helm chart and passes a values file and parameter overrides:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: helm-demo-app
spec:
  project: default
  source:
    repoURL: http://host.docker.internal:5000/kk-org/cgoa-demos
    path: manifests/helm/highway-chart
    targetRevision: HEAD
    helm:
      valueFiles:
        - values.yaml
      parameters:
        - name: replicaCount
          value: "7"
        - name: image.tag
          value: "green"
        - name: service.type
          value: "NodePort"
  destination:
    server: https://kubernetes.default.svc
    namespace: helm-demo-app
  syncPolicy:
    automated: {}
    syncOptions:
      - CreateNamespace=true
```

<Frame>
  <img alt="The image shows the Argo CD user interface displaying details of a Helm demo application. Options such as sync settings, retry options, and application status are visible." />
</Frame>

You can also edit parameters from the Argo CD UI. For example, change `replicaCount` to `7`, set `image.tag` to `green`, or update other values. After saving, Argo CD will detect a drift (OutOfSync) between the live cluster and the desired state.

<Frame>
  <img alt="The image shows a screenshot of an Argo CD application interface with parameters set for a Helm chart, including container port, environment variables, image repository, and replica count." />
</Frame>

Argo CD shows diffs between live manifests and desired manifests (e.g., `replicas: 1` vs `replicas: 7`, changed image tags, or modified env vars). When you run a sync, Argo CD applies the updated manifests to the cluster.

<Frame>
  <img alt="The image shows a user interface of the Argo CD application dashboard, displaying the sync status and health of a &#x22;helm-demo-app&#x22; and related services in a flowchart format. The &#x22;helm-demo-app&#x22; is marked as &#x22;OutOfSync&#x22; while its health status is &#x22;Healthy.&#x22;" />
</Frame>

If a sync gets stuck or an operation must be interrupted, Argo CD provides controls to terminate and re-trigger operations.

<Frame>
  <img alt="The image shows a software application interface with a pop-up dialog asking if the user wants to terminate an operation. It also displays system status information related to a sync operation." />
</Frame>

After a successful sync, the cluster reflects the updated values (for example, `replicaCount: 7` results in 7 running pods). If something doesn’t render properly in the Argo CD UI (for example, quoting/format issues), check your YAML formatting in the override editor and prefer properly formatted YAML.

<Frame>
  <img alt="The image displays a web interface of Argo CD, detailing the &#x22;helm-demo-app&#x22; with its application health and sync status, along with a visual representation of the application's components and their health states." />
</Frame>

A consistent values override you can paste into Argo CD’s editor:

```yaml theme={null}
replicaCount: 9
image:
  tag: "green"
env:
  - name: POD_COUNT
    value: "9"
```

With that override and a sync, the cluster will run nine pods using the updated image tag and environment variable.

> **lightbulb** Tip: Keep configuration as code in Git (edit `values.yaml` in your repo) so changes remain auditable and follow GitOps best practices. Use Argo CD parameters or UI overrides for temporary or environment-specific adjustments.

## Summary

Helm templates + `values.yaml` let you templatize Kubernetes manifests for reuse and consistency. Pairing Helm with Argo CD creates a GitOps workflow: store charts and values in Git, let Argo CD render and deploy them, and update configuration through Git or controlled UI overrides to reconcile clusters to the desired state.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/521f8b23-4b5d-47d4-961f-c184187a8b71)


# Demo Kustomize

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/Tooling/Demo-Kustomize/page

Guide to using Kustomize to manage Kubernetes manifests with environment overlays and deploying them via Argo CD in a GitOps workflow.

This guide demonstrates a template-free way to manage Kubernetes manifests using Kustomize, and how to deploy those manifests with Argo CD in a GitOps workflow. You'll learn how to structure a repository with a canonical base and environment-specific overlays, patch resources with strategic merges, and create Argo CD Applications that point to overlay paths to keep clusters in sync.

Repository layout

* The repo contains a `manifest` folder with two top-level directories: `helm` and `kustomize`.
* Inside `kustomize` there are `base` and `overlays` folders. `base` holds canonical manifests (Deployment, Service, Namespace) and a `kustomization.yml`. `overlays` include environment-specific patches (e.g., `dev`, `prod`) that Kustomize applies on top of the base.

<Frame>
  <img alt="The image shows a directory structure of a project, likely involving Kubernetes configurations, with folders and YAML files under &#x22;base&#x22; and &#x22;overlays/dev&#x22; paths. It includes files like &#x22;deployment.yml,&#x22; &#x22;service.yml,&#x22; and other Kustomize-related files." />
</Frame>

Base kustomization

* The `base/kustomization.yml` lists the core manifests to be managed as the canonical source:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yml
  - service.yml
  - namespace.yml
```

Base Deployment (canonical)

* `base/deployment.yml` defines the default configuration: image tag `blue`, labels, and a single replica:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
spec:
  replicas: 1
  selector:
    matchLabels:
      app: highway-animation
  template:
    metadata:
      labels:
        app: highway-animation
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:blue
          ports:
            - containerPort: 3000
          env:
            - name: POD_COUNT
              value: "1"
```

Overlays concept

* Overlays reference the `base` and apply environment-specific changes using Kustomize patches and per-overlay kustomization files (for example, `overlays/dev/kustomization.yml` and `overlays/prod/kustomization.yml`).
* Typical overlay changes include replica counts, environment variables, image tags, and namespace assignments.

Dev overlay

* `overlays/dev/kustomization.yml` points to the base and applies two patches (replica and env), and forces resources into the `kustomize-dev` namespace:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
namespace: kustomize-dev
patches:
  - path: replica-patch.yml
    target:
      kind: Deployment
      name: highway-animation
  - path: env-patch.yml
    target:
      kind: Deployment
      name: highway-animation
```

Dev patch: replicas

* `overlays/dev/replica-patch.yml` sets the dev replica count:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
spec:
  replicas: 2
```

Dev patch: env

* `overlays/dev/env-patch.yml` updates the container environment variable. Note that the container `name` must match the base so Kustomize can perform a strategic merge correctly:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
spec:
  template:
    spec:
      containers:
        - name: highway-animation
          env:
            - name: POD_COUNT
              value: "2"
```

> **lightbulb** Kustomize performs a strategic merge when applying patches. Always include the container `name` in your patch when modifying container-level fields (`env`, `image`, `ports`, etc.) so Kustomize can match and update the correct container.

Prod overlay

* `overlays/prod/kustomization.yml` references the same base, sets `kustomize-prod` as the namespace, and applies three patches (replicas, env, image):

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
namespace: kustomize-prod
patches:
  - path: replica-patch.yml
    target:
      kind: Deployment
      name: highway-animation
  - path: env-patch.yml
    target:
      kind: Deployment
      name: highway-animation
  - path: image-patch.yml
    target:
      kind: Deployment
      name: highway-animation
```

Prod patches (examples)

* Replica patch (`overlays/prod/replica-patch.yml`):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
spec:
  replicas: 5
```

* Env patch (`overlays/prod/env-patch.yml`):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
spec:
  template:
    spec:
      containers:
        - name: highway-animation
          env:
            - name: POD_COUNT
              value: "5"
```

* Image patch (`overlays/prod/image-patch.yml`):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
spec:
  template:
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:green
```

Deploying with Argo CD (GitOps)

* With overlays in Git, create an Argo CD Application per environment that targets the overlay path (for example, `manifest/kustomize/overlays/dev` for dev).
* Recommended Argo CD settings:
  * App name: `kustomize-dev` (or `kustomize-prod` for production)
  * Repo path: `manifest/kustomize/overlays/dev` (or `.../overlays/prod`)
  * Sync policy: automatic (if you want continuous reconciliation)
  * Option: enable auto-create namespace (or let Kustomize create it via `namespace.yml` in `base`)

Argo CD will render the kustomization, apply the base plus selected overlays, and continuously reconcile the cluster to match Git state.

<Frame>
  <img alt="The image shows the Argo CD application interface, where a user is configuring an application with options for sync policy, project name, and various sync settings." />
</Frame>

Dev application example (live)

* Creating the Argo CD Application for `overlays/dev` results in Argo CD applying:
  * The base resources
  * The dev overlay patches (replicas and env)
  * The `kustomize-dev` namespace (if configured)
* The Application should show as Synced and Healthy after the cluster converges.

<Frame>
  <img alt="The image shows an Argo CD user interface displaying the status and structure of a Kubernetes application named &#x22;kustomize-dev.&#x22; The application is healthy and synced, as depicted in a visual graph layout." />
</Frame>

What you should observe

* The base Deployment had `replicas: 1` and `POD_COUNT: "1"`.
* The dev overlay patches change replicas to `2` and `POD_COUNT` to `"2"`.
* The prod overlay sets replicas to `5`, `POD_COUNT` to `"5"`, and updates the image to `green`.

Comparison at a glance

| Resource / Field           |                                 Base |                   Dev overlay result |                   Prod overlay result |
| -------------------------- | -----------------------------------: | -----------------------------------: | ------------------------------------: |
| Namespace                  |                    default (or none) |                      `kustomize-dev` |                      `kustomize-prod` |
| `replicas`                 |                                  `1` |                                  `2` |                                   `5` |
| `POD_COUNT` env var        |                                `"1"` |                                `"2"` |                                 `"5"` |
| Image                      | `siddharth67/highway-animation:blue` | `siddharth67/highway-animation:blue` | `siddharth67/highway-animation:green` |
| Example NodePort (Service) |                                    — |                    `30906` (example) |                     `30247` (example) |

Live Deployment excerpt (dev)

* The live Deployment in `kustomize-dev` will reflect the merged configuration:

```yaml theme={null}
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:blue
          env:
            - name: POD_COUNT
              value: '2'
status:
  availableReplicas: 2
  readyReplicas: 2
  replicas: 2
  updatedReplicas: 2
```

Accessing the application

* If the Service is exposed via NodePort, use the node IP and NodePort (for example, `http://<NODE_IP>:30906`) to reach the dev application.
* Dev pods will use the `blue` image; prod pods will use `green` if the prod image patch is applied.

Production deployment notes

* Create a separate Argo CD Application pointing at `manifest/kustomize/overlays/prod`. Argo CD will apply prod patches: `replicas: 5`, `POD_COUNT: "5"`, and `image: ...:green`. The live prod Deployment will reflect these changes and scale accordingly.

Summary and best practices

* Kustomize enables one canonical base with environment-specific overlays—no templating required.
* Use strategic merge patches in overlays to modify the base; include `containers[].name` when patching container fields to ensure accurate merges.
* Use Argo CD to point to overlay paths so each environment is an independent Argo CD Application that continuously reconciles Git → cluster (GitOps).
* Organize overlays clearly (e.g., `dev`, `staging`, `prod`) and keep patches small and focused (replicas, env, image).

> **lightbulb** When writing [Kustomize](https://learn.kodekloud.com/user/courses/kustomize) patches that modify container fields (env, image, etc.), include the container `name` in the patch so Kustomize can match and merge the correct container entry.

That's all for now.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/24630e6a-9f49-42d1-abd0-75bafc02ce01/lesson/3a500485-031d-44b4-b718-2c13f00d916b)
