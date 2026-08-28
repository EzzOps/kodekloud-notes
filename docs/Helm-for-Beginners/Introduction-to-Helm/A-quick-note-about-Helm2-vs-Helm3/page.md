# Service definition for hello-world
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
# Deployment definition for hello-world
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 2
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
          image: nginx
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

Helm charts adhere to a specific directory structure that typically includes the `templates/` folder along with files such as `Chart.yaml`, `values.yaml`, `LICENSE`, and `README.md`.

## Using Helm to Scaffold the Chart

You do not need to manually create this structure. The Helm CLI can generate a skeleton chart for you:

```bash theme={null}
$ helm create nginx-chart
$ ls nginx-chart
charts  Chart.yaml  templates  values.yaml
```

Now, you can replace or add your own Kubernetes manifest files (for example, the deployment and service files shown above) into the `templates/` directory. Initially, the generated `Chart.yaml` file contains default data based on the provided chart name.

### Examining and Modifying Chart Metadata

At this stage, you might want to update the `Chart.yaml` file to include more detailed metadata. For instance, if your company is developing this chart for internal use, you can update the file with a more descriptive summary and add maintainer contacts.

To open and edit the file:

```bash theme={null}
$ cd nginx-chart
$ vi Chart.yaml
```

The original content may resemble this:

```yaml theme={null}
apiVersion: v2
name: nginx-chart
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.16.0"
```

Modify it to add details and contact information:

```yaml theme={null}
apiVersion: v2
name: nginx-chart
description: Basic nginx website
type: application
version: 0.1.0
appVersion: "1.16.0"
maintainers:
  - name: john smith
    email: john@example.com
```

Once you have updated the metadata, remove any unnecessary sample template files from the `templates/` directory:

```bash theme={null}
$ cd nginx-chart
$ ls templates
deployment.yaml  _helpers.tpl  hpa.yaml  ingress.yaml  NOTES.txt  serviceaccount.yaml  service.yaml  tests
```

For your simple application, add your custom deployment and service YAML files to this folder, and your chart will be ready for installation.

## Static vs. Templated Names

When you install a Helm chart, the objects in the templates are created exactly as defined. For example:

```bash theme={null}
$ helm install hello-world-1 ./nginx-chart
$ kubectl get deployment
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
hello-world   0/2     2            0           24s
```

Since the deployment name is hardcoded as `hello-world`, installing another release of the same chart leads to name conflicts:

```bash theme={null}
$ helm install hello-world-2 ./nginx-chart
Error: rendered manifests contain a resource that
already exists. Unable to continue with install:
Deployment "hello-world" in namespace "default" exists
and cannot be imported into the current release:
invalid ownership metadata; annotation validation
error: key "meta.helm.sh/release-name" must equal "hello-world-2"; current value is "hello-world-1"
```

To avoid conflicts, leverage Helm's templating language to create dynamic names based on the release name. For instance, update your service and deployment definitions as follows:

```yaml theme={null}
# templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-svc
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
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-nginx
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
          image: "{{ .Values.image }}"
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

Now, when you install the chart using different release names, Helm replaces the template directives (e.g., `{{ .Release.Name }}`) with your specified release name:

```bash theme={null}
$ helm install hello-world-1 ./nginx-chart
$ helm install hello-world-2 ./nginx-chart
$ kubectl get deployment
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
hello-world-1-nginx     1/2     2            1           8s
hello-world-2-nginx     0/2     2            0           4s
```

<Callout icon="lightbulb">
  Basing resource names on the Helm release name ensures that multiple installations in the same namespace do not conflict.
</Callout>

## Exposing Configurable Values

Customization is key for production-ready charts. Often, you might want to configure deployment attributes—such as the number of replicas or the container image—to suit different environments. The `values.yaml` file serves this purpose by storing default configurations that your templates can reference.

Consider the following simple `values.yaml`:

```yaml theme={null}
# Default values for nginx-chart.
replicaCount: 2
image: nginx
```

Your deployment template then references these values:

```yaml theme={null}
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-nginx
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
          image: "{{ .Values.image }}"
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

This setup allows users to override default settings during installation, for example:

```bash theme={null}
$ helm install hello-world-1 ./nginx-chart \
    --set replicaCount=3 \
    --set image=nginx
```

For more intricate configurations, you can structure the values file as a dictionary. For example, separate the image details:

```yaml theme={null}
# Default values for nginx-chart.
replicaCount: 2
image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.16.0"
```

And update your deployment template accordingly:

```yaml theme={null}
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-nginx
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
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

This approach constructs the complete container image string dynamically and allows you to adjust the image pull policy as needed.

## Summary

When you install a Helm chart, Helm processes the templates in your `templates/` directory together with several sources of configuration:

• Release-specific details (such as release name, namespace, and revision)\
• Default values defined in `values.yaml`\
• Metadata from `Chart.yaml`\
• Information from your Kubernetes cluster

The resulting manifest files are then used by Kubernetes to deploy your resources. By designing templates with dynamic naming (using `{{ .Release.Name }}`) and configurable values (via `values.yaml`), you guarantee that each chart installation creates uniquely named objects and can be tailored easily by users.

Happy templating, and see you in the next lesson!

***

For more information on Helm, visit the [Helm Documentation](https://helm.sh/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/helm-for-beginners/module/b90a4aa4-31b5-43d3-a7aa-383d48c50db0/lesson/2d967724-3d1e-49d6-bb1a-6e6528998cce" />
</CardGroup>


# A quick note about Helm2 vs Helm3

Source: https://notes.kodekloud.com/docs/Helm-for-Beginners/Introduction-to-Helm/A-quick-note-about-Helm2-vs-Helm3/page

This article reviews the evolution of Helm and highlights the major architectural changes introduced in Helm 3 compared to Helm 2.

Helm has come a long way since its inception. Understanding the differences between Helm 2 and Helm 3 is crucial when browsing charts and technical articles. This article reviews the evolution of Helm and highlights the major architectural changes introduced in Helm 3.

Helm 1.0 debuted in February 2016, followed by Helm 2.0 in November 2016 and Helm 3.0 in November 2019. The project has matured significantly, driven largely by enhancements in Kubernetes.

<Frame>
  ![The image is a timeline of Helm's version history, showing releases 1.0 in February 2016, 2.0 in November 2016, and 3.0 in November 2019.](https://kodekloud.com/kk-media/image/upload/v1752878958/notes-assets/images/Helm-for-Beginners-A-quick-note-about-Helm2-vs-Helm3/helm-version-history-timeline.jpg)
</Frame>

Improvements in Kubernetes empowered Helm with more robust tools, enabling a simpler and more effective design in Helm 3 compared to Helm 2. In this lesson, we focus on Helm 3, which simplifies the overall design and introduces enhanced features—particularly in security and revision management.

## Architecture: Removing Tiller

Helm uses a command-line client on your local machine to execute commands on a Kubernetes cluster. In Helm 2, limitations in Kubernetes—such as the absence of role-based access control (RBAC) and custom resource definitions (CRDs)—necessitated an extra component called Tiller. The Helm client communicated with Tiller, which then interacted with Kubernetes to implement your commands.

<Frame>
  ![The image is a diagram illustrating the architecture of Helm 2, showing the interaction between the Helm CLI and Tiller, with references to Kubernetes and notes on Role-Based Access Control and Custom Resource Definitions.](https://kodekloud.com/kk-media/image/upload/v1752878959/notes-assets/images/Helm-for-Beginners-A-quick-note-about-Helm2-vs-Helm3/helm-2-architecture-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  In Helm 2, Tiller functioned with full privileges by default, which introduced significant security concerns.
</Callout>

With the introduction of RBAC and CRDs in Kubernetes, the need for Tiller was eliminated. Consequently, Helm 3 removes Tiller entirely, allowing direct communication between the Helm CLI and the Kubernetes API. This change not only reduces complexity but also enhances security by enforcing Kubernetes’ RBAC policies consistently—whether commands are executed via kubectl or Helm.

<Frame>
  ![The image is a diagram illustrating Helm 3 architecture, showing the interaction between the Helm CLI, Kubernetes, and features like Role-Based Access Control and Custom Resource Definitions.](https://kodekloud.com/kk-media/image/upload/v1752878960/notes-assets/images/Helm-for-Beginners-A-quick-note-about-Helm2-vs-Helm3/helm-3-architecture-diagram.jpg)
</Frame>

## Three-Way Strategic Merge Patch: Intelligent Rollbacks and Upgrades

One of the standout improvements in Helm 3 is the introduction of a three-way strategic merge patch mechanism. This mechanism functions as a snapshot system, creating revisions of the release state to facilitate intelligent rollbacks and upgrades.

Consider the following example:

1. Install a WordPress website using a Helm chart, which creates revision number one:

   ```bash theme={null}
   $ helm install wordpress
   ```

2. Later, upgrade to a newer chart that changes the image version from WordPress 4.8 to WordPress 5.8. Before the upgrade, your deployment configuration might look like this:

   ```yaml theme={null}
   containers:
     - image: wordpress:4.8-apache
   ```

   After the upgrade, the configuration updates to:

   ```yaml theme={null}
   containers:
     - image: wordpress:5.8-apache
   ```

   Execute the upgrade command with:

   ```bash theme={null}
   $ helm upgrade wordpress
   ```

At this point, Helm assigns revision number two to record the new state. These revisions act as snapshots, enabling you to roll back to a previous version if necessary. Running a rollback command results in the creation of a new revision that reflects the restored state:

```bash theme={null}
$ helm rollback wordpress
```

In Helm 2, rollbacks based solely on comparing the current chart with the previous chart did not accommodate manual changes made via kubectl. For instance:

1. Install the WordPress deployment (revision one):

   ```bash theme={null}
   $ helm install wordpress
   ```

2. A user manually updates the application image using kubectl:

   ```bash theme={null}
   $ kubectl set image wordpress wordpress=5.8-apache
   ```

Since this modification occurred outside of Helm, no new revision was created. Attempting a rollback:

```bash theme={null}
$ helm rollback wordpress
```

would yield no change as Helm 2 simply compares the charts and sees no differences.

In contrast, Helm 3 performs a three-way strategic merge patch by comparing:

* The current chart in use (if a revision exists),
* The desired chart from the previous revision, and
* The live state of the Kubernetes objects.

For example, if the live state shows the WordPress image as 5.8-apache but revision one indicates wordpress:4.8-apache, Helm 3 detects the difference and reverts the changes accordingly.

```bash theme={null}
$ helm install wordpress
$ kubectl set image wordpress wordpress=5.8-apache
$ helm rollback wordpress
```

This intelligent capability ensures that changes made outside of Helm are recognized and handled appropriately during rollbacks and upgrades.

## Summary

The key differences between Helm 2 and Helm 3 are summarized below:

| Feature            | Helm 2                                                          | Helm 3                                                                                  |
| ------------------ | --------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Tiller             | Required for managing releases, with full privileges by default | Removed for direct CLI-to-Kubernetes communication                                      |
| Rollback Mechanism | Based solely on chart comparison, ignoring manual changes       | Uses a three-way strategic merge patch to intelligently record and revert state changes |

<Frame>
  ![The image is a comparison table between Helm 2 and Helm 3, showing that Helm 2 uses Tiller while Helm 3 does not, and Helm 3 supports 3-Way Strategic Merge Patch while Helm 2 does not.](https://kodekloud.com/kk-media/image/upload/v1752878960/notes-assets/images/Helm-for-Beginners-A-quick-note-about-Helm2-vs-Helm3/helm-2-vs-helm-3-comparison.jpg)
</Frame>

That concludes this article. In the next lesson, we will explore more advanced Helm topics and further refine our practices in managing Kubernetes deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/helm-for-beginners/module/15e220ca-1229-4779-81f0-3bc9f804aa6b/lesson/9f3e63c6-1bec-4b90-b946-2ddd9a974478" />
</CardGroup>
