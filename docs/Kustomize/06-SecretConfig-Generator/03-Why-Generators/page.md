# Old ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-cred-jj26gh
data:
  password: "password1"

# New ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-cred-a477b
data:
  password: "password2"
```

```yaml theme={null}
# Before build
env:
- name: DB_PASSWORD
  valueFrom:
    configMapKeyRef:
      name: db-cred-jj26gh
      key: password

# After build
env:
- name: DB_PASSWORD
  valueFrom:
    configMapKeyRef:
      name: db-cred-a477b
      key: password
```

Since the ConfigMap name changes, Kubernetes treats the Deployment as updated and automatically initiates a rollout—no extra CLI steps required.

## Defining a ConfigMap Generator

Add a `configMapGenerator` section to your `kustomization.yaml`. Specify the generator `name` and key-value pairs under `literals`:

```yaml theme={null}
configMapGenerator:
- name: db-cred
  literals:
    - password=password1
```

Running `kustomize build` produces:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-cred-jj26gh
data:
  password: "password1"
```

### Using File Inputs for ConfigMaps

You can load entire files instead of literals. Kustomize uses the filename as the data key:

```yaml theme={null}
configMapGenerator:
- name: nginx-config
  files:
    - nginx.conf
```

Contents of `nginx.conf`:

```nginx theme={null}
server {
    listen 80;
    server_name example.com;
    location / {
    }
}
```

Generated resource:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config-jj26gh
data:
  nginx.conf: |
    server {
        listen 80;
        server_name example.com;
        location / {
        }
    }
```

> **lightbulb** Using files allows you to keep complex configurations version-controlled and modular.

## Defining a Secret Generator

Secrets follow the same pattern as ConfigMaps. Replace `configMapGenerator` with `secretGenerator`:

```yaml theme={null}
secretGenerator:
- name: db-cred
  literals:
    - password=password1
```

Generated Secret:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: db-cred-dd6525th4g
type: Opaque
data:
  password: cGFzc3dvcmlQ
```

File-based secrets are also supported:

```yaml theme={null}
secretGenerator:
- name: nginx-secret
  files:
    - nginx-conf
```

> **triangle-alert** Avoid committing sensitive information in plaintext to source control. Use sealed secrets or external secret management services for production workloads.

## Generator Types Overview

| Generator Type | Use Case                        | Kustomization Key  |
| -------------- | ------------------------------- | ------------------ |
| ConfigMap      | Non-sensitive configuration     | configMapGenerator |
| Secret         | Sensitive data (base64-encoded) | secretGenerator    |

## References

* [Kubernetes ConfigMap Documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)
* [Kubernetes Secret Documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
* [Kustomize Generators](https://kubectl.docs.kubernetes.io/references/kustomize/generators/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kustomize/module/51823d3e-7be4-4792-836a-2c4690c0c547/lesson/4d922c66-e6da-4764-ba66-f5461ef566a3)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kustomize/module/51823d3e-7be4-4792-836a-2c4690c0c547/lesson/49973abe-d000-44cc-90ad-5802d6dedf73)


# Why Generators

Source: https://notes.kodekloud.com/docs/Kustomize/SecretConfig-Generator/Why-Generators/page

This article explains how to automate pod rollouts in Kubernetes when ConfigMaps or Secrets are updated.

In Kubernetes, workloads often rely on ConfigMaps or Secrets for configuration data. However, when these resources change, pods do not automatically pick up the updates. Config generators (and secret generators) solve this by automating rollouts whenever underlying ConfigMaps or Secrets are modified. In this lesson, we’ll demonstrate this problem and prepare for the next section on generators.

## Initial Setup

### 1. Create a ConfigMap for Database Credentials

First, define a ConfigMap to hold your database password. In production, you should use a Secret, but for demonstration the behavior is identical.

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-credentials
data:
  password: "password1"
```

> **lightbulb** Use a [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) in real deployments to protect sensitive data.

Save this as `configmap.yaml` and apply:

```bash theme={null}
kubectl apply -f configmap.yaml
```

### 2. Deploy an NGINX Pod Referencing the ConfigMap

Next, deploy an NGINX container that injects the password as an environment variable:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      component: nginx
  template:
    metadata:
      labels:
        component: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          env:
            - name: DB_PASSWORD
              valueFrom:
                configMapKeyRef:
                  name: db-credentials
                  key: password
```

Save as `deployment.yaml` and apply:

```bash theme={null}
kubectl apply -f deployment.yaml
```

## Verifying the Environment Variable

1. List the running pods:

   ```bash theme={null}
   kubectl get pods
   ```

2. Exec into the NGINX pod and print the `DB_PASSWORD`:

   ```bash theme={null}
   POD=$(kubectl get pods -l component=nginx -o jsonpath="{.items[0].metadata.name}")
   kubectl exec "$POD" -- printenv | grep -i db
   ```

Expected output:

```text theme={null}
DB_PASSWORD=password1
```

## Changing the Password

After some time, update the database password in your ConfigMap:

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-credentials
data:
  password: "password2"
```

Reapply the manifest:

```bash theme={null}
kubectl apply -f configmap.yaml
```

Even though the ConfigMap reflects the new value:

```bash theme={null}
kubectl describe configmap db-credentials
```

```text theme={null}
Data
====
password:
----
password2
```

the pod still reports the old password:

```bash theme={null}
kubectl exec "$POD" -- printenv | grep -i db
