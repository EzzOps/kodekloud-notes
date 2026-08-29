# Create a new secret named "my-secret" from files in folder "bar"
kubectl create secret generic my-secret --from-file=path/to/bar

# Create a secret with specified keys from files rather than using disk filenames as keys
kubectl create secret generic my-secret --from-file=ssh-privatekey=path/to/id_rsa --from-file=ssh-publickey=path/to/id_rsa.pub

# Create a secret with literal key-value pairs
kubectl create secret generic my-secret --from-literal=key1=supersecret --from-literal=key2=topsecret

# Create a secret using a combination of a file and a literal value
kubectl create secret generic my-secret --from-file=ssh-privatekey=path/to/id_rsa --from-literal=passphrase=topsecret

# Create a secret from environment variable files
kubectl create secret generic my-secret --from-env-file=path/to/foo.env --from-env-file=path/to/bar.env
```

Additional options include:

* **--allow-missing-template-keys=true:** Ignores errors in templates if fields or keys are missing.
* **--append-hash=false:** Appends a hash of the secret to its name.
* **--dry-run:** Specify "none", "server", or "client" to perform a dry run or see what object would be sent.

For this demonstration, a secret is created with a literal value:

```bash theme={null}
kubectl create secret generic my-secret --from-literal=key1=supersecret
```

The output confirms the creation:

```bash theme={null}
secret/my-secret created

# Listing the secret
kubectl get secret
NAME        TYPE      DATA   AGE
my-secret   Opaque    1      5s
```

You can inspect the secret details with:

```bash theme={null}
kubectl describe secret my-secret
```

To view the secret in YAML format, use:

```bash theme={null}
kubectl get secret my-secret -o yaml
```

Example YAML output:

```yaml theme={null}
apiVersion: v1
data:
  key1: c3VwZXJzZWNyZXQ=
kind: Secret
metadata:
  creationTimestamp: "2022-10-24T05:34:13Z"
  name: my-secret
  namespace: default
  resourceVersion: "2111"
  uid: dfe97c62-5aa1-46a8-b71c-ffa0cd4c08ec
type: Opaque
```

If you decode the base64-encoded value, you will obtain the cleartext secret:

```bash theme={null}
echo "c3VwZXJzZWNyZXQ=" | base64 --decode
```

Output:

```text theme={null}
supersecret
```

<Callout icon="triangle-alert">
  Because secrets are stored as base64 encoded plaintext, anyone with access to etcd can decode and view them. Avoid storing secret definition files in public repositories without further protection.
</Callout>

***

## Inspecting Secret Data in etcd

Next, examine how Kubernetes stores secrets in etcd, where the data is kept unencrypted by default. To inspect the stored secrets, use the etcdctl utility with API version 3.

1. Start by verifying that etcd is running on your cluster:

   ```bash theme={null}
   kubectl get pods -n kube-system
   ```

   You should see an etcd pod (for example, "etcd-controlplane").

2. Confirm the existence of the certificate file:

   ```bash theme={null}
   ls /etc/kubernetes/pki/etcd/ca.crt
   ```

3. If etcdctl is not installed, install it using:

   ```bash theme={null}
   apt-get install etcd-client
   ```

4. Set the ETCDCTL\_API to version 3 and check the etcdctl version:

   ```bash theme={null}
   etcdctl
   ```

5. Retrieve and inspect your secret stored in etcd. Adjust the key path to match your secret (e.g., "my-secret"):

   ```bash theme={null}
   ETCDCTL_API=3 etcdctl \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \
     --key=/etc/kubernetes/pki/etcd/server.key \
     get /registry/secrets/default/my-secret | hexdump -C
   ```

The output will display a hex dump showing the secret fields, including the cleartext value ("supersecret"), confirming that etcd stores the data unencrypted.

***

## Configuring Encryption at Rest

To secure secret data, enable encryption at rest in etcd. Begin by verifying whether encryption is already configured in your cluster. Check the Kube API server for the "encryption-provider-config" flag:

```bash theme={null}
ps -aux | grep kube-api | grep "encryption-provider-config"
```

If no output is returned, encryption is not yet enabled.

1. Inspect the API server manifest, typically located in:

   ```bash theme={null}
   ls /etc/kubernetes/manifests/
   ```

2. Open the kube-apiserver manifest:

   ```bash theme={null}
   vi /etc/kubernetes/manifests/kube-apiserver.yaml
   ```

Since encryption is missing from the configuration, create an encryption configuration file and update the kube-apiserver manifest accordingly.

### Encryption Configuration File

Create a YAML file (for example, `enc.yaml`) with the following content. This configuration specifies that secret objects will be encrypted using the AESCBC provider:

```yaml theme={null}
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: INSERT_BASE64_ENCODED_32_BYTE_KEY_HERE
      - identity: {}
```

Generate a 32-byte random key and encode it in base64 using:

```bash theme={null}
head -c 32 /dev/urandom | base64
```

Replace `INSERT_BASE64_ENCODED_32_BYTE_KEY_HERE` with the generated key. Move the `enc.yaml` file to your control plane node:

```bash theme={null}
mkdir -p /etc/kubernetes/enc
mv enc.yaml /etc/kubernetes/enc/
```

### Updating the Kube API Server Manifest

Edit the kube-apiserver manifest (`/etc/kubernetes/manifests/kube-apiserver.yaml`) to apply the encryption configuration:

1. Append the following flag to reference the encryption configuration file:

   ```yaml theme={null}
   - --encryption-provider-config=/etc/kubernetes/enc/enc.yaml
   ```

2. Under the `volumeMounts` section of the kube-apiserver container, add:

   ```yaml theme={null}
   - name: enc
     mountPath: /etc/kubernetes/enc
     readOnly: true
   ```

3. Under the `volumes` section, add a hostPath volume:

   ```yaml theme={null}
   - name: enc
     hostPath:
       path: /etc/kubernetes/enc
       type: DirectoryOrCreate
   ```

A simplified excerpt of the manifest changes:

```yaml theme={null}
spec:
  containers:
    - name: kube-apiserver
      command:
        - kube-apiserver
        - --advertise-address=10.6.118.3
        # ... other flags ...
        - --encryption-provider-config=/etc/kubernetes/enc/enc.yaml
      volumeMounts:
        # ... existing volume mounts ...
        - name: enc
          mountPath: /etc/kubernetes/enc
          readOnly: true
  volumes:
    # ... existing volumes ...
    - name: enc
      hostPath:
        path: /etc/kubernetes/enc
        type: DirectoryOrCreate
```

After saving your changes, the kube-apiserver will automatically restart and apply the new encryption settings.

***

## Verifying Encryption

Once the API server has restarted with the new encryption configuration, create a new secret so it will be encrypted on write:

```bash theme={null}
kubectl create secret generic my-secret-2 --from-literal=key2=topsecret
```

Verify that the secret is created:

```bash theme={null}
kubectl get secret
NAME          TYPE    DATA   AGE
my-secret     Opaque  1      16m
my-secret-2   Opaque  1      3s
```

Now, inspect the new secret in etcd:

```bash theme={null}
ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret-2 | hexdump -C
```

The output will confirm that the secret value ("topsecret") is no longer plainly visible because it is now encrypted.

<Callout icon="lightbulb">
  Note that secrets created before enabling encryption remain unencrypted until updated. To re-encrypt these, fetch and replace them without modifying the data:

  ```bash theme={null}
  kubectl get secrets --all-namespaces -o json | kubectl replace -f -
  ```
</Callout>

***

## Summary

This article demonstrated how to:

1. Create and inspect Kubernetes secrets.
2. Verify that secrets are stored in etcd as base64-encoded plaintext.
3. Enable encryption at rest by creating an encryption configuration file.
4. Update the kube-apiserver manifest to integrate the encryption config.
5. Confirm that new secrets are encrypted and secure in etcd.

Encrypting secret data at rest is essential for protecting sensitive information from unauthorized access. Remember that encryption applies only to future changes unless existing secrets are updated.

Thank you for following this guide on encrypting Kubernetes secrets at rest!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/1d117b1c-8f6d-4aa2-a012-db396e38ce09" />
</CardGroup>


# Environment Variables

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Configuration/Environment-Variables/page

This article explains how to set environment variables in Kubernetes Pods using direct definitions, ConfigMaps, and Secrets for flexible deployment scenarios.

In this article, we explain how to set environment variables in a Kubernetes Pod. Environment variables can be defined directly in your Pod specification or managed externally using ConfigMaps and Secrets, offering flexibility for different deployment scenarios.

## Directly Defining Environment Variables

When creating a Pod, you can directly assign environment variables using the `env` property in the container specification. The `env` property is an array where each variable is defined with a `name` and `value`. For example, if you would run a Docker container with an environment variable like this:

```bash theme={null}
docker run -e APP_COLOR=pink simple-webapp-color
```

you can define the same variable in your Kubernetes Pod manifest as follows:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  containers:
  - name: simple-webapp-color
    image: simple-webapp-color
    ports:
    - containerPort: 8080
    env:
    - name: APP_COLOR
      value: pink
```

In this YAML configuration, the environment variable `APP_COLOR` is directly set to `pink`.

<Callout icon="lightbulb">
  Direct assignment is a straightforward approach, ideal for simple scenarios or development environments.
</Callout>

## Managing Environment Variables with ConfigMaps and Secrets

For more dynamic configuration management, you can externalize environment variable data using ConfigMaps or Secrets. Instead of hardcoding a value, you reference the value using the `valueFrom` field. This helps decouple configuration from application code and allows a more secure and manageable configuration.

Consider the previous direct definition:

```yaml theme={null}
env:
- name: APP_COLOR
  value: pink
```

You can modify it to use a ConfigMap like this:

```yaml theme={null}
env:
- name: APP_COLOR
  valueFrom:
    configMapKeyRef:
      name: my-config
      key: app_color
```

In this configuration, Kubernetes retrieves the value for `APP_COLOR` from a ConfigMap named `my-config` instead of hardcoding it in the manifest.

<Callout icon="lightbulb">
  Using ConfigMaps or Secrets is recommended in production environments to manage sensitive data and configuration changes without modifying the application code.
</Callout>

## Comparison of Environment Variable Methods

| Method              | Description                                             | Use Case                          |
| ------------------- | ------------------------------------------------------- | --------------------------------- |
| Direct Assignment   | Environment variable is hardcoded in the Pod manifest.  | Simple setups or development.     |
| ConfigMap Reference | Environment variable value is sourced from a ConfigMap. | Dynamic configuration management. |
| Secret Reference    | Environment variable value is sourced from a Secret.    | Managing sensitive data securely. |

## Conclusion

Managing environment variables effectively is essential for successful Kubernetes deployments. Whether you use direct assignments or manage them via ConfigMaps and Secrets, Kubernetes provides the flexibility to suit your application's needs.

That's it for this article. For more information on managing configurations in Kubernetes, visit [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/2335417e-c12b-45e5-9fa9-0fb919d588e8" />
</CardGroup>
