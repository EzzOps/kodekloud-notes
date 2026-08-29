# Install ArgoCD via Glasskube
~ glasskube install argo-cd
Version not specified. The latest version v2.11.7+1 of argo-cd will be installed.
Would you like to enable automatic updates? (y/N) y

Summary:
* The following packages will be installed in your cluster (minikube):
  1. argo-cd (version v2.11.7+1)
* Automatic updates will be enabled

Continue? (Y/n) Y
✓ argo-cd is now installed in minikube.
```

Glasskube will add ArgoCD into the `argocd` namespace (or the namespace configured by Glasskube). After installation, ArgoCD exposes a web UI that you can open via the Glasskube dashboard.

## Retrieve the initial admin password

ArgoCD generates a one-time admin password at installation. Retrieve it with the `argocd` CLI:

```bash theme={null}
# Get the first-time admin password for ArgoCD (namespace: argocd)
argocd admin initial-password -n argocd
```

Sample output (your password will differ):

```bash theme={null}
YYVqv2RjBXFT7uUY
This password must be only used for first time login. We strongly recommend you update the password using `argocd account update-password`.
```

Log in with username `admin` and the printed initial password. After logging in, immediately update the password:

```bash theme={null}
# Update admin password interactively
argocd account update-password
```

You can also authenticate via the CLI (adjust host/port if you’re using port-forwarding or a custom ingress):

```bash theme={null}
# Example CLI login (adjust host if using port-forwarding or a different host)
argocd login localhost:8080 --username admin --password YYVqv2RjBXFT7uUY
```

<Callout icon="lightbulb">
  For production environments: serve the ArgoCD UI over HTTPS, rotate the default `admin` password immediately, and consider integrating Single Sign-On (SSO) and role-based access controls. Also restrict UI access using network policies or an authenticated ingress.
</Callout>

## Access the ArgoCD dashboard via Glasskube

After installation and authentication, open the ArgoCD entry point from the Glasskube dashboard. In local setups you may need to accept a browser security exception when using HTTP or a self-signed certificate.

<Frame>
  <img alt="The image shows a user interface for a software platform called Glasskube, featuring a grid of Kubernetes-related packages available for installation or opening. There are options like Argo CD, cert-manager, and Kubernetes dashboard." />
</Frame>

<Callout icon="warning">
  If you expose ArgoCD directly (NodePort/LoadBalancer) for testing, ensure you secure the endpoint. Avoid leaving the initial admin password unchanged or exposing the UI without authentication in non-development environments.
</Callout>

## Next steps

* Connect ArgoCD to your application Git repositories and create Application resources (manifests, Helm charts, or Kustomize overlays).
* Configure automated sync and health checks for GitOps-driven rollouts.
* Integrate ArgoCD with observability and alerting systems for deployment monitoring.

Useful references:

* ArgoCD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* ArgoCD CLI reference: [https://argo-cd.readthedocs.io/en/stable/cli\_installation/](https://argo-cd.readthedocs.io/en/stable/cli_installation/)
* Glasskube (installation UI/CLI): check your project's Glasskube documentation or repository for details.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/c3806869-7f9e-4cc2-8dc5-aa10304e3d1c/lesson/674a70d0-051c-4538-9e35-65c8e653b188" />
</CardGroup>


# Database CloudNativePG

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Installation/Database-CloudNativePG/page

Guide to installing and using the CloudNativePG Kubernetes operator to deploy and manage PostgreSQL clusters with StatefulSets, Services, and monitoring via Glasskube.

Welcome back. In this lesson we'll add a managed PostgreSQL database to the cluster using the CloudNativePG operator. CloudNativePG is a Kubernetes operator that simplifies running and operating PostgreSQL clusters on Kubernetes by provisioning StatefulSets, Services, and handling failover and replica management.

<Frame>
  <img alt="The image depicts a diagram of a Single-Node Kubernetes Cluster, highlighting observability, continuous deployment, and database components. It is labeled &#x22;Cluster Scoped&#x22; with icons representing each component." />
</Frame>

Overview: this is the fourth and final cluster-scoped package we install. Key characteristics of this package:

| Property     | Details                |
| ------------ | ---------------------- |
| Scope        | Cluster-scoped package |
| Values       | No value definitions   |
| Entry points | No entry points        |
| Dependencies | No dependencies        |

<Frame>
  <img alt="The image is about a database operator for managing PostgreSQL workloads, highlighting features like &#x22;Cluster scoped,&#x22; &#x22;No value definitions,&#x22; and &#x22;No entry points.&#x22;" />
</Frame>

We install the CloudNativePG operator into the `cnpg-system` namespace. The operator watches Postgres Cluster custom resources and creates StatefulSet-backed PostgreSQL instances and the Service endpoint applications use to connect. The diagram below shows the operator running in a system namespace while a sample application in a different namespace connects to the database cluster.

<Frame>
  <img alt="The image is a diagram illustrating a single-node Kubernetes cluster setup, showing a database with PostgreSQL primary instances in separate namespaces and a development namespace containing an application interacting with the database cluster." />
</Frame>

Create a Postgres cluster by applying a Cluster manifest. The operator will translate this manifest into StatefulSets, PersistentVolumes (via PVCs), Services, and monitoring resources.

Example minimal Cluster manifest (3 instances, 1Gi storage, PodMonitor enabled):

```yaml theme={null}
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: cluster-with-metrics
spec:
  instances: 3
  storage:
    size: 1Gi
  monitoring:
    enablePodMonitor: true
```

You can install CloudNativePG from the Glasskube UI or via the Glasskube CLI. This is the installation screen in Glasskube:

<Frame>
  <img alt="The image shows the Glasskube UI for installing the &#x22;cloudnative-pg&#x22; package, with version selection and installation details." />
</Frame>

Confirm the operator package is available in the Glasskube catalog with `glasskube list`. Sample output showing the `cloudnative-pg` entry:

```bash theme={null}
glasskube list
PACKAGE NAME        NAMESPACE        NAME                             VERSION       AUTO-UPDATE        REPOSITORY         STATUS
ingress-nginx                        glasskube                       Not installed
quickwit                              glasskube                       Not installed

NAME                            VERSION          AUTO-UPDATE        REPOSITORY           STATUS
akri                            -                -                  glasskube            Not installed
argo-cd                         v2.11.7+1       Enabled            glasskube            Ready
caddy-ingress-controller        -                -                  glasskube            Not installed
cert-manager                    -                -                  glasskube            Not installed
cloudnative-pg                  -                -                  glasskube            Not installed
cyclops                         -                -                  glasskube            Not installed
kube-prometheus-stack           v61.6.0+1       -                  glasskube            Ready
kubetail                        v0.6.0+1       Enabled            glasskube            Ready
```

In this walkthrough we enabled automatic updates and installed CloudNativePG from the Glasskube catalog. After installation, the package will appear as installed in the UI.

Before applying the Cluster manifest, switch your kubectl context to the `cnpg-system` namespace so commands default there:

```bash theme={null}
kubectl config set-context --current --namespace=cnpg-system
```

Apply the Cluster manifest using a heredoc to kubectl:

```bash theme={null}
kubectl apply -f - <<EOF
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: cluster-with-metrics
spec:
  instances: 3
  storage:
    size: 1Gi
  monitoring:
    enablePodMonitor: true
EOF
```

Watch the operator and StatefulSet pods initialize. If you have an alias like `kgp` for `kubectl get pods`, you can use that; otherwise run:

```bash theme={null}
kubectl get pods -n cnpg-system
```

Initial sample output while pods initialize (you will see init containers and join phases):

```text theme={null}
NAME                                      READY   STATUS            RESTARTS   AGE
cluster-with-metrics-1-initdb-lgsdq      0/1     Completed         0          23s
cluster-with-metrics-2-join-8dp7k        0/1     Init:0/1          0          5s
cnpg-controller-manager-987494b46-p7hqk  1/1     Running           0          2m6s
```

After a short time, the StatefulSet pods become Ready and the operator controller-manager is running:

```text theme={null}
NAME                                      READY   STATUS    RESTARTS   AGE
cluster-with-metrics-1                    1/1     Running   0          73s
cluster-with-metrics-2                    1/1     Running   0          44s
cluster-with-metrics-3                    1/1     Running   0          25s
cnpg-controller-manager-987494b46-p7hqk  1/1     Running   0          3m2s
```

<Callout icon="lightbulb">
  After the cluster is ready, CloudNativePG creates a Kubernetes Service for client connections and maintains that Service through failover events. Inspect the Service and Endpoints in `cnpg-system` to get host and port information used by applications.
</Callout>

That completes the demo. Practice installing the CloudNativePG operator and creating a Postgres Cluster using the manifest above.

Links and references:

* CloudNativePG documentation: [https://cloudnative-pg.io/](https://cloudnative-pg.io/)
* Kubernetes StatefulSets: [https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
* Glasskube project: [https://github.com/traefik/glasskube](https://github.com/traefik/glasskube) (Glasskube UI/CLI)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/c3806869-7f9e-4cc2-8dc5-aa10304e3d1c/lesson/2f665637-d054-4a1e-815d-1dc8926e9fe6" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/c3806869-7f9e-4cc2-8dc5-aa10304e3d1c/lesson/8cc03408-c700-46e0-b7fd-f4023f25df1d" />
</CardGroup>
