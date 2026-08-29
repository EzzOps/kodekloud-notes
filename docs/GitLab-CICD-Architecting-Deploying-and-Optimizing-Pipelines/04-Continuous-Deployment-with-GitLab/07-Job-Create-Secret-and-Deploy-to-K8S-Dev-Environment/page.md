# .gitlab-ci.yml (without KUBECONFIG)
k8s_dev_deploy:
  stage: dev-deploy
  image: alpine:3.7
  before_script:
    - wget https://storage.googleapis.com/kubernetes-release/release/\
$(wget -q -O - https://storage.googleapis.com/kubernetes-release/stable.txt)/\
bin/linux/amd64/kubectl
    - chmod +x kubectl && mv kubectl /usr/bin/kubectl
  script:
    - kubectl version -o yaml
```

Attempting to run the job yields:

```bash theme={null}
$ kubectl version -o yaml
ClientVersion:
  gitVersion: v1.29.1
...
ERROR: Job failed: exit code 1
```

Without server credentials in a `kubeconfig`, `kubectl` cannot reach your cluster’s API endpoint.

## Local vs. CI: Kubernetes Authentication

### On Your Local Machine

With a valid `~/.kube/config`, you will see both client and server versions:

```bash theme={null}
$ kubectl version -o yaml
```

```yaml theme={null}
clientVersion:
  gitVersion: v1.29.1
serverVersion:
  gitVersion: v1.29.1
```

Your trimmed `kubeconfig` might look like this:

```yaml theme={null}
apiVersion: v1
clusters:
- name: vke-cluster
  cluster:
    server: https://example-cluster:6443
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0t...
contexts:
- name: vke-cluster
  context:
    cluster: vke-cluster
    user: admin
current-context: vke-cluster
kind: Config
users:
- name: admin
  user:
    client-certificate-data: <omitted>
    client-key-data: <omitted>
```

Verify your context and nodes locally:

```bash theme={null}
kubectl config get-contexts
kubectl get nodes
```

## Storing Kubeconfig in GitLab CI/CD

To securely pass your `kubeconfig` into CI jobs, add it as a **File**-type variable in your project’s CI/CD Settings:

| Key               | Type | Value                             | Environment Scope |
| ----------------- | ---- | --------------------------------- | ----------------- |
| `DEV_KUBE_CONFIG` | File | *Paste entire kubeconfig content* | All (or specific) |

![The image shows a GitLab CI/CD settings page where variables are being managed, with options to add a new variable and configure its type and flags.](https://kodekloud.com/kk-media/image/upload/v1752877199/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Job-Configuring-Kubeconfig-file/gitlab-ci-cd-variables-settings.jpg)

> **triangle-alert** Treat your `kubeconfig` as sensitive data. File variables are stored encrypted, but avoid exposing them in job logs or unsecured scopes.

## Updating the CI Job to Use Kubeconfig

Modify your `.gitlab-ci.yml` job to export the `KUBECONFIG` environment variable from the File variable before invoking any `kubectl` commands:

```yaml theme={null}
# .gitlab-ci.yml
k8s_dev_deploy:
  stage: dev-deploy
  image: alpine:3.7
  before_script:
    - wget https://storage.googleapis.com/kubernetes-release/release/\
$(wget -q -O - https://storage.googleapis.com/kubernetes-release/stable.txt)/\
bin/linux/amd64/kubectl
    - chmod +x kubectl && mv kubectl /usr/bin/kubectl
  script:
    - export KUBECONFIG=$DEV_KUBE_CONFIG
    - kubectl version -o yaml
    - kubectl config get-contexts
    - kubectl get nodes
```

Commit your changes and trigger the pipeline. The `k8s_dev_deploy` job should now complete successfully:

![The image shows a GitLab CI/CD job interface where a job named "k8s\_dev\_deploy" has successfully passed. The job log details the steps executed, and the interface includes project navigation options on the left.](https://kodekloud.com/kk-media/image/upload/v1752877201/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Job-Configuring-Kubeconfig-file/gitlab-ci-cd-k8s-dev-deploy.jpg)

## Verifying the CI Job Output

With the kubeconfig in place, your CI job will display both client and server details and list the cluster nodes:

```bash theme={null}
$ kubectl version -o yaml
ClientVersion:
  gitVersion: v1.29.1
ServerVersion:
  gitVersion: v1.29.1

$ kubectl config get-contexts
CURRENT   NAME            CLUSTER         AUTHINFO
*         vke-cluster     vke-cluster     admin

$ kubectl get nodes
NAME                  STATUS   ROLES    AGE   VERSION
gitlab-node-1         Ready    <none>   5h    v1.29.1
gitlab-node-2         Ready    <none>   5h    v1.29.1
```

## Further Reading and References

* [Kubernetes Configuration Best Practices](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
* [GitLab CI/CD Variables Documentation](https://docs.gitlab.com/ee/ci/variables/#file-type)
* [Kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/17485780-3db2-4065-b9dd-16389dd03093)


# Job Create Secret and Deploy to K8S Dev Environment

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Deployment-with-GitLab/Job-Create-Secret-and-Deploy-to-K8S-Dev-Environment/page

This guide covers creating a Kubernetes Secret and deploying application manifests to the development namespace using GitLab CI/CD.

In this guide, we’ll walk through creating a Kubernetes Secret and deploying application manifests to the `development` namespace using GitLab CI/CD. You’ll learn how to integrate secret creation into your pipeline and verify a successful deploy.

## 1. Verify the Development Namespace

First, confirm the `development` namespace is clean:

```bash theme={null}
kubectl -n development get all
```

*No resources found in development namespace.*

> **lightbulb** Always ensure you’re targeting the correct namespace before deploying to avoid unintended changes.

***

## 2. Initial CI Job Definition

Here’s a basic `k8s_dev_deploy` job from `.gitlab-ci.yml`:

```yaml theme={null}
k8s_dev_deploy:
  stage: dev-deploy
  image: alpine:3.7
  dependencies: []
  before_script:
    - wget https://storage.googleapis.com/kubernetes-release/release/$(wget -q -O - https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    - chmod +x ./kubectl && mv ./kubectl /usr/bin/kubectl
    - apk add --no-cache gettext
    - envsubst -V
  script:
    - export KUBECONFIG=$DEV_KUBE_CONFIG
    - kubectl version -o yaml
    - kubectl config get-contexts
    - kubectl get nodes
    - export INGRESS_IP=$(kubectl -n ingress-nginx get service ingress-nginx-controller -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
    - for manifest in kubernetes/manifest/*.yaml; do
        envsubst < $manifest | kubectl apply -f -
      done
```

> **triangle-alert** At this stage, deployment will fail because the application requires a `mongo-db-creds` secret that doesn’t exist yet.

***

## 3. Required Manifests

Define the Kubernetes resources for your application. Below are two essential manifest examples:

### Ingress

```yaml theme={null}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: solar-system
  namespace: ${NAMESPACE}
  annotations:
    kubernetes.io/ingress.class: nginx
    kubernetes.io/tls-acme: "true"
spec:
  rules:
    - host: solar-system-${NAMESPACE}.${INGRESS_IP}.nip.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: solar-system
                port:
                  number: 3000
  tls:
    - hosts:
        - solar-system-${NAMESPACE}.${INGRESS_IP}.nip.io
      secretName: ingress-local-tls
```

### Deployment

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: solar-system
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS}
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
          image: ${K8S_IMAGE}
          imagePullPolicy: Always
          ports:
            - name: http
              containerPort: 3000
      envFrom:
        - secretRef:
            name: mongo-db-creds
```

| Resource   | Purpose                                    |
| ---------- | ------------------------------------------ |
| Ingress    | Route HTTP/TLS traffic to the service      |
| Deployment | Manage pods, replicas, and rolling updates |

The `mongo-db-creds` secret must include:

* `MONGO_URI`
* `MONGO_USERNAME`
* `MONGO_PASSWORD`

***

## 4. Create Secret and Update CI Job

Incorporate secret creation into your pipeline before applying manifests:

```yaml theme={null}
k8s_dev_deploy:
  stage: dev-deploy
  image: alpine:3.7
  dependencies: []
  before_script:
    - wget https://storage.googleapis.com/kubernetes-release/release/$(wget -q -O - https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    - chmod +x ./kubectl && mv ./kubectl /usr/bin/kubectl
    - apk add --no-cache gettext
    - envsubst -V
  script:
    - export KUBECONFIG=$DEV_KUBE_CONFIG
    - INGRESS_IP=$(kubectl -n ingress-nginx get service ingress-nginx-controller -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
    - echo "Ingress IP: $INGRESS_IP"
    - kubectl -n $NAMESPACE create secret generic mongo-db-creds \
        --from-literal=MONGO_URI="$MONGO_URI" \
        --from-literal=MONGO_USERNAME="$MONGO_USERNAME" \
        --from-literal=MONGO_PASSWORD="$MONGO_PASSWORD" \
        --dry-run=client -o yaml | kubectl apply -f -
    - for manifest in kubernetes/manifest/*.yaml; do
        envsubst < $manifest | kubectl apply -f -
      done
    - kubectl -n $NAMESPACE get all,secret,ingress
```

> **lightbulb** Using `--dry-run=client -o yaml` ensures idempotent secret creation.

***

## 5. Pipeline Configuration

Define the overall GitLab pipeline, stages, and variables:

```yaml theme={null}
workflow:
  name: Solar System NodeJS Pipeline

stages:
  - test
  - containerization
  - dev-deploy

variables:
  DOCKER_USERNAME: siddharth67
  IMAGE_VERSION: $CI_PIPELINE_ID
  K8S_IMAGE: $DOCKER_USERNAME/solar-system:$IMAGE_VERSION
  MONGO_URI: 'mongodb+srv://supercluster.d83ji.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: $M_DB_PASSWORD
```

| Variable          | Description                         |
| ----------------- | ----------------------------------- |
| `DOCKER_USERNAME` | Docker Hub username                 |
| `IMAGE_VERSION`   | Image tag (CI pipeline ID)          |
| `K8S_IMAGE`       | Full image name for Kubernetes pull |
| `MONGO_*`         | MongoDB connection credentials      |

Include a containerization job if needed:

```yaml theme={null}
docker_build:
  stage: containerization
  image: docker:24.0.5
  services:
    - docker:24.0.5-dind
  script:
    - docker load -i image/solar-system-image:$IMAGE_VERSION.tar
    - docker login --username=$DOCKER_USERNAME --password=$DOCKER_PASSWORD
    - docker push $K8S_IMAGE
```

Once pushed, GitLab will visualize the pipeline:

![The image shows a GitLab CI/CD pipeline interface for a NodeJS project named "Solar System," displaying completed jobs for containerization and deployment stages.](https://kodekloud.com/kk-media/image/upload/v1752877201/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Job-Create-Secret-and-Deploy-to-K8S-Dev-Environment/gitlab-cicd-nodejs-solar-system.jpg)

***

## 6. Inspect the Dev-Deploy Logs

Your `dev-deploy` job logs should look like this:

```bash theme={null}
$ envsubst -V
envsubst (GNU gettext-runtime) 0.19.8.1
$ export KUBECONFIG=$DEV_KUBE_CONFIG
$ kubectl version -o yaml
