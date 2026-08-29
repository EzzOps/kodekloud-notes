# Output:
# deployment.apps/api-deployment created
kubectl apply -f k8s/cache
# (Applies cache-related configurations)
```

You can also deploy all configurations in one command by appending multiple `-f` flags:

```bash theme={null}
kubectl apply -f k8s/api
kubectl apply -f k8s/cache
kubectl apply -f k8s/db
```

To delete all resources simultaneously, you can run:

```bash theme={null}
kubectl delete -f k8s/db -f k8s/cache -f k8s/api
```

> **lightbulb** Using multiple `-f` flags simplifies bulk deployment and deletion. However, as your infrastructure grows, managing these commands can become cumbersome.

## Simplifying Resource Management with Kustomize

Kustomize makes it easier to manage and customize your application configurations. Begin by creating a `kustomization.yaml` file in the root of your K8s directory. This file specifies the API version and kind required by Kustomize:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
```

Next, define the resources you wish to manage by listing the file paths relative to the `kustomization.yaml` file's location. For example:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - api/api-depl.yaml
  - api/api-service.yaml
  - cache/redis-config.yaml
  - cache/redis-depl.yaml
  - cache/redis-service.yaml
  - db/db-config.yaml
  - db/db-depl.yaml
  - db/db-service.yaml
```

You can then build the complete set of manifests using the Kustomize CLI:

```bash theme={null}
kustomize build k8s/
```

This command outputs the final Kubernetes manifests, combining configurations from the API, cache, and database folders. While `kustomize build` displays the resulting configuration, it does not apply it to your cluster. To deploy these resources, pipe the output to `kubectl apply`:

```bash theme={null}
kustomize build k8s/ | kubectl apply -f -
```

Alternatively, leverage the built-in support for Kustomize in kubectl with the `-k` flag:

```bash theme={null}
kubectl apply -k k8s/
```

After applying the configurations, verify that the resources have been successfully created by checking the pods:

```bash theme={null}
kubectl get pods
```

Expected output:

```bash theme={null}
NAME                                           READY   STATUS    RESTARTS   AGE
api-deployment-64dd567b46-1mw4c               1/1     Running   0          27s
db-deployment-657c8fbd8-vnjs7                  1/1     Running   0          26s
redis-deployment-587fd758cf-7pt57              1/1     Running   0          26s
```

> **lightbulb** For quick troubleshooting, always verify your pods' status with `kubectl get pods` after deploying configurations.

## Advanced Directory Structuring with Kustomize

While maintaining a single `kustomization.yaml` in the root directory works for simple projects, a more scalable practice is to include a `kustomization.yaml` file in each subdirectory. In this method, each directory imports only the YAML files specific to its component, while a root `kustomization.yaml` aggregates these directories.

### API Directory Configuration

In the API folder, create a `kustomization.yaml` that lists the API deployment and service manifests:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - api-depl.yaml
  - api-service.yaml
```

### Cache Directory Configuration

In the cache directory, set up the following `kustomization.yaml`:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - redis-config.yaml
  - redis-depl.yaml
  - redis-service.yaml
```

### Database Directory Configuration

Similarly, for the database directory, create a `kustomization.yaml`:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - db-config.yaml
  - db-depl.yaml
  - db-service.yaml
```

### Root Directory Aggregation

Finally, update the root `kustomization.yaml` to reference these subdirectories. When a directory is specified as a resource, Kustomize automatically searches for a `kustomization.yaml` file inside:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - api/
  - cache/
  - db/
```

Before re-deploying, delete any previously applied resources:

```bash theme={null}
kubectl delete -f k8s/db -f k8s/cache -f k8s/api
```

Then, build the final configuration with Kustomize:

```bash theme={null}
kustomize build k8s/
```

Review the output to ensure it meets your expectations, then apply the aggregated configuration:

```bash theme={null}
kubectl apply -k k8s/
```

The expected output should be similar to:

```bash theme={null}
configmap/redis-credentials created
service/api-service created
service/db-service created
service/redis-cluster-ip-service created
deployment.apps/api-deployment created
deployment.apps/db-deployment created
deployment.apps/redis-deployment created
```

Verify the pods again:

```bash theme={null}
kubectl get pods
```

Expected output:

```bash theme={null}
NAME                                           READY   STATUS    RESTARTS   AGE
api-deployment-64dd567b46-1mw4c               1/1     Running   0          27s
db-deployment-657c8fbd8-vnjs7                  1/1     Running   0          26s
redis-deployment-587fd758cf-7pt57              1/1     Running   0          26s
```

This structured approach using Kustomize not only centralizes the management of your Kubernetes configurations but also offers a scalable solution for handling an expanding set of resources within your infrastructure.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/031e84b8-bcbc-4f39-94d6-66d93b05bddc/lesson/a5f8f67c-8464-47f3-bce5-af33781f3964)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/031e84b8-bcbc-4f39-94d6-66d93b05bddc/lesson/cc61109a-4e64-441d-9896-b25712f0d63c)


# Managing Directories

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Kustomize-Basics-2025-Updates/Managing-Directories/page

This guide explains how to structure Kubernetes YAML files effectively using Kustomize for streamlined management and deployment workflows.

Organizing and managing your Kubernetes manifests across multiple directories can be streamlined with Kustomize. This guide explains how to structure your YAML files effectively, simplify deployment workflows, and maintain a clean configuration hierarchy for your clusters.

## Basic Directory Structure Without Kustomize

Initially, you might store all your Kubernetes YAML files in a single directory (e.g., a directory named "k8s"). In this simple setup, you could have files such as:

* API deployment YAML file
* API service YAML file
* Database deployment YAML file
* Database service YAML file

To deploy these configurations, navigate to your "k8s" directory and run:

```bash theme={null}
kubectl apply -f .
```

This method works well for a small number of files. However, as your application scales, you'll likely end up with dozens of manifests, which can clutter your directory and complicate maintenance.

## Organizing YAML Files into Subdirectories

A more structured approach is to organize your manifests into subdirectories. For instance, you can place API-related configurations in an "api" subdirectory and database-related configurations in a "db" subdirectory. Deployment commands for each subdirectory would look like this:

```bash theme={null}
kubectl apply -f k8s/api/
```

```bash theme={null}
kubectl apply -f k8s/db/
```

While this method is functional, it may become cumbersome when dealing with numerous subdirectories, especially when managing repetitive commands in CI/CD pipelines.

## Simplifying Deployment with Kustomize

Kustomize simplifies this process by letting you define a single `kustomization.yaml` file that aggregates resources from multiple directories. Create a `kustomization.yaml` file in the root of your "k8s" directory with a list of resources and their relative paths. For example:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
