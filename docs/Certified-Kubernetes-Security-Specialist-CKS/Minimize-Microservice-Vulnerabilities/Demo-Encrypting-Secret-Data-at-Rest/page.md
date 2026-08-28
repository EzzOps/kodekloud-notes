# Demo Encrypting Secret Data at Rest

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Minimize-Microservice-Vulnerabilities/Demo-Encrypting-Secret-Data-at-Rest/page

This guide explains how to secure secret data at rest in Kubernetes by encrypting it within the etcd datastore.

In this guide, you'll learn how to secure secret data at rest in Kubernetes by encrypting it inside the etcd datastore. We cover creating secret objects, inspecting their base64-encoded storage, and finally enabling encryption at rest through an encryption configuration. This step-by-step process helps ensure that confidential information remains protected even if someone gains access to your etcd datastore.

***

## 1. Creating a Secret in Kubernetes

Begin by launching your single-node Kubernetes playground built with Kubernetes and ContainerD. Open your terminal to create a secret object using various methods. Here are several examples:

```bash theme={null}
