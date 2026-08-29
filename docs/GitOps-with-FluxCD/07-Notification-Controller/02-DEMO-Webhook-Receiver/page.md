# in bb-app-source/2-demo/deployment.yaml
spec:
  replicas: 1
```

Commit and push the update. Once Flux reconciles, you will see a notification in **flux-alerts-channel**:

![The image shows a Slack workspace with a channel named "flux-alerts-channel" where users and bots are interacting, including messages about a Flux Alerts Application and a git repository update.](https://kodekloud.com/kk-media/image/upload/v1752877686/notes-assets/images/GitOps-with-FluxCD-DEMO-Alerts-amp-Providers/slack-workspace-flux-alerts-channel-4.jpg)

***

## 6. Verify the Update in Kubernetes

Confirm that your deployment reflects the new replica count:

```bash theme={null}
kubectl -n 2-demo get pods
```

***

Congratulations! You have successfully configured Flux Notification Controller to deliver Slack alerts for all your Flux events.

***

## Links and References

* [Flux Notification Providers](https://fluxcd.io/docs/components/notification/providers/)
* [Flux CLI](https://fluxcd.io/docs/cmd/flux/)
* [Kubernetes kubectl Reference](https://kubernetes.io/docs/reference/kubectl/overview/)
* [Slack API Documentation](https://api.slack.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/6f4f2854-e5a5-4f3e-8910-85c47c018029/lesson/dced4ec0-5ccc-4a5b-8603-b9cf5d737de4)


# DEMO Webhook Receiver

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Notification-Controller/DEMO-Webhook-Receiver/page

This tutorial explains using FluxCD’s Notification Controller to trigger on-demand reconciliation of a GitRepository resource via GitHub webhooks.

In this tutorial, we’ll walk through how to use FluxCD’s Notification Controller Receiver API to trigger on-demand reconciliation of a `GitRepository` resource via GitHub webhooks. By the end, you’ll reduce your GitOps feedback loop from minutes to seconds.

## 1. Setup & Scaling the Deployment

First, switch to the `2-demo` branch and inspect the existing pod:

```bash theme={null}
git checkout 2-demo
kubectl -n 2-demo get pods
```

Example output:

```plaintext theme={null}
NAME                               READY   STATUS    RESTARTS   AGE
block-buster-75f77549b-cjixm       1/1     Running   3          23h
```

### 1.1 Scale the Deployment

Edit the `block-buster` Deployment manifest to increase replicas from 1 to 2:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: block-buster
  namespace: 2-demo
spec:
  replicas: 2                      # was 1
  selector:
    matchLabels:
      app: block-buster
  template:
    metadata:
      labels:
        app: block-buster
        api: downward
        usage: global
    spec:
      containers:
        - name: block-buster
          image: your-image:7.2.0
```

Save, commit, and watch the new pods spin up:

```bash theme={null}
git add .
git commit -m "Scale block-buster to 2 replicas"
kubectl -n 2-demo get pods -w
```

By default, Flux polls the Git repository every minute. The `GitRepository` in `flux-system` might look like this:

```yaml theme={null}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: 2-demo-source-git-bb-app
  namespace: flux-system
spec:
  interval: 1m0s
  ref:
    branch: 2-demo
  url: https://github.com/sidd-harth-2/bb-app-source
```

Verify Flux polling status:

```bash theme={null}
flux get sources git 2-demo-source-git-bb-app -w
```

## 2. Introducing Webhooks for Immediate Reconciliation

Waiting for the static `interval` isn’t always ideal. FluxCD’s Notification Controller lets you trigger reconciliation on demand via webhooks. The high-level workflow is:

| Step | Action                                                    |
| ---- | --------------------------------------------------------- |
| 1    | Expose Notification Controller as a service               |
| 2    | Create a Kubernetes Secret with your GitHub webhook token |
| 3    | Generate a Receiver CR listening for `ping` and `push`    |
| 4    | Configure the GitHub webhook with payload URL and secret  |
| 5    | Push a commit and watch Flux reconcile immediately        |

### 2.1 Expose Notification Controller

Expose the `notification-controller` as a NodePort service:

```bash theme={null}
kubectl -n flux-system expose deployment notification-controller \
  --name receiver \
  --port 80 \
  --target-port 9292 \
  --type NodePort
```

Confirm the service is up:

```bash theme={null}
kubectl -n flux-system get svc receiver
```

Example:

```plaintext theme={null}
NAME      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
receiver  NodePort    10.107.229.12   <none>        80:30547/TCP     8s
```

### 2.2 Create the GitHub Webhook Secret

Generate a Kubernetes secret in `flux-system`. The token must match the “Secret” configured in GitHub:

```bash theme={null}
kubectl -n flux-system create secret generic github-webhook-token \
  --from-literal=token='secret-token-dont-share'
```

> **lightbulb** Keep your webhook token secure. Never commit it to a public repo.

### 2.3 Create a Flux Receiver

Use `flux` CLI to create a Receiver CR that listens for `ping` and `push` events:

```bash theme={null}
flux create receiver github-webhook-receiver \
  --type github \
  --event ping,push \
  --secret-ref github-webhook-token \
  --resource GitRepository/2-demo-source-git-bb-app \
  --export > github-webhook-receiver.yml
```

That generates:

```yaml theme={null}
apiVersion: notification.toolkit.fluxcd.io/v1beta2
kind: Receiver
metadata:
  name: github-webhook-receiver
  namespace: flux-system
spec:
  type: github
  events:
    - ping
    - push
  resources:
    - kind: GitRepository
      name: 2-demo-source-git-bb-app
  secretRef:
    name: github-webhook-token
```

Apply and push:

```bash theme={null}
git add github-webhook-receiver.yml
git commit -m "Add GitHub webhook receiver"
git push
flux reconcile source git flux-system
```

Check the Receiver status:

```bash theme={null}
flux get receivers
```

Example:

```plaintext theme={null}
NAME                       SUSPENDED   READY   MESSAGE
github-webhook-receiver    False       True    Receiver initialized for path: /hook/ab09b3ac...
```

Copy the webhook path (`/hook/ab09b3ac...`) for GitHub configuration.

### 2.4 Configure GitHub Webhook

In your GitHub repo’s **Settings → Webhooks → Add webhook**, set:

* **Payload URL**: `https://<your-host>/hook/<receiver-path>`
* **Content type**: `application/json`
* **Secret**: your `github-webhook-token`

> **lightbulb** Select only the **push** (and optionally **ping**) event to avoid unnecessary traffic.

If testing on a local cluster, you can expose your service via `localtunnel`:

```bash theme={null}
npx localtunnel --port 30547
