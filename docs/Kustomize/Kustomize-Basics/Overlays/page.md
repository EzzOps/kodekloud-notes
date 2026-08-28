# or
kubectl apply -k k8s/
```

<Callout icon="lightbulb">
  `kubectl apply -k` invokes Kustomize natively—you don’t need the standalone binary.
</Callout>

## When the Resource List Grows

Adding more services (e.g., `cache/`, `kafka/`) quickly makes the root manifest unwieldy:

```text theme={null}
k8s/
├── api/
├── db/
├── cache/
│   ├── redis-config.yaml
│   ├── redis-depl.yaml
│   └── redis-service.yaml
└── kafka/
    ├── kafka-config.yaml
    ├── kafka-depl.yaml
    └── kafka-service.yaml
```

A flat list of ten or more files in one `kustomization.yaml` is hard to maintain.

## Nested kustomization.yaml Files

A cleaner pattern is to give each subdirectory its own `kustomization.yaml`:

**`k8s/api/kustomization.yaml`**

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - api-depl.yaml
  - api-service.yaml
```

**`k8s/db/kustomization.yaml`**

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - db-depl.yaml
  - db-service.yaml
```

Repeat for `cache/` and `kafka/`. Then simplify your root `kustomization.yaml`:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - api/
  - db/
  - cache/
  - kafka/
```

Deploy everything in one go:

```bash theme={null}
kubectl apply -k k8s/
# or
kustomize build k8s/ | kubectl apply -f -
```

This hierarchical layout keeps the root file concise and scales seamlessly.

## Command Reference

| Layout                    | Command                                      |
| ------------------------- | -------------------------------------------- |
| Flat folder               | `kubectl apply -f k8s/`                      |
| Single-root Kustomization | `kubectl apply -k k8s/`                      |
| Build then apply          | `kustomize build k8s/ \| kubectl apply -f -` |

## Links and References

* [Kustomize Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [kubectl apply](https://kubernetes.io/[AWS_SECRET_ACCESS_KEY]-commands#apply)
* [Kubernetes Manifests Guide](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[SECRET_REDACTED]-c5e2-4411-afc1-443d3f2ba735/lesson/4b621de0-dbb3-4f3c-a60b-6abfe7ba9e83" />
</CardGroup>


# Overlays

Source: https://notes.kodekloud.com/docs/Kustomize/Kustomize-Basics/Overlays/page

This guide explains how to use Overlays in Kustomize for managing environment-specific configurations while maintaining a shared base configuration.

In this guide, you’ll learn how to maintain a shared **base** configuration and apply environment-specific changes using **Overlays** in Kustomize. Overlays let you centralize common resources in a `base/` directory and then customize or extend them for `dev`, `stg`, `prod`, or any other environment.

<Frame>
  ![The image is a diagram labeled "Overlays" showing a hierarchy with "Env" at the top, branching into "dev," "stg," and "prod" environments.](https://kodekloud.com/kk-media/image/upload/v1752880924/notes-assets/images/Kustomize-Overlays/overlays-hierarchy-env-dev-stg-prod.jpg)
</Frame>

Below is a typical Kustomize directory layout:

```bash theme={null}
k8s/
├── base/
│   ├── kustomization.yaml
│   ├── nginx-depl.yaml
│   ├── service.yaml
│   └── redis-depl.yaml
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

| Directory     | Contents                                             | Purpose                                    |
| ------------- | ---------------------------------------------------- | ------------------------------------------ |
| base/         | `nginx-depl.yaml`, `service.yaml`, `redis-depl.yaml` | Shared deployments and services            |
| overlays/dev  | `config-map.yaml` + kustomization file               | Dev-specific patches (e.g., replica count) |
| overlays/stg  | `config-map.yaml` + kustomization file               | Staging tweaks                             |
| overlays/prod | `config-map.yaml` + kustomization file               | Production patches and extra resources     |

***

## 1. Base kustomization

The **base** holds all common Kubernetes manifests.

```yaml theme={null}
