# Kubernetes resources to be managed by Kustomize
resources:
  - api/api-depl.yaml
  - api/api-service.yaml
  - db/db-depl.yaml
  - db/db-service.yaml
```

With this configuration, deploy all resources from the root directory using one of the following commands:

```bash theme={null}
kustomize build k8s/ | kubectl apply -f -
```

Or leverage kubectl's native Kustomize support:

```bash theme={null}
kubectl apply -k k8s/
```

These commands aggregate the YAML files specified in `kustomization.yaml` and deploy them simultaneously, eliminating the need to apply individual directories manually.

## Scaling with Multiple Directories

As your Kubernetes project grows, you might add more subdirectories for additional services like caches or messaging systems (e.g., Redis or Kafka). For instance, your root `kustomization.yaml` file might expand to include these new resources:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# Kubernetes resources across multiple subdirectories
resources:
  - api/api-depl.yaml
  - api/api-service.yaml
  - db/db-depl.yaml
  - db/db-service.yaml
  - cache/redis-depl.yaml
  - cache/redis-service.yaml
  - cache/redis-config.yaml
  - kafka/kafka-depl.yaml
  - kafka/kafka-service.yaml
  - kafka/kafka-config.yaml
```

> **lightbulb** Consider breaking down the configurations into subdirectories with their own `kustomization.yaml` files. This not only simplifies maintenance but also enhances scalability.

### Using Individual kustomization.yaml Files in Subdirectories

For improved maintainability, create a separate `kustomization.yaml` file within each subdirectory (such as "api", "db", "cache", and "kafka"). For example, in the "db" directory, create a file with the following content:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - db-depl.yaml
  - db-service.yaml
```

Then, update the root `kustomization.yaml` file to reference each subdirectory:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - api/
  - db/
  - cache/
  - kafka/
```

Kustomize will recursively process each subdirectory's `kustomization.yaml`, aggregating all the resources for deployment. This modular approach makes your configuration more manageable over time.

## Deploying the Configurations

After setting up both the root and subdirectory-specific `kustomization.yaml` files, deployment becomes effortless. Simply run one of the following commands to deploy all configurations:

```bash theme={null}
kustomize build k8s/ | kubectl apply -f -
```

Or, using kubectl’s built-in Kustomize support:

```bash theme={null}
kubectl apply -k k8s/
```

Both methods compile all the manifests from your subdirectories and apply them in a single, efficient deployment process.

## Conclusion

By organizing your Kubernetes YAML files into dedicated subdirectories and leveraging Kustomize with individual `kustomization.yaml` files, you can manage complex deployments more effectively. This approach not only cleans up your configuration hierarchy but also streamlines CI/CD pipelines by reducing repetitive commands.

For more insights on Kubernetes configuration management, consider exploring the following resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kustomize Overview](https://kubectl.docs.kubernetes.io/references/kustomize/)

> **triangle-alert** Always test your Kustomize configurations in a staging environment before deploying to production. This practice helps ensure that your aggregated manifests work as expected across your Kubernetes clusters.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/031e84b8-bcbc-4f39-94d6-66d93b05bddc/lesson/2ce4f9d0-46e1-4fb3-bd7d-1d44669edd64)


# Overlays

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Kustomize-Basics-2025-Updates/Overlays/page

Overlays in Kustomize allow customization of base Kubernetes configurations for different environments like development, staging, and production.

Overlays in Kustomize allow you to customize a base Kubernetes configuration on a per-environment basis. This method is particularly useful for environments such as development, staging, and production, where you need to apply environment-specific adjustments to shared configurations.

Kustomize projects are typically organized into two main sections:

1. **Base Configuration:** Contains all shared and default Kubernetes resource definitions.
2. **Overlay Directories:** Each environment (e.g., dev, stg, prod) has its own overlay folder with patches to modify the base configuration as needed.

Below is a diagram illustrating a common directory structure for managing these configurations:

![The image illustrates a directory structure for Kubernetes configurations, showing a base directory for shared configs and overlay directories for environment-specific configurations (dev, stg, prod). It highlights the use of Kustomize for managing these configurations.](https://kodekloud.com/kk-media/image/upload/v1752869807/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Overlays/kubernetes-config-directory-structure.jpg)

> **lightbulb** In this setup, the base folder holds the shared resource files, while each overlay folder contains a `kustomization.yaml` that references the shared resources in the base along with overlays (patches or additional resources) specific to that environment.

## Base Configuration Example

Imagine that you have an `nginx-deployment.yaml` file within your base folder with a replica count set to 1. The corresponding `kustomization.yaml` in the base folder might look like this:

```yaml theme={null}
