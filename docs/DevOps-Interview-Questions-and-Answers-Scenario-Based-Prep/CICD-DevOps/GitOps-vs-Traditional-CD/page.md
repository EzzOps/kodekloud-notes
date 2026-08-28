# GitOps vs Traditional CD

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/CICD-DevOps/GitOps-vs-Traditional-CD/page

Compares traditional push-based CD with GitOps pull-and-reconcile, showing how GitOps prevents cluster drift, improves auditability and rollbacks, and enforces Git as the single source of truth.

A common interview question I love asking:

Why does GitOps even exist? Continuous Deployment (CD) solutions like Jenkins or GitHub Actions have been around for years—haven't we already solved deployment? Understanding the gap between traditional CD and GitOps explains why GitOps matters today.

## The problem with traditional CD

In a typical traditional CD workflow, a pipeline runs `kubectl apply` and pushes manifests into the cluster. You see a green status, close your laptop, and move on:

```bash theme={null}
$ kubectl apply -f deploy.yaml
✓ deployment.apps/api configured
✓ service/api unchanged
```

But clusters are mutable. Someone can SSH into production and make a quick fix, or a teammate might run `kubectl edit` to ramp up replicas during a traffic spike. These manual or ad-hoc changes create "drift": the live cluster no longer matches what's stored in Git.

Example — a quick server-side change:

```bash theme={null}
$ ssh prod
$ vi app.env
