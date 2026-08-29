# redis-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: redis-pod
  labels:
    app: demo-voting-app
spec:
  containers:
    - name: redis
      image: redis
      ports:
        - containerPort: 6379
```

Then, create the Redis Deployment (`redis-deploy.yaml`) using the same template as the voting app deployment. Update the component names, labels, and container details accordingly:

```yaml theme={null}
# redis-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deploy
  labels:
    name: redis-deploy
    app: demo-voting-app
spec:
  replicas: 1
  selector:
    matchLabels:
      name: redis-pod
      app: demo-voting-app
  template:
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

***

## PostgreSQL Deployment

Transform the PostgreSQL Pod into a Deployment. First, consider the original PostgreSQL Pod definition with environment variables:

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

Now, create the PostgreSQL Deployment (`postgres-deploy.yaml`). Ensure that the selector matches the Pod template labels:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deploy
  labels:
    name: postgres-deploy
    app: demo-voting-app
spec:
  replicas: 1
  selector:
    matchLabels:
      name: postgres-pod
      app: demo-voting-app
  template:
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

***

## Worker App Deployment

For the worker application, start with its Pod definition:

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
      image: kodekloud/examplevotingapp
```

Then, create a corresponding Deployment (`worker-app-deploy.yaml`). Update the names, labels, and selectors as required:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker-app-deploy
  labels:
    name: worker-app-deploy
    app: demo-voting-app
spec:
  replicas: 1
  selector:
    matchLabels:
      name: worker-app-pod
      app: demo-voting-app
  template:
    metadata:
      name: worker-app-pod
      labels:
        name: worker-app-pod
        app: demo-voting-app
    spec:
      containers:
        - name: worker-app
          image: kodekloud/examplevotingapp
```

***

## Result App Deployment

Similarly, convert the result application from a Pod to a Deployment. Create the file `result-app-deploy.yaml`, update the names and labels from the original Pod definition, and ensure that the template matches the selector criteria.

Your project directory should now include files similar to the following:

```text theme={null}
voting-app-pod.yaml
result-app-pod.yaml
redis-pod.yaml
postgres-pod.yaml
redis-service.yaml
postgres-service.yaml
voting-app-service.yaml
result-app-service.yaml
worker-app-pod.yaml
voting-app-deploy.yaml
redis-deploy.yaml
postgres-deploy.yaml
worker-app-deploy.yaml
result-app-deploy.yaml
```

***

## Deploying on Kubernetes

Before creating the new Deployments and Services, ensure that any previously created resources are removed. Verify by running:

```bash theme={null}
kubectl get pods
```

Once the cluster is clean, proceed with the deployments.

### Creating the Voting App Deployment

Deploy the voting app using the command below:

```bash theme={null}
kubectl create -f voting-app-deploy.yaml
```

Verify the deployment:

```bash theme={null}
kubectl get deployment
```

Expected output:

```bash theme={null}
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
voting-app-deploy   1/1     1            1           19s
```

### Deploying Redis, PostgreSQL, and Their Services

First, deploy Redis and its service:

```bash theme={null}
kubectl create -f redis-deploy.yaml
kubectl create -f redis-service.yaml
```

Then, deploy PostgreSQL and its service:

```bash theme={null}
kubectl create -f postgres-deploy.yaml
kubectl create -f postgres-service.yaml
```

Confirm that all Pods are running:

```bash theme={null}
kubectl get pods
```

Sample output:

```bash theme={null}
NAME                                 READY   STATUS    RESTARTS   AGE
postgres-deploy-847c9c8d8f-dzk8m     1/1     Running   0          19s
redis-deploy-5b479fbfd5-ndxbn         1/1     Running   0          27s
voting-app-deploy-7775f98f7d-2xdlz    1/1     Running   0          56s
```

### Deploying Worker and Result Applications

Deploy the worker application (which does not have an associated Service):

```bash theme={null}
kubectl create -f worker-app-deploy.yaml
```

Next, deploy the result application and its service:

```bash theme={null}
kubectl create -f result-app-deploy.yaml
kubectl create -f result-app-service.yaml
```

Finally, check that all Deployments and Services are active:

```bash theme={null}
kubectl get deployments,svc
```

Example output:

```bash theme={null}
NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/postgres-deploy         1/1     1            1           91s
deployment.apps/redis-deploy            1/1     1            1           99s
deployment.apps/result-app-deploy       1/1     1            1           18s
deployment.apps/voting-app-deploy       1/1     1            1           2m8s
deployment.apps/worker-app-deploy       1/1     1            1           45s

NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/db                  ClusterIP   10.107.65.177   <none>        5432/TCP         88s
service/kubernetes          ClusterIP   10.96.0.1       <none>        443/TCP          2d1h
service/redis               ClusterIP   10.104.71.94    <none>        6379/TCP         95s
service/result-service      NodePort    10.105.105.132  <none>        80:3005/TCP      15s
service/voting-service      NodePort    10.100.70.146   <none>        80:3004/TCP      119s
```

***

## Accessing the Front-End Applications

Use Minikube to retrieve the URLs for the voting and result services:

```bash theme={null}
minikube service voting-service --url
minikube service result-service --url
# Expected output: http://192.168.99.101:30005
```

Open these URLs in your web browser to interact with the voting app. Load balancing within the Deployment ensures that different pods serve your requests.

***

## Scaling the Voting App Deployment

Scaling the voting application is straightforward with Deployments. For example, to increase the number of voting app replicas from one to three, run:

```bash theme={null}
kubectl scale deployment voting-app-deploy --replicas=3
```

After scaling, verify the status:

```bash theme={null}
kubectl get deployments
```

Refresh the voting service URL in your browser several times to observe that requests are being handled by multiple pods, confirming that the scaling is effective.

***

This lesson demonstrates how Kubernetes Deployments simplify application management by enabling effortless scaling, rolling updates, and high availability. Happy deploying, and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/a603e70d-8473-4de4-aec9-7cc76c396ad3/lesson/3cf172f2-c6b0-4676-bfb0-6da0d0792814" />
</CardGroup>


# Demo Deploying voting app on Kubernetes

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/Microservices-Architecture/Demo-Deploying-voting-app-on-Kubernetes/page

This tutorial guides deploying a multi-tier voting application on

In this tutorial, you will deploy a multi-tier voting application on a Minikube cluster. This guide explains step-by-step how to create the pod definition files for each application component and then expose them using Kubernetes services.

***

## Pod Definitions

Start by creating a new project folder (e.g., "voting-app") and defining the pods for each component in separate YAML files.

### 1. Voting App Pod

Create a file named `voting-app-pod.yaml`. This file specifies the API version, kind, metadata (including name and labels), and the container details. The labels group all the components as part of the same application while differentiating each component.

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
      image: kodekloud/example-voting-app:_vote-v1
      ports:
        - containerPort: 80
```

### 2. Result App Pod

Copy the voting app pod template to create the result app pod. Save it as `result-app-pod.yaml` and update the metadata (name, labels) and container details accordingly.

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

### 3. Redis Pod

For the Redis pod, create a file named `redis-pod.yaml`. Use the previous template and update the names accordingly. Note that the container port has been changed from 80 to 6379 (the default Redis port).

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

### 4. PostgreSQL (DB) Pod

Using the Redis pod template, create the PostgreSQL pod definition file named `postgres-pod.yaml`. Update the pod and container names, use the official `postgres` image, and change the container port to 5432. Additionally, include environment variables for the initial username and password required by the worker and result pods.

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

### 5. Worker Pod

Finally, create the worker pod in a file named `worker-app-pod.yaml`. Use the voting app pod template as a base but update the name and container properties to indicate background processing. Since the worker does not run any service or listen on ports, remove the container port definition.

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

***

## Service Definitions

After defining the pods, create the corresponding services to expose them. All components except the worker require external or internal services.

### 1. Redis Service (Internal)

Create a file named `redis-service.yaml`. This service exposes the Redis pod on port 6379 internally, ensuring the selector matches the labels defined in the Redis pod.

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

### 2. PostgreSQL (DB) Service (Internal)

Since the worker expects the Postgres service name to be "DB", create a file named `postgres-service.yaml`. This service exposes PostgreSQL on port 5432 and selects the appropriate pod.

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

### 3. Voting App Service (External)

To make the front-end voting app accessible externally, create a service named `voting-app-service.yaml`. Set the service type to `NodePort`, expose port 80, and assign a node port, such as 30004. Ensure that the selector matches the labels defined in the voting app pod.

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

### 4. Result App Service (External)

Similarly, create an external service for the result app. Save this file as `result-app-service.yaml`. This service is also set to type `NodePort`, exposing port 80 with a node port (e.g., 30005). Update the selector to match the result app pod.

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

***

## Deploying the Application

With all five pod and service definition files created, navigate to your project directory (e.g., `voting-app`) and deploy each object using the `kubectl create -f` command.

```bash theme={null}
