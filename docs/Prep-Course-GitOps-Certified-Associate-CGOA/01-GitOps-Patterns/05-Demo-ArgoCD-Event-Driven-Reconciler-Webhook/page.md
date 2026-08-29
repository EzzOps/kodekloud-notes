# create the canary namespace
kubectl create ns canary

# apply the rollout and service manifests
kubectl -n canary apply -f cgoa-demos/patterns/canary/

# confirm resources
kubectl -n canary get all
```

Expected simplified output after apply:

```bash theme={null}
namespace/canary created
rollout.argoproj.io/app-rollout created
service/app-rollout-service created

# kubectl -n canary get all
NAME                                       READY   STATUS    RESTARTS   AGE
pod/app-rollout-76f479c6bf-251rz          1/1     Running   0          8s
... (other app-rollout pods)

NAME                                       TYPE       CLUSTER-IP     PORT(S)
service/app-rollout-service                NodePort   10.109.7.217   80:30797/TCP

NAME                                           DESIRED   CURRENT   READY
replicaset.apps/app-rollout-76f479c6bf         10        10        10
```

<Callout icon="lightbulb">
  Argo Rollouts manages ReplicaSets and pods for `Rollout` resources. You will not see a Kubernetes `Deployment` for this workload — instead look for `rollout.argoproj.io` and ReplicaSets.
</Callout>

## Inspecting Rollouts

List rollouts in the cluster or a specific namespace:

```bash theme={null}
# list rollouts in the current namespace
kubectl get rollouts

# list rollouts in the canary namespace
kubectl get rollouts -n canary
```

Example output:

```bash theme={null}
# kubectl get rollouts -n canary
NAME         DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
app-rollout  10        10        10           10          37s
```

## Accessing the application and observing canary traffic

The `Service` exposes the app on a NodePort (e.g., `30797`). In the demo we continuously polled the `/app` endpoint and printed the reported application version. Use this local script (adjust the port as necessary):

```bash theme={null}
while true; do
  echo -n "$(date '+%H:%M:%S') - ";
  curl -s --max-time 1 http://localhost:30797/app 2>/dev/null |
  awk '{
    if ($0 ~ /Application Version:/) {
      if ($0 ~ /v1/) print "\033[34m" $0 "\033[0m";
      else if ($0 ~ /v2/) print "\033[33m" $0 "\033[0m";
      else print $0;
    } else print $0;
  }';
  sleep 1;
done
```

This output will show mostly `v1` at first, then occasional `v2` responses as the canary begins, then a growing mix of `v2` as the setWeight increases, and finally all `v2` once the rollout completes.

## Promoting a new version (UI or CLI)

To promote a new revision, update the container image to `v2` in the manifest and apply it (or use the UI). The Rollout will create a new revision and follow the configured canary steps:

* A `setWeight: 20` step means 2 of 10 pods will run `v2` while 8 run `v1`.
* If the first step contains `pause: {}`, the rollout will stop for manual promotion.
* On manual promotion, the rollout proceeds to 40%, 60%, 80%, and finally 100% (with configured pauses).

Promote with the kubectl plugin:

```bash theme={null}
# promote to the next step
kubectl argo rollouts promote <rollout-name>

# promote fully (skip intermediate steps)
kubectl argo rollouts promote --full <rollout-name>
```

Make sure the `kubectl-argo-rollouts` plugin is installed if you plan to promote from the CLI. Alternatively, use the Argo Rollouts UI.

<Frame>
  <img alt="The image shows the interface of Argo Rollouts, displaying a canary deployment strategy with various weighted steps and a successful revision summary." />
</Frame>

Example progression (polling output):

```text theme={null}
11:17:45 - Application Version: v1
11:17:48 - Application Version: v2
11:17:51 - Application Version: v2
11:18:04 - Application Version: v1
11:18:14 - Application Version: v2
...
11:19:14 - Application Version: v2
11:19:29 - Application Version: v2
```

As you promote through higher `setWeight` steps, the frequency of `v2` responses increases until all pods serve `v2`.

<Frame>
  <img alt="The image shows an Argo Rollouts dashboard for managing application rollout strategies, specifically using a canary deployment strategy. It displays steps with weight settings, a container selection, and revision details." />
</Frame>

## Rollbacks and stability

Argo Rollouts keeps a revision history and supports rollback to a previous revision if issues are detected during promotion. You can revert using the UI or the CLI to restore a stable revision. The UI highlights stable revisions and current status for easy rollback.

<Frame>
  <img alt="The image shows a software interface for managing application rollouts, displaying steps like setting weights and pauses, with revisions marked as stable or &#x22;No Pods&#x22;." />
</Frame>

## Quick reference

Table: common pause durations and promotion commands

| Topic                | Example                                                    |
| -------------------- | ---------------------------------------------------------- |
| Pause formats        | `yaml<br>pause: { duration: 10s }` or `yaml<br>pause: {} ` |
| Promote to next step | `kubectl argo rollouts promote <rollout-name>`             |
| Promote fully        | `kubectl argo rollouts promote --full <rollout-name>`      |

Summary of best practices

* Use `setWeight` steps to route a specific percentage of traffic to a new revision.
* Combine timed pauses (e.g., `10s`, `1m`) with indefinite pauses (`{}`) for manual verification.
* Observe application metrics and logs during each pause before promoting.
* Use the Argo Rollouts UI or `kubectl-argo-rollouts` plugin to promote, inspect, and roll back as needed.

<Callout icon="lightbulb">
  Ensure Argo Rollouts CRDs and controller are installed in your cluster and install the `kubectl-argo-rollouts` plugin if you intend to promote or inspect rollouts from the CLI. See the Argo Rollouts installation guide for details.
</Callout>

## Links and references

* Argo Rollouts documentation: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)
* kubectl-argo-rollouts plugin installation: [https://argoproj.github.io/argo-rollouts/installation/#kubectl-plugin](https://argoproj.github.io/argo-rollouts/installation/#kubectl-plugin)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

That's all for now.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/6f3f1da1-beae-47f1-aab1-80bd01295229" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/6853933e-4532-4fc2-9e48-3fb5c05ba5d7" />
</CardGroup>


# Demo ArgoCD Event Driven Reconciler Webhook

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Demo-ArgoCD-Event-Driven-Reconciler-Webhook/page

Demonstrates configuring and using Argo CD webhooks for event driven GitOps reconciliation, including webhook setup, TLS caveats, demo environment, and monitoring application sync.

This lesson demonstrates an event-driven GitOps workflow using Argo CD webhooks. Instead of relying on periodic polling, Argo CD can accept webhook events (for example, Git push events) and start reconciling immediately when a change is pushed to a repository.

Argo CD supports Git webhook notifications from major providers, including Gitea. The webhook endpoint on the Argo CD server is `/api/webhook`.

<Frame>
  <img alt="The image shows a webpage from the Argo CD documentation, detailing the configuration of Git webhooks. It includes an overview, instructions, and navigation links." />
</Frame>

## Webhook configuration checklist

When creating a webhook for Argo CD, configure the provider with these minimum settings:

* Payload URL: Argo CD server + `/api/webhook` (for example, `http://host.docker.internal/api/webhook`)
* HTTP method: `POST`
* Content-Type: `application/json`
* Optional: secret for payload signing (validate on Argo CD side)
* Trigger events: typically `push` (or whatever events correspond to your workflow)
* Optional: branch and/or path filters to avoid unnecessary deliveries

<Frame>
  <img alt="The image shows a Git Webhook configuration page on a website, detailing settings for adding a webhook, including fields for Payload URL, Content type, and event triggers." />
</Frame>

| Field          | Recommended value                  | Notes                                                                  |
| -------------- | ---------------------------------- | ---------------------------------------------------------------------- |
| Payload URL    | `http://<ARGOCD_HOST>/api/webhook` | Use the reachable host/port for your environment (see examples below). |
| HTTP method    | `POST`                             | Required by Argo CD webhook receiver.                                  |
| Content-Type   | `application/json`                 | Argo CD expects JSON payloads.                                         |
| Trigger events | `push` (or repo-specific events)   | Filter to only relevant events to reduce noise.                        |
| Secret         | Optional                           | Use payload signing if you require validation.                         |

Links and references:

* Argo CD Webhook docs: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Gitea: [https://gitea.io/](https://gitea.io/)

## Dealing with self-signed TLS in demo environments

If your Argo CD server uses a self-signed certificate, some Git hosting services (including Gitea) may not deliver webhooks to it. For local labs and demos a common workaround is to run the Argo CD server in insecure mode (disable TLS) so the webhook endpoint is reachable over HTTP.

<Callout icon="warning">
  Setting `server.insecure: "true"` disables TLS on the Argo CD server. This is insecure and should only be used for local testing or demos — do not use this in production.
</Callout>

To enable insecure mode, edit the Argo CD CLI parameters ConfigMap and add `server.insecure: "true"`:

```bash theme={null}
kubectl edit configmap argocd-cmd-params-cm -n argocd
```

Add (or update) the `data` section:

```yaml theme={null}
data:
  server.insecure: "true"
```

Restart the Argo CD server deployment to apply the flag:

```bash theme={null}
kubectl -n argocd rollout restart deployment argocd-server
```

Verify pod status while the server restarts:

```bash theme={null}
kubectl -n argocd get pods
```

Example (abridged) output:

```bash theme={null}
NAME                                         READY   STATUS    RESTARTS   AGE
argocd-application-controller-0              1/1     Running   0          38m
argocd-repo-server-74c7b5889-7dgp            1/1     Running   0          84m
argocd-server-669b680cb-vndv4                1/1     Running   0          84m
argocd-server-75bf58bd-hclm8                 0/1     Running   0          5s
```

After the restart, the Argo CD UI will be accessible over plain HTTP in this insecure/demo configuration.

<Frame>
  <img alt="The image shows a UI from Argo CD displaying the status of a Kubernetes application called &#x22;highway-animation,&#x22; which is healthy and synced. The visual representation includes services and deployments with their current statuses." />
</Frame>

## Example: webhook target URL in a Docker-based demo

In the demo environment, `host.docker.internal` was used so the Gitea container (running on the host) could reach the Argo CD server. Example webhook target:

`http://host.docker.internal/api/webhook`

Adjust host and port to match your environment (for example, `http://argocd.example.com/api/webhook`).

Configure the webhook with:

* HTTP method: `POST`
* Content type: `application/json`
* Trigger events: `push` (or other relevant events)
* Optional: branch filter (e.g. `main`) to restrict triggers

<Frame>
  <img alt="The image shows a screenshot of the Argo CD application interface with a context menu open for copying. It displays application details such as sync status and creation time." />
</Frame>

After adding the webhook in Gitea (or your Git provider), use the provider’s “test delivery” feature to verify connectivity. A successful delivery returns HTTP 200 from Argo CD.

When Argo CD accepts the webhook and the application is configured with an automated sync policy, Argo CD will immediately reconcile the application to the desired state. You can monitor the application dashboard to watch the reconciliation and status changes.

<Frame>
  <img alt="The image shows a web interface for setting up a webhook in a repository, with fields for Target URL, HTTP Method, and options for triggering events." />
</Frame>

## Watch the reconciliation in Kubernetes

Monitor pods in the application namespace while you trigger a change:

```bash theme={null}
kubectl -n highway-animation get pods
