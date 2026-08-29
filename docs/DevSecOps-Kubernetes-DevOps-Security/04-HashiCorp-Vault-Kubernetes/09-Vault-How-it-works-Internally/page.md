# s3cR3t!
```

## Viewing Secrets Directly in etcd

With etcd client certificates, stored Secrets appear in plain text:

```bash theme={null}
ETCDCTL_API=3 etcdctl get /registry/secrets/default/mysql-crds \
  --cacert /etc/kubernetes/pki/etcd/ca.crt \
  --cert    /etc/kubernetes/pki/etcd/server.crt \
  --key     /etc/kubernetes/pki/etcd/server.key
```

```text theme={null}
/registry/secrets/default/mysql-crds
k8s.io/v1Secret: |
  {"password":"s3cR3t!"}
```

## Mitigation: Encryption at Rest

Kubernetes supports encrypting Secrets in etcd with an `EncryptionConfiguration`.

1. Create `/etc/kubernetes/pki/encryption-config.yaml`:

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
                 secret: RSYzZbCmZbshlScWcjm+zAbB83coDIJ47HTRLOOW4=
         - identity: {}
   ```

2. Update the API server flags:

   ```text theme={null}
   --encryption-provider-config=/etc/kubernetes/pki/encryption-config.yaml
   ```

3. Restart the kube-apiserver. All new Secrets will be encrypted in etcd.

> **lightbulb** To encrypt existing Secrets, run:

  ```bash theme={null}
  kubectl get secrets --all-namespaces -o json \
    | kubectl replace -f -
  ```

After re-encryption, etcd shows only metadata:

```bash theme={null}
ETCDCTL_API=3 etcdctl get /registry/secrets/default/mysql-crds \
  --cacert /etc/kubernetes/pki/etcd/ca.crt \
  --cert    /etc/kubernetes/pki/etcd/server.crt \
  --key     /etc/kubernetes/pki/etcd/server.key
```

```text theme={null}
/registry/secrets/default/mysql-crds
k8s:enc:aescbc:v1:key1
```

## Best Practices for Kubernetes Secrets

| Best Practice                | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| Restrict etcd access         | Limit etcdctl and API access to cluster administrators only. |
| Enforce TLS                  | Enable TLS for all component communications.                 |
| Audit logging                | Turn on audit logs for `kubectl` and API server operations.  |
| Use an external secret store | Integrate HashiCorp Vault for dynamic, auditable secrets.    |

## Next Steps

In the next lesson, we’ll dive into the Vault Kubernetes Agent Injector—a mutating admission webhook that injects secrets via init and sidecar containers, removing static Kubernetes Secrets altogether.

***

## Links and References

* [Kubernetes Secrets][k8s-secrets]
* [Encrypting Data at Rest][etcd-encryption]
* [HashiCorp Vault][vault-docs]

[k8s-secrets]: https://kubernetes.io/docs/concepts/configuration/secret/

[etcd-encryption]: https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/

[vault-docs]: https://www.vaultproject.io/docs/

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/baf5859d-32c2-4e7c-9808-f3486d6b9827/lesson/56de0285-8e7e-48b7-9429-58c23fa7bd5a)


# Vault How it works Internally

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/HashiCorp-Vault-Kubernetes/Vault-How-it-works-Internally/page

This guide explores HashiCorp Vault's internal workflow, including pod injection, Kubernetes authentication, and secret rendering for applications.

In this guide, we’ll dive into HashiCorp Vault’s internal workflow—covering pod injection, Kubernetes authentication, and secret rendering for applications.

## Architecture Overview

When you install Vault with the official Helm chart, two key pods are deployed:

| Pod Name             | Role                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------- |
| vault-0              | Primary Vault server. Initialize Vault, add secrets, configure policies and auth.     |
| vault-agent-injector | Mutating webhook controller that injects Vault Agent containers into application Pods |

Kubernetes processes Pod creation in four main phases:

1. Authentication & Authorization
2. Mutating Admission Controllers (includes Vault injector)
3. Schema & Validation Admission Controllers
4. Persistence to etcd

After these steps, the scheduler assigns the Pod to a node and mounts its service account—at this point, secrets are not yet available inside the container.

## Injecting the Vault Agent into a Pod

To enable automatic injection, annotate your Pod manifest:

```bash theme={null}
kubectl patch pod my-app \
  --type='json' \
  -p='[{"op":"add","path":"/metadata/annotations/vault.hashicorp.com~1agent-inject","value":"true"}]'
```

When the `vault-agent-injector` webhook intercepts Pod creation, it adds:

* **Init Container**\
  Fetches secrets from Vault and writes them to a shared volume.
* **Sidecar Container (Vault Agent)**\
  Continuously renews the Vault token and re-renders secrets into the same volume.

> **lightbulb** Make sure your Kubernetes service account has the proper `system:auth-delegator` role binding so Vault can perform TokenReview requests.

## Authentication Flow

Injected containers authenticate to Vault using the Pod’s service account JWT:

1. Vault Agent sends a POST to Vault’s Kubernetes auth endpoint with the JWT.
2. Vault calls the Kubernetes TokenReview API to validate the token.
3. If the response is authenticated and matches a bound role, Vault issues a client token.
4. The token is stored at `/home/vault/.vault-token` inside the agent container.

### Sample TokenReview Request

```bash theme={null}
curl --location --request POST "https://$KUBE_API_SERVER/apis/authentication.k8s.io/v1/tokenreviews" \
  --header "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  --header "Content-Type: application/json" \
  --data '{
    "apiVersion": "authentication.k8s.io/v1",
    "kind": "TokenReview",
    "spec": {
      "token": "<POD_SERVICE_ACCOUNT_TOKEN>"
    }
  }'
```

## Configuring Vault Roles and Policies

On your Vault server (`vault-0`), enable Kubernetes auth and bind service accounts to policies:

```bash theme={null}
