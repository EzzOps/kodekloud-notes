# Version not specified. The latest version of kubetail will be installed.
# Would you like to enable automatic updates? (y/N)
# Summary:
# * The following packages will be installed in your cluster (minikube):
#   1. kubetail (version vX.Y.Z)
# * Automatic updates will be enabled
# Continue? (Y/n)
```

Open the Kubetail UI from Glasskube:

```bash theme={null}
glasskube open kubetail
```

Once opened, Kubetail exposes Kubernetes objects (Deployments, DaemonSets, CronJobs, Pods, etc.) and allows you to stream and filter logs across containers and nodes in real time.

<Frame>
  <img alt="The image shows a web interface displaying Kubernetes resources, including deployments, jobs, pods, and replica sets, with their namespaces and creation times." />
</Frame>

<Frame>
  <img alt="The image is a screenshot of a Kubernetes log viewer, displaying system logs with time stamps, info messages, and network data related to pods. The interface allows filtering based on sources like pods, containers, OS, architecture, and node." />
</Frame>

***

## kube-prometheus-stack: metrics, dashboards, and alerting

The kube-prometheus-stack bundles Prometheus, Alertmanager, Grafana, and several exporters into a pre-configured monitoring solution. It provides:

* Prometheus for metric collection and alerting rules
* Alertmanager for routing/notification
* Grafana with pre-built dashboards
* Exporters such as node-exporter to collect node metrics

This stack is especially useful for Kubernetes cluster-level monitoring and quick setup of observability capabilities.

Package characteristics (kube-prometheus-stack)

| Field        | Value                                                                                       |
| ------------ | ------------------------------------------------------------------------------------------- |
| Scope        | cluster-scoped                                                                              |
| Values       | multiple (customize Prometheus, Alertmanager, Grafana, exporters, storage, retention, etc.) |
| Entrypoint   | yes (Grafana)                                                                               |
| Dependencies | none                                                                                        |

You’ll get many dashboards out of the box:

<Frame>
  <img alt="The image displays a dashboard interface featuring a list of various folders and items related to Kubernetes and other technologies on the left sidebar, and a central panel listing dashboard names with their associated tags." />
</Frame>

Alerting rules are pre-configured and can be managed from the Rules UI:

<Frame>
  <img alt="The image displays an Alert Rules dashboard from a monitoring system, showing various Prometheus rule files with their states such as firing, normal, and recording. The interface includes a navigation sidebar, a search option, and a summary of alert statuses." />
</Frame>

When installing kube-prometheus-stack from Glasskube you can toggle components and fine-tune values. Common toggles include:

* Enable/disable Alertmanager
* Enable/disable Grafana
* Enable node-exporter host network for richer node metrics
* Configure Prometheus retention and storage size

Glasskube exposes these options in the package configuration UI:

<Frame>
  <img alt="The image shows a user interface for configuring the &#x22;kube-prometheus-stack&#x22; package on Glasskube, detailing options for enabling features like Alertmanager and Grafana for Kubernetes monitoring." />
</Frame>

After installation Glasskube will create the `kube-prometheus-stack` namespace and the stack’s pods will begin to initialize. Verify namespace and pod status:

```bash theme={null}
kubectl get namespace
```

Check pods in the monitoring namespace while resources start up:

```bash theme={null}
kubectl get pods -n kube-prometheus-stack
# Example output while pods initialize:
# NAME                                                       READY   STATUS    RESTARTS   AGE
# alertmanager-kube-prometheus-stack-kube-alertmanager-0    0/2     Init:0/1  0          13s
# kube-prometheus-stack-kube-operator-<id>                  1/1     Running   0          20s
# kube-prometheus-stack-grafana-<id>                        0/3     Init:0/1  0          20s
# prometheus-kube-prometheus-stack-kube-prometheus-0        0/2     Init:0/1  0          12s
```

Give pods a minute or two to reach Running. A fully started example:

```bash theme={null}
kubectl get pods -n kube-prometheus-stack
# NAME                                                       READY   STATUS    RESTARTS   AGE
# alertmanager-kube-prometheus-stack-kube-alertmanager-0    2/2     Running   0          89s
# kube-prometheus-stack-kube-operator-<id>                  1/1     Running   0          96s
# kube-prometheus-stack-grafana-<id>                        2/3     Running   0          96s
# prometheus-kube-prometheus-stack-n<id>                    1/1     Running   0          96s
# kube-prometheus-stack-kube-prometheus-0                   2/2     Running   0          88s
```

Glasskube will display the Grafana entrypoint once the service or ingress is ready. When you open Grafana you will be prompted for credentials. The kube-prometheus-stack Helm chart typically stores the Grafana admin username and password in a Kubernetes secret inside the `kube-prometheus-stack` namespace.

To find and decode the Grafana admin credentials:

```bash theme={null}
# list secrets in the namespace and find the Grafana secret name
kubectl get secrets -n kube-prometheus-stack

# once you identify the Grafana secret name (eg. kube-prometheus-stack-grafana or <release>-grafana),
# decode the admin username and password (key names may vary by chart/version):
kubectl get secret <grafana-secret-name> -n kube-prometheus-stack -o jsonpath="{.data.admin-user}" | base64 --decode; echo
kubectl get secret <grafana-secret-name> -n kube-prometheus-stack -o jsonpath="{.data.admin-password}" | base64 --decode; echo
```

<Callout icon="lightbulb">
  Default Grafana credentials for many kube-prometheus-stack installs are:

  * Username: `admin`
  * Password: `prom-operator`
    Always confirm by decoding the actual Kubernetes secret in your cluster (see command above) — some releases or charts may override defaults.
</Callout>

After logging into Grafana, dashboards will populate as Prometheus begins scraping metrics. It may take a few minutes for metrics to appear and for panels to show data.

<Frame>
  <img alt="The image displays a dashboard interface with multiple panels showing metrics for a Kubernetes API server, though many sections indicate &#x22;No data.&#x22;" />
</Frame>

The Rules UI shows alerting rules and their current state (firing, pending, or normal):

<Frame>
  <img alt="The image shows the alert rules dashboard in a monitoring application, displaying a list of alert rules and their statuses, such as &#x22;firing&#x22; and &#x22;normal.&#x22; The interface includes options to create new alert or recording rules." />
</Frame>

Glasskube provides a central packages view for installing and managing both Kubetail and kube-prometheus-stack, plus many other packages:

<Frame>
  <img alt="The image shows a web interface for Glasskube, listing various Kubernetes-related packages available for installation, such as &#x22;akri,&#x22; &#x22;argo-cd,&#x22; and &#x22;gpu-operator.&#x22; The interface provides options to install these packages and has a user-friendly design with a dark theme." />
</Frame>

<Frame>
  <img alt="The image displays a software interface for configuring the &#x22;kube-prometheus-stack&#x22; in Glasskube. Options like enabling Alertmanager, Grafana, and setting Prometheus retention and storage size are visible." />
</Frame>

<Frame>
  <img alt="The image shows a web interface for &#x22;Glasskube&#x22; with a list of software packages related to Kubernetes, each accompanied by an &#x22;Install&#x22; button. There's also a notification about Glasskube Cloud launching, encouraging users to join the waitlist for early access." />
</Frame>

***

## Summary

With Kubetail and kube-prometheus-stack deployed via Glasskube you gain both:

* Real-time log streaming and filtering across pods and containers (Kubetail)
* A full metrics collection, visualization, and alerting platform (Prometheus + Alertmanager + Grafana)

These tools together provide comprehensive observability for Kubernetes clusters, enabling faster troubleshooting and proactive alerting.

Further reading and references:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Prometheus Operator / kube-prometheus](https://github.com/prometheus-operator/kube-prometheus)
* [Grafana Docs](https://grafana.com/docs/)
* [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)

This concludes the monitoring section.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/c3806869-7f9e-4cc2-8dc5-aa10304e3d1c/lesson/1a7fb216-b12c-4abf-a4af-a61c2c935d36" />
</CardGroup>


# Package Scopes

Source: https://notes.kodekloud.com/docs/Kubernetes-Administration-Package-Management-with-Glasskube/Package-Installation/Package-Scopes/page

Explains Glasskube package scopes, differences between cluster-scoped and namespaced packages, use cases, UI locations, and how to author package manifests safely.

Before we dive into package configuration and installation, it helps to understand the two package scopes Glasskube supports: cluster-scoped and namespaced packages. Choosing the right scope determines how a package is deployed, who can reuse it, and whether it can create cluster-level resources.

Cluster-scoped packages

* Cluster-scoped packages manage cluster-wide resources such as `ClusterRole`, `ClusterRoleBinding`, and `CustomResourceDefinition` (CRD).
* Because they operate at the cluster level, these packages are typically installed once per cluster and shared across namespaces.
* Common use cases: cluster networking, global observability, cluster-wide security tools, and CRD providers.

<Frame>
  <img alt="The image depicts a diagram of a Single-Node Cluster divided into &#x22;Cluster Scoped&#x22; and &#x22;Namespace Scoped&#x22; sections, featuring observability, continuous deployment, and analytics." />
</Frame>

Namespaced packages

* Namespaced packages are confined to a single Kubernetes namespace and don’t manage cluster-level resources.
* They can be installed multiple times in different namespaces, providing isolated instances for teams, environments, or applications.
* Common use cases: per-team deployments, environment-specific instances (dev/stage/prod), and application-scoped tooling.

How to choose a scope

* Use cluster-scoped packages for functionality that must be shared across the cluster or that manages cluster-level resources (e.g., networking, cluster-wide monitoring, CRDs).
* Use namespaced packages when you need multiple isolated instances of the same package (e.g., separate team environments) or when the package only affects resources within a single namespace.

| Scope          | Typical resources managed                                           | When to use                                                       |
| -------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Cluster-scoped | `ClusterRole`, `ClusterRoleBinding`, `CustomResourceDefinition`     | Shared services, global controllers, CRD providers                |
| Namespaced     | `Role`, `RoleBinding`, `Deployment`, `Service` (within a namespace) | Per-team or per-environment isolation, application-scoped tooling |

<Callout icon="lightbulb">
  Cluster-scoped packages are ideal for functionality that must be installed only once per cluster (e.g., an operator that provides CRDs). Namespaced packages are best when you need repeatable, isolated deployments across namespaces.
</Callout>

Glasskube UI and where scopes appear

* In the Glasskube web UI:
  * Cluster-scoped packages appear under the `Cluster Packages` tab.
  * Namespaced packages appear under the `Packages` tab.

Authoring package manifests
When creating Glasskube package definition files, set the `kind` to `ClusterPackage` for cluster-scoped packages or `Package` for namespaced packages. For example:

```yaml theme={null}
apiVersion: packages.glasskube.dev/v1alpha1
kind: ClusterPackage
metadata:
  creationTimestamp: null
  name: argo-cd
spec:
  packageInfo:
    name: argo-cd
    repositoryName: glasskube
    version: v2.11.7+1
```

<Callout icon="warning">
  Be cautious when authoring cluster-scoped packages: because they affect cluster-wide state, changes can impact all namespaces. Test cluster-scoped manifests in a safe environment before deploying to production clusters.
</Callout>

Links and references

* Glasskube package docs: [https://glasskube.dev/docs](https://glasskube.dev/docs) (refer to your Glasskube installation docs)
* Kubernetes RBAC and resources: [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* CustomResourceDefinitions: [https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)

Now that you know how package scopes work and how to pick between them, you’re ready to move on to installing and configuring packages with Glasskube.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/k8s-administration-package-management-with-glasskube/module/c3806869-7f9e-4cc2-8dc5-aa10304e3d1c/lesson/2f9b77f1-bc91-4775-bf0f-c7f9bcb33428" />
</CardGroup>
