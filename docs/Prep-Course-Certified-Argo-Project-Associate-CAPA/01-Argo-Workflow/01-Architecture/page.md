# Architecture

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Workflow/Architecture/page

Overview of Argo Workflows architecture on Kubernetes, detailing control and execution planes, components, integrations with external systems, and workflow lifecycle for secure scalable deployments

This article explains the Argo Workflows architecture: how Argo runs on Kubernetes, how the control and execution planes are separated, and how Argo integrates with external systems (artifact stores, identity providers, monitoring, etc.). Understanding these components and their interactions helps you design secure, scalable workflow deployments on Kubernetes.

At a high level there are two logical planes:

* Control plane (Argo namespace) — components that manage and orchestrate workflows.
* Execution plane (user namespaces) — where the workflow tasks run as Kubernetes pods.

Below are the key components and how they interact.

## Argo namespace (control plane)

* Argo Server: exposes the Argo REST API and the web UI. Users and CLIs interact with Argo Server; it's commonly fronted by a LoadBalancer or Ingress for external access. For high availability, Argo Server can be deployed with multiple replicas.
  * Docs: [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)
* Workflow Controller: the reconciliation engine that watches Workflow custom resources (CRs), advances their state, and creates or updates Kubernetes resources (Pods, ConfigMaps, Secrets, etc.) to execute workflow steps. The controller runs in the Argo namespace and requires RBAC permissions via its ServiceAccount to operate cluster resources.

## User namespace (execution plane)

* Workflow Pods: when the controller schedules work, it creates pods in a target namespace (commonly one namespace per workflow or per tenant). These pods run containers that perform each workflow step. Large or parallel workflows generally produce multiple pods (often one per step). Pod lifecycle is managed by the Kubernetes control plane (kube-scheduler, kubelet, etc.).

## Kubernetes API (cluster interactions)

* Argo components (controller, server, agents) interact with the Kubernetes API server to create and manage resources such as Pods, Services, ConfigMaps, Secrets, and PersistentVolumeClaims.
* Access is governed by Kubernetes RBAC and the ServiceAccounts assigned to Argo components.

## User interaction paths

Users and systems submit and manage workflows through several interfaces. Below is a quick reference.

| Interface                 | Use case                                                                       | Link                                                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| argo CLI                  | Submit, manage, and inspect workflows from the terminal                        | [https://argoproj.github.io/argo-workflows/cli\_installation/](https://argoproj.github.io/argo-workflows/cli_installation/)            |
| kubectl                   | Interact with Workflow CRs directly using standard Kubernetes tooling          | [https://kubernetes.io/docs/reference/kubectl/](https://kubernetes.io/docs/reference/kubectl/)                                         |
| Web UI                    | Visualize and manage workflows in a browser                                    | [https://argoproj.github.io/argo-workflows/](https://argoproj.github.io/argo-workflows/)                                               |
| API clients / SDKs        | Automate workflow submission and retrieval programmatically (e.g., Python SDK) | [https://github.com/argoproj/argo-workflows/tree/master/sdk/python](https://github.com/argoproj/argo-workflows/tree/master/sdk/python) |
| Webhooks / Event triggers | Event-driven workflow triggers via Argo Events or custom webhook integrations  | [https://argoproj.github.io/argo-events/](https://argoproj.github.io/argo-events/)                                                     |

## External integrations

Argo workflows typically rely on external systems for storage, authentication, and observability. Common integration patterns:

| Integration                    | Purpose                                                                 | Examples                                  |
| ------------------------------ | ----------------------------------------------------------------------- | ----------------------------------------- |
| Artifact stores                | Persist workflow inputs/outputs (artifacts)                             | Amazon S3, Google Cloud Storage, MinIO    |
| Workflow archiving             | Archive workflow metadata, logs, and history for retention and auditing | MySQL, PostgreSQL, S3-compatible backends |
| Authentication / Authorization | Delegate user authentication and map identities to RBAC                 | OAuth/OIDC providers (OpenID Connect)     |
| Monitoring / Metrics           | Emit metrics for scraping and alerting                                  | Prometheus + Grafana                      |

Links and references:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Argo Workflows](https://argoproj.github.io/argo-workflows/)
* [Argo Events](https://argoproj.github.io/argo-events/)
* [Prometheus](https://prometheus.io/)

## Lifecycle summary

1. A user submits a Workflow to the Argo Server (via argo CLI, UI, or API).
2. The Workflow Controller detects the new Workflow CR and starts reconciling its state.
3. The controller creates the necessary Kubernetes pods in the chosen namespace to execute each step defined in the Workflow spec.
4. Pods read inputs and write outputs to configured artifact stores; the controller observes pod status and advances the workflow accordingly.
5. After completion, workflow metadata and logs can be archived to a database or object store and metrics emitted for monitoring and alerting.

<Frame>
  <img alt="A high-level architecture diagram of Argo Workflows on a Kubernetes cluster. It shows users and CLIs interacting with an Argo server/load balancer and workflow controller, workflow pods running in namespaces, and external services like artifact storage, OAuth provider, and monitoring." />
</Frame>

> **lightbulb** Note: The Workflow Controller reconciles Workflow CRs and must have the ServiceAccount RBAC permissions to create and manage the resources your workflows require (pods, configmaps, secrets, pvc, etc.). Verify Role/ClusterRole bindings for multi-namespace or cluster-scoped workflows.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/44223b5d-ccc3-4dcb-8292-66036e2ea023/lesson/2b1fcf85-c045-4af3-bb2c-5172dcfec048)
