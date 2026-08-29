# parallel example (only the pipeline.steps portion shown)
steps:
- - name: step-one
    template: print-message
    arguments:
      parameters:
      - name: message
        value: "Hello from KodeKloud!"
  - name: step-two
    template: print-message
    arguments:
      parameters:
      - name: message
        value: "Hello from Nourhan!"
```

Argo will show progress while steps execute (e.g., 1/2, 2/2) and list completed steps when finished.

***

## 3) DAG (Directed Acyclic Graph) workflows

DAGs express explicit dependencies between tasks. Tasks with no dependencies start immediately; dependent tasks wait for their dependencies to succeed. Use DAGs for complex pipelines where dependency relationships matter (e.g., build → tests → deploy).

Example `dag-workflow.yaml` models a build → tests → deploy pipeline. `test-unit` and `test-integration` both depend on `build` and run in parallel; `deploy` depends on both tests:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: dag-demo-
  namespace: argo
spec:
  entrypoint: pipeline
  templates:
  - name: pipeline
    dag:
      tasks:
      - name: build
        template: run-step
        arguments:
          parameters:
          - name: message
            value: "Building"
      - name: test-unit
        template: run-step
        dependencies: [build]
        arguments:
          parameters:
          - name: message
            value: "Unit testing"
      - name: test-integration
        template: run-step
        dependencies: [build]
        arguments:
          parameters:
          - name: message
            value: "Integration testing"
      - name: deploy
        template: run-step
        dependencies: [test-unit, test-integration]
        arguments:
          parameters:
          - name: message
            value: "Deploying"
  - name: run-step
    inputs:
      parameters:
      - name: message
    container:
      image: alpine:3.18
      command: [echo]
      args: ["{{inputs.parameters.message}}"]
```

Submit the DAG:

```bash theme={null}
argo submit dag-workflow.yaml -n argo --watch
```

Expected execution order:

* `build` runs first.
* `test-unit` and `test-integration` start once `build` completes (they run concurrently).
* `deploy` runs after both tests succeed.

Example `argo get` summary when finished:

```plaintext theme={null}
Name:            dag-demo-btns6
Namespace:       argo
Status:          Succeeded
Duration:        30 seconds
Progress:        4/4

STEP                         TEMPLATE        DURATION
✔ build                      run-step        3s
✔ test-integration           run-step        4s
✔ test-unit                  run-step        4s
✔ deploy                     run-step        4s
```

***

## 4) Running kubectl from a workflow (RBAC considerations)

Workflows can run images that include `kubectl` to query or modify cluster resources. To interact with the cluster, the workflow’s ServiceAccount must have the proper RBAC permissions.

Example `kubectl-workflow.yaml` uses `bitnami/kubectl` to check a deployment rollout and then list pods in the `argo` namespace:

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: kubectl-pipeline-
  namespace: argo
spec:
  entrypoint: pipeline
  serviceAccountName: default
  templates:
  - name: pipeline
    steps:
    - - name: check-rollout
        template: rollout-status
    - - name: get-pods
        template: list-pods
  - name: rollout-status
    container:
      image: bitnami/kubectl:latest
      command: [kubectl]
      args: [rollout, status, deployment/nginx-app, -n, argo]
  - name: list-pods
    container:
      image: bitnami/kubectl:latest
      command: [kubectl]
      args: [get, pods, -n, argo]
```

Submit and watch:

```bash theme={null}
argo submit kubectl-workflow.yaml -n argo --watch
```

View combined logs from the latest workflow run:

```bash theme={null}
argo logs -n argo @latest
```

Example `argo logs` output (abridged):

```plaintext theme={null}
kubectl -n argo rollout status -w deployment "nginx-app"
deployment "nginx-app" successfully rolled out

kubectl -n argo get pods
NAME                                READY   STATUS      RESTARTS  AGE
argo-server-xxxxxx                  1/1     Running     0         28m
hello-world-xxxx                    0/2     Completed   0         67s
...
```

<Callout icon="warning">
  Do not run workflows with overly permissive credentials. Avoid using the cluster-admin `default` ServiceAccount in production. Create a dedicated ServiceAccount with only the RBAC rules it needs (Role/ClusterRole and RoleBinding/ClusterRoleBinding).
</Callout>

***

## Key concepts and quick reference

| Concept            | Purpose                                    | Notes / Example                                        |
| ------------------ | ------------------------------------------ | ------------------------------------------------------ |
| Workflow           | Top-level Argo object                      | Defines `spec.entrypoint` and `templates`              |
| Template           | Reusable unit (container/script/DAG/steps) | Templates accept `inputs.parameters` and produce tasks |
| steps              | Sequential + grouped parallel execution    | Array of arrays — inner arrays run in parallel         |
| dag                | Dependency graph                           | Tasks use `dependencies: [name]` for ordering          |
| serviceAccountName | Identity for Pod actions                   | Bind minimal RBAC permissions to this account          |

***

## Summary

* Argo Workflows runs containerized tasks as Kubernetes pods to orchestrate automation, pipelines, and arbitrary job sequences.
* Use `templates` to create reusable task definitions with parameters.
* `steps` provide ordered and parallel grouping via arrays of arrays.
* `dag` defines explicit dependency-based execution with `dependencies`.
* For workflows that interact with the cluster, set `serviceAccountName` and grant only necessary RBAC permissions.

Further reading:

* Argo Workflows docs: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Argo CLI reference: [https://argoproj.github.io/argo-workflows/cli/](https://argoproj.github.io/argo-workflows/cli/)
* Kubernetes RBAC: [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/417a9437-044d-4734-9691-8d489a034f2b" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/868fe7a5-4cdd-41c9-b7e4-f1cdfdb5902d" />
</CardGroup>


# Extending Kubernetes Custom Resources and API Extensions

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-APIs-and-Self-Service-Capabilities/Extending-Kubernetes-Custom-Resources-and-API-Extensions/page

Explains how to extend the Kubernetes API with CustomResourceDefinitions, define CRDs and schemas, validate via OpenAPI v3, and reconcile custom resources with controllers

Kubernetes exposes a rich API, but its built-in primitives (Pods, Services, Deployments, etc.) are generic. Platform teams and developers think in higher-level, domain-specific concepts — for example, "database" — which Kubernetes does not natively represent. Modeling those domain concepts using only primitive resources produces complexity, duplication, and operational gaps.

In this lesson you will learn how to extend the Kubernetes API with domain-specific concepts using CustomResourceDefinitions (CRDs). We'll cover why built-in resources fall short for platform abstractions, how the API extension model works, how to author CRDs (group, names, scope, versions, and schema), and how to validate resources with OpenAPI v3 schemas. Finally, you'll understand the lifecycle between CRD, Custom Resource (CR), and the controller that reconciles them.

<Frame>
  <img alt="The image outlines learning objectives related to Kubernetes, detailing steps such as understanding built-in resources, API extension models, defining CRDs, and validating resources with openAPIV3Schema." />
</Frame>

## Problem: Mapping platform concepts to primitives

A common anti-pattern is modeling a single domain concept (e.g., a database) with multiple unrelated Kubernetes objects. For example, a single database might be represented by five separate resources: StatefulSet, ConfigMap, Secret, ServiceAccount, and NetworkPolicy.

<Frame>
  <img alt="The image is an infographic illustrating Kubernetes built-in resources and their limits, featuring icons and terms like StatefulSet, ConfigMap, Secret, and others." />
</Frame>

With 40 microservices each needing a database, that anti-pattern can produce 200 database-related objects that have no single logical representation or lifecycle. That makes discovery, validation, governance, and automation harder.

Four key limitations when using only built-in resources:

* No domain-specific abstractions: you cannot represent a Database as a single, first-class object.
* No custom validation beyond primitive field checks (for example, you cannot require "production databases must have backups enabled" at the API layer).
* No simple trigger point for platform workflows when a logical resource changes.
* Platform concepts like teams, environments, and cost centers are not represented natively.

<Frame>
  <img alt="The image outlines the limitations of Kubernetes built-in resources, highlighting gaps such as lack of domain-specific abstractions, custom validation, business logic integration, and platform-specific concepts." />
</Frame>

Before CRDs, answering “which databases do we have?” required custom scripts that correlated multiple objects by labels. After introducing a Database CRD, teams could run `kubectl get databases` and see meaningful results directly.

## Kubernetes extension model — same API, new types

Kubernetes APIs follow a consistent URL pattern: group, version, namespace (if namespaced), and resource. For built-in Deployments the path is:

/apis/apps/v1/namespaces/default/deployments

Custom resources follow the same pattern. For example, a Database custom resource could be served at:

/apis/platform.acme.io/v1/namespaces/dev/databases

Because custom APIs use the same API server, they are first-class:

* `kubectl` can get/list/describe/delete CRs.
* RBAC can secure them.
* GitOps tools (ArgoCD, Flux) can sync them.
* Policy engines (Gatekeeper/Open Policy Agent) can enforce rules.

Creating a CRD registers the new type with the API server — you get these integrations without building a separate API server.

## CRD anatomy

A CRD defines a new resource type. Key fields include `group`, `names`, `scope`, `versions`, and the `openAPIV3Schema`. Below is a concise reference table for the most important CRD fields.

| Field                   | Purpose                                              | Example                      |
| ----------------------- | ---------------------------------------------------- | ---------------------------- |
| `metadata.name`         | Unique name for the CRD — must be `<plural>.<group>` | `databases.platform.acme.io` |
| `spec.group`            | API group to avoid collisions (usually your domain)  | `platform.acme.io`           |
| `spec.names.plural`     | Plural name used in URLs and `kubectl get`           | `databases`                  |
| `spec.names.singular`   | Singular form for API usage                          | `database`                   |
| `spec.names.kind`       | Kind used in manifests (`kind: Database`)            | `Database`                   |
| `spec.names.shortNames` | Short aliases for convenience                        | `- db`                       |
| `spec.scope`            | `Namespaced` or `Cluster`                            | `Namespaced`                 |
| `spec.versions`         | List of versions served; each version has schema     | `v1` with `openAPIV3Schema`  |
| `openAPIV3Schema`       | OpenAPI v3 schema used for API-level validation      | See YAML example below       |

Each version in `spec.versions` can be `served: true/false` and one version can be `storage: true` (the persisted version).

### Example CRD (illustrative)

This CRD demonstrates group, names, version, and an `openAPIV3Schema` for validation.

```yaml theme={null}
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.platform.acme.io
spec:
  group: platform.acme.io
  scope: Namespaced
  names:
    plural: databases
    singular: database
    kind: Database
    shortNames:
      - db
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          required:
            - spec
          properties:
            spec:
              type: object
              required:
                - size
              properties:
                size:
                  type: string
                  enum: [small, medium, large]
                engine:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 10
                  default: 3
            status:
              type: object
              properties:
                phase:
                  type: string
                  enum: [Pending, Ready, Failed]
```

Notes on schema and fields:

* `metadata.name` must be `<plural>.<group>` (e.g., `databases.platform.acme.io`).
* `group` is typically your company or platform domain to avoid naming collisions.
* `names.plural` is used for URLs and `kubectl get`.
* `kind` is the manifest `kind` (e.g., `Database`).
* `scope` determines whether objects are cluster-scoped or namespaced.
* `versions` let you evolve APIs; `storage: true` marks which version is stored in etcd.
* `openAPIV3Schema` enables API-server level validation (types, enums, required fields, numeric constraints, and defaults where supported).

## Validation with OpenAPI v3 schemas

`openAPIV3Schema` is the first line of defense: the API server validates objects before passing them to controllers. The schema supports:

* Type validation: `string`, `integer`, `boolean`, `array`, `object`.
* Enums: restrict allowed values (e.g., `size: enum [small, medium, large]`).
* Required fields: enforce mandatory inputs.
* Numeric constraints: `minimum`, `maximum`.
* Defaults: where supported, the API server can apply default values.

Example: if `spec.size` is restricted by an `enum`, sending `xlarge` will be rejected with a validation error. If `replicas` has `maximum: 10`, creating a resource with 100 replicas will be rejected.

## CRD lifecycle and reconciliation loop

The lifecycle consists of three main players:

1. CRD — the class definition (schema and metadata) registered with the API server.
2. CR (Custom Resource) — an instance that conforms to the CRD.
3. Controller — code that watches CRs and reconciles desired state into real resources (StatefulSets, Secrets, external provisioning operations), and updates `status`.

<Frame>
  <img alt="The image is a flowchart illustrating the transition from Custom Resource Definition (CRD) to Custom Resource (CR) and Controller, with CRD representing the schema, CR as the instance, and the Controller as the logic. It includes definitions for each component." />
</Frame>

A simple mental model: the CRD is the menu, the CR is your order, and the controller is the kitchen that makes the order real.

### Example Custom Resource

An instance that conforms to the CRD shown above:

```yaml theme={null}
apiVersion: platform.acme.io/v1
kind: Database
metadata:
  name: orders-db
spec:
  size: medium
  engine: postgresql
  replicas: 3
```

Apply the CR with kubectl:

```bash theme={null}
kubectl apply -f database.yaml
```

Typical interactions after applying the CR:

```bash theme={null}
kubectl get databases
