# Running the application on the local k8s cluster

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Building-and-containerizing-sample-application/Running-the-application-on-the-local-k8s-cluster/page

This guide explains how to deploy an ASP.NET Core Web App on a local Kubernetes cluster using Docker images and `kubectl`.

Deploying an ASP.NET Core Web App with Docker images to a Kubernetes environment involves creating deployments, exposing services, and scaling replicas. This guide walks you through running your app on a **local** Kubernetes cluster using `kubectl`.

## Table of Contents

1. [Verify Kubernetes Version](#1-verify-kubernetes-version)
2. [Create a Deployment](#2-create-a-deployment)
3. [Expose the Deployment as a Service](#3-expose-the-deployment-as-a-service)
4. [Display the Machine Name in the Web App](#4-display-the-machine-name-in-the-web-app)
5. [Build and Tag a New Docker Image](#5-build-and-tag-a-new-docker-image)
6. [Redeploy Using Version 2](#6-redeploy-using-version-2)
7. [Test the Load Balancer](#7-test-the-load-balancer)
8. [Command Reference Table](#8-command-reference-table)
9. [Links and References](#9-links-and-references)

***

## 1. Verify Kubernetes Version

Before deploying, confirm the `kubectl` client and the local cluster version:

```bash theme={null}
kubectl version --short
```

Sample output:

```bash theme={null}
Flag --short has been deprecated, and will be removed in the future. The --short output will become the default.
Client Version: v1.25.4
Kustomize Version: v4.5.7
Server Version: v1.25.4
```

> **lightbulb** Keeping your `kubectl` client in sync with the server helps avoid compatibility issues.

***

## 2. Create a Deployment

Create a Deployment named `kodekloudapp` using the `kodekloudapp:v1` image with **2 replicas**:

```bash theme={null}
kubectl create deployment kodekloudapp \
  --image=kodekloudapp:v1 \
  --replicas=2
```

Verify:

```bash theme={null}
kubectl get deployment kodekloudapp
```

Expected output:

```bash theme={null}
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
kodekloudapp    2/2     2            2           10s
```

***

## 3. Expose the Deployment as a Service

Expose the Deployment on port **8080** (host) → **80** (container). On a local cluster this defaults to a `NodePort` service, but in cloud environments it provisions a load balancer.

```bash theme={null}
kubectl expose deployment kodekloudapp \
  --type=LoadBalancer \
  --port=8080 \
  --target-port=80
```

Check the Service:

```bash theme={null}
kubectl get service kodekloudapp
```

Sample output:

```bash theme={null}
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
kodekloudapp    LoadBalancer   10.106.40.151   localhost     8080:31032/TCP  30s
```

Open your browser at [http://localhost:8080](http://localhost:8080) to see the running app.

> **triangle-alert** On local clusters, `LoadBalancer` maps to a `NodePort`. When you move to [AKS](https://azure.microsoft.com/services/kubernetes-service/), this will create a cloud load balancer.

***

## 4. Display the Machine Name in the Web App

To confirm traffic distribution across replicas, update the Razor page to display the machine name.

Edit **Pages/Index.cshtml**:

```html theme={null}
@page
@model IndexModel

@{
    ViewData["Title"] = "Home page";
}

<div class="text-center">
    <h1 class="display-4">Welcome</h1>
    <p>Learn about <a href="https://docs.microsoft.com/aspnet/core">building Web apps with ASP.NET Core</a>.</p>
    <p>Message: @Model.Message</p>
    <p>Machine: @Environment.MachineName</p>
</div>
```

Save changes and restart the app locally to confirm the additional line appears.

***

## 5. Build and Tag a New Docker Image

After updating the code, build a new image tagged `kodekloudapp:v2`:

```bash theme={null}
cd .\RiderProjects\KodeKloudApp\
docker build -t kodekloudapp:v2 .
```

List your local images:

```bash theme={null}
docker image ls
```

You should see both `v1` and `v2` tags:

```bash theme={null}
REPOSITORY      TAG  IMAGE ID       CREATED
kodekloudapp    v2   3693d7352914   7 seconds ago
kodekloudapp    v1   8177c6374c5c   42 minutes ago
```

***

## 6. Redeploy Using Version 2

First, clean up existing resources:

```bash theme={null}
kubectl delete service kodekloudapp
kubectl delete deployment kodekloudapp
```

Recreate the Deployment with the **v2** image:

```bash theme={null}
kubectl create deployment kodekloudapp \
  --image=kodekloudapp:v2 \
  --replicas=2
```

Expose it again:

```bash theme={null}
kubectl expose deployment kodekloudapp \
  --type=LoadBalancer \
  --port=8080 \
  --target-port=80
```

Verify:

```bash theme={null}
kubectl get service kodekloudapp
```

***

## 7. Test the Load Balancer

Visit [http://localhost:8080](http://localhost:8080) in two different browser sessions. You’ll see the **Machine** field alternate between replica hosts, confirming load balancing across pods.

***

## 8. Command Reference Table

| Command                                                                 | Purpose                                |
| ----------------------------------------------------------------------- | -------------------------------------- |
| `kubectl version --short`                                               | Check client/server versions           |
| `kubectl create deployment ... --replicas=2`                            | Deploy the application with 2 replicas |
| `kubectl get deployment`                                                | Verify Deployment status               |
| `kubectl expose deployment ... --type=LoadBalancer`                     | Expose Deployment as a Service         |
| `kubectl get service`                                                   | List Services and their endpoints      |
| `kubectl delete service <name>`<br />`kubectl delete deployment <name>` | Clean up resources before redeployment |

***

## 9. Links and References

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* [ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core)
* [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/services/kubernetes-service/)

- [Watch Video](https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/20789863-851c-44c5-a251-8cb7f78f60b5/lesson/692c885b-b6db-483d-a845-de94794e4431)
