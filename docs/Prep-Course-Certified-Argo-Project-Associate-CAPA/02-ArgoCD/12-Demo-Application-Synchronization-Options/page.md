# Enter Username: admin
# Enter Password: <your-admin-password>
```

Re-run the create command after successful login:

```bash theme={null}
argocd app create health-check-app \
  --repo http://host.docker.internal:5000/kk-org/gitops-argocd-capa \
  --path ./health-check \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace health-check \
  --project default \
  --revision HEAD \
  --sync-policy none \
  --sync-option CreateNamespace=true
# application 'health-check-app' created
```

Back in the Argo CD UI you should now see the new application in OutOfSync / Missing state (before sync):

<Frame>
  <img alt="Screenshot of the Argo CD web UI showing the &#x22;health-check-app&#x22; application marked OutOfSync and Missing. A synchronization panel is open on the right with sync options (Auto-create Namespace checked) and three resources selected for sync." />
</Frame>

## Sync the application and verify resources

Sync the application. Argo CD will create the namespace, then the ConfigMap, the Service, and finally the Deployment. The pod will initially show states like ContainerCreating / Progressing in the UI:

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing details for the pod &#x22;random-shapes-5d55cc76-lc95h&#x22; in the health-check namespace. The pod is in state &#x22;ContainerCreating&#x22; with health &#x22;Progressing,&#x22; and the left sidebar shows application navigation and resource filters." />
</Frame>

You can also verify namespace and pod status with kubectl:

```bash theme={null}
kubectl get namespaces
# Example output:
# NAME                STATUS    AGE
# default             Active    16h
# argocd              Active    4h47m
# health-check        Active    27s
kubectl -n health-check get pods
# Example output:
# NAME                           READY   STATUS    RESTARTS   AGE
# random-shapes-5d55cc76-lc95h   1/1     Running   0          34s
```

## Add a custom health check for ConfigMap

In this demo the triangle becomes invisible when `TRIANGLE_COLOR` is `white`. We'll use that condition to mark the application as Degraded by adding a custom health check. Edit the argocd-cm ConfigMap in the `argocd` namespace and add a Lua snippet under the key `resource.customizations.health.ConfigMap`. The script below sets `Degraded` when `TRIANGLE_COLOR` equals `white` and returns a helpful message.

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.health.ConfigMap: |
    hs = {}
    hs.status = "Healthy"
    hs.message = ""
    -- If the triangle color is white, mark as Degraded
    if obj.data ~= nil and obj.data.TRIANGLE_COLOR == "white" then
      hs.status = "Degraded"
      hs.message = "Use any color other than white for TRIANGLE_COLOR"
    end
    return hs
```

> **lightbulb** Custom health checks are Lua scripts executed by Argo CD. Be careful with Lua equality operators: `==` tests equality, `~=` tests inequality.

Apply the change by editing the ConfigMap:

```bash theme={null}
kubectl -n argocd edit configmap argocd-cm
# paste the resource.customizations.health.ConfigMap entry and save
```

After saving the ConfigMap, refresh the Application in the Argo CD UI. Because the deployed ConfigMap `moving-shapes-colors` has `TRIANGLE_COLOR` set to `white`, Argo CD will evaluate the health hook and mark the ConfigMap (and the Application) as Degraded with the message you supplied ("Use any color other than white for TRIANGLE\_COLOR").

## Resolve the degraded state

To resolve the degraded state, change the `TRIANGLE_COLOR` value either in the Git repo and sync, or edit the deployed ConfigMap directly and then restart pods if necessary so they pick up the change.

Example: edit the deployed ConfigMap in the `health-check` namespace:

```bash theme={null}
kubectl -n health-check edit configmap moving-shapes-colors
# change TRIANGLE_COLOR: white -> TRIANGLE_COLOR: red
```

Once the ConfigMap no longer matches the Degraded condition, Argo CD's custom health check will evaluate to Healthy and the application health will return to Healthy.

The Argo CD UI resource tree will then display the ConfigMap, Service, Deployment/pods, and overall application health:

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the &#x22;health-check-app&#x22; application with sync and health status panels at the top and a resource tree diagram on the right listing components like moving-shapes-colors, random-shapes-svc, and pods. The left sidebar shows navigation and resource filters." />
</Frame>

## Summary

* Add custom health checks by editing `argocd-cm` and providing Lua scripts under `resource.customizations.health.*`.
* Use `resource.customizations.health.ConfigMap` to apply checks for core ConfigMap resources.
* Argo CD executes these Lua checks and surfaces any custom `status` and `message` in the UI for the resource and its parent Application.

## Links and references

* Argo CD Resource Health docs: [https://argo-cd.readthedocs.io/en/stable/operator-manual/resource\_customizations/](https://argo-cd.readthedocs.io/en/stable/operator-manual/resource_customizations/)
* Kubernetes Concepts: [https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/b96c9445-9c82-499b-b50e-30ab59300181)


# Demo Application Synchronization Options

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Application-Synchronization-Options/page

Explains Argo CD sync policies — Auto Sync, Self Heal, and Prune for keeping Kubernetes cluster state aligned with Git.

This lesson explains Argo CD synchronization policies for an application: Auto‑Sync, Self‑Heal, and Prune Resources. These options determine how Argo CD keeps the cluster's live state aligned with the desired state declared in Git (GitOps workflow).

In the Argo CD application settings for `health-check`, you can enable sync policies:

* Auto‑Sync: Argo CD watches the Git repository and automatically applies detected manifest changes to the cluster (no manual sync required).
* Self‑Heal: If a resource is changed or deleted directly in the cluster (out‑of‑band), Argo CD will attempt to reconcile the resource back to the manifest in Git.
* Prune Resources: When a resource is removed from Git, Argo CD will delete the corresponding resource from the cluster on the next sync.

> **lightbulb** When Auto‑Sync is enabled, Argo CD applies changes detected in Git automatically. Self‑Heal reconciles manual cluster changes to match Git. Prune removes cluster resources that were removed from Git. With Auto‑Sync + Self‑Heal + Prune enabled, resources present in Git will be recreated if manually deleted, while resources removed from Git will be deleted from the cluster.

***

## 1) Auto‑Sync — automatically apply updates from Git

To see Auto‑Sync in action, change the Deployment manifest in your Git repository (for example, increase replicas from 1 to 2). Example Deployment manifest:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: random-shapes
spec:
  selector:
    matchLabels:
      app: random-shapes
  replicas: 2
  template:
    metadata:
      labels:
        app: random-shapes
    spec:
      containers:
        - name: random-shapes
          image: siddharth67/php-random-shapes:v1
          imagePullPolicy: Always
          envFrom:
            - configMapRef:
                name: moving-shapes-colors
```

* Commit and push the change to the repository.
* With Auto‑Sync enabled on the `health-check` application, Argo CD will detect the change and apply it automatically.

Verify the Deployment scaled to 2 replicas:

```bash theme={null}
$ kubectl -n health-check get deploy random-shapes
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
random-shapes   2/2     2            2           10m
```

This output confirms Auto‑Sync applied the updated manifest from Git without requiring a manual sync in the Argo CD UI.

***

## 2) Self‑Heal — Argo CD reconciles manual cluster changes

If Self‑Heal is enabled and you manually delete or modify a resource in the cluster, Argo CD will detect the divergence and restore the resource to match the manifest in Git.

Example sequence deleting a Service:

```bash theme={null}
$ kubectl -n health-check get svc
NAME                 TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
random-shapes-svc    NodePort   10.110.210.43   <none>        80:31366/TCP    5m

$ kubectl -n health-check delete svc random-shapes-svc
service "random-shapes-svc" deleted
```

After a short time (Argo CD reconciliation interval), the Service is recreated because the Service manifest still exists in Git:

```bash theme={null}
$ kubectl -n health-check get svc
NAME                 TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
random-shapes-svc    NodePort   10.110.210.43   <none>        80:31366/TCP    10s
```

This demonstrates Self‑Heal: Argo CD detected the manual deletion and re‑applied the resource from Git.

***

## 3) Prune Resources — remove resources from the cluster when removed from Git

When you remove a manifest from Git and have Auto‑Sync with Prune enabled, Argo CD will delete the corresponding cluster resource during the next sync.

Example outcome after removing the Service manifest and allowing Auto‑Sync + Prune to take effect:

```bash theme={null}
$ kubectl -n health-check get svc
No resources found in health-check namespace.
```

Because the Service was removed from Git and Prune was enabled, Argo CD deleted it from the cluster.

***

## Quick reference — behavior comparison

| Sync Option | Purpose                                   | Typical behavior                                                   |
| ----------- | ----------------------------------------- | ------------------------------------------------------------------ |
| Auto‑Sync   | Apply Git changes automatically           | Detects Git commits and applies manifests without manual sync      |
| Self‑Heal   | Reconcile manual cluster changes          | Restores resources modified or deleted in the cluster to match Git |
| Prune       | Remove cluster resources removed from Git | Deletes resources from the cluster that no longer exist in Git     |

Use combinations of these options to match your operational model: continuous delivery with self‑correction (Auto‑Sync + Self‑Heal + Prune), or a more controlled/manual approach (disable Auto‑Sync and trigger syncs manually).

***

## Summary

* Auto‑Sync automatically applies Git changes to the cluster.
* Self‑Heal reconciles and restores resources when manual modifications occur in the cluster.
* Prune Resources removes cluster resources when they are deleted from Git.
* Combine these policies to implement the GitOps workflow that fits your environment.

## Links and references

* [Argo CD — Learn KodeKloud course](https://learn.kodekloud.com/user/courses/gitops-with-argocd)
* [Argo CD official documentation](https://argo-cd.readthedocs.io/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/17053d38-cf7f-445a-9090-2694a38be55a)
