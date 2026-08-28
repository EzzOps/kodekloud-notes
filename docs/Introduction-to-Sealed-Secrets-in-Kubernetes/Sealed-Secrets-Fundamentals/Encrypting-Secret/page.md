# password123
```

## 4. Next Steps: Sealing the Secret

Now that you have `secret.yaml`, pass it through kubeseal to produce a secure SealedSecret:

```bash theme={null}
kubeseal --format yaml < secret.yaml > sealedsecret.yaml
```

This encrypted manifest can be safely stored in Git and applied to any cluster that holds your Sealed Secrets key.

***

## References

* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
* [Sealed Secrets (kubeseal)](https://github.com/bitnami-labs/sealed-secrets)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes/module/0f3ed562-f151-48f9-bb8c-8d3a4dbb4fc3/lesson/0c6da7ae-2f36-40a2-9d6e-5dccdb4ed8d3" />
</CardGroup>


# Encrypting Secret

Source: https://notes.kodekloud.com/docs/Introduction-to-Sealed-Secrets-in-Kubernetes/Sealed-Secrets-Fundamentals/Encrypting-Secret/page

This guide explains how to use Bitnami Sealed Secrets to encrypt Kubernetes Secret manifests for secure storage in Git repositories.

In this guide, you'll learn how to use the Bitnami Sealed Secrets controller to safely encrypt a Kubernetes `Secret` manifest. Sealed Secrets allow you to store encrypted secrets in Git repositories without exposing sensitive data.

## Prerequisites

* A running Kubernetes cluster
* `kubectl` configured to communicate with your cluster
* [Sealed Secrets controller](https://github.com/bitnami/sealed-secrets) deployed (e.g., via Helm or `kubectl apply`)
* `kubeseal` CLI installed locally

<Callout icon="lightbulb">
  Ensure the `kubeseal` client version matches your controller version. Mismatched versions can lead to encryption or decryption errors.
</Callout>

## Step 1: Prepare Your Secret Manifest

Create a file named `secret.yaml` containing your sensitive data in Kubernetes `Secret` format:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: database
  namespace: default
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=  # base64-encoded string
```

## Step 2: Encrypt the Secret

Run the following command to generate a `SealedSecret` resource from your `secret.yaml`. The encrypted output is written to `sealed-secret.yaml`:

```bash theme={null}
kubeseal \
  --controller-name my-release-sealed-secrets \
  --controller-namespace kube-system \
  --format yaml \
  < secret.yaml \
  > sealed-secret.yaml
```

### Flag Reference

| Flag                     | Description                                     | Example                     |
| ------------------------ | ----------------------------------------------- | --------------------------- |
| `--controller-name`      | Name of the Sealed Secrets controller release   | `my-release-sealed-secrets` |
| `--controller-namespace` | Namespace where the controller is running       | `kube-system`               |
| `--format`               | Output format (yaml or json)                    | `yaml`                      |
| `< secret.yaml`          | Reads your original Kubernetes Secret manifest  | —                           |
| `> sealed-secret.yaml`   | Writes the encrypted SealedSecret to a new file | —                           |

## Step 3: Review the SealedSecret

Open `sealed-secret.yaml` to verify its contents. It should look similar to this:

```yaml theme={null}
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: database
  namespace: default
spec:
  encryptedData:
    DB_PASSWORD: AgAKG7A3zkILGotJJq+...Tb
```

The `encryptedData` field contains the fully encrypted payload. Since this data is encrypted with the controller’s public key, it’s safe to commit to version control.

<Callout icon="triangle-alert">
  Do **not** include the original `secret.yaml` in your Git repository. Only commit the generated `sealed-secret.yaml`.
</Callout>

## Next Steps

1. Apply the SealedSecret to your cluster:
   ```bash theme={null}
   kubectl apply -f sealed-secret.yaml
   ```
2. Verify that the controller has created the unsealed `Secret`:
   ```bash theme={null}
   kubectl get secret database -n default -o yaml
   ```
3. Reference the `Secret` in your Deployment or Pod specs as usual.

***

## Links and References

* [Bitnami Sealed Secrets GitHub](https://github.com/bitnami/sealed-secrets)
* [Installing Sealed Secrets Controller](https://github.com/bitnami/sealed-secrets#installing)
* [kubeseal CLI Usage](https://github.com/bitnami/sealed-secrets#client)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-sealed-secrets-in-kubernetes/module/0f3ed562-f151-48f9-bb8c-8d3a4dbb4fc3/lesson/b9921e8d-59e5-4805-98e5-1bc020c290f6" />
</CardGroup>
