# Check cert-manager components
kubectl -n cert-manager get deploy cert-manager cert-manager-webhook cert-manager-cainjector

# Check Prometheus Operator deployment
kubectl -n monitoring get deploy prometheus-operator

# Create the shared namespace for application-facing resources
kubectl create namespace combined
```

Example output:

```bash theme={null}
$ kubectl -n cert-manager get deploy cert-manager cert-manager-webhook cert-manager-cainjector
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager            1/1     1            1           2m13s
cert-manager-webhook    1/1     1            1           2m13s
cert-manager-cainjector 1/1     1            1           2m13s

$ kubectl -n monitoring get deploy prometheus-operator
NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
prometheus-operator  1/1     1            1           2m5s
```

Both sets of application-facing custom resources will live in the `combined` namespace while their controllers continue to run in separate operator namespaces.

## cert-manager resources (Issuer + Certificate)

Inspect the cert-manager resources: an Issuer (who signs) and a Certificate (what certificate is requested and which Secret should receive it). The Certificate in this lesson targets the Secret `web-tls` in namespace `combined`.

<Frame>
  <img alt="The image shows a Visual Studio Code interface with an open folder containing files like &#x22;cert-resources.yaml&#x22; and &#x22;prometheus-resources.yaml.&#x22; The main area displays the VS Code welcome logo with shortcut tips." />
</Frame>

cert-resources.yaml:

```yaml theme={null}
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned
  namespace: combined
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: web-tls
  namespace: combined
spec:
  secretName: web-tls
  dnsNames:
    - apps.kodekloud.com
  issuerRef:
    name: selfsigned
    kind: Issuer
```

Apply the resources and wait for the Certificate to become Ready. The Ready condition means cert-manager has issued the certificate and populated the Secret.

```bash theme={null}
kubectl apply -f cert-resources.yaml
kubectl -n combined wait --for=condition=Ready certificate/web-tls --timeout=180s
```

Example output:

```text theme={null}
certificate.cert-manager.io/web-tls condition met
```

Verify the Secret type is `kubernetes.io/tls`, the standard type used by applications for TLS secrets:

```bash theme={null}
kubectl -n combined get secret web-tls -o jsonpath='{.type}{"\n"}'
```

Example output:

```text theme={null}
kubernetes.io/tls
```

## Prometheus resources (Deployment, Service, ServiceMonitor, Prometheus)

Next, create the monitoring resources that the Prometheus Operator will reconcile. This example includes:

* a small example Deployment that exports metrics,
* a Service exposing the metrics port,
* a ServiceMonitor that discovers the Service,
* a Prometheus custom resource that selects ServiceMonitors via labels.

prometheus-resources.yaml:

```yaml theme={null}
# Deployment for example-app (exports metrics)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-app
  namespace: combined
  labels:
    app: example-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: example-app
  template:
    metadata:
      labels:
        app: example-app
    spec:
      containers:
      - name: app
        image: prom/node-exporter
        ports:
        - name: metrics
          containerPort: 9100
---
# Service exposing the metrics port for the Deployment
apiVersion: v1
kind: Service
metadata:
  name: example-app
  namespace: combined
spec:
  selector:
    app: example-app
  ports:
  - name: metrics
    port: 9100
    targetPort: metrics
---
# ServiceMonitor that targets the Service by label
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: example-app
  namespace: combined
  labels:
    team: combined
spec:
  selector:
    matchLabels:
      app: example-app
  endpoints:
    - port: metrics
---
# Prometheus custom resource that selects ServiceMonitors by label
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: combined
  namespace: combined
spec:
  serviceAccountName: prometheus
  replicas: 1
  serviceMonitorSelector:
    matchLabels:
      team: combined
```

Apply the Prometheus resources:

```bash theme={null}
kubectl apply -f prometheus-resources.yaml
```

Example apply output:

```bash theme={null}
deployment.apps/example-app created
service/example-app created
serviceaccount/prometheus created
clusterrole.rbac.authorization.k8s.io/prometheus-combined created
clusterrolebinding.rbac.authorization.k8s.io/prometheus-combined created
servicemonitor.monitoring.coreos.com/example-app created
prometheus.monitoring.coreos.com/combined created
```

The Prometheus Operator reconciles the Prometheus CR and will create the actual Prometheus StatefulSet. The generated StatefulSet name may vary by operator version; this example expects `prometheus-combined`.

```bash theme={null}
kubectl -n combined rollout status statefulset/prometheus-combined --timeout=300s
```

If the operator generated a differently named StatefulSet, find it with:

```bash theme={null}
kubectl -n combined get statefulset
```

## Quick reference: resources created in `combined` namespace

| Resource Type   | Purpose                                   | Example resource/name                             |
| --------------- | ----------------------------------------- | ------------------------------------------------- |
| Issuer          | Signs certificates                        | `Issuer/selfsigned`                               |
| Certificate     | Requests TLS certificate into a Secret    | `Certificate/web-tls`                             |
| Secret          | TLS secret produced by cert-manager       | `Secret/web-tls` (type `kubernetes.io/tls`)       |
| Deployment      | Example app that exposes metrics          | `Deployment/example-app`                          |
| Service         | Exposes metrics port for scraping         | `Service/example-app`                             |
| ServiceMonitor  | Service discovery for Prometheus          | `ServiceMonitor/example-app`                      |
| Prometheus (CR) | Operator-managed Prometheus configuration | `Prometheus/combined`                             |
| StatefulSet     | Operator-generated Prometheus instance    | `StatefulSet/prometheus-combined` (name may vary) |

## Validate operator ownership and selector match

List and inspect resources in the `combined` namespace to confirm both workflows coexist without ownership overlap:

* cert-manager produced `web-tls` Secret from the Certificate request.
* Prometheus Operator generated the Prometheus StatefulSet and included the ServiceMonitor in its scrape targets.

Finally, verify the label selector match between the Prometheus resource and the ServiceMonitor. Both values should be `combined` so the ServiceMonitor is included in Prometheus' configuration:

```bash theme={null}
# Get the serviceMonitorSelector label value from the Prometheus CR
kubectl -n combined get prometheus combined -o jsonpath='{.spec.serviceMonitorSelector.matchLabels.team}{"\n"}'

# Get the label value from the ServiceMonitor
kubectl -n combined get servicemonitor example-app -o jsonpath='{.metadata.labels.team}{"\n"}'
```

Expected output:

```text theme={null}
combined
combined
```

When these match, the Prometheus Operator includes the ServiceMonitor target in Prometheus' generated scrape configuration.

## Summary

You now have two operators performing different responsibilities within the same namespace:

* cert-manager issued a certificate and wrote a `kubernetes.io/tls` Secret for application consumption.
* Prometheus Operator generated the Prometheus StatefulSet and configured scraping via the ServiceMonitor you created.

Running multiple operators side-by-side is a common pattern; namespaces are convenient observation boundaries but do not change CR ownership. For more details see the operator projects:

* [cert-manager documentation](https://cert-manager.io/docs/)
* [Prometheus Operator documentation](https://prometheus-operator.dev/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/b5e6237b-c98e-4357-b26a-f18c583af395/lesson/27b5fb3a-47d5-4240-8c0e-d0bb2eae96b8)


# Prometheus Operator

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Consuming-Popular-Operators/Prometheus-Operator/page

Describes how the Prometheus Operator automates Prometheus on Kubernetes using CRDs like ServiceMonitor PodMonitor and PrometheusRule to manage configuration, selectors, ownership, and reconciliation

Prometheus is the de facto monitoring engine for collecting metrics and evaluating alerting rules in cloud-native environments. Running Prometheus effectively on Kubernetes requires more than a single container: you must provision the server, choose durable storage, wire up scrape targets, load recording and alerting rules, and keep configuration synchronized with cluster resources.

<Frame>
  <img alt="The image describes Prometheus as a monitoring engine, highlighting tasks like creating the server, choosing storage, wiring scrape targets, loading alerting rules, and keeping configuration in sync." />
</Frame>

The Prometheus Operator automates these operational tasks using Kubernetes-native, declarative resources and a controller that continuously reconciles the desired state into a running Prometheus instance.

<Frame>
  <img alt="The image depicts a flowchart titled &#x22;A Monitoring Assembly Line,&#x22; illustrating how application and platform teams contribute to creating a final Prometheus configuration through an operator." />
</Frame>

Conceptually, think of the operator as a monitoring assembly line:

* Application teams express what should be monitored (monitoring intent).
* Platform teams define Prometheus instances that will do the scraping and alerting.
* The operator composes those inputs into a final Prometheus runtime configuration (prometheus.yml, StatefulSets, Services, ConfigMaps, Secrets) and keeps them in sync.

Instead of manually editing a central prometheus.yml, you work with custom resources (CRDs) such as Prometheus, ServiceMonitor, PodMonitor, and PrometheusRule. Each custom resource declares desired behavior and ownership; the controller implements that desired state by creating and updating the underlying Kubernetes objects.

<Frame>
  <img alt="The image describes how custom resources, such as Prometheus, ServiceMonitor, PodMonitor, and PrometheusRule, can replace manual edits of prometheus.yml for tasks like scraping and alerting." />
</Frame>

## Key custom resources (CRDs)

| Resource       | Purpose                                                                                                       | Example / Notes                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Prometheus     | Describes a Prometheus server instance and drives creation of StatefulSet, Services, ConfigMaps, and Secrets. | Controls which monitors and rules are selected via selectors.                  |
| ServiceMonitor | Selects Services and tells Prometheus which endpoints to scrape.                                              | Useful when metrics are exposed via Services. See example below.               |
| PodMonitor     | Selects Pods directly — ideal when applications expose metrics on pod endpoints instead of Service endpoints. | Alternative to ServiceMonitor for pod-level scraping.                          |
| PrometheusRule | Holds recording and alerting rules for Prometheus.                                                            | Recording rules precompute series; alerting rules send alerts to Alertmanager. |

## Example: ServiceMonitor

A ServiceMonitor lets application teams publish monitoring intent as Kubernetes objects. The operator discovers matching ServiceMonitors and includes them in the generated Prometheus configuration.

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-service-monitor
spec:
  selector:
    matchLabels:
      app: api
  endpoints:
    - port: metrics
      path: /metrics
```

## Example: Prometheus resource with selectors

Platform teams use the Prometheus CR to define a Prometheus instance and scope which monitoring objects it ingests. Use label selectors to enforce clear ownership boundaries across teams.

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: payments-prometheus
spec:
  serviceMonitorSelector:
    matchLabels:
      team: payments
  ruleSelector:
    matchLabels:
      team: payments
```

A ServiceMonitor owned by the payments team would include the corresponding label:

```yaml theme={null}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-service-monitor
  labels:
    team: payments
spec:
  selector:
    matchLabels:
      app: api
  endpoints:
    - port: metrics
      path: /metrics
```

This label-selector pattern enables platform and application teams to collaborate without giving direct write access to a shared Prometheus config file. The operator composes those independent resources into a coherent Prometheus runtime configuration.

## How selectors and ownership work

A Prometheus resource uses selectors to determine which ServiceMonitors, PodMonitors, and PrometheusRules belong to it. This model supports multi-tenant or shared clusters by scoping ingestion to labeled resources:

* Platform teams create one or more Prometheus instances and configure selectors.
* Application teams label their ServiceMonitors/PodMonitors/PrometheusRules to indicate ownership.
* The operator discovers matching objects and includes them in the generated Prometheus configuration.

Use consistent label conventions (for example, `team: payments`) to make ownership and intent explicit across your organization.

## Operator responsibilities and reconciliation

The Prometheus Operator handles lifecycle details that are error-prone when done manually:

* When selected ServiceMonitors or PrometheusRules change, the operator regenerates the Prometheus configuration and triggers a reload.
* When the Prometheus custom resource changes, the operator updates the managed StatefulSet and related resources so the running server matches the desired state.
* The controller continuously reconciles discrepancies (drift) instead of relying on manual reloads or human memory.

<Frame>
  <img alt="The image illustrates a process where changes in monitors, rules, and Prometheus resources lead to generated config updates and StatefulSet adjustments, highlighting reconciliation handling drift." />
</Frame>

## Deployment patterns and ecosystem

In production clusters, the Prometheus Operator is frequently installed as part of a broader monitoring stack (for example, using Helm charts) that includes:

* Prometheus servers
* Alertmanager
* Grafana
* Prometheus exporters
* Dashboards and default alerting rules

After installation, cluster resources (ServiceMonitors, PodMonitors, PrometheusRules) are the primary extension points teams use to customize monitoring behavior for their applications.

> **lightbulb** Selectors in the Prometheus resource control which monitoring objects a Prometheus instance will ingest. Use labels and selectors to enforce clear ownership boundaries in shared clusters.

## Links and references

* Prometheus Operator (GitHub): [https://github.com/prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
* Prometheus documentation: [https://prometheus.io/docs/introduction/overview/](https://prometheus.io/docs/introduction/overview/)
* Alertmanager: [https://prometheus.io/docs/alerting/latest/alertmanager/](https://prometheus.io/docs/alerting/latest/alertmanager/)
* Helm charts and packaging: [https://helm.sh/](https://helm.sh/)
* Kubernetes concepts (labels & selectors): [https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)

You will deploy Prometheus through the operator, create a monitored target, and use a ServiceMonitor to connect it to the Prometheus instance.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-operators/module/b5e6237b-c98e-4357-b26a-f18c583af395/lesson/3e771024-889a-41f8-b990-bdbdcea51ec4)
