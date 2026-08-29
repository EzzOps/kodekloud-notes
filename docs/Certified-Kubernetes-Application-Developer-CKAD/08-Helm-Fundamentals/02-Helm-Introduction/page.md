# Example output:
# https://hub.helm.sh/charts/kube-wordpress/wordp...  0.1.0  1.1     this is my wordpress package
# https://hub.helm.sh/charts/groundhog2k/wordpress    0.4.1  5.8.0-apache  A Helm chart for Wordpress on Kubernetes
# https://hub.helm.sh/charts/bitnami-aks/wordpress    12.1.1 5.8.0  Web publishing platform for Wordpress...
```

If you want to use charts from a specific repository (for example Bitnami), add that repo to your local Helm configuration and search the repo:

```bash theme={null}
helm repo add bitnami https://charts.bitnami.com/bitnami

helm search repo wordpress
# Example output:
# NAME                CHART VERSION  APP VERSION  DESCRIPTION
# bitnami/wordpress   12.1.14        5.8.1        Web publishing platform for building blogs and ...
```

To install a chart on your cluster:

```bash theme={null}
helm install <release-name> <chart>
# Example:
helm install my-release bitnami/wordpress
```

Each installation of a chart is called a release. You can install the same chart multiple times under different release names; each release is independent:

```bash theme={null}
helm install release-1 bitnami/wordpress
helm install release-2 bitnami/wordpress
helm install release-3 bitnami/wordpress
```

Common chart components and their purpose

| Chart file / template     | Purpose                                                                       |
| ------------------------- | ----------------------------------------------------------------------------- |
| templates/deployment.yaml | Defines the application Deployment and container image reference.             |
| templates/service.yaml    | Exposes the application via Service (ClusterIP, NodePort, LoadBalancer).      |
| templates/pv.yaml         | Defines a PersistentVolume to back storage requests (cluster-level resource). |
| templates/pvc.yaml        | Requests storage from PVs (namespaced PersistentVolumeClaim).                 |
| templates/secret.yaml     | Stores credentials or secrets (data must be base64-encoded).                  |
| values.yaml               | Central place to override template variables per deployment.                  |
| Chart.yaml                | Chart metadata: name, version, description, maintainers, sources.             |

Useful Helm commands (summary)

| Command           | What it does                                         |
| ----------------- | ---------------------------------------------------- |
| helm search hub   | Searches Artifact Hub from the CLI for charts.       |
| helm repo add     | Adds a remote chart repository (e.g., Bitnami).      |
| helm search repo  | Searches charts in the local repo index.             |
| helm install      | Installs a chart as a release in the cluster.        |
| helm list         | Lists deployed releases.                             |
| helm uninstall    | Removes a release from the cluster.                  |
| helm pull --untar | Downloads and extracts a chart to a local directory. |

Examples and tips:

```bash theme={null}
helm list
# Shows installed releases, e.g.:
# NAME        NAMESPACE  REVISION  UPDATED                      STATUS    CHART                   APP VERSION
helm uninstall my-release

helm pull --untar bitnami/wordpress
ls wordpress
# Example listing:
# Chart.lock  README.md  ci  values.schema.json
helm install release-4 ./wordpress
# Install the local, modified chart directory
```

> **lightbulb** Kubernetes Secret data values (the "data" field) must be base64-encoded. In the earlier secret template, .Values.passwordEncoded is expected to already be base64-encoded. If you prefer to supply the raw password in values.yaml and have Helm encode it during rendering, you can use the b64enc template function, for example:

  ```yaml theme={null}
  data:
    password: {{ .Values.password | b64enc }}
  ```

  Alternatively, use the Secret's stringData field to provide raw (unencoded) string values and let the API server handle encoding:

  ```yaml theme={null}
  stringData:
    password: "{{ .Values.password }}"
  ```

  Avoid including raw passwords in plain text in version control; consider using external secret management or encrypted values files.

This lesson covered the essential Helm concepts for packaging and deploying applications: templates, values, charts, repositories, and the basic Helm CLI workflow. For production use and advanced exam topics, explore additional Helm features such as subcharts, chart dependencies, chart testing, hooks, and templating functions.

Further reading and references

* Helm documentation: [https://helm.sh/docs/](https://helm.sh/docs/)
* Artifact Hub: [https://artifacthub.io/](https://artifacthub.io/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/bc61a673-47c3-4bef-b7f5-12f85c65cbbb/lesson/a5451bdd-8dc1-4b42-964e-e32a998ee5a9)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/bc61a673-47c3-4bef-b7f5-12f85c65cbbb/lesson/428149c4-b60c-4be7-aaa2-0b7b6636415d)


# Helm Introduction

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Helm-Fundamentals/Helm-Introduction/page

This article explores Helms role in simplifying the management of complex Kubernetes applications by treating them as cohesive packages.

In this article, we will explore Helm and its role in simplifying the management of complex Kubernetes applications. While Kubernetes excels at orchestrating infrastructure, handling multiple interconnected objects in a single application can become challenging. For example, deploying a WordPress site might require several components, including:

* A Deployment to run the pods for components such as MySQL database servers or web servers.
* A Persistent Volume for database storage.
* A Persistent Volume Claim to request storage.
* A Service to expose the web server.
* A Secret to securely store the admin password.

Traditionally, each of these objects would be defined in separate YAML files and applied individually using the `kubectl apply` command. Managing configurations across multiple files becomes tedious and error-prone—if, for instance, you need to increase the persistent volume size from 20 GB to a higher capacity, every related YAML file must be manually updated. Additionally, upgrading or removing the application involves tracking down and managing all individual objects.

Consider the following YAML snippet:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: wordpress-admin-password
data:
  key: CajnHWVUxSdzIZQzg0SERXhBQTvQ1FzN2JE9PQ==
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: wordpress-pv
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOne
  gcePersistentDisk:
    pdName: wordpress-2
    fsType: ext4
```

While organizing related objects into separate files (for example, placing deployment configurations in `mysql-deployment.yaml`) can offer some clarity, it still requires searching across multiple files to update settings.

![The image illustrates Helm, a Kubernetes package manager, with components like Service, Deployment, Secret, PVC, and PV.](https://kodekloud.com/kk-media/image/upload/v1752871217/notes-assets/images/Certified-Kubernetes-Application-Developer-CKAD-Helm-Introduction/frame_170.jpg)

Enter Helm. Unlike Kubernetes, which considers each object independently, Helm recognizes that these objects are part of a cohesive package—such as a WordPress application. With Helm, you manage the application as a single unit instead of juggling multiple YAML files.

Consider this analogy: a computer game is composed of hundreds or thousands of files (executables, audio, graphics, configuration data). Instead of downloading and organizing each file manually, you run an installer that efficiently places everything in the correct locations. Helm provides a similar level of abstraction for your Kubernetes manifests. It allows you to install, upgrade, roll back, and uninstall an application, regardless of how many individual objects it encompasses.

For example, to install a WordPress package using Helm, you would execute:

```bash theme={null}
helm install wordpress ...
```

Helm leverages a central configuration file—typically named `values.yaml`—to manage custom settings. This file might look like:

```yaml theme={null}
wordpressUsername: user
wordpressEmail: user@example.com
wordpressFirstName: FirstName
wordpressLastName: LastName
```

This centralized configuration lets you adjust critical settings—such as persistent volume sizes, website names, admin passwords, and database configurations—in one place, eliminating the need to modify multiple YAML files.

> **lightbulb** By centralizing configuration management, Helm significantly streamlines application lifecycle management in Kubernetes.

Managing the application lifecycle becomes even simpler with Helm. With a single command, you can upgrade your application, and Helm calculates the necessary changes to each object. Rolling back to a previous version or uninstalling the application is equally straightforward. For example, a typical workflow might involve:

```bash theme={null}
helm install wordpress ...
helm upgrade wordpress ...
helm rollback wordpress ...
helm uninstall wordpress ...
```

By treating Kubernetes applications as cohesive packages rather than isolated objects, Helm reduces administrative overhead and simplifies application management. This package and release management approach allows you to focus on application development rather than micromanaging individual Kubernetes objects.

For further reading, consider visiting the [Kubernetes Documentation](https://kubernetes.io/docs/) and learning more about [Helm](https://helm.sh/).

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/bc61a673-47c3-4bef-b7f5-12f85c65cbbb/lesson/980d80bf-92fb-48ef-abfc-56835f0732e5)
