# Deploying applications web console

Source: https://notes.kodekloud.com/docs/OpenShift-4/Openshift-Concepts-Projects-and-Users/Deploying-applications-web-console/page

Deploy applications on OpenShift using the web console with methods like manual deployment and importing from a Git repository.

Deploy applications on OpenShift quickly and efficiently using multiple methods. In this guide, we cover two primary approaches: deploying via the Workloads > Deployments interface and importing a Git repository. We also briefly touch on using the terminal with kubectl for deployment.

***

## Method 1: Creating a Deployment via the Workloads Interface

To create a deployment manually using the web console, follow these steps:

1. Navigate to **Workloads** and then **Deployments**.
2. Click on **Create Deployment**.

![The image shows the Red Hat OpenShift Container Platform dashboard, highlighting the "Deployments" section in the sidebar and providing options for getting started with resources and exploring new admin features.](https://kodekloud.com/kk-media/image/upload/v1752882699/notes-assets/images/OpenShift-4-Deploying-applications-web-console/openshift-dashboard-deployments-sidebar.jpg)

In the editor provided, you can paste a standard Kubernetes manifest. For example, the YAML below deploys an HTTP server:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: httpd
spec:
  containers:
    - name: httpd
      image: image-registry.openshift-image-registry.svc:5000/opens
      ports:
        - containerPort: 8080
```

> **lightbulb** For applications with multiple components (e.g., services, deployments, daemon sets), consider using automated methods to deploy all configurations simultaneously.

***

## Deploying a Sample Nginx Application

For demonstration, deploy a stateless Nginx application with the following Kubernetes manifest:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2  # instructs the deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.14.2
          ports:
            - containerPort: 80
```

1. Copy the manifest into the editor and click **Create Deployment**.
2. The deployment process will start, and you can verify its status after a few moments.

Once running, you can view key details like the namespace, deployment name, update strategy, node selector, and pod selector. The dashboard also provides options to view the YAML configuration and a list of running pods.

![The image shows a Red Hat OpenShift Container Platform interface displaying deployment details for an "nginx-deployment" with 2 pods. The sidebar includes options like Home, Operators, and Workloads.](https://kodekloud.com/kk-media/image/upload/v1752882701/notes-assets/images/OpenShift-4-Deploying-applications-web-console/openshift-nginx-deployment-details.jpg)

To inspect deployed pods:

* Navigate to **Pods** under the deployment.
* Click on a specific pod to view its details, logs, and even access an embedded terminal (similar to executing "kubectl exec").

![The image shows the Red Hat OpenShift Container Platform interface, displaying a list of running pods under the "nginx-deployment" with their status, readiness, and other details.](https://kodekloud.com/kk-media/image/upload/v1752882703/notes-assets/images/OpenShift-4-Deploying-applications-web-console/openshift-nginx-deployment-pods.jpg)

![The image shows the Red Hat OpenShift Container Platform interface, displaying details of a running Nginx deployment pod. It includes tabs for metrics, YAML, environment, logs, events, and terminal.](https://kodekloud.com/kk-media/image/upload/v1752882704/notes-assets/images/OpenShift-4-Deploying-applications-web-console/openshift-nginx-deployment-interface.jpg)

For example, executing this command in the interactive terminal:

```bash theme={null}
