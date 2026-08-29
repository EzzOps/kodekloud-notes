# As the current user
kubectl auth can-i create deployments
kubectl auth can-i delete nodes
# Impersonate dev-user
kubectl auth can-i create deployments --as dev-user
kubectl auth can-i create pods --as dev-user
# → yes
```

To test in a different namespace:

```bash theme={null}
kubectl auth can-i create pods --as dev-user --namespace test
# → no  # dev-user has no access in 'test'
```

***

## 5. Restricting Access to Specific Resource Names

Limit Role permissions to named resources using `resourceNames`:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-limited
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "create", "update"]
    resourceNames: ["blue", "orange"]
```

Apply:

```bash theme={null}
kubectl apply -f role-pod-limited.yaml
```

***

## Links and References

* [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* [kubectl auth can-i](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#auth)
* [Kubernetes Concepts: RBAC](https://kubernetes.io/docs/concepts/security/rbac/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/93558bc7-a21e-46e1-8ea6-2da5d8389c99)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/0148994b-9ccc-4725-a77b-a4a63592152f/lesson/ba48419f-271a-47b1-b21f-8057b0790046)


# Secrets

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Kubernetes-Security-Fundamentals/Secrets/page

This article explains how to use Kubernetes Secrets to securely manage sensitive data in a Python web application.

In this lesson, we’ll refactor a simple Python web application that connects to a MySQL database. Currently, the database hostname, username, and password are hardcoded in the source—an insecure practice. We'll move sensitive values into Kubernetes **Secrets** to keep credentials safe.

```python theme={null}
import os
from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def main():
    conn = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        database="mysql",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
    return render_template("hello.html", color=fetchcolor())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

> **triangle-alert** Never store plaintext passwords in your code or in a `ConfigMap`. Use [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) for all sensitive data.

| Resource  | Purpose                          | Example                                     |
| --------- | -------------------------------- | ------------------------------------------- |
| ConfigMap | Non-sensitive configuration data | `DB_HOST`, `DB_USER`                        |
| Secret    | Sensitive data (passwords, keys) | `DB_PASSWORD`, API tokens, TLS certificates |

***

## 1. Creating Secrets

Secrets can be created imperatively with `kubectl` or declaratively with a YAML manifest.

### 1.1 Imperative Creation

Specify key-value pairs on the command line:

```bash theme={null}
kubectl create secret generic app-secret \
  --from-literal=DB_HOST=mysql \
  --from-literal=DB_USER=root \
  --from-literal=DB_PASSWORD=paswrd
```

Or load from a file (`key=value` per line):

```bash theme={null}
