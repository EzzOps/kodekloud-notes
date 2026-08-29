# Section Introduction

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Installation/Section-Introduction/page

Guide to configuring and installing cluster and namespaced packages with Glasskube, covering monitoring, continuous deployment, analytics, databases, scopes, manifests, and RBAC best practices.

Welcome to the package installation chapter. Here we’ll move from provisioning your Kubernetes cluster into actively configuring and installing packages using Glasskube. This section shows how to manage packages for real-world workloads and maintain a balanced cluster that meets the needs of cluster operators and administrators.

We begin with package scopes — a core concept in Glasskube package management. You’ll learn the difference between cluster-scoped and namespaced packages, when to choose each, and the operational implications of those choices.

After that, we’ll walk through configuring and installing five packages that span four core areas:

* Monitoring
* Continuous deployment
* Analytics
* Databases

Each walkthrough provides step-by-step guidance so you can follow along and apply the same patterns in your own cluster using Glasskube.

<Callout icon="lightbulb">
  This chapter is hands-on: you’ll see how to configure package manifests, choose scopes, and perform installs. If you’re new to Kubernetes, review the [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) first to get the most out of these examples.
</Callout>

## Package scopes: cluster-scoped vs. namespaced

Understanding scope is essential to safe package management. Use cluster-scoped packages when the software must operate across the cluster (for example, a network plugin or cluster-wide monitoring). Use namespaced packages when the software’s resources should be isolated to a single namespace (for example, an application-specific database).

| Scope          | When to use                                                                                                                          | Operational impact                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Cluster-scoped | Services that require cluster-wide resources or control plane access (e.g., cluster-level monitoring, network policies)              | Requires cluster-admin permissions to install; affects resources across namespaces |
| Namespaced     | Application-level components that should be contained to a namespace (e.g., app-specific databases, logging agents for a single app) | Can be installed by namespace-scoped operators; reduces blast radius               |

<Callout icon="warning">
  Cluster-scoped package installations typically require elevated privileges. Always review RBAC and resource definitions before granting cluster-wide install permissions.
</Callout>

## What we’ll install (overview)

We’ll configure and install five representative packages that cover the four core areas listed above. These examples demonstrate common patterns in Glasskube package manifests and show how to choose scope, set configuration values, and perform safe upgrades.

| Area                  | Purpose                                          | Typical example packages      |
| --------------------- | ------------------------------------------------ | ----------------------------- |
| Monitoring            | Collect metrics and visualize cluster/app health | Prometheus, Grafana           |
| Continuous deployment | Automate application deployments                 | Argo CD, Flux                 |
| Analytics             | Collect and analyze usage or logs                | Elasticsearch, Kibana, Matomo |
| Databases             | Persistent application data storage              | PostgreSQL, MariaDB           |

Note: The examples above are typical choices in Kubernetes ecosystems. In the walkthroughs that follow, we’ll show manifest structure, configuration best practices, and install commands using Glasskube for packages in these areas.

## How to follow along

* Use a cluster you can safely modify (a lab cluster, local kind/minikube, or a test namespace in a development cluster).
* Ensure you have Glasskube installed and authenticated against the target cluster.
* Review each package’s configuration before applying it, paying special attention to `scope` and RBAC requirements.

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* Glasskube docs: `/docs/glasskube` (see local documentation for installation and CLI reference)
* Best practices for RBAC: [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/c3806869-7f9e-4cc2-8dc5-aa10304e3d1c/lesson/f142dd6a-2d0d-473c-a4b0-0acf72fed7bc" />
</CardGroup>
