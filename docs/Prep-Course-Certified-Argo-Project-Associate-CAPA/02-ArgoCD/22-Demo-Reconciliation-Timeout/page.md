# Add the 'kind-argo-cluster-1' context to Argo CD
argocd cluster add kind-argo-cluster-1
```

Example (abridged) output:

```json theme={null}
{"level":"info","msg":"ServiceAccount \"argocd-manager\" created in namespace \"kube-system\"","time":"2025-10-23T17:29:59Z"}
{"level":"info","msg":"ClusterRole \"argocd-manager-role\" created","time":"2025-10-23T17:29:59Z"}
{"level":"info","msg":"ClusterRoleBinding \"argocd-manager-role-binding\" created","time":"2025-10-23T17:29:59Z"}
{"level":"info","msg":"Created bearer token secret \"argocd-manager-long-lived-token\" for ServiceAccount \"argocd-manager\"","time":"2025-10-23T17:29:59Z"}
Cluster 'https://172.26.60.148:38449' added
```

Argo CD stores the target cluster's connection data (API server URL, CA, token) as a Kubernetes Secret in the Argo CD namespace of the control cluster.

Switch back to the control cluster and list secrets in the Argo CD namespace to view the stored cluster secret:

```bash theme={null}
# Switch to the cluster where Argo CD is installed (control plane)
kubectl config use-context docker-desktop
Switched to context "docker-desktop".

# List secrets in the argocd namespace
kubectl -n argocd get secrets
NAME                                   TYPE    DATA   AGE
argocd-initial-admin-secret            Opaque  1      10h
argocd-notifications-secret            Opaque  0      10h
argocd-redis                           Opaque  1      10h
argocd-secret                          Opaque  5      10h
cluster-172.26.60.148-931191031        Opaque  3      46s
```

The `cluster-<ip>-<suffix>` secret contains the API server URL, CA data, and token Argo CD uses to communicate with the KinD cluster.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the Settings → Clusters page with cluster details for https://172.26.60.148:38449 (name: kind-argo-cluster-1), credentials Token/Basic Auth, and namespaces set to All namespaces. The connection state reads &#x22;Unknown&#x22; and notes the cluster has no applications and is not being monitored." />
</Frame>

If you open the Argo CD UI (Settings → Clusters) the new cluster may show a Connection status of "Unknown" initially. This often happens when Argo CD has not yet created or is not actively monitoring any applications on that cluster.

## 4) Create an application that targets the remote cluster

In the Argo CD Create Application form you can:

* Set the Git repository and path containing the manifests.
* Choose the destination cluster (the KinD cluster) and the target namespace.
* Enable Automatic Sync and check "Auto-create namespace" so Argo CD will create the namespace on the destination if missing.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the &#x22;Create Application&#x22; form for &#x22;health-check-app-2&#x22; (project: default) with Automatic sync selected and &#x22;Enable Auto-Sync&#x22; checked. The left sidebar displays navigation (Applications, Settings, User Info) and application/health status filters." />
</Frame>

Select the repository and the path where the application manifests live. In this demo the repo contains a folder for the Health Check app:

<Frame>
  <img alt="A dark-themed web interface for a Git repository (kk-org/gitops-argocd-capa) showing a list of folders and recent commit messages. The right sidebar displays repo details like license, size and language stats, and the top bar shows navigation tabs (Code, Issues, Pull Requests, etc.)." />
</Frame>

Choose the correct path (for example `./health-check`) and select the destination cluster and namespace (`health-check-app-2` in this example):

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing an application create/edit form with the HEAD path set to &#x22;./health-check&#x22; and DESTINATION fields populated with a cluster URL and namespace (&#x22;health-check-app-2&#x22;). The left sidebar shows navigation (Applications, Settings) and application filter/status panels." />
</Frame>

## 5) Application sync and health checks

After creation, Argo CD syncs manifests to the target cluster. This example app uses a ConfigMap-based health check: certain data values determine whether a resource is healthy. If a monitored value is considered unhealthy (for example `TRIANGLE_COLOR: "white"`), Argo CD will show the application's health as Degraded even if it is successfully synced.

Example ConfigMap excerpt:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: moving-shapes-colors
  namespace: health-check-app-2
  annotations:
    argocd.argoproj.io/tracking-id: health-check-app-2:/ConfigMap:health-check-app-2/moving-shapes-colors
data:
  CIRCLE_COLOR: "pink"
  OVAL_COLOR: "lightgreen"
  RECTANGLE_COLOR: "blue"
  SQUARE_COLOR: "orange"
  TRIANGLE_COLOR: "white"
```

Because `TRIANGLE_COLOR` is set to `white` and the health check treats that as unhealthy, the application appears Degraded while its sync status is Synced:

<Frame>
  <img alt="Screenshot of the Argo CD web interface showing an application named &#x22;health-check-app-2&#x22; with a &#x22;Degraded&#x22; health indicator and a &#x22;Synced&#x22; status. The main pane displays a resource graph linking components like &#x22;moving-shapes-colors&#x22; and &#x22;random-shapes&#x22; to their pods." />
</Frame>

From the Applications list you can confirm the destination cluster for this app is the KinD cluster (different from apps targeting the control cluster):

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing a list of Kubernetes applications with project/name, source and destination fields and colored health/sync status indicators. The left sidebar shows navigation and application filters while the top has buttons for creating, syncing and refreshing apps." />
</Frame>

## 6) Verify the application on the remote cluster

Switch your kubectl context to the KinD cluster and confirm the namespace and resources were created by Argo CD:

```bash theme={null}
# Switch to the KinD cluster
kubectl config use-context kind-argo-cluster-1
Switched to context "kind-argo-cluster-1".

# List namespaces on the KinD cluster
kubectl get ns
NAME                   STATUS    AGE
default                Active    75m
health-check-app-2     Active    79s
kube-node-lease        Active    75m
kube-public            Active    75m
kube-system            Active    75m
local-path-storage     Active    73m
```

You can also inspect pods and other resources in `health-check-app-2` to confirm the sync succeeded. Pods may briefly show `ContainerCreating` while images are pulled.

## Summary

* Use `argocd cluster add <context>` to register remote clusters with Argo CD. This creates a ServiceAccount and stores cluster credentials as a Secret in the Argo CD control cluster.
* Registered clusters appear as destinations in the Argo CD UI and can be targeted by Applications, either from the UI or via Application CRs.
* A cluster showing Connection status "Unknown" may simply have no managed applications yet — creating an application that targets it causes Argo CD to actively monitor it.
* Health checks can mark an otherwise-synced application as Degraded based on resource content (ConfigMaps, status probes, etc.).

## Links and references

* Argo CD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Kubernetes kubectl: [https://kubernetes.io/docs/reference/kubectl/](https://kubernetes.io/docs/reference/kubectl/)
* Argo CD CLI reference: [https://argo-cd.readthedocs.io/en/stable/cli\_commands/](https://argo-cd.readthedocs.io/en/stable/cli_commands/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/66cc159d-1eb9-4813-bcdf-14e816d61efe" />
</CardGroup>


# Demo Reconciliation Timeout

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Reconciliation-Timeout/page

How to shorten Argo CD repository reconciliation interval, patch argocd-cm timeout.reconciliation, restart argocd-repo-server, and enable Auto-Sync so changes apply faster.

This guide explains how Argo CD polls Git/Helm repositories, how to shorten the reconciliation/polling interval, and how to ensure the change takes effect by restarting the repo server. Use this to make Argo CD detect commits faster than the default interval.

What you'll learn:

* Default Argo CD polling behavior
* How to configure `timeout.reconciliation` in `argocd-cm`
* How to restart `argocd-repo-server` so the new interval is used
* How to enable Auto-Sync so detected changes are applied automatically

Default behavior

By default, Argo CD checks Git or Helm repositories at intervals up to 3 minutes (see the Argo CD FAQ). If you need faster detection of commits, adjust the reconciliation timeout.

<Frame>
  <img
    alt="A screenshot of the Argo CD documentation FAQ page showing the question &#x22;How
often does Argo CD check for changes to my Git or Helm repository?&#x22; with the
main text in the center, navigation links on the left, and a table of contents
on the
right."
  />
</Frame>

Create a sample application

Create an Argo CD Application that points to a Git repository containing a simple Deployment manifest. Example source/destination settings:

```yaml theme={null}
