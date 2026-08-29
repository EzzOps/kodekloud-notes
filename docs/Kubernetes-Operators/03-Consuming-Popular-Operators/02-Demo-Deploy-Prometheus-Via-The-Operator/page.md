# Demo Deploy Prometheus Via The Operator

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Consuming-Popular-Operators/Demo-Deploy-Prometheus-Via-The-Operator/page

Guide to installing and using the Prometheus Operator to create Prometheus and ServiceMonitor custom resources and let the operator reconcile StatefulSets and scale Prometheus via CRs

In this lesson you will consume the Prometheus Operator like a platform user: install the operator bundle, create Prometheus custom resources (CRs), and let the operator reconcile those CRs into running monitoring workloads. The operator manages the generated StatefulSet and Prometheus configuration for you, so you do not hand-edit StatefulSets or manually reload Prometheus configuration. Instead, you declare intent via CRs (custom resources).

## What you'll learn

* Install the Prometheus Operator bundle (CRDs + controller).
* Create a Prometheus CR and a ServiceMonitor CR that the operator will reconcile.
* Observe how the operator generates and manages the underlying StatefulSet and configuration.
* Scale Prometheus by updating the Prometheus CR (not by editing generated workloads).

## Prerequisites

* kubectl configured to the target cluster
* Network access to fetch the operator bundle
* (Optional) Familiarity with Kubernetes CRDs and RBAC

## Install the Prometheus Operator bundle

Set an environment variable pointing to the operator bundle release, then apply it with server-side apply:

```bash theme={null}
$ printenv PROM_OPERATOR_BUNDLE_URL
https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.87.0/bundle.yaml
$ kubectl apply --server-side -f "$PROM_OPERATOR_BUNDLE_URL"
```

<Callout icon="lightbulb">
  We use `--server-side` because operator bundles often include very large CRD definitions. Server-side apply delegates the final object merge to the Kubernetes API server, avoiding heavy client-side serialization and improving compatibility with large or complex manifests.
</Callout>

The bundle will create CRDs, the operator Deployment, RBAC rules, a ServiceAccount, and other supporting resources. Example server response (trimmed):

```bash theme={null}
customresourcedefinition.apiextensions.k8s.io/prometheuses.monitoring.coreos.com serverside-applied
customresourcedefinition.apiextensions.k8s.io/prometheusrules.monitoring.coreos.com serverside-applied
customresourcedefinition.apiextensions.k8s.io/scrapeconfigs.monitoring.coreos.com serverside-applied
customresourcedefinition.apiextensions.k8s.io/servicemonitors.monitoring.coreos.com serverside-applied
customresourcedefinition.apiextensions.k8s.io/thanosrulers.monitoring.coreos.com serverside-applied
clusterrolebinding.rbac.authorization.k8s.io/prometheus-operator serverside-applied
clusterrole.rbac.authorization.k8s.io/prometheus-operator serverside-applied
deployment.apps/prometheus-operator serverside-applied
serviceaccount/prometheus-operator serverside-applied
```

This installation is platform-admin work: once the controller and CRDs are present, application teams can create Prometheus and ServiceMonitor CRs.

## Wait for the operator to be ready

If you create CRs before the operator controller is running, those CRs will exist in the API but nothing will reconcile them into workloads. Wait for the operator Deployment rollout to complete:

```bash theme={null}
$ kubectl -n default rollout status deploy/prometheus-operator --timeout=180s
deployment "prometheus-operator" successfully rolled out
```

<Callout icon="warning">
  Do not create Prometheus CRs until the operator Deployment is Ready. CRs created while the controller is down will not be reconciled into StatefulSets until the controller is running.
</Callout>

## Key CRDs used

| Resource Type                          | Purpose                                                                                    | Example / Notes                                                      |
| -------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| Prometheus (monitoring.coreos.com)     | Declares a Prometheus server instance (replicas, retention, serviceMonitor selector, etc.) | Selects `ServiceMonitor` objects by label                            |
| ServiceMonitor (monitoring.coreos.com) | Declares scrape targets and endpoints for Prometheus to scrape                             | Labels are used to bind to a Prometheus via `serviceMonitorSelector` |
| Service                                | Network access to an application to be scraped                                             | `ServiceMonitor` selects services by label selector                  |

## Create a Prometheus CR

Inspect and apply a manifest that creates a ServiceAccount, a minimal ClusterRole, and a Prometheus custom resource named `demo`. The Prometheus CR uses a `serviceMonitorSelector` to pick up matching ServiceMonitor objects.

prometheus.yaml:

```yaml theme={null}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prometheus
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus
rules:
  - apiGroups: [""]
    resources: ["nodes", "services", "endpoints", "pods"]
    verbs: ["get", "list", "watch"]
---
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: demo
spec:
  serviceAccountName: prometheus
  replicas: 1
  serviceMonitorSelector:
    matchLabels:
      team: demo
```

Apply the manifest:

```bash theme={null}
$ kubectl apply -f prometheus.yaml
serviceaccount/prometheus created
clusterrole.rbac.authorization.k8s.io/prometheus created
clusterrolebinding.rbac.authorization.k8s.io/prometheus created
prometheus.monitoring.coreos.com/demo created
```

The operator will generate a StatefulSet for this Prometheus instance (for example `prometheus-demo`). Wait for the StatefulSet to be created and become ready:

```bash theme={null}
$ kubectl wait --for=condition=ready sts/prometheus-demo --timeout=120s
$ kubectl rollout status sts/prometheus-demo --timeout=180s
```

Notes:

* The operator generates the StatefulSet and related Pod spec. The Prometheus Pod often includes helper containers such as a config-reloader alongside the Prometheus binary.
* You should not edit generated StatefulSets directly; edit the Prometheus CR and let the operator reconcile changes.

## Create a ServiceMonitor to define scrape targets

A ServiceMonitor describes the endpoints Prometheus should scrape. It uses labels that match the Prometheus `serviceMonitorSelector`, so the operator can wire the scrape configuration automatically.

servicemonitor.yaml:

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: operator-self
  labels:
    team: demo
spec:
  selector:
    matchLabels:
      app.kubernetes.io/component: controller
      app.kubernetes.io/name: prometheus-operator
  endpoints:
    - port: http-metrics
      path: /metrics
      interval: 30s
```

Apply the ServiceMonitor:

```bash theme={null}
$ kubectl apply -f servicemonitor.yaml
servicemonitor.monitoring.coreos.com/operator-self created
```

Verify that the label on the ServiceMonitor matches the Prometheus `serviceMonitorSelector`:

```bash theme={null}
$ kubectl get servicemonitor operator-self -o yaml
$ kubectl get prometheus demo -o yaml
```

They should both contain the same label (for example `team: demo`). That label equality is how the Prometheus instance selects which ServiceMonitors to include in its generated configuration.

## Scale Prometheus by patching the CR

To change the replica count, patch the Prometheus CR. The operator will update the generated StatefulSet to match the desired replica count.

Patch to request two replicas and wait for the StatefulSet rollout:

```bash theme={null}
$ kubectl patch prometheus demo --type=merge -p '{"spec":{"replicas":2}}'
$ kubectl rollout status sts/prometheus-demo --timeout=240s
Waiting for 1 pods to be ready...
statefulset rolling update complete 2 pods at revision prometheus-demo-8674fb6f5c...
```

Confirm desired vs ready replicas:

```bash theme={null}
$ kubectl get sts prometheus-demo -o jsonpath='{.spec.replicas}{" "}{.status.readyReplicas}{"\n"}'
2 2
```

The first number is the desired replica count (spec.replicas). The second number is how many replicas are currently ready (status.readyReplicas). This demonstrates the consumer-side operator pattern: modify the CR and let the operator manage generated workloads.

## Quick checklist

* [ ] Operator bundle applied (CRDs + controller).
* [ ] Operator Deployment rollout completed.
* [ ] Prometheus CR created with `serviceMonitorSelector`.
* [ ] ServiceMonitor created with matching label(s).
* [ ] StatefulSet generated and Pods are ready.
* [ ] Scale or update by patching the Prometheus CR.

## Links and references

* Prometheus Operator releases: [https://github.com/prometheus-operator/prometheus-operator/releases](https://github.com/prometheus-operator/prometheus-operator/releases)
* cert-manager (optional integration): [https://cert-manager.io/docs/](https://cert-manager.io/docs/)
* Kubernetes Concepts: [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)

That covers the Prometheus Operator workflow: install the operator, create Prometheus and ServiceMonitor CRs, and manage your monitoring instance via CRs rather than directly editing generated Kubernetes workloads.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/b5e6237b-c98e-4357-b26a-f18c583af395/lesson/40f0ab25-5020-4911-bef9-afbf09eee9cf" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/kubernetes-operators/module/b5e6237b-c98e-4357-b26a-f18c583af395/lesson/e1c3f4ca-1da2-4085-aa81-40b86e24fe22" />
</CardGroup>
