# Horizontal Pod Autoscaler

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Cloud-Native-Architecture/Horizontal-Pod-Autoscaler/page

Learn about the Horizontal Pod Autoscaler in Kubernetes and how it adjusts the number of running pods based on current resource usage.

In this lesson, you'll learn about the Horizontal Pod Autoscaler (HPA) in Kubernetes and discover how it automatically adjusts the number of running pods based on the current resource usage. As its name implies, the HPA scales the pods horizontally—deploying more instances when demand increases and removing excess pods when demand decreases.

> **lightbulb** The HPA is one of Kubernetes' many controllers that works by adjusting the replica count of a Deployment. It scales up the replicas as demand grows and scales them down when the pressure eases.

## How the HPA Works

The HPA monitors your application's resource consumption by leveraging metrics collected from a metrics server. This server continuously tracks resource usage across nodes and pods in the cluster, providing accurate data for the HPA to decide when to scale.

The HPA configuration typically involves:

* Defining a Deployment for the application.
* Setting resource limits and requests within the Deployment.
* Creating an HPA object that targets the Deployment.

Let's explore an example configuration.

## Example Configuration

Below is an example YAML configuration for a Deployment that uses a container image with defined CPU resource limits:

```yaml theme={null}
