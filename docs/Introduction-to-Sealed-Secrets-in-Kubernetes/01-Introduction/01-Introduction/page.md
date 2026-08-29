# Introduction

Source: https://notes.kodekloud.com/docs/Introduction-to-Sealed-Secrets-in-Kubernetes/Introduction/Introduction/page

This article explains Sealed Secrets, an open-source tool for securely managing sensitive data in Kubernetes and Terraform environments.

## Introduction

Sealed Secrets is an open-source tool by Bitnami for managing sensitive data securely in Kubernetes and other environments like Terraform. Instead of storing raw secrets in your Git repository, you encrypt them into “sealed” Secrets, which only the target cluster can decrypt.

In this lesson, we will:

* Define Sealed Secrets and its primary use cases
* Explore core components and workflow
* Demonstrate a hands-on example to seal and unseal secrets

> **lightbulb** You will need access to a running Kubernetes cluster and the `kubeseal` CLI installed locally.

***

## What You’ll Learn

| Topic                | Description                                                            |
| -------------------- | ---------------------------------------------------------------------- |
| Core Concepts        | Overview of Sealed Secrets architecture and components                 |
| Workflow Overview    | Encrypting, committing, and decrypting secrets                         |
| Demo                 | Creating a Kubernetes Secret, sealing it, and applying it to a cluster |
| Integration with IaC | Using Sealed Secrets in Terraform and GitOps pipelines                 |

***

## Core Components Overview

Sealed Secrets relies on three main components:

* SealedSecret custom resource for encrypted data
* Controller that runs in-cluster to decrypt SealedSecrets into native Kubernetes Secrets
* kubeseal CLI for encrypting Secret manifests outside the cluster

***

## References

* [Sealed Secrets GitHub Repository][sealed-secrets-gh]
* [Bitnami Sealed Secrets Documentation][sealed-secrets-docs]
* [Kubernetes Secrets][k8s-secrets]

[kubeseal-docs]: https://github.com/bitnami-labs/sealed-secrets#usage

[sealed-secrets-gh]: https://github.com/bitnami-labs/sealed-secrets

[sealed-secrets-docs]: https://github.com/bitnami-labs/sealed-secrets#readme

[k8s-secrets]: https://kubernetes.io/docs/concepts/configuration/secret/

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes/module/fbf97fdc-fe0f-4d01-b19a-d1be56322bac/lesson/febac6c6-137c-4a40-b684-cf1d940c625a)
