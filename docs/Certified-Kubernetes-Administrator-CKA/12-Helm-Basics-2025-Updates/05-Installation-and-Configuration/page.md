# Service and Deployment templates
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
---
# values.yaml snippet
replicaCount: 1
image:
  repository: nginx
---
# Chart.yaml snippet
apiVersion: v2
appVersion: "1.16.0"
name: hello-world
description: A web application
type: application
```

Again, the chart can be installed with:

```bash theme={null}
$ helm install hello-world
```

## Example: WordPress Chart

For a more complex use case, consider a WordPress chart that depends on additional services like MariaDB. Below is an example of a Chart.yaml file for a WordPress deployment:

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

## Helm Chart Directory Structure

A typical Helm chart directory includes the following components:

* **templates/**: Contains all the manifest templates (e.g., Deployment, Service).
* **values.yaml**: Defines default configuration values.
* **Chart.yaml**: Holds metadata about the chart.
* **charts/**: Optionally includes dependent charts (e.g., the MariaDB chart for WordPress).
* Other optional files such as **LICENSE** or **README** for additional information.

## Deploying a Chart from a Repository

To deploy the WordPress chart from the Bitnami repository, execute the following commands:

```bash theme={null}
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm install my-release bitnami/wordpress
```

You can verify your installation using similar commands:

```plaintext theme={null}
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm install my-release bitnami/wordpress
```

This concludes our overview of Helm Charts. In the next lesson, we will delve deeper into chart templating techniques and explore advanced methods to customize your Kubernetes deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/10d7440b-907c-46da-ac5c-d833e7022375/lesson/d1dc40b6-5b6b-497f-950b-165ec4b803aa" />
</CardGroup>


# Installation and configuration

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Helm-Basics-2025-Updates/Installation-and-Configuration/page

This lesson explains the steps required to install Helm, a package manager for Kubernetes, on Linux systems.

This lesson explains the steps required to install Helm, a package manager for Kubernetes. Before starting, ensure you have a functioning Kubernetes cluster and that kubectl is properly configured. Verify that your kubeconfig file contains the correct credentials to access your Kubernetes cluster.

<Callout icon="lightbulb">
  Make sure your system has access to a working Kubernetes cluster and that
  `kubectl` is set up correctly. A valid kubeconfig file is essential for Helm
  to connect to your cluster.
</Callout>

Helm is compatible with Linux, Windows, and macOS. This guide focuses on installing Helm on Linux systems.

## Installing Helm on Linux

### Using Snap

If your system supports Snap, you can install Helm using the command below. The `--classic` option offers a more relaxed sandbox environment, enabling Helm to easily locate your kubeconfig file in your home directory and connect to your Kubernetes cluster:

```bash theme={null}
sudo snap install helm --classic
```

### Using APT (Debian/Ubuntu)

For apt-based systems such as Debian or Ubuntu, follow these steps to add the Helm package repository and its signing key, then install Helm:

```bash theme={null}
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

### Using PKG

On systems that support PKG, you can install Helm with the following command:

```bash theme={null}
pkg install helm
```

<Callout icon="lightbulb">
  For the most current installation procedures, always refer to the official
  Helm documentation.
</Callout>

## Conclusion

With Helm installed, you are now ready to explore its capabilities in your lab environment. This guide provided step-by-step instructions for various Linux distributions to help streamline your Helm installation process.

Happy Helming!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/10d7440b-907c-46da-ac5c-d833e7022375/lesson/c51c3be3-4f45-4e06-b304-7b38d66e076d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/10d7440b-907c-46da-ac5c-d833e7022375/lesson/8443e601-9fef-4eec-999b-484482325bf0" />
</CardGroup>
