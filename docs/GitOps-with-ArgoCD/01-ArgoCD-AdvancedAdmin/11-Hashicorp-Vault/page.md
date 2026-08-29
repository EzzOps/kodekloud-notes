# Hashicorp Vault

Source: https://notes.kodekloud.com/docs/GitOps-with-ArgoCD/ArgoCD-AdvancedAdmin/Hashicorp-Vault/page

This article explains integrating the ArgoCD Vault Plugin with HashiCorp Vault to securely fetch and inject secrets into Kubernetes resources.

In this article, we demonstrate how the ArgoCD Vault Plugin fetches secrets from HashiCorp Vault and injects them into Kubernetes resources. This guide explains how the plugin retrieves secrets from secret management systems—such as HashiCorp Vault, IBM Cloud Secrets Manager, and AWS Secrets Manager—and integrates them into your Kubernetes YAML manifests.

## Overview

The ArgoCD Vault Plugin is a custom extension for ArgoCD that securely retrieves secrets from external vaults and dynamically injects them into Kubernetes configurations. In our example, HashiCorp Vault is used to store secrets securely. The plugin then retrieves these secrets and replaces placeholders in the Kubernetes manifest with the actual secret values.

HashiCorp Vault controls access to sensitive data in public or hybrid environments using secret engines. In this guide, the key-value secrets engine is enabled to store and retrieve plain text secrets. Here, the `kvput` command writes a secret—specifically the `MYSQL-PASSWORD`—to a defined path in Vault.

<Callout icon="lightbulb">
  In Vault, sensitive values stored in plain text are referenced in Kubernetes manifests using the `stringData` field rather than `data`. The `stringData` field accepts plain text without requiring Base64 encoding.
</Callout>

## Example Walkthrough

Below is a comprehensive example that illustrates the necessary commands and configuration details.

### Step 1: Enable the Key-Value Secrets Engine

Enable the key-value secrets engine (version 2) at a specified path:

```bash theme={null}
