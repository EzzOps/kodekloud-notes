# Inline patch for api-deployment
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
```

### Referencing an External Patch File

Alternatively, you can reference a separate file. In this example, the external file (`replica-patch.yaml`) is used for the "nginx-deployment":

```yaml theme={null}
# Reference to an external file for nginx-deployment
patches:
  - path: replica-patch.yaml
    target:
      kind: Deployment
      name: nginx-deployment
```

In the external file (`replica-patch.yaml`), the patch is defined as follows:

```yaml theme={null}
- op: replace
  path: /spec/replicas
  value: 5
```

## Strategic Merge Patches

For strategic merge patches, you can similarly choose between inline definitions or referencing an external file.

### Inline Strategic Merge Patch in kustomization.yaml

The following example shows an inline strategic merge patch for the "api-deployment":

```yaml theme={null}
patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: api-deployment
      spec:
        replicas: 5
```

### Using an External YAML File for Strategic Merge Patch

To reference a file for a strategic merge patch, simply include the file path in your kustomization.yaml:

```yaml theme={null}
patches:
  - path: replica-patch.yaml
```

<Callout icon="lightbulb">
  Both inline definitions and separate patch files are valid options. Choose the approach that best suits your project structure and maintenance preferences.
</Callout>

## Summary Table

| Patch Type            | Inline Example                                         | External File Example                          |
| --------------------- | ------------------------------------------------------ | ---------------------------------------------- |
| JSON 6902 Patch       | Inline definition in kustomization.yaml as shown above | Reference external file (`replica-patch.yaml`) |
| Strategic Merge Patch | Inline definition in kustomization.yaml as shown above | Reference external file (`replica-patch.yaml`) |

Using external patch files is particularly beneficial if you have a high number of patches or if you want to keep your kustomization.yaml lean and easy to manage.

For more in-depth information and best practices on patching in Kubernetes, explore the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/1b0aa541-7251-472c-89f3-8763fee58898" />
</CardGroup>


# Image Transformers

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Image-Transformers/page

This guide demonstrates how to leverage Kustomize's image transformer for efficient container image and tag modifications in Kubernetes manifests.

In this article, we explore how to modify container images in Kubernetes manifests using Kustomize image transformers. This powerful technique enables you to update image references—and even image tags—in your deployment files without editing them manually.

Below is an example deployment manifest (deployment.yaml) for an Nginx server:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: web
  template:
    metadata:
      labels:
        component: web
    spec:
      containers:
      - name: web
        image: nginx
```

To modify the image used by this deployment, create a Kustomize image transformer in a file named `kustomization.yaml`. In the transformer, the `name` property specifies the image to search for (in this case, "nginx"), and the `newName` property defines the replacement image. For example, to replace Nginx with HAProxy, use the following configuration:

```yaml theme={null}
images:
- name: nginx
  newName: haproxy
```

The image transformer scans all Kubernetes configuration files for containers using an image named "nginx" and replaces it with "haproxy."

<Callout icon="lightbulb">
  The `name` field in the `kustomization.yaml` file strictly refers to the image name and is not related to the container name specified in the deployment manifest.
</Callout>

After applying this transformation, the deployment manifest is updated so that the container image changes from "nginx" to "haproxy." The modified deployment appears as follows:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: web
  template:
    metadata:
      labels:
        component: web
    spec:
      containers:
      - name: web
        image: haproxy
```

***

## Changing the Image Tag

If you want to update only the image tag without switching the image itself, the image transformer can modify the tag value. Begin with the original deployment manifest:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: web
  template:
    metadata:
      labels:
        component: web
    spec:
      containers:
      - name: web
        image: nginx
```

Next, update your `kustomization.yaml` to specify the new tag:

```yaml theme={null}
images:
- name: nginx
  newTag: 2.4
```

Once applied, the container image in the deployment is updated to include the new tag, yielding the following transformed manifest:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: web
  template:
    metadata:
      labels:
        component: web
    spec:
      containers:
      - name: web
        image: nginx:2.4
```

***

## Combining Image and Tag Transformations

You can perform both image name and tag transformations simultaneously in a single `kustomization.yaml` file. For instance, if you want to change the Nginx image to HAProxy and update its tag to "2.4," use the following configuration:

```yaml theme={null}
images:
- name: nginx
  newName: haproxy
  newTag: 2.4
```

After applying this configuration, the final deployment manifest will feature the container image updated to "haproxy:2.4."

***

This guide demonstrates how to leverage Kustomize's image transformer for efficient container image and tag modifications, ensuring a consistent deployment process while minimizing manual edits.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/2503ab74-a871-4b65-a677-7180c001d5c5/lesson/632a781d-9494-4120-80d3-e7e86b4e88cf" />
</CardGroup>
