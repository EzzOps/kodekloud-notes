# Local shell
whoami
# Confirm pod is running
kubectl get pod
# NAME             READY   STATUS    RESTARTS   AGE
# Inside the container
kubectl exec ubuntu-sleeper -- whoami
# → root
```

**Answer:** The `sleep` process runs as **root** by default.

***

## 2. Edit the Ubuntu Sleeper pod to run the process as UID 1010

1. Export the existing Pod manifest:
   ```bash theme={null}
   kubectl get pod ubuntu-sleeper -o yaml > ubuntu-sleeper.yaml
   ```
2. In `ubuntu-sleeper.yaml`, add a container-level `securityContext`:
   ```yaml theme={null}
   spec:
     containers:
       - name: ubuntu
         image: ubuntu
         command: ["sleep", "4800"]
         securityContext:
           runAsUser: 1010
         # ...other fields...
   ```
3. Delete and recreate the Pod:
   ```bash theme={null}
   kubectl delete pod ubuntu-sleeper --force
   kubectl apply -f ubuntu-sleeper.yaml
   ```
4. Verify inside the container:
   ```bash theme={null}
   kubectl exec ubuntu-sleeper -- whoami
   # → 1010
   ```

> **lightbulb** Using `--force` deletes the Pod immediately. In production clusters, prefer a graceful rollout (e.g., updating a Deployment).

**Result:** The `sleep` process now runs as UID **1010**.

***

## 3. Which user starts processes in the `web` container of `multi-pod.yaml`?

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  securityContext:
    runAsUser: 1001      # pod-level default
  containers:
    - name: web
      image: ubuntu
      command: ["sleep", "5000"]
      securityContext:
        runAsUser: 1002  # container override
    - name: sidecar
      image: ubuntu
      command: ["sleep", "5000"]
      # no override → inherits pod-level
```

Container-level settings override pod-level defaults.

**Answer:** The `web` container runs as **1002**.

***

## 4. Which user starts processes in the `sidecar` container?

Since the `sidecar` container has no `runAsUser` block, it inherits from the Pod:

| Container | runAsUser |
| --------- | --------- |
| web       | 1002      |
| sidecar   | 1001      |

**Answer:** The `sidecar` container runs as **1001**.

***

## 5. Update Ubuntu Sleeper to run as root and add the `SYS_TIME` capability

1. Remove any `runAsUser` lines in `ubuntu-sleeper.yaml`.
2. Under the container’s `securityContext`, add the `SYS_TIME` capability:
   ```yaml theme={null}
   spec:
     containers:
       - name: ubuntu
         image: ubuntu
         command: ["sleep", "4800"]
         securityContext:
           capabilities:
             add:
               - SYS_TIME
   ```
3. Apply the changes:
   ```bash theme={null}
   kubectl delete pod ubuntu-sleeper --force
   kubectl apply -f ubuntu-sleeper.yaml
   ```

> **triangle-alert** Granting `SYS_TIME` allows processes to modify the system clock. Only use this capability if absolutely necessary.

**Result:** The pod runs as **root** with the **SYS\_TIME** capability.

***

## 6. Add the `NET_ADMIN` capability to the Ubuntu Sleeper pod

Extend the same `securityContext` to include both capabilities:

```yaml theme={null}
spec:
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "4800"]
      securityContext:
        capabilities:
          add:
            - SYS_TIME
            - NET_ADMIN
```

Reapply the manifest:

```bash theme={null}
kubectl delete pod ubuntu-sleeper --force
kubectl apply -f ubuntu-sleeper.yaml
```

**Result:** The pod now has both **SYS\_TIME** and **NET\_ADMIN** capabilities.

***

## References

* [Pod Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
* [Container Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#set-the-security-context-of-a-container)
* [Capability Lists](https://man7.org/linux/man-pages/man7/capabilities.7.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/f35655a9-b8e7-4bac-b6a1-85c2ca4900be)


# Access to Sensitive Data

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Threat-Model/Access-to-Sensitive-Data/page

This article discusses unauthorized access to sensitive data in Kubernetes and offers best practices for mitigation.

In this lesson, we explore how attackers might gain unauthorized access to sensitive information in a Kubernetes cluster and provide best practices to mitigate these risks. By following the principles of least privilege, secure logging, and network encryption, you can significantly reduce the attack surface.

## Common Attack Vectors

| Attack Vector           | Description                                                                               | Mitigation                                                                 |
| ----------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| etcd Access             | Direct reads or writes to etcd can expose Secrets, ConfigMaps, and cluster state.         | Enable TLS for etcd, use RBAC for etcd API, rotate encryption keys.        |
| Kubelet API             | Exposed kubelet endpoints may reveal logs, exec shells, and pod details.                  | Restrict kubelet API with TLS client certs and network policies.           |
| Application Logs        | Logs containing passwords, tokens, or PII become high-value targets if compromised.       | Redact sensitive fields and centralize logs in an access-controlled store. |
| Persistent Volumes      | Mounting volumes in another pod or network-exposed volumes can leak data.                 | Use volume accessModes, encryption at rest, and Pod Security Policies.     |
| Network Shares (NFS)    | Unprotected NFS/SMB shares may be read by unauthorized clients.                           | Enforce mount restrictions, network segmentation, and authentication.      |
| Cluster Encryption Keys | If master encryption keys are compromised, all encrypted data at rest becomes accessible. | Rotate keys regularly and store them in Hardware Security Modules.         |

## Example: Over-Permissive RBAC in a Node.js Backend

Imagine a Node.js service running in the `backend` namespace. Its ServiceAccount (`backend-sa`) has read access to Secrets and ConfigMaps. An attacker who compromises the pod could enumerate sensitive data.

### Secret Definition

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials
  namespace: backend
type: Opaque
data:
  DB_USERNAME: dXNlcm5hbWU=      # base64 "username"
  DB_PASSWORD: cGFzc3dvcmQ=      # base64 "password"
  DB_HOST: ZGItc2VydmVyLmV4YW1wbGUuY29tOjU0MzI=  # base64 "db-server.example.com:5432"
  DB_PORT: NTQzMg==              # base64 "5432"
```

### Misconfigured RBAC

This Role grants broad read access to Secrets and pods:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: backend-read-only
  namespace: backend
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: backend-rolebinding
  namespace: backend
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: backend-read-only
subjects:
- kind: ServiceAccount
  name: backend-sa
  namespace: backend
```

> **triangle-alert** Granting `get`/`list` on Secrets lets any pod with that ServiceAccount access database credentials, API keys, or other secrets.

### Hardened RBAC

Limit the ServiceAccount to only the resources it truly needs:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: backend-limited
  namespace: backend
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: backend-limited-binding
  namespace: backend
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: backend-limited
subjects:
- kind: ServiceAccount
  name: backend-sa
  namespace: backend
```

> **lightbulb** Always follow the [principle of least privilege](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#principle-of-least-privilege) when defining RBAC rules.

## Securing Application Logs

Logging sensitive data can expose credentials, tokens, and PII if logs are compromised.

### Risky Logging Example

```text theme={null}
[INFO] Connected to database at db-server.example.com:5432
[INFO] Executing query: SELECT * FROM users WHERE email='user@example.com' AND password='superSecretPassword123'
[ERROR] Connection timed out with username db_user and password dbPass123!
[DEBUG] Payload: {"creditCardNumber":"4111111111111111","expiration":"12/25","cvv":"123"}
```

### Redacted Logging Example

```text theme={null}
[INFO] Connected to database at db-server.example.com:5432
[INFO] Executing query: SELECT * FROM users WHERE email='**********' AND password='**********'
[ERROR] Connection timed out with username db_user and password='**********'
[DEBUG] Payload: {"creditCardNumber":"************","expiration":"**/**","cvv":"***"}
```

Best practices for log security:

* Avoid logging credentials, tokens, or other secrets.
* Mask or redact sensitive fields before writing logs.
* Centralize logs in a secure, access-controlled system (e.g., Elasticsearch with RBAC).
* Continuously monitor log access and anomalies.

## Encrypting Network Traffic

All inter-service communication should use TLS to prevent packet sniffing and man-in-the-middle attacks.

### Unencrypted HTTP Example

```http theme={null}
GET /api/user/login HTTP/1.1
Host: backend.example.com
Content-Type: application/json

{
  "username": "john_doe",
  "password": "superSecret123"
}
```

### Encrypted HTTPS Example

```http theme={null}
GET /api/user/login HTTP/1.1
Host: backend.example.com
Authorization: Bearer <token>
Content-Type: application/json
TLS: true

{
  "username": "john_doe",
  "password": "superSecret123"
}
```

Enable mTLS between pods and enforce HTTPS for all east-west and north-south traffic.

## Summary & Best Practices

* Apply **least-privilege RBAC** so pods only have the permissions they require.
* **Never log sensitive information**; mask or omit secrets in application logs.
* **Enforce TLS/mTLS** for all inter-service and external communications.
* Rotate encryption keys and Secrets regularly.

Implementing these controls will help safeguard your Kubernetes cluster against unauthorized data access.

## Links and References

* [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* [etcd Security](https://etcd.io/docs/v3.5/op-guide/security/)
* [Logging Best Practices](https://12factor.net/logs)
* [mTLS in Kubernetes](https://istio.io/latest/docs/concepts/security/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/6da25ade-b162-485c-b9b9-f351990e99c2/lesson/30d5aa37-14c8-43db-9832-3f0b55ca52b8)
