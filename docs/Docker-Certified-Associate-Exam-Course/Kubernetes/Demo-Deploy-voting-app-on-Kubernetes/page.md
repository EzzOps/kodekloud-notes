# No resources found
```

Create each Deployment and its Service:

```bash theme={null}
kubectl apply -f voting-app-deploy.yaml
kubectl apply -f voting-app-service.yaml

kubectl apply -f redis-deploy.yaml
kubectl apply -f redis-service.yaml

kubectl apply -f postgres-deploy.yaml
kubectl apply -f postgres-service.yaml

kubectl apply -f worker-app-deploy.yaml

kubectl apply -f result-app-deploy.yaml
kubectl apply -f result-app-service.yaml
```

## 3. Verify Deployments and Services

Check Deployments and Pods:

```bash theme={null}
kubectl get deployments
kubectl get pods
```

Confirm Services:

```bash theme={null}
kubectl get svc
```

| SERVICE        | TYPE      | CLUSTER-IP | PORT(S)      |
| -------------- | --------- | ---------- | ------------ |
| voting-service | NodePort  | 10.100.x.y | 80:30004/TCP |
| result-service | NodePort  | 10.105.x.z | 80:30005/TCP |
| redis          | ClusterIP | 10.104.x.y | 6379/TCP     |
| db             | ClusterIP | 10.107.x.z | 5432/TCP     |

## 4. Access Front-end Services

Retrieve and open URLs:

```bash theme={null}
minikube service voting-service --url
minikube service result-service --url
```

Visit the voting app, cast a vote, then check the result app to verify it’s recorded.

## 5. Scale the Front-end

Scaling with Deployments is straightforward. Increase replicas for the voting app:

```bash theme={null}
kubectl scale deployment voting-app-deploy --replicas=3
```

Verify three Pods are Running:

```bash theme={null}
kubectl get pods -l component=voting
```

Refresh the voting URL to observe traffic served by multiple replicas—no downtime required!

***

## Links and References

* [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* [Minikube Service Command](https://minikube.sigs.k8s.io/docs/commands/service/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/fe0a56cf-2269-4e44-a14f-8a56f6c40583" />
</CardGroup>


# Demo Deploy voting app on Kubernetes

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Demo-Deploy-voting-app-on-Kubernetes/page

Tutorial showing how to deploy a multi-tier voting application on Minikube using Pod and Service YAML manifests for frontend, worker, Redis and Postgres components

In this tutorial you'll deploy the multi-tier voting application to a Minikube cluster. The app consists of five components: voting frontend, result frontend, redis, postgres, and a worker. We'll create one Pod manifest per component and Services to expose them. The project directory is named `voting-app`.

Prerequisites:

* Minikube or a Kubernetes cluster
* kubectl configured to target your cluster
* Files saved under the `voting-app` directory

Quick reference:

* Source for the sample images: [dockersamples/example-voting-app](https://github.com/dockersamples/example-voting-app)
* Kubernetes docs: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

## Pod manifests

Create the following Pod YAML files inside the `voting-app` directory.

Voting app Pod (voting-app-pod.yaml)

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: voting-app-pod
  labels:
    name: voting-app-pod
    app: demo-voting-app
spec:
  containers:
  - name: voting-app
    image: kodekloud/examplevotingapp_vote:v1
    ports:
    - containerPort: 80
```

The voting app image referenced above comes from a sample repository similar to the one below: [dockersamples/example-voting-app](https://github.com/dockersamples/example-voting-app)

<Frame>
  <img alt="A screenshot of a GitHub repository page for &#x22;dockersamples/example-voting-app,&#x22; showing the Code tab with a file list, branch selector, commit info, and action buttons like &#x22;Go to file,&#x22; &#x22;Add file,&#x22; and &#x22;Code.&#x22;" />
</Frame>

Result app Pod (result-app-pod.yaml)

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: result-app-pod
  labels:
    name: result-app-pod
    app: demo-voting-app
spec:
  containers:
  - name: result-app
    image: kodekloud/examplevotingapp_result:v1
    ports:
    - containerPort: 80
```

Redis Pod (redis-pod.yaml)

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: redis-pod
  labels:
    name: redis-pod
    app: demo-voting-app
spec:
  containers:
  - name: redis
    image: redis
    ports:
    - containerPort: 6379
```

Postgres Pod (postgres-pod.yaml)

The worker and result components require a PostgreSQL database. For this demo we inject credentials via plain environment variables in the Pod manifest. In production, store credentials securely using Kubernetes Secrets or an external vault.

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: postgres-pod
  labels:
    name: postgres-pod
    app: demo-voting-app
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

<Callout icon="lightbulb">
  Using plain text environment variables for database credentials is convenient for demos, but in production you should store credentials in Kubernetes Secrets or a vault solution.
</Callout>

Worker Pod (worker-app-pod.yaml)

The worker is an internal background process and does not expose network ports, so we omit the ports section.

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: worker-app-pod
  labels:
    name: worker-app-pod
    app: demo-voting-app
spec:
  containers:
  - name: worker-app
    image: kodekloud/examplevotingapp_worker:v1
```

## Service manifests

Create Services to expose the Pods. Redis and Postgres use internal ClusterIP Services. The frontends are exposed via NodePort so they are accessible from your host/Minikube.

Redis Service (redis-service.yaml)

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: redis
  labels:
    name: redis-service
    app: demo-voting-app
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    name: redis-pod
    app: demo-voting-app
```

Postgres Service (postgres-service.yaml / named `db`)

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: db
  labels:
    name: postgres-service
    app: demo-voting-app
spec:
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    name: postgres-pod
    app: demo-voting-app
```

Voting Service (voting-app-service.yaml) — NodePort on 30004

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: voting-service
  labels:
    name: voting-service
    app: demo-voting-app
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30004
  selector:
    name: voting-app-pod
    app: demo-voting-app
```

Result Service (result-app-service.yaml) — NodePort on 30005

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: result-service
  labels:
    name: result-service
    app: demo-voting-app
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30005
  selector:
    name: result-app-pod
    app: demo-voting-app
```

## Resources summary

| Resource                    | Purpose                                               | Service Type / Port                 |
| --------------------------- | ----------------------------------------------------- | ----------------------------------- |
| voting-app-pod (voting-app) | Frontend to submit votes                              | NodePort — 80 -> 30004              |
| result-app-pod (result-app) | Shows aggregated results                              | NodePort — 80 -> 30005              |
| redis-pod (redis)           | Queue/storage for votes                               | ClusterIP — 6379                    |
| postgres-pod (postgres)     | Persistent storage for aggregated results             | ClusterIP — 5432 (service name: db) |
| worker-app-pod (worker)     | Background worker to move data from Redis -> Postgres | Internal, no service                |

## Apply manifests and verify

From the `voting-app` directory (where all YAML files are saved), apply the manifests in the following recommended order (frontend first, then datastore services, then worker, then result frontend):

Example file listing

```bash theme={null}
admin@ubuntu-server voting-app# ls
postgres-pod.yaml    postgres-service.yaml    redis-pod.yaml
redis-service.yaml   result-app-pod.yaml      result-app-service.yaml
voting-app-pod.yaml  voting-app-service.yaml  worker-app-pod.yaml
```

Create resources

```bash theme={null}
