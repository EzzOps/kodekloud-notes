# kubectl run nginx --image=nginx
pod/nginx created

# kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          3s
```

The output confirms that the pod is running. The "READY" column indicates how many containers are in a ready state, "RESTARTS" shows the number of times the container has restarted, and "AGE" reflects how long the pod has been active.

### Inspecting Pod Details

For more in-depth information about the pod—including its labels, node assignment, internal IP address, and container specifics—use the `kubectl describe` command:

```bash theme={null}
# kubectl run nginx --image=nginx
pod/nginx created

# kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          3s

# kubectl describe pod nginx
Name:           nginx
Namespace:      default
Priority:       0
Node:           minikube/192.168.99.100
Start Time:     Sat, 11 Jul 2020 00:49:39 -0400
Labels:         run=nginx
Annotations:    <none>
Status:         Running
IP:             172.17.0.3
IPs:
  IP: 172.17.0.3
Containers:
  nginx:
    Container ID:   docker://987785b312ad2e38c77132300f8709b8a027566462c2d18634ff13b34
    Image:          nginx
    Image ID:       docker-pullable://nginx@sha256:a23a9056789b968a186c5205f4
```

This command output provides essential metadata and status details such as the pod's start time, the node it is running on, and its internal IP address (172.17.0.3). If multiple containers were running within the pod, each would be listed under the "Containers" section.

Additionally, the bottom section of the output displays event information that tracks the lifecycle of the pod—from scheduling on the Minikube node to pulling the image and finally creating and launching the container:

```bash theme={null}
Initialized           True
Ready                 True
ContainersReady       True
PodScheduled          True
Volumes:
  default-token-f5ntk:
    Type:           Secret (a volume populated by a Secret)
    SecretName:     default-token-f5ntk
    Optional:       false
    QoS Class:      BestEffort
    Node-Selectors: <none>
    Tolerations:
      node.kubernetes.io/not-ready:NoExecute for 300s
      node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason             Age   From                Message
  ----    ------             ----  ----                -------
  Normal  Scheduled          46s   default-scheduler   Successfully assigned default/nginx to minikube
  Normal  Pulling            45s   kubelet, minikube   Pulling image "nginx"
  Normal  Pulled             44s   kubelet, minikube   Successfully pulled image "nginx"
  Normal  Created            44s   kubelet, minikube   Created container nginx
  Normal  Started            44s   kubelet, minikube   Started container nginx
```

### Viewing Pod Information in Wide Format

For a summary that also includes node and internal IP details, use the following command:

```bash theme={null}
kubectl get pods -o wide
```

The output will resemble:

```bash theme={null}
NAME    READY   STATUS    RESTARTS   AGE     IP           NODE       NOMINATED NODE
nginx   1/1     Running   0          2m28s   172.17.0.3   minikube   <none>
```

Here, each pod is assigned its own internal IP address (in this case, 172.17.0.3), which enables network communications within the cluster.

***

This demonstration has shown how to deploy a pod in a Minikube environment using the `kubectl` command line. In upcoming lessons, we will explore how to define pods using YAML configuration files for more complex deployment scenarios.

For further reading and detailed Kubernetes concepts, visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/509501a0-727a-41b9-b9a5-e022735c098e/lesson/9c2de9f5-180b-494e-970b-639cad788168" />
</CardGroup>


# Demo ReplicaSets

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Kubernetes-Resources/Demo-ReplicaSets/page

Learn to create and manage a ReplicaSet using a Pod definition file to maintain a consistent number of identical Pods.

In this lesson, you'll learn how to create and manage a ReplicaSet using a pre-existing Pod definition file. Previously, you created a Pod using YAML; now, we'll extend that knowledge by grouping Pods into a ReplicaSet to ensure that a consistent number of identical Pods is running at all times.

***

## Creating the ReplicaSet YAML

Start by navigating to your project directory. You should already have a directory named `pods` containing your Pod definition files. Next, create a new directory for ReplicaSets and add a file called `replicaset.yaml` inside it.

Open `replicaset.yaml` and begin by specifying the API version and kind. For ReplicaSets, use `apps/v1` as the API version and `ReplicaSet` as the kind. Then add metadata including the ReplicaSet’s name and labels. In this example, we use the label `app: myapp`.

Under the `spec` section:

* Define the `selector` that matches the labels on the Pods managed by this ReplicaSet.
* Set the number of replicas (e.g., 3).
* Provide the Pod template. You can copy the template from your existing Pod definition, but ensure that the indentation is correct after pasting.

<Callout icon="lightbulb">
  Ensure that the labels under the `selector` and in the Pod template exactly match, as these are the only labels that affect the ReplicaSet's operation. The label assigned to the ReplicaSet itself in the metadata is not used for matching.
</Callout>

Below is an example ReplicaSet definition:

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
---
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

***

## Validating the ReplicaSet Configuration

After saving the file, verify that your directory structure is correct. Your project root should now contain a new directory (for example, `replicatesets`) with the `replicaset.yaml` file. For instance:

```bash theme={null}
admin@ubuntu-server kubernetes-for-beginners # ls
pods replicates
admin@ubuntu-server kubernetes-for-beginners # cd replicatesets/
```

Check the file by listing its contents:

```bash theme={null}
admin@ubuntu-server replicatesets # ls
replicaset.yaml
admin@ubuntu-server replicatesets #
```

Clear your screen and create the ReplicaSet using:

```bash theme={null}
kubectl create -f replicatesets/replicaset.yaml
```

Soon after, you can verify the ReplicaSet status with:

```bash theme={null}
kubectl get replicaset
```

Expected output:

```bash theme={null}
NAME               DESIRED   CURRENT   READY   AGE
myapp-replicaset   3         3         3       8s
```

This output confirms that the ReplicaSet has successfully created three Pods. To inspect the created Pods further, run:

```bash theme={null}
kubectl get pods
```

You might see output similar to:

```bash theme={null}
NAME                     READY   STATUS    RESTARTS   AGE
myapp-replicaset-8nxxl   1/1     Running   0          24s
myapp-replicaset-jlgr2   1/1     Running   0          24s
myapp-replicaset-pm4rl   1/1     Running   0          24s
```

Note how each Pod's name begins with `myapp-replicaset`, indicating its association with the ReplicaSet.

***

## Testing the ReplicaSet Self-Healing

ReplicaSets continuously ensure that the defined number of Pods is running. To test this self-healing mechanism:

1. **List Your Pods:**\
   Identify a Pod to delete (e.g., one ending with `8nxxl`):

   ```bash theme={null}
   kubectl get pods
   ```

   Sample output:

   ```bash theme={null}
   NAME                     READY   STATUS    RESTARTS   AGE
   myapp-replicaset-8nxxl   1/1     Running   0          45s
   myapp-replicaset-jlgr2   1/1     Running   0          45s
   myapp-replicaset-pm4rl   1/1     Running   0          45s
   ```

2. **Delete the Selected Pod:**

   ```bash theme={null}
   kubectl delete pod myapp-replicaset-8nxxl
   ```

   You should see confirmation similar to:

   ```bash theme={null}
   pod "myapp-replicaset-8nxxl" deleted
   ```

After a few seconds, list the Pods again. The ReplicaSet will have automatically created a new Pod to maintain the desired replica count. To inspect the ReplicaSet details, including its events, run:

```bash theme={null}
kubectl describe replicaset myapp-replicaset
```

Scroll through the details to verify that a new Pod was created after deletion.

***

## Preventing Extra Pods from Running

A core feature of ReplicaSets is to ensure that only the specified number of Pods are active. If you attempt to create an additional Pod with a label matching the ReplicaSet selector, the ReplicaSet controller will automatically delete the extra Pod.

For instance, update your existing `nginx.yaml` file so that the Pod uses the same label as defined in the ReplicaSet selector:

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

Before applying changes, verify the current Pods:

```bash theme={null}
kubectl get pods
```

Then, create the Pod:

```bash theme={null}
kubectl create -f nginx.yaml
```

Shortly after, run:

```bash theme={null}
kubectl get pods
```

You'll notice that the extra Pod is immediately marked for termination. The ReplicaSet controller consistently enforces that only the predefined number of Pods remain active. To see related events, describe the ReplicaSet:

```bash theme={null}
kubectl describe replicaset myapp-replicaset
```

***

## Updating the ReplicaSet

There are scenarios where you may need to adjust the number of replicas in your ReplicaSet. There are two methods to achieve this:

### Method 1: Edit the Running Configuration

Use `kubectl edit` to modify the live configuration of the ReplicaSet. This command opens the configuration in your default text editor (such as Vim):

```bash theme={null}
kubectl edit replicaset myapp-replicaset
```

Modify the `spec.replicas` field (for example, change it from 3 to 4), then save and exit the editor. Kubernetes will immediately update the ReplicaSet and create new Pods as necessary. Verify the update by listing your Pods:

```bash theme={null}
kubectl get pods
```

### Method 2: Utilize the Scale Command

Alternatively, you can scale the ReplicaSet directly:

```bash theme={null}
kubectl scale replicaset myapp-replicaset --replicas=2
```

This command scales the ReplicaSet down to two Pods. Verify the change with:

```bash theme={null}
kubectl get pods
```

You may see an output similar to:

```bash theme={null}
NAME                    READY   STATUS      RESTARTS   AGE
myapp-replicaset-bvlst  0/1     Terminating 0          5m30s
myapp-replicaset-cssz8  0/1     Terminating 0          48s
myapp-replicaset-jlgr2  1/1     Running     0          6m31s
myapp-replicaset-pm4rl  1/1     Running     0          6m31s
```

After termination completes, only two Pods will remain active.

***

## Conclusion

In this lesson, you learned how to create a ReplicaSet from an existing Pod definition file, observed the self-healing behavior when Pods are deleted, and explored two methods to update the number of replicas—editing the running configuration or scaling directly. These features ensure that your cluster consistently maintains the desired number of active Pods.

Happy clustering, and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/509501a0-727a-41b9-b9a5-e022735c098e/lesson/95e8d2c6-3d72-44a5-9824-d60f54808b97" />
</CardGroup>
