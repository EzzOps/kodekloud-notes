# JSON 6902 Patch:
kustomization:
  patches:
    - target:
        kind: Deployment
        name: api-deployment
      patch: |
        - op: replace
          path: /spec/replicas
          value: 5
```

### 2. Strategic Merge Patch

This approach resembles a standard Kubernetes configuration file. You provide a snippet that mirrors the original resource configuration and includes only the fields to be updated:

```yaml theme={null}
# Strategic Merge Patch:
kustomization:
  patches:
    - patch: |
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: api-deployment
        spec:
          replicas: 5
```

With the strategic merge patch, Kustomize merges the provided snippet with the original configuration, ensuring that only the specified fields are updated.

<Callout icon="lightbulb">
  Both JSON 6902 and strategic merge patches are valid options. Choose JSON 6902 for detailed control when you need explicit patch operations, or opt for strategic merge patches for a more readable and Kubernetes-native configuration style.
</Callout>

## Summary

Patches in Kustomize allow for precise modifications to Kubernetes objects by specifying:

* **Operation Type**: Determines whether to add, remove, or replace a value.
* **Target**: Defines the resource(s) the patch applies to using specific matching criteria.
* **Value**: Contains the updated data or new configuration value.

This article detailed examples for renaming a deployment and updating replica counts and compared the JSON 6902 and strategic merge patch methods. Both approaches offer unique advantages, empowering you to choose the best fit for your Kubernetes configuration management needs.

For more information on Kubernetes configurations and patching strategies, refer to the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/3c149071-8b87-45e0-9fd5-850f0440ff4b" />
</CardGroup>


# Patches list

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Patches-List/page

This article explores methods for managing list operations in Kubernetes configurations, including removing, replacing, and adding items using patches.

In this article, we explore several methods for managing list operations in Kubernetes configurations. Specifically, you'll learn how to remove, replace, and add items using patches. We begin with a deployment configuration that includes a single container named "nginx" running the "nginx" image. Since the containers are defined as a list (indicated by the dash before each item), you can easily extend the configuration to include multiple containers if needed.

Below is the initial deployment configuration:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: api
  template:
    metadata:
      labels:
        component: api
    spec:
      containers:
      - name: nginx
        image: nginx
```

## Replacing a Container Using a JSON 6902 Patch

To update the container by changing its name and image, you can use a JSON 6902 patch. In your `kustomization.yaml` file, the patch targets the specific Deployment object and applies a replace operation on the container at index 0. Remember that list indexes start at 0; hence, the first (and only) container is at index 0.

```yaml theme={null}
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: replace
        path: /spec/template/spec/containers/0
        value:
          name: haproxy
          image: haproxy
```

After applying this patch, the "nginx" container is updated to have the name "haproxy" and image "haproxy".

## Replacing a Container Using a Strategic Merge Patch

Alternatively, a strategic merge patch can update a container. With this method, you create a separate patch file (for example, `label-patch.yaml`) that specifies the container properties to be merged with the original configuration. The patch file identifies the container by name (in this case, "nginx") and details the new image.

Assuming your original deployment configuration is as shown above, your `label-patch.yaml` might look like this:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    spec:
      containers:
      - name: nginx
        image: haproxy
```

In your `kustomization.yaml` file, reference the patch as follows:

```yaml theme={null}
patches:
  - label-patch.yaml
```

This approach instructs Kustomize to locate the container named "nginx" and update its image to "haproxy".

## Adding a Container to the List Using a JSON 6902 Patch

To add a second container to your Deployment, you can use a JSON 6902 patch with an "add" operation. The dash (`-`) at the end of the path indicates that the new container should be appended to the existing list.

Given the initial one-container configuration, the following patch adds a second container:

```yaml theme={null}
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: add
        path: /spec/template/spec/containers/-
        value:
          name: haproxy
          image: haproxy
```

In this patch, the dash after `containers/` signals Kustomize to append the new container. After applying the patch, the Deployment will include two containers: the original "nginx" container and the added "haproxy" container.

Below is a representation of the final configuration after adding the new container:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: api
  template:
    metadata:
      labels:
        component: api
    spec:
      containers:
        - name: nginx
          image: nginx
        - name: haproxy
          image: haproxy
```

## Deleting a Container from the List Using a JSON 6902 Patch

Next, we demonstrate how to remove an item from the list. Consider a Deployment configuration with two containers—one named "web" running nginx and another named "database" running mongo:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: api
  template:
    metadata:
      labels:
        component: api
    spec:
      containers:
        - name: web
          image: nginx
        - name: database
          image: mongo
```

To remove the second container (i.e., the "database" container), apply the following patch. Since list indexes are zero-based, the "database" container is at index 1:

```yaml theme={null}
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch:
      - op: remove
        path: /spec/template/spec/containers/1
```

After applying this patch, only the "web" container remains in the configuration.

<Callout icon="lightbulb">
  If you are working with multiple containers, always verify the correct index of the container you want to modify. Misidentifying the index can lead to unexpected configuration errors.
</Callout>

## Deleting a Container Using a Strategic Merge Patch

Another method to remove a container is by using a strategic merge patch. In this approach, you create a patch file (for example, `label-patch.yaml`) and leverage the `$patch: delete` directive, which explicitly marks the container for removal. Using the previous configuration that contains both "web" and "database" containers, the patch to delete the "database" container is as follows:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    spec:
      containers:
      - $patch: delete
        name: database
```

Then, reference the patch file in your `kustomization.yaml` like so:

```yaml theme={null}
patches:
  - label-patch.yaml
```

This configuration instructs Kustomize to remove the container with the name "database", leaving only the "web" container in your Deployment.

***

Each patch example in this guide illustrates how to manipulate list items in a Kubernetes configuration—whether replacing, adding, or deleting containers—using both JSON 6902 patches and strategic merge patches. For more information on Kubernetes patching techniques, please refer to the [Kubernetes Documentation](https://kubernetes.io/docs/).

Happy patching!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/5e018d72-ca12-47c0-9816-5bde98ec4ca5" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/919f7a3a-8ba1-4c84-a363-2108c51fff1d" />
</CardGroup>
