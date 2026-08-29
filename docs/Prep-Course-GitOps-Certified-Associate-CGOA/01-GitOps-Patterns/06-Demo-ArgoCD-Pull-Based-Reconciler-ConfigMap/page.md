# or watch continuously:
kubectl -n highway-animation get pods -w
```

Before the change (example):

```bash theme={null}
NAME                                    READY   STATUS    RESTARTS   AGE
highway-animation-c88486bd5-4hbhf       1/1     Running   0          31m
highway-animation-c88486bd5-5z542       1/1     Running   0          31m
```

Now update the deployment manifest in Git to increase replicas and update the `POD_COUNT` environment variable. Example patch: change `replicas: 2` to `replicas: 8`.

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
  namespace: highway-animation
spec:
  replicas: 8
  selector:
    matchLabels:
      app: highway-animation
  template:
    metadata:
      labels:
        app: highway-animation
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:blue
          ports:
            - containerPort: 3000
          env:
            - name: POD_COUNT
              value: "8"
```

Commit and push the change to your Git repository. Gitea will send a webhook to Argo CD; Argo CD will receive it and, when auto-sync is enabled for the application, immediately start reconciling to the new desired state.

You can inspect webhook deliveries and responses in your Git provider’s UI to confirm successful delivery and the HTTP 200 response from Argo CD.

<Frame>
  <img alt="The image shows the Argo CD dashboard displaying an application's deployment status, including its health as &#x22;Healthy&#x22; and sync status as &#x22;Synced.&#x22; The interface also shows a visual representation of the application's components and their current deployment states." />
</Frame>

Within Argo CD you can review the application sync history and events to confirm the webhook-triggered sync was initiated and completed. In this demo the reconciliation completed quickly and the Deployment scaled to the target replica count.

<Callout icon="lightbulb">
  To avoid unnecessary reconciliations (for example, when non-manifest files like `README.md` or `.gitignore` are committed), configure branch or path filters in your Git provider’s webhook settings or limit triggers to commits that change manifest files. This reduces noise and conserves reconciliation resources.
</Callout>

That completes the demonstration of using webhooks to enable event-driven reconciliation in Argo CD.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/58bf23dc-377b-49b0-b736-4b7eed7ee677" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/b45b14a9-9560-4a64-83ad-773069aaad8f" />
</CardGroup>


# Demo ArgoCD Pull Based Reconciler ConfigMap

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Demo-ArgoCD-Pull-Based-Reconciler-ConfigMap/page

How to speed up ArgoCD Git polling by setting timeout.reconciliation in argocd-cm ConfigMap, restarting the application controller, and verifying faster reconciliation

ArgoCD performs reconciliation by polling Git and comparing the desired state to cluster state. By default ArgoCD polls at a relatively low frequency (often on the order of minutes). This guide shows how to tune ArgoCD's pull-based reconciler to poll Git more frequently (for example, every 10s) by updating the `argocd-cm` ConfigMap and restarting the application controller so the new setting takes effect.

Key steps

* Edit the `argocd-cm` ConfigMap in the `argocd` namespace and set `timeout.reconciliation` to a duration string (for example, `"10s"`).
* Restart the ArgoCD application controller (Deployment or StatefulSet) so it loads the updated configuration.
* Verify the new behavior by changing an ArgoCD-managed manifest in Git and observing faster reconciliation.

<Frame>
  <img alt="The image is a screenshot of the Argo CD documentation webpage, displaying information about automated sync semantics in Kubernetes, with a sidebar menu for navigation." />
</Frame>

## 1. Edit the ConfigMap (set poll/reconciliation interval)

Open the `argocd-cm` ConfigMap in the `argocd` namespace and edit it:

```bash theme={null}
kubectl -n argocd edit cm argocd-cm
```

Under the ConfigMap `data:` section add or update `timeout.reconciliation` with a duration string (examples: `"10s"`, `"60s"`, `"1m"`). The value must be a string.

Minimal example to add:

```yaml theme={null}
apiVersion: v1
data:
  # Poll/reconciliation interval. This must be a string duration.
  timeout.reconciliation: "10s"
```

If your ConfigMap already contains `resource.customizations` (for ignoring noisy fields or other behaviors), keep those entries. A common pattern includes `resource.customizations.ignoreResourceUpdates.*` to avoid unnecessary drift detection noise. Example entries you can keep or adapt:

```yaml theme={null}
data:
  resource.customizations.ignoreResourceUpdates.ConfigMap: |
    jqPathExpressions:
      # Ignore cluster-autoscaler last-updated annotation
      - '.metadata.annotations["cluster-autoscaler.kubernetes.io/last-updated"] = ""'
      # Ignore legacy leader election annotation
      - '.metadata.annotations["control-plane.alpha.kubernetes.io/leader"] = ""'
  resource.customizations.ignoreResourceUpdates.Endpoints: |
    jsonPointers:
      - /metadata
      - /subsets
  resource.customizations.ignoreResourceUpdates.all: |
    jsonPointers:
      - /status
```

Note: The exact customization keys and formats depend on your ArgoCD version and needs. The important setting for poll frequency is `timeout.reconciliation`.

<Callout icon="lightbulb">
  After you save the edited ConfigMap, you must restart the ArgoCD application controller (Deployment or StatefulSet) so the controller picks up the new `timeout.reconciliation` value.
</Callout>

## 2. Restart the application controller

The application controller must be restarted to load the new ConfigMap value. Most ArgoCD installations use a Deployment named `argocd-application-controller`, but some use a StatefulSet.

For a Deployment:

```bash theme={null}
kubectl -n argocd rollout restart deployment argocd-application-controller
```

For a StatefulSet:

```bash theme={null}
kubectl -n argocd rollout restart sts argocd-application-controller
```

Confirm the rollout status:

```bash theme={null}
kubectl -n argocd get deployment argocd-application-controller
