# Reconciliation loop

Source: https://notes.kodekloud.com/docs/GitOps-with-ArgoCD/ArgoCD-Intermediate/Reconciliation-loop/page

This article explains how ArgoCD synchronizes application updates in Kubernetes using its reconciliation loop and configurable timeout settings.

ArgoCD continuously reconciles the current state of your Kubernetes cluster to match the desired state defined in Git. In a GitOps workflow, application updates occur several times a day as developers commit changes. This article explains how ArgoCD synchronizes these updates with your cluster using its reconciliation loop.

ArgoCD’s reconciliation loop determines how frequently it pulls the desired state from the Git repository. Typically, the default timeout is set to 3 minutes. This timeout value, configurable within the ArgoCD repo server, dictates the wait period for a reconciliation operation before timing out.

The ArgoCD repo server fetches the desired state from Git and its behavior can be modified through the environment variable `ARGOCD_RECONCILIATION_TIMEOUT`. This variable is established using the key `timeout.reconciliation` in the ArgoCD configuration map (`argocd-cm`). By default, this configuration map is empty upon installation. You can customize the reconciliation timeout (for example, to 300 seconds) by patching this configuration map and then restarting the ArgoCD repo server deployment.

Once the configuration is updated and the deployment is restarted, ArgoCD checks for any changes in the Git repository every 5 minutes—unless webhooks are implemented to trigger immediate reconciliations.

<Callout icon="lightbulb">
  For immediate synchronization after each commit, configure a webhook on your Git provider that targets `[ARGOCD_SERVER_URL]/api/webhook`. This setup bypasses the default polling mechanism.
</Callout>

Below is a consolidated set of commands to patch the configuration map, restart the repo server, and verify the updated timeout setting:

```bash theme={null}
