# What is Kubernetes

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Interview-Setup/What-is-Kubernetes/page

Overview of Kubernetes fundamentals for DevOps interview covering desired state model, control plane components, scheduling, kubelet responsibilities, and running containerized workloads at scale.

In this lesson/article for a DevOps engineer interview, we’ll start with the fundamentals of Kubernetes and how it makes running containers at scale reliable and declarative.

What is Kubernetes?

Kubernetes is a control plane that runs containerized workloads across a fleet of machines and continuously reconciles the cluster to match the desired state you declare. Instead of specifying which machine should run a workload, you declare the desired outcome (for example, how many replicas of a service you want) and Kubernetes makes that happen — and keeps it that way.

Example: declare three replicas

```yaml theme={null}
