# ArgoCD Vault Plugin CLI

Source: https://notes.kodekloud.com/docs/GitOps-with-ArgoCD/ArgoCD-AdvancedAdmin/ArgoCD-Vault-Plugin-CLI/page

This guide explains how to use the ArgoCD Vault Plugin to fetch secrets from HashiCorp Vault and generate Kubernetes manifest files.

This guide demonstrates how the ArgoCD Vault Plugin connects with HashiCorp Vault to fetch secrets and generate Kubernetes manifest files by replacing placeholders with actual secret data.

***

## Overview

The ArgoCD Vault Plugin is a Git repository tool that retrieves secrets from various secret management systems, including HashiCorp Vault, IBM Cloud Secret Manager, and AWS Secret Manager. In this demo, we will focus on integrating with HashiCorp Vault.

<Frame>
  ![The image shows a GitHub page for the "argocd-vault-plugin," displaying its status badges and a brief description of its functionality related to secret management in Kubernetes.](https://kodekloud.com/kk-media/image/upload/v1752877456/notes-assets/images/GitOps-with-ArgoCD-ArgoCD-Vault-Plugin-CLI/argocd-vault-plugin-github-page.jpg)
</Frame>

***

## Setting Up HashiCorp Vault

To get started, you need to deploy a Vault instance where you can add and later retrieve secrets. For this demo, we will deploy Vault using the HashiCorp Vault Helm chart and manage the deployment via ArgoCD.

### Installing Vault via Helm

Follow these steps to install Vault with Helm:

1. Add the HashiCorp Helm repository:

   ```bash theme={null}
   helm repo add hashicorp https://helm.releases.hashicorp.com
   # "hashicorp" has been added to your repositories
   ```

2. Install Vault:

   ```bash theme={null}
   helm install vault hashicorp/vault
   ```

3. Create an ArgoCD application for the Vault Helm chart. For this example, we deploy version 0.16.0 into the namespace “vault-demo.” Modify the Vault configuration to disable data storage by setting `server.datastore.enabled` to false and change the UI service type to NodePort to access the Vault UI through a browser.

   For instance, your Vault configuration snippet might resemble:

   ```bash theme={null}
   ui = true
   listener "tcp" { 
     tls_disable = 1 
     address = "[::]:8200" 
     cluster_address = "[::]:8201" 
   }
   storage "consul" { 
     path = "vault" 
     address = "HOST_IP:8500" 
   }
   ```

   And update the service configuration with:

   ```yaml theme={null}
   apiVersion: v1
   kind: Service
   metadata:
     name: vault-app
   spec:
     type: NodePort
     ports:
       - name: http
         port: 8200
         targetPort: 8200
       - name: https-internal
         port: 8201
         targetPort: 8201
     selector:
       app.kubernetes.io/instance: vault-app
       app.kubernetes.io/name: vault
       component: server
   ```

   After synchronizing the application, multiple resources will be created. The Vault pod may be in a progressing state until Vault is fully initialized.

<Frame>
  ![The image shows a dashboard interface of an application management tool, displaying a tree structure of components related to a "vault-app" with various sync and health statuses.](https://kodekloud.com/kk-media/image/upload/v1752877457/notes-assets/images/GitOps-with-ArgoCD-ArgoCD-Vault-Plugin-CLI/vault-app-dashboard-interface-tree.jpg)
</Frame>

***

### Accessing and Initializing Vault

After the Vault application is deployed, check the “vault-demo” namespace to verify the running resources:

```bash theme={null}
