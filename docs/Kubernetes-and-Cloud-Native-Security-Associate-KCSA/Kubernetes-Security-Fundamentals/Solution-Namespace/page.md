# app_secret.properties
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=paswrd

kubectl create secret generic app-secret --from-env-file=app_secret.properties
```

### 1.2 Declarative Creation

Define a `Secret` manifest in `secret-data.yaml`:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DB_HOST: bXlzcWw=      # echo -n 'mysql' | base64
  DB_USER: cm9vdA==      # echo -n 'root'  | base64
  DB_PASSWORD: cGFzd3Jk  # echo -n 'paswrd'| base64
```

Apply the manifest:

```bash theme={null}
kubectl apply -f secret-data.yaml
```

Generate base64-encoded values:

```bash theme={null}
echo -n 'mysql'  | base64  # bXlzcWw=
echo -n 'root'   | base64  # cm9vdA==
echo -n 'paswrd' | base64  # cGFzd3Jk
```

<Callout icon="lightbulb">
  You can decode any value with `echo '<base64>' | base64 --decode`. Keep your raw files out of version control.
</Callout>

***

## 2. Viewing Secrets

List all existing secrets:

```bash theme={null}
kubectl get secrets
```

Inspect a specific secret:

```bash theme={null}
kubectl describe secret app-secret
```

Output the raw YAML (with encoded data):

```bash theme={null}
kubectl get secret app-secret -o yaml
```

Decode an encoded secret value:

```bash theme={null}
echo 'cGFzd3Jk' | base64 --decode  # outputs: paswrd
```

***

## 3. Injecting Secrets into Pods

You can consume Secrets as environment variables or as mounted volumes.

### 3.1 All Keys as Environment Variables

Add an `envFrom` directive to your Pod spec:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
spec:
  containers:
    - name: simple-webapp
      image: simple-webapp:latest
      ports:
        - containerPort: 8080
      envFrom:
        - secretRef:
            name: app-secret
```

Apply the Pod definition:

```bash theme={null}
kubectl apply -f pod-definition.yaml
```

### 3.2 Single Key as an Environment Variable

Use `valueFrom.secretKeyRef` for a specific key:

```yaml theme={null}
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: app-secret
        key: DB_PASSWORD
```

### 3.3 Mounting Secrets as Files

Mount the secret into a volume:

```yaml theme={null}
volumes:
  - name: app-secret-volume
    secret:
      secretName: app-secret

containers:
  - name: simple-webapp
    image: simple-webapp:latest
    volumeMounts:
      - name: app-secret-volume
        mountPath: /opt/secrets
```

Inside the running Pod:

```bash theme={null}
ls /opt/secrets
cat /opt/secrets/DB_PASSWORD
# paswrd
```

***

Try the exercises to practice creating, viewing, and injecting Secrets in your Kubernetes clusters!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/4dca62df-d690-4360-99f0-10f24974f41f" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/0f29d43a-a993-41fb-b58d-5c99f56c356a" />
</CardGroup>


# Solution Namespace

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Solution-Namespace/page

This article explains how to manage Kubernetes namespaces, including listing, counting, and deploying resources, as well as using DNS-based service discovery.

In this solution walkthrough, we’ll explore how to list and count namespaces, inspect pods within them, deploy resources, and leverage DNS-based service discovery both within the same namespace and across namespaces.

## 1. List and Count Namespaces

You can view all namespaces in your cluster using:

```bash theme={null}
kubectl get namespaces
