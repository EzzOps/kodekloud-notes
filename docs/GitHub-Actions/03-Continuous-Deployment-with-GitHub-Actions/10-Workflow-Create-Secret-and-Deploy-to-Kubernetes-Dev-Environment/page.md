# Run azure/k8s-set-context@v3
with:
  method: kubeconfig
  kubeconfig: ***
  cluster-type: generic
env:
  MONGO_URI: mongodb+srv://supercluster.d83jj.mongodb.net/superData
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: ***

# Run kubectl version --short
Flag --short has been deprecated and will be removed in the future. The --short output will become the default.
Client Version: v1.26.0
Kustomize Version: v4.5.7
Server Version: v1.26.9

# Run kubectl get nodes
NAME                           STATUS   ROLES   AGE   VERSION
lke136455-201804-875c46000000  Ready    node    2d    v1.26.3
```

Using this setup, `kubectl` authenticates with your remote cluster via the secure Kubeconfig file stored in GitHub Actions secrets.

## Links and References

* [azure/setup-kubectl](https://github.com/Azure/setup-kubectl) – GitHub Action to install `kubectl`
* [azure/k8s-set-context](https://github.com/Azure/k8s-set-context) – GitHub Action to configure Kubernetes context
* [GitHub Actions Secrets](https://docs.github.com/actions/security-guides/encrypted-secrets)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/92928734-1d5a-462d-9414-2d3865f5ef79/lesson/f3f51b8d-1a5a-4060-86c6-fb65233bd156" />
</CardGroup>


# Workflow Create Secret and Deploy to Kubernetes Dev Environment

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Deployment-with-GitHub-Actions/Workflow-Create-Secret-and-Deploy-to-Kubernetes-Dev-Environment/page

This article explains how to create a MongoDB secret and deploy it to a Kubernetes development environment using GitHub Actions.

Extend your GitHub Actions CI/CD pipeline to securely generate a MongoDB secret and deploy your Kubernetes manifests into a `development` namespace. This ensures automated, secure credential management and consistent application delivery.

## 1. Configuring the Dev-Deploy Job

Under `jobs:` in your workflow YAML, add a `dev-deploy` job that:

* Replaces placeholders in your manifest files
* Creates a Kubernetes secret for MongoDB credentials
* Applies all manifests to your development namespace

```yaml theme={null}
name: Solar System Workflow

on:
  workflow_dispatch:
  push:
    branches:
      - main
      - 'feature/*'

env:
  MONGO_URI: 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: ${{ vars.MONGO_USERNAME }}
  MONGO_PASSWORD: ${{ secrets.MONGO_PASSWORD }}

jobs:
  unit-testing: … 
  code-coverage: … 
  docker: … 
  dev-deploy:
    name: Deploy to Dev Env
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Replace tokens in manifests
        uses: cschlieden/replace-tokens@v1
        with:
          tokenPrefix: '_{'
          tokenSuffix: '}'
          files:
            - kubernetes/development/*.yaml
        env:
          NAMESPACE: ${{ vars.NAMESPACE }}
          REPLICAS: ${{ vars.REPLICAS }}
          IMAGE: ${{ vars.DOCKERHUB_USERNAME }}/solar-system:${{ github.sha }}
          INGRESS_IP: ${{ env.INGRESS_IP }}

      - name: Show processed manifests
        run: cat kubernetes/development/*.yaml

      - name: Create MongoDB secret
        run: |
          kubectl -n ${{ vars.NAMESPACE }} create secret generic mongo-db-creds \
            --from-literal=MONGO_URI=${{ env.MONGO_URI }} \
            --from-literal=MONGO_USERNAME=${{ env.MONGO_USERNAME }} \
            --from-literal=MONGO_PASSWORD=${{ secrets.MONGO_PASSWORD }} \
            --save-config \
            --dry-run=client \
            -o yaml | kubectl apply -f -

      - name: Deploy manifests
        run: kubectl apply -f kubernetes/development
```

<Callout icon="lightbulb">
  Ensure that `vars.NAMESPACE`, `vars.REPLICAS`, and your Docker Hub credentials are configured in your GitHub repository settings.
</Callout>

### Workflow Steps at a Glance

| Step              | Action                  | Description                                        |
| ----------------- | ----------------------- | -------------------------------------------------- |
| Checkout          | `actions/checkout@v3`   | Clones your repository                             |
| Token Replacement | `replace-tokens@v1`     | Injects variables into Kubernetes YAML files       |
| Secret Creation   | `kubectl create secret` | Generates or updates `mongo-db-creds` in namespace |
| Deployment        | `kubectl apply`         | Applies all manifests in `kubernetes/development`  |

## 2. Kubernetes Deployment Manifest

In `kubernetes/development/deployment.yaml`, reference the `mongo-db-creds` secret to populate environment variables for your container:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: solar-system
  namespace: _{NAMESPACE}
  labels:
    app: solar-system
spec:
  replicas: _{REPLICAS}
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
          image: _{IMAGE}
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
              name: http
              protocol: TCP
      envFrom:
        - secretRef:
            name: mongo-db-creds
```

For more on Kubernetes secrets, see [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).

## 3. Why Use a Secret?

Your Dockerfile includes placeholder environment variables:

```dockerfile theme={null}
FROM node:18-alpine3.17
WORKDIR /usr/app
COPY package.json /usr/app/
RUN npm install
COPY . .

ENV MONGODB_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder

EXPOSE 3000
CMD ["npm", "start"]
```

By leveraging a Kubernetes secret:

* You avoid hard-coding sensitive data
* Credentials are injected at runtime
* Configuration is decoupled from your application image

<Callout icon="triangle-alert">
  Never commit real credentials into source control. Use GitHub Secrets and Kubernetes Secrets to manage sensitive data.
</Callout>

## 4. Verify a Fresh `development` Namespace

Before deployment, confirm that the namespace is empty:

```bash theme={null}
kubectl -n development get all
kubectl -n development get secrets
