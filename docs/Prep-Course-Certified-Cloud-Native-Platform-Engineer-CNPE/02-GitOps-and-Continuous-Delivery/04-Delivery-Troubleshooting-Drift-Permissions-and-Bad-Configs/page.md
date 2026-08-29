# Chart.yaml
apiVersion: v2
name: myapp
version: 0.1.0
```

```yaml theme={null}
# values.yaml
replicaCount: 1
image:
  repository: myapp
  tag: v1.0.0
```

```yaml theme={null}
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Chart.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

Rendering the chart with a different values file (for example `values-prod.yaml`) produces plain Kubernetes YAML with substituted values. Helm is particularly useful for:

* Packaging third-party applications (Prometheus, cert-manager)
* Reusing community charts
* Complex manifests that require logic

<Frame>
  <img alt="The image describes the strengths and challenges of the Helm template engine. Strengths include rich templating and a large chart ecosystem, while challenges involve learning curve and debugging complexity." />
</Frame>

## Kustomize (patch-driven)

* Kustomize starts from valid Kubernetes YAML "bases" and applies declarative overlays (patches) per environment.
* Since base manifests are valid YAML, you can `kubectl apply -f base/` directly — bases are not templates.
* Overlays are focused: change the image tag, set replicas, add labels, or merge small diffs via patches. Kustomize is usually easier to read and debug for teams that prefer plain YAML.
* Limitation: no native loops or conditionals. Very complex transformations can become verbose.

Example Kustomize layout and files:

```text theme={null}
my-app/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        ├── kustomization.yaml
        └── replicas-patch.yaml
```

```yaml theme={null}
# base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:latest
```

```yaml theme={null}
# base/kustomization.yaml
resources:
  - deployment.yaml
  - service.yaml
```

```yaml theme={null}
# overlays/prod/kustomization.yaml
resources:
  - ../../base
images:
  - name: myapp
    newTag: v2.1.0
patchesStrategicMerge:
  - replicas-patch.yaml
```

```yaml theme={null}
# overlays/prod/replicas-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5
```

Render the overlay with:

```bash theme={null}
kubectl kustomize overlays/prod
```

Kustomize emphasizes small, explicit patches to an otherwise valid base. It’s built into `kubectl`, so extra tooling is often unnecessary. For many teams this makes debugging and review simpler.

## Trade-offs and guidance

Use the right tool for the right job:

* Helm
  * Best when you need expressive templating (loops, conditionals)
  * Ideal for packaging and installing third-party apps
  * Use when you want versioned charts and community ecosystem support
* Kustomize
  * Best when you prefer base manifests to remain valid YAML
  * Ideal for in-house services and small environment-specific patches
  * Simpler to read and debug for teams managing their own manifests

Many teams adopt a hybrid approach: use Helm for packaged third-party applications and Kustomize for internal service manifests. Both are supported by GitOps tools (Argo CD, Flux), so workflows can accommodate either or both.

<Frame>
  <img alt="The image is a comparison chart between Helm and Kustomize, highlighting their different approaches, base files, conditionals/loops, package ecosystem, and best use cases." />
</Frame>

Comparison table: Helm vs Kustomize

| Area              | Helm (templating)                            | Kustomize (patching)                           |
| ----------------- | -------------------------------------------- | ---------------------------------------------- |
| Primary approach  | Generate YAML from Go templates              | Patch valid YAML bases                         |
| Best for          | Complex parameterization, third-party charts | Simple environment patches, in-house manifests |
| Templates / Logic | Loops, conditionals, functions               | No native loops or conditionals                |
| Ecosystem         | Large chart repository (Artifact Hub)        | Lightweight, built-in to kubectl               |
| Debuggability     | Can be harder to read for complex templates  | Easier to inspect resulting YAML and patches   |
| Packaging         | Chart packaging & versioning                 | No chart packaging; use Git structure          |

Further reading and references

* Helm documentation and charts: [https://artifacthub.io/](https://artifacthub.io/)
* Kustomize and `kubectl kustomize`: [https://kubernetes.io/docs/reference/kubectl/overview/](https://kubernetes.io/docs/reference/kubectl/overview/)
* GitOps with Argo CD: [https://learn.kodekloud.com/user/courses/gitops-with-argocd](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* GitOps with Flux CD: [https://learn.kodekloud.com/user/courses/gitops-with-fluxcd](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd)
* Helm for Beginners course: [https://learn.kodekloud.com/user/courses/helm-for-beginners](https://learn.kodekloud.com/user/courses/helm-for-beginners)
* Kustomize course: [https://learn.kodekloud.com/user/courses/kustomize](https://learn.kodekloud.com/user/courses/kustomize)

## Summary

* Never manage multiple environments by copying YAML files.
* Helm generates YAML from Go templates and excels at expressive parameterization and packaging third-party apps.
* Kustomize patches valid YAML bases and is a good fit for readable overlays and simple environment changes.
* Both integrate with GitOps tools; choose the approach that best fits the team, the application, and operational needs.

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/dff5382b-dbe7-4cac-bd2b-d5a47028945e/lesson/dd65e2cc-6e0c-487f-ac70-31523af5309e)


# Delivery Troubleshooting Drift Permissions and Bad Configs

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/GitOps-and-Continuous-Delivery/Delivery-Troubleshooting-Drift-Permissions-and-Bad-Configs/page

Guide to diagnosing and resolving Argo CD GitOps delivery failures focusing on drift, RBAC permissions, and invalid manifests with diagnostic commands and remediation steps

Everything we've covered so far assumes sync will succeed. When it doesn't, diagnosing the failure quickly is critical. Argo CD applications reported as OutOfSync or SyncFailed usually fall into three categories:

* Drift (external controllers or manual changes)
* Permissions (RBAC / service account limitations)
* Invalid configurations (bad manifests, missing CRDs, missing namespaces)

This guide provides a compact, systematic troubleshooting toolkit with the key diagnostic commands and remediation steps to resolve most GitOps delivery failures.

Three categories cover about ninety percent of GitOps failures. For each category you'll find: the diagnostic question, quick commands to inspect the problem, and typical remediation patterns.

<Frame>
  <img alt="The image lists four learning objectives related to resolving technical issues, validating manifests, and using specific tools and commands effectively. The objectives are visually highlighted with numbered tags on a gradient background." />
</Frame>

Real-world example
A platform team repeatedly synced an Argo CD application. Git matched the desired manifests, the cluster was reachable, and each sync initially succeeded — but within seconds the app returned to OutOfSync. Root cause: an HPA controlling replicas. Git declared `spec.replicas: 3`, while the HPA scaled the Deployment to 7. Argo CD reconciled the Deployment back to 3; the HPA then bumped it to 7, causing a continuous drift loop.

Key lesson: not every difference between Git and the cluster is an error. Controllers (HPAs, operators) and the API server often mutate objects. Recognize expected drift and tell Argo CD what to ignore.

Common symptoms and usual causes

* Perpetual OutOfSync — often drift from HPAs, operators, or manual edits that continuously change cluster state.
* SyncFailed — typically permission problems: Argo CD cannot create/update/delete resources.
* Degraded / Progressing — resources were applied but are not becoming healthy; usually bad configurations (image pull errors, insufficient resources, missing dependencies).
* Unknown health — Argo CD cannot determine health for a resource type, often because CRDs or health checks are missing.

<Frame>
  <img alt="The image outlines four common symptoms of sync failures: Perpetual OutOfSync, SyncFailed, Degraded/Progressing, and Unknown, along with their potential causes." />
</Frame>

Quick reference: symptoms → likely cause → first diagnostic command

|                Symptom | Likely cause                                    | First diagnostic command                                      |
| ---------------------: | ----------------------------------------------- | ------------------------------------------------------------- |
|    Perpetual OutOfSync | Drift (HPA, operator, controller, manual edits) | `argocd app diff <app>`                                       |
|             SyncFailed | RBAC / permissions                              | `kubectl auth can-i ... --as=system:serviceaccount:<ns>:<sa>` |
| Degraded / Progressing | Bad manifests, image pull, resources            | `kubectl describe <resource>` / `kubectl logs`                |
|         Unknown health | Missing CRD / custom health checks              | `kubectl get crd` / check Argo CD health overrides            |

Diagnosis and remediation — start with the most common: drift

Drift (most common cause of perpetual OutOfSync)

* Diagnostic question: Why does my app stay OutOfSync even after syncing?
* Diagnostic tool: Argo CD diff (UI or CLI Diff tab) to see field-by-field differences between Git and live cluster.

Example CLI:

```bash theme={null}
