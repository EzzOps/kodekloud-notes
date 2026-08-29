# Sample Falco output:
22:57:09.163982780: Notice A shell was spawned in a container ...
23:09:03.279503809: Warning Sensitive file opened for reading ...
```

These alerts complement Kubernetes audit logs by surfacing container-level anomalies.

## Kubernetes API Server Request Stages

Every API request flows through the server in four logical stages. You can choose to log specific stages via your audit policy:

| Stage            | Description                                                                      |
| ---------------- | -------------------------------------------------------------------------------- |
| RequestReceived  | Recorded immediately upon receipt, before authn/authz.                           |
| ResponseStarted  | Emitted when the server begins processing long-running requests (e.g., `watch`). |
| ResponseComplete | Logged after the response is sent to the client.                                 |
| Panic            | Captures internal server errors or panics during request handling.               |

## Defining an Audit Policy

An audit policy is a YAML file that specifies which events to include or omit. Start with a minimal policy:

```yaml theme={null}
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - "RequestReceived"
rules:
  # Define your rules here
```

* `omitStages`: Skip logging for specified stages (optional).
* `rules`: A list of match conditions and the `level` of logging.

### Audit Levels

| Level           | Captured Data                            |
| --------------- | ---------------------------------------- |
| None            | Do not log the event.                    |
| Metadata        | Timestamps, user, verb, resource, etc.   |
| Request         | Metadata + request body.                 |
| RequestResponse | Metadata + request body + response body. |

### Example: Log Pod Deletions in Production

This policy logs only DELETE operations on the Pod `webapp-pod` in `prod-namespace` at the full request/response level:

```yaml theme={null}
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - "RequestReceived"
rules:
  - level: RequestResponse
    verbs:
      - delete
    namespaces:
      - prod-namespace
    resources:
      - groups: ""
        resources:
          - pods
        resourceNames:
          - webapp-pod
```

You can add another rule to capture all secret-related operations at the Metadata level:

```yaml theme={null}
  - level: Metadata
    resources:
      - groups: ""
        resources:
          - secrets
```

## Enabling Audit Logging

To activate auditing, point your API server to the audit policy and log file:

### kubeadm-based Clusters

Edit the static pod manifest `/etc/kubernetes/manifests/kube-apiserver.yaml`:

```yaml theme={null}
spec:
  containers:
    - name: kube-apiserver
      command:
        - kube-apiserver
        # ...
        - --audit-policy-file=/etc/kubernetes/audit-policy.yaml
        - --audit-log-path=/var/log/k8s-audit.log
        - --audit-log-maxage=10
        - --audit-log-maxbackup=5
        - --audit-log-maxsize=100
```

### systemd-based API Server

Add the same flags to the service unit file under the `ExecStart` section.

* `--audit-policy-file`: Path to your YAML policy
* `--audit-log-path`: Destination for audit logs
* `--audit-log-maxage`: Retention days for old logs
* `--audit-log-maxbackup`: Number of rotated files to keep
* `--audit-log-maxsize`: Max size (MB) before rotation

After updating, restart the API server to apply changes.

## Verifying Audit Logs

Delete the target Pod to generate an audit entry:

```bash theme={null}
kubectl delete pod webapp-pod -n prod-namespace
```

Inspect the logs:

```bash theme={null}
tail /var/log/k8s-audit.log
```

You should see a `delete` event for `webapp-pod` in `prod-namespace`.

> **lightbulb** Use `kubectl apply -f audit-policy.yaml` to update your policy dynamically and trigger events for testing.

***

## References

* [Kubernetes Audit Documentation](https://kubernetes.io/docs/tasks/debug-application-cluster/audit/)
* [Falco Security Monitoring](https://falco.org/docs/)
* [API Server Command-Line Flags](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/c3b4f553-f11b-4575-9326-5181c4ad914e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/b2419d37-95cc-40d0-9fa4-54400aacf84f)


# Authentication

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Authentication/page

This lesson covers authenticating access to a Kubernetes cluster, detailing methods and configurations for securing API server interactions.

Welcome to this lesson on authenticating access to a Kubernetes cluster. A cluster consists of multiple physical or virtual nodes and several internal components working together to run your workloads. It’s crucial to secure management access by verifying identities for anyone or anything interacting with the API server.

Actors interacting with the cluster:

| Actor           | Description                                | Examples                            |
| --------------- | ------------------------------------------ | ----------------------------------- |
| Administrators  | Manage infrastructure and policies         | Cluster operators, DevOps engineers |
| Developers      | Deploy and maintain applications           | CI/CD engineers, application owners |
| Robotic Clients | Automated systems accessing the API server | Monitoring tools, pipelines         |

Kubernetes relies on external identity sources (files, certificates, identity services like LDAP or OIDC) for human user authentication, while it internally manages *service accounts*. All requests pass through the **kube-apiserver**, which authenticates before authorizing.

Supported authentication methods:

| Method                    | Description                                                       |
| ------------------------- | ----------------------------------------------------------------- |
| Static Password File      | CSV listing `username`, `password`, `UID`, \[optional groups]     |
| Static Token File         | CSV listing bearer `token`, `username`, `UID`, \[optional groups] |
| Client Certificates       | X.509 certificates for users                                      |
| External Identity Service | LDAP, OIDC, webhook token authentication                          |

![The image illustrates authentication mechanisms for "kube-apiserver," including static password files, static token files, certificates, and identity services.](https://kodekloud.com/kk-media/image/upload/v1752880776/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Authentication/kube-apiserver-authentication-mechanisms.jpg)

***

## 1. Static Password File

The simplest approach uses a CSV file with one line per user:

```csv theme={null}
password123,user1,u0001,group1
password123,user2,u0002,group1
password123,user3,u0003,group2
password123,user4,u0004,group2
password123,user5,u0005,group2
```

### Configuring the API Server

Choose your setup:

1. **Systemd unit** (`/etc/systemd/system/kube-apiserver.service`):
   ```shell theme={null}
   ExecStart=/usr/local/bin/kube-apiserver \
     --advertise-address=${INTERNAL_IP} \
     --allow-privileged=true \
     --authorization-mode=Node,RBAC \
     --bind-address=0.0.0.0 \
     --etcd-servers=https://127.0.0.1:2379 \
     --service-cluster-ip-range=10.32.0.0/24 \
     --service-node-port-range=30000-32767 \
     --runtime-config=api/all \
     --enable-swagger-ui=true \
     --event-ttl=1h \
     --v=2 \
     --basic-auth-file=/path/to/user-details.csv
   ```

2. **kubeadm** (edit `/etc/kubernetes/manifests/kube-apiserver.yaml` under `spec.containers.command`):
   ```yaml theme={null}
   apiVersion: v1
   kind: Pod
   metadata:
     name: kube-apiserver
     namespace: kube-system
   spec:
     containers:
     - name: kube-apiserver
       image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
       command:
       - kube-apiserver
       - --authorization-mode=Node,RBAC
       - --allow-privileged=true
       - --advertise-address=172.17.0.107
       - --etcd-servers=https://127.0.0.1:2379
       - --service-cluster-ip-range=10.32.0.0/24
       - --service-node-port-range=30000-32767
       - --runtime-config=api/all
       - --enable-bootstrap-token-auth=true
       - --enable-swagger-ui=true
       - --event-ttl=1h
       - --v=2
       - --basic-auth-file=/path/to/user-details.csv
   ```

After saving changes, the API server will restart automatically (kubeadm) or after reloading your systemd unit.

### Testing Password Authentication

```bash theme={null}
curl -u user1:password123 https://<api-server-ip>:6443/api/v1/nodes
```

***

## 2. Static Token File

Bearer tokens offer another static method. Create a CSV containing tokens:

```csv theme={null}
KpjCVbI7cCEAHYPkByTizRb7gulcUc4B,user0,u0010,group1
rJjncHmvtXHc6MlWQddhtvNyyhgTdxSC,user1,u0011,group1
mjoOFTEiFOKL9toikaRNtt59ePtczZSq,user2,u0012,group2
PG41IXhs7QjqWkmBkvG9gICloYuQzI,user3,u0013,group2
```

Add to your API server flags:

```shell theme={null}
--token-auth-file=/path/to/user-token-details.csv
```

### Testing Token Authentication

```bash theme={null}
curl -H "Authorization: Bearer KpjCVbI7cCEAHYPkByTizRb7gulcUc4B" \
     https://<api-server-ip>:6443/api/v1/namespaces
```

***

> **triangle-alert** Storing usernames, passwords, or tokens in plain text is **not recommended** for production. Use secure vaults or external identity providers for sensitive environments.

![The image contains a note with three bullet points about authentication mechanisms, volume mounting in kubeadm setup, and setting up role-based authorization for new users.](https://kodekloud.com/kk-media/image/upload/v1752880777/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Authentication/authentication-volume-mounting-kubeadm.jpg)

## Security Considerations

* For **kubeadm** clusters, mount your credential files into the API server Pod via a volume.
* Protect files with restrictive filesystem permissions (`chmod 600`).
* After authenticating users, configure [Role-Based Access Control (RBAC)](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) to grant least-privilege permissions.

***

Next, we’ll explore certificate-based authentication and how Kubernetes components use TLS certificates to secure communication.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/e28adb71-1b9e-4f03-9194-898630bea28e)
