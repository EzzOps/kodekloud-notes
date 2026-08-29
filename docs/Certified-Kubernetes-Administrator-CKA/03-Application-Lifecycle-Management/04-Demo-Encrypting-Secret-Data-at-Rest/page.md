# Demo Encrypting Secret Data at Rest

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Application-Lifecycle-Management/Demo-Encrypting-Secret-Data-at-Rest/page

This guide explains how to secure secret data in Kubernetes by enabling encryption at rest.

In this guide, we explain how to secure secret data in your Kubernetes cluster by enabling encryption at rest. We start by creating secret objects, examine how Kubernetes encodes them in etcd, and then show you how to configure the API server to encrypt these secrets.

***

## Creating a Secret Object

Begin by launching your Kubernetes playground—a single-node cluster running Kubernetes with ContainerD. Kubernetes makes it easy to create secrets from files, literal values, or environment files. Below are some example commands:

```bash theme={null}
