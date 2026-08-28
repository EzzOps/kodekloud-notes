# replicaset.yaml (for reference)
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
      labels:
        app: myapp
    spec:
      containers:
      - name: nginx
        image: nginx
```

***

## 2. Create the Deployment manifest

Copy the spec from the ReplicaSet into `deployments/deployment.yaml`, then:

* Change `kind` to `Deployment`
* Set `metadata.name` and labels to match your application
* Adjust `replicas` to **3** (or your desired count)

```yaml theme={null}
# deployments/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    tier: frontend
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: nginx
        image: nginx
```

<Callout icon="lightbulb">
  The `selector.matchLabels` field must exactly match the labels on the Pod template. Otherwise, Kubernetes won’t know which Pods belong to this Deployment.
</Callout>

***

## 3. Apply the Deployment

Run:

```bash theme={null}
kubectl apply -f deployments/deployment.yaml
```

Or, if you prefer `create`:

```bash theme={null}
kubectl create -f deployments/deployment.yaml
```

***

## 4. Verify the rollout and inspect resources

You can quickly see the status of your Deployment and its Pods:

| Action                | Command                                        | Description                                  |
| --------------------- | ---------------------------------------------- | -------------------------------------------- |
| List Deployments      | `kubectl get deployments`                      | Show READY, UP-TO-DATE, AVAILABLE columns    |
| List all Pods         | `kubectl get pods`                             | Confirm your Pods are Running                |
| Describe a Deployment | `kubectl describe deployment myapp-deployment` | View events, strategy, and replica counts    |
| List all resources    | `kubectl get all`                              | Get Pods, Services, Deployments, ReplicaSets |

1. **Check the Deployment status**
   ```bash theme={null}
   kubectl get deployments
   ```
   Example output:
   ```text theme={null}
   NAME               READY   UP-TO-DATE   AVAILABLE   AGE
   myapp-deployment   3/3     3            3           10s
   ```

2. **List the Pods**
   ```bash theme={null}
   kubectl get pods
   ```
   Example output:
   ```text theme={null}
   NAME                                    READY   STATUS    RESTARTS   AGE
   myapp-deployment-5d8fcb5b6c-abc         1/1     Running   0          30s
   myapp-deployment-5d8fcb5b6c-def         1/1     Running   0          30s
   myapp-deployment-5d8fcb5b6c-ghi         1/1     Running   0          30s
   ```

3. **Describe the Deployment**
   ```bash theme={null}
   kubectl describe deployment myapp-deployment
   ```
   You’ll see details such as desired vs. available replicas, rollout strategy, and recent events:

<Frame>
  ![The image shows a terminal window displaying Kubernetes deployment details for an application named "myapp," including container information, conditions, and events related to scaling the replica set.](https://kodekloud.com/kk-media/image/upload/v1752873987/notes-assets/images/Docker-Certified-Associate-Exam-Course-Demo-Deployments/kubernetes-myapp-deployment-details.jpg)
</Frame>

4. **View all objects in the namespace**
   ```bash theme={null}
   kubectl get all
   ```
   Example output:
   ```text theme={null}
   NAME                                   READY   STATUS    RESTARTS   AGE
   pod/myapp-deployment-5d8fcb5b6c-abc    1/1     Running   0          1m
   pod/myapp-deployment-5d8fcb5b6c-def    1/1     Running   0          1m
   pod/myapp-deployment-5d8fcb5b6c-ghi    1/1     Running   0          1m

   NAME                     TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
   service/kubernetes       ClusterIP   10.96.0.1      <none>        443/TCP   15m

   NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/myapp-deployment   3/3     3            3           1m

   NAME                                          DESIRED   CURRENT   READY   AGE
   replicaset.apps/myapp-deployment-5d8fcb5b6c   3         3         3       1m
   ```

<Callout icon="lightbulb">
  To roll out updates, modify `spec.template.spec.containers[].image` and run:

  ```bash theme={null}
  kubectl apply -f deployments/deployment.yaml
  ```

  Then track progress with:

  ```bash theme={null}
  kubectl rollout status deployment/myapp-deployment
  ```
</Callout>

***

## Links and References

* [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
* [Rolling Updates and Rollbacks](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/cfd3de08-2ac9-429b-ac3c-aee10229f83e" />
</CardGroup>


# Demo PODS with YAML

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Demo-PODS-with-YAML/page

This guide explains how to create and deploy a Kubernetes Pod using a YAML manifest without `kubectl run`.

In this guide, you'll author a `pod.yaml` manifest and deploy a simple NGINX Pod without using `kubectl run`. Defining Pods in YAML is ideal for version control, reproducibility, and automation in CI/CD pipelines.

## 1. Create the YAML file

1. Open your terminal and launch your editor to create **pod.yaml**:
   ```bash theme={null}
   vim pod.yaml
   ```
2. Every Pod manifest requires four top-level fields:
   ```yaml theme={null}
   apiVersion: v1
   kind: Pod
   metadata:
   spec:
   ```

## 2. Add metadata

Under `metadata`, set a unique name and labels to organize and select resources:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
    tier: frontend
spec:
```

<Callout icon="lightbulb">
  YAML is sensitive to spaces. Always use **two spaces** per indent level and avoid tabs.
</Callout>

## 3. Define the Pod spec

Inside `spec`, list your containers. Each entry needs at least `name` and `image`:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
    tier: frontend
spec:
  containers:
    - name: nginx
      image: nginx
```

Add more containers by appending additional list items under `containers`.

Save and exit your editor (e.g., in Vim: `Esc` then `:wq`).

## 4. Verify the manifest

Inspect the content to ensure indentation and syntax are correct:

```bash theme={null}
cat pod.yaml
```

Expected output:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
    tier: frontend
spec:
  containers:
    - name: nginx
      image: nginx
```

## 5. Deploy the Pod

Apply the YAML manifest to create the Pod:

```bash theme={null}
kubectl apply -f pod.yaml
```

You should see:

```console theme={null}
pod/nginx created
```

<Callout icon="triangle-alert">
  `kubectl apply -f` is idempotent and tracks changes, while `kubectl create -f` errors if the object already exists. For iterative edits, prefer `apply`.
</Callout>

Use this command to check the Pod's status:

```bash theme={null}
kubectl get pod nginx
```

Wait until `STATUS` transitions to **Running**.

## 6. Inspect and debug

For detailed Pod information and events:

```bash theme={null}
kubectl describe pod nginx
```

Sample output highlights Pod health, container state, and recent events:

```console theme={null}
Name:         nginx
Namespace:    default
Status:       Running
IP:           172.17.0.3
Containers:
  nginx:
    Image:     nginx
    State:     Running
    Ready:     True
    Restart Count: 0
Events:
  Type    Reason     Age   Message
  ----    ------     ----  -------
  Normal  Scheduled  10s   Successfully assigned default/nginx to minikube
  Normal  Pulling    10s   Pulling image "nginx"
```

## Quick Reference

| Command                   | Description                 | Example                      |
| ------------------------- | --------------------------- | ---------------------------- |
| Create or update resource | Apply YAML manifest         | `kubectl apply -f pod.yaml`  |
| List Pods                 | View Pod status             | `kubectl get pod nginx`      |
| Describe Pod              | Detailed Pod and event logs | `kubectl describe pod nginx` |

## Links and References

* [Kubernetes Official Documentation](https://kubernetes.io/docs/)
* [YAML Specification](https://yaml.org/spec/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

***

Next, explore advanced manifest templating with Kustomize and Helm.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/8c84a314-515e-431e-9dbe-62c434da9772" />
</CardGroup>
