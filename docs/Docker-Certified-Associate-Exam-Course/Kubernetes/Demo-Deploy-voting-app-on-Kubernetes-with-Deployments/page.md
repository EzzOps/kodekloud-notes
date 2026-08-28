# Demo Deploy voting app on Kubernetes with Deployments

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Demo-Deploy-voting-app-on-Kubernetes-with-Deployments/page

This article demonstrates how to deploy a voting app on Kubernetes using Deployments for automated management and scaling.

Managing individual Pods poses challenges such as manual scaling and downtime during updates. Kubernetes **Deployments** resolve these by automating ReplicaSet management, rolling updates, and rollbacks.

<Callout icon="lightbulb">
  Deployments provide declarative updates, automatic rollbacks, and easy scaling.\
  Learn more: [Kubernetes Deployments](https://kubernetes.[SECRET_REDACTED]/).
</Callout>

## Voting App Architecture

<Frame>
  ![The image is a diagram of an example voting app architecture using Kubernetes, showing multiple pods for voting and result apps, along with Redis and database services. It illustrates the deployment and service connections between these components.](https://kodekloud.com/kk-media/image/upload/v1752873979/notes-assets/images/Docker-Certified-Associate-Exam-Course-Demo-Deploy-voting-app-on-Kubernetes-with-Deployments/voting-app-architecture-kubernetes-diagram.jpg)
</Frame>

## 1. Define Deployment Manifests

Below is a summary of all Deployment YAML files:

| Manifest File          | Component        | Image                                  |
| ---------------------- | ---------------- | -------------------------------------- |
| voting-app-deploy.yaml | Voting Frontend  | `kodekloud/examplevotingapp_vote:v1`   |
| redis-deploy.yaml      | Redis Cache      | `redis`                                |
| postgres-deploy.yaml   | PostgreSQL DB    | `postgres`                             |
| worker-app-deploy.yaml | Background Work  | `kodekloud/examplevotingapp_worker:v1` |
| result-app-deploy.yaml | Results Frontend | `kodekloud/examplevotingapp_result:v1` |

### voting-app-deploy.yaml

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voting-app-deploy
  labels:
    app: demo-voting-app
    component: voting
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-voting-app
      component: voting
  template:
    metadata:
      labels:
        app: demo-voting-app
        component: voting
    spec:
      containers:
      - name: voting-app
        image: kodekloud/examplevotingapp_vote:v1
        ports:
        - containerPort: 80
```

### redis-deploy.yaml

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deploy
  labels:
    app: demo-voting-app
    component: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-voting-app
      component: redis
  template:
    metadata:
      labels:
        app: demo-voting-app
        component: redis
    spec:
      containers:
      - name: redis
        image: redis
        ports:
        - containerPort: 6379
```

### postgres-deploy.yaml

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deploy
  labels:
    app: demo-voting-app
    component: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-voting-app
      component: postgres
  template:
    metadata:
      labels:
        app: demo-voting-app
        component: postgres
    spec:
      containers:
      - name: postgres
        image: postgres
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_USER
          value: "postgres"
        - name: POSTGRES_PASSWORD
          value: "postgres"
```

### worker-app-deploy.yaml

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker-app-deploy
  labels:
    app: demo-voting-app
    component: worker
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-voting-app
      component: worker
  template:
    metadata:
      labels:
        app: demo-voting-app
        component: worker
    spec:
      containers:
      - name: worker-app
        image: kodekloud/examplevotingapp_worker:v1
```

### result-app-deploy.yaml

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: result-app-deploy
  labels:
    app: demo-voting-app
    component: result
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-voting-app
      component: result
  template:
    metadata:
      labels:
        app: demo-voting-app
        component: result
    spec:
      containers:
      - name: result-app
        image: kodekloud/examplevotingapp_result:v1
        ports:
        - containerPort: 80
```

## 2. Apply Deployments and Services

First, ensure no leftover Pods or Services:

```bash theme={null}
kubectl get pods,svc
