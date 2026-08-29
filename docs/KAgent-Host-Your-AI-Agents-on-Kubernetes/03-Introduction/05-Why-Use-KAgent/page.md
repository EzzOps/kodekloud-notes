# change spec.selector.version: v1 -> v2
```

Verify:

```bash theme={null}
kubectl get endpoints -n default
curl http://localhost:30081
```

After the fix the Service endpoints are populated and the curl returns the application page (or the pod's default page if using an nginx image).

Root cause: label/selector mismatch (`version=v1` vs `version=v2`) between the Service and the Deployment pods.

***

## Task 2 — HPA not reaching minReplicas in `backend-apps`

Scenario: An HPA is configured for `inventory-service` with:

* CPU target: 80%
* `minReplicas: 3`
* `maxReplicas: 10`

Steps to investigate:

1. Inspect HPA and pods:

```bash theme={null}
kubectl get hpa -n backend-apps
kubectl get pods -n backend-apps
```

Example HPA output:

```text theme={null}
NAME                   REFERENCE                       TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
inventory-service      Deployment/inventory-service    cpu: 0%/80%     3         10        3          22m
```

But pods show only 1 replica running.

2. Describe the HPA to view events/conditions:

```bash theme={null}
kubectl describe hpa -n backend-apps
```

You may see events like:

```text theme={null}
Warning  FailedGetResourceMetric      failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
Warning  FailedComputeMetricsReplicas invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value
```

3. Check cluster metrics availability:

```bash theme={null}
kubectl top nodes
```

If `kubectl top nodes` returns values, node metrics server is responding. HPA CPU/resource metrics may still be affected if Pods' metrics are missing or metrics-server has issues.

4. Inspect namespace events for pod creation failures:

```bash theme={null}
kubectl get events -n backend-apps --sort-by='.lastTimestamp'
```

Look for events such as `Pod ... Forbidden: exceeded quota` or `FailedScheduling`.

5. Check ResourceQuota in the namespace:

```bash theme={null}
kubectl get resourcequota -n backend-apps
```

Example output:

```text theme={null}
NAME               REQUEST                                                        AGE   LIMIT
compute-quota      pods: 1/1, requests.cpu: 100m/2, requests.memory: 128Mi/2903Mi    25m   limits.cpu: 200m/2, limits.memory: 256Mi/2903Mi
```

Here the namespace quota limits pods to `1/1`, preventing the HPA from creating the `minReplicas=3`.

Fix:

* Update the ResourceQuota to allow more pods (for example `pods: 10`) or adjust quota to match expected application scale.

```bash theme={null}
kubectl edit resourcequota compute-quota -n backend-apps
# change pods: 1 to pods: 10 (or apply an updated manifest)
kubectl rollout restart deployment inventory-service -n backend-apps
```

* After increasing the quota, the cluster can create additional pods and the HPA should converge to the desired replicas.

Verify:

```bash theme={null}
kubectl get pods -n backend-apps
kubectl get events -n backend-apps --sort-by='.lastTimestamp'
kubectl describe hpa -n backend-apps
```

Important diagnosis notes:

* The HPA warnings about metrics indicate a metrics failure path that should be investigated (metrics-server, kubelet metrics, scraping), but the immediate blocker preventing scale-up was the `ResourceQuota` restricting pods to 1. Always correlate events + quotas + metrics to determine the decisive cause.

> **warning** Do not increase namespace quotas indiscriminately in production. Align quota changes with capacity planning and organizational policies. If unsure, request approval or test changes in a non-production environment first.

***

## Manual troubleshooting summary

| Issue                               |                                               Evidence | Fix                                                                     |
| ----------------------------------- | -----------------------------------------------------: | ----------------------------------------------------------------------- |
| `order-api` Service no endpoints    |     Service selector `version=v1` vs pods `version=v2` | Patch Service selector to `v2` or reconcile Deployment labels           |
| `inventory-service` HPA not scaling | HPA shows metric errors; events show `pods: 1/1` quota | Increase namespace `ResourceQuota` pods limit and re-rollout deployment |

Troubleshooting tip: Combine `kubectl get/describe`, events, metrics (`kubectl top`), and namespace quotas to build the causal chain.

***

## KAgent: AI-powered Kubernetes troubleshooting

KAgent exposes a chat-style UI and executes a defined toolset (get resources, describe, get YAML, apply manifests, etc.). When given a natural language prompt such as:

"Why isn't the service `order-api` in namespace `default` routing?"

the agent runs investigative commands, aggregates the results, and sends them to an LLM for analysis. The agent can iterate (requesting additional data) until it provides a prioritized diagnosis and actionable remediation.

Example metadata the agent uses to identify resources:

```json theme={null}
{
  "namespace": "default",
  "resource_name": "order-api",
  "resource_type": "service"
}
```

The agent detects the selector mismatch (`version=v1` vs pods `version=v2`), recommends updating the Service selector to `version=v2`, and can apply that change automatically (via a manifest or `kubectl apply`) and then re-check endpoints.

<Frame>
  <img alt="A screenshot of a chat interface for a Kubernetes agent (kagent/k8s-agent) showing a message that the service &#x22;order-api&#x22; now uses the selector app=order-api, version=v2. The right sidebar lists available k8s tools and agent details while a cursor highlights the selector text." />
</Frame>

KAgent follows a similar investigation for the HPA + `inventory-service`: describe HPA, check events, inspect ReplicaSet/Deployment, and verify ResourceQuota. It produces a prioritized list of causes (metrics-server issues vs quota) and recommends changing the `ResourceQuota` to allow more pods as the decisive remediation.

<Frame>
  <img alt="A screenshot of a chat-style web UI showing an AI agent response titled &#x22;kagent/k8s-agent&#x22; with troubleshooting steps about a Kubernetes HPA not scaling, and a text input box at the bottom. The right sidebar lists k8s tools/commands while the left shows the chat list." />
</Frame>

Advantages of using KAgent

* Natural language triage: describe the issue in plain English and let the agent gather evidence.
* Faster discovery: consistent, repeatable investigative flow reduces manual rework.
* Evidence surfacing: shows exactly which commands and outputs lead to a conclusion.
* Improved MTTR and operational consistency across teams.

***

## Closing and next steps

In this lesson we:

* Manually diagnosed two common Kubernetes problems: a Service selector mismatch and a namespace `ResourceQuota` preventing HPA scaling.
* Demonstrated how KAgent can automate the same investigative steps and recommend or perform safe remediation.

Next lessons will cover:

* Building custom agents and configuring LLM providers
* Defining a safe toolset and guardrails for automated remediation
* Instrumenting clusters to improve metrics and observability

References and further reading

* [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Horizontal Pod Autoscaler (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
* [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
* [kubectl documentation](https://kubernetes.io/docs/reference/kubectl/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/a2bef22f-2221-4587-9f26-3c0bce28059e/lesson/2af65038-fb0e-44d5-98dd-1c26efb2be50)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/a2bef22f-2221-4587-9f26-3c0bce28059e/lesson/b6b570e7-07e8-4afe-892d-d131158fd249)


# Why Use KAgent

Source: https://notes.kodekloud.com/docs/KAgent-Host-Your-AI-Agents-on-Kubernetes/Introduction/Why-Use-KAgent/page

KAgent is an open source framework for running agentic AI on Kubernetes, offering CRDs, controllers, multi‑LLM support, observability, and GitOps-friendly deployment for DevOps and platform teams.

Hello — welcome to this concise guide to KAgent. This lesson explains what KAgent is, why it exists, and how to apply its capabilities in cloud-native environments. The content is organized for clarity and practical use, stepping through architecture, operational concerns, and real-world scenarios.

KAgent is an open source framework that brings agentic AI to Kubernetes. It targets DevOps and platform teams and integrates naturally into environments that already use Kubernetes primitives and GitOps workflows. KAgent provides Kubernetes-native APIs and controllers, built-in observability, and multi-LLM provider support.

> **lightbulb** KAgent is part of the CNCF Sandbox (accepted April 25). There is both an open source edition and a commercial offering backed by Solo. The stable release as of January 2026 is `v0.7.8`. For community discussion and support, see the project Discord and GitHub repository.

<Frame>
  <img alt="A dark-themed infographic titled &#x22;Cloud Native Sandbox — April 2025&#x22; showing kagent and CNCF logos. Colored boxes highlight topics like Governance, Security, Community Standards and benefits such as enterprise-grade project maturity and a path to incubation." />
</Frame>

KAgent delivers:

* Stable APIs and CRDs (v1alpha1 and v1alpha2).
* A controller implementation that is Kubernetes-native.
* Built-in observability using OpenTelemetry.
* Multi-LLM provider support and easy provider switching.

<Frame>
  <img alt="A release-style poster for &#x22;kagent&#x22; (Cloud Native Sandbox, April 2025) highlighting Version 0.7.8 and the current version v0.7.8+. It also lists features like a stable API, controller implementation, observability and multi-provider LLM support, and shows an OpenTelemetry logo." />
</Frame>

Community and project health:

* GitHub: 1,665+ stars, 331+ forks.
* Contributors: 100+ developers.
* Active Discord community (800+ members) and regular releases/issues management.

Next, we’ll examine where KAgent excels: technical, operational, and use-case perspectives.

## Where KAgent Excels — At a Glance

| Perspective | Key benefits                                                                           | Example / Notes                                                                                  |
| ----------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Technical   | Kubernetes-native, declarative config, multi-LLM support, extensibility, observability | CRDs + controllers, OpenTelemetry tracing, `model` config controls token limits & temperature    |
| Operational | Easy deployment, multiple interfaces, community & governance                           | Helm charts / CLI single-command install, Web UI + APIs, CNCF backing                            |
| Use-case    | Kubernetes ops automation, DevOps CI/CD, multi-agent orchestration                     | Pre-built agents for debugging, chain agents for complex workflows, GitOps-friendly YAML configs |

## Technical advantages

* Kubernetes native: KAgent builds on CRDs, controllers, and supports HPA. It integrates with Kubernetes lifecycles and scales with cluster capacity.
* Declarative, IaC-friendly configuration: Agents are YAML/CRD resources suitable for GitOps (`argocd`, `flux`) and version control.
* Multi-provider LLM support: Out of the box support for providers such as OpenAI, Anthropic, Google Vertex AI, Azure OpenAI, Ollama, etc. Switching providers is usually a single-line change in an agent resource.
* Rich tool ecosystem: Pre-built tools for Kubernetes operations and a standardized tool protocol enable tool interoperability. Agents can also call other agents as tools.
* Observability: Built-in OpenTelemetry tracing lets you connect KAgent to existing tracing/monitoring stacks to visualize agent operations, diagnose failures, and measure latencies.
* Extensibility: Open source design permits adding/removing tools, custom MCP-protocol tools, and fine-grained model-level configuration.
* Production-ready architecture: Stable APIs and a controller-based design allow you to scale KAgent as long as the cluster provides the required CPU/memory/network resources.

<Frame>
  <img alt="A slide titled &#x22;Technical Advantages&#x22; listing seven numbered features (Kubernetes Native; Declarative configuration; Multi-provider LLM support; Rich tool ecosystem; Observability; Extensibility; Production ready), with the multi-provider LLM item highlighted. The lower section expands on multi-provider LLM support, noting major providers (OpenAI, Anthropic, Google, Azure, Ollama) and easy switching between them." />
</Frame>

KAgent supports custom integrations such as AI Gateways and an MCP-style tool protocol to connect external services, Kubernetes APIs, and other agents into reusable tooling libraries.

<Frame>
  <img alt="A slide titled &#x22;Technical Advantages&#x22; showing seven numbered feature boxes (Kubernetes native; declarative configuration; multi-provider LLM support; rich tool ecosystem; observability; extensibility; production ready), with the &#x22;Rich tool ecosystem&#x22; highlighted. Below it is an expanded dark panel listing pre-built tools for Kubernetes, an MCP protocol for tool integration, and that agents can use other agents as tools." />
</Frame>

Observability is first-class via OpenTelemetry, enabling trace collection for agent decisions, tool calls, and LLM interactions to support debugging and performance tuning.

<Frame>
  <img alt="An infographic titled &#x22;Technical Advantages&#x22; showing seven numbered feature boxes (Kubernetes native; declarative configuration; multi‑provider LLM support; rich tool ecosystem; observability; extensibility; production ready). Below is a highlighted Observability section describing OpenTelemetry tracing, monitoring agent operations, and debug/troubleshoot capabilities." />
</Frame>

> **warning** KAgent scales with your cluster. Ensure you provision appropriate CPU, memory, and network resources for agent workloads and LLM calls (e.g., large-context models may increase memory and request rates).

Extensibility and production readiness make KAgent suitable for platform teams that want to expose agent-driven automation across clusters while retaining control via Kubernetes RBAC, network policies, and secrets management.

<Frame>
  <img alt="A presentation slide titled &#x22;Technical Advantages&#x22; showing seven numbered feature boxes (e.g., Kubernetes Native, Declarative configuration, Multi-provider LLM support, Rich tool ecosystem, Observability, Extensibility, Production ready). Below is a larger &#x22;Production Ready&#x22; section with sub-items like Stable API, Controller-based architecture, and Scalable design." />
</Frame>

## Operational advantages

* Easy deployment: Install via Helm charts or the `kagent` CLI. The CLI supports single-command installation and includes pre-configured agent examples to get started fast.
* Multiple interfaces: Interact through a Web UI, CLI, or programmatic APIs for automation and integration.
* Community & governance: CNCF sandbox status, active documentation, and community channels provide guidance, security recommendations, and operational best practices.

<Frame>
  <img alt="A presentation slide titled &#x22;Operational Advantages&#x22; listing four numbered points: Easy deployment, Multiple interfaces, Community support, and CNCF backing. Below is a highlighted &#x22;Easy Deployment&#x22; section with details like Helm charts available, single-command installation, and pre-configured agents." />
</Frame>

## Use-case advantages

KAgent ships with community-maintained pre-built agents focused on Kubernetes operations. These are practical for:

* Debugging and troubleshooting cluster issues.
* Automation for resource management and policy enforcement.
* CI/CD and GitOps integration where agents act on declarative YAML resources.

Multi-agent orchestration is a powerful pattern: run agents in isolation for safety, or chain agents into workflows to handle complex automation tasks and coordinate cross-cutting actions.

<Frame>
  <img alt="A slide titled &#x22;Use Case Advantages&#x22; showing three numbered focus areas: Kubernetes operations, DevOps automation, and multi-agent systems. The lower section expands DevOps automation into CI/CD integration, infrastructure management, and monitoring & alerting." />
</Frame>

## Quick links and references

* KAgent GitHub: [https://github.com/kagent](https://github.com/kagent) (search the project repository for installation and examples)
* CNCF Sandbox: [https://www.cncf.io/sandbox/](https://www.cncf.io/sandbox/)
* GitOps: [https://www.gitops.tech/](https://www.gitops.tech/)
* OpenTelemetry: [https://opentelemetry.io/](https://opentelemetry.io/)
* Major LLM providers: OpenAI, Anthropic, Google Vertex AI, Azure OpenAI, Ollama

Use these links to explore installation guides, example agent CRDs, and community resources.

- [Watch Video](https://learn.kodekloud.com/user/courses/kagents-host-your-ai-agents-on-kubernetes/module/a2bef22f-2221-4587-9f26-3c0bce28059e/lesson/11a92265-50e4-4341-88a7-4e0845fc8d45)
