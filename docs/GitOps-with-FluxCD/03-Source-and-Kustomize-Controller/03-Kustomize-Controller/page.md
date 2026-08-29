# NAME                                  READY  MESSAGE
# 4-demo-source-minio-s3-bucket-bb-app  True
```

> **triangle-alert** Storing credentials in plain text can be insecure. Consider using [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) or a vault in production.

***

## 7. Confirm Deployment in `4-demo`

Flux will now apply the manifests under the `4-demo` namespace:

```bash theme={null}
kubectl -n 4-demo get all
```

Example output:

```text theme={null}
NAME                                      READY   STATUS    RESTARTS   AGE
pod/block-buster-7f8c7c588f-xqf8k        1/1     Running   0          40s

NAME                                TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)         AGE
service/block-buster-service        NodePort   10.98.175.100    <none>        80:30004/TCP    40s

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/block-buster         1/1     1            1           40s
```

Access the application at [http://localhost:30004](http://localhost:30004). In version **7.4.0**, a new score counter updates whenever a brick is hit.

***

## Resources & References

| Resource       | Use Case                                | Documentation                                                                                        |
| -------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Flux Bucket    | Track S3 or HTTP directories as sources | [https://fluxcd.io/docs/components/source/bucket/](https://fluxcd.io/docs/components/source/bucket/) |
| Flux Kustomize | Declarative application deployment      | [https://fluxcd.io/docs/components/kustomize/](https://fluxcd.io/docs/components/kustomize/)         |
| MinIO          | S3-compatible object store              | [https://min.io/](https://min.io/)                                                                   |

* [FluxCD Documentation](https://fluxcd.io/docs/)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [GitOps with FluxCD](https://fluxcd.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/857e34cf-a086-433b-bf3b-88a5a5096a6f/lesson/8c58aa74-a8d6-4e4b-aa82-89fde8f37ff3)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/857e34cf-a086-433b-bf3b-88a5a5096a6f/lesson/30e47598-8a5d-49b0-801a-9aa449bf2cfa)


# Kustomize Controller

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Source-and-Kustomize-Controller/Kustomize-Controller/page

The Kustomize Controller ensures cluster state matches desired Kubernetes manifests by validating, applying, monitoring, and optionally pruning resources.

The **Kustomize Controller** is the Flux component that ensures your cluster’s actual state matches the desired state described by Kubernetes manifests. It retrieves artifacts from the Source Controller and then:

| Feature                      | Description                                                                 |
| ---------------------------- | --------------------------------------------------------------------------- |
| Validation                   | Checks your manifests against the Kubernetes API before applying changes.   |
| Apply / Update               | Creates or updates resources based on the desired state.                    |
| Health Assessment            | Monitors workloads to ensure they remain healthy after deployment.          |
| Pruning (Garbage Collection) | Optionally removes resources that no longer exist in your source manifests. |

> **lightbulb** Make sure you have installed [Flux](https://fluxcd.io/docs/installation/) and configured a `GitRepository` or other supported source.

## 1. Creating a Kustomization

Use the `flux create kustomization` command to link your source to a path containing Kustomize overlays. You can also enable garbage collection:

```bash theme={null}
flux create kustomization kustomization-app1 \
  --source=GitRepository/source-app1 \
  --path=./solar-system \
  --prune=true \
  --export > kustomization.yaml
```

The `--export` flag prints the `Kustomization` resource manifest:

```yaml theme={null}
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: kustomization-app1
  namespace: flux-system
spec:
  interval: 1m0s
  path: ./solar-system
  prune: true
  sourceRef:
    kind: GitRepository
    name: source-app1
```

Apply it with:

```bash theme={null}
kubectl apply -f kustomization.yaml
```

## 2. Automatic Build Behavior

If there’s no `kustomization.yaml` file under `./solar-system`, Flux will auto-generate one for you:

```bash theme={null}
kustomize create --autodetect --recursive --output kustomization.yaml
```

This populates `kustomization.yaml` with all discovered resources:

```yaml theme={null}
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
```

> **lightbulb** You don’t need to run the above command yourself—Flux performs it automatically when needed.

## 3. Providing Your Own Overlays

If you include a custom `kustomization.yaml` (or Kustomization overlay) in the specified path, the controller will skip auto-generation and apply your overlays directly. This allows you to:

* Add labels or annotations
* Patch existing resources
* Customize namespace or image tags

## 4. Checking Status

To inspect all active `Kustomization` resources and their reconciliation state:

```bash theme={null}
flux get kustomizations
```

Example output:

```plaintext theme={null}
NAME                   REVISION          SUSPENDED   READY   MESSAGE
flux-system            main/7e35674...   False       True    Applied revision: 'main/7e35674...'
kustomization-app1     main/1b31558...   False       True    Applied revision: 'main/1b31558...'
```

## Links and References

* [Flux Documentation](https://fluxcd.io/docs/)
* [Kustomize Official Site](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [GitRepository Source for Flux](https://fluxcd.io/docs/components/source/git/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/857e34cf-a086-433b-bf3b-88a5a5096a6f/lesson/ffda282a-fad8-47c2-912e-38b034592ed9)
