# Reconciliation loop

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Reconciliation-loop/page

Explains Argo CD reconciliation loop, adjusting polling interval via timeout.reconciliation in argocd-cm, restarting repo-server, and using webhooks for instant sync.

A reconciliation loop is how often an [Argo CD](https://argo-cd.readthedocs.io/en/stable/) Application controller attempts to synchronize the declared desired state in Git with the live state in the Kubernetes cluster. In typical GitOps workflows with frequent commits, Argo CD polls the Git repository periodically (about every three minutes by default) to detect changes.

The polling behavior is implemented by the argocd-repo-server and is driven by the config key `timeout.reconciliation`. This key is exposed to the repo-server as the environment variable `ARGOCD_RECONCILIATION_TIMEOUT` via the `argocd-cm` ConfigMap.

To adjust how often Argo CD polls Git (for example, to poll every five minutes instead of the default three), update the `argocd-cm` ConfigMap with a new `timeout.reconciliation` value and restart the argocd-repo-server so it reads the change.

|                              Setting | Purpose                                    | Example                         |
| -----------------------------------: | ------------------------------------------ | ------------------------------- |
| `argocd-cm` `timeout.reconciliation` | Controls repo-server polling interval      | `"300s"` or `"5m"`              |
|                              Env var | Exposes the ConfigMap value to repo-server | `ARGOCD_RECONCILIATION_TIMEOUT` |
|                            Component | Where the change takes effect              | `argocd-repo-server` deployment |

Steps to change the reconciliation interval:

1. Inspect the repo-server pod environment to confirm the `ARGOCD_RECONCILIATION_TIMEOUT` reference.
2. Patch the `argocd-cm` ConfigMap with the desired timeout (include a time unit).
3. Restart the repo-server deployment to pick up the new value.
4. Verify the restarted pod shows the updated environment reference.

Example commands:

```bash theme={null}
