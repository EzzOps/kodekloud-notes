# Kustomize ApiVersion Kind

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Basics/Kustomize-ApiVersion-Kind/page

This article discusses the importance of specifying `apiVersion` and `kind` in `kustomization.yaml` for stability and compatibility in Kustomize.

## Kustomize: Specifying `apiVersion` and `kind`

When authoring your `kustomization.yaml`, explicitly declaring the `apiVersion` and `kind` fields is a recommended best practice. Although Kustomize infers sensible defaults when they’re omitted, specifying them ensures compatibility with future Kustomize releases and helps prevent unexpected breaking changes.

### Example `kustomization.yaml`

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
