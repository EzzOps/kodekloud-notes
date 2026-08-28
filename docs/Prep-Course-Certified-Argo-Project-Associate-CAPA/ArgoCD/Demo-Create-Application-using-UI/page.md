# Non-HA
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.1.5/manifests/install.yaml

# High-Availability
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.1.5/manifests/ha/install.yaml
```

<Callout icon="lightbulb">
  Choose the non-HA manifest for single-node or local clusters (quickstart). Use
  the HA manifest for production-grade deployments that require multiple
  replicas and higher availability.
</Callout>

## Example environment and initial cluster state

This example uses a single-node Docker Desktop cluster (Kubernetes v1.34.1). Use these commands to inspect nodes and namespaces before installing Argo CD:

```bash theme={null}
# Node
kubectl get nodes
# NAME             STATUS   ROLES         AGE   VERSION
# Namespaces (before install)
kubectl get ns
# NAME               STATUS   AGE
# default            Active   11h
# kube-node-lease    Active   11h
# kube-public        Active   11h
# kube-system        Active   11h
```

## Install Argo CD (example using v3.1.5 non-HA)

Create the namespace and apply the manifest for the specific version:

```bash theme={null}
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.1.5/manifests/install.yaml
```

The install manifest creates many Kubernetes resources—CRDs, ServiceAccounts, RBAC, ConfigMaps, Secrets, Services, Deployments, StatefulSets, and NetworkPolicies. Example creation output (shortened):

```bash theme={null}
# Selected created resources (example)
namespace/argocd created
customresourcedefinition.apiextensions.k8s.io/applications.argoproj.io created
serviceaccount/argocd-application-controller created
service/argocd-server created
deployment.apps/argocd-server created
statefulset.apps/argocd-application-controller created
# ...many other resources created...
```

### Common resource types created by the Argo CD install

| Resource Type            | Use Case                                                          |
| ------------------------ | ----------------------------------------------------------------- |
| Namespace                | Isolate Argo CD components (`argocd`)                             |
| CRDs                     | Define Argo CD custom resources (Applications, AppProjects, etc.) |
| Deployments/StatefulSets | Run controllers, server, repo-server, etc.                        |
| Services                 | Expose Argo CD components (ClusterIP by default)                  |
| Secrets                  | Store initial admin password and other credentials                |
| RBAC (Roles/Bindings)    | Grant permissions to Argo CD components                           |

## Verify pods and services

Watch the resources in the `argocd` namespace as pods start:

```bash theme={null}
kubectl -n argocd get all
# Example (pods may be initializing)
# NAME                                              READY   STATUS              RESTARTS   AGE
# pod/argocd-application-controller-0               0/1     ContainerCreating   0          20s
# pod/argocd-server-xxxxx                           0/1     ContainerCreating   0          23s
# ...
```

When controllers finish starting, the Deployments and StatefulSets should show READY:

```bash theme={null}
kubectl -n argocd get deploy,statefulset
# Example final state:
# deployment.apps/argocd-server                                   1/1     1   1  7m
# statefulset.apps/argocd-application-controller                  1/1     1   1  6m
```

## Expose the Argo CD server for local access (NodePort)

By default, the `argocd-server` Service is type `ClusterIP`. For local development you can patch it to `NodePort`:

```bash theme={null}
kubectl -n argocd patch svc argocd-server -p '{"spec": {"type": "NodePort"}}'
# service/argocd-server patched
```

List services to see the assigned NodePorts (example output):

```bash theme={null}
kubectl -n argocd get svc
# NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)
# argocd-server        NodePort    10.101.182.0     <none>        80:31148/TCP,443:30203/TCP
# argocd-repo-server   ClusterIP   10.107.211.176   <none>        8081/TCP,8084/TCP
# ...
```

How to determine the URL to open:

* If the PORT(S) column shows "80:31148/TCP,443:30203/TCP", use [https://localhost:30203](https://localhost:30203) (HTTPS NodePort mapped to 443).
* If you use the NodePort mapped to port 80, you can use `http://localhost:<nodeport>`.
* On Docker Desktop NodePorts are typically reachable at localhost; on other environments use the node IP or cloud load balancer as appropriate.

Note: Browsers may show a certificate warning for the self-signed certificate. Accept the warning to proceed to the Argo CD UI.

<Frame>
  <img
    alt="A Chrome browser error page showing &#x22;Your connection is not private&#x22; for
https://localhost:31148 with a red triangle exclamation icon. It displays
NET::ERR_CERT_AUTHORITY_INVALID and options like &#x22;Advanced&#x22; and &#x22;Back to
safety.&#x22;"
  />
</Frame>

## Retrieve the initial admin password and log in

Argo CD stores the initial admin password in the `argocd-initial-admin-secret` Secret. Decode it with:

```bash theme={null}
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 --decode
# prints the initial admin password
```

<Callout icon="lightbulb">
  On macOS the base64 CLI flag may differ—if `--decode` doesn't work try `base64
      -D`.
</Callout>

If your installation uses a different secret name or structure, list secrets and inspect the relevant secret:

```bash theme={null}
kubectl -n argocd get secrets
kubectl -n argocd describe secret <secret-name>
```

Use username `admin` and the decoded password to sign in to the Argo CD web UI. The default login screen looks like this:

<Frame>
  <img
    alt="A web app login screen for Argo with a purple starry background, the text
&#x22;Let's get stuff deployed!&#x22; and a smiling orange octopus/alien mascot standing
on a gear. On the right is a white login panel with the Argo logo and
username/password fields (username &#x22;admin&#x22;
entered)."
  />
</Frame>

## Update the admin password

After your first login, immediately change the admin password from the Account Settings -> Update account password dialog. Updating the default password is strongly recommended to secure your Argo CD instance.

<Frame>
  <img
    alt="A screenshot of a web app &#x22;Update account password&#x22; page showing masked
fields for Current Password, New Password, and Confirm New Password with &#x22;SAVE
NEW PASSWORD&#x22; and &#x22;CANCEL&#x22; buttons. The app branding reads &#x22;argo&#x22; and there's
a dark navigation sidebar on the
left."
  />
</Frame>

## Summary

* Installed Argo CD into the `argocd` namespace (stable or specific version).
* Patched `argocd-server` to NodePort for local access.
* Retrieved and decoded the initial admin password from the Kubernetes Secret.
* Logged into the Argo CD web UI and updated the admin password.
* Next steps: create Argo CD Applications, connect Git repositories, and add clusters for GitOps-based deployments.

## Links and References

* [Argo CD Documentation](https://argo-cd.readthedocs.io/)
* [Argo Project GitHub Release Manifests](https://github.com/argoproj/argo-cd/tree/stable/manifests)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/aa65f38b-6b37-4190-a77c-6c724123305f" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/9facbd04-7a3f-4200-9d6e-53936e93d875/lesson/37230076-2c41-4e48-b0ce-314db9042398" />
</CardGroup>


# Demo Create Application using UI

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Create-Application-using-UI/page

Create and deploy an Argo CD Application via the web UI to sync Kubernetes manifests from a Git repo, including namespace creation and manual sync.

In this lesson we'll create an Argo CD Application using the Argo CD web UI and deploy a small example app from a Git repository.

What you'll learn:

* How to point Argo CD at a repository and path containing Kubernetes manifests
* How to configure the Application (project, destination, sync policy)
* How Argo CD reports OutOfSync resources and how to perform a manual sync

## Repository overview

For this demo we use a self-hosted Git server with organization `kk-org` and repo `capa-demos`. The manifests to deploy live in the `vanilla` folder and include two resources: a Deployment and a NodePort Service.

Deployment (deploys the app image, exposes port 3000, sets POD\_COUNT env var, single replica, namespace `highway-animation`):

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

Service (NodePort exposing container port 3000 via nodePort 32000):

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: highway-animation-service
  namespace: highway-animation
spec:
  selector:
    app: highway-animation
  ports:
  - protocol: TCP
    port: 3000
    targetPort: 3000
    nodePort: 32000
  type: NodePort
```

Summary of resources:

| Resource Type | Purpose                               | Location (repo path)       |
| ------------- | ------------------------------------- | -------------------------- |
| Deployment    | Runs the web application container    | `./vanilla/deployment.yml` |
| Service       | Exposes application on nodePort 32000 | `./vanilla/service.yml`    |

<Frame>
  <img alt="A dark-themed repository browser (Gitea) showing the kk-org/capa-demos project with the &#x22;vanilla&#x22; folder open, listing deployment.yml and service.yml. The left sidebar shows other folders like jenkins-demo, manifests, patterns and sealed-secrets." />
</Frame>

## Create the Argo CD Application (UI)

Follow these steps in the Argo CD web UI to create the Application:

1. Click "New App" (or "Create Application") in Argo CD.
2. Enter an Application name (for example: `highway-animation`).
3. Project: choose `default` (or another project you have configured).
4. Sync policy: for this demo set to **Manual** (you can enable Automatic sync later).
5. Enable the sync option CreateNamespace so Argo CD will create the `highway-animation` namespace during sync.
6. Destination: select the cluster where Argo CD is installed and set the target namespace to `highway-animation`.
7. Source: set the repository URL and the path to the manifests: `./vanilla`.
8. Click Create to persist the Application resource in the cluster.

Example source fields in the create form:

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing a form to create an application, with fields for Repository URL (http://localhost:50.../kk-org/capa-demos), Revision set to HEAD, and Path set to ./vanilla. The left sidebar shows navigation items like Applications, Settings, User Info, and Documentation." />
</Frame>

<Callout icon="lightbulb">
  If Argo CD is running inside a Kubernetes environment such as Docker Desktop, avoid using `localhost` in the repository URL because `localhost` inside the cluster does not point to your host machine. Use the Docker Desktop host DNS name instead, for example:
  `http://host.docker.internal:5000/kk-org/capa-demos`
</Callout>

When you create the Application with CreateNamespace enabled, Argo CD will create the `highway-animation` namespace at sync time (not when the Application resource is created).

<Frame>
  <img alt="A screenshot of the Argo web UI showing an &#x22;Create&#x22; application form. The Destination section lists Cluster URL &#x22;https://kubernetes.default.svc&#x22; and the Namespace field highlighted as &#x22;highway-animation.&#x22;" />
</Frame>

## Inspect Application status and diffs

After creating the Application, Argo CD reads the repository and compares the manifests to the cluster. Initially the Application will show as OutOfSync and Missing because Argo CD has not applied the resources yet.

You can confirm that the namespace has not been created:

```bash theme={null}
kubectl get namespaces
