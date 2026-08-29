# Services ClusterIP

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Services-ClusterIP/page

This article explains the Kubernetes Service type ClusterIP for stable in-cluster communication and load balancing among Pods.

In this lesson, we’ll deep-dive into the Kubernetes Service of type **ClusterIP**—the default Service type for in-cluster communication. In a typical multi-tier application (front-end, back-end, in-memory cache like [Redis](https://redis.io/), and a database such as [MySQL](https://www.mysql.com/)), each component lives in its own set of Pods. Since Pod IPs are ephemeral, you need a stable endpoint for reliable, load-balanced communication between tiers.

A **ClusterIP Service** assigns a virtual IP and DNS name inside the cluster. Pods can address the Service by name (e.g., `back-end`), and Kubernetes will distribute traffic across the matching Pods.

![The image is a diagram of a Kubernetes ClusterIP setup, showing a network of pods organized into front-end, back-end, and Redis layers, each with specific IP addresses.](https://kodekloud.com/kk-media/image/upload/v1752874032/notes-assets/images/Docker-Certified-Associate-Exam-Course-Services-ClusterIP/kubernetes-clusterip-diagram-pods.jpg)

## Why Use a ClusterIP Service?

| Benefit                   | Description                                                                 |
| ------------------------- | --------------------------------------------------------------------------- |
| Stable in-cluster address | Pods reference a single virtual IP and DNS name instead of changing Pod IPs |
| Built-in load balancing   | Distributes traffic evenly across all healthy Pods                          |
| Decoupling components     | Front-end, back-end, cache, and DB tiers communicate via service names      |

## Defining a ClusterIP Service

Create `service-definition.yml` to expose your back-end Pods:

```yaml theme={null}
