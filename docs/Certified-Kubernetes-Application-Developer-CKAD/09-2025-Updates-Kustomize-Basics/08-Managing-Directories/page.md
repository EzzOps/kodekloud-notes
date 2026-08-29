# Managing Directories

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Managing-Directories/page

Learn to efficiently manage Kubernetes manifests across multiple directories using Kustomize for streamlined configurations and deployments.

Up to this point, we've only covered the absolute basics of a kustomization.yaml file. While we haven't explored every feature of Kustomize, you already have the tools to perform some powerful operations. One common requirement is managing Kubernetes manifests distributed across multiple directories. In this guide, you'll learn how to organize and apply configurations efficiently using Kustomize.

***

## Traditional Organization and Its Limitations

Imagine a directory named "k8s" that contains four YAML files:

* An API deployment manifest
* An API service manifest
* A database deployment manifest
* A database service manifest

With this simple setup, you might navigate to the "k8s" directory and run:

```bash theme={null}
$ kubectl apply -f .
```

This approach works based on standard Kubernetes behavior without requiring Kustomize. However, as the number of YAML files increases—perhaps to 20, 30, 50, or more—the directory can quickly become cluttered. To better manage the files, you might group related manifests into subdirectories. For example:

* Move the API deployment and service YAML files into an `api` subdirectory.
* Move the database deployment and service YAML files into a `db` subdirectory.

After reorganizing, you can no longer apply the configuration files from the root directory using one command. Instead, you must apply each group with separate commands like:

```bash theme={null}
$ kubectl apply -f k8s/api/
$ kubectl apply -f k8s/db/
```

This approach soon becomes cumbersome, especially when updating configurations or automating deployments with CI/CD pipelines.

***

## Simplifying with Kustomize

Kustomize can significantly streamline the process by allowing you to manage multiple directories from a single kustomization.yaml file.

> **lightbulb** With Kustomize, you can maintain a single command to deploy resources, reducing manual steps and potential errors.

### Setting Up Your Root kustomization.yaml

1. In the root of your "k8s" directory, create a `kustomization.yaml` file.
2. List all individual resource files using their relative paths.

For example:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
