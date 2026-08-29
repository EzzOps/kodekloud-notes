# Demo Status Scale Printer Columns Short Names

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Custom-Resource-Definitions-Deep-Dive/Demo-Status-Scale-Printer-Columns-Short-Names/page

Explains how to configure a WebApp CRD so it behaves like native Kubernetes workloads by enabling status and scale subresources, printer columns, and categories

Previously we had a working WebApp custom resource: CRD, schema, validation, and a controller. Functionally it worked, but it didn't behave like a first-class Kubernetes resource:

* `kubectl get wa` showed only NAME and AGE.
* `kubectl scale wa` failed.
* A regular `kubectl apply` could overwrite `.status` because the API server wasn't preventing writes to it.

Below is the minimal CRD we started from:

```yaml theme={null}
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: webapps.webapp.kodekloud.com
spec:
  group: webapp.kodekloud.com
  scope: Namespaced
  names:
    plural: webapps
    singular: webapp
    kind: WebApp
    listKind: WebAppList
    shortNames: [wa]
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
```

In this guide we add four CRD fields that make your WebApp resource behave like a built-in workload:

* Enable the `status` subresource so only the `/status` endpoint (typically controllers) can update `.status`.
* Enable the `scale` subresource so `kubectl scale` and HPAs can target the CR.
* Add `additionalPrinterColumns` so `kubectl get wa` shows meaningful columns.
* Add `categories: [all]` so tools that honor categories treat your CR as a top-level workload.

No controller code changes or rebuilds are required — the API server enforces these behaviors based purely on the CRD.

## Quick overview: What each CRD field does

| CRD Field                  | Purpose                                   | Effect                                                                                |
| -------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------- |
| `schema` includes `status` | Prevents server-side pruning of `.status` | Controllers can write status; ordinary writes will not persist status fields          |
| `subresources.status`      | Exposes `/status` endpoint                | Only `/status` updates `.status` (prevents accidental writes via `apply`)             |
| `subresources.scale`       | Exposes `/scale` endpoint                 | `kubectl scale` and HPAs can update `.spec.replicas` and read `.status.readyReplicas` |
| `additionalPrinterColumns` | Customize `kubectl get` output            | Shows meaningful columns like Image, Replicas, Ready, Port, Age                       |
| `names.categories`         | Categorize the CR                         | Tools (and `kubectl api-resources --categories=all`) include it in tooling groups     |

***

## Step 1 — Teach the schema about `.status` and tighten `.spec` validation

Add a `status` object to the OpenAPI schema so the API server does not prune it. Also make `spec` validation explicit (required fields, types and ranges):

```yaml theme={null}
