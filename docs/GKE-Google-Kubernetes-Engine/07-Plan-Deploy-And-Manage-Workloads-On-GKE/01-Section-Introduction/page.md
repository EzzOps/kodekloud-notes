# Section Introduction

Source: https://notes.kodekloud.com/docs/GKE-Google-Kubernetes-Engine/Plan-Deploy-And-Manage-Workloads-On-GKE/Section-Introduction/page

This guide covers planning, deploying, and managing various workloads on Google Kubernetes Engine for optimal performance and scalability.

Welcome to your guide on optimizing workloads in Google Kubernetes Engine (GKE). In this tutorial, you’ll learn how to plan, deploy, and operate a variety of workloads—ranging from stateless services to stateful applications and batch jobs—while ensuring performance, scalability, and resilience.

![The image is a diagram illustrating "Effective Workload Management" with GKE, focusing on planning, deploying, and managing for performance, scalability, and resilience.](https://kodekloud.com/kk-media/image/upload/v1752875735/notes-assets/images/GKE-Google-Kubernetes-Engine-Section-Introduction/effective-workload-management-gke-diagram.jpg)

## Table of Contents

* [Workload Planning](#workload-planning)
  * [Stateless vs. Stateful](#stateless-vs-stateful)
  * [Batch Jobs](#batch-jobs)
  * [DaemonSets](#daemonsets)
* [Node Taints and Tolerations](#node-taints-and-tolerations)
* [Rolling Updates in GKE](#rolling-updates-in-gke)
* [Further Reading](#further-reading)

***

## Workload Planning

Before you deploy to GKE, identify which workload type best fits your application requirements:

| Workload Type | Use Case                               | Kubernetes Resource |
| ------------- | -------------------------------------- | ------------------- |
| Stateless     | Web front-ends, APIs                   | `Deployment`        |
| Stateful      | Databases, message queues              | `StatefulSet`       |
| Batch         | Data processing, CI/CD tasks           | `Job` / `CronJob`   |
| Daemon        | Node log collection, monitoring agents | `DaemonSet`         |

### Stateless vs. Stateful

Stateless applications can scale horizontally without preserving local state.\
Stateful workloads require stable network identities and persistent storage.

```yaml theme={null}
