# Kubernetes resources to be managed by Kustomize
resources:
  - api/api-depl.yaml
  - api/api-service.yaml
  - db/db-depl.yaml
  - db/db-service.yaml
```

Now, instead of applying each subdirectory manually, you can deploy all the resources with a single command. There are two primary options:

1. Build the complete configuration and pipe it to kubectl:

   ```bash theme={null}
   $ kustomize build k8s/ | kubectl apply -f -
   ```

2. Apply directly using kubectl’s built-in Kustomize support:

   ```bash theme={null}
   $ kubectl apply -k k8s/
   ```

Both commands process the `kustomization.yaml` file and deploy the defined resources automatically.

***

## Scaling with Additional Directories

Over time, your application may bring in new components—such as a cache for Redis or a Kafka service. In that case, your root kustomization.yaml might expand to list many individual resources:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# Kubernetes resources to be managed by Kustomize
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

While this configuration is entirely valid, the root file can become cluttered as the number of resources grows.

***

## A Cleaner Approach with Subdirectory kustomization.yaml Files

A more elegant solution delegates resource management to the individual subdirectories. In each subdirectory (e.g., `api`, `db`, `cache`, and `kafka`), create a separate `kustomization.yaml` file that lists only the YAML files contained within that directory.

For example, the `db` directory might have the following kustomization.yaml file:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - db-depl.yaml
  - db-service.yaml
```

Repeat a similar configuration for the other subdirectories.

Next, update the root kustomization.yaml file to reference these directories:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - api/
  - db/
  - cache/
  - kafka/
```

Now, when you run either:

```bash theme={null}
$ kustomize build k8s/ | kubectl apply -f -
```

or

```bash theme={null}
$ kubectl apply -k k8s/
```

Kustomize will traverse each subdirectory, process the individual kustomization.yaml files, and aggregate all the specified resources into one cohesive deployment. This approach keeps your root configuration clean, scalable, and easier to maintain.

***

By organizing your configurations with subdirectory kustomization.yaml files, you not only simplify the management of Kubernetes manifests but also streamline your deployment processes—ideal for continuous integration and continuous delivery (CI/CD) pipelines.

For more details on deploying and managing Kubernetes applications, visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

Happy Kustomizing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/2ce4f9d0-46e1-4fb3-bd7d-1d44669edd64" />
</CardGroup>


# Overlays

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Overlays/page

This guide explores leveraging Kustomize overlays to customize a base Kubernetes configuration for different environments while maintaining a consistent base configuration.

This guide explores how to leverage Kustomize overlays to customize a base Kubernetes configuration for different environments. Using overlays allows you to maintain a single, consistent base configuration while easily applying environment-specific changes for development, staging, and production.

## Folder Structure

A typical Kustomize project is organized into two main sections:

1. **Base Configuration:** Contains the shared Kubernetes configurations.
2. **Overlay Directories:** Contains environment-specific folders where you can adjust or extend the base configuration using patches or by adding new resources.

Below is an example directory structure:

```plaintext theme={null}
k8s/
└── base/
    ├── kustomization.yaml
    ├── nginx-depl.yaml
    ├── service.yaml
    └── redis-depl.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── config-map.yaml
    ├── stg/
    │   ├── kustomization.yaml
    │   └── config-map.yaml
    └── prod/
        ├── kustomization.yaml
        └── config-map.yaml
```

## Base Configuration

The base configuration contains all the shared resources used across environments. For example, a base `kustomization.yaml` could reference your primary Kubernetes resources:

```yaml theme={null}
resources:
  - nginx-depl.yaml
  - service.yaml
  - redis-depl.yaml
```

An example deployment file, `nginx-depl.yaml`, might look like this:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
```

## Overlays Using Patches

One of the key benefits of Kustomize is its ability to use overlays to modify the base configuration specific to each environment. Overlays allow you to apply patches that adjust parameters such as replica counts without duplicating the entire base configuration.

### Example: Development Environment

In the development overlay, you may want to increase the replica count from 1 to 2. The `kustomization.yaml` file in the `dev` directory could be structured as follows:

```yaml theme={null}
bases:
  - ../../base
patch: |-
  - op: replace
    path: /spec/replicas
    value: 2
```

Here, the `bases` field points to the common base configuration, and the patch adjusts the `/spec/replicas` property specifically for the development environment.

### Example: Production Environment

For the production environment, if you want to set the replica count to 3, the overlay's `kustomization.yaml` would look similar with a slight change:

```yaml theme={null}
bases:
  - ../../base
patch: |-
  - op: replace
    path: /spec/replicas
    value: 3
```

This mechanism allows each overlay to tailor the configuration to meet specific operational requirements.

## Adding New Resources in Overlays

Overlays are not limited to patching existing resources; they can also introduce new resources that are unique to an environment. For example, in a production overlay, you might add a Grafana deployment. The directory structure can be updated as follows:

```plaintext theme={null}
k8s/
└── base/
    ├── kustomization.yaml
    ├── nginx-depl.yaml
    ├── service.yaml
    └── redis-depl.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   ├── config-map.yaml
    │   └── volume.yaml
    ├── stg/
    │   ├── kustomization.yaml
    │   └── config-map.yaml
    └── prod/
        ├── kustomization.yaml
        ├── config-map.yaml
        └── grafana-depl.yaml
```

In the production overlay’s `kustomization.yaml`, you can include the additional Grafana resource:

```yaml theme={null}
bases:
  - ../../base
resources:
  - grafana-depl.yaml
patch: |-
  - op: replace
    path: /spec/replicas
    value: 2
```

This configuration continues to import the common resources from the base while adding the unique Grafana deployment specific to production.

## Flexibility in Directory Structure

Kustomize's flexible design helps manage complexity by separating common configurations from environment-specific customizations. This approach lets you centralize shared settings in one place and maintain clear, organized overlays for each environment.

<Callout icon="lightbulb">
  Using overlays reduces configuration duplication and streamlines the management of different deployment environments. This approach ensures consistency across environments while allowing specific modifications as needed.
</Callout>

By understanding and utilizing Kustomize overlays, you can efficiently manage Kubernetes configurations across multiple environments, making your deployment workflows more robust and easier to maintain.

For more detailed information on how to implement and optimize Kustomize for your projects, consider exploring additional resources on [Kubernetes Documentation](https://kubernetes.io/docs/) and related tools.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/d02f6c7a-d704-4c64-b08b-d3ef01ee9a4d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/a2d3ef06-b264-41a2-8e13-2ec409afabfe" />
</CardGroup>
