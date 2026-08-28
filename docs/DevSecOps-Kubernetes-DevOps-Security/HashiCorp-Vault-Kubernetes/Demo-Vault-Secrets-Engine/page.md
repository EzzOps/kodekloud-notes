# Example output:
# NAME                                 READY   STATUS    RESTARTS   AGE
# php-5bc8df55fb-c7tj6                 1/1     Running   0          10s
# vault-0                              1/1     Running   0          55m
kubectl get svc
# Example output:
# NAME                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
# php                          NodePort    10.96.105.209    <none>        80:30835/TCP                 20s
# vault                        ClusterIP   10.109.140.61    <none>        8200/TCP,8201/TCP           56m
kubectl get sa
# Example output:
# NAME                     SECRETS   AGE
# app                      1         32s
# default                  1         57m
# vault                    1         56m
```

Accessing the UI

* The php Service is exposed as a NodePort. Use the node (VM) public IP and NodePort to open the app in your browser:

```text theme={null}
http://<NODE_PUBLIC_IP>:<NODE_PORT>
# e.g. http://40.76.109.0:30835
```

* Behavior:
  * If Vault has not injected the three files at `/vault/secrets/`, the UI shows a red background with "File(s) Not Found".
  * Once Vault Agent Injector mounts/writes the secrets into `/vault/secrets/` inside the pod, the UI will switch to green and display the username, password, and API key.

Pod-level verification

* Inspect the pod filesystem to validate whether the secret files exist:

```bash theme={null}
kubectl get pods
kubectl exec -it <php-pod-name> -- ls /vault/secrets
# If files are missing you'll see: ls: cannot access '/vault/secrets': No such file or directory
# If files exist you will see: username  password  apikey
```

* If files are missing, the UI remains in the red "File(s) Not Found" state. After successful injection, the UI displays secrets (as shown in index.php).

Security notes

* The demo uses the PHP `@` operator to suppress file warnings; prefer explicit error handling in production.
* Use `htmlspecialchars()` (as done here) or other sanitization to avoid HTML injection when rendering secrets in a browser. For production, avoid rendering raw secrets in UI and use secure secrets handling patterns.

<Callout icon="lightbulb">
  Make sure the mount path used by your Vault injection configuration matches the file paths the application expects (here: /vault/secrets/username, /vault/secrets/password, /vault/secrets/apikey). Also confirm the ServiceAccount used by the Deployment has the necessary annotations and role bindings for Vault Agent Injector to work.
</Callout>

Next steps and references

* Configure and review the Vault Agent Injector annotations in the patch file to write secrets into the pod filesystem.
* Consider using environment variables or in-memory secret stores instead of writing secrets to disk for stronger security.
* Useful links:
  * HashiCorp Vault: [https://www.vaultproject.io/](https://www.vaultproject.io/)
  * Vault Kubernetes integration: [https://www.vaultproject.io/docs/platform/k8s](https://www.vaultproject.io/docs/platform/k8s)
  * Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/baf5859d-32c2-4e7c-9808-f3486d6b9827/lesson/f840eabb-c3ee-43a1-9f04-cd1b70ba3757" />
</CardGroup>


# Demo Vault Secrets Engine

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/HashiCorp-Vault-Kubernetes/Demo-Vault-Secrets-Engine/page

This guide explains how to enable and use the Key-Value version 2 secrets engine in HashiCorp Vault for securely storing and managing secrets.

In this guide, you’ll learn how to enable and use the Key-Value (KV) version 2 secrets engine in HashiCorp Vault. The KV secrets engine allows you to securely store arbitrary secrets—like database credentials, API keys, or certificates—and manage multiple versions, metadata, and lifecycle operations.

## Prerequisites

* Vault CLI installed and configured
* A running and unsealed Vault server
* [Vault Authentication](https://www.vaultproject.io/docs/auth) set up for your environment

<Callout icon="lightbulb">
  Ensure your Vault server is unsealed and your CLI is authenticated (`vault login`) before proceeding.
</Callout>

## 1. Enable the KV v2 Secrets Engine

Mount the KV v2 engine at the `crds/` path:

```bash theme={null}
vault secrets enable -path=crds kv-v2
