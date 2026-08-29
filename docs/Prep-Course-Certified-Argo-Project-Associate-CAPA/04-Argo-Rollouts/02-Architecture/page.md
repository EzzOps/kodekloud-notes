# Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Architecture/page

Overview of Argo Rollouts architecture and controller-driven canary progressive delivery with traffic splitting, AnalysisRuns, and automated promotion or rollback

Let's examine the Argo Rollouts architecture and how it orchestrates a canary release with progressive delivery best practices.

Argo Rollouts uses a controller-driven model to implement the strategy declared in a Rollout custom resource. When you apply an updated Rollout manifest (for example, with a changed pod template), the rollout controller follows a coordinated set of steps to create, validate, and promote the new version while keeping the previous version available for quick rollback.

High-level sequence performed by the Rollout controller:

* Create a new canary ReplicaSet containing the updated pod template while retaining the existing stable ReplicaSet.
* Coordinate traffic splitting between the stable and canary ReplicaSets by integrating with an ingress controller or service mesh (for example, [NGINX Ingress](https://kubernetes.github.io/ingress-nginx/), [Istio VirtualService](https://istio.io/latest/docs/reference/config/networking/virtual-service/), [SMI](https://smi-spec.io/) traffic split providers, [Linkerd](https://linkerd.io/), or other supported controllers).
* Execute automated analysis by creating an AnalysisRun from an AnalysisTemplate referenced in the Rollout. AnalysisRuns can:
  * Query metrics from providers such as [Prometheus](https://prometheus.io/), [Datadog](https://www.datadoghq.com/), or other metric backends.
  * Launch Kubernetes Jobs to perform custom validation, smoke tests, or synthetic checks.
* Evaluate AnalysisRun results and the rollout strategy (weights, pauses, promotion rules). Based on the decision logic, the controller will either:
  * Progress the canary by increasing traffic weights until it becomes the stable ReplicaSet, or
  * Roll back to the previous stable ReplicaSet if the analysis indicates a failure.

This controller-driven approach enables safe, automated progressive delivery by combining gradual traffic shifts with objective, metric-driven analysis and automated decision-making.

| Component                      |                                                                                                 Role | Typical Use Cases                                                    |
| ------------------------------ | ---------------------------------------------------------------------------------------------------: | -------------------------------------------------------------------- |
| Rollout resource               | Declarative spec describing strategy (canary, blue/green), steps, traffic routing, AnalysisTemplates | Define the desired release strategy and thresholds                   |
| Rollout controller             |                                   Reconciles Rollout resources; manages ReplicaSets and AnalysisRuns | Implements the rollout state machine and decision logic              |
| ReplicaSets                    |                                                            Represent stable and canary pod templates | Keep previous version available and run the new version side-by-side |
| Traffic routing integration    |                                                    Adjusts traffic split via Ingress or service mesh | Gradual traffic shift by weight or route manipulation                |
| AnalysisRun / AnalysisTemplate |                              Reusable analysis definitions that fetch metrics or run validation jobs | Gate promotion based on metrics and custom checks                    |
| Decision logic                 |                                                       Evaluates analysis outcomes and strategy rules | Continue rollout, promote canary, or trigger rollback                |

Key behaviors and interactions

* Traffic orchestration: The controller does not itself proxy traffic. Instead, it integrates with a supported provider that performs weighted routing or route patching to direct a percentage of user requests to the canary.
* Automated analysis: AnalysisRuns let you run metric queries (Prometheus, Datadog, etc.) or Jobs to validate application health and user experience before promoting the canary.
* Promotion and rollback: Promotion happens when defined success criteria are met. Rollback is triggered automatically if metrics or tests fail, minimizing user impact.

> **lightbulb** Make sure the cluster has the required CRDs and RBAC configured for Argo Rollouts, and that any external metric providers used by AnalysisTemplates are reachable from the cluster.

> **warning** Traffic routing behavior depends on the integration you choose (Ingress vs. service mesh). Ensure the chosen provider is supported and properly configured before running automated canaries.

Best practices and recommendations

* Start small: Use small initial canary weights and short, monitored increments to limit blast radius.
* Automate validation: Use AnalysisTemplates to codify checks (latency SLOs, error rate thresholds, end-to-end smoke tests).
* Observe and alert: Integrate with observability tooling (Prometheus, Grafana, Datadog) and configure alerts for AnalysisRun failures.
* Validate routing: Test the chosen traffic provider in a non-production environment to confirm that weighted routing behaves as expected.

Links and references

* [Argo Rollouts documentation](https://argoproj.github.io/argo-rollouts/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
* [Istio VirtualService](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
* [Prometheus](https://prometheus.io/)
* [Datadog](https://www.datadoghq.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/871ac10a-5b48-4dc7-923d-7fcffbbed88d)
