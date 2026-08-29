# Demo ReplicaSets

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/Kubernetes-Concepts-Pods-ReplicaSets-Deployments/Demo-ReplicaSets/page

Learn to create and manage ReplicaSets using a YAML file based on a pre-existing Pod definition in Kubernetes.

In this lesson, you will learn how to create and manage ReplicaSets using a YAML file based on a pre-existing Pod definition. Previously, we created Pods using YAML inside the "Pods" directory. Now, we will create a new directory called "ReplicaSets," where you will define your ReplicaSet in a file named "replica-set.yaml".

## Creating the ReplicaSet YAML File

Start by creating the "ReplicaSets" directory and then create a file named "replica-set.yaml" inside it. Begin your file by specifying the appropriate API version for ReplicaSets, which is `apps/v1`, followed by setting the kind as ReplicaSet.

Below is a sample YAML snippet for the ReplicaSet. The metadata includes the ReplicaSet’s name (`myapp-replicaset`) and a label (`app: myapp`). Within the `spec` section, Visual Studio Code's YAML extension may automatically add a selector field. Here, we are using the `matchLabels` option so that it matches the label in our previously created Pods. For instance, if your Pod’s definition uses a label such as `env: production`, include the same label in the ReplicaSet selector.

After defining the selector, specify the number of desired replicas (three in this example) and include the Pod template, which is copied from the original Pod YAML file. When pasting, ensure the indentation is correct; in Visual Studio Code, you can select the pasted block (except the first line) and press Tab twice to adjust the indentation.

Below is the sample YAML for our ReplicaSet, followed by the original Pod definition for reference:

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

<Callout icon="lightbulb">
  The label defined in the ReplicaSet's metadata (e.g., `app: myapp`) is not used for matching. Ensure that the label in the Pod template and the selector (here, `env: production`) match exactly to allow the ReplicaSet to manage the pods properly.
</Callout>

## Deploying the ReplicaSet

1. Save the "replica-set.yaml" file.

2. Open your terminal, navigate to the project root where the "ReplicaSets" directory is located, and verify the file exists:

   ```bash theme={null}
   admin@ubuntu-server replicatesets # ls
   replicaset.yaml
   admin@ubuntu-server replicatesets #
   ```

3. Use `cat` to inspect the file content and confirm its correctness:

   ```bash theme={null}
   admin@ubuntu-server replicatesets # cat replicaset.yaml
   ```

4. Create the ReplicaSet with the following command:

   ```bash theme={null}
   kubectl create -f replicaset.yaml
   ```

5. Check the status of the ReplicaSet:

   ```bash theme={null}
   kubectl get replicaset
   ```

   Expected output:

   ```bash theme={null}
   NAME               DESIRED   CURRENT   READY   AGE
   myapp-replicaset   3         3         3       8s
   ```

6. List the pods to further validate:

   ```bash theme={null}
   kubectl get pods
   ```

   Expected output:

   ```bash theme={null}
   NAME                     READY   STATUS    RESTARTS   AGE
   myapp-replicaset-8nxxl   1/1     Running   0          24s
   myapp-replicaset-jlgr2   1/1     Running   0          24s
   myapp-replicaset-pm4rl   1/1     Running   0          24s
   ```

Each pod name begins with the ReplicaSet's name (`myapp-replicaset`), making it easy to identify managed pods.

## Pod Deletion and Automatic Replacement

To verify that the ReplicaSet maintains the desired number of pods, delete one of them. For example:

```bash theme={null}
kubectl delete pod myapp-replicaset-8nxxl
```

After a few seconds, list the pods again:

```bash theme={null}
kubectl get pods
```

You will observe that although one pod is deleted, the ReplicaSet automatically creates a new one to maintain three replicas. For more details about this process, run:

```bash theme={null}
kubectl describe replicaset myapp-replicaset
```

This command displays the ReplicaSet's configuration, selectors, pod template details, and a history of events including the creation of replacement pods.

## Creating a Pod with Matching Labels

Now, consider what happens if you manually create a Pod that uses a label matching the ReplicaSet's selector. Use the following Pod definition saved as "nginx.yaml":

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx-2
  labels:
    app: myapp
spec:
  containers:
    - name: nginx
      image: nginx
```

If you create this pod using:

```bash theme={null}
kubectl create -f nginx.yaml
```

the new Pod might initially show a "terminating" status. This is because the ReplicaSet controller, which is responsible for maintaining the desired replica count, will delete any pod that does not fit its management criteria. You can confirm this behavior by inspecting the ReplicaSet events with:

```bash theme={null}
kubectl describe replicaset myapp-replicaset
```

## Updating a ReplicaSet

To update your ReplicaSet—for instance, changing the number of replicas from 3 to 4—run:

```bash theme={null}
kubectl edit replicaset myapp-replicaset
```

This command opens the ReplicaSet’s configuration in your default text editor. Note that the displayed file is temporary and includes fields managed by Kubernetes. Locate the `spec` section and update the replica count:

```yaml theme={null}
spec:
  replicas: 4
  selector:
    matchLabels:
      app: myapp
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

Save and exit the editor. Kubernetes will apply the changes immediately by creating new pods to meet the updated replica count. Verify the changes with:

```bash theme={null}
kubectl get pods
```

## Scaling with kubectl scale

Alternatively, you can scale the ReplicaSet without editing the configuration file by using the `kubectl scale` command. To scale down the ReplicaSet to two replicas, run:

```bash theme={null}
kubectl scale replicaset myapp-replicaset --replicas=2
```

After a short period, check the pods to confirm scaling:

```bash theme={null}
kubectl get pods
```

You might see an output like:

```bash theme={null}
NAME                     READY   STATUS        RESTARTS   AGE
myapp-replicaset-bvlst   0/1     Terminating   0          5m30s
myapp-replicaset-cssz8   0/1     Terminating   0          48s
myapp-replicaset-jlgr2   1/1     Running       0          6m31s
myapp-replicaset-pm4rl   1/1     Running       0          6m31s
```

Once the terminating pods are removed, only two pods should remain. Confirm the final state with:

```bash theme={null}
kubectl get pods
```

Expected final output:

```bash theme={null}
NAME                     READY   STATUS    RESTARTS   AGE
myapp-replicaset-jlgr2   1/1     Running   0          6m50s
myapp-replicaset-pm4rl   1/1     Running   0          6m50s
```

<Callout icon="lightbulb">
  This lesson demonstrated how to create, manage, update, and scale a ReplicaSet in Kubernetes. Using ReplicaSets ensures that the desired number of pod replicas are consistently maintained, promoting high availability in your deployments.
</Callout>

Happy clustering! For further reading, check out the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/0919dae3-bc94-479f-b205-d52156817c98/lesson/40e62ea3-3cef-494c-aa04-c5480ea2a901" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/0919dae3-bc94-479f-b205-d52156817c98/lesson/21cad4d7-4f5c-4896-b8dd-dea4a55b6c05" />
</CardGroup>
