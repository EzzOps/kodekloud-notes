# Check initial state
kubectl get pods
kubectl get replicaset

# After changes, verify new ReplicaSet and its details
kubectl get replicaset
kubectl describe replicaset new-replica-set

# Determine the image used and check Pod error
kubectl describe pod new-replica-set-7r2qw

# Demonstrate automatic Pod replacement
kubectl delete pod new-replica-set-wkzjh
kubectl get pods

# Create ReplicaSets from YAML and fix errors
kubectl create -f /root/replicaset-definition-1.yaml
kubectl create -f /root/replicaset-definition-2.yaml

# Delete newly created ReplicaSets
kubectl delete rs replicaset-1
kubectl delete rs replicaset-2

# Update the image in the original ReplicaSet
kubectl edit rs new-replica-set

# Delete faulty Pods so new ones are created with the correct image
kubectl delete pod new-replica-set-vpkh8 new-replica-set-tn2mp new-replica-set-7r2qw

# Scale the ReplicaSet upward
kubectl scale rs new-replica-set --replicas=5
kubectl get pods

# Scale the ReplicaSet downward using editing
kubectl edit rs new-replica-set
```

Happy learning and successful Kubernetes management!

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/eae8cedf-d483-471f-8796-49f69baec6cf/lesson/393649a3-9f23-4b61-8571-296e8341d3a5)


# Multi Container Pods

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Multi-Container-Pods/Multi-Container-Pods/page

This article explores the design, functionality, and benefits of using multi-container pods in Kubernetes.

Hello and welcome to this comprehensive lesson on multi-container pods in Kubernetes. My name is Mumshad Mannambeth, and in this guide, we will explore the design, functionality, and benefits of using multi-container pods.

Multi-container pods in Kubernetes allow you to run two or more containers together in a single pod. This approach is essential when containerized services must work closely together, such as pairing a web server with a logging agent. In such cases, the containers share the same lifecycle, network namespace, and storage volumes, ensuring smooth communication and synchronized behavior.

![The image lists course objectives, including core concepts, configuration, multi-container pods, observability, pod design, services and networking, and state persistence, with a focus on "Ambassador."](https://kodekloud.com/kk-media/image/upload/v1752871227/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Multi-Container-Pods/frame_20.jpg)

## Microservices vs. Tightly Coupled Services

Modern application development increasingly favors microservices, where large monolithic applications are broken down into smaller, independent sub-components. This design paradigm allows developers to build, deploy, and scale individual services independently, streamlining both development and maintenance.

![The image shows a diagram with colored dots representing microservices architecture, labeled "MICROSERVICES" at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752871229/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Multi-Container-Pods/frame_50.jpg)

However, there are specific situations when two services must operate side by side. For example, a web server might need a dedicated logging agent running alongside it to capture detailed logs without incorporating supplementary code into the web server container. This setup facilitates independent deployment and scaling while keeping the application code modular.

![The image shows a diagram with a large dark circle labeled "WEB Server" and a smaller orange circle labeled "LOG Agent" on a light background.](https://kodekloud.com/kk-media/image/upload/v1752871230/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Multi-Container-Pods/frame_80.jpg)

## Advantages of Multi-Container Pods

Multi-container pods offer several significant advantages:

* **Shared Lifecycle:** All containers in the pod start and stop simultaneously.
* **Unified Network Namespace:** Containers communicate via localhost without extra configuration.
* **Shared Storage Volumes:** Persistent and shared storage is available between containers.

![The image illustrates a diagram of multi-container pods, highlighting lifecycle, network, and storage components within a pod structure.](https://kodekloud.com/kk-media/image/upload/v1752871232/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Multi-Container-Pods/frame_110.jpg)

> **lightbulb** To create a multi-container pod, simply list multiple container definitions under the `containers` array in your pod specification file.

## Creating a Multi-Container Pod

Below is an example of a basic pod definition with a single container:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
  labels:
    name: simple-webapp
spec:
  containers:
  - name: simple-webapp
    image: simple-webapp
    ports:
    - containerPort: 8080
```

To transform this into a multi-container pod, add another container entry to include, for instance, a log agent container alongside the web server:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
  labels:
    name: simple-webapp
spec:
  containers:
  - name: simple-webapp
    image: simple-webapp
    ports:
    - containerPort: 8080
  - name: log-agent
    image: log-agent
```

## Multi-Container Pod Design Patterns

There are three common patterns for designing multi-container pods:

1. **Sidecar Pattern**
2. **Adapter Pattern**
3. **Ambassador Pattern**

### Sidecar Pattern

The sidecar pattern involves deploying a supplemental container, such as a logging agent, alongside your primary container. This design pattern enables services to extend or enhance the capabilities of the main application without altering its code. It is particularly useful when the application produces logs in various formats across different services.

![The image illustrates the Sidecar design pattern, showing a sidecar component connected to a log server.](https://kodekloud.com/kk-media/image/upload/v1752871233/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Multi-Container-Pods/frame_180.jpg)

### Adapter Pattern

The adapter pattern is useful when you need to standardize data formats. For example, when logs from multiple sources need to be unified before they are processed by a central logging service. Log messages might vary as follows:

```plaintext theme={null}
12-JULY-2018 16:05:49 "GET /index1.html" 200
12/JUL/2018:16:05:49 -0800 "GET /index2.html" 200
GET 1531411549 "/index3.html" 200
```

An adapter container can normalize these formats, ensuring consistency before the logs reach the centralized system.

### Ambassador Pattern

The ambassador pattern is applied when an application needs to communicate with different database environments. For example, the application might require a local database for development, another for testing, and a production database in live deployment. Instead of incorporating logic to handle multiple environments in the application code, an ambassador container acts as a proxy. The application always sends requests to localhost, while the ambassador routes traffic to the appropriate database backend.

![The image illustrates the Ambassador design pattern, showing connections from a central point to Dev, Test, and Prod environments.](https://kodekloud.com/kk-media/image/upload/v1752871234/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Multi-Container-Pods/frame_220.jpg)

Each of these patterns leverages the flexible design of multi-container pods by including multiple containers within a single pod specification.

> **lightbulb** Head over to the coding exercises section to practice configuring multi-container pods. Real-world practice will solidify your understanding of these patterns and their implementation in Kubernetes.

That concludes this lesson on multi-container pods in Kubernetes. Thank you for reading, and see you in the next lesson!

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/c679b7ba-0bdd-4f3d-b4a6-296d299406fe/lesson/7684fc5c-f94f-4d85-b265-ccae5ad22c80)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/c679b7ba-0bdd-4f3d-b4a6-296d299406fe/lesson/516ec23d-b246-4ba3-b3a0-23c8b60c6c8f)
