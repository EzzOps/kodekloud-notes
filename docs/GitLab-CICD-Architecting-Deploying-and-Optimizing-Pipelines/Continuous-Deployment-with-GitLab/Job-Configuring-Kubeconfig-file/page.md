# Pods, Services, Deployments
pod/nginx-deploy-d845cc945-hnj2v          1/1 Running   0        8m
service/nginx-deploy                     ClusterIP    10.96.14.252   80/TCP    8m
deployment.apps/nginx-deploy             1/1          1              8m

# Ingress
nginx-demo   <none>   nginx-default.34.82.207.123.nip.io   34.82.207.123   80,443   7m
```

Copy the Ingress host into your browser. You may encounter a security warning due to a self-signed certificate:

<Callout icon="triangle-alert">
  The default Ingress TLS certificate is self-signed. Browsers will warn before displaying the NGINX welcome page.
</Callout>

<Frame>
  ![The image shows a browser displaying the default "Welcome to nginx!" page, indicating that the nginx web server is successfully installed and running.](https://kodekloud.com/kk-media/image/upload/v1752877198/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Kubernetes-Cluster/nginx-welcome-page-browser-display.jpg)
</Frame>

This confirms external traffic is routed correctly.

## Configuring kubectl and kubeconfig for CI/CD

To automate deployments in GitLab CI, ensure `kubectl` is installed and authenticated via kubeconfig.

Check client and server versions:

```bash theme={null}
kubectl version --short
```

```bash theme={null}
Client Version: v1.29.1
Server Version: v1.29.0-gke.1381000
```

View the active kubeconfig context:

```bash theme={null}
kubectl config view --minify
```

```yaml theme={null}
apiVersion: v1
clusters:
- cluster:
    server: https://35.230.61.213
    certificate-authority-data: DATA+OMITTED
  name: gke_clgcporg8-090_us-west1-a_cluster-1
contexts:
- context:
    cluster: gke_clgcporg8-090_us-west1-a_cluster-1
    namespace: kube-system
    user: gitlab-cluster-admin
  name: gke_clgcporg8-090_us-west1-a_cluster-1
users:
- name: gitlab-cluster-admin
  user:
    token: REDACTED
```

A dedicated user or service account (e.g., `gitlab-cluster-admin`) should authenticate your GitLab CI jobs.

## Creating Namespaces for Environments

Instead of separate clusters, use dedicated namespaces to isolate **development** and **staging** workloads:

```bash theme={null}
k create namespace development
k create namespace staging
```

```bash theme={null}
namespace/development created
namespace/staging created
```

Verify all namespaces:

```bash theme={null}
k get namespaces
```

```bash theme={null}
NAME                  STATUS   AGE
default               Active   30m
development           Active   1m
staging               Active   1m
ingress-nginx         Active   25m
kube-system           Active   30m
```

Your cluster is now prepared for GitLab CI pipelines targeting **development** and **staging**.

## Kubernetes CLI Command Reference

| Command                            | Description                          |
| ---------------------------------- | ------------------------------------ |
| `kubectl get nodes`                | List all cluster nodes               |
| `kubectl get namespaces`           | Show active namespaces               |
| `kubectl -n ingress-nginx get all` | Inspect Ingress Controller resources |
| `kubectl get ingress`              | Display all Ingress resources        |
| `kubectl config view --minify`     | Show current kubeconfig context      |
| `kubectl create namespace <name>`  | Create a new namespace               |

## Links and References

* [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
* [Kubernetes Ingress NGINX Controller](https://kubernetes.github.io/ingress-nginx/)
* [kubectl CLI Reference](https://kubernetes.io/docs/reference/kubectl/)
* [GitLab CI/CD Pipeline Configuration](https://docs.gitlab.com/ee/ci/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/54935e20-2ab8-4fbd-bd5d-93fb2e90894d" />
</CardGroup>


# Job Configuring Kubeconfig file

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Deployment-with-GitLab/Job-Configuring-Kubeconfig-file/page

This guide explains how to inject a Kubernetes kubeconfig into a GitLab CI pipeline for kubectl authentication and cluster interaction.

In this guide, you’ll learn how to inject your Kubernetes `kubeconfig` into a GitLab CI pipeline so that `kubectl` can authenticate and interact with your cluster. This setup is essential for automated deployments, health checks, and infrastructure management within your CI/CD workflows.

## Why You Need to Provide a Kubeconfig

When `kubectl` runs without a valid `kubeconfig`, it can only display client information and will fail to contact the API server:

```yaml theme={null}
