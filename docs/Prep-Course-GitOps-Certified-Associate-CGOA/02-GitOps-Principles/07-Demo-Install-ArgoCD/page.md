# Demo Install ArgoCD

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Principles/Demo-Install-ArgoCD/page

Guide to install Argo CD on Kubernetes, expose the server for browser access using NodePort for demos, and obtain the initial admin password

In this walkthrough you'll install Argo CD into a Kubernetes cluster, expose its server so the UI is reachable from a browser, and retrieve the initial admin credentials. The steps show how to install a specific Argo CD release (not necessarily the latest) and how to quickly test the UI using a `NodePort` exposure for demos.

1. Create the argocd namespace and install Argo CD

* The Argo CD Getting Started docs show installing the latest release, but you can install a specific version by referencing the Git tag in the manifest URL.

| Install type             | Command                                                                                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Non-HA (single-instance) | `bash kubectl create namespace argocd kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.0.5/manifests/install.yaml `    |
| HA (high-availability)   | `bash kubectl create namespace argocd kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.0.5/manifests/ha/install.yaml ` |

2. Verify cluster connectivity and namespaces

* Confirm your kubeconfig is working and list nodes and namespaces:

```bash theme={null}
kubectl get nodes
kubectl get ns
```

3. Review the install output

* Applying the manifest creates many Kubernetes resources (ConfigMaps, Secrets, Services, Deployments, StatefulSets, NetworkPolicies, RBAC objects, CRDs, etc.). Typical console output after applying the install manifest:

```text theme={null}
configmap/argocd-rbac-cm created
secret/argocd-initial-admin-secret created
service/argocd-server created
deployment.apps/argocd-server created
statefulset.apps/argocd-application-controller created
networkpolicy.networking.k8s.io/argocd-server-network-policy created
rolebinding.rbac.authorization.k8s.io/argocd-server created
clusterrolebinding.rbac.authorization.k8s.io/argocd-application-controller created
```

* For a quick reference, common resource types created are:

| Resource Type            | Purpose                                                    |
| ------------------------ | ---------------------------------------------------------- |
| ConfigMap / Secret       | Configuration and credentials (e.g., initial admin secret) |
| Service                  | Network access (argocd-server, repo-server, etc.)          |
| Deployment / StatefulSet | Application controller, repo server, server                |
| NetworkPolicy            | Restrict network traffic to Argo CD components             |
| RBAC                     | Roles and rolebindings for Argo CD controllers             |

4. Check Argo CD pods and services

* Give Kubernetes a minute, then list pod, service, and deployment resources in the `argocd` namespace:

```bash theme={null}
kubectl -n argocd get pods,svc,deployments
```

Sample output (representative):

```text theme={null}
NAME                                       READY   STATUS    RESTARTS   AGE
pod/argocd-application-controller-0        1/1     Running   0          2m
pod/argocd-repo-server-xxxxxx              1/1     Running   0          2m
pod/argocd-server-xxxxx                    1/1     Running   0          2m

NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
service/argocd-server        ClusterIP   10.106.172.73   <none>        80/TCP,443/TCP
service/argocd-repo-server   ClusterIP   10.104.191.94   <none>        8081/TCP,8084/TCP
```

5. Expose the argocd-server Service via NodePort (for browser access)

* For a quick demo from your workstation, change the `argocd-server` Service type from `ClusterIP` to `NodePort`:

```bash theme={null}
kubectl -n argocd edit svc argocd-server
