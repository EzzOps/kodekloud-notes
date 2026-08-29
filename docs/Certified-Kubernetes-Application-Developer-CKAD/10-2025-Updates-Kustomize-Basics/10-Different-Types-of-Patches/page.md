# Different Types of Patches

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/2025-Updates-Kustomize-Basics/Different-Types-of-Patches/page

This article explains methods for defining patches in Kubernetes using JSON 6902 and strategic merge patches, with options for inline or external file references.

This article explains two methods for defining patches in Kubernetes: JSON 6902 patches and strategic merge patches. You have the flexibility to define patches either inline within the kustomization.yaml file or by referencing external patch files. Inline patches consolidate everything in one file, while external files keep your kustomization.yaml concise, especially when managing numerous patches.

## JSON 6902 Patches

### Inline Definition in kustomization.yaml

Below is an example of an inline patch applied to the "api-deployment":

```yaml theme={null}
