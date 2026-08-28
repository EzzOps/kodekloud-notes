# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-world
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app: hello-world
```

```yaml theme={null}
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
        - name: nginx
          image: {{ .Values.image.repository }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

```yaml theme={null}
# values.yaml
replicaCount: 1
image:
  repository: nginx
```

In this example, the `values.yaml` file provides dynamic configuration values (such as replica count and image repository), allowing you to customize deployments effortlessly without altering the core chart templates.

## Advanced Templating Example

For more complex applications, such as deploying WordPress, Helm chart templates leverage advanced functions and conditionals to manage intricate Kubernetes manifest generation. Below is an excerpt from a sophisticated Helm chart template:

```yaml theme={null}
# Deployment template snippet from a complex chart
apiVersion: {{ include "common.capabilities.deployment.apiVersion" . }}
kind: Deployment
metadata:
  name: {{ include "common.names.fullname" . }}
  namespace: {{ .Release.Namespace | quote }}
  labels:
    {{- include "common.labels.standard" . | nindent 4 }}
    {{- if .Values.commonLabels }}
    {{- include "common.tplvalues.render" (dict "value" .Values.commonLabels "context" $) }}
    {{- end }}
    {{- if .Values.commonAnnotations }}
  annotations: {{ include "common.tplvalues.render" (dict "value" .Values.commonAnnotations) }}
    {{- end }}
spec:
  selector:
    matchLabels: {{- include "common.labels.matchLabels" . | nindent 6 }}
  strategy: {{- toYaml .Values.updateStrategy | nindent 4 }}
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
```

This snippet demonstrates how Helm uses templating functions and conditionals to dynamically generate a Deployment manifest, adapting parameters according to different configuration settings.

## Managing Releases with Helm

One of Helm's standout features is its ability to manage multiple releases from the same chart. For instance, you might deploy two distinct instances of a WordPress website—one for external customers and another for internal development. Although both releases use the same chart, they are managed independently, each with its own configuration and revision history.

Below are some example commands to install two separate releases from the same Helm chart:

```bash theme={null}
# Install the first release with a custom name 'my-site'
$ helm install my-site bitnami/wordpress

# Install a second independent release named 'my-second-site'
$ helm install my-second-site bitnami/wordpress
```

<Callout icon="lightbulb">
  Using the same chart source for different environments, such as production and development, simplifies management while keeping configurations isolated.
</Callout>

## Discovering Available Helm Charts

Helm charts are available from a variety of trusted providers worldwide, including Appscode, community operators, TrueCharts, and Bitnami. Instead of visiting each repository individually, you can use the Artifact Hub (also known as Helm Hub) to browse a consolidated view of available charts. Visit [artifacthub.io](https://artifacthub.io) to explore the extensive collection of Helm charts.

<Frame>
  ![The image is a diagram showing Helm repositories connected to ArtifactHub.io, with nodes labeled Appscode, Community Operators, TrueCharts, and Bitnami.](https://kodekloud.com/kk-media/image/upload/v1752878962/notes-assets/images/Helm-for-Beginners-Helm-Components/helm-repositories-artifacthub-diagram.jpg)
</Frame>

Artifact Hub currently hosts over 6300 packages, allowing you to search for specific charts or browse by category. Pay attention to charts marked with official or verified publisher badges for added trust.

Furthermore, Artifact Hub features an intuitive web interface for filtering and exploring charts:

<Frame>
  ![The image shows a webpage from ArtifactHUB displaying Helm repositories, including "kube-prometheus-stack" and "ingress-nginx," with filters and search options on the left.](https://kodekloud.com/kk-media/image/upload/v1752878963/notes-assets/images/Helm-for-Beginners-Helm-Components/artifacthub-helm-repositories-webpage.jpg)
</Frame>

## Conclusion

In this article, we covered the fundamentals of Helm's architecture, including its core components, chart templating capabilities, and release management. Additionally, we explored strategies for discovering and utilizing publicly available Helm charts. Future lessons will delve deeper into Helm's advanced templating features and real-world deployment scenarios.

Thank you for reading, and we look forward to exploring more in our next lesson.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/helm-for-beginners/module/15e220ca-1229-4779-81f0-3bc9f804aa6b/lesson/2e84cb4f-7da4-47c2-a2d6-02245eb91221" />
</CardGroup>


# Helm charts

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Introduction-to-Helm/Helm-charts/page

This article explains how Helm Charts automate application deployment on Kubernetes using templated resources and customizable configurations.

In this guide, we explore how Helm Charts simplify application deployment on Kubernetes. Helm is a powerful command-line tool that automates complex operations, such as installation, uninstallation, upgrades, and rollbacks. Rather than executing multiple manual steps, you instruct Helm to perform the desired action, and it takes care of all the necessary behind-the-scenes processes.

Helm achieves this automation using Charts. Charts are collections of files that define all the Kubernetes resources needed for an application. They include templated files (with a defined structure) that dynamically replace placeholders with values from a configuration file (typically `values.yaml`). For example, placeholders for image names or replica counts in Kubernetes manifests can be populated with user-defined values during deployment.

Below are examples of two templated Kubernetes objects—a Service and a Deployment—for a simple application:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: hello-world
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app: hello-world
```

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
        - name: hello-world
          image: "{{ .Values.image.repository }}"
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

When you run the command below, Helm processes the templates with your specified values and deploys the application:

```bash theme={null}
$ helm install hello-world
```

## Chart.yaml and Helm Chart Structure

Every Helm Chart includes a `Chart.yaml` file that holds metadata about the chart. This metadata covers the chart API version, application version, chart version, name, description, and additional descriptive fields. For example, Helm 3 charts set the API version to `v2`, while Helm 2 charts use `v1`. This versioning ensures that Helm correctly interprets available features like `dependency` and `type`.

Below is an example of a `Chart.yaml` file for a WordPress Chart:

```yaml theme={null}
apiVersion: v2
appVersion: 5.8.1
version: 12.1.27
name: wordpress
description: Web publishing platform for building blogs and websites.
type: application
dependencies:
  - condition: mariadb.enabled
    name: mariadb
    repository: https://charts.bitnami.com/bitnami
    version: 9.x.x
keywords:
  - application
  - blog
  - wordpress
maintainers:
  - email: containers@bitnami.com
    name: Bitnami
home: https://github.com/bitnami/charts/tree/master/bitnami/wordpress
icon: https://bitnami.com/assets/stacks/wordpress/img/wordpress-stack-220x234.png
```

Key elements in the `Chart.yaml` include:

* **apiVersion:** Indicates the chart API version. Helm 3 charts use `v2` and Helm 2 charts use `v1`.
* **appVersion:** Specifies the version of the packaged application (e.g., WordPress version 5.8.1).
* **version:** Represents the chart version and helps track changes independently of the application version.
* **name, description, and type:** Define the chart's name (WordPress), provide a brief description, and indicate that it is an "application" type chart.
* **dependencies:** Lists any dependent charts. In this example, the WordPress chart depends on a MariaDB chart, managing its deployment separately.
* **keywords, maintainers, home, and icon:** Provide additional metadata useful for chart discovery and reference.

A typical Helm chart directory structure includes:

* A **templates** directory containing all templated resource manifests.
* A **values.yaml** file that defines configuration parameters.
* A **Chart.yaml** file holding chart metadata.
* Optionally, a **charts** directory for dependencies and files such as a README or license.

To install the WordPress chart from the Bitnami repository, run the following commands:

```bash theme={null}
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm install my-release bitnami/wordpress
```

<Callout icon="lightbulb">
  Helm charts integrate templated manifests with customizable configurations, streamlining application deployment on Kubernetes. This eliminates many manual steps and ensures consistency across environments.
</Callout>

This setup demonstrates how Helm charts efficiently manage configurations and deployments on Kubernetes through a blend of templated resources and user-defined configurations. In subsequent lessons, we will delve deeper into chart templating, dependency management, and advanced customization options.

That’s all for now. See you in the next article!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/helm-for-beginners/module/15e220ca-1229-4779-81f0-3bc9f804aa6b/lesson/393844b9-2284-4ce9-8023-c6792a2a0efa" />
</CardGroup>
