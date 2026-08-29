# Demo Deploying voting app on Kubernetes with Deployments

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/Microservices-Architecture/Demo-Deploying-voting-app-on-Kubernetes-with-Deployments/page

This lesson explains how to deploy a voting app on Kubernetes using

In this lesson, we enhance the initial demo—which deployed Pods and Services directly—by leveraging Kubernetes Deployments. This improved approach addresses the challenges of scaling and updating applications without downtime. By using Deployments, you can automate the management of ReplicaSets, making it simple to scale, roll out updates, and perform rollbacks while retaining a history of revisions.

![The image illustrates a Kubernetes deployment architecture for a voting app, featuring multiple pods for voting, results, Redis, database, and worker services.](https://kodekloud.com/kk-media/image/upload/v1752884953/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Demo-Deploying-voting-app-on-Kubernetes-with-Deployments/frame_50.jpg)

> **lightbulb** Deploying individual Pods limits your ability to easily increase the number of service instances or update the container image without downtime. Using Deployments streamlines these processes.

In the upgraded setup, each application component—including the front-end apps (voting and results), databases, and worker applications—is encapsulated within its own Deployment. The project directory now hosts both the original Pod and Service definition files, along with new files for the Deployments.

***

## Voting App Deployment

We begin by defining a basic Pod for the voting app:

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

Then, create a Deployment file (`votingapp-deployment.yaml`) based on this pod template. Adjust the API version to `apps/v1`, change the kind to Deployment, and add the `selector` and `replicas` fields:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voting-app-deploy
  labels:
    name: voting-app-deploy
    app: demo-voting-app
spec:
  replicas: 1
  selector:
    matchLabels:
      name: voting-app-pod
      app: demo-voting-app
  template:
    metadata:
      name: voting-app-pod
      labels:
        name: voting-app-pod
        app: demo-voting-app
    spec:
      containers:
        - name: voting-app
          image: kodekloud/examplevotingapp
          ports:
            - containerPort: 80
```

This configuration allows you to start with a single replica on your cluster for resource efficiency, with the option to scale up as needed.

***

## Redis Deployment

Begin with the original Redis Pod definition:

```yaml theme={null}
