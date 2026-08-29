# Demo Manual sync

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/ArgoCD/Demo-Manual-sync/page

Demonstrates using Argo CD manual sync mode to apply Git manifests, detect drift from live edits, and reconcile cluster resources back to Git desired state.

This guide demonstrates how to perform a manual synchronization in the Argo CD web UI. It walks through:

* What happens when an application is configured with manual sync mode.
* Creating cluster resources from Git via the Argo CD UI.
* How Argo CD detects drift when live resources are edited directly.
* Reconciling the application back to Git’s desired state.

Argo CD was configured with synchronization mode set to manual. That means Argo CD reads the manifests from the Git repository (the desired state) but will not apply changes to the cluster until you explicitly trigger a sync.

## Desired manifests discovered by Argo CD

Argo CD inspects the Git repo and shows the desired manifests. For example, the Service manifest discovered by Argo CD:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  annotations:
    argocd.argoproj.io/tracking-id: highway-animation:/Service:highway-animation/highway-animation-service
  name: highway-animation-service
  namespace: highway-animation
spec:
  ports:
    - nodePort: 32000
      port: 3000
      protocol: TCP
      targetPort: 3000
  selector:
    app: highway-animation
```

Because the application has not yet been applied to the cluster, there is no “live” manifest for these resources. To create them, use the Argo CD UI’s Synchronize action.

<Frame>
  <img alt="A screenshot of the Argo CD web UI showing the &#x22;highway-animation&#x22; application marked OutOfSync, with a Synchronize dialog open on the right and options like &#x22;Auto-create namespace&#x22; checked. The left sidebar shows navigation items (Applications, Settings) and resource filters." />
</Frame>

When you click Synchronize, choose relevant options (for example, check “Auto-create namespace” if the namespace does not exist), then confirm the sync. Argo CD will pull the manifests from Git and apply them to the cluster: creating Namespace, Deployment, Service, ReplicaSet, and Pods.

## Verify resources with kubectl

Use kubectl to confirm the namespace and resources were created:

```bash theme={null}
