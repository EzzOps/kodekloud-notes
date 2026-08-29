# Canary Deployment

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Canary-Deployment/page

Explains canary deployment and Argo Rollouts for incremental, monitored traffic shifts to validate and safely release new application versions.

This guide explains the Canary deployment strategy and how Argo Rollouts implements it for safer, incremental releases.

A canary deployment releases a new application version to a small subset of users or traffic, validates behavior, and then gradually increases exposure until the new version replaces the old one. Running the new version alongside the stable version and shifting only a fraction of live traffic at each step reduces risk and helps detect regressions or performance issues early.

Typical canary flow:

* Deploy the new version alongside the stable version.
* Route a small percentage (for example 5–10%) of traffic to the canary.
* Monitor metrics and optionally run automated analysis.
* If metrics look good, increase canary traffic in steps (for example: 25%, 50%) with observation pauses between steps.
* If an issue is detected, rollback by routing traffic back to the stable version.

Scenario
Imagine you manage a critical backend API consumed by mobile and web clients. Production currently runs version 1.0.0 (100% traffic). You want to release 1.1.0 with performance improvements and a new feature, but a faulty rollout could impact all users. You choose a canary rollout to validate 1.1.0 on a small subset of real traffic before promoting it to 100%.

Example Argo Rollout manifest
Below is a multi-step canary Rollout manifest. It sets traffic weights, adds a manual pause, runs an automated analysis (for example Prometheus queries checking error rates), and includes a longer pause under heavier load.

```yaml theme={null}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: web-api-rollout
spec:
  replicas: 10
  selector:
    matchLabels:
      app: web-api
  template:
    metadata:
      labels:
        app: web-api
    spec:
      containers:
        - name: web-api-container
          # This is the new version being rolled out as the canary.
          image: my-repo/web-api:1.1.0
          ports:
            - containerPort: 8080
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: {}
        - setWeight: 25
        - analysis:
            templates:
              - templateName: check-api-error-rate
                args:
                  - name: service-name
                    value: web-api-canary-svc
        - setWeight: 50
        - pause: { duration: 5m }
      # Services that the Rollout controller will manipulate to split traffic
      canaryService: web-api-canary-svc
      stableService: web-api-stable-svc
```

How the rollout steps work

* `setWeight: 10` — Start by sending 10% of traffic to the canary (version 1.1.0).
* `pause: {}` — Manual pause requiring human approval; useful for dashboards and smoke checks with real traffic.
* `setWeight: 25` — Increase traffic to 25%.
* `analysis` — Run automated analysis (e.g., Prometheus queries) using a predefined analysis template named `check-api-error-rate`. If the analysis fails, the rollout can be aborted and traffic reverted.
* `setWeight: 50` — Increase traffic to 50% if checks pass.
* `pause: { duration: 5m }` — Let the canary run under heavier load to detect slow-developing issues such as memory leaks or downstream timeouts.

> **warning** Manual pauses require a human decision. Ensure monitoring dashboards and
  alerting are available during these pauses so reviewers can approve or abort
  the rollout quickly.

Traffic routing and services
Argo Rollouts manages traffic by switching the backing endpoints for two services you specify:

* stableService (web-api-stable-svc) points to the older ReplicaSet (v1.0.0).
* canaryService (web-api-canary-svc) points to the new ReplicaSet (v1.1.0).

Traffic splitting is achieved by how the ingress/traffic router distributes requests between those services. The exact mechanism depends on your environment and can include:

* Ingress controller annotations ([Kubernetes Ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/))
* Service mesh integrations (e.g., Istio)
* External load balancer/traffic manager configurations

Blue/Green vs Canary
Blue/Green and Canary are both strategies to reduce deployment risk, but they target different trade-offs.

<Frame>
  <img
    alt="A presentation slide titled &#x22;Blue/Green vs Canary Deployment&#x22; showing a
two-column comparison table of deployment features. It lists and contrasts
items like primary goal, environment, traffic split, rollback, complexity,
feedback loop, risk reduction, resource usage, and best-use cases for each
approach."
  />
</Frame>

Key differences:

* Primary goal: Blue/Green focuses on a fast, zero-downtime switch; Canary focuses on gradually exposing changes to reduce risk.
* Environment: Blue/Green uses two full environments (Blue and Green); Canary uses one environment with a subset of new instances.
* Traffic split: Blue/Green performs an immediate switch; Canary increments traffic gradually (e.g., 5% → 25% → 50% → 100%).
* Rollback: Blue/Green switches back to the previous environment instantly; Canary reduces canary weight to 0% to revert traffic.
* Complexity & resources: Blue/Green is simpler operationally but more resource-intensive. Canary requires more routing and analysis logic but is more resource-efficient initially.
* Feedback: Blue/Green validates before the final switch; Canary provides continuous real-time feedback from a subset of users during rollout.

Comparison table (quick reference)

| Aspect         | Blue/Green                             | Canary                                   |
| -------------- | -------------------------------------- | ---------------------------------------- |
| Primary goal   | Instant, zero-downtime switch          | Gradual exposure to reduce risk          |
| Environment    | Two complete environments              | Single environment, subset of instances  |
| Traffic change | Immediate switch                       | Incremental traffic shifts               |
| Rollback       | Instant switch back                    | Reduce canary weight to 0%               |
| Complexity     | Lower (but resource heavy)             | Higher (routing + analysis)              |
| Resource usage | High (duplicate environments)          | Lower at start                           |
| Best for       | Major releases with staging validation | Continuous delivery, risk-averse changes |

Progressive delivery
Progressive delivery is an umbrella strategy that incrementally exposes changes while minimizing risk through automated validations and feature control. It combines canary rollouts with complementary techniques like feature flags, A/B testing, and traffic mirroring.

<Frame>
  <img
    alt="The image is a presentation slide titled &#x22;Progressive Delivery&#x22; showing four
blue rounded boxes labeled &#x22;Canary Deployment,&#x22; &#x22;Feature Flags,&#x22; &#x22;A/B
Testing,&#x22; and &#x22;Traffic Mirroring,&#x22; each with a simple icon. It appears to
summarize deployment
strategies."
  />
</Frame>

> **lightbulb** Progressive delivery techniques include canaries (gradual traffic shifts),
  feature flags (runtime toggles), A/B testing (compare variants), and traffic
  mirroring (shadow production traffic for safe performance testing).

Progressive delivery options and use cases:

* Canary deployments: Incremental traffic shifts with monitoring and automated analysis.
* Feature flags: Turn features on/off at runtime without redeploying; ideal for fine-grained rollouts and immediate rollback.
* A/B testing: Split traffic to collect behavioral and performance data for data-driven decisions.
* Traffic mirroring (shadowing): Send a copy of production traffic to a test instance so you can validate under real load without affecting users.

By combining these techniques you can:

* Reduce blast radius for new releases
* Rapidly iterate while maintaining safety
* Gather meaningful production feedback before a full rollout

Links and references

* Argo Rollouts: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)
* Prometheus: [https://prometheus.io/](https://prometheus.io/)
* Kubernetes Ingress controllers: [https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
* Feature flag patterns: [https://martinfowler.com/articles/feature-toggles.html](https://martinfowler.com/articles/feature-toggles.html)

Recommended next steps

* Add an automated analysis template (Prometheus or external) to the Rollout manifest to validate key SLOs.
* Configure alerting and dashboards for manual pause decisions.
* Integrate a service mesh or ingress traffic manager if you need advanced traffic splitting features.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/3f8098c7-49b5-4299-a369-c478f74f02de)
