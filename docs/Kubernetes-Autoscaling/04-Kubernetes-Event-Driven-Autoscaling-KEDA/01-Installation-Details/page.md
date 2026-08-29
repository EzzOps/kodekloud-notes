# sample output
NAME                                  READY   STATUS      RESTARTS   AGE
flask-web-app-5d9dbb9d44-spjm         0/1     Init:0/1    0          4s
flask-web-app-78689f449c-kq8xs        1/1     Running     0          12m
```

<Frame>
  <img alt="A split-screen image: the left side is a slide titled &#x22;Kubernetes Autoscaling&#x22; listing options (Manual Scaling, HPA, VPA, CPA, KEDA), and the right side shows a bearded man in a purple &#x22;KodeKloud&#x22; shirt speaking into a microphone." />
</Frame>

Horizontal Pod Autoscaler (HPA)
The HPA automates replica scaling based on observed metrics. In this course you'll learn:

* The HPA control loop and how it queries metrics providers.
* Native HPA using resource metrics (CPU/memory) via `metrics-server`.
* Custom and external metrics via adapters (Prometheus Adapter, custom metrics API).
* Installation requirements and debugging steps (how to verify metrics, HPA events, and controller behavior).

<Frame>
  <img alt="A presentation slide titled &#x22;HPA Architecture Framework&#x22; showing CPU and Memory icons inside a rounded box labeled &#x22;Traditional/Native HPA.&#x22; A small circular video thumbnail of a presenter appears in the bottom-right corner." />
</Frame>

Vertical Pod Autoscaler (VPA)
VPA focuses on right-sizing pods by providing resource recommendations and (optionally) updating pod resource requests. Key points covered:

* VPA architecture and how it samples resource usage over time.
* `updateMode` behavior: `Off` (recommendations only), `Auto` (apply), `Initial` (set only at pod creation).
* Resource policies for fine-grained control per container.

Example VPA manifest:

```yaml theme={null}
---
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: flask-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  updatePolicy:
    updateMode: "Off"
  resourcePolicy:
    containerPolicies:
      # Add container-specific policies as needed, for example:
      # - containerName: "flask-container"
      #   mode: "Auto"
```

VPA is most useful when you need to increase per-pod resources (CPU/memory) rather than changing replica counts — for example, stateful workloads or pods where vertical tuning yields better performance.

Cluster Proportional Autoscaler (CPA)
CPA scales controller replicas (such as controllers for DaemonSets or infrastructure components) proportionally to the cluster — by node count or aggregate CPU. Labs include ladder configurations and demonstrate how CPA handles priorities and preemption.

Example ladder configuration (YAML containing JSON for the ladder payload):

```yaml theme={null}
data:
  ladder: |-
    {
      "coresToReplicas": [],
      "nodesToReplicas": [],
      "includeUnschedulableNodes": false
    }
```

KEDA — Kubernetes Event-Driven Autoscaling
KEDA integrates with Kubernetes to enable autoscaling from external event sources and schedulers. You’ll build demos that trigger scaling from Redis queues, cron schedules, and other event sources using KEDA scalers.

<Frame>
  <img alt="A presentation slide titled &#x22;KEDA – Introduction&#x22; showing the KEDA logo above three feature cards labeled &#x22;Event-driven Autoscaler,&#x22; &#x22;External events, volume based,&#x22; and &#x22;Kubernetes-native integration.&#x22; A small circular webcam overlay with a speaker appears in the lower-right corner." />
</Frame>

Each section blends theory with practical labs so you can design, deploy, and operate advanced autoscaling strategies in real clusters. Labs are intentionally hands-on to encourage experimentation, troubleshooting, and learning from mistakes.

Community and next steps
Join the KodeKloud community to ask questions, share discoveries, and collaborate with other learners — community engagement accelerates learning and deepens practical understanding.

Now that the course outline is set, proceed to the first lab to practice manual scaling and get comfortable with `kubectl` workflows.

Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Horizontal Pod Autoscaler (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
* [Vertical Pod Autoscaler (VPA)](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler)
* [Cluster Proportional Autoscaler (CPA) — autoscaler repo](https://github.com/kubernetes/autoscaler)
* [KEDA documentation](https://keda.sh/docs/)
* [metrics-server](https://github.com/kubernetes-sigs/metrics-server)
* [Prometheus Adapter (custom/external metrics)](https://github.com/kubernetes-sigs/prometheus-adapter)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/13b7ea01-bb9e-497b-a190-aafcddaa3f11/lesson/a0518bc3-09b2-441b-bf02-7718e42a327a)


# Installation Details

Source: https://notes.kodekloud.com/docs/Kubernetes-Autoscaling/Kubernetes-Event-Driven-Autoscaling-KEDA/Installation-Details/page

Explains installing KEDA with Helm, what Kubernetes resources the chart creates, verification commands, RBAC considerations, and troubleshooting tips.

Welcome.

This lesson describes the KEDA installation flow you'll run through and what the Helm chart will create in your Kubernetes cluster. KEDA (Kubernetes Event-driven Autoscaling) is commonly installed with Helm — a package manager for Kubernetes that packages resources as charts to make complex installations repeatable. KEDA maintains its official Helm charts on GitHub, so you can pull a supported configuration and install reliably.

<Frame>
  <img alt="A slide titled &#x22;KEDA Installation&#x22; showing the KEDA logo on the left and the Helm logo on the right connected by a dashed arrow. Below them is the URL https://kedacore.github.io/charts." />
</Frame>

Why use Helm for KEDA

* Helm packages KEDA's CRDs, Deployments, ServiceAccounts, Roles/ClusterRoles, and more in a single chart.
* The chart automates resource ordering (CRDs first), RBAC binding, and lifecycle hooks so KEDA components are installed and configured correctly.

Core components the Helm chart installs and why they matter

* CustomResourceDefinitions (CRDs)\
  CRDs extend the Kubernetes API so KEDA can introduce custom objects such as ScaledObjects, ScaledJobs, TriggerAuthentication, and ClusterTriggerAuthentication. These let you declare KEDA scaling behavior alongside standard Kubernetes manifests.
* APIService / Metrics API Server\
  The Metrics API Server exposes external metrics under `external.metrics.k8s.io`, enabling HPAs and other consumers to read KEDA-provided metrics.
* Deployments\
  KEDA's operator, the Metrics API Server, and the Admission Webhook are deployed as standard Kubernetes Deployments. These controllers implement the logic to observe event sources and act on scaling decisions.
* ServiceAccounts\
  ServiceAccounts define the identity KEDA components use when interacting with the Kubernetes API.
* ClusterRoles and ClusterRoleBindings\
  Cluster-wide permissions are declared via ClusterRoles and bound to ServiceAccounts with ClusterRoleBindings.
* Roles and RoleBindings\
  Roles and RoleBindings grant namespace-scoped permissions and can reference ClusterRoles to restrict cluster-level capabilities to a particular namespace.

<Frame>
  <img alt="A slide titled &#x22;Keda Components&#x22; showing six labeled vertical panels (Custom Resource Definitions, API Service, Cluster Roles & Role Bindings, Deployments, Service Accounts, Role Bindings) with brief descriptions of each. It outlines the core Kubernetes resources and permissions used to integrate and run KEDA." />
</Frame>

Quick reference table — resources installed and how to check them

|                           Resource | Purpose                                                    | Example command to inspect                    |                                |
| ---------------------------------: | ---------------------------------------------------------- | --------------------------------------------- | ------------------------------ |
|                               CRDs | Define KEDA custom objects (ScaledObject, ScaledJob, etc.) | \`kubectl get crds                            | grep keda\`                    |
|                        Deployments | Run KEDA operator, metrics-server, admission webhook       | `kubectl get deploy -n <namespace>`           |                                |
|                    ServiceAccounts | Identity for KEDA components                               | `kubectl get sa -n <namespace>`               |                                |
| ClusterRoles / ClusterRoleBindings | Cluster-wide permissions for KEDA                          | \`kubectl get clusterrole                     | grep keda\`                    |
|               Roles / RoleBindings | Namespace-scoped permissions                               | `kubectl get role,rolebinding -n <namespace>` |                                |
|                         APIService | External metrics surface (`external.metrics.k8s.io`)       | \`kubectl get apiservice                      | grep external.metrics.k8s.io\` |

Important notes on RBAC and RoleBindings

> **lightbulb** RoleBindings can reference ClusterRoles. This is useful when you want to grant cluster-level permissions but restrict the effect to a specific namespace by creating a RoleBinding in that namespace that references a ClusterRole.

> **warning** Installing KEDA's CRDs and cluster-level resources requires cluster-wide permissions (for example, `cluster-admin` or equivalent). Ensure you run Helm with an account that has the necessary RBAC privileges.

Typical Helm installation flow (high level)

* Add the KEDA Helm repository and update:

```bash theme={null}
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
```

* Install the KEDA chart. Example (creates namespace if needed):

```bash theme={null}
helm install <release-name> kedacore/keda --namespace keda --create-namespace
```

* The chart will:
  * Create KEDA CRDs (ScaledObjects, ScaledJobs, TriggerAuthentication, ClusterTriggerAuthentication, etc.).
  * Deploy the KEDA operator, Metrics API Server, and Admission Webhook.
  * Create ServiceAccounts and bind Roles/ClusterRoles and RoleBindings/ClusterRoleBindings.
  * Register an APIService to surface metrics under `external.metrics.k8s.io`.

Verification checklist — commands to confirm installation

* Verify CRDs exist:

```bash theme={null}
kubectl get crds | grep keda
```

* Check KEDA deployments in the namespace (example uses `keda`):

```bash theme={null}
kubectl get deploy -n keda
```

* Confirm ServiceAccounts, Roles, and RoleBindings:

```bash theme={null}
kubectl get sa,role,rolebinding,clusterrole,clusterrolebinding -n keda
```

* Verify the external metrics API service is present:

```bash theme={null}
kubectl get apiservice | grep external.metrics.k8s.io
```

* Inspect the operator logs if a pod is not ready:

```bash theme={null}
kubectl logs -n keda deploy/keda-operator
```

Best practices and troubleshooting tips

* Install CRDs before resources that depend on them. The official Helm chart handles this, but manual installs should respect ordering.
* Use a dedicated namespace (for example, `keda`) to scope visibility and RoleBindings.
* If HPAs cannot see external metrics, ensure the `APIService` for `external.metrics.k8s.io` is `Available` and that RBAC rules allow the Metrics API Server to list/ get the resources it needs.
* For upgrades, follow Helm upgrade best practices and watch for CRD changes — some CRD updates require manual steps.

Summary
Installing KEDA with Helm creates a small set of cluster and namespace resources (CRDs, deployments, ServiceAccounts, Roles, RoleBindings, and an APIService) that allow KEDA to observe external event sources, expose metrics via the external metrics API, and drive scaling through HPAs and the KEDA operator. Use the verification commands above to confirm a successful installation and to troubleshoot common issues.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/c218f836-7d7e-425b-a8b7-0148914eb040/lesson/2274b91d-9b99-4611-8d83-86efd2ed3f77)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-autoscaling/module/c218f836-7d7e-425b-a8b7-0148914eb040/lesson/a6803172-1a10-4637-a1ff-0019932958e2)
