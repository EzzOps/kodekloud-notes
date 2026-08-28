# Example GitHub Actions job for AKS deployment
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t myregistry.azurecr.io/myapp:${{ github.sha }} .
      - name: Push to ACR
        run: docker push myregistry.azurecr.io/myapp:${{ github.sha }}
      - name: Deploy to AKS
        run: |
          kubectl set image deployment/myapp myapp=myregistry.azurecr.io/myapp:${{ github.sha }}
          kubectl rollout status deployment/myapp
```

<Callout icon="lightbulb">
  Push-based pipelines are straightforward and give you direct control over each deployment step. They work well if you prefer an explicit trigger model.
</Callout>

## Pull-based Workflow (GitOps)

In a **GitOps** (pull-based) model, you store your Kubernetes manifests alongside application code or in a dedicated Git repo. A GitOps operator (Flux, Argo CD) watches the repo and applies changes automatically:

```yaml theme={null}
# Simplified Flux v2 GitRepository resource
apiVersion: source.toolkit.fluxcd.io/v1beta1
kind: GitRepository
metadata:
  name: aks-config
spec:
  interval: 1m
  url: https://github.com/contoso/aks-config
  branch: main
---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta1
kind: Kustomization
metadata:
  name: apps
spec:
  path: ./apps/prod
  prune: true
  sourceRef:
    kind: GitRepository
    name: aks-config
```

<Callout icon="lightbulb">
  GitOps ensures that your cluster’s live state automatically converges with the declared Git state. This model enhances auditability, reversibility, and compliance.
</Callout>

Effective observability is critical for running production workloads on AKS. Azure provides:

* **Azure Monitor for Containers**: Collects metrics, logs, and health data for nodes and pods.
* **Azure Log Analytics**: Enables querying of container logs using Kusto Query Language (KQL).
* **Application Insights**: Offers distributed tracing, exception tracking, and performance monitoring for your applications.

| Feature                        | Purpose                                      | Example Query                   |                                     |
| ------------------------------ | -------------------------------------------- | ------------------------------- | ----------------------------------- |
| Container CPU & Memory Metrics | Track resource utilization                   | \`InsightsMetrics               | where Name == "cpuUsageNanoCores"\` |
| Pod Log Collection             | Aggregate stdout/stderr logs from containers | \`ContainerLog                  | where PodName == "myapp"\`          |
| Distributed Tracing            | Monitor service-to-service calls             | View in Application Insights UI |                                     |

Refer to the following resources for more details:

* [Azure Kubernetes Service Documentation](https://docs.microsoft.com/azure/aks/)
* [Azure Monitor for Containers Overview](https://docs.microsoft.com/azure/azure-monitor/containers/)
* [Getting Started with Flux v2 on AKS](https://fluxcd.io/docs/get-started/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/60e74513-d231-493d-90a3-71787380ae79/lesson/6da6dbba-f38c-49be-9172-ab5c9a9abeaf" />
</CardGroup>


# Choosing the right Container platform on Azure

Source: https://notes.kodekloud.com/docs/Azure-Kubernetes-Service/Close-out/Choosing-the-right-Container-platform-on-Azure/page

Guide to choosing Azure container hosting options and trade-offs between control scalability and operational overhead

We're almost at the end of this module — great work making it this far.

As you start using containers on Azure, a common question arises: is AKS the only option, and is it the right platform for every workload? The short answer: it depends on how much control, flexibility, and operational responsibility your applications require.

Below is a concise guide to the main Azure container hosting options, when to choose each, and the trade-offs to consider.

## When you need full control: AKS, Kubernetes on VMs, Azure Red Hat OpenShift

* AKS, self-managed Kubernetes on VMs, and [Azure Red Hat OpenShift](https://learn.kodekloud.com/user/courses/openshift-4) provide a full Kubernetes/OpenShift cluster experience.
* These options expose cluster APIs so you can install operators and CRDs, run custom controllers, customize networking (custom CNI), and tune ingress, storage, and scheduling.
* Choose these when you require:
  * Fine-grained orchestration control
  * Custom networking or ingress setups
  * Operator-managed software stacks or custom controllers
  * Advanced multi-tenant or hybrid scenarios

<Callout icon="lightbulb">
  AKS supports both Linux and Windows containers via node pools. Windows containers are supported but have platform-specific constraints and fewer features compared to Linux node pools — factor this into planning and architecture decisions.
</Callout>

<Callout icon="warning">
  Self-managed Kubernetes and managed OpenShift (ARO) typically increase operational overhead and may incur additional licensing or management costs. Choose them only when you need the extra flexibility they provide.
</Callout>

## Developer-focused managed platforms

* Azure Container Apps
  * Built on Kubernetes but provides a higher-level, developer-centric experience.
  * The platform manages the underlying cluster; developers work with services, revisions, and DAPR-style service invocation instead of cluster APIs.
  * Built-in autoscaling (KEDA), traffic splitting, and observability make it excellent for microservices where you want rapid delivery with minimal ops.

* Azure Container Instances (ACI)
  * Runs containers as single, isolated instances with strong container-level isolation.
  * No VM or cluster management — ideal for short-lived jobs, burst capacity, or isolated test environments.
  * ACI can be integrated as virtual nodes into AKS for burst scenarios.

* Azure App Service
  * A PaaS for web apps and APIs with platform-managed runtimes or custom container support.
  * Two models: the "code" model (use platform runtime images) and the "container" model (Web App for Containers).
  * Good when you want a platform-managed web host with integrated deployment, authentication, and scaling.

* Azure Functions
  * Event-driven, serverless compute for short-lived or event-triggered code.
  * Supports the Functions programming model, and can be deployed in containers when needed.
  * Use for lightweight, highly event-driven workloads with automatic scale-to-zero and bindings.

## Quick comparison table

| Resource Type                   | Best for                           |                         Access & control |                               Scaling behavior | Typical use cases                                              |
| ------------------------------- | ---------------------------------- | ---------------------------------------: | ---------------------------------------------: | -------------------------------------------------------------- |
| AKS / K8s on VMs / ARO          | Full orchestration control         |        Full cluster API, CRDs, operators | User-defined (cluster autoscaler, HPA, custom) | Complex microservices, operator-driven apps, custom networking |
| Azure Container Apps            | Managed microservices              |      No direct K8s API; platform-managed |                      Built-in KEDA autoscaling | Event-driven microservices, APIs, service-to-service apps      |
| Azure Container Instances (ACI) | Short-lived or isolated containers | Container-level only; no cluster control |          Per-container allocation (fast start) | Jobs, CI/CD tasks, ephemeral testing, burst capacity           |
| Azure App Service               | Managed web apps/APIs              |   Platform runtimes or custom containers |                       Platform-managed scaling | Web apps, APIs, straightforward containerized apps             |
| Azure Functions                 | Event-driven, serverless           |    Function model, can run in containers |                       Automatic, scale-to-zero | Event handlers, cron jobs, serverless APIs                     |

## Decision guidance — pick by workload needs

* If you need maximum control, advanced networking, or operators: choose AKS, ARO, or self-managed Kubernetes.
* If you want Kubernetes benefits without operating a cluster: choose Azure Container Apps.
* For single-container, short-lived tasks or fast-start isolated runs: choose ACI.
* For traditional web apps with minimal infra management: choose App Service (code model or container).
* For event-driven, short-duration logic with minimal ops: choose Azure Functions.

## Useful links and references

* [Kubernetes documentation](https://kubernetes.io/docs/)
* [Azure Kubernetes Service (AKS) documentation](https://learn.microsoft.com/azure/aks/)
* [Azure Container Apps documentation](https://learn.microsoft.com/azure/container-apps/)
* [Azure Container Instances documentation](https://learn.microsoft.com/azure/container-instances/)
* [Azure App Service documentation](https://learn.microsoft.com/azure/app-service/)
* [Azure Functions documentation](https://learn.microsoft.com/azure/azure-functions/)

<Frame>
  <img alt="An infographic that maps Azure container hosting options on two axes — from infrastructure management to serverless and from unopinionated to opinionated containers. It shows examples like Azure Kubernetes Service, Kubernetes on VMs, Azure Red Hat OpenShift, Azure Container Instances and Container Apps, plus Azure App Service and Azure Functions." />
</Frame>

Consider the trade-offs between control and operational overhead, and choose the service that best matches your application's needs for customization, isolation, scaling, and developer experience. Review the links above and test a small proof-of-concept in the chosen platform before committing to it in production.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/azure-kubernetes-service/module/ee946e5f-161f-4c37-acff-b9a805538288/lesson/52ebb1ee-01c4-4468-950f-4cea4ef6852d" />
</CardGroup>
