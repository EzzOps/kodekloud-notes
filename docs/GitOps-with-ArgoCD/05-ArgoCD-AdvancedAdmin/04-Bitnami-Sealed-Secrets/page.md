# Install the AVP plugin (as root so we can copy to /usr/local/bin)
ENV AVP_VERSION=0.2.2
ENV BIN=argocd-vault-plugin
RUN curl -L -o ${BIN} https://github.com/argoproj-labs/argocd-vault-plugin/releases/download/v${AVP_VERSION}/${BIN}
RUN chmod +x ${BIN}
RUN mv ${BIN} /usr/local/bin

# Switch back to non-root user
USER 999
```

> **lightbulb** Embedding the plugin in your custom image can simplify deployment in environments where using an initContainer is less desirable.

***

## 3. Configuring the Config Management Plugin

Once the Vault plugin binary is available, update the ArgoCD ConfigMap to instruct ArgoCD on how to invoke the plugin for manifest generation. Add the following configuration in your ConfigMap:

```yaml theme={null}
data:
  configManagementPlugins: |-
    - name: argocd-vault-plugin
      generate:
        command: ["argocd-vault-plugin"]
        args: ["generate", "./"]
```

This configuration directs ArgoCD to execute the command `argocd-vault-plugin generate ./` during the reconciliation process.

***

## 4. Updating the Repo Server Deployment with Vault Plugin Credentials

Below is a revised ArgoCD repo server deployment example. This configuration includes a secret reference for Vault credentials and updates the Vault plugin version to 1.7.1. Ensure that the environment variable is correctly defined as AVP\_VERSION.

```yaml theme={null}
metadata:
  name: argocd-repo-server
spec:
  template:
    spec:
      containers:
        - name: argocd-repo-server
          volumeMounts:
            - name: custom-tools
              mountPath: /usr/local/bin/argocd-vault-plugin
              subPath: argocd-vault-plugin
          envFrom:
            - secretRef:
                name: argocd-vault-plugin-credentials
      volumes:
        - name: custom-tools
          emptyDir: {}
      initContainers:
        - name: download-tools
          image: alpine:3.8
          command: [sh, -c]
          env:
            - name: AVP_VERSION
              value: "1.7.1"
          args:
            - >
              wget -O argocd-vault-plugin https://github.com/argoproj-labs/argocd-vault-plugin/releases/download/v${AVP_VERSION}/argocd-vault-plugin &&
              chmod +x argocd-vault-plugin &&
              mv argocd-vault-plugin /custom-tools/
          volumeMounts:
            - name: custom-tools
              mountPath: /custom-tools
      automountServiceAccountToken: true
```

After deploying these changes using, for example, `kubectl edit deployment argocd-repo-server -n argocd`, the repo server downloads the Vault plugin and processes manifests containing Vault annotations.

***

## 5. Creating an Application Using Vault Secrets

To use the Vault plugin, enable it within your ArgoCD application. In the ArgoCD UI, create a new application (e.g., *Vault Secret App Demo*) within the default or demo project. Configure the sync policy to manual and let the target namespace be automatically created.

![The image shows a web interface for configuring an application in Argo CD, with fields for application name, project, sync policy, and other settings. The interface includes options for sync and health status, labels, and projects on the left sidebar.](https://kodekloud.com/kk-media/image/upload/v1752877465/notes-assets/images/GitOps-with-ArgoCD-ArgoCD-Vault-Plugin-with-ArgoCD/argo-cd-application-config-interface.jpg)

Within your Git repository, include a secret manifest that uses an annotation to specify the Vault path. An example manifest is:

```yaml theme={null}
kind: Secret
apiVersion: v1
metadata:
  name: app-crds
  annotations:
    avp.kubernetes.io/path: "credentials/data/app"
type: Opaque
stringData:
  apiKey: <apikey>
  username: <username>
  password: <password>
```

When the application is synchronized, the Vault plugin detects the annotation, connects to Vault (using the configuration provided either in the repo server’s secret or hard-coded), fetches the secret data from the specified path, and outputs a final Kubernetes Secret manifest.

In your ArgoCD application settings, configure the following Vault parameters (adjust based on your environment):

* AVP\_TYPE: vault
* AVP\_AUTH\_TYPE: token
* VAULT\_ADDR: e.g., [http://vault-app.vault-demo.svc.cluster.local:8200](http://vault-app.vault-demo.svc.cluster.local:8200)
* VAULT\_TOKEN: (Your Vault token)

![The image shows a user interface of Argo CD, displaying application settings with fields for revision, path, destination, and plugin configuration. The left sidebar includes filters and status indicators for sync and health.](https://kodekloud.com/kk-media/image/upload/v1752877466/notes-assets/images/GitOps-with-ArgoCD-ArgoCD-Vault-Plugin-with-ArgoCD/argo-cd-user-interface-settings.jpg)

Once configured, the application will connect to Vault and generate the desired manifest with resolved secret data.

***

## 6. Verifying the Application Deployment

After deploying your application, check the ArgoCD dashboard to ensure that the application status is synced and healthy.

![The image shows a dashboard interface of Argo CD, displaying a list of applications with their statuses, including options to sync, refresh, or delete each application. The applications are organized in a grid format, with details like project name, status, and repository URL.](https://kodekloud.com/kk-media/image/upload/v1752877467/notes-assets/images/GitOps-with-ArgoCD-ArgoCD-Vault-Plugin-with-ArgoCD/argo-cd-dashboard-applications-status.jpg)

Inspect the application details to confirm sync status and health. The Vault plugin replaces the secret placeholders with the actual data fetched from Vault.

![The image shows a configuration screen for an application in Argo CD, with settings for a Kubernetes cluster and a plugin named "argocd-vault-plugin." Various environment variables like VAULT\_TOKEN and VAULT\_ADDR are displayed.](https://kodekloud.com/kk-media/image/upload/v1752877468/notes-assets/images/GitOps-with-ArgoCD-ArgoCD-Vault-Plugin-with-ArgoCD/argo-cd-configuration-kubernetes-plugin.jpg)

To verify the new Kubernetes Secret with resolved data, run:

```bash theme={null}
# Verify the namespace and secret
kubectl get ns
kubectl -n <target-namespace> get secrets
```

To check the content of a secret, decode a value by replacing `<secret-name>` and `<key>`:

```bash theme={null}
kubectl -n <target-namespace> get secret <secret-name> -o json | jq -r '.data["<key>"]' | base64 -d
```

***

## 7. Additional CLI Configuration

You can perform further adjustments using the command line. For example, edit the repo server deployment or ConfigMap with these commands:

```bash theme={null}
kubectl -n argocd edit deploy argocd-repo-server
kubectl -n argocd edit cm argocd-cm
```

After applying your changes, check the pod status:

```bash theme={null}
kubectl -n argocd get po
```

Also, verify your Vault environment file (e.g., `vault.env`):

```bash theme={null}
cat vault.env
```

A sample `vault.env` file may look like this:

```bash theme={null}
VAULT_ADDR=http://vault-app.vault-demo.svc.cluster.local:8200
VAULT_TOKEN=s.OnqTXn3rmQoKuK7Xb87bWz
AVP_TYPE=vault
AVP_AUTH_TYPE=token
```

> **lightbulb** Always double-check your Vault credentials and make sure that all environment variables are correctly configured to ensure secure secret management.

***

## Conclusion

In this lesson, we demonstrated how to integrate HashiCorp Vault with ArgoCD using the Vault plugin. The key steps included:

1. Modifying the ArgoCD repo server deployment to download the plugin via an initContainer.
2. Optionally baking the plugin into a custom Docker image.
3. Configuring the ArgoCD ConfigMap to register and invoke the plugin.
4. Creating an application with Vault annotations so that the plugin fetches the secret data from Vault.
5. Verifying the application’s deployment using both the ArgoCD dashboard and CLI tools.

By following these steps, you enhance your GitOps workflow with robust secret management through Vault integrated with ArgoCD.

Thank you.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-argocd/module/ef6b6fef-0bd5-4fab-b437-b6d613fa74b4/lesson/3c526c11-5690-4ec9-95e5-b6e5e6c61549)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/gitops-with-argocd/module/ef6b6fef-0bd5-4fab-b437-b6d613fa74b4/lesson/248f96bc-53c0-41c2-8429-534ed8af4ede)


# Bitnami Sealed Secrets

Source: https://notes.kodekloud.com/docs/GitOps-with-ArgoCD/ArgoCD-AdvancedAdmin/Bitnami-Sealed-Secrets/page

This guide explores integrating Bitnami Sealed Secrets with ArgoCD to securely manage Kubernetes secrets in Git repositories.

In this guide, we explore how Bitnami Sealed Secrets integrates with ArgoCD to securely manage Kubernetes secrets. Bitnami Sealed Secrets allows you to encrypt plain Kubernetes secrets so they can be safely stored in Git repositories—public or private—without exposing sensitive data. Only the Sealed Secrets controller running in your cluster can decrypt these secrets at runtime.

## Creating a Kubernetes Secret

Typically, you create a Kubernetes secret using the kubectl CLI command or by applying a YAML manifest. However, in line with GitOps best practices, all resources—including secrets—should be stored declaratively in Git. The challenge arises when storing Base64-encoded secrets in a repository.

For instance, you can create a Kubernetes secret from a literal value by running:

```bash theme={null}
kubectl create secret generic mysql-password --from-literal=password=S1Ddh@rt# --dry-run=client -o yaml > mysql-password_k8s-secret.yaml
```

The command produces an output similar to this YAML manifest:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: mysql-password
data:
  password: czFEZGhAcnQj
```

## Overview of Available Solutions

There are several tools for managing Kubernetes secrets securely:

* Bitnami Sealed Secrets
* HashiCorp Vault
* Kubernetes External Secrets

In this article, our focus remains on Bitnami Sealed Secrets.

## How Bitnami Sealed Secrets Work

The Sealed Secrets controller is deployed inside your Kubernetes cluster. It converts a plain Kubernetes secret into a sealed secret that is safe to store in any Git repository—even a public one. Only the controller can decrypt the sealed secret, ensuring that sensitive information stays protected.

The controller can be installed in various ways, including Kustomize, Helm Charts, or directly from source. In our example, we deploy and manage the Sealed Secrets controller using ArgoCD via a Helm Chart.

> **lightbulb** Deploying the Sealed Secrets controller via ArgoCD is optional; you can also opt to use Helm directly.

Once the controller is running, the client-side tool KubeSeal encrypts your secret using asymmetric cryptography. KubeSeal automatically retrieves the public key from the running controller. If it cannot fetch the certificate automatically, you can manually specify it using the `-cert` flag. The certificate is typically stored in the Kubernetes secret created during the controller's installation.

## Deploying the Sealed Secrets Controller with ArgoCD

To deploy the Sealed Secrets controller with ArgoCD using a Helm Chart, run the following command:

```bash theme={null}
argocd app create sealed-secrets \
  --repo https://bitnami-labs.github.io/sealed-secrets \
  --helm-chart sealed-secrets \
  --revision 2.2.0 \
  --dest-server https://1.2.3.4 \
  --dest-namespace kube-system
```

The output will confirm the creation of the application:

```text theme={null}
application 'sealed-secrets' created
```

## Encrypting the Secret with KubeSeal

After deploying the controller, install the KubeSeal CLI tool. The installation command downloads and installs KubeSeal into the `/usr/local/bin` directory:

```bash theme={null}
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/kubeseal-0.18.0-linux-amd64.tar.gz -O kubeseal && sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

With KubeSeal installed, you can encrypt your Kubernetes secret by executing:

```bash theme={null}
kubeseal -o yaml --scope cluster-wide --cert sealedSecret.crt < mysql-password_k8s-secret.yaml > mysql-password_sealed-secret.yaml
```

After encryption, you will have two manifest files:

1. The original Secret manifest (for reference):

   ```yaml theme={null}
   apiVersion: v1
   kind: Secret
   metadata:
     name: mysql-password
   data:
     password: czFEZGhAcnQj
   ```

2. The SealedSecret manifest that can be stored safely in Git:

   ```yaml theme={null}
   apiVersion: bitnami.com/v1alpha1
   kind: SealedSecret
   metadata:
     name: mysql-password
   spec:
     encryptedData:
       password: AgBgdDGPdfg3nr7k3tA/Cg0bU2Q1dwT39ocVDs=
     annotations:
       sealedsecrets.bitnami.com/cluster-wide: "true"
   ```

When you apply the SealedSecret manifest to your cluster, the Sealed Secrets controller decrypts it and creates a regular Kubernetes Secret. Your pods then reference this secret as they would with any standard Kubernetes secret, with all encryption and decryption handled transparently.

## Summary

By leveraging Bitnami Sealed Secrets in combination with ArgoCD and KubeSeal, you ensure that your secrets remain encrypted and secure in Git repositories while maintaining adherence to GitOps principles. This approach protects your Kubernetes clusters by providing a robust and transparent method for managing secrets.

For further information and best practices, consider visiting these resources:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Bitnami Sealed Secrets GitHub Repository](https://github.com/bitnami-labs/sealed-secrets)

Thank you.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-with-argocd/module/ef6b6fef-0bd5-4fab-b437-b6d613fa74b4/lesson/782c3648-a892-4de6-ad13-c40b96503fe3)
