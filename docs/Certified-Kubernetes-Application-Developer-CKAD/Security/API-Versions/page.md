# API Versions

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/API-Versions/page

This article explores API versions in Kubernetes, detailing their stages, organization, and management for effective configuration.

In this lesson, we explore API versions in Kubernetes—a topic that builds upon core concepts such as APIs, API groups, resources, and verbs. Understanding the evolution of these API versions—from experimental to stable—is key to effectively managing your Kubernetes configurations.

## Overview of API Organization

Kubernetes organizes everything under its API into API groups (e.g., apps, extensions, networking). Each API group can support multiple versions. A version labeled as "v1" typically indicates a generally available (GA) and stable release. Other labels like v1beta1 or v1alpha1 denote beta or alpha stages respectively. Let’s break down what each of these stages means.

## API Version Stages

### Alpha

An alpha version represents the initial development stage of an API. Once an API is added to the Kubernetes code base and included in a release for the first time, it is marked as alpha (for example, v1alpha1, v1alpha2). At this stage, the API is not enabled by default, may lack comprehensive end-to-end tests, and could contain bugs. For instance, at the time of recording, the API group `internal.apiserver.k8s.io` (which includes the StorageVersion resource) exists only in its alpha form.

If you attempt to create an object using the following YAML:

```yaml theme={null}
apiVersion: internal.apiserver.k8s.io/v1alpha1
kind: StorageVersion
metadata:
  name: sv-1
spec:
```

the API server will reject the creation because the alpha version is not enabled by default. This version is intended for expert users who want to test and provide early feedback.

### Beta

After addressing major bugs in the alpha API and adding comprehensive tests, the API advances to beta (e.g., v1beta1, v1beta2). Beta APIs are enabled by default and include end-to-end tests. While minor bugs might still exist, there is a commitment from the community to advance these APIs to GA. For example, the flow-control group is currently in the beta stage.

### GA (Stable)

An API promoted to GA has successfully navigated the beta phase, undergone multiple releases, and received numerous bug fixes. The version number drops any alpha or beta suffix, appearing simply as "v1." GA APIs are reliably enabled by default and become part of conformance tests. Most API groups, such as apps, authentication, authorization, certificates, and coordination, are now available in their GA versions.

<Frame>
  ![The image outlines API versioning stages: Alpha, Beta, and GA (Stable), detailing their version names, enablement, testing, reliability, support, and target audience.](https://kodekloud.com/kk-media/image/upload/v1752871272/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-API-Versions/frame_210.jpg)
</Frame>

<Callout icon="lightbulb">
  For production environments, always ensure you use GA versions of the APIs to maintain a stable and supported deployment.
</Callout>

## Supporting Multiple Versions in an API Group

An API group can support several versions simultaneously. For example, the apps group might offer v1, v1beta1, and v1alpha1, allowing you to reference any of these versions in your YAML file. Below are examples of a Deployment resource defined using different API versions:

```yaml theme={null}
