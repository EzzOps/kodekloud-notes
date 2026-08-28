# (...)
```

<Callout icon="lightbulb">
  The clusters generator reads cluster Secrets in the argocd namespace and exposes fields like `.name` and `.server`. Reference these generated parameters in your ApplicationSet template to target destinations automatically.
</Callout>

When you manage dozens of clusters, the clusters generator significantly reduces maintenance compared to manually updating a list generator.

## Example: Deploy nginx to all clusters

This ApplicationSet example uses the clusters generator to deploy an nginx application to every cluster Argo CD knows about:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: common-nginx-server
  namespace: argocd
spec:
  goTemplate: true
  generators:
    - clusters: {}
  template:
    metadata:
      name: '{{ .name }}-nginx-server'
    spec:
      project: default
      source:
        repoURL: http://host.docker.internal:5000/kk-org/gitops-argocd-capa
        targetRevision: HEAD
        path: ./nginx-app
      destination:
        server: '{{ .server }}'
        namespace: nginx-server
      syncPolicy:
        automated: {}
        syncOptions:
          - CreateNamespace=true
```

Notes:

* `generators: - clusters: {}` tells Argo CD to generate one Application per discovered cluster.
* The template uses `.name` for each generated Application’s name and `.server` for the destination cluster server URL (both supplied by cluster Secrets).

## Applying the ApplicationSet and troubleshooting

If you attempt to apply an ApplicationSet before the ApplicationSet CRD and controller are installed, the apply will fail with a "no matches for kind" error.

Example failure when CRDs are missing:

```console theme={null}
kubectl -n argocd apply -f https://gist.github.com/sidd-[SECRET_REDACTED]/[AWS_SECRET_ACCESS_KEY]/application-set-nginx.yml
error: resource mapping not found for name: "common-nginx-server" namespace: "argocd" from "https://gist.github.com/sidd-[SECRET_REDACTED]/[AWS_SECRET_ACCESS_KEY]/application-set-nginx.yml": no matches for kind "ApplicationSet" in version "argoproj.io/v1alpha1"
ensure CRDs are installed first
```

Check for CRDs:

```console theme={null}
kubectl get crds
No resources found
```

<Callout icon="warning">
  If you target the wrong kubecontext (for example, a cluster without Argo CD installed), kubectl will not find the ApplicationSet CRD. Switch to the context that hosts Argo CD (e.g., your Docker Desktop or kind cluster) and re-run the apply after ensuring the ApplicationSet CRD and controller are installed.
</Callout>

After switching to the correct context and ensuring the CRDs/controller are present, applying the ApplicationSet should succeed and create the ApplicationSet resource:

```console theme={null}
kubectl -n argocd apply -f https://gist.github.com/sidd-[SECRET_REDACTED]/[AWS_SECRET_ACCESS_KEY]/application-set-nginx.yml
applicationset.argoproj.io/common-nginx-server created

kubectl get applicationsets -n argocd
NAME                  AGE
common-nginx-server   1m

kubectl describe applicationset common-nginx-server -n argocd
# (excerpted)
Repo URL:        http://host.docker.internal:5000/kk-org/gitops-argocd-capa
Target Revision: HEAD
Sync Policy:
  Automated:
  Sync Options:
    CreateNamespace=true
Status:
  Conditions:
    - Type: ParametersGenerated
      Status: "True"
      Reason: ParametersGenerated
      Message: Successfully generated parameters for all Applications
    - Type: ResourcesUpToDate
      Status: "True"
      Reason: ApplicationSetUpToDate
      Message: ApplicationSet up to date
Events:
  Type    Reason    Age   From                         Message
  ----    ------    ---   ----                         -------
  Normal  created   18s   applicationset-controller    created Application "in-cluster-nginx-server"
  Normal  created   17s   applicationset-controller    created Application "kind-argo-cluster-1-nginx-server"
```

The events show that Applications were generated — one per discovered cluster.

## Verify in the Argo CD UI

Inspect the generated Applications in the Argo CD web UI. Use search and filters to locate the nginx applications deployed across your clusters.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing an applications dashboard with a search dropdown and a list of Kubernetes apps. The left sidebar shows navigation and sync/health filters while the main pane lists app names, projects, source/destination info and health/sync status badges." />
</Frame>

In this example the UI shows multiple nginx Applications — one for the in-cluster destination and another for the kind cluster. Using a single ApplicationSet with the clusters generator lets you create identical Applications targeted to multiple clusters automatically.

## Further reading and references

* Official ApplicationSet docs: [https://argoproj.github.io/argo-cd/operator-manual/applicationset/](https://argoproj.github.io/argo-cd/operator-manual/applicationset/)
* Argo CD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* ApplicationSet controller repo and examples: [https://github.com/argoproj-labs/applicationset](https://github.com/argoproj-labs/applicationset)

That's all for this lesson — you should now be able to choose between the list and clusters generators and deploy workloads across multiple clusters using a single ApplicationSet.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/db742489-0b3a-459a-9d8d-0d6fb616dff7" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/007a37af-9773-4611-aefe-44fc62967b92" />
</CardGroup>


# Demo ArgoCD Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-ArgoCD-Installation/page

Guide to installing and configuring Argo CD on a Kubernetes cluster, exposing the server locally, retrieving initial admin credentials, and updating the default password.

This guide walks through installing Argo CD on a Kubernetes cluster, exposing the Argo CD server for local access, logging into the web UI, and updating the initial admin password. It includes commands, verification steps, example outputs, and screenshots to help you quickly get started with Argo CD.

## Prerequisites

* A working Kubernetes cluster (example uses Docker Desktop with Kubernetes).
* kubectl configured to target the cluster.
* Internet access to fetch the Argo CD manifests from GitHub.

## Install Argo CD (stable)

To install the latest stable release of Argo CD, create the `argocd` namespace and apply the stable install manifest:

```bash theme={null}
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Install a specific Argo CD version

If you need a particular release, point to the release tag on GitHub. Below are example commands for installing Argo CD v3.1.5 in either non-HA or HA mode.

```bash theme={null}
