# Deployment Strategy Canary

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/POD-Design/Deployment-Strategy-Canary/page

This guide explores implementing canary deployments in Kubernetes to safely introduce new changes while minimizing risk during production testing.

In this guide, we explore how to implement canary deployments in Kubernetes to safely introduce new changes. A canary deployment enables you to deploy a new version of your application alongside the current version while routing only a small percentage of traffic to the latest version. This approach minimizes risk while testing new features in production.

Below you will find a detailed explanation of how to achieve this strategy using Kubernetes Deployments and Services.

## Overview of the Canary Deployment Process

Begin by deploying the primary version of your application. In this configuration, the primary deployment runs five pods, and a Kubernetes Service routes traffic to these pods. A label, for example, `version: v1`, is assigned to the pods to facilitate proper routing.

Next, deploy a secondary deployment for the canary version. Initially, all traffic is directed to version v1. The canary deployment tests the new version (version v2) by ensuring that only a small portion of traffic is routed to it. If the new version meets expectations, you can later update the primary deployment and retire the canary.

The key steps include:

1. Using a single Service to route traffic to both deployments by leveraging a common label (e.g., `app: front-end`).
2. Setting a lower replica count for the canary deployment (e.g., `replicas: 1`) so that a limited percentage of traffic reaches version v2.
3. Once testing is successful, upgrading the primary deployment to the new version and removing the canary deployment.

Consider the following diagram that illustrates the traffic distribution, with roughly 83% of traffic directed to version v1 and 17% to version v2:

<Frame>
  ![The image illustrates a canary deployment strategy, routing 83% of traffic to version v1 and 17% to version v2 of a front-end app.](https://kodekloud.com/kk-media/image/upload/v1752871252/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Deployment-Strategy-Canary/frame_170.jpg)
</Frame>

## Implementation Details

### Primary Deployment and Service

The primary version of the application is deployed using a Kubernetes Deployment. A corresponding Service directs traffic to the pods, which are marked with the label `app: front-end` to ensure correct routing.

### Canary Deployment

A separate deployment is created for the canary version, which uses a new image (e.g., version 2.0) and labels the pods with `version: v2`. Although both deployments share the common label `app: front-end`, setting the canary deployment’s replica count to 1 ensures that only a minor portion of traffic is routed to the new version.

<Callout icon="lightbulb">
  Keep in mind that the percentage of traffic routed to each version is directly influenced by the number of pod replicas. The inherent traffic distribution mechanism in Kubernetes spreads traffic evenly across all pods.
</Callout>

### Limitation

One limitation of this Kubernetes-only setup is that traffic distribution is solely determined by the number of pods in each deployment. For example, if you want an exact percentage split (e.g., precisely 1% to the canary), Kubernetes alone may not suffice unless you have a very high number of pods. For more granular control, consider using a service mesh like [Istio Service Mesh](https://learn.kodekloud.com/user/courses/istio-service-mesh), which allows for precise, percentage-based traffic routing regardless of pod count.

## Code Example

Below are examples of Kubernetes configuration files to define your primary and canary deployments alongside a Service.

```yaml theme={null}
