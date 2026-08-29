# Demo Replica Sets

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Demo-Replica-Sets/page

This guide teaches how to define, deploy, self-heal, and scale a Kubernetes ReplicaSet for high availability and fault tolerance.

In this guide, you’ll learn how to define, deploy, self-heal, and scale a Kubernetes ReplicaSet. A ReplicaSet ensures a specified number of Pod replicas are running at all times, providing high availability and fault tolerance.

## Directory Structure

Assuming your project root is named `Kubernetes-for-Beginners`, the layout might look like this:

```text theme={null}
Kubernetes-for-Beginners/
├── pods/
│   └── nginx.yaml
└── replicasets/
    └── replicaset.yaml
```

## 1. Defining the ReplicaSet

Create the file `replicasets/replicaset.yaml`:

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
      env: production
  replicas: 3
  template:
    metadata:
      name: nginx-2
      labels:
        env: production
    spec:
      containers:
        - name: nginx
          image: nginx
```

<Callout icon="lightbulb">
  The `selector.matchLabels` field must exactly match the labels under `template.metadata.labels`. The labels in `metadata.labels` on the ReplicaSet itself are not used for Pod selection.
</Callout>

For reference, here’s the original Pod definition in `pods/nginx.yaml`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx-2
  labels:
    env: production
spec:
  containers:
    - name: nginx
      image: nginx
```

## 2. Deploying the ReplicaSet

From the project root, apply the ReplicaSet manifest:

```bash theme={null}
cd replicasets
kubectl create -f replicaset.yaml
```

Verify the ReplicaSet and its Pods:

```bash theme={null}
kubectl get replicaset
