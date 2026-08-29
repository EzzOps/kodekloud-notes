# Image Transformers

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Basics/Image-Transformers/page

Leverage Kustomize’s image transformer to override container images in Kubernetes manifests while maintaining original YAML files.

Leverage Kustomize’s image transformer to override container images in your Kubernetes manifests without touching the original YAML files. This approach keeps your base configurations DRY and promotes reusability across environments.

## Prerequisites

* Kubernetes cluster or local setup (e.g., Docker Desktop, Minikube)
* `kubectl` v1.18+
* Kustomize v3.2+ (bundled with `kubectl` since v1.14)

For more details, see [Kubernetes Documentation](https://kubernetes.io/docs/) and [Kustomize Official Guide](https://kubectl.docs.kubernetes.io/guides/kustomize/).

***

## 1. Replace the Image Name

Suppose you have a Deployment manifest (`deployment.yaml`) deploying an NGINX container:

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

To swap `nginx` for `haproxy`, create a `kustomization.yaml` in the same directory:

```yaml theme={null}
images:
  - name: nginx
    newName: haproxy
```

Run the build command:

```shell theme={null}
kustomize build .
```

Kustomize will find every `nginx` image reference and replace it with `haproxy`. The rendered Deployment becomes:

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

> **lightbulb** The `name` field under `images` matches the image name from your resources, **not** the container name in the Pod spec.

***

## 2. Change Only the Image Tag

If you want to keep `nginx` but bump its version tag to `2.4`, specify `newTag` instead:

```yaml theme={null}
images:
  - name: nginx
    newTag: 2.4
```

After `kustomize build .`, the Deployment’s container image updates to:

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

## 3. Combine Image Name and Tag Changes

You can simultaneously override both the repository and the tag:

```yaml theme={null}
images:
  - name: nginx
    newName: haproxy
    newTag: 2.4
```

The resulting manifest will then reference `haproxy:2.4`:

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
          image: haproxy:2.4
```

***

## Image Transformer Fields

| Field   | Description                           | Example   |
| ------- | ------------------------------------- | --------- |
| name    | Original image name in your resources | `nginx`   |
| newName | Replacement image repository or name  | `haproxy` |
| newTag  | New version tag for the image         | `2.4`     |

> **triangle-alert** Omitting both `newName` and `newTag` in an `images` entry has no effect. Ensure at least one property is set.

***

## Links and References

* [Kustomize Image Transformer](https://kubectl.docs.kubernetes.io/references/kustomize/image/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [kubectl Customization](https://kubectl.docs.kubernetes.io/guides/introduction/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kustomize/module/8b591384-c5e2-4411-afc1-443d3f2ba735/lesson/d01d540c-4e1c-45ad-aa72-2b0c46e8f68c)
