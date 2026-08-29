# Demo ApplicationSet Cluster Generator

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-ApplicationSet-Cluster-Generator/page

How to use Argo CD ApplicationSet generators, especially list and clusters, to automatically create and deploy Applications across multiple clusters, with an nginx demo

In this guide you'll learn how a single ApplicationSet can generate multiple Argo CD Applications across several clusters by using generators. We focus on the list and clusters generators, showing examples and a practical demo that deploys an nginx application to all clusters known to Argo CD.

ApplicationSets use generators to produce parameter sets which are rendered into the ApplicationSet template. Generators available include list, clusters, git, matrix, merge, and others. This article demonstrates the list and clusters generators and walks through deploying an nginx app across multiple clusters using the clusters generator.

## Overview: ApplicationSet generators

Use generators to produce parameter combinations for the ApplicationSet template. Typical use-cases:

| Generator | Use case                                                                                   |
| --------- | ------------------------------------------------------------------------------------------ |
| list      | Explicitly enumerate targets (key/value pairs). Best for small, known sets.                |
| clusters  | Discover clusters from Argo CD cluster secrets. Great for many clusters managed centrally. |
| git       | Generate parameters from Git repo contents or branches.                                    |
| matrix    | Combine multiple generators to create Cartesian products of parameters.                    |
| merge     | Merge results from multiple generators into a single parameter set.                        |

For more detail see the official ApplicationSet documentation: [Argo CD ApplicationSet Controller](https://argoproj.github.io/argo-cd/operator-manual/applicationset/).

## List generator

The list generator allows you to explicitly list cluster-like elements (key/value pairs). It's ideal when you have a finite, known set of targets and you want precise control over each generated Application.

Example ApplicationSet using the list generator:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
    - list:
        elements:
          - cluster: engineering-dev
            url: https://kubernetes.default.svc
          # - cluster: engineering-prod
          #   url: https://kubernetes.default.svc
  template:
    metadata:
      name: '{{ .cluster }}-guestbook'
    spec:
      project: my-project
      source:
        repoURL: https://github.com/argoproj/argo-cd.git
        targetRevision: HEAD
        path: applicationset/examples/list-generator/guestbook/{{ .cluster }}
      destination:
        server: '{{ .url }}'
        namespace: guestbook
```

Key points:

* The generator emits parameters (here `.cluster` and `.url`) for each listed element.
* The template uses those parameters to produce distinct Application resources. For example, with `cluster: engineering-dev` the application name becomes `engineering-dev-guestbook`.
* Add another element (e.g., `engineering-prod`) to generate an additional Application.

## Cluster generator

The clusters generator discovers clusters registered with Argo CD (stored as cluster Secrets in the argocd namespace) and generates parameters from those secrets. This is the recommended approach if you manage many clusters and prefer automatic discovery.

A basic clusters generator that selects clusters by label:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
    - clusters:
        selector:
          matchLabels:
            staging: "true"
```

The clusters generator exposes parameters such as `.name`, `.server`, and metadata fields that come from the cluster Secrets Argo CD creates when you add clusters.

<Frame>
  <img alt="A screenshot of the Argo CD documentation page titled &#x22;Cluster Generator,&#x22; showing a left navigation menu, the main content describing cluster parameters and secrets, and a right-hand table of contents. The page explains generated parameter values like name, server, and metadata fields." />
</Frame>

Argo CD stores cluster connection details as Secrets labeled with `argocd.argoproj.io/secret-type: cluster`. An illustrative (decoded) example of such a Secret:

```yaml theme={null}
kind: Secret
metadata:
  labels:
    argocd.argoproj.io/secret-type: cluster
data:
  # In Kubernetes these fields are base64-encoded; shown here decoded for readability.
  config: '{"tlsClientConfig":{"insecure":false}}'
  name: "in-cluster2"
  server: "https://kubernetes.default.svc"
