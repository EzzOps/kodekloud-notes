# Patches Intro

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Patches-Intro/page

This article explores customized patches for modifying Kubernetes configurations, enabling precise changes to specific objects or fields without affecting the entire configuration.

In this article, we explore how customized patches provide a surgical approach to modifying Kubernetes configurations. Unlike common transformers that apply changes broadly (e.g., assigning a label or namespace to all objects), patches enable you to target specific objects—or even individual fields within an object. For example, if you need to update the replica count in a deployment, a patch lets you modify only that value.

To create a patch, you must provide three components:

1. **Operation Type**\
   This specifies the action you want to perform. The three most common operations are:

   * **add**: Introduces a new element. For instance, adding a container to an existing list.
   * **remove**: Eliminates an existing element, such as taking away a container or label.
   * **replace**: Substitutes an existing value with a new one. For example, changing the replica count from 5 to 10.

2. **Target**\
   The target defines the match criteria for determining which Kubernetes object(s) the patch should apply to. This may include properties such as kind, version, name, namespace, label selectors, or annotation selectors. You can combine multiple criteria to precisely identify the desired resource(s).

3. **Value**\
   This represents the new data to add or use for replacement. Note that if the operation is `remove`, no value is required.

Below is an example that demonstrates these concepts using a Kustomize patch.

***

Consider the following sample deployment configuration in `deployment.yaml`, where the deployment's name is currently set to "api-deployment". The goal is to update it to "web-deployment".

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

The corresponding patch defined in `kustomization.yaml` is shown below:

```yaml theme={null}
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: replace
        path: /metadata/name
        value: web-deployment
```

In this inline patch:

* The `|-` introduces the patch details.
* `op` specifies the operation (in this case, replace).
* `path` points to the YAML property you want to change – here, `/metadata/name`.
* `value` provides the new value ("web-deployment").

After applying this patch, the deployment configuration is updated as follows:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
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

***

> **lightbulb** Patches are especially useful when you need to make precise, minimal modifications without affecting the entire configuration. This helps in managing changes in large-scale deployments.

## Example: Updating the Replica Count

Let's explore another scenario. Suppose you want to update the replica count from 1 to 5 in your deployment. The original `deployment.yaml` looks like this:

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

You can define the patch in `kustomization.yaml` as follows:

```yaml theme={null}
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |
      - op: replace
        path: /spec/replicas
        value: 5
```

In this example, the path `/spec/replicas` pinpoints the replica count field under the spec, which is then updated with the new value.

***

## Two Methods for Defining Patches

Kustomize supports two primary methods for defining patches:

### 1. JSON 6902 Patch

This method explicitly specifies both the target and patch details using JSON patch semantics. For example:

```yaml theme={null}
