# Different Types of Patches

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Kustomize-Basics-2025-Updates/Different-Types-of-Patches/page

This guide explains how to define patches using JSON 6902 and strategic merge patch methods with inline and separate file approaches.

In this guide, we explain how to define patches using both JSON 6902 and strategic merge patch methods. There are two primary approaches to defining a patch:

1. Inline—where the patch is embedded directly within the kustomization.yaml file.
2. Separate File—where the patch is stored in an external YAML file, keeping the kustomization.yaml file clean and uncluttered.

Below are detailed examples for both methods.

***

## Inline Patch Definition

In the inline approach, the patch is directly embedded in your kustomization.yaml file. This method is ideal for simple or singular modifications. For example:

```yaml theme={null}
Kustomization:
  patches:
    - target:
        kind: Deployment
        name: api-deployment
      patch: |
        - op: replace
          path: /spec/replicas
          value: 5
```

> **lightbulb** Use inline patches for quick adjustments when you have only a few changes to manage.

***

## Separate File Patch Definition

Alternatively, you can store your patch in an external YAML file and reference it in your kustomization.yaml file. This approach is beneficial when dealing with multiple patches or when you want to keep your main configuration file streamlined.

In your kustomization.yaml file, reference the external patch file:

```yaml theme={null}
Kustomization:
  patches:
    - path: replica-patch.yaml
      target:
        kind: Deployment
        name: nginx-deployment
```

And here is how the external file named replica-patch.yaml might look:

```yaml theme={null}
- op: replace
  path: /spec/replicas
  value: 5
```

> **lightbulb** Using a separate file for patches enhances readability and maintainability when working with complex configurations.

***

## Strategic Merge Patches

You can apply the same methodologies when working with strategic merge patches. Below are examples for both inline and separate file approaches.

### Inline Approach for Strategic Merge Patch

Embed the strategic merge patch directly into your configuration:

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

### Separate File Approach for Strategic Merge Patch

Reference an external patch file in your kustomization.yaml:

```yaml theme={null}
patches:
  - path: replica-patch.yaml
    target:
      kind: Deployment
      name: nginx-deployment
```

And in the external replica-patch.yaml:

```yaml theme={null}
- op: replace
  path: /spec/replicas
  value: 5
```

For a strategic merge patch defined as a complete resource patch in a single YAML block, consider this inline approach:

```yaml theme={null}
patches: |
  - patch: |
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: api-deployment
      spec:
        replicas: 5
```

Or reference the complete resource patch from an external file:

```yaml theme={null}
patches:
  - replica-patch.yaml
```

> **triangle-alert** Always ensure that your patch operations accurately reflect the intended changes to avoid potential misconfigurations.

***

## Conclusion

Choose the inline method for simplicity when only a few patches are needed, or opt for the separate file approach to maintain a cleaner and more manageable kustomization.yaml—especially when dealing with multiple or complex patches.

For further details on patching strategies and best practices, refer to the [Kustomize documentation](https://github.com/kubernetes-sigs/kustomize).

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/031e84b8-bcbc-4f39-94d6-66d93b05bddc/lesson/1b0aa541-7251-472c-89f3-8763fee58898)
