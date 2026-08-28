# Example output:
# NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
# argocd-application-controller    0/1     0            0           45m
# (after a short while)
# argocd-application-controller    1/1     1            1           46m
```

Verify the ConfigMap contains the new timeout:

```bash theme={null}
kubectl -n argocd get cm argocd-cm -o yaml | grep -i timeout
# Expected output:
# timeout.reconciliation: 10s
```

<Frame>
  <img alt="The image shows a GitHub issue page for the project &#x22;argo-cd,&#x22; where an open issue titled &#x22;Timeout.Reconciliation setting not affecting polling frequency&#x22; is being discussed. The issue, labeled as a bug, includes a checklist and a description of the problem." />
</Frame>

## 3. Verify with a deployment change (test reconciliation frequency)

Make a small change in the Git repo for an ArgoCD-managed app to confirm faster polling. In this demo we change the replica count of a Deployment. This is the manifest as stored in Git before the change:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
  namespace: highway-animation
spec:
  replicas: 10
  selector:
    matchLabels:
      app: highway-animation
  template:
    metadata:
      labels:
        app: highway-animation
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:blue
          ports:
            - containerPort: 3000
          env:
            - name: POD_COUNT
              value: "10"
```

Change `replicas` to a new value (for example `7`), commit and push. Example updated manifest:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: highway-animation
  namespace: highway-animation
spec:
  replicas: 7
  selector:
    matchLabels:
      app: highway-animation
  template:
    metadata:
      labels:
        app: highway-animation
    spec:
      containers:
        - name: highway-animation
          image: siddharth67/highway-animation:blue
          ports:
            - containerPort: 3000
          env:
            - name: POD_COUNT
              value: "7"
```

After pushing the change, ArgoCD will poll the Git repository according to the configured `timeout.reconciliation` (plus any processing time). Check the target namespace to observe pod scaling and reconciliation:

```bash theme={null}
kubectl -n highway-animation get po
# Example output shows new pods being created and old pods terminating as the Deployment scales:
# NAME                                       READY   STATUS              RESTARTS   AGE
# highway-animation-97b59688-rrnh2           1/1     Running             0          14s
# highway-animation-c88486bd5-kfkqp          0/1     Pending             0          0s
# ...
```

Timing may vary slightly due to controller scheduling and cluster load. If `timeout.reconciliation: "10s"` is set and the application controller was restarted, you should observe reconciliation occurring more frequently than the default (often within the configured interval plus controller processing time).

## Quick reference — common commands

| Task                              | Command / Notes                                                                  |                   |
| --------------------------------- | -------------------------------------------------------------------------------- | ----------------- |
| Edit ConfigMap                    | `kubectl -n argocd edit cm argocd-cm`                                            |                   |
| Set poll interval                 | Add `timeout.reconciliation: "10s"` under `data:` in the ConfigMap               |                   |
| Restart controller (Deployment)   | `kubectl -n argocd rollout restart deployment argocd-application-controller`     |                   |
| Restart controller (StatefulSet)  | `kubectl -n argocd rollout restart sts argocd-application-controller`            |                   |
| Verify ConfigMap contains timeout | \`kubectl -n argocd get cm argocd-cm -o yaml                                     | grep -i timeout\` |
| Check controller logs             | `kubectl -n argocd logs -l app.kubernetes.io/name=argocd-application-controller` |                   |
| Inspect target namespace pods     | `kubectl -n <namespace> get po`                                                  |                   |

## Troubleshooting tips

* Ensure `timeout.reconciliation` is a quoted string value (for example `"10s"`) under the ConfigMap `data:`; unquoted values may be rejected or parsed incorrectly.
* Always restart the `argocd-application-controller` after editing `argocd-cm`; the controller reads this ConfigMap at startup.
* If reconcilation is still slow:
  * Confirm the controller restart succeeded (`kubectl -n argocd get deployment argocd-application-controller`).
  * Inspect controller logs for errors or warnings:
    ```bash theme={null}
    kubectl -n argocd logs -l app.kubernetes.io/name=argocd-application-controller
    ```
  * Check for any cluster-level rate limiting or heavy controller load that could delay reconciliation.
* For ArgoCD version-specific behavior or additional tuning options, refer to the official docs: [Argo CD documentation - Configuration](https://argo-cd.readthedocs.io/) and [Argo CD troubleshooting](https://argo-cd.readthedocs.io/en/stable/troubleshooting/).

This walkthrough demonstrates how to tune ArgoCD's pull/poll frequency by updating `timeout.reconciliation` in the `argocd-cm` ConfigMap and ensuring the application controller loads the new configuration.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/5818fb58-625e-49da-96e9-ea1d5ad611ba" />
</CardGroup>


# Demo Encrypt Secrets Using Bitnami Sealed Secrets

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Patterns/Demo-Encrypt-Secrets-Using-Bitnami-Sealed-Secrets/page

Demonstrates encrypting Kubernetes Secrets with Bitnami Sealed Secrets using kubeseal and Argo CD so secrets can be safely stored in Git and decrypted only by the cluster controller

In this lesson we encrypt Kubernetes Secrets with Bitnami Sealed Secrets so they can be safely stored in Git and only be decrypted by the Sealed Secrets controller running in the target cluster.

We will work inside the `sealed-secret` directory of the `cgoa-demos` repository.

<Frame>
  <img alt="The image shows a GitHub repository interface with files and folders listed, including updates and commit details. It highlights the use of the Smarty language." />
</Frame>

In that directory you can see a Deployment, a Service, and a standard Kubernetes Secret file that was recently updated.

<Frame>
  <img alt="The image shows a file directory from a web-based code repository, featuring a folder called &#x22;sealed-secrets&#x22; with YAML files related to deployment and services. The repository interface displays recent updates, including modifications to a &#x22;secret.yml&#x22; file." />
</Frame>

Important: a Kubernetes Secret stores values Base64-encoded, not encrypted. Anyone with the file can decode the values.

Example of a plain Secret YAML (values are Base64-encoded):

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: app-crds
data:
  apikey: emFDRUxnTC0wa1l5ZmM4bVZM3dzQWF3
  username: YWRtaW4=
  password: cGFzc3dvcmQ=
```

Because GitOps workflows keep manifests in Git, never commit plain (or only Base64-encoded) Secrets. Instead, encrypt secrets for storage in Git with a tool that only the cluster controller can decrypt — for example, Bitnami Sealed Secrets.

Overview — how this works

* The Sealed Secrets controller in the cluster holds a private key.
* You fetch the controller's public certificate and use `kubeseal` to encrypt a regular Secret YAML into a SealedSecret.
* The SealedSecret is safe to commit to Git because it contains only encrypted data.
* When applied to a cluster, the controller decrypts it and creates a standard Kubernetes Secret for pods to consume.

Step 1 — get the Sealed Secrets controller public certificate
The `kubeseal` client needs the controller's public cert to encrypt secrets. Fetch it from the namespace where the controller is installed (commonly `kube-system`):

1. List secrets in the controller namespace:

```bash theme={null}
kubectl -n kube-system get secret
```

2. Extract and decode the controller certificate (replace `<SECRET_NAME>` with the secret name you found):

```bash theme={null}
kubectl -n kube-system get secret <SECRET_NAME> -o json \
  | jq -r '.data["tls.crt"]' \
  | base64 --decode > ss-public.crt
```

Notes:

* The bracket notation `["tls.crt"]` is required because the key contains a dot.
* `ss-public.crt` will contain the controller public certificate in PEM format, e.g.:

```text theme={null}
-----BEGIN CERTIFICATE-----
MIIzEDCArSgAwIBAgIQNydvhgVzGKbSCcZ...
-----END CERTIFICATE-----
```

<Frame>
  <img alt="The image shows a terminal window in a code editor displaying encoded or encrypted text." />
</Frame>

Step 2 — generate the Secret YAML locally (without applying it)
Use `kubectl create secret` with a dry-run to produce the Secret YAML file:

```bash theme={null}
kubectl create secret generic app-crds \
  --from-literal=apikey=zaCELGm8vAyarYr4Rx-Af50DDqtlx \
  --from-literal=username=admin-dev-group \
  --from-literal='password=pa$$w0rd123' \
  -o yaml --dry-run=client > mysql-password.yaml
```

Tip: quote literal values that include shell-sensitive characters (like `$`) to prevent expansion, as shown for the `password`.

Generated Secret (simplified):

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: app-crds
data:
  apikey: emFRUXnTC0wAlmbm4ZWM3dzQWF3
  username: YWRtaW4tZGV2LWxpcw==
  password: cGEtJHcwdmQxMjM=
```

Step 3 — encrypt the Secret with kubeseal
Use the public certificate and choose a scope for the resulting SealedSecret (`cluster-wide` or `namespace`):

```bash theme={null}
kubeseal --cert ss-public.crt --scope cluster-wide -o yaml \
  < mysql-password.yaml > sealed-secret.yaml
```

This reads the cleartext Secret from stdin and writes a SealedSecret resource to `sealed-secret.yaml`. A SealedSecret uses `spec.encryptedData` (not `data`) and is safe to commit.

Example (truncated):

```yaml theme={null}
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: app-crds
  annotations:
    sealedsecrets.bitnami.com/cluster-wide: "true"
spec:
  encryptedData:
    apikey: AgAWtLEpdg/433zTXjKhuIrubYubbDA1or7Mm4UmMw0m/...
    password: AgB6ZlGxWrdZYrMUrYTM...
  template:
    metadata:
      annotations:
        sealedsecrets.bitnami.com/cluster-wide: "true"
```

<Callout icon="lightbulb">
  Do not commit plain Secret YAML files to Git. Commit only the SealedSecret YAML so secrets remain encrypted in the repository.
</Callout>

Step 4 — commit the SealedSecret to Git and deploy with Argo CD

* Commit `sealed-secret.yaml` to the repository path monitored by Argo CD.
* Configure an Argo CD Application pointing at the repo/path containing the SealedSecret (you can create the application's namespace via Argo CD or beforehand).
* Sync the Argo CD Application.

When Argo CD applies the SealedSecret, the Sealed Secrets controller intercepts it, decrypts the `encryptedData` with its private key, and creates a regular Kubernetes Secret in the target namespace for your application.

Argo CD UI — application view

<Frame>
  <img alt="The image shows a user interface of Argo CD, displaying a list of applications with their synchronization and health statuses. It includes details for each application, like repository, target revision, and last sync time." />
</Frame>

You can inspect application relationships and sync/health status in Argo CD.

<Frame>
  <img alt="The image shows the interface of Argo CD, depicting the application status and a visual representation of application resources and their relationships. It indicates a &#x22;Healthy&#x22; app health and a &#x22;Synced&#x22; sync status." />
</Frame>

Step 5 — verify the Secret in the cluster

1. Verify namespaces (you should see `secret-app` if Argo CD created it):

```bash theme={null}
kubectl get ns
```

2. Check resources in the application namespace:

```bash theme={null}
kubectl -n secret-app get all
```

3. Inspect the created Secret (the Sealed Secrets controller creates a normal `Secret` resource — values are still Base64-encoded per Kubernetes format, but represent the decrypted values from the original Secret):

```bash theme={null}
kubectl get secret app-crds -n secret-app -o json
```

Example output (truncated):

```json theme={null}
{
  "apiVersion": "v1",
  "data": {
    "apikey": "emFDRUnTC0wAlmbmM4bZVM3dzQWF3",
    "password": "cGFzc3dvcmQ=",
    "username": "YWRtaW4="
  },
  "kind": "Secret",
  "metadata": {
    "name": "app-crds",
    "namespace": "secret-app",
    "annotations": {
      "sealedsecrets.bitnami.com/cluster-wide": "true"
    },
    "ownerReferences": [
      {
        "apiVersion": "bitnami.com/v1alpha1",
        "controller": true,
        "kind": "SealedSecret",
        "name": "app-crds"
      }
    ]
  },
  "type": "Opaque"
}
```

<Frame>
  <img alt="The image shows a screenshot of a Bitnami interface displaying encrypted credentials such as username, password, and API key, noting they are managed with Bitnami Sealed Secrets." />
</Frame>

Key takeaways

* SealedSecrets are safe to commit to Git because they store only encrypted data.
* The cluster's Sealed Secrets controller holds the private key and will decrypt SealedSecrets to create real Kubernetes Secrets in the target namespace.
* Applications consume the resulting Secret as usual.

Quick command reference

| Task                                 | Command                                                                                                                                                                     |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| List secrets in controller namespace | `kubectl -n kube-system get secret`                                                                                                                                         |
| Extract controller cert              | `kubectl -n kube-system get secret <SECRET_NAME> -o json \| jq -r '.data["tls.crt"]' \| base64 --decode > ss-public.crt`                                                    |
| Create a Secret YAML (dry-run)       | `kubectl create secret generic app-crds --from-literal=apikey=... --from-literal=username=... --from-literal='password=...' -o yaml --dry-run=client > mysql-password.yaml` |
| Encrypt Secret to SealedSecret       | `kubeseal --cert ss-public.crt --scope cluster-wide -o yaml < mysql-password.yaml > sealed-secret.yaml`                                                                     |
| Verify created Secret in cluster     | `kubectl get secret app-crds -n secret-app -o json`                                                                                                                         |

Alternatives and further reading

* Bitnami Sealed Secrets: [https://github.com/bitnami-labs/sealed-secrets](https://github.com/bitnami-labs/sealed-secrets)
* kubeseal (client): [https://github.com/bitnami-labs/sealed-secrets#kubeseal](https://github.com/bitnami-labs/sealed-secrets#kubeseal)
* Argo CD documentation: [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/)
* Other GitOps secret management tools: Mozilla SOPS, HashiCorp Vault

This concludes the demo.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/5ea48f92-ff16-413d-bd6c-825bd3e109b9" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/f1538ace-dc97-454d-b894-15bdd35bcb64/lesson/d2278d36-c266-43a8-9465-62f77bd3a4cb" />
</CardGroup>
