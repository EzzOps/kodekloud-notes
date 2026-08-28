# Namespaces

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Namespaces/page

Namespaces partition Kubernetes clusters into virtual sub-clusters, simplifying resource management and isolation for teams or environments.

## Overview

Namespaces partition Kubernetes clusters into virtual sub-clusters, simplifying resource management and isolation for teams or environments. This guide covers core concepts, commands, and best practices for working with namespaces.

## The House Analogy

Imagine two boys named Mark living in separate houses. To avoid confusion, one is called Mark Smith and the other Mark Williams. Inside each house, family members use only first names; outsiders always use the full name. Each house maintains its own rules and resources.

<Frame>
  ![The image shows two houses labeled "Mark Smith" and "Mark Williams," each containing figures representing people. A central figure is depicted with speech bubbles indicating the names "Mark Smith" and "Mark Williams."](https://kodekloud.com/kk-media/image/upload/v1752874000/notes-assets/images/Docker-Certified-Associate-Exam-Course-Namespaces/houses-mark-smith-williams-figures.jpg)
</Frame>

In Kubernetes, a **namespace** is like a house. Every Pod, Deployment, and Service lives in one namespace. By default, clusters include:

| Namespace   | Description                                                 |
| ----------- | ----------------------------------------------------------- |
| default     | User workloads by default                                   |
| kube-system | Cluster-internal components (DNS, networking plugins, etc.) |
| kube-public | Public resources visible to all users                       |

<Callout icon="triangle-alert">
  Avoid modifying resources in the **kube-system** namespace directly; changes can disrupt critical cluster services.
</Callout>

## Custom Namespaces

For development, testing, or multi-tenant clusters, create additional namespaces (e.g., **dev**, **prod**) to isolate:

* Resources
* Policies (RBAC rules)
* Quotas

<Frame>
  ![The image illustrates the concept of namespace isolation using house-shaped diagrams, each containing a circle, triangle, and square, labeled with different namespaces like "kube-system," "Default," "kube-public," "Dev," and "Prod."](https://kodekloud.com/kk-media/image/upload/v1752874001/notes-assets/images/Docker-Certified-Associate-Exam-Course-Namespaces/namespace-isolation-diagram-houses.jpg)
</Frame>

## RBAC and Resource Quotas

You can enforce per-namespace access control with RoleBindings and restrict resource usage using ResourceQuotas:

<Frame>
  ![The image illustrates a Kubernetes namespace resource limits concept, showing different environments (Default, Prod, Dev) with nodes and containers represented by various icons. It highlights how resources are allocated and managed across these environments.](https://kodekloud.com/kk-media/image/upload/v1752874003/notes-assets/images/Docker-Certified-Associate-Exam-Course-Namespaces/kubernetes-namespace-resource-limits.jpg)
</Frame>

## Service Discovery Across Namespaces

Within the same namespace, Services resolve by name:

```python theme={null}
