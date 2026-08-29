# ensure the kubectl argo rollouts plugin is available
kubectl argo rollouts version

# create namespace
kubectl create ns canary

# apply manifests
kubectl -n canary apply -f .

# verify resources
kubectl -n canary get all
kubectl get rollouts -n canary
```

Example outputs (trimmed):

```bash theme={null}
# kubectl argo rollouts version
kubectl-argo-rollouts: v1.8.3+49fa151
BuildDate: 2025-06-04T22:15:54Z
GitCommit: 49fa1516cf71672b69e265267da4e1d16e1fe114
GoVersion: go1.23.9
Platform: linux/amd64

# applying manifests
rollout.argoproj.io/app-rollout created
service/app-rollout-service created

# checking resources
kubectl -n canary get all
NAME                                   READY   STATUS    RESTARTS   AGE
pod/app-rollout-76f479c6bf-251lrz      1/1     Running   0          8s
... (other pods) ...

NAME                         TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
service/app-rollout-service  NodePort   10.109.7.217   <none>        80:30797/TCP    8s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/app-rollout-76f479c6bf      10        10        10      8s
```

Note: a Rollout is not a Deployment. You will see ReplicaSets and Pods, but not a Deployment object when using `kind: Rollout`.

5. Access the application and observe versions

In the example the NodePort is `30797`. Poll the `/app` endpoint to observe which version responds as the canary progresses.

Polling script (bash) — polls every second and prints the version returned:

```bash theme={null}
while true; do
  echo -n "$(date '+%H:%M:%S') - ";
  response=$(curl -s --max-time 1 http://localhost:30797/app 2>/dev/null)
  if [ -z "$response" ]; then
    echo "ERROR: Service unreachable"
  else
    echo "$response"
  fi
  sleep 1
done
```

6. Promote a rollout to the next step

Promote manually either from the Argo Rollouts web UI (click Promote) or from the CLI using the kubectl plugin.

Promote examples:

```bash theme={null}
# Promote the named rollout to the next step (include -n <namespace> if not default)
kubectl argo rollouts promote app-rollout -n canary

# Promote repeatedly until the rollout reaches 100% or update the image to finish the rollout.
```

<Frame>
  <img alt="A screenshot of the Argo Rollouts web UI for an &#x22;app-rollout&#x22; canary deployment, showing a left-hand step timeline with &#x22;Set Weight&#x22; and &#x22;Pause&#x22; steps. The center/right panels display the strategy summary (set vs actual weight), container info, and revision details." />
</Frame>

## What happens during promotion

* If a canary step sets weight to 20% and you have 10 replicas, Argo Rollouts will direct \~2 replicas (20% of 10) to the new ReplicaSet.
* Subsequent promotions increase the percentage according to configured weights (40%, 60%, 80%, etc.).
* Pauses are opportunities to run tests, observe metrics, or require manual approval before advancing.

## Observing traffic during the rollout

* While partially promoted, traffic is split based on weights. Your polling script should show intermittent responses from the new version (e.g., v2) until the rollout reaches 100% and all traffic flows to the new revision.

## Rollback and automation

* Argo Rollouts supports automated analysis and rollbacks via pre/post-promotion analysis templates.
* Combine Rollouts with GitOps (for example, Argo CD) to let manifests in a Git repo drive the rollout state and history.
* See the Argo Rollouts docs for configuring analysis templates and automated rollbacks.

## Quick reference: common commands

| Action               | Command                                               |
| -------------------- | ----------------------------------------------------- |
| Check plugin version | `kubectl argo rollouts version`                       |
| Apply manifests      | `kubectl -n canary apply -f .`                        |
| List rollouts        | `kubectl get rollouts -n canary`                      |
| Promote rollout      | `kubectl argo rollouts promote app-rollout -n canary` |

> **lightbulb** To promote a rollout from the CLI, use: kubectl argo rollouts promote \<rollout-name> -n \<namespace>. If a step is paused indefinitely (pause: ), you must promote it manually.

> **lightbulb** Pause durations must include a time unit suffix (for example "10s", "1m", "1h") or be specified as an empty object (pause: ) to pause indefinitely.

That's it — a compact walkthrough showing how to incrementally release a new application version using Argo Rollouts' Canary strategy.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/c63717a8-f29b-4fb1-9b2c-99f75f589f7d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/c79e939b-1286-4dd6-bafc-352ae31ea295)


# Demo Clarification

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Demo-Clarification/page

Describes how an AnalysisRun succeeded because the AnalysisTemplate checks result.code in the JSON health response instead of the HTTP status.

This lesson explains why the AnalysisRun succeeded even though earlier sessions showed a different health payload. The key point: the AnalysisTemplate evaluates a JSON field inside the health endpoint response (result.code), not the HTTP status code.

The AnalysisRun invoked the health check three times and evaluated the success condition against the JSON payload returned by the service. The metric reads show three values (one per probe):

```text theme={null}
Value Time
[object Object] 12:48:52 AM
[object Object] 12:48:57 AM
[object Object] 12:49:02 AM
Success condition: result.code >= 200 && result.code < 300
```

Because the AnalysisTemplate inspects `result.code`, the content of the JSON body matters. Below are two versions of the health response and the relevant AnalysisTemplate snippet.

Frame the successful (green) version JSON — it includes a numeric `code` field:

<Frame>
  ```json theme={null}
  {
    "code": 200,
    "status": "OK",
    "message": "Highway Animation Server is running",
    "timestamp": 1761386576672
  }
  ```
</Frame>

> **lightbulb** Note: The AnalysisTemplate's success condition checks the JSON payload (for example, `result.code`). It does not evaluate the HTTP response code returned by the server.

Here is the AnalysisTemplate as shown by kubectl (trimmed to the relevant fields). Notice the web provider URL and the same success condition:

```bash theme={null}
$ k -n argo-analysis-lab describe at http-health-check
Name:               http-health-check
Namespace:          argo-analysis-lab
Kind:               AnalysisTemplate
Spec:
  Args:
    Name: service-name
  Metrics:
    Count:    3
    Interval: 5s
    Name:     health-check
    Provider:
      Web:
        Method: GET
        URL: http://{{args.service-name}}.argo-analysis-lab.svc.cluster.local/health
  Success Condition: result.code >= 200 && result.code < 300
```

Contrast that with the older (blue) version of the application whose health endpoint returned a simpler payload without a `code` field:

<Frame>
  ```json theme={null}
  {
    "status": "OK",
    "message": "Highway Animation Server is running"
  }
  ```
</Frame>

> **warning** If the AnalysisRun queries a response that lacks `result.code`, the metric extraction for `result.code` will fail and the success condition cannot be satisfied — even if the HTTP status is 200. Ensure the JSON payload contains the field referenced by your success condition.

Summary — why the AnalysisRun passed

* The AnalysisTemplate success condition is evaluated against the JSON payload returned by the health endpoint (e.g., `result.code`).
* The green version includes the `code` field with a value in the 200–299 range, satisfying the condition.
* The blue version lacks the `code` field, so the same AnalysisTemplate would fail when run against it.

Comparison table

| Aspect                                                        | Green version (passed) | Blue version (would fail) |
| ------------------------------------------------------------- | ---------------------- | ------------------------- |
| JSON payload includes `code`                                  | Yes (`"code": 200`)    | No                        |
| Success condition (`result.code >= 200 && result.code < 300`) | Evaluates to true      | Fails (field missing)     |
| AnalysisRun result                                            | Success                | Failure                   |

Links and references

* [Argo Rollouts — AnalysisOverview](https://argoproj.github.io/argo-rollouts/features/analysis/)
* [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
* Consider using JSONPath or JQ locally to inspect responses: e.g., `curl -s http://svc/health | jq .`

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/1b05b8b7-b043-4ad1-bac3-2a695bbb51db)
