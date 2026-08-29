# Adds a ConfigMap to the kustomization file
kustomize edit add configmap NAME --from-literal=k=v

# Sets the nameprefix field
kustomize edit set nameprefix <prefix-value>

# Sets the namesuffix field
kustomize edit set namesuffix <suffix-value>
```

## Key Subcommands

| Subcommand    | Action                                |
| ------------- | ------------------------------------- |
| `edit set`    | Modify existing fields                |
| `edit add`    | Add generators, resources, or plugins |
| `edit remove` | Remove items from the kustomization   |

***

## edit set

Use `kustomize edit set` to change fields in your `kustomization.yaml` without editing it by hand.

### Change an image tag

```bash theme={null}
kustomize edit set image nginx=nginx:1.2.2
```

Resulting entry:

```yaml theme={null}
images:
- name: nginx
  newTag: 1.2.2
```

### Set or update a namespace

```bash theme={null}
kustomize edit set namespace staging
```

Produces:

```yaml theme={null}
namespace: staging
```

<Callout icon="lightbulb">
  This command only updates your `kustomization.yaml`. It does **not** apply changes to your cluster.
</Callout>

### Add common labels

```bash theme={null}
kustomize edit set label org=KodeKloud env=staging
```

Yields:

```yaml theme={null}
commonLabels:
  org: KodeKloud
  env: staging
```

### Set replica count for a Deployment

```bash theme={null}
kustomize edit set replicas nginx-deployment=5
```

Adds:

```yaml theme={null}
replicas:
- name: nginx-deployment
  count: 5
```

***

## edit add

The `add` subcommands let you generate ConfigMaps, Secrets, and include additional resources.

### Add a ConfigMap generator

```bash theme={null}
kustomize edit add configmap db-creds \
  --from-literal=password=password1 \
  --from-literal=username=root
```

Generates:

```yaml theme={null}
configMapGenerator:
- name: db-creds
  literals:
  - password=password1
  - username=root
```

### Add a Secret generator

```bash theme={null}
kustomize edit add secret my-secret \
  --from-literal=login=user1 \
  --from-literal=password=mypassword
```

Produces:

```yaml theme={null}
secretGenerator:
- name: my-secret
  type: Opaque
  literals:
  - login=user1
  - password=mypassword
```

### Add a resource

Include external YAML manifests in your kustomization:

```bash theme={null}
kustomize edit add resource db/db-depl.yaml
```

Results in:

```yaml theme={null}
resources:
- db/db-depl.yaml
```

***

## Which `kustomization.yaml` Gets Updated?

If your project uses multiple overlays or bases, the file modified depends on where you run the command:

```bash theme={null}
cd k8/base
kustomize edit set label org=KodeKloud
cd ../overlays/prod
kustomize edit set namespace prod
# Updates k8/overlays/prod/kustomization.yaml
```

If there’s no `kustomization.yaml` in your current directory, you’ll see an error.

***

## Links and References

* [Kustomize Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [Kubernetes Configuration](https://kubernetes.io/docs/concepts/overview/config-management/)
* [GitHub: kustomize](https://github.com/kubernetes-sigs/kustomize)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kustomize/module/060e95ac-e56c-42ed-be87-8701328432c3/lesson/e18c8a87-99db-439e-a8bc-bff7cc658853" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kustomize/module/060e95ac-e56c-42ed-be87-8701328432c3/lesson/f83fd542-9130-4e60-8e67-ed2d7548d895" />
</CardGroup>


# Garbage Collection

Source: https://notes.kodekloud.com/docs/Kustomize/SecretConfig-Generator/Garbage-Collection/page

This guide shows how to label and prune unused resources to keep your namespace clean.

When you use Kustomize’s `configMapGenerator` or `secretGenerator`, each modification produces a brand-new ConfigMap or Secret. Over time, this leads to multiple stale objects cluttering your cluster. This guide shows how to label and prune unused resources to keep your namespace clean.

## The Problem: Stale ConfigMaps & Secrets

Run the following command to list all ConfigMaps:

```bash theme={null}
kubectl get configmap
```

You might see output like this:

```bash theme={null}
NAME                       DATA   AGE
db-cred-b6fhfd8c67         1      38h
db-cred-bf778fgm5h         1      2m13s
db-cred-mh7c9fbtfc         1      2m5s
kube-root-ca.crt           1      9d
redis-cred-229bkfk6cd      1      82s
redis-cred-b6fhfd8c67      1      38h
redis-cred-kh464kfbf2      1      118s
```

Here, you can spot three versions each of `db-cred` and `redis-cred`, but only the most recent ones are actually in use. The rest are stale leftovers.

## Solution Overview: `kubectl apply --prune`

By adding a shared label to all generated ConfigMaps/Secrets and running `kubectl apply --prune`, Kubernetes will automatically delete any resource with that label that is no longer part of your current build.

### Step 1: Add a Common Label

In your `kustomization.yaml`, include identical labels under `options` for each generator:

```yaml theme={null}
