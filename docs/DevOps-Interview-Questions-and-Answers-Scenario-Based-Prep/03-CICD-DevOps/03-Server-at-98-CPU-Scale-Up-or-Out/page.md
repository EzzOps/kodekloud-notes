# quick fix
+ PATCHED=1
```

Example — an inline `kubectl edit` tweak:

```bash theme={null}
$ kubectl edit deployment api
# changed in editor:
replicas: 3 -> 7
image: app:v1.4.2 -> app:v1.4.1
# quick fix
```

From Git's perspective, the manifest still shows:

```yaml theme={null}
kind: Deployment
replicas: 3
image: app:v1.4.2
env: []
```

But the cluster is actually running:

```yaml theme={null}
kind: Deployment
replicas: 7   # drift
image: app:v1.4.1
env:
  - name: PATCHED
    value: "1"
```

Until something breaks, nobody may notice the mismatch.

## Why that matters

Traditional CD pipelines are good at pushing changes, but they don't guarantee the cluster will remain in the declared state over time or that the cluster state will be visible (and auditable) to the whole team.

GitOps flips the direction: instead of pushing desired state into the cluster, the cluster pulls desired state from Git and continuously reconciles itself to match the repo.

<Frame>
  <img alt="The image explains how GitOps pulls the desired state from Git to a cluster using Argo CD to ensure the cluster matches the repository." />
</Frame>

## How GitOps works (in-cluster pull + reconcile)

Install an agent (for example, Argo CD or Flux) inside the cluster. The agent periodically pulls the desired state from Git and asks one question on a loop: Does the cluster match the repo?

* If yes: nothing to do.
* If no: the agent either corrects the cluster to match Git or raises an alert for manual remediation.

This architecture provides a declarative, observable, and auditable system of record.

> **lightbulb** The real power of GitOps is the agent's pull-and-reconcile loop. Treat Git as the single source of truth and let the in-cluster agent enforce that state.

## Key benefits of GitOps

* Drift becomes visible and actionable. Manual changes are either reverted or flagged immediately.
* Rollbacks are simple: revert the commit in Git and the agent will reconcile the cluster back to that state—no special redeploy pipeline needed.
* Auditability and change history live naturally in Git (commit history, PRs, code review).
* Security posture improves because write access to the cluster can be limited while Git remains the edit surface.

## Common anti-patterns and warnings

A frequent mistake is installing Argo CD or Flux but continuing to push changes directly from CI/CD (e.g., Jenkins) into the cluster. That still allows drift and undermines GitOps guarantees.

> **warning** If CI/CD pipelines continue to write directly to the cluster while an in-cluster GitOps agent is active, you can reintroduce drift and break auditability. Make Git the only source of truth for desired state.

## Quick comparison

| Concern             | Traditional CD (push)               | GitOps (pull & reconcile)                        |
| ------------------- | ----------------------------------- | ------------------------------------------------ |
| Who applies changes | CI/CD pipeline pushes via `kubectl` | In-cluster agent (Argo CD, Flux) pulls from Git  |
| Visibility          | Changes may not be reflected in Git | Git is the single source of truth and change log |
| Drift detection     | Often invisible until failure       | Agent detects or remediates drift automatically  |
| Rollback            | Custom pipeline or redeploy         | Revert commit in Git, agent reconciles           |
| Best practice       | CI/CD drives cluster                | Git drives cluster; CI/CD updates Git            |

## Practical advice / best practices

* Make Git the only place to change manifests or Kustomize/Helm inputs. Use pull requests, reviews, and CI checks.
* Use the in-cluster agent for reconciliation; configure it to either auto-sync or require manual approval depending on risk tolerance.
* Limit direct access to the cluster (kubectl, SSH) and route fixes through Git (or have a documented emergency process).
* Integrate image scanners, policy checks (e.g., OPA/Gatekeeper), and CI tests into the PR flow before merging into the desired branch.

## Further reading

* Argo CD: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Flux: [https://fluxcd.io/](https://fluxcd.io/)
* Kubernetes GitOps guide: [https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/)

This is the essence of why GitOps exists: to make cluster state declarative, visible, and self-healing by reversing the deployment flow and giving the cluster an agent that continuously enforces the repository as the single source of truth.

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-interview-prep/module/370000ef-b6bc-4986-8d29-0793ebb2c9e7/lesson/b62cecb6-3dfd-45d6-a858-2916d72a8937)


# Server at 98 CPU Scale Up or Out

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/CICD-DevOps/Server-at-98-CPU-Scale-Up-or-Out/page

Guidance on diagnosing high CPU and choosing between vertical scaling and horizontal autoscaling by making applications stateless and fixing root causes before adding capacity

Let's work through a common DevOps interview scenario.

Your production server just hit 98% CPU during a traffic spike. Your manager says, "Just add more RAM and CPU." Is vertical scaling (scale-up) the right answer?

Short answer: it depends. Many people get this backwards.

## What scale-up (vertical scaling) means — and its drawbacks

Vertical scaling is upgrading a single server (more CPU, RAM, or a bigger VM/instance). It’s easy to understand, but it has three important limitations:

* Hard ceiling: a single machine can only go so far before you hit maximum instance sizes or physical limits.
* Single point of failure: if that one machine fails, the whole service can go down.
* Downtime / disruption: resizing hardware or a VM often requires downtime or causes degraded performance during the change.

## What scale-out (horizontal scaling) means — and common pitfalls

Horizontal scaling is adding more servers (instances) and distributing load across them. It sounds like the safer approach, but it also introduces complexity:

* In-memory sessions can break when a user is routed to a different instance.
* Files written to local disk won’t be available on other instances unless you use shared storage.
* Adding nodes without addressing state, consistency, and orchestration can create new failure modes.

## Quick comparison

| Strategy               |                                                      When to use | Pros                                        | Cons                                                                     |
| ---------------------- | ---------------------------------------------------------------: | ------------------------------------------- | ------------------------------------------------------------------------ |
| Vertical (scale-up)    | Short-term relief, simple apps, or when scale-out is impractical | Fast to implement; no architectural changes | Limited headroom, single point of failure, possible downtime             |
| Horizontal (scale-out) |           Web services, microservices, high-availability systems | Better fault tolerance and capacity growth  | Requires stateless design, shared storage, load balancing, orchestration |

## A practical three-step approach

Rather than reflexively adding CPU, follow this sequence:

1. Diagnose before you scale

* Identify what is actually consuming CPU: a runaway process, a bad SQL query, GC churn, or system bottleneck?
* Scaling hides bugs; it doesn't fix them. If a specific query is monopolizing CPU, adding hardware only delays the problem.

Useful quick command:

```bash theme={null}
$ top
```

Other helpful tools/commands:

* `htop` — interactive process viewer
* `ps -eo pid,cmd,%cpu,%mem --sort=-%cpu | head` — find top CPU consumers
* Database slow query logs and `EXPLAIN` plans
* Application tracing / APM (e.g., Jaeger, Zipkin, Datadog, New Relic)
* OS-level metrics: load average, context switches, I/O wait

2. Make your application stateless

* Move session storage out of process memory into a shared store (for example, Redis or Memcached).
* Use object storage (e.g., AWS S3) or a network file system for uploaded files rather than local disk.
* Ensure any instance can handle any request without relying on local in-memory state.

Best practices:

* Use sticky session avoidance; store auth tokens or session IDs in a shared backend.
* Use object or CDN-backed storage for static assets and user uploads.
* Instrument the app for metrics and tracing to observe cross-instance behavior.

3. Scale horizontally — autoscaling behind a load balancer

* With a stateless application, place instances behind a load balancer and configure autoscaling.
* Example autoscaling policy: add instances when average CPU across the fleet exceeds 70%; scale down when it drops below 30%. Include cooldown windows and max/min instance limits.
* Implement health checks and graceful termination so in-flight requests complete when instances are removed.

Autoscaling checklist:

* Proper health checks (HTTP 200, readiness/liveness endpoints)
* Graceful shutdown handling (SIGTERM → complete current requests)
* Cooldown periods to avoid rapid thrashing
* Limits to prevent runaway provisioning costs

<Frame>
  <img alt="The image illustrates the concepts of making an app stateless by using Redis and S3 for sessions and files, and auto-scaling with a load balancer, which adjusts servers based on CPU usage thresholds." />
</Frame>

A real-world caution: many teams buy bigger instances only to discover the root cause was a single bad SQL query, inefficient algorithm, or a memory leak. Diagnose first; scale second.

> **lightbulb** Scaling can mask defects. Profile and fix underlying issues (queries, memory leaks, hotspots) before increasing capacity.

> **warning** If you must resize or replace a running instance (vertical scaling), plan for potential downtime and test the process in staging. Vertical changes often require service disruption.

## Quick references

* [Kubernetes Concepts — What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Redis: [https://redis.io/](https://redis.io/)
* AWS S3: [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
* Autoscaling and load balancing patterns: [https://aws.amazon.com/autoscaling/](https://aws.amazon.com/autoscaling/) and [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-interview-prep/module/370000ef-b6bc-4986-8d29-0793ebb2c9e7/lesson/e05894ff-3d3e-46d3-a585-048ff0ab07bf)
