# Demo Setup Bitnami Sealed Secrets

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Demo-Setup-Bitnami-Sealed-Secrets/page

Guide to deploying Bitnami Sealed Secrets using Helm or Argo CD and installing kubeseal to enable encrypted Kubernetes secrets for GitOps workflows.

In this guide you'll deploy Bitnami Sealed Secrets into a Kubernetes cluster using Argo CD. We'll reference the official Helm chart on Artifact Hub and walk through both a direct Helm install and an Argo CD Application-based deployment. Finally, you'll install the kubeseal CLI so you can create SealedSecrets that are safe to store in Git — enabling a GitOps workflow.

<Frame>
  <img alt="The image shows a webpage for &#x22;sealed-secrets&#x22; on Artifact Hub, detailing a Helm chart for a sealed-secrets controller with options to install, templates, default values, and a changelog. It also features a banner for KubeCon + CloudNativeCon India 2023." />
</Frame>

The Artifact Hub page lists the Helm repository URL, available chart versions, values and installation instructions. You can either install the chart locally with Helm or configure Argo CD to fetch the Helm chart and keep it synchronized.

## Option A — Install locally with Helm

Add the Bitnami Labs repo and install the sealed-secrets chart. Pick a chart version that matches your requirements (example below uses `2.17.3`):

```bash theme={null}
helm repo add bitnami-labs https://bitnami-labs.github.io/sealed-secrets/
helm repo update
helm install my-sealed-secrets bitnami-labs/sealed-secrets --version 2.17.3
```

Tip: override chart values by creating a `values.yaml` file and passing `-f values.yaml` to `helm install`.

## Option B — Deploy via Argo CD (recommended for GitOps)

Configure an Argo CD Application that points to the Bitnami Labs Helm repo so Argo CD can fetch and sync the chart automatically.

Steps in the Argo CD UI:

* Set Source Type to **Helm** and paste the Helm repository URL: `https://bitnami-labs.github.io/sealed-secrets/`
* Select the `sealed-secrets` chart and pick the desired chart version (for example, `2.17.0` or `2.17.3`)
* Set the Destination cluster and choose the target namespace (this example uses `kube-system`)
* Optionally enable Auto-Sync so changes in the chart are applied automatically

<Frame>
  <img alt="The image shows a software configuration interface for an application called &#x22;sealed-secrets&#x22; in ArgoCD, with options for setting sync policies and other settings like schema validation and namespace creation." />
</Frame>

After you create the Application, Argo CD will fetch the chart, render templates (using chart defaults unless you override them), and deploy the resources to the target namespace. The sealed-secrets Helm chart typically creates:

| Resource Type     | Purpose                                               |
| ----------------- | ----------------------------------------------------- |
| Deployment / Pods | Runs the sealed-secrets controller                    |
| Services          | Controller and metrics endpoints                      |
| RBAC              | ServiceAccount, Roles, and RoleBindings required      |
| CRDs              | CustomResourceDefinitions for SealedSecret            |
| TLS Secret        | Controller keypair (public key is used by `kubeseal`) |

When sync completes in Argo CD, the Application should show a healthy and synced status.

<Frame>
  <img alt="The image shows an Argo CD interface with two applications, &#x22;highway-animation&#x22; and &#x22;sealed-secrets,&#x22; both displaying a status of &#x22;Healthy&#x22; and &#x22;Synced.&#x22; It includes options to sync, refresh, or delete the applications." />
</Frame>

You can also inspect the Application and its resources in the Argo CD UI.

<Frame>
  <img alt="The image shows a user interface of Argo CD, displaying the &#x22;sealed-secrets&#x22; application with a healthy and synced status, along with its related resources and configurations." />
</Frame>

## Verify the controller in Kubernetes

Use kubectl to confirm the controller, services and the TLS secret are present in the target namespace (example uses `kube-system`):

```bash theme={null}
