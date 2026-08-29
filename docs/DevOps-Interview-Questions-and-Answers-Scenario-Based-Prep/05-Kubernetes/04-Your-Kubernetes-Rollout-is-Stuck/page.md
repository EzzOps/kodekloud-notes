# Your Kubernetes Rollout is Stuck

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Kubernetes/Your-Kubernetes-Rollout-is-Stuck/page

Guide to diagnose and safely recover stuck Kubernetes Deployment rollouts by inspecting deployment conditions, pod statuses, events, probes, logs, ReplicaSets and configuration without deleting resources.

Here's a common Kubernetes interview-style debugging scenario.

You deploy a new version of your app with `kubectl apply` and the terminal output looks fine. But when you run `kubectl rollout status`, it hangs:

```bash theme={null}
$ kubectl apply -f deployment.yaml
deployment.apps/myapp configured

$ kubectl rollout status deployment/myapp
Waiting for deployment "myapp" rollout to finish:
2 of 3 updated replicas are available...
