# Demo Implementing Pull Based Deployments

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Principles/Demo-Implementing-Pull-Based-Deployments/page

Implementing pull-based deployments with Argo CD using Git as single source of truth, registering repos, creating applications, and syncing manifests to observe desired versus live state

In this lesson we implement a pull-based deployment pattern using Argo CD and a Git repository as the single source of truth. You will learn how to register a repository, create an Argo CD Application that points to YAML manifests, and understand how Argo CD reports desired vs live state before a sync.

<Frame>
  <img alt="The image shows a dashboard interface of the Argo application with no current applications available. It prompts the user to create a new application and includes options for syncing apps and refreshing the page." />
</Frame>

Where are the manifests?

The Kubernetes manifest files used in this demo live in a Gitea repository (our GitOps source-of-truth). For this walkthrough we reference the YAML files inside the `vanilla` directory — it contains a Deployment and a Service that Argo CD will manage.

Creating the Argo CD Application (UI)

Use the Argo CD web UI to create the application that points to the Git repo and the `vanilla` path:

1. Click "New App".
2. Set a name for the application (we use `highway-animation`).
3. Choose the Argo CD project — `default` is fine for demo purposes. Projects provide scoping and policy controls for applications.
4. For synchronization, choose Manual (you can switch to Automatic later).
5. Enable "Create namespace" during sync so Argo CD will create the `highway-animation` namespace when you sync.
6. Source: provide the Git repository URL and set the path to `vanilla` so Argo CD reads the Deployment and Service manifests from that subdirectory.
7. Destination: select the Kubernetes cluster where Argo CD should deploy. For this demo select the local cluster (Argo CD runs in-cluster) and set the target namespace to `highway-animation`.
8. Save / Create the application.

Note on connecting to local Git services from within containers

When Argo CD runs inside Kubernetes (or Docker Desktop), `localhost` refers to the container or pod network, not your laptop/host. If your Gitea instance is running on the Docker host, Argo CD cannot use `http://localhost:...` to reach it. Use `host.docker.internal` or an address reachable from the cluster.

If the repository cannot be reached you'll see a repository access error while creating the app:

<Frame>
  <img alt="The image shows the user interface of an Argo application setup. There's an error message indicating the inability to create an application due to repository access issues, with options for syncing and source information visible." />
</Frame>

Fixing the repository URL (for example using `host.docker.internal`) and recreating the application allows Argo CD to read the manifests. Because synchronization is set to Manual, the application will initially appear as Missing and OutOfSync until you explicitly sync it:

<Frame>
  <img alt="The image shows the Argo CD interface displaying an application called &#x22;highway-animation&#x22; with a status of &#x22;Missing&#x22; and &#x22;OutOfSync.&#x22; The application details include repository information and options to sync, refresh, or delete." />
</Frame>

Inspecting the discovered resources

Click into the application to view the resources Argo CD discovered under the `vanilla` path. You should see two desired resources: a Deployment and a Service. Argo CD reads the YAML manifests from Git (desired state), but the live resources in the cluster are reported as "Resource not found" until you sync.

Here is the Deployment manifest Argo CD fetched (the desired state pulled from Gitea):

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    argocd.argoproj.io/tracking-id: highway-animation:apps/Deployment:highway-animation/highway-animation
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
          image: sjddhart67/highway-animation:blue
          ports:
            - containerPort: 3000
          env:
            - name: POD_COUNT
              value: "1"
```

This confirms Argo CD successfully connected to Gitea and read the manifest. Because sync is manual, Argo CD will not apply the manifests to the cluster until you click Sync (or change the app to Automatic sync).

> **lightbulb** Because this repository is referenced across multiple demos, add it to Argo CD’s repository settings so it appears as a pre-populated choice when creating new applications.

Registering the Git repository in Argo CD

To avoid retyping or troubleshooting the repo for each application, register the repository in Argo CD Settings:

* Go to Argo CD → Settings → Repositories.
* Click "Connect Repo" and enter the repository URL (choose Git and HTTP/S as appropriate).
* If the repo is public, credentials can be omitted. For private repos provide credentials or an SSH key.
* Click "Connect" to register the repository.

After connecting, the repository appears in the new application form for quick selection.

<Frame>
  <img alt="The image shows the Argo CD interface with the &#x22;Repositories&#x22; settings page open, displaying a connected Git repository with a successful connection status." />
</Frame>

Summary and key points

| Topic                     | Explanation                                             | Action / Example                                         |
| ------------------------- | ------------------------------------------------------- | -------------------------------------------------------- |
| Source-of-truth           | Use a Git repo (Gitea in this demo) for manifests       | Place YAML in `vanilla` directory                        |
| Argo CD sync mode         | Manual vs Automatic controls when resources are applied | We used Manual to observe desired vs live states         |
| Common networking pitfall | Containers cannot reach host `localhost`                | Use `host.docker.internal` or cluster-accessible address |
| Registering repos         | Pre-register Git repos in Argo CD settings              | Settings → Repositories → Connect Repo                   |

Next steps

* Perform a manual sync to apply the Deployment and Service to the cluster and observe Argo CD transitioning resources from Missing → Synced.
* Experiment with Automatic sync mode to see continuous reconciliation.
* Inspect the created namespace and resources with `kubectl` (e.g., `kubectl get all -n highway-animation`).

Links and references

* Argo CD documentation: [https://argo-cd.readthedocs.io/en/stable/](https://argo-cd.readthedocs.io/en/stable/)
* Gitea: [https://gitea.io](https://gitea.io)
* Docker Desktop: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/e7a5e275-5428-4f90-890a-913b4ce18bc2)
