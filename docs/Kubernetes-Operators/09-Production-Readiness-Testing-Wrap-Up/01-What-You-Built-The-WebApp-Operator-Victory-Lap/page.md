# 1) Build the image with an explicit image reference (include registry and tag)
make docker-build IMG=myregistry.example.com/webapp-operator:v1

# 2) Push the image so the cluster can pull it
make docker-push IMG=myregistry.example.com/webapp-operator:v1

# 3) Apply the install manifests (Kustomize build + kubectl apply)
make deploy IMG=myregistry.example.com/webapp-operator:v1
```

IMG is not cosmetic — the exact image reference you set becomes part of the generated install manifests (the container image field in the manager Deployment). If you set an incorrect `IMG` the cluster may pull the wrong image or the controller may fail to start.

After deploying, verify the controller manager is running and is using the image you pushed:

```bash theme={null}
# Confirm the Deployment exists and shows the expected image
kubectl -n <namespace> get deployment webapp-operator-controller-manager -o yaml | grep image

# Check pods and logs
kubectl -n <namespace> get pods
kubectl -n <namespace> logs deploy/webapp-operator-controller-manager -c manager
```

Finally, create a WebApp custom resource and confirm the installed operator reconciles it from inside the cluster — the same behavior you validated locally should now occur with the controller running as a Kubernetes workload.

<Frame>
  <img alt="The image displays a three-step process titled &#x22;The Lab: Ship It End to End,&#x22; which includes building/using an image, deploying manifests, and verifying the controller manager running, each marked as complete." />
</Frame>

This section closes with a brief look at Operator Lifecycle Manager (OLM). OLM is not required for every operator deployment, but it's important to understand its model: bundles, ClusterServiceVersions (CSVs), catalogs, and subscriptions. Raw manifests or a kustomize-based install are sufficient for many environments; OLM becomes valuable when you need install metadata, upgrade channels, and marketplace-style distribution.

By the end of this section you will have a repeatable packaging and deployment path for the web app Operator: a container image, published install manifests, a verified manager running in-cluster, and an upgrade story you can use going forward.

<Callout icon="lightbulb">
  When using the Makefile targets, always set `IMG` to the exact image reference you intend to deploy (including registry and tag). The deployed manifests will reference that value, so an incorrect `IMG` will cause the cluster to pull a different image or fail to start the controller.
</Callout>

<Callout icon="warning">
  Ensure you have credentials and write access to the target registry before running `make docker-push`. Also confirm the cluster can pull from that registry (private registries may require imagePullSecrets).
</Callout>

## References

* Kubebuilder: [https://book.kubebuilder.io/](https://book.kubebuilder.io/)
* Kustomize: [https://kustomize.io/](https://kustomize.io/)
* Operator Lifecycle Manager (OLM): [https://olm.operatorframework.io/](https://olm.operatorframework.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/5a9bfe56-bc26-4325-b659-06027d4e815f/lesson/f81893d3-e35e-4a4a-a360-ab8e27c866e4" />
</CardGroup>


# What You Built The WebApp Operator Victory Lap

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Production-Readiness-Testing-Wrap-Up/What-You-Built-The-WebApp-Operator-Victory-Lap/page

Guide to building a WebApp Kubernetes operator that uses CRDs, reconcile loops, child resources, finalizers, status, events, and production readiness practices.

Take a moment to review the path you’ve traveled building the WebApp operator. What started as a simple idea — “I want a single Kubernetes object to describe a small web application” — became a working controller pattern that turns intent into cluster behavior.

At a high level, the operator you built contains these recurring elements:

* A custom API (CRD) that expresses intent.
* A controller with a reconcile loop that enforces that intent.
* Child resources (Deployments, Services, ConfigMaps) that implement the desired state.
* Lifecycle edges (finalizers, ownerReferences) to manage deletion and ownership.
* Status and events to surface operator state to users.
* Packaging/deployment for running the controller in a real cluster.

The first win: the API. A CustomResourceDefinition made `WebApp` a first-class resource. The `spec` lets users declare a promise (for example, which container image and how many replicas). This single object simplifies the user experience — they no longer need to assemble each Kubernetes detail manually.

The controller gives that API a heartbeat. Reconcile loops watch `WebApp` objects, compare desired state to actual cluster state, and move the cluster toward the specification. That compare-and-fix loop is the center of the operator pattern: the user declares a desired state, and the controller works continuously to align reality with that request.

<Frame>
  <img alt="The image illustrates a cyclical process titled &#x22;The Controller's Heartbeat – Reconcile,&#x22; showing four stages: CR (Contract), Reconcile (Repair), Managed work (Real resources), and Status/events (Signals), connected by a &#x22;core loop.&#x22;" />
</Frame>

You implemented the child resources that make the web app real. A `Deployment` runs the application Pods, a `Service` provides a stable network entry, and a `ConfigMap` carries configuration. Those YAML manifests are no longer ad-hoc files — they are resources that the controller creates and maintains from the parent `WebApp` CR.

<Frame>
  <img alt="The image is a diagram showing a &#x22;WebApp&#x22; as the parent resource connected to three child resources: &#x22;Deployment,&#x22; &#x22;Service,&#x22; and &#x22;ConfigMap,&#x22; each with their respective functions in a computing context." />
</Frame>

OwnerReferences connected those children back to the parent CR. With ownerReferences in place, Kubernetes knows the ownership relationship and can garbage-collect or reason about the hierarchy instead of treating every object as unrelated.

<Frame>
  <img alt="The image illustrates a relationship diagram showing a &#x22;WebApp&#x22; as the parent linked to &#x22;Deployment,&#x22; &#x22;Service,&#x22; and &#x22;ConfigMap&#x22; via owner references." />
</Frame>

Status and events make the operator readable from the outside. `status` fields report what the controller observed so users don’t need to inspect every child resource. Events are short, human-friendly signals recorded as separate Kubernetes Event objects when meaningful things happen (Events are not a subfield of `status`). Together, they turn an otherwise silent controller into something a user can understand quickly.

<Callout icon="lightbulb">
  Use `status` for persistent operator-observed state (conditions, replica counts, URLs). Use Events for transient, human-readable signals like "Deployment created" or "ScalingReplicaSet". Events are stored separately as Event objects in Kubernetes.
</Callout>

Example `status` snippet:

```yaml theme={null}
status:
  phase: Ready
  readyReplicas: 3
  url: web-app.svc
```

Example Events (Events are separate Kubernetes objects; shown here to illustrate typical messages):

```yaml theme={null}
