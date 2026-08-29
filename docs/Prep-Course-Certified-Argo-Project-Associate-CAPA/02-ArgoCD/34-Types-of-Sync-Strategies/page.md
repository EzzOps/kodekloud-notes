# Types of Sync Strategies

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Types-of-Sync-Strategies/page

Overview of Argo CD sync strategies explaining manual versus automatic sync, auto-pruning, and self-heal options for keeping Kubernetes clusters aligned with Git manifests

This article explains the synchronization strategies Argo CD uses to apply changes from a Git repository to a Kubernetes cluster. Understanding these options helps you choose the right GitOps behavior for your environment—whether you prefer hands-off deployment, strict cluster hygiene, or automatic recovery from out-of-band changes.

Argo CD sync policies determine how and when Git changes are propagated to the cluster:

* Manual vs Automatic sync
  * Automatic sync: Argo CD applies new or changed manifests from Git to the cluster as soon as it detects them (for example via a webhook).
  * Manual sync: Argo CD detects the change but waits for a user or operator to trigger the sync operation.

* Auto-pruning
  * With pruning enabled, resources removed from Git are deleted from the target cluster during the next sync.
  * With pruning disabled, deleting manifests from Git does not remove the corresponding resources from the cluster.

* Self-heal (automatic reconciliation of out-of-band changes)
  * With self-heal enabled, Argo CD automatically reverts manual or out-of-band changes made directly to the cluster (for example via kubectl), restoring the state defined in Git.
  * With self-heal disabled, Argo CD does not automatically revert such manual changes.

<Callout icon="lightbulb">
  Key points about the Argo CD syncPolicy automated block:

  * Presence of the `automated` block enables automatic sync; there is no `enabled` boolean—omitting `automated` leaves sync manual.
  * `automated.prune: true` enables automatic deletion of resources removed from Git.
  * `automated.selfHeal: true` enables automatic reconciliation of out-of-band cluster changes.
</Callout>

A minimal Application snippet that enables automatic sync, pruning, and self-heal looks like this:

```yaml theme={null}
