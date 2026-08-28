# Create Application using CLI

Source: https://notes.kodekloud.com/docs/GitOps-with-ArgoCD/ArgoCD-Basics/Create-Application-using-CLI/page

This guide explains how to create, synchronize, and verify an ArgoCD application using the command-line interface.

In this guide, you will learn how to create, synchronize, and verify an ArgoCD application using the command-line interface (CLI). Previously, we explored creating and deleting applications via the UI. Now, we'll delve into performing these tasks with the CLI for a more automated and scriptable approach.

## Creating Applications

You can create an ArgoCD application with the `argocd app create` command. This command supports various configuration options, allowing you to deploy applications managed as Git directory-based manifests, Jsonnet, Helm (from both Git and Helm repositories), Kustomize, or even using a custom configuration management plugin.

Below are examples for different application types:

```bash theme={null}
