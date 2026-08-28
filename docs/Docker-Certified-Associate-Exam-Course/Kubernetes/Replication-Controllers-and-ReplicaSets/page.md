# Replication Controllers and ReplicaSets

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Replication-Controllers-and-ReplicaSets/page

This article explains Kubernetes Replication Controllers and ReplicaSets, their differences, usage, and how to create and manage them for high availability.

Kubernetes controllers act as the control plane’s “brain,” continuously observing cluster objects and reconciling the current state with your declared desired state. In this lesson, we’ll deep dive into two controllers that manage Pod replicas: **ReplicationController** and **ReplicaSet**.

## Why Use Replication Controllers?

Running a single Pod is risky—if it crashes, your application goes offline. A ReplicationController (RC) maintains a specified number of identical Pods, ensuring high availability and load distribution.

* High availability: If one Pod fails, others continue serving traffic.

<Frame>
  ![The image illustrates a high availability setup with a user accessing a node containing a replication controller managing two pods.](https://kodekloud.com/kk-media/image/upload/v1752874026/notes-assets/images/Docker-Certified-Associate-Exam-Course-Replication-Controllers-and-ReplicaSets/high-availability-replication-controller-pods.jpg)
</Frame>

* Redundancy and load balancing across nodes:

<Frame>
  ![The image illustrates a high availability setup with two nodes, each containing a replication controller and pods, indicating redundancy and load balancing.](https://kodekloud.com/kk-media/image/upload/v1752874028/notes-assets/images/Docker-Certified-Associate-Exam-Course-Replication-Controllers-and-ReplicaSets/high-availability-setup-nodes-redundancy.jpg)
</Frame>

* Scaling across nodes to meet growing demand:

<Frame>
  ![The image illustrates a load balancing and scaling concept using Kubernetes, showing multiple pods distributed across nodes with a replication controller managing them.](https://kodekloud.com/kk-media/image/upload/v1752874029/notes-assets/images/Docker-Certified-Associate-Exam-Course-Replication-Controllers-and-ReplicaSets/kubernetes-load-balancing-scaling-diagram.jpg)
</Frame>

## ReplicationController vs. ReplicaSet

While both controllers maintain a set of Pod replicas, **ReplicaSet** (RS) is the modern API (`apps/v1`) and supports set-based label selectors. **ReplicationController** (`v1`) is older and has fewer selector capabilities. We recommend using ReplicaSets for new deployments.

| Feature               | ReplicationController (`v1`) | ReplicaSet (`apps/v1`)           |
| --------------------- | ---------------------------- | -------------------------------- |
| API Version           | v1                           | apps/v1                          |
| Selector Support      | Equality-based labels only   | Equality & set-based label match |
| Recommended for Usage | Deprecated                   | Yes                              |

## Creating a ReplicationController

1. Define `rc-definition.yaml`:

   ```yaml theme={null}
   apiVersion: v1
   kind: ReplicationController
   metadata:
     name: myapp-rc
     labels:
       app: myapp
       tier: front-end
   spec:
     replicas: 3
     template:
       metadata:
         name: myapp-pod
         labels:
           app: myapp
           tier: front-end
       spec:
         containers:
           - name: nginx-container
             image: nginx
   ```

2. Apply the manifest and verify:

   ```bash theme={null}
   kubectl create -f rc-definition.yaml
   kubectl get replicationcontroller
   ```

   Example output:

   ```text theme={null}
   NAME       DESIRED   CURRENT   READY   AGE
   myapp-rc   3         3         3       19s
   ```

3. List Pods managed by the RC:

   ```bash theme={null}
   kubectl get pods
   ```

   ```text theme={null}
   NAME            READY   STATUS    RESTARTS   AGE
   myapp-rc-4lvk9  1/1     Running   0          20s
   myapp-rc-mc2mf  1/1     Running   0          20s
   myapp-rc-px9pz  1/1     Running   0          20s
   ```

## Introducing ReplicaSets

A ReplicaSet manifest closely mirrors an RC, with two key differences:

* **apiVersion**: `apps/v1`
* **selector**: Required to match Pods

```yaml theme={null}
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-replicaset
  labels:
    app: myapp
    tier: front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      tier: front-end
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        tier: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx
```

Apply and verify:

```bash theme={null}
kubectl create -f replicaset-definition.yaml
kubectl get replicaset
kubectl get pods
```

## Labels and Selectors

Labels are key/value pairs attached to objects. A ReplicaSet’s `spec.selector.matchLabels` determines which Pods it manages—even pre-existing ones.

Example Pod with labels:

```yaml theme={null}
metadata:
  name: myapp-pod
  labels:
    tier: front-end
```

Matching selector in a ReplicaSet:

```yaml theme={null}
selector:
  matchLabels:
    tier: front-end
```

## Scaling a ReplicaSet

You can adjust replica counts by editing the YAML or using `kubectl scale`:

Option 1: Update `replicas` in `replicaset-definition.yaml` and apply:

```bash theme={null}
kubectl replace -f replicaset-definition.yaml
```

Option 2: Scale on the fly:

```bash theme={null}
kubectl scale --replicas=6 -f replicaset-definition.yaml
```

<Callout icon="lightbulb">
  Using `kubectl scale` updates in-memory replica counts but does not modify your source YAML file.\
  For automatic scaling based on metrics, see the [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
</Callout>

## Command Cheat Sheet

| Command                                    | Description                          |
| ------------------------------------------ | ------------------------------------ |
| kubectl create -f `<file>`                 | Create any Kubernetes object         |
| kubectl get `<resource>`                   | List resources (e.g., pods, rs)      |
| kubectl delete `<resource>` `<name>`       | Delete a resource by name            |
| kubectl replace -f `<file>`                | Update by replacing the manifest     |
| kubectl scale --replicas=`<n>` -f `<file>` | Scale replicas from the command line |

## Links and References

* [Kubernetes Controllers](https://kubernetes.[AWS_SECRET_ACCESS_KEY]/)
* [ReplicationController API](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#replicationcontroller-v1-core)
* [ReplicaSet API](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/#replicaset-v1-apps)
* [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/85653cf3-ce30-4902-9354-69e981880eeb" />
</CardGroup>
