# Owner References And Garbage Collection

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Building-The-WebApp-Operator-Core-Reconcile/Owner-References-And-Garbage-Collection/page

Explains Kubernetes ownerReferences and garbage collection, showing how controllers set controller references to prevent orphaned child resources and enable automatic cleanup and reconciliation

Think of owner references as the family tree Kubernetes uses to automatically clean up related resources.

Imagine a parent WebApp named `site` with three children: a Deployment named `site`, a Service named `site`, and a ConfigMap named `site-config`. Each child points back to the parent. What happens if you delete the parent?

```bash theme={null}
$ kubectl delete webapp site
```

If the children aren’t linked to the parent, they remain in the cluster as orphaned resources. Orphans continue to occupy names, Service endpoints, and configuration even though the WebApp that depended on them no longer exists.

<Frame>
  <img alt="The image depicts orphaned objects from a WebApp, labeled as &#x22;site&#x22; and &#x22;site-config,&#x22; all marked as &#x22;Orphaned.&#x22; It indicates they are still consuming resources without an explanation." />
</Frame>

Kubernetes owner references solve this cleanup problem. An owner reference is metadata on a child object that points back to its parent resource. In this example, the parent is the WebApp and the children are the Deployment, Service, and ConfigMap. The key detail: the reference points to the parent's UID, not only its name. A UID is Kubernetes’ unique identity for an object, so using the UID ensures the cluster can distinguish two objects that share a name but are different instances.

Example owner reference snippet:

```yaml theme={null}
ownerReferences:
  - apiVersion: example.com/v1
    kind: WebApp
    name: site
    uid: 7c2f9a11-...e04b
```

Because the UID is unique, deleting a WebApp and later creating another WebApp with the same name will not confuse the garbage collector—the UIDs differ, so Kubernetes treats them as distinct objects.

In the Go operator world, the common helper is `controllerutil.SetControllerReference` from the [`controller-runtime`](https://github.com/kubernetes-sigs/controller-runtime) project. You pass the parent object (the WebApp), the child object you will create, and the controller `Scheme` (the registry that maps Go types to Kubernetes API kinds).

Call the helper before creating the child so the owner reference is set at creation time:

```go theme={null}
if err := controllerutil.SetControllerReference(webapp, deploy, r.Scheme); err != nil {
    return err
}
```

When the WebApp is deleted, Kubernetes garbage collection can automatically remove owned children. This means you usually do not need to write manual delete logic for simple child resources—the cluster garbage collector handles cleanup when owner references are set correctly.

Example deletion flow:

```bash theme={null}
$ kubectl delete webapp site
webapp.example.com "site" deleted
$ kubectl get deploy,svc,cm -l app=site
No resources found in default namespace.
```

When the controller is configured to watch owned Deployments, Services, and ConfigMaps, `controller-runtime` will receive events for those children and enqueue the parent WebApp for reconciliation when changes occur.

<Frame>
  <img alt="The image illustrates a process where a controller watches for changes in owned children, such as Deployment, Service, and ConfigMap, and re-queues the parent when a change is detected." />
</Frame>

This gives your reconciler another chance to repair missing or modified children during subsequent reconciliation loops.

Best practices summary

| Scenario                                         | Owner reference effect                                            | When to use                                                                           |
| ------------------------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Prevent orphaned resources after parent deletion | Child is garbage-collected when parent is removed                 | Use for simple children created by the controller (ConfigMaps, Deployments, Services) |
| Reconcile on child change                        | Changes to child enqueue parent for reconciliation (when watched) | Use when you want a single reconciliation point for parent-managed children           |
| Cross-namespace ownership                        | Not supported unless the owner is cluster-scoped                  | Avoid ownerReferences across namespaces; prefer explicit cleanup or different design  |

<Callout icon="lightbulb">
  Set the controller reference for every child the WebApp creates before you call the API to create that child. This avoids orphaned resources and makes ownership visible with `kubectl` inspection.
</Callout>

<Callout icon="warning">
  Owner references have important constraints: owners and dependents must be in the same namespace unless the owner is cluster-scoped. Also, be cautious when setting ownerReferences for resources created by users outside the operator—you may unintentionally enable deletion of user-managed objects.
</Callout>

For this lesson, follow this simple rule: every child the WebApp creates should get a controller reference to the WebApp before creation. Doing so prevents orphaned resources, enables automatic garbage collection, and integrates child-change events into the parent’s reconciliation lifecycle.

<Frame>
  <img alt="The image provides a rule for setting a controller reference for every child created by a web application before it gets created to prevent orphaned resources." />
</Frame>

Links and references

* Kubernetes owner/dependent docs: [https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)
* Kubernetes UIDs: [https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids)
* Garbage collection in Kubernetes: [https://kubernetes.io/docs/concepts/workloads/controllers/garbage-collection/](https://kubernetes.io/docs/concepts/workloads/controllers/garbage-collection/)
* controller-runtime `SetControllerReference`: [https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/controller/controllerutil#SetControllerReference](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/controller/controllerutil#SetControllerReference)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/2c5de16a-1141-4e94-9284-e6c9d55a2b7f" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/ef5c1b44-311a-415f-8eeb-8a460e759cfe/lesson/2cd4e01e-f876-46b9-ac4b-bb0a11becd4d" />
</CardGroup>
