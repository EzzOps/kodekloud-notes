# Demo Deployments

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/Kubernetes-Concepts-Pods-ReplicaSets-Deployments/Demo-Deployments/page

This lesson covers creating a Kubernetes deployment using an existing ReplicaSet definition to streamline the process.

In this lesson, we will create a Kubernetes deployment by leveraging an existing ReplicaSet definition. This approach helps streamline the process by reusing a familiar structure.

## Step 1: Set Up the Deployment Directory

First, navigate to your project directory and create a new folder called `deployments`. Inside this folder, create a file named `deployment.yaml`.

## Step 2: Review the ReplicaSet Definition

For reference, open the existing ReplicaSet definition on the right side of your split editor:

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

> **lightbulb** Review this ReplicaSet definition carefully, as you will reuse its structure when defining your new deployment.

## Step 3: Create the Deployment Configuration

In your new `deployment.yaml` file, start with the `apiVersion` (apps/v1) as used in the ReplicaSet. Set the kind to `Deployment`, and then define the metadata with a unique name and appropriate labels. In our example, we use the name `myapp-deployment` with labels like `tier: frontend` and `app: nginx`.

For the spec section, copy the structure from the ReplicaSet but modify the configuration to meet the deployment requirements. In this case, we reduce the number of replicas from four to three.

Below is the final configuration for your deployment:

```yaml theme={null}
