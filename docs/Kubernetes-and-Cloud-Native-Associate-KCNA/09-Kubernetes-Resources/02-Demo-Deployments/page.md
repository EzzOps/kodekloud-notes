# Demo Deployments

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Kubernetes-Resources/Demo-Deployments/page

Learn to create a Kubernetes Deployment using a ReplicaSet definition, including setup, configuration, deployment, and verification steps.

In this lesson, you will learn how to create a Kubernetes Deployment using a configuration similar to a ReplicaSet definition. Follow these steps to create a Deployment, starting from setting up the necessary files to verifying the deployment status in your cluster.

## Step 1: Set Up Your Project Directory

Create a new folder called `Deployments` within your project directory. Then, inside the `Deployments` folder, create a file named `deployment.yaml`.

<Callout icon="lightbulb">
  Using a split editor can help you compare the new deployment file with your existing ReplicaSet definition side by side.
</Callout>

## Step 2: Base Your Deployment on the ReplicaSet Definition

Locate your existing `ReplicaSet.yaml` file and open it in a split view with your new `deployment.yaml` file. This approach lets you reference the ReplicaSet configuration while you build your Deployment.

Begin your `deployment.yaml` file by specifying the API version and kind. Since the ReplicaSet uses `apps/v1`, you will use the same API version, but change the kind to `Deployment`:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
```

## Step 3: Define Metadata

Next, add metadata details for your deployment. For example, set the deployment name to `myapp-deployment` and include labels to help categorize and identify the deployment:

```yaml theme={null}
metadata:
  name: myapp-deployment
  labels:
    tier: frontend
    app: nginx
```

## Step 4: Configure the Spec Section

The specification section of the deployment is very similar to the ReplicaSet's. You can copy the spec section from `ReplicaSet.yaml` and modify it as necessary. In this example, update the replica count to three:

```yaml theme={null}
spec:
  selector:
    matchLabels:
      app: myapp
  replicas: 3
  template:
    metadata:
      name: nginx-2
      labels:
        app: myapp
    spec:
      containers:
        - name: nginx
          image: nginx
```

For reference, here is the original `ReplicaSet.yaml` content that served as a starting point:

```yaml theme={null}
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-replicaset
  labels:
    app: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  replicas: 4
  template:
    metadata:
      name: nginx-2
      labels:
        app: myapp
    spec:
      containers:
        - name: nginx
          image: nginx
```

## Step 5: Deploy Your Configuration

After saving your changes to `deployment.yaml`, open your terminal, navigate to the project's root directory, and confirm that the `Deployments` directory exists.

To create the deployment, run the following command using `kubectl` with the `-f` flag to specify your deployment file:

```bash theme={null}
kubectl create -f deployment.yaml
```

Once the command completes, verify the deployment's status with:

```bash theme={null}
kubectl get deployments
```

You should see output indicating that the deployment is running with three available Pods, similar to the following:

```text theme={null}
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
myapp-deployment    3/3     3            3           10s
```

## Step 6: Verify the Pods and Deployment Details

To view the Pods created by the ReplicaSet for this deployment, execute:

```bash theme={null}
kubectl get pods
```

The output will list the three running Pods, for example:

```text theme={null}
NAME                     READY   STATUS    RESTARTS   AGE
myapp-replicaset-pjs89   1/1     Running   0          34m
myapp-replicaset-pwv6h   1/1     Running   0          34m
myapp-replicaset-zr6c7   1/1     Running   0          23s
```

Next, inspect the details of your deployment by running:

```bash theme={null}
kubectl describe deployment myapp-deployment
```

This command provides comprehensive information, including the deployment's name, namespace, labels, POD template details, and scaling events indicating that three Pods are ready.

## Step 7: List All Kubernetes Objects

To view all objects created in your cluster, run the following command:

```bash theme={null}
kubectl get all
```

This will display the deployment, its corresponding ReplicaSet (named `myapp-replicaset`), and the three Pods managed by the ReplicaSet.

<Callout icon="lightbulb">
  This lesson has guided you through creating a Kubernetes Deployment from a ReplicaSet template, deploying it using `kubectl`, and verifying the deployment along with its associated Pods.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/509501a0-727a-41b9-b9a5-e022735c098e/lesson/5dcb9f63-d684-43e9-b647-c2e8f75582dc" />
</CardGroup>
