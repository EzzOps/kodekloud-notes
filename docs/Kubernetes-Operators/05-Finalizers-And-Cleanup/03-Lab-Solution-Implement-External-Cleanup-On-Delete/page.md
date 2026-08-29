# NAME  STATUS       AGE
kubectl describe webapp site
# Events:
#   Warning  CleanupFailed  external DNS delete timed out
```

Owner references and finalizers are complementary:

<Frame>
  <img alt="The image is a comparison of Kubernetes tools, &#x22;Owner references&#x22; and &#x22;Finalizers,&#x22; highlighting their roles in managing resources within a cluster and tasks Kubernetes cannot handle by itself." />
</Frame>

|         Mechanism | Best for                                                      | Behavior                                                                                                                               |
| ----------------: | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `ownerReferences` | In-cluster children (Pods, Deployments, Services, ConfigMaps) | Kubernetes garbage-collects children automatically when the owner is deleted.                                                          |
|      `finalizers` | External resources or any cleanup Kubernetes cannot perform   | The API server delays object removal until all finalizers are removed; controllers must remove their finalizer after cleanup succeeds. |

Best practices for finalizers and cleanup

* Use stable, namespaced finalizer names like `webapp.kodekloud.com/finalizer` to show ownership and avoid collisions.
* Each controller should only remove the finalizers it added.
* Ensure cleanup is idempotent and resilient to transient errors.
* Surface blocking errors via Status, Events, and Logs.

There is an administrative escape hatch when cleanup is irrecoverably stuck: manually remove the finalizer. This forces Kubernetes to forget the object even if external cleanup did not complete.

```bash theme={null}
kubectl patch webapp site --type=merge \
  -p '{"metadata":{"finalizers":[]}}'
```

> **warning** Force-removing finalizers bypasses cleanup. Use it only as a recovery or emergency action, and after documenting the consequences.

> **lightbulb** Always add your controller's finalizer before creating external resources, and make cleanup idempotent so retries and crashes are safe.

Demo overview

The accompanying demo implements this pattern in a webapp reconciler: the controller adds a finalizer during normal reconcile, detects deletion via `deletionTimestamp`, performs a simulated external cleanup, removes its finalizer upon success, and then allows Kubernetes to complete the deletion.

Links and references

* [Kubernetes API Conventions: Finalizers](https://kubernetes.io/docs/reference/using-api/api-concepts/#finalizers)
* [Owner References and Garbage Collection](https://kubernetes.io/docs/concepts/workloads/controllers/garbage-collection/)
* [Controller pattern: Finalizers and Cleanup](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/6a375c4e-4bda-4d13-a58f-4d85961676cc/lesson/ba932ebc-db78-4929-8307-b8482caaecbe)


# Lab Solution Implement External Cleanup On Delete

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Finalizers-And-Cleanup/Lab-Solution-Implement-External-Cleanup-On-Delete/page

Demonstrates using a Kubernetes finalizer and controller to ensure external resource cleanup before a custom WebApp resource is fully deleted.

This lesson demonstrates how a finalizer ensures external cleanup is completed before a custom WebApp resource is fully removed from a Kubernetes cluster. The environment for this exercise is already prepared — files and cluster state are in place. Focus on the command outputs and the Kubernetes behavior that illustrate how finalizers protect external resources.

Prerequisites

* A Kubernetes cluster with the WebApp custom resource and a controller that implements a finalizer-based external cleanup.
* Namespace: `webapp-demo` (for the WebApp CR) and `webapp-external` (for the external ConfigMap).

Steps

1. Confirm the WebApp custom resource exists and inspect its finalizers.

```bash theme={null}
$ kubectl -n webapp-demo get webapp site
NAME   AGE
site   2m48s

$ kubectl -n webapp-demo get webapp site -o jsonpath='{.metadata.finalizers}{"\n"}'
["webapp.kodekloud.com/finalizer"]
```

The JSONPath output shows the finalizer `webapp.kodekloud.com/finalizer` attached to the WebApp resource. This finalizer prevents the API server from permanently removing the object until the controller performing external cleanup removes the finalizer.

2. Confirm the external ConfigMap exists and has no owner references.

```bash theme={null}
$ kubectl -n webapp-external get cm site-external
NAME            DATA   AGE
site-external   2      3m33s

$ kubectl -n webapp-external get cm site-external -o jsonpath='{.metadata.ownerReferences}{"\n"}'
```

The second command returns an empty line, indicating there are no `ownerReferences` set on the external ConfigMap. Because the external resource is not owned by the WebApp object, it requires explicit external cleanup by the controller (which is coordinated via the finalizer).

> **lightbulb** Finalizers are used when deleting a Kubernetes object requires external cleanup steps (for example, deleting resources in another namespace or cleaning up entries in an external system). The finalizer blocks the API server from completing deletion until the controller performs the cleanup and removes the finalizer.

3. Delete the WebApp resource and observe the result.

```bash theme={null}
$ kubectl -n webapp-demo delete webapp site --wait=true --timeout=60s
webapp.webapp.kodekloud.com "site" deleted
```

When you issue this delete, the API server marks the WebApp with a deletion timestamp but will not remove the resource until the finalizer is cleared. The controller should detect the pending deletion, perform external cleanup (delete the external ConfigMap in `webapp-external`), then remove the finalizer so the API server can complete the deletion.

4. Verify that both the WebApp resource and the external ConfigMap are gone.

```bash theme={null}
$ kubectl -n webapp-demo get webapp site
Error from server (NotFound): webapps.webapp.kodekloud.com "site" not found

$ kubectl -n webapp-external get cm site-external
Error from server (NotFound): configmaps "site-external" not found
```

Both resources are now absent. This confirms the finalizer protected the WebApp resource from being fully deleted until the external cleanup (removal of the external ConfigMap) was completed by the controller.

Summary

| Resource             | Namespace         | Name            | Purpose                                                                |
| -------------------- | ----------------- | --------------- | ---------------------------------------------------------------------- |
| Custom Resource (CR) | `webapp-demo`     | `site`          | WebApp custom resource with finalizer `webapp.kodekloud.com/finalizer` |
| ConfigMap (external) | `webapp-external` | `site-external` | External resource that requires explicit cleanup (no ownerReferences)  |

Links and references

* [Kubernetes Finalizers](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#finalizers)
* [Kubernetes API Concepts: Deletion](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)
* [Build and Run Controllers](https://kubernetes.io/docs/concepts/architecture/controller/)

This exercise illustrates the pattern where a finalizer coordinates a controller-driven cleanup of external resources before the API server completes deletion of a Kubernetes object.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/6a375c4e-4bda-4d13-a58f-4d85961676cc/lesson/ea1e0265-598d-4dfe-8587-79462ce1f492)
