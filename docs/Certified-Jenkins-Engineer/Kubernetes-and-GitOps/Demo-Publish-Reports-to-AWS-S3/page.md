# deployment.yaml  service.yaml
```

Open **kubernetes/deployment.yaml** to confirm its contents:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: solar-system
  namespace: solar-system
  labels:
    app: solar-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: solar-system
  template:
    metadata:
      labels:
        app: solar-system
    spec:
      containers:
        - name: solar-system
          image: siddharth67/solar-system:3e906e3be059342b1916f020c034434fb267dca
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
              name: http
```

This deployment expects a secret named `mongo-db-creds`, which you’ll create in the next sections.

***

## 2. Migrate to Your Git Host

If you need to host your manifests elsewhere (for example, Gitea or another GitHub organization), use your Git provider’s import or migration tools:

<Frame>
  ![The image shows a web interface for migrating a Git repository, with fields for the repository URL, access token, and options for migration settings.](https://kodekloud.com/kk-media/image/upload/v1752870940/notes-assets/images/Certified-Jenkins-Engineer-Demo-Manifest-Repository-and-Configure-ArgoCD/git-repo-migration-interface.jpg)
</Frame>

After migration, ensure that both `kubernetes/deployment.yaml` and `kubernetes/service.yaml` are present in your new repository.

***

## 3. Create the MongoDB Secret

Verify your Kubernetes cluster context and namespaces:

```bash theme={null}
kubectl get namespaces
# NAME              STATUS   AGE
# argocd            Active   2d20h
# default           Active   3d1h
# kube-system       Active   3d1h
kubectl get nodes -o wide
# NAME           STATUS   AGE   VERSION
# node-1         Ready    3d1h  v1.29.9
# node-2         Ready    3d1h  v1.29.9
```

Generate a Kubernetes Secret manifest for your MongoDB credentials without applying it:

```bash theme={null}
kubectl -n solar-system create secret generic mongo-db-creds \
  --from-literal=MONGO_URI='mongodb+srv://supercluster.d83jji.mongodb.net/superData' \
  --from-literal=MONGO_USERNAME='superuser' \
  --from-literal=MONGO_PASSWORD='SuperPassword' \
  --save-config --dry-run=client -o yaml > mongo-creds_k8s-secret.yaml
```

Inspect the output:

```yaml theme={null}
apiVersion: v1
kind: Secret
metadata:
  name: mongo-db-creds
  namespace: solar-system
data:
  MONGO_URI: bW9uZ2RiOi8v...
  MONGO_USERNAME: c3VwZXJ1c2Vy
  MONGO_PASSWORD: U3VwZXJQYXdzd29yZA==
```

<Callout icon="triangle-alert">
  Do **not** commit raw secrets to Git. Use an encryption mechanism like [Bitnami Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) to secure your credentials.
</Callout>

***

## 4. Seal the Secret with Bitnami Sealed Secrets

### 4.1 Retrieve the Controller’s Public Certificate

Check that the Sealed Secrets controller is running:

```bash theme={null}
kubectl -n kube-system get pods | grep sealed-secrets
# sealed-secrets-controller-xxxxx   1/1     Running   20h
```

Find its TLS secret:

```bash theme={null}
kubectl -n kube-system get secrets | grep sealed
# sealed-secrets-key8dv5k   kubernetes.io/tls   2      20h
```

Extract the certificate:

```bash theme={null}
kubectl -n kube-system get secret sealed-secrets-key8dv5k \
  -o jsonpath='{.data.tls\.crt}' | base64 -d > sealed-secret-public-cert.crt
```

### 4.2 Install and Verify `kubeseal`

Ensure you have the `kubeseal` CLI:

```bash theme={null}
kubeseal --version
# kubeseal version: v0.27.1
```

### 4.3 Create the SealedSecret

Encrypt your Secret manifest:

```bash theme={null}
kubeseal --cert sealed-secret-public-cert.crt \
  --scope cluster-wide \
  -o yaml < mongo-creds_k8s-secret.yaml > mongo-creds_sealed-secret.yaml
```

The resulting file looks like this:

```yaml theme={null}
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mongo-db-creds
  namespace: solar-system
  annotations:
    sealedsecrets.bitnami.com/cluster-wide: "true"
spec:
  encryptedData:
    MONGO_URI: Ag0/...
    MONGO_USERNAME: A1gZx...
    MONGO_PASSWORD: Ag0/wX...
```

Commit **only** the sealed secret and other manifest files to Git.

***

## 5. Configure Argo CD

Verify Argo CD is running in the `argocd` namespace:

```bash theme={null}
kubectl -n argocd get all
# NAME                          TYPE        CLUSTER-IP       PORT(S)
# service/argocd-server         NodePort    10.245.106.185   80:31663/TCP,443:32346/TCP
# deployment.apps/argocd-server 1/1         1                2d20h
# statefulset/apps/argocd-application-controller 1/1   2d20h
```

The server’s NodePort is **31663**, accessible via CLI or browser.

<Frame>
  ![The image shows the Argo CD interface displaying an application named "bitnami-sealed-secrets" with its status as "Healthy" but "OutOfSync." The interface includes options to sync, refresh, or delete the application.](https://kodekloud.com/kk-media/image/upload/v1752870943/notes-assets/images/Certified-Jenkins-Engineer-Demo-Manifest-Repository-and-Configure-ArgoCD/argo-cd-bitnami-sealed-secrets.jpg)
</Frame>

### 5.1 Create the Solar System Application

1. In the Argo CD UI, click **+ New App**.
2. Enter the following:
   * **Application Name**: `solar-system-argo-app`
   * **Project**: `default`
   * **Sync Policy**: Manual
   * **Destination Namespace**: `solar-system` (enable auto-create)
   * **Repository URL**: `<your-manifest-repo-url>`
   * **Revision**: `main`
   * **Path**: `kubernetes`
3. Click **Create**.

<Frame>
  ![The image shows a Gitea repository interface for "solar-system-gitops-argocd," displaying recent commits and a README file outlining its use for Kubernetes manifest files in a project demo via Jenkins.](https://kodekloud.com/kk-media/image/upload/v1752870945/notes-assets/images/Certified-Jenkins-Engineer-Demo-Manifest-Repository-and-Configure-ArgoCD/gitea-solar-system-gitops-argocd.jpg)
</Frame>

<Frame>
  ![The image shows a user interface of Argo CD, displaying application settings with options for source repository configuration and sync status.](https://kodekloud.com/kk-media/image/upload/v1752870946/notes-assets/images/Certified-Jenkins-Engineer-Demo-Manifest-Repository-and-Configure-ArgoCD/argo-cd-application-settings-ui.jpg)
</Frame>

After creating the app, Argo CD will mark it **OutOfSync**:

<Frame>
  ![The image shows the Argo CD interface displaying two applications, "bitnami-sealed-secrets" and "solar-system-argo-app," both marked as "OutOfSync" with different health statuses.](https://kodekloud.com/kk-media/image/upload/v1752870947/notes-assets/images/Certified-Jenkins-Engineer-Demo-Manifest-Repository-and-Configure-ArgoCD/argo-cd-bitnami-solar-system-outofsync.jpg)
</Frame>

Inspect details to troubleshoot missing resources:

<Frame>
  ![The image shows an Argo CD interface displaying the status of an application called "solar-system-argo-app," which is currently "OutOfSync" and "Missing." The interface includes a visual representation of the application's components and their statuses.](https://kodekloud.com/kk-media/image/upload/v1752870948/notes-assets/images/Certified-Jenkins-Engineer-Demo-Manifest-Repository-and-Configure-ArgoCD/argo-cd-solar-system-status.jpg)
</Frame>

Whenever you update `deployment.yaml` (for example, bumping the Docker image tag) and push your commit, return to Argo CD and click **Sync** to deploy the changes.

<Frame>
  ![The image shows a Git repository interface with a list of YAML files related to Kubernetes, including "deployment.yml," "secret.yml," and "service.yml." The files have recent commit messages and timestamps.](https://kodekloud.com/kk-media/image/upload/v1752870949/notes-assets/images/Certified-Jenkins-Engineer-Demo-Manifest-Repository-and-Configure-ArgoCD/git-repo-yaml-files-kubernetes.jpg)
</Frame>

***

## Conclusion

You’ve now:

* Cloned and migrated a Kubernetes manifest repository.
* Created and encrypted a MongoDB Secret using Bitnami Sealed Secrets.
* Configured an Argo CD application to deploy the Solar System app.

This GitOps approach ensures all manifests and secrets remain in Git as the single source of truth, with strong encryption and declarative deployments.

***

## Links and References

* [Argo CD Documentation](https://argoproj.github.io/argo-cd/)
* [Bitnami Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
* [Gitea](https://gitea.io/)
* [GitHub](https://github.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/01d04ab3-0694-4c67-bd1a-c3eaaa8d64d3/lesson/d2103553-e170-4740-9d5f-ff1d755c4cb6" />
</CardGroup>


# Demo Publish Reports to AWS S3

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Kubernetes-and-GitOps/Demo-Publish-Reports-to-AWS-S3/page

Learn to upload Jenkins pipeline test, coverage, and security reports to an Amazon S3 bucket for centralized storage and sharing.

In this guide, you’ll learn how to upload your Jenkins pipeline’s test, coverage, and security reports to an Amazon S3 bucket. This approach centralizes all your build artifacts in S3 for easy sharing and long-term storage.

**Table of Contents**

1. [Inspecting the Jenkins Workspace](#inspecting-the-jenkins-workspace)
2. [Creating the S3 Bucket](#creating-the-s3-bucket)
3. [Configuring IAM and Jenkins Credentials](#configuring-iam-and-jenkins-credentials)
4. [Installing the Pipeline: AWS Steps Plugin](#installing-the-pipeline-aws-steps-plugin)
5. [Generating an S3 Upload Snippet](#generating-an-s3-upload-snippet)
6. [Adding the Upload Stage to the Jenkinsfile](#adding-the-upload-stage-to-the-jenkinsfile)
7. [Authenticating with AWS in the Pipeline](#authenticating-with-aws-in-the-pipeline)
8. [Running the Pipeline](#running-the-pipeline)
9. [Reviewing the Console Output](#reviewing-the-console-output)
10. [Verifying Artifacts in S3](#verifying-artifacts-in-s3)
11. [Links and References](#links-and-references)

***

## Inspecting the Jenkins Workspace

First, browse your Jenkins workspace via the Classic UI to verify all generated reports are present:

```bash theme={null}
nodejs:22-6-0  – Use a tool from a predefined Tool Installation
