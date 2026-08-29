# flightticket.yml
apiVersion: flights.com/v1
kind: FlightTicket
metadata:
  name: my-flight-ticket
spec:
  from: Mumbai
  to: London
  number: 2
```

You can create this resource and verify its status using these commands:

```bash theme={null}
kubectl create -f flightticket.yml
# Output:
kubectl get flightticket
# Output:
# NAME              STATUS
# my-flight-ticket  Pending
```

> **lightbulb** While you can implement controllers in various programming languages, using the Kubernetes Go client is recommended. The Go client (client-go library) provides shared informers that offer efficient caching and queuing mechanisms, making it ideal for building robust controllers.

The same FlightTicket YAML definition provides context for this process:

```yaml theme={null}
# flightticket.yml
apiVersion: flights.com/v1
kind: FlightTicket
metadata:
  name: my-flight-ticket
spec:
  from: Mumbai
  to: London
  number: 2
```

And here are the related creation commands:

```bash theme={null}
kubectl create -f flightticket.yml
# Output:
kubectl get flightticket
# Output:
# NAME              STATUS
# my-flight-ticket  Pending
```

Using Go simplifies the development process due to its seamless integration with Kubernetes libraries that support robust controller patterns.

## Getting Started with a Custom Controller

To build your custom controller, follow these steps:

1. **Clone the SampleController Repository**\
   Clone the repository from GitHub using the following command:

   ```bash theme={null}
   git clone https://github.com/kubernetes/sample-controller.git
   # Cloning into 'sample-controller'...
   # Resolving deltas: 100% (15787/15787), done.
   ```

2. **Customize Your Controller Logic**\
   Navigate to the repository directory and modify the `controller.go` file to include your custom logic, such as invoking the flight booking API:

   ```bash theme={null}
   cd sample-controller
   go build -o sample-controller .
   # Output during build might include:
   # go: downloading k8s.io/client-go v0.0.0-20211001003700-dbfa30b9d908
   # go: downloading golang.org/x/text v0.3.6
   ```

3. **Run the Controller**\
   Execute the controller by specifying the `kubeconfig` file for authentication:

   ```bash theme={null}
   ./sample-controller --kubeconfig=$HOME/.kube/config
   # Example output:
   # I1013 02:11:07.489479   4017 controller.go:115] Setting up event handlers
   # I1013 02:11:07.489701   4017 controller.go:156] Starting FlightTicket controller
   ```

   When executed, the controller runs locally, monitors the creation of FlightTicket objects, and triggers the necessary API calls.

> **lightbulb** After verifying that your controller functions correctly, consider packaging it into a Docker image and deploying it inside your Kubernetes cluster as a pod or deployment. This approach eliminates the need for manual rebuilding and execution each time.

## Overview

This article provides a high-level overview of building a custom controller. Although detailed coding questions about custom controllers are unlikely to appear in certification exams, it is essential to understand concepts such as:

* Custom Resource Definitions (CRDs)
* Managing CRD files
* Working with existing controller patterns

For more in-depth information on Kubernetes resources, refer to the following links:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)

Operators extend these concepts further by automating more complex operational tasks in Kubernetes environments.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/ee404020-8c94-4f3b-a69a-240984b9553e/lesson/991c9c4d-6fb0-4031-8f50-a7c89dd7dfe2)


# Custom Resource Definition

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/Custom-Resource-Definition/page

This article explains how to create and manage Custom Resource Definitions in Kubernetes, using a FlightTicket example to illustrate the process.

In this lesson, we explore how Custom Resource Definitions (CRDs) work in Kubernetes. You will learn how standard Kubernetes resources, such as Deployments, are created, stored in etcd, and managed by built-in controllers. Then, we’ll demonstrate how to extend Kubernetes by defining and using a custom resource—illustrated here as a "FlightTicket"—and explain why a dedicated custom controller is necessary to act upon these new resources.

***

## Standard Kubernetes Resource: Deployment

When you create a Deployment in Kubernetes, the API server stores its state in etcd. A built-in controller, known as the deployment controller, continuously monitors the Deployment to ensure that the desired state (for example, maintaining three replicas) is met by creating or deleting pods as needed.

Below is an example Deployment definition file:

```yaml theme={null}
