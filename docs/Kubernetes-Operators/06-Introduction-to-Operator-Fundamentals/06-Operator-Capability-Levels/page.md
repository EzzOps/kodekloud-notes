# Operator Capability Levels

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Introduction-to-Operator-Fundamentals/Operator-Capability-Levels/page

Explains the five-level capability ladder for Kubernetes operators and how to match operator features to production needs.

[OperatorHub](https://operatorhub.io) lists hundreds of operators. At a glance many look the same: similar names, similar READMEs, and similar install instructions. Behind that surface, however, functionality (and production-readiness) varies widely — and GitHub stars or last-commit dates won't reliably tell you which is which.

The Operator Framework formalized this into a five-level capability ladder. Every operator on [OperatorHub](https://operatorhub.io) declares its level on its page, so check that before you click install.

<Frame>
  <img alt="The image shows a comparison of three operators labeled &#x22;operator-a,&#x22; &#x22;operator-b,&#x22; and &#x22;operator-c&#x22; with similar ratings and installation options, but different functionalities such as &#x22;failover,&#x22; &#x22;backups,&#x22; &#x22;upgrades,&#x22; and &#x22;happy-path install only.&#x22;" />
</Frame>

An operator that only handles a “happy-path” install is a very different beast from one that implements failover, backups, and zero-downtime upgrades. The capability-level badge on an operator’s OperatorHub page is a quick indicator of the operator’s scope and production-readiness.

<Frame>
  <img alt="The image shows a heading &#x22;A Level You Can Read off the Page&#x22; with a badge labeled &#x22;postgres-operator&#x22; indicating &#x22;Capability L3.&#x22; It includes links to resources like &#x22;OperatorHub,&#x22; &#x22;README,&#x22; and &#x22;install.&#x22;" />
</Frame>

If you’ve read about self-driving cars, the ladder metaphor will be familiar: five graded rungs where each step adds more automation and responsibility.

<Frame>
  <img alt="The image is a diagram illustrating the levels of self-driving car automation, ranging from driver assist to full self-driving, represented on a diagonal line with increasing levels of automation." />
</Frame>

Use the ladder to match an operator’s capabilities to your workload’s needs — higher levels are not always better for every use case. Below is a concise summary, followed by details on each level.

| Level   | Primary capabilities                                                                     | When to choose                                                                             |
| ------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Level 1 | Install and configure from a Custom Resource (CR); reconcile basic manifests             | Simple web apps, stateless workloads, or when you only need automated manifest application |
| Level 2 | Seamless upgrades, CRD version conversion support                                        | When operators will be upgraded over time and state migrations are required                |
| Level 3 | Full lifecycle: backups, restores, failure recovery, finalizers, leader election         | Stateful workloads where data safety and automated recovery matter (databases, queues)     |
| Level 4 | Observability: Prometheus metrics, structured events, alerts, detailed status conditions | Production-grade SRE requirements and deep operational insight                             |
| Level 5 | Autopilot: auto-scaling, auto-healing, auto-tuning, anomaly detection                    | Very advanced automation when the operator manages complex, self-adapting systems          |

Level details

Level 1 — Basic install

* The operator installs and configures the workload from a Custom Resource (CR).
* It watches CRs, applies manifests, and ensures pods come up with the spec honored.
* Many simple web-app or CRUD-style operators implemented in a single reconcile loop live here.

Level 2 — Seamless upgrades

* The operator upgrades itself and the operand across versions without losing state.
* New CRD versions are served via CRD conversion (conversion webhooks or the CRD conversion API) so older CRs remain readable.
* Users typically install a newer operator bundle (for example via the `Operator Lifecycle Manager (OLM)` or by applying manifests with `kubectl`) and the operator performs any required migration.

<Frame>
  <img alt="The image illustrates &#x22;Level 2 – Smooth Upgrades,&#x22; showing a migration process from apps/v1 to apps/v2 while maintaining the same state via a conversion webhook, indicating partial automation." />
</Frame>

Conversion webhooks and distribution via `OLM` (see `https://olm.operatorframework.io/`) are common tools to implement Level 2 behavior.

Level 3 — Full lifecycle

* The operator owns backups, restores, failure recovery, and complex reconfiguration.
* It can snapshot, restore, and rebuild failed replicas without manual `kubectl` intervention.
* Finalizers (cleanup logic before resource deletion), leader election, and careful status reporting are essential at this level.

<Frame>
  <img alt="The image illustrates the &#x22;Level 3 – Full Lifecycle&#x22; of a system with features like backups, restores, failure recovery, and reconfiguration, alongside processes like snapshot, restore, and rebuild. It emphasizes conditional automation and mentions recovery without kubectl and cleanup before delete." />
</Frame>

Finalizers, cleanup logic, and clear status conditions/events move an operator from “install-only” to “full lifecycle” ownership.

Level 4 — Deep insights

* The operator emits Prometheus metrics, structured Kubernetes events, alerts, and clear status conditions.
* It explains why a reconcile failed (not just that it failed), enabling SREs to trust it in production.
* Many operators use `controller-runtime` for the reconcile loop and its instrumentation helpers; the metrics endpoint is commonly scraped for observability.

<Frame>
  <img alt="The image displays a dashboard titled &#x22;Level 4 – Deep Insights&#x22; showing metrics, events, alerts, and conditions related to system automation. It alerts a &#x22;Firing&#x22; status and indicates the &#x22;Ready&#x22; condition is false due to an &#x22;ImagePullBackOff&#x22;." />
</Frame>

Level 5 — Autopilot

* Auto-scaling, auto-healing, auto-tuning, and anomaly detection are hallmarks of Autopilot.
* Few operators reach Level 5, and most workloads don't require that degree of automation.
* `cert-manager` ([https://cert-manager.io/](https://cert-manager.io/)) is an example of a mature operator that is production-ready without being a Level 5 Autopilot database operator — showing that a higher level is not always necessary.

<Frame>
  <img alt="The image illustrates &#x22;Level 5 – Autopilot&#x22; in automation, highlighting features like autoscaling, autohealing, autotuning, and anomaly detection, with a note that few operators reach this level." />
</Frame>

What the capability level represents

* The declared capability level reflects scope and responsibilities (what the operator does), not necessarily project maturity, community size, or stability.
* A low-level operator can be useful and appropriate; a high-level operator can introduce risk if it overreaches for your use case.

Two practical takeaways:

* When evaluating an operator outside your team, check its declared capability level on `OperatorHub`. A Level 2 operator managing your production database is often a red flag — you probably want Level 3 or higher for stateful systems.
* When building your own operator, start at Level 1 and add capabilities incrementally. Evolve through the levels as operational requirements (backup, restore, observability, automation) justify the added complexity.

<Callout icon="warning">
  If your workload stores critical data, prefer operators declared as Level 3+ for production use. Level 2 is about upgrade behavior, not full lifecycle management — it may not provide automated recovery or backups.
</Callout>

<Callout icon="lightbulb">
  Build iteratively: implement reliable installs first (Level 1), add upgrade/migration support (Level 2), then introduce backups and recovery (Level 3). Use metrics and events later to reach Level 4.
</Callout>

<Frame>
  <img alt="The image contains two takeaways: checking a declared level (L3) and the red flag of L2 on a production database, illustrated with a level progression graphic featuring a car moving upwards." />
</Frame>

Next up: a short demo deploying `cert-manager`.

Links and references

* `OperatorHub` — [https://operatorhub.io/](https://operatorhub.io/)
* `Operator Lifecycle Manager (OLM)` — [https://olm.operatorframework.io/](https://olm.operatorframework.io/)
* `cert-manager` — [https://cert-manager.io/](https://cert-manager.io/)
* `controller-runtime` — [https://pkg.go.dev/sigs.k8s.io/controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/7d198de7-d651-4c7e-a61d-166023fc1031/lesson/8bcb92e2-cc85-4ecc-9467-7d967f94bf2d" />
</CardGroup>
