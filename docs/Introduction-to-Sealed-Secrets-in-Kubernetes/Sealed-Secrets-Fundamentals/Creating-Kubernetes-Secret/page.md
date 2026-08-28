# Creating Kubernetes Secret

Source: https://notes.kodekloud.com/docs/Introduction-to-Sealed-Secrets-in-Kubernetes/Sealed-Secrets-Fundamentals/Creating-Kubernetes-Secret/page

This article explains how to create a Kubernetes Secret manifest and seal it for secure storage.

In this step, we’ll generate a standard Kubernetes Secret manifest that can later be sealed and encrypted with kubeseal. By outputting the YAML without applying it, you get full control over your secret definitions.

## 1. Generate the Secret YAML

Use the following command to create a generic Secret named `database` in the `default` namespace. The `DB_PASSWORD` key is set to `password123`.

```bash theme={null}
kubectl create secret generic database \
  -n default \
  --from-literal=DB_PASSWORD=password123 \
  --dry-run=client \
  -o yaml > secret.yaml
```

| Option                         | Description                                | Example                                  |
| ------------------------------ | ------------------------------------------ | ---------------------------------------- |
| `create secret generic <name>` | Creates a generic Secret resource          | `kubectl create secret generic database` |
| `-n <namespace>`               | Specifies the target namespace             | `-n default`                             |
| `--from-literal=KEY=VALUE`     | Adds literal key-value pairs to the Secret | `--from-literal=DB_PASSWORD=password123` |
| `--dry-run=client -o yaml`     | Outputs the manifest without applying it   | `--dry-run=client -o yaml`               |

<Callout icon="lightbulb">
  Kubernetes Secrets store data as base64-encoded strings, not encrypted values. Always seal or encrypt sensitive data before committing to version control.
</Callout>

## 2. Inspecting the Generated YAML

Your `secret.yaml` will look like this:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: database
  namespace: default
data:
  DB_PASSWORD: cGFzc3dvcmQxMjM=
```

## 3. Verifying the Base64 Encoding

To confirm the encoding, decode the `DB_PASSWORD` field:

```bash theme={null}
echo cGFzc3dvcmQxMjM= | base64 --decode
