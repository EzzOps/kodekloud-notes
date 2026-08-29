# Deploy the Sealed Secrets Operator

Source: https://notes.kodekloud.com/docs/Introduction-to-Sealed-Secrets-in-Kubernetes/Sealed-Secrets-Fundamentals/Deploy-the-Sealed-Secrets-Operator/page

This guide explains how to install the Sealed Secrets Operator using Helm and securely manage Kubernetes Secrets.

Safely encrypt your Kubernetes Secrets using the [Sealed Secrets Operator](https://github.com/bitnami-labs/sealed-secrets). This guide walks you through installing the operator via Helm, fetching its public key, and sealing a Secret.

<Callout icon="lightbulb">
  * Helm 3.x installed
  * `kubectl` configured with access to your target cluster
  * Cluster-admin privileges (or equivalent)
</Callout>

## 1. Add the Sealed-Secrets Helm Repository

Register the Bitnami Sealed Secrets chart and update your local repo cache:

```bash theme={null}
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm repo update
```

## 2. Install the Sealed-Secrets Chart

Choose between installing into the default namespace or a custom namespace.

| Installation Scope                    | Helm Command                                                           |
| ------------------------------------- | ---------------------------------------------------------------------- |
| Default Namespace                     | `helm install my-release sealed-secrets/sealed-secrets`                |
| Custom Namespace (e.g. `kube-system`) | `helm install my-release sealed-secrets/sealed-secrets -n kube-system` |

## 3. Verify the Operator Pod

Confirm that the Sealed Secrets controller is running:

| Namespace                   | Command                           |
| --------------------------- | --------------------------------- |
| Default                     | `kubectl get pods`                |
| Custom (e.g. `kube-system`) | `kubectl get pods -n kube-system` |

You should see a pod like `my-release-sealed-secrets-controller-<id>` in `Running` status.

## 4. Fetch the Controller’s Public Key

Download the operator’s certificate to seal Secrets locally. Replace `<release-name>` and `<namespace>` as needed:

```bash theme={null}
kubeseal \
  --controller-name=my-release-sealed-secrets-controller \
  --controller-namespace=kube-system \
  --fetch-cert \
  > mycert.pem
```

<Callout icon="lightbulb">
  If you installed into the default namespace, omit `--controller-namespace` or set it to `default`.
</Callout>

## 5. Create and Seal a Secret

1. **Generate a Kubernetes Secret manifest** (client-side dry run):

   ```bash theme={null}
   kubectl create secret generic secret-name \
     --from-literal=foo=bar \
     --dry-run=client \
     -o yaml \
     > secret.yaml
   ```

2. **Seal the Secret** using the fetched certificate:

   ```bash theme={null}
   kubeseal \
     --format yaml \
     --cert mycert.pem \
     < secret.yaml \
     > mysealedsecret.yaml
   ```

3. **Apply the SealedSecret** to your cluster:

   ```bash theme={null}
   kubectl apply -f mysealedsecret.yaml
   ```

## 6. Confirm Deployment

Ensure the Sealed Secrets Operator is still running after sealing:

| Namespace                   | Command                           |
| --------------------------- | --------------------------------- |
| Default                     | `kubectl get pods`                |
| Custom (e.g. `kube-system`) | `kubectl get pods -n kube-system` |

Once verified, your Sealed Secrets Operator is ready to encrypt and manage Kubernetes Secrets securely!

***

## Links and References

* [Sealed-Secrets GitHub](https://github.com/bitnami-labs/sealed-secrets)
* [Helm Documentation](https://helm.sh/docs/)
* [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes/module/0f3ed562-f151-48f9-bb8c-8d3a4dbb4fc3/lesson/287c3990-00f9-4090-96ed-0d4797afc898" />
</CardGroup>
