# Output
database.platform.acme.io/orders-db created
```

It appears successful, but there is still no PostgreSQL instance, no network configuration, and no status updates. Without a controller, the CR is only persisted in etcd — nothing reconciles it to reality.

<Frame>
  <img alt="The image is a diagram highlighting the limitations of CRDs as etcd data, including issues like no database creation, lack of status updates, absence of drift correction, and no cleanup on delete." />
</Frame>

Controller = the software that makes desired state real. A helpful analogy:

<Frame>
  <img alt="The image explains the roles of CRD (Menu), CR (Order), and Controller (Kitchen) in a Kubernetes context, using a restaurant analogy." />
</Frame>

* CRD is the menu: it defines what can be requested.
* CR (the object you apply) is the order you place.
* Controller is the kitchen: it actually prepares the meal and reports progress.

The Reconciliation Loop

Reconciliation is the core control logic controllers run repeatedly to converge actual state to desired state. Typical phases:

1. Watch / observe — get notifications for creates/updates/deletes.
2. Compare — compute desired state (from `spec`) vs actual state (external resources, cloud APIs, cluster objects).
3. Act — create/update/delete resources to close the gap.
4. Report — update the CR's `status` (conditions, observedGeneration, phase).

Examples for a Database CR:

* If the external DB does not exist, create it.
* If the `size` changed, resize the DB.
* If the CR is deleted, perform cleanup.
* Update `status` to show provisioning progress or readiness.

Follow three guiding principles for safe and robust reconcilers:

* Level-triggered: react to current state, not transient events. If an event is missed, the next reconcile still inspects state and corrects drift.
* Idempotency: running Reconcile multiple times should produce the same final result as running it once—always check current state first.
* Eventual consistency: the system can take multiple reconciles to converge; expect retries and backoff.

<Frame>
  <img alt="The image outlines the key principles of &#x22;The Reconciliation Loop: Desired vs Actual,&#x22; emphasizing level-triggered processes, eventual consistency, and idempotent operations. It suggests reconciling based on current state rather than events, allowing systems to converge over time and handle repeated operations with consistent results." />
</Frame>

Use status to inform users: a five-minute provisioning operation can report `Progressing` while the controller continues to reconcile and later update `Ready`.

Controller internals: four collaborating layers

Most operator frameworks implement this architecture for you; your job is to implement the Reconciler (the business logic).

1. API server — source of truth and where desired state is stored.
2. Informer — watches API server and maintains a local cache to reduce API traffic.
3. Work queue — the informer enqueues resource keys; queue deduplicates events so the reconciler runs for the latest state.
4. Reconciler — your implementation: read resource, compare desired vs actual, act, and return a result (requeue/no-requeue/error).

<Frame>
  <img alt="The image is a diagram of a controller architecture consisting of three components: API Server, Informer, and Work Queue, each with specific roles described alongside." />
</Frame>

<Frame>
  <img alt="The image illustrates a controller architecture composed of four components: an API Server, an Informer, a Work Queue, and a Reconciler, each with specific functions outlined." />
</Frame>

The framework handles watching, queuing, retries, and worker scaling so you can focus on making the reconciler idempotent and correct.

<Frame>
  <img alt="The image illustrates a &#x22;Controller Architecture&#x22; with focus on resilience, consistency, and scalability, explaining the benefits of the design. It highlights that the framework manages watching, queuing, and retries, while the user writes the reconciler." />
</Frame>

Reconcile function pattern (conceptual Go example)

You don't need to memorize Go—focus on the flow. This example mirrors the signature used by controller-runtime: `Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error)`.

```go theme={null}
// Reconcile compares desired and actual state and acts to converge them.
// Signature in controller-runtime: Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error)
func (r *DBReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. Fetch the resource
    db := &platformv1.Database{}
    if err := r.Get(ctx, req.NamespacedName, db); err != nil {
        if apierrors.IsNotFound(err) {
            // Resource deleted after request — nothing to do.
            return ctrl.Result{}, nil
        }
        // Transient error reading the object — requeue.
        return ctrl.Result{}, err
    }

    // 2. Check if being deleted (finalizer handling)
    if db.GetDeletionTimestamp() != nil {
        return r.handleDeletion(ctx, db)
    }

    // 3. Main reconcile logic (idempotent): ensure external DB exists and matches spec
    if err := r.ensureDatabase(ctx, db); err != nil {
        // If transient, requeue with backoff
        return ctrl.Result{}, err
    }

    // 4. Update status: observedGeneration, conditions, phase, etc.
    db.Status.ObservedGeneration = db.Generation
    db.Status.Phase = "Ready"
    // set conditions as appropriate...
    if err := r.Status().Update(ctx, db); err != nil {
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

Best practices for your reconcile function:

* Always fetch the latest object from the API server or cache.
* Handle deletion via finalizers and short-circuit if the object is gone.
* Make operations idempotent — check external state before making changes.
* Use the `status` subresource to update fields like `observedGeneration` and `conditions`.

Status and conditions

Status is how your controller reports progress and health. Kubernetes conditions are a well-established pattern: each condition includes `type`, `status` (`True`/`False`/`Unknown`), `reason`, and `message`.

Common condition types:

* `Available` / `Ready` — resource is ready to serve.
* `Progressing` — creation/update is in progress.
* `Degraded` — running but not operating correctly.

observedGeneration pattern

When a user modifies the `spec`, Kubernetes increments `metadata.generation`. Your controller sets `status.observedGeneration` to the generation it last reconciled. Comparing `metadata.generation` and `status.observedGeneration` tells users whether the controller has acted on the latest change.

<Frame>
  <img alt="The image explains the &#x22;observedGeneration&#x22; pattern, where you compare metadata.generation with status.observedGeneration to check if changes are processed." />
</Frame>

Finalizers and deletion flow

Finalizers allow controllers to perform cleanup before Kubernetes permanently removes a CR. When a user deletes a CR, the API server sets `deletionTimestamp` but keeps the object until finalizers are cleared—this is the controller's opportunity to delete external resources (cloud instances, secrets, networks).

Typical finalizer handling:

```go theme={null}
// This runs when the CR has a deletion timestamp set.
func (r *DBReconciler) handleDeletion(ctx context.Context, db *platformv1.Database) (ctrl.Result, error) {
    if hasFinalizer(db, dbFinalizer) {
        // Perform cleanup of external resources.
        if err := deleteRDSInstance(ctx, db.Spec.Name); err != nil {
            // Retry on transient errors; log and requeue.
            return ctrl.Result{}, err
        }
        if err := deleteSecrets(ctx, db.Namespace, db.Name); err != nil {
            return ctrl.Result{}, err
        }

        // Remove finalizer and update the object to allow deletion.
        removeFinalizer(db, dbFinalizer)
        if err := r.Update(ctx, db); err != nil {
            return ctrl.Result{}, err
        }
    }
    // Nothing else to do; let API server delete the object.
    return ctrl.Result{}, nil
}
```

Deletion flow summary:

1. User runs `kubectl delete`.
2. API server sets `deletionTimestamp` and retains the object.
3. Controller observes the timestamp, performs cleanup, and removes finalizers.
4. When no finalizers remain, the API server deletes the object.

> **warning** If cleanup fails (for example, cloud API outages), the object will remain in a Terminating state while finalizers persist. Implement robust retries, exponential backoff, and comprehensive logging so cleanup eventually completes and you avoid orphaned resources.

Operator frameworks

Most teams avoid writing controller boilerplate from scratch. Common frameworks let you focus on business logic:

<Frame>
  <img alt="The image is a comparison chart of three operator frameworks: Kubebuilder, Operator SDK, and Metacontroller, highlighting their features and best use cases." />
</Frame>

Below is a concise comparison to help you choose:

| Framework      | Language / Style    | Best for                                | Notes & Links                                                                                 |
| -------------- | ------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------- |
| Kubebuilder    | Go (code-first)     | Production Go operators                 | `https://book.kubebuilder.io/` — scaffolds controllers, CRDs, webhooks, testing               |
| Operator SDK   | Go / Helm / Ansible | Multi-language teams, Red Hat ecosystem | Built on Kubebuilder; supports Helm & Ansible operators — `https://sdk.operatorframework.io/` |
| Metacontroller | Any (webhook)       | Lightweight, polyglot operators         | Implement reconcile as an HTTP server — `https://metacontroller.github.io/`                   |

Key takeaways

<Frame>
  <img alt="The image outlines four key takeaways about controllers, CRDs, reconciliation, status, and finalizers in a technology context. Each point is numbered and highlighted with a colored icon." />
</Frame>

* CRDs without controllers are just stored data — controllers make the desired state become real.
* Design your Reconcile to be idempotent and level-triggered: always read current state and act only when needed.
* Use `status`, conditions, and `observedGeneration` to transparently communicate what the controller has processed.
* Implement finalizers to clean up external resources; handle errors with retries and backoff to avoid stuck Terminating objects.

Additional resources

* Kubernetes controllers & reconciliation concepts: [https://kubernetes.io/docs/concepts/architecture/controller/](https://kubernetes.io/docs/concepts/architecture/controller/)
* controller-runtime (Reconcile signature and helpers): [https://github.com/kubernetes-sigs/controller-runtime](https://github.com/kubernetes-sigs/controller-runtime)
* Kubebuilder book: [https://book.kubebuilder.io/](https://book.kubebuilder.io/)
* Operator SDK docs: [https://sdk.operatorframework.io/](https://sdk.operatorframework.io/)
* Metacontroller: [https://metacontroller.github.io/](https://metacontroller.github.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/4c8d6b72-361f-4c1c-8b62-cf84a251000f)


# Platform Building Blocks Crossplane XRs Compositions and Functions

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Cloud-Native-Platform-Engineer-CNPE/Platform-APIs-and-Self-Service-Capabilities/Platform-Building-Blocks-Crossplane-XRs-Compositions-and-Functions/page

Explains how Crossplane uses XRDs and Compositions to create Kubernetes native platform APIs that unify application and infrastructure provisioning for GitOps based self service

We have CRDs and controllers to model custom APIs and their behavior, plus orchestration workflows for complex systems. Yet many organizations still have a painful gap: application delivery happens through a Kubernetes-native GitOps workflow, but infrastructure provisioning uses separate tooling. Two tools. Two workflows. Two mental models.

Crossplane extends Kubernetes so you can manage infrastructure using the same declarative YAML, kubectl commands, RBAC, and GitOps patterns you already use. This article explains how Crossplane closes the gap and helps platform teams expose self-service, Kubernetes-native platform APIs using Composite Resource Definitions (XRDs) and Compositions.

<Frame>
  <img alt="The image lists four learning objectives related to app and infrastructure workflows, providers, XRDs, platform APIs, and mapping APIs, with a colorful numbered design." />
</Frame>

In this guide you will learn to:

* Explain why separate app and infrastructure workflows are problematic.
* Understand Crossplane’s core concepts and architecture.
* Define platform APIs with XRDs and map those APIs to concrete resources using Compositions.
* Compose Kubernetes resources and cloud infrastructure together in a single abstraction.

Why separate app and infra workflows cause friction

A typical developer flow at many organizations looks like:

* Push application code to Git; Argo CD deploys the app.
* Need a database → switch to Terraform, author HCL.
* Infrastructure team reviews and applies the Terraform plan (multi-day SLA).
* Platform team or devops manually creates Kubernetes Secrets with connection strings.
* Argo CD syncs the secret; app finally connects.

From “I need a database” to a connected app often takes days — and requires multiple tools and mental models.

<Frame>
  <img alt="The image illustrates a step-by-step workflow for self-service provisioning, highlighting nine stages from pushing code to app connectivity, with approximate durations and specific actions involved at each step." />
</Frame>

Contrast that with a Kubernetes-native workflow: a developer applies a single manifest and Crossplane (running in-cluster) provisions cloud resources, injects Secrets, and the app connects within minutes.

<Frame>
  <img alt="The image shows a five-step Kubernetes-native workflow for transitioning from multi-tool delays to self-service provisioning, including applying a manifest, using the Kubernetes API, provisioning a database, injecting a secret, and connecting an app." />
</Frame>

Common requirements for platform teams

* Single abstraction: one YAML file to declare app + DB + networking + security.
* Namespace isolation: teams operate in their own namespaces with RBAC boundaries.
* Continuous reconciliation: detect drift and self-heal cloud and Kubernetes resources.

<Frame>
  <img alt="The image is a diagram titled &#x22;Infrastructure and Apps Remain Separate,&#x22; listing three platform needs: single abstraction, namespace-based isolation, and continuous reconciliation." />
</Frame>

Crossplane provides these capabilities by treating Kubernetes as the universal control plane and extending it with a few key primitives.

Callout icon example to highlight the main benefit:

> **lightbulb** Crossplane lets platform teams create Kubernetes-native platform APIs so developers use the same GitOps, kubectl, and YAML workflows they already know — simplifying self-service and reducing mean time to provision.

Crossplane’s core concepts

Kubernetes already offers a strong control plane model: declarative APIs, reconciliation loops, RBAC, and a vibrant ecosystem. Crossplane leverages that model and extends it to provision and reconcile external infrastructure. The four core Crossplane concepts are:

| Concept                             | Purpose                                                                                                                                                      | Example                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Providers                           | Adapters that connect Crossplane to cloud APIs (AWS, GCP, Azure) or other control planes. Providers install CRDs for managed resources and act like drivers. | `provider-aws` package                                             |
| Managed resources                   | Kubernetes representations of real cloud resources (S3 bucket, RDS instance). Created by Crossplane using provider APIs.                                     | `Bucket`, `RDSInstance` CRDs                                       |
| Composite resources (XRs)           | Higher-level, opinionated abstractions developers request (e.g., Database). An XR may represent multiple managed resources.                                  | `Database` XR that encapsulates RDS + SecurityGroup + Secret       |
| CompositeResourceDefinitions (XRDs) | CRD-like definitions that declare the API schema for XRs — the platform API that developers use.                                                             | `CompositeResourceDefinition` for `databases.platform.example.com` |

<Frame>
  <img alt="The image is an infographic titled &#x22;Crossplane – Kubernetes for Everything,&#x22; showing four components: Providers, Managed Resources, Composite Resources (XRs), and XRDs, each with a brief description." />
</Frame>

High-level Crossplane flow (platform team → developer)

1. Platform team authors an XRD to define a platform API (schema, fields, defaults).
2. Platform team creates one or more Compositions that map the XRD to concrete resources.
3. Developers create instances of the XR (Composite Resources) in their namespaces; Crossplane matches the XR to a Composition and provisions everything automatically.

Providers

Providers are installed as packages and supply the managed resource CRDs required by Compositions. Example Provider installation:

```yaml theme={null}
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws
spec:
  package: xpkg.upbound.io/upbound/provider-aws:v1.0.0
```

Once a provider is installed and configured (with credentials via a ProviderConfig), you can create managed resources as Kubernetes objects. Managed resources typically include a `spec.forProvider` section containing provider-specific configuration. Crossplane performs the cloud API calls and continuously reconciles state.

Example managed resource (S3 bucket):

```yaml theme={null}
apiVersion: s3.aws.upbound.io/v1beta2
kind: Bucket
metadata:
  name: my-bucket
  namespace: team-frontend
spec:
  forProvider:
    region: us-east-1
    providerConfigRef:
      name: aws-creds
```

XRDs: define the developer-facing platform API

XRDs declare what developers can request and the schema for those requests. Think of an XRD as a CRD focused on Crossplane composition. XRDs:

* Describe fields, types, required properties, and defaults.
* Set the `scope` to `Namespaced` or `Cluster`. Namespaced XRs enable multi-tenancy by allowing teams to create XRs directly in their namespaces (no claims/proxy objects required).

Example XRD snippet:

```yaml theme={null}
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: databases.platform.example.com
spec:
  group: platform.example.com
  names:
    kind: Database
    plural: databases
  scope: Namespaced
```

Developer-facing XR example (requesting a database):

```yaml theme={null}
apiVersion: platform.example.com/v1
kind: Database
metadata:
  name: orders-db
  namespace: team-orders
spec:
  engine: postgresql
  size: medium
```

Compositions: map XRs to concrete resources

A Composition maps an XR schema to one or more composed resources (managed resources, Kubernetes resources, or both). Compositions generally execute as pipelines: each step runs a function that renders or transforms a composed resource. The most-used function is `function-patch-and-transform`, which maps values from the XR into the composed resources.

Typical Composition pipeline flow:

* Developer creates an XR instance.
* Crossplane selects a matching Composition.
* The Composition pipeline runs functions that render composed resource manifests.
* Crossplane creates and continuously reconciles those composed resources.

Example mapping behavior: `function-patch-and-transform` can map `spec.size` from an XR to `spec.forProvider.instanceClass` in an RDS managed resource, translating friendly sizes (e.g., `medium`) into provider-specific instance classes (e.g., `db.r5.large`).

Compose Kubernetes resources and cloud infrastructure together

Compositions are not limited to cloud managed resources. Any Kubernetes resource can be composed — Deployments, Services, ConfigMaps, Ingresses, Secrets — alongside cloud resources such as RDS instances and SecurityGroups. This enables a single platform API to provision an entire microservice stack: app Deployment, network routing, DB instance, and the Secret with credentials.

<Frame>
  <img alt="The image is a diagram titled &#x22;Compose Apps and Infrastructure Together,&#x22; illustrating components such as Deployment, Services, ConfigMaps, Ingress Resource with RDS Instance, and Security Group." />
</Frame>

Example developer XR for a microservice (one apply creates everything):

```yaml theme={null}
apiVersion: platform.acme.io/v1
kind: Microservice
metadata:
  name: user-api
  namespace: team-backend
spec:
  image: acme/user-api:v2
  replicas: 3
  database: postgresql
  ingress: true
```

A Composition for this XR could render:

* A Kubernetes Deployment and Service
* An Ingress resource
* An RDS instance (managed resource)
* A Security Group and network configuration
* A Secret containing the DB connection string (populated by Crossplane)

One resource, one `kubectl apply`, continuous reconciliation — that’s the platform API experience Crossplane enables.

Best practices and operational notes

* Use Namespaced XRs for team multi-tenancy; set RBAC to control who can create which XRs.
* Keep Compositions declarative and idempotent; prefer pipeline functions for transformation logic.
* Install Providers as packages and centralize ProviderConfig credentials in platform-managed namespaces.
* Treat XRDs and Compositions as platform code: version, review, and store them in Git to enable GitOps workflows.

Summary / Key takeaways

* XRDs define your platform API and the schema developers use.
* XRs (Composite Resources) are instances of that API; namespaced XRs simplify multi-tenancy.
* Compositions map XRs to concrete Kubernetes and cloud managed resources, typically using pipeline mode with functions for rendering and transformation.
* You can compose any Kubernetes resource alongside cloud infrastructure to provide unified, GitOps-friendly platform APIs.

<Frame>
  <img alt="The image lists four key takeaways related to platform API, multi-tenancy, pipeline compositions, and Kubernetes resources, highlighted with numbered colored markers." />
</Frame>

Further reading and references

* Crossplane: [https://crossplane.io/](https://crossplane.io/)
* Kubernetes kubectl reference: [https://kubernetes.io/docs/reference/kubectl/](https://kubernetes.io/docs/reference/kubectl/)
* Argo CD (GitOps): [https://argo-cd.readthedocs.io/en/stable/](https://argo-cd.readthedocs.io/en/stable/)
* Terraform: [https://www.terraform.io/](https://www.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prep-course-certified-cloud-native-platform-engineer-cnpe/module/756ffaae-767b-4743-9724-c05d3fbf9a18/lesson/55341bf2-b35e-4453-b9d0-b4dd3aaaf898)
