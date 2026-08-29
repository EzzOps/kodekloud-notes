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

Rather than building charts from scratch, you can download pre-built charts from public repositories. Customizing a deployment typically involves modifying the `values.yaml` file, which serves as the configuration for the Helm chart.

For more complex applications like WordPress, charts can include multiple files and advanced templating features. More detailed explorations of templating and chart structures will be discussed in future lessons. For now, grasping these simple examples will provide you with a solid foundation.

A more advanced templating snippet within a Deployment might look like this:

```yaml theme={null}
apiVersion: {{ include "common.capabilities.deployment.apiVersion" . }}
kind: Deployment
metadata:
  name: {{ include "common.names.fullname" . }}
  namespace: {{ .Release.Namespace | quote }}
  labels: 
    {{- include "common.labels.standard" . | nindent 4 }}
  {{- if .Values.commonLabels }}
    {{- include "common.tplvalues.render" (dict "value" .Values.commonLabels "context" $) | nindent 4 }}
  {{- end }}
  {{- if .Values.commonAnnotations }}
  annotations: 
    {{- include "common.tplvalues.render" (dict "value" .Values.commonAnnotations "context" $) | nindent 4 }}
  {{- end }}
spec:
  selector:
    matchLabels: {{- include "common.labels.matchLabels" . | nindent 6 }}
  {{- if .Values.updateStrategy }}
  strategy: {{- toYaml .Values.updateStrategy | nindent 4 }}
  {{- end }}
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
```

## Releases and Multiple Installations

When applying a chart to your cluster, Helm creates a release—a distinct instance of the application. This approach allows you to deploy multiple separate instances of the same chart with unique release names. For example, you can deploy two different WordPress sites using separate releases:

```bash theme={null}
# helm install [release-name] [chart]
$ helm install my-site bitnami/wordpress

$ helm install my-SECOND-site bitnami/wordpress
```

Each release is tracked independently, even if they are based on the same chart. This functionality is particularly useful when maintaining different environments, such as having one release for a public-facing website and another for development purposes. Experimentation in the development release can then inform upgrades or changes to the production version.

## Helm Repositories and Artifact Hub

Beyond our basic examples, Helm charts are available for a wide range of applications—from Redis to Prometheus—across numerous public repositories. Providers such as Appscode, Community Operators, TrueCharts, and Bitnami host charts in their repositories, making it easy to deploy various applications.

Instead of visiting multiple repositories separately, you can use the centralized [Artifact Hub](https://artifacthub.io) to search for and manage charts. Artifact Hub currently features over 6,300 packages and highlights charts published by official developers with verified publisher badges for added trustworthiness.

![The image is a diagram showing Helm repositories connected to ArtifactHub.io, with nodes labeled Appscode, Community Operators, TrueCharts, and Bitnami.](https://kodekloud.com/kk-media/image/upload/v1752869781/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Helm-Components/helm-repositories-artifacthub-diagram.jpg)

Artifact Hub also provides a searchable interface to help you quickly find the charts you need:

![The image shows a webpage from ArtifactHUB displaying search results for Helm repositories, including "kube-prometheus-stack" and "ingress-nginx," with filters and options on the left.](https://kodekloud.com/kk-media/image/upload/v1752869782/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Helm-Components/artifacthub-helm-repositories-search.jpg)

> **lightbulb** In upcoming lessons, we will explore chart installation and customization in greater detail. Continue following our guide to deepen your knowledge of the practical applications of Helm in Kubernetes.

Happy Helm-ing, and see you in the next lesson!

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/10d7440b-907c-46da-ac5c-d833e7022375/lesson/4017fa2b-b35c-49e3-9b73-eed0b452c8e3)


# Helm charts

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Helm-Basics-2025-Updates/Helm-charts/page

This article explores Helm Charts for managing Kubernetes applications, detailing their structure, usage, and deployment processes.

In this lesson, we explore Helm Charts—a powerful tool for managing Kubernetes applications. Helm simplifies tasks such as installing, upgrading, rolling back, and uninstalling applications by automating the complex steps required to achieve the desired state.

Helm Charts act as comprehensive instruction manuals for your deployments. Each chart is a structured collection of files that define an application's configuration and behavior on Kubernetes. For example, the parameters in the values.yaml file enable operators to customize configurations without modifying the underlying templates.

> **lightbulb** Use Helm’s templating syntax (e.g., `{{ .Values.replicaCount }}`) in your manifests to keep configuration flexible and reusable. All dynamic values are defined in the values.yaml file.

Below is a simple example of Helm template files that create two Kubernetes objects—a Deployment and a Service. The Deployment manages a set of Pods based on a specified image, and the Service exposes these Pods as a NodePort service:

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
---
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

To install this chart, run the following command:

```bash theme={null}
$ helm install hello-world
```

Notice that values like the image repository and replica count are not hardcoded. Instead, they utilize Helm’s templating syntax, which references configurations defined in the values.yaml file. This approach allows you to easily adjust parameters without directly editing the template files.

## Chart Metadata

Every Helm chart includes a Chart.yaml file that contains essential metadata, such as:

* **API Version:** For Helm 3, set to `v2` (Helm 2 charts use `v1` or omit this field).
* **App Version:** Indicates the version of the application deployed.
* **Chart Version:** Tracks the version of the chart itself, independent of the application version.
* **Name and Description:** Provide identification and a brief summary of the chart.
* **Type:** Specifies whether the chart is for an application (default) or is a library chart.
* **Dependencies:** Declare any external charts that the chart relies on.
* **Additional Fields:** Optional fields like keywords, maintainers, home, and icon help with discovery and branding.

Below is an example that combines Kubernetes manifest templates with chart metadata:

```yaml theme={null}
