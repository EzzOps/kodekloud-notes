# List namespaces
kubectl get ns
```

Example output after synchronization:

```bash theme={null}
NAME                 STATUS   AGE
argocd               Active   169m
default              Active   14h
highway-animation    Active   32s
kube-node-lease      Active   14h
kube-public          Active   14h
kube-system          Active   14h
```

```bash theme={null}
# List resources in the highway-animation namespace
kubectl -n highway-animation get all
```

Example output:

```bash theme={null}
NAME                                         READY   STATUS    RESTARTS   AGE
pod/highway-animation-56456787df-h69n7      1/1     Running   0          39s

NAME                               TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE
service/highway-animation-service  NodePort   10.103.55.242   <none>        3000:32000/TCP    42s

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/highway-animation  1/1     1            1           41s

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/highway-animation-56456787df     1         1         1       41s
```

The application in this example renders vehicles on a highway. The Deployment in Git uses image tag `blue`, so the running app shows blue vehicles.

## Deployment (desired state in Git)

Deployment manifest stored in Git (replicas: 1, POD\_COUNT env = "1"):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
  namespace: highway-animation
spec:
  replicas: 1
  selector:
    matchLabels:
      app: highway-animation
  template:
    metadata:
      labels:
        app: highway-animation
    spec:
      containers:
      - name: highway-animation
        image: siddharth67/highway-animation:blue
        ports:
        - containerPort: 3000
        env:
        - name: POD_COUNT
          value: "1"
```

## Manual change on the cluster (drift)

If a developer edits the live Deployment directly (for example using `kubectl edit`) and increases replicas to 5 and updates POD\_COUNT to "5", the live cluster will diverge from Git:

```yaml theme={null}
spec:
  replicas: 5
  template:
    spec:
      containers:
      - name: highway-animation
        image: siddharth67/highway-animation:blue
        env:
        - name: POD_COUNT
          value: "5"
```

After saving the edit, kubectl confirms the change:

```bash theme={null}
kubectl -n highway-animation get deployments.apps highway-animation
# or the edit response
deployment.apps/highway-animation edited
```

The cluster will begin creating the additional pods:

```bash theme={null}
kubectl -n highway-animation get pods
```

Example output while scaling up:

```bash theme={null}
NAME                                      READY   STATUS              RESTARTS   AGE
highway-animation-56456787df-fks89        0/1     Pending             0          2s
highway-animation-56456787df-flqxp        0/1     ContainerCreating   0          3s
highway-animation-56456787df-h69n7        1/1     Running             0        118s
highway-animation-56456787df-wfh6d        0/1     Pending             0          3s
highway-animation-56456787df-zspp8        0/1     Pending             0          3s
highway-animation-7fd646d45c-j29tb        0/1     Pending             0          2s
highway-animation-7fd646d45c-q9sss        0/1     Pending             0          2s
```

Because the live Deployment now has replicas: 5 but Git defines replicas: 1, Argo CD detects drift and marks the application OutOfSync. Argo CD shows the live and desired values for the resource and highlights the difference.

## Reconcile by syncing from Git

To restore the cluster to the Git-defined desired state, click Synchronize in the Argo CD UI. Argo CD will fetch manifests from Git and apply them to the cluster — scaling the Deployment back to 1 replica and updating POD\_COUNT back to "1". Extra pods created by the manual edit will be terminated.

After a successful sync, the resource tree displays resources as Synced and Healthy:

<Frame>
  <img alt="A screenshot of the Argo CD web UI for the &#x22;highway-animation&#x22; application showing App Health as Healthy and Sync status as Synced. The main area displays a resource tree diagram with service, deployment, replica sets and multiple pods, with a left sidebar for filters." />
</Frame>

You can observe pods terminating while reconciliation proceeds:

```bash theme={null}
kubectl -n highway-animation get pods
```

Example output during sync:

```bash theme={null}
NAME                                    READY   STATUS      RESTARTS   AGE
highway-animation-56456787df-n9gf2      1/1     Running     0          20s
highway-animation-7fd646d45c-2tmg6      1/1     Terminating 0          75s
highway-animation-7fd646d45c-j29tb      1/1     Terminating 0          110s
highway-animation-7fd646d45c-p5c5x      1/1     Terminating 0          105s
highway-animation-7fd646d45c-qgsss      1/1     Terminating 0          110s
highway-animation-7fd646d45c-rwqff      1/1     Terminating 0          81s
```

Once the sync completes, only the single pod defined in Git remains and the Argo CD application reports Synced and Healthy.

## Quick reference — kubectl commands used

| Command                                  | Purpose                                                | Example output                                   |
| ---------------------------------------- | ------------------------------------------------------ | ------------------------------------------------ |
| kubectl get ns                           | Verify namespaces                                      | Shows highway-animation namespace                |
| kubectl -n highway-animation get all     | List resources created by the app                      | Pods, Services, Deployments, ReplicaSets         |
| kubectl edit deployment \<name> -n \<ns> | Edit a live resource (creates drift if managed by Git) | deployment.apps/\<name> edited                   |
| kubectl -n highway-animation get pods    | Watch pod creation/termination during scaling or sync  | Pod status lines (Running, Pending, Terminating) |

## Further reading

* [Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/)
* [Kubernetes kubectl reference](https://kubernetes.io/docs/reference/kubectl/)

> **lightbulb** Argo CD treats Git as the source of truth. Manual edits to live cluster resources cause drift (OutOfSync). To make a permanent change, update the manifests in the Git repository and then let Argo CD apply those changes (or use Argo CD’s UI to sync Git into the cluster). Avoid modifying cluster-managed resources directly unless you intentionally want to bypass Git.

That's all for this demo.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/53ee1ade-ac10-4b85-b8a0-a15f874bc19c)


# Demo Multi Cluster Application Deployment

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Multi-Cluster-Application-Deployment/page

How to register remote Kubernetes clusters with Argo CD and deploy applications to them, including adding clusters, creating applications, and verifying deployments.

This guide shows how to register a remote Kubernetes cluster with Argo CD and deploy an application to that cluster. By default, Argo CD manages resources in the cluster where it is installed (the control plane). To deploy to other clusters you must add them as destinations so Argo CD can authenticate and talk to them.

> **lightbulb** Before you begin:

  * Ensure your local kubeconfig contains contexts for both the Argo CD control cluster and any target clusters (e.g., KinD).
  * Ensure the `argocd` CLI is installed and authenticated against your Argo CD server (`argocd login`).

## 1) Identify the kubeconfig context to add

List your current kubeconfig contexts to identify the context name you will add to Argo CD:

```bash theme={null}
kubectl config get-contexts
CURRENT   NAME                    CLUSTER                 AUTHINFO               NAMESPACE
*         docker-desktop          docker-desktop          docker-desktop
          kind-argo-cluster-1     kind-argo-cluster-1     kind-argo-cluster-1
```

In this example:

* `docker-desktop` is the control cluster where Argo CD runs.
* `kind-argo-cluster-1` is the KinD cluster we will add as a destination.

## 2) Argo CD cluster commands

Use the `argocd cluster` subcommands to manage cluster destinations. Common commands:

| Command                   | Use case                                | Example                                                                       |
| ------------------------- | --------------------------------------- | ----------------------------------------------------------------------------- |
| List clusters             | Show registered clusters                | `argocd cluster list -o json`                                                 |
| Add cluster               | Register a context from your kubeconfig | `argocd cluster add <kubecontext-name>`                                       |
| Get cluster info          | Inspect cluster details                 | `argocd cluster get <cluster-name> -o wide`                                   |
| Remove cluster            | Unregister a cluster                    | `argocd cluster rm <cluster-name>`                                            |
| Update cluster properties | Rename or set properties                | `argocd cluster set <CLUSTER_NAME> --name <new-cluster-name> --namespace '*'` |

> **warning** Running `argocd cluster add` creates a ServiceAccount (commonly `argocd-manager`) on the target cluster with cluster-wide privileges and generates a long-lived token. Only register clusters you trust and for which this level of access is acceptable.

## 3) Add the KinD cluster to Argo CD

Add the KinD context (must exist in your kubeconfig). The CLI will create a ServiceAccount, ClusterRole, ClusterRoleBinding, and a bearer token secret on the target cluster, then register the cluster with Argo CD:

```bash theme={null}
