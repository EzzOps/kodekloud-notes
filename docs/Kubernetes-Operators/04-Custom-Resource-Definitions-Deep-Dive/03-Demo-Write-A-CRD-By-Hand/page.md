# fragment: spec.versions[0].schema.openAPIV3Schema
type: object
properties:
  spec:
    type: object
    required: [image, replicas]
    properties:
      image:
        type: string
      replicas:
        type: integer
        minimum: 1
        maximum: 10
      port:
        type: integer
        default: 8080
  status:
    type: object
    properties:
      readyReplicas:
        type: integer
      labelSelector:
        type: string
```

This schema change ensures:

* The API server preserves `.status` (it won't be removed by pruning).
* Clients get clear validation errors for missing or invalid `spec` fields.

## Step 2 — Enable `/status` and add the `scale` subresource

Turn on the `/status` endpoint by adding an empty `status: {}` under `subresources`. Add the `scale` block and point it to the JSONPaths for desired and observed replicas and for the label selector:

```yaml theme={null}
# fragment: spec.versions[0].subresources
subresources:
  status: {}
  scale:
    specReplicasPath: .spec.replicas
    statusReplicasPath: .status.readyReplicas
    labelSelectorPath: .status.labelSelector
```

With this in place:

* `kubectl scale wa <name> --replicas=<n>` is routed to the scale subresource and updates `.spec.replicas`.
* HorizontalPodAutoscalers (HPAs) that target this resource can read replicas and update the scale endpoint.

<Callout icon="lightbulb">
  Enabling the `status` subresource prevents ordinary `apply`/`update` requests from modifying `.status`. Only the `/status` endpoint (used by controllers) may change status fields.
</Callout>

## Step 3 — Add additional printer columns for `kubectl get`

Define columns so `kubectl get wa` displays useful information. Each column needs `name`, `type`, and a `jsonPath`. Use `priority: 1` to hide less important columns unless `-o wide` is requested:

```yaml theme={null}
# fragment: spec.versions[0].additionalPrinterColumns
additionalPrinterColumns:
  - name: Image
    type: string
    jsonPath: .spec.image
    priority: 1
  - name: Replicas
    type: integer
    jsonPath: .spec.replicas
  - name: Ready
    type: integer
    jsonPath: .status.readyReplicas
  - name: Port
    type: integer
    jsonPath: .spec.port
  - name: Age
    type: date
    jsonPath: .metadata.creationTimestamp
```

These columns make `kubectl get wa` feel like a native resource listing (Image, Replicas, Ready, Port, Age).

## Step 4 — Add `categories: [all]`

Add `categories: [all]` under `spec.names` so tools that respect categories (and `kubectl api-resources --categories=all`) include the resource among top-level workload types:

```yaml theme={null}
# fragment: spec.names
names:
  plural: webapps
  singular: webapp
  kind: WebApp
  listKind: WebAppList
  shortNames: [wa]
  categories: [all]
```

Note: `kubectl get all` is a hard-coded convenience command and will not list CRDs even if they declare `categories: [all]`. The category is still useful for other tooling and `kubectl api-resources --categories=all`.

<Callout icon="warning">
  `kubectl get all` will not list your CRs even if `categories: [all]` is set. Use `kubectl api-resources --categories=all` or `kubectl get webapps` / `kubectl get wa` to view your resources.
</Callout>

***

## Final consolidated CRD (relevant fragments)

Below is a consolidated view showing the key fields you should include. Fill in the remaining CRD metadata as appropriate for your project.

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
    categories: [all]
  versions:
    - name: v1
      served: true
      storage: true
      subresources:
        status: {}
        scale:
          specReplicasPath: .spec.replicas
          statusReplicasPath: .status.readyReplicas
          labelSelectorPath: .status.labelSelector
      additionalPrinterColumns:
        - name: Image
          type: string
          jsonPath: .spec.image
          priority: 1
        - name: Replicas
          type: integer
          jsonPath: .spec.replicas
        - name: Ready
          type: integer
          jsonPath: .status.readyReplicas
        - name: Port
          type: integer
          jsonPath: .spec.port
        - name: Age
          type: date
          jsonPath: .metadata.creationTimestamp
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              required: [image, replicas]
              properties:
                image:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 10
                port:
                  type: integer
                  default: 8080
            status:
              type: object
              properties:
                readyReplicas:
                  type: integer
                labelSelector:
                  type: string
```

## Apply the CRD

No API server restart is required — changes to CRDs are picked up immediately.

```bash theme={null}
$ kubectl apply -f webapp-crd.yaml
customresourcedefinition.apiextensions.k8s.io/webapps.webapp.kodekloud.com configured
```

After applying:

* `kubectl get wa` will show the extra columns you defined. (The `Image` column may be hidden unless you use `-o wide` because it has `priority: 1`.)
* `kubectl scale wa <name> --replicas=<n>` updates `.spec.replicas` via the scale subresource.
* Regular `kubectl apply` / `kubectl update` attempts that include `.status` will see `.status` fields dropped — only `/status` updates persist status.

## Validate category registration

```bash theme={null}
$ kubectl api-resources --categories=all | grep -E 'NAME|webapp'
NAME       SHORTNAMES   APIVERSION                 NAMESPACED   KIND
webapps    wa           webapp.kodekloud.com/v1    true         WebApp
```

## Summary

By adding these CRD fields:

* `schema` for `status` and `spec` validation
* `subresources.status`
* `subresources.scale`
* `additionalPrinterColumns`
* `names.categories: [all]`

you make your custom resource behave like a first-class Kubernetes workload. All of the enforcement is handled by the API server from the CRD itself — you do not need to change or rebuild the controller.

References:

* [Kubebuilder](https://kubebuilder.io) can generate these CRD fields automatically from Go marker comments on your types.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ba392f08-9d70-442b-9751-fdc2052b777e/lesson/e548531a-9522-478c-a1f2-5b2d4467a0c3" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ba392f08-9d70-442b-9751-fdc2052b777e/lesson/bdaa4a6c-ee26-4b84-8fcf-1f0074e15286" />
</CardGroup>


# Demo Write A CRD By Hand

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Custom-Resource-Definitions-Deep-Dive/Demo-Write-A-CRD-By-Hand/page

Handbook for creating Kubernetes CustomResourceDefinitions with schema validation, defaults, versions, and kubectl commands.

Sometimes you need Kubernetes to store and validate a resource that doesn't exist yet (for example, a WebApp). Scaffolding tools can feel like a black box. The reliable, explicit solution is a CustomResourceDefinition (CRD): a Kubernetes object that teaches the API server about your new kind so it can be discovered, validated, and stored.

## CRD basics

A CRD is itself a Kubernetes object and uses the same top-level fields you already know: `apiVersion`, `kind`, `metadata`, and `spec`. For CRDs:

* `apiVersion` is always `apiextensions.k8s.io/v1`
* `kind` is `CustomResourceDefinition`
* `metadata.name` must be set to the plural form of your resource followed by a dot and the API group (see note below)
* `spec` contains `group`, `scope`, `names`, and `versions`

<Callout icon="lightbulb">
  Always set `metadata.name` to `<plural>.<group>`. For example, if your group is `webapp.kodekloud.com` and your plural is `webapps`, the metadata name must be `webapps.webapp.kodekloud.com`.
</Callout>

Minimal header example:

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
    shortNames:
      - wa
```

Quick reference: top-level CRD `spec` fields

| Field          | Purpose                                                         | Example                |
| -------------- | --------------------------------------------------------------- | ---------------------- |
| `group`        | API group under `/apis`                                         | `webapp.kodekloud.com` |
| `scope`        | `Namespaced` or `Cluster`                                       | `Namespaced`           |
| `names.plural` | Plural resource name used in API and `metadata.name`            | `webapps`              |
| `names.kind`   | Title-cased Kind shown in `kubectl`                             | `WebApp`               |
| `versions`     | Versions served by the API server with schemas and subresources | See below              |

## Versions and schema validation

A CRD can serve multiple versions. Important rules:

* Exactly one version must have `storage: true` — this is the version persisted to etcd.
* Versions you want available via the API server should have `served: true`.
* Validation and defaults are expressed using `openAPIV3Schema` for each version.

We'll start with a single version `v1alpha1` that is both `served` and `storage`. The following schema declares `spec` fields and constraints:

* `spec.image` — string (required)
* `spec.replicas` — integer (required), minimum 1, maximum 10
* `spec.port` — integer, default 8080

Complete CRD (with validation and defaults):

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
    shortNames:
      - wa
  versions:
    - name: v1alpha1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              required:
                - image
                - replicas
              properties:
                image:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 10
                port:
                  type: integer
                  default: 8080
```

When the API server reads this CRD, it will register a new endpoint at:

`/apis/webapp.kodekloud.com/v1alpha1`

and kubectl discovery will expose the new resource types automatically.

## Apply the CRD and confirm discovery

Apply the CRD manifest:

```bash theme={null}
kubectl apply -f webapp-crd.yaml
```

Expected creation output:

```text theme={null}
customresourcedefinition.apiextensions.k8s.io/webapps.webapp.kodekloud.com created
```

Check CRD status conditions (wait until the API server finishes registering the CRD; you should see `NamesAccepted` and `Established`):

```bash theme={null}
kubectl get crd webapps.webapp.kodekloud.com -o jsonpath='{.status.conditions[*].type}'
```

Expected output:

```text theme={null}
NamesAccepted Established
```

Because discovery is dynamic, `kubectl explain` immediately recognizes your new type:

```bash theme={null}
kubectl explain webapp.spec
```

Example output:

```text theme={null}
GROUP:       webapp.kodekloud.com
KIND:        WebApp
VERSION:     v1alpha1
FIELD:       spec <Object>
DESCRIPTION:
    <empty>
FIELDS:
  image <string> -required-
    <no description>
  port <integer>
    <no description>
  replicas <integer> -required-
    <no description>
```

No API server restart or plugin installation is required — discovery updates automatically.

## Schema validation in action

Create a sample WebApp that violates the `replicas` maximum (set to 99). Save this as `sample-webapp.yaml`:

```yaml theme={null}
apiVersion: webapp.kodekloud.com/v1alpha1
kind: WebApp
metadata:
  name: bad-sample
spec:
  image: nginx
  replicas: 99
```

Apply it:

```bash theme={null}
kubectl apply -f sample-webapp.yaml
```

The API server will reject the resource due to schema validation. Example error:

```text theme={null}
The WebApp "bad-sample" is invalid: spec.replicas: Invalid value: 99: spec.replicas in body should be less than or equal to 10
```

Fix the `replicas` value (for example, to 3) and apply again:

```yaml theme={null}
apiVersion: webapp.kodekloud.com/v1alpha1
kind: WebApp
metadata:
  name: bad-sample
spec:
  image: nginx
  replicas: 3
```

```bash theme={null}
kubectl apply -f sample-webapp.yaml
```

Expected success output:

```text theme={null}
webapp.webapp.kodekloud.com/bad-sample created
```

Now fetch the created resource and inspect the `spec` (pipe through `jq` to format). Notice the server-populated default for `port`:

```bash theme={null}
kubectl get webapp bad-sample -o json | jq .spec
```

Expected JSON:

```json theme={null}
{
  "image": "nginx",
  "port": 8080,
  "replicas": 3
}
```

The API server applied the default defined in the CRD schema. This demonstrates both validation and defaulting are enforced at the API level before objects are persisted to etcd.

## Next steps and useful extensions

You can extend this CRD to improve UX and integration with kubectl:

* Add `status` as a subresource to allow controllers to update status safely.
* Add a `scale` subresource to support `kubectl scale`.
* Define `additionalPrinterColumns` so `kubectl get webapp` displays meaningful columns.

Table: common kubectl checks and commands for CRDs

| Action                 | Command                                                                                   |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| Apply CRD              | `kubectl apply -f webapp-crd.yaml`                                                        |
| Check CRD conditions   | `kubectl get crd webapps.webapp.kodekloud.com -o jsonpath='{.status.conditions[*].type}'` |
| Explain type           | `kubectl explain webapp.spec`                                                             |
| Create instance        | `kubectl apply -f sample-webapp.yaml`                                                     |
| Inspect created object | `kubectl get webapp bad-sample -o json \| jq .spec`                                       |

<Callout icon="warning">
  Two common mistakes to watch for:

  * `metadata.name` must be `plural.group` (example: `webapps.webapp.kodekloud.com`).
  * Exactly one version must have `storage: true` — that is the version persisted in etcd.
</Callout>

## Links and references

* [Kubernetes Custom Resource Definitions (CRDs)](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
* [apiextensions.k8s.io v1 reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#customresourcedefinition-v1-apiextensions-k8s-io)

This demonstrates a complete, hand-authored CRD: names, group, versioning, schema validation, and defaults — all defined in a single YAML manifest.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ba392f08-9d70-442b-9751-fdc2052b777e/lesson/2d5366fc-2798-4b9e-abb3-2cc01fbf16fb" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ba392f08-9d70-442b-9751-fdc2052b777e/lesson/4c1e3c6d-8185-4c15-865f-6ac7aa58f4a8" />
</CardGroup>
