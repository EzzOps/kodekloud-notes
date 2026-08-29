# kubectl get namespaces
NAME                 STATUS   AGE
argocd               Active   16m
default              Active   3h1m
kube-node-lease      Active   3h1m
kube-public          Active   3h1m
kube-system          Active   3h1m
```

## 2. Synchronize the Argo CD application

In the Argo CD web UI, click "Synchronize" for the application. Choose to auto-create the namespace if prompted and synchronize both the Deployment and Service manifests. Argo CD will apply those manifests and report the created ReplicaSet and Service details (such as the NodePort).

<Frame>
  <img alt="The image shows an interface for ArgoCD, displaying the status and details of an application called &#x22;highway-animation,&#x22; which is healthy and synced to the latest commit. A visual workflow represents the deployment process from service to pod." />
</Frame>

You can inspect logs, events, and a summary of the applied YAML from the Argo CD UI.

## 3. Inspect the created Pod manifest (live cluster)

Here is the Pod manifest that was created by the Deployment in the cluster:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: '2025-07-29T08:40:03Z'
  generateName: highway-animation-c5ccdf6b-
  labels:
    app: highway-animation
    pod-template-hash: c5ccdf6b
  name: highway-animation-c5ccdf6b-5pl4d
  namespace: highway-animation
  ownerReferences:
    - apiVersion: apps/v1
      blockOwnerDeletion: true
      controller: true
      kind: ReplicaSet
      name: highway-animation-c5ccdf6b
      uid: 175a22f1-a852-4b16-b992-8bf08f8793a52
  resourceVersion: '15018'
  uid: 57c6c5a5-3497-4104-87c2-26cb35703be2
spec:
  containers:
    - env:
        - name: POD_COUNT
          value: '1'
      image: siddharth67/highway-animation:blue
      imagePullPolicy: IfNotPresent
      name: highway-animation
      ports:
        - containerPort: 3000
          protocol: TCP
      resources: {}
      terminationMessagePath: /dev/termination-log
      terminationMessagePolicy: File
```

## 4. Confirm the new namespace and resources

After synchronization, the `highway-animation` namespace should exist:

```bash theme={null}
# kubectl get namespaces
NAME                  STATUS   AGE
argocd                Active   17m
default               Active   3h2m
highway-animation     Active   35s
kube-node-lease       Active   3h2m
kube-public           Active   3h2m
kube-system           Active   3h2m
```

List all resources in the `highway-animation` namespace:

```bash theme={null}
# kubectl -n highway-animation get all
NAME                                      READY   STATUS    RESTARTS   AGE
pod/highway-animation-c5ccdf6b-5pl4d     1/1     Running   0          47s

NAME                                  TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)            AGE
service/highway-animation-service     NodePort   10.100.200.170   <none>        3000:32000/TCP     47s

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/highway-animation     1/1     1            1           47s

NAME                                      DESIRED   CURRENT   READY   AGE
replicaSet.apps/highway-animation-c5ccdf6b   1         1         1       47s
```

The app is reachable via the NodePort (e.g., `http://localhost:32000`) and will render the highway animation. With the Deployment set to 1 replica, you will see one vehicle.

## 5. Create drift: manually scale the Deployment in-cluster

In a non-GitOps workflow, an operator might directly edit the Deployment in the cluster to increase replicas:

```bash theme={null}
# kubectl -n highway-animation edit deployment highway-animation
```

Make these edits in the live Deployment manifest:

* Change `replicas: 1` to `replicas: 5`
* Update the container environment variable `POD_COUNT` value from `'1'` to `'5'`

After saving, Kubernetes will create 4 additional pods and the app will show five vehicles.

Important: This manual change modifies the live cluster state but does not update the Git repository. That causes the live state to diverge from the desired state declared in Git.

## 6. Example: live (cluster) Deployment after manual edit

Live (cluster) Deployment snippet showing the manual change:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  generation: 2
  name: highway-animation
  namespace: highway-animation
spec:
  progressDeadlineSeconds: 600
  replicas: 5
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: highway-animation
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
  template:
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:blue
          env:
            - name: POD_COUNT
              value: '5'
```

## 7. Desired (Git) Deployment in the repository

The desired manifest stored in Git still declares 1 replica:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
  namespace: highway-animation
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: highway-animation
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
  template:
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:blue
          env:
            - name: POD_COUNT
              value: '1'
```

Because the live cluster has 5 replicas while Git declares 1, Argo CD will detect a difference and mark the application OutOfSync. In the Argo CD UI you can click "Diff" to view the highlighted mismatches between the live and desired manifests.

## 8. Reconcile back to Git (manual sync)

To restore the cluster to the Git-declared desired state, click "Synchronize" in Argo CD. Argo CD will reconcile the resources and update the live cluster to match the manifests in the repository. In this scenario it will update the Deployment (not the Service) to revert the replica count back to 1.

<Frame>
  <img alt="The image shows an Argo CD dashboard displaying the status and configuration of a Kubernetes application named &#x22;highway-animation,&#x22; indicating a healthy sync status with a visual representation of its components and pods." />
</Frame>

After synchronization, Argo CD will revert the cluster to the Git desired state and the application will again show a single pod/vehicle.

## Quick reference: kubectl & Argo CD actions

| Action                      |                                               Command or UI step | Purpose                               |
| --------------------------- | ---------------------------------------------------------------: | ------------------------------------- |
| List namespaces             |                                         `kubectl get namespaces` | Verify cluster namespaces             |
| List resources in namespace |                           `kubectl -n highway-animation get all` | Inspect deployed resources            |
| Edit a live Deployment      | `kubectl -n highway-animation edit deployment highway-animation` | Make ad-hoc changes (not recommended) |
| Sync app in Argo CD         |                          Argo CD UI → Select app → "Synchronize" | Apply Git manifests to cluster        |
| View diff in Argo CD        |                                 Argo CD UI → Select app → "Diff" | Compare live vs. desired manifests    |

## Best practice

<Callout icon="lightbulb">
  Never make long-lived configuration changes directly in the cluster. Always update the Git repository with the desired state and let your GitOps operator (Argo CD) reconcile the cluster. This ensures a single source of truth, prevents configuration drift, and makes rollbacks and audits straightforward.
</Callout>

## Links and references

* Argo CD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Kubernetes: Deployments — [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* GitOps principles: [https://www.weave.works/technologies/gitops/](https://www.weave.works/technologies/gitops/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/7a01b8bf-971f-452e-8e36-bac6b22a1676" />
</CardGroup>


# GitOps Principles

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Principles/GitOps-Principles/page

Overview of GitOps principles for managing cloud-native systems using declarative configuration, Git as source of truth, automated operators, and continuous reconciliation for reproducible, auditable, self-healing deployments

GitOps is an operational paradigm that applies software engineering practices—like version control, CI/CD, and declarative configuration—to infrastructure and application delivery. Below we break down the four core GitOps principles, why they matter, and how they work in practice.

GitOps is built on four fundamental principles that make it a robust, reproducible, and auditable methodology for operating cloud-native systems.

## 1) Declarative desired state

The first principle requires that your entire system—both infrastructure and application configuration—be defined declaratively. In practice this means storing *what* the final state should be, not *how* to achieve it.

Declarative manifests (for example, Kubernetes YAML or Helm charts) express the intended state in a machine-readable format. This differs from imperative operations (one-off CLI commands or ad-hoc scripts), which do not capture the resulting state and are harder to reproduce, audit, or recover.

<Callout icon="lightbulb">
  Declare the desired state so the system can be inspected, versioned, and reconciled automatically.
</Callout>

Benefits of using a declarative approach:

* Versioning and diffability of configuration
* Easier peer review (PRs for desired-state changes)
* Deterministic rollouts and rollbacks

## 2) Use Git as the single source of truth

Store all desired-state definitions in Git. Git gives you an immutable, versioned history and an auditable record of changes, making it the natural single source of truth for your system configuration.

Using Git enables:

* Clear change history and accountability
* Reproducible rollbacks by reverting commits
* Policy and security enforcement via code review workflows (pull requests)

Common GitOps workflows:

* PR-based change proposals with automated validation
* Branch-per-environment or directory-per-cluster organization
* Git hooks and CI to run tests and linters against manifests

## 3) Apply changes automatically

With desired state stored in Git, software agents (GitOps operators) should automatically apply those changes to your environments. Operators continuously watch Git repositories and sync the declared manifests to the runtime environment (for example, Kubernetes clusters).

A typical declarative manifest stored in Git:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.21.6
          ports:
            - containerPort: 80
```

Popular GitOps operators include Argo CD and Flux. An operator:

* Continuously pulls manifests from Git
* Applies the manifests to one or more clusters
* Can manage multiple clusters from the same repository structure

## 4) Continuous reconciliation (self-healing)

Continuous reconciliation is the observe → diff → act loop that keeps the actual state aligned with the desired state:

* Observe: The operator watches both the Git repository (desired state) and the live system (actual state).
* Diff: It computes differences between desired and actual states.
* Act: If drift is detected, the operator takes corrective actions to bring the system back into alignment.

This loop provides:

* Automated self-healing of configuration drift
* Faster recovery from human or system errors
* Consistent environments across development, staging, and production

## Summary table

| Principle                     | Why it matters                                      | Example                                     |
| ----------------------------- | --------------------------------------------------- | ------------------------------------------- |
| Declarative desired state     | Enables versioning, inspection, and reproducibility | `Kubernetes` manifests or `Helm` charts     |
| Git as single source of truth | Auditability, history, and rollback capability      | `git` repo with PR-based workflow           |
| Apply changes automatically   | Consistent, automated deployments                   | `Argo CD` or `Flux` syncing repo to cluster |
| Continuous reconciliation     | Self-healing, drift detection and correction        | Operator observe → diff → act loop          |

Putting it together, these four principles—declarative manifests, Git as the source of truth, automated application via operators, and continuous reconciliation—form the foundation of GitOps and make it a powerful pattern for managing modern infrastructure and applications.

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Argo CD](https://argo-cd.readthedocs.io/)
* [Flux CD](https://fluxcd.io/)
* [Git Documentation](https://git-scm.com/doc)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/14fc5de9-15a6-432c-b715-3bb1f0c52817" />
</CardGroup>
