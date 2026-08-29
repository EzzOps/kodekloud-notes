# Demo Pods

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Kubernetes-Resources/Demo-Pods/page

This tutorial teaches how to deploy a pod in a Minikube cluster using the kubectl command-line tool.

In this tutorial, you'll learn how to deploy a pod in your Minikube cluster. A pod is the smallest and simplest deployable unit in Kubernetes, designed to hold one or more application containers. We'll use the `kubectl` command-line tool to interact with our cluster.

> **lightbulb** You can specify an image tag or use an alternative container registry if your desired image is hosted elsewhere.

## Pod Operations

### Creating a Pod

To create a pod named "nginx" using the Docker image "nginx" (pulled from Docker Hub), run the following command:

```bash theme={null}
kubectl run nginx --image=nginx
```

Once this command executes, Kubernetes creates the pod. You can verify its creation and status by checking the list of pods:

```bash theme={null}
