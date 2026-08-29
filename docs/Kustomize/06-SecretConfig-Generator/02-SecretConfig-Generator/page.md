# kustomization.yaml
configMapGenerator:
  - name: db-cred
    literals:
      - password=password122
    options:
      labels:
        app-config: my-config
  - name: redis-cred
    literals:
      - password=password122
    options:
      labels:
        app-config: my-config
```

### Step 2: Update Your Generator

When you change a literal—e.g., updating the password—keep the same label:

```yaml theme={null}
# kustomization.yaml (after update)
configMapGenerator:
  - name: db-cred
    literals:
      - password=password1224
    options:
      labels:
        app-config: my-config
  - name: redis-cred
    literals:
      - password=password1224
    options:
      labels:
        app-config: my-config
```

### Step 3: Apply with Prune

Use the `--prune` flag along with `-l` to target your shared label:

```bash theme={null}
kubectl apply -k k8s/overlays/prod/ --prune -l app-config=my-config
```

<Callout icon="triangle-alert">
  `kubectl apply --prune` will delete **any** resource in the namespace matching the label selector that isn’t in the current Kustomize output. Make sure only intended resources use this label.
</Callout>

### Step 4: Verify Cleanup

After pruning, run:

```bash theme={null}
kubectl get configmap
```

You should now see only the active ConfigMaps:

```bash theme={null}
NAME                      DATA   AGE
db-cred-44h89htdm7        1      27m
kube-root-ca.crt          1      9d
redis-cred-c6k6d6bh64     1      2m7s
```

## Quick Reference

| Action                     | Command / Config Snippet                                     |
| -------------------------- | ------------------------------------------------------------ |
| Label generators           | `options.labels.app-config: my-config`                       |
| Apply with pruning         | `kubectl apply -k <overlay> --prune -l app-config=my-config` |
| List ConfigMaps post-prune | `kubectl get configmap`                                      |

## Further Reading

* [Kustomize Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [Prune Flag Guide](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kustomize/module/51823d3e-7be4-4792-836a-2c4690c0c547/lesson/f2d30e37-cef9-4725-97e9-69f2380e9a2d" />
</CardGroup>


# SecretConfig Generator

Source: https://notes.kodekloud.com/docs/Kustomize/SecretConfig-Generator/SecretConfig-Generator/page

Learn to use Kustomize generators for automatic Kubernetes rollouts triggered by configuration changes without manual commands.

In this tutorial, you’ll learn how to use Kustomize generators—both ConfigMap and Secret generators—to automatically trigger rollouts in Kubernetes when configuration changes. Kustomize appends a randomized suffix to generated resource names and updates all workload references at build time, ensuring seamless updates without manual `kubectl rollout` commands.

## How Kustomize Generators Work

When you define a generator in **Kustomize**, it outputs a standard Kubernetes resource—either a `ConfigMap` or a `Secret`—with a unique suffix added to the name. This suffix guarantees that any change in generator inputs produces a new resource, prompting Kubernetes to detect updates and redeploy your workloads.

Example: Generating a `ConfigMap` named `db-cred` with a literal key-value pair:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-cred-jj26gh
data:
  password: "password1"
```

Kustomize ensures uniqueness by appending `-jj26gh` to the base name.

Your Deployment or Pod spec references the generator by its base name (`db-cred`), and Kustomize will rewrite it to include the full suffix:

```yaml theme={null}
env:
- name: DB_PASSWORD
  valueFrom:
    configMapKeyRef:
      name: db-cred
      key: password
```

At build time, this becomes:

```yaml theme={null}
env:
- name: DB_PASSWORD
  valueFrom:
    configMapKeyRef:
      name: db-cred-jj26gh
      key: password
```

## Automatic Rollouts on Configuration Change

When you update the generator inputs—for instance, changing `password1` to `password2`—Kustomize generates a new `ConfigMap` (e.g., `db-cred-a477b`) and updates your Deployment spec accordingly:

```yaml theme={null}
