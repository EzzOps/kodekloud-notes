# Wait a few seconds…
kubectl -n database get secret secret-mysql
```

FluxCD detects the drift and re-applies the manifest, recreating the Secret.

***

## 3. Suspend Reconciliation

Pause the `Kustomization` so FluxCD stops reconciling this directory:

```bash theme={null}
flux suspend kustomization infra-database-kustomize-git-mysql
flux get kustomization infra-database-kustomize-git-mysql
```

Now, deleting the Secret **will not** trigger re-creation:

```bash theme={null}
kubectl -n database delete secret secret-mysql
kubectl -n database get secrets
```

***

## 4. Trigger Pod Failure

Force a deployment restart to spawn a new Pod, which will fail due to the missing Secret:

```bash theme={null}
kubectl -n database rollout restart deployment mysql
kubectl -n database get pods -w
```

Observe a `CreateContainerConfigError`:

```bash theme={null}
kubectl -n database describe pod mysql-*
# ...
# Warning  Failed  Error: cannot find secret "secret-mysql"
```

***

## 5. Encrypt the Secret with kubeseal

Ensure you have:

* The [`kubeseal`](https://github.com/bitnami-labs/sealed-secrets#kubeseal) CLI installed.
* The Sealed Secrets public key (`sealed-secrets.pub`).

Encrypt the existing Secret manifest:

```bash theme={null}
kubeseal --cert ../../sealed-secrets.pub \
  --scope cluster-wide \
  -o yaml < secret-mysql.yaml > sealed-secret-mysql.yaml
```

This creates a `SealedSecret` resource:

```yaml theme={null}
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: secret-mysql
  namespace: database
  annotations:
    sealedsecrets.bitnami.com/cluster-wide: "true"
spec:
  encryptedData:
    password: AgBv9SokhhVk4WNdTmmPxd9D0J2ETJY...
  template:
    metadata:
      name: secret-mysql
      namespace: database
```

<Callout icon="lightbulb">
  Only the Secret’s values are encrypted. The keys (`password`) stay in cleartext for mapping.
</Callout>

***

## 6. Replace the Plaintext Secret

Backup the original manifest and commit the sealed version:

```bash theme={null}
mv secret-mysql.yaml secret-mysql.yaml.bak
git add sealed-secret-mysql.yaml
git commit -m "Add SealedSecret for MySQL password"
git push
```

***

## 7. Resume Reconciliation

Sync your Git source and resume the Kustomization:

```bash theme={null}
flux reconcile source git flux-system
flux resume kustomization infra-database-kustomize-git-mysql
```

FluxCD applies the `SealedSecret`, and the Bitnami controller decrypts it into a normal Kubernetes Secret in `database`.

***

## 8. Verify the Decrypted Secret

Check that the Secret has been created:

```bash theme={null}
kubectl -n database get secret secret-mysql
```

Decode and inspect the password:

```bash theme={null}
kubectl -n database get secret secret-mysql -o jsonpath='{.data.password}' | base64 -d
# => mysql-password-0123456789
```

Confirm the Pod is now running:

```bash theme={null}
kubectl -n database get pods
```

***

## 9. Conclusion

You have successfully:

1. Suspended FluxCD reconciliation.
2. Deleted a plaintext Secret and saw a Pod failure.
3. Used `kubeseal` to create an encrypted `SealedSecret`.
4. Committed the `SealedSecret` to your Git repo.
5. Resumed FluxCD reconciliation and verified automatic decryption.

By integrating Bitnami Sealed Secrets with FluxCD and Kustomize, you can store encrypted secrets in Git, maintain GitOps workflows, and ensure secrets only decrypt inside your Kubernetes cluster.

***

## Links and References

* [Bitnami Sealed Secrets GitHub](https://github.com/bitnami-labs/sealed-secrets)
* [FluxCD Kustomization Documentation](https://fluxcd.io/docs/components/kustomize/kustomization/)
* [Kustomize Tooling](https://kubectl.docs.kubernetes.io/guides/introduction/kustomization/)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/ab6dc091-5ddd-40ce-935b-09d5f0f091c6" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitops-with-fluxcd/module/c8ad2608-2804-4413-9041-5e8dc9126d53/lesson/05fbab53-e949-4d5f-aadc-8ba1950fbc5c" />
</CardGroup>


# DEMO Install Cosign

Source: https://notes.kodekloud.com/docs/GitOps-with-FluxCD/Secret-Management-Sign-Verification/DEMO-Install-Cosign/page

This tutorial covers installing Cosign for signing OCI artifacts and configuring Flux CD for secure supply chain workflows.

In this tutorial, you’ll install Sigstore’s Cosign binary, verify your setup, generate a key pair for signing OCI artifacts, and configure Flux CD to use the Cosign public key. By following these steps, you’ll enable secure supply chain workflows for container images.

## Verify Cosign Is Not Installed

First, confirm Cosign isn’t already available:

```bash theme={null}
root@host:~# cosign version
bash: cosign: command not found
```

<Callout icon="lightbulb">
  Seeing `command not found` means Cosign isn’t installed. Continue to the installation methods below.
</Callout>

## Installation Options

Cosign is part of the [Sigstore project](https://sigstore.dev). Choose the method that best fits your environment:

| Method            | Use Case                | Example Command                        |
| ----------------- | ----------------------- | -------------------------------------- |
| Standalone Binary | Quick install on Linux  | Download, move to PATH, set executable |
| RPM Package       | RPM-based Linux distros | `sudo rpm -Uvh cosign-*.rpm`           |
| DEB Package       | Debian/Ubuntu systems   | `sudo dpkg -i cosign_*.deb`            |

### 1. Standalone Binary

```bash theme={null}
