# Working with Kubernetes

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Kubernetes/Working-with-Kubernetes/page

This guide covers the fundamentals of Kubernetes, focusing on pods, deployments, and managing multiple clusters within a CI/CD pipeline.

In this guide, you'll learn the fundamentals of working with Kubernetes while integrating it into a CI/CD pipeline alongside [Jenkins](https://learn.kodekloud.com/user/courses/jenkins). Although this article does not cover every detail of Kubernetes, you will gain a solid understanding of core components necessary for effective cluster management.

## Understanding Pods in Kubernetes

In Kubernetes, you deploy applications as pods rather than as individual containers. A pod is an abstraction layer that encapsulates one or more containers that work in unison, making it easier to manage them as a single unit. For instance, if your application requires three instances, you deploy three pods instead of dealing with three separate containers.

Below is an example YAML configuration for creating a pod:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    name: myapp
spec:
  containers:
    - name: myapp
      image: <Image>
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
      ports:
        - containerPort: 5000
```

Key aspects of the YAML file include:

* **Kind**: Specifies that the resource is a Pod.
* **Metadata**: Contains the pod name and labels (key-value pairs used to tag resources).
* **Spec**: Defines the configuration, including the list of containers, each with their name, image (which can be sourced from [Docker Hub](https://hub.docker.com) or private repositories), resource limits, and ports.

To deploy this pod, run the following command using the Kubernetes CLI (`kubectl`):

```bash theme={null}
