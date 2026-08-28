# Helm Concept

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Helm-Fundamentals/Helm-Concept/page

Describes Helm packaging and templating for deploying Kubernetes applications using charts, values.yaml, repositories and CLI commands illustrated with a WordPress example

This lesson explains how Helm packages, templating, and values solve Kubernetes configuration and deployment challenges for applications like WordPress. A Helm chart bundles manifest templates (parameterized using Go templating) together with a values.yaml file that supplies concrete values. When Helm renders the templates with values, it produces the final Kubernetes manifests that are applied to the cluster.

Templates use Go template syntax (for example, `{{ .Values.image }}`) so a single values.yaml can customize many resources in one place. Below are example template files that you might find in a WordPress Helm chart. Each template demonstrates how variables are referenced and where values come from.

templates/deployment.yaml

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
  labels:
    app: wordpress
spec:
  selector:
    matchLabels:
      app: wordpress
      tier: frontend
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: wordpress
        tier: frontend
    spec:
      containers:
        - name: wordpress
          image: { { .Values.image } }
```

templates/pv.yaml

```yaml theme={null}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: wordpress-pv
spec:
  capacity:
    storage: { { .Values.storage } }
  accessModes:
    - ReadWriteOnce
  gcePersistentDisk:
    pdName: wordpress-2
    fsType: ext4
```

templates/service.yaml

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: wordpress
  labels:
    app: wordpress
spec:
  ports:
    - port: 80
  selector:
    app: wordpress
    tier: frontend
  type: LoadBalancer
```

templates/pvc.yaml

```yaml theme={null}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: wp-pv-claim
  labels:
    app: wordpress
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: { { .Values.storage } }
```

templates/secret.yaml

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: wordpress-admin-password
data:
  password: { { .Values.passwordEncoded } }
```

These template variables (for example, .Values.image, .Values.storage, .Values.passwordEncoded) are populated from the chart's values.yaml file. Anyone deploying the chart can customize the deployment by editing that single file.

Example values.yaml

```yaml theme={null}
image: wordpress:4.8-apache
storage: 20Gi
passwordEncoded: CajhWVUxSdzIZQzg0
```

Together, templates + values.yaml form a Helm chart. Charts also include Chart metadata (Chart.yaml) describing the chart itself.

<Frame>
  <img
    alt="A presentation slide titled &#x22;Helm Chart&#x22; showing a dashed box labeled Helm
Chart on the right, containing three stacked rounded buttons: &#x22;Templates&#x22;,
&#x22;values.yaml&#x22;, and
&#x22;Chart.yaml&#x22;."
  />
</Frame>

Example Chart.yaml

```yaml theme={null}
apiVersion: v2
name: wordpress
version: 9.0.3
description: Web publishing platform for building blogs and websites.
keywords:
  - wordpress
  - cms
  - blog
  - http
  - web
  - application
  - php
home: http://www.wordpress.com/
sources:
  - https://github.com/bitnami/bitnami-docker-wordpress
maintainers:
  - email: containers@bitnami.com
    name: Bitnami
```

You can author your own chart or reuse community charts hosted on Artifact Hub. Artifact Hub is a central index of community-contributed Helm charts and other Kubernetes packages.

<Frame>
  <img
    alt="Screenshot of the Artifact Hub repository homepage showing a large headline
&#x22;Find, install and publish Kubernetes packages&#x22; with a central search box,
example queries, and package/release statistics. The site URL
(https://artifacthub.io/) is shown in the
corner."
  />
</Frame>

As of this lesson, there are thousands of charts available on Artifact Hub. You can search charts from the web UI or directly from the Helm CLI.

Search Artifact Hub from the Helm CLI:

```bash theme={null}
helm search hub wordpress
