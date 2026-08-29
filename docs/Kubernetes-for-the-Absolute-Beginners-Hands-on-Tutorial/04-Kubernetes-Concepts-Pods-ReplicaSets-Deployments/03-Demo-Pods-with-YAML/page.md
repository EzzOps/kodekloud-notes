# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    tier: frontend
    app: nginx
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

<Callout icon="lightbulb">
  The deployment uses the same selector as the ReplicaSet, matching on `app: myapp`. This ensures that the deployment's pods are correctly managed.
</Callout>

## Step 4: Reference the Original ReplicaSet Definition

For comparison, here is the unchanged ReplicaSet definition saved in `replicaset.yaml`:

```yaml theme={null}
# replicaset.yaml
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

## Step 5: Deploy the Configuration to Your Cluster

Save your deployment configuration and create the deployment by running the following command in your terminal:

```bash theme={null}
kubectl create -f deployment.yaml
```

After creating the deployment, verify it with:

```bash theme={null}
kubectl get deployments
```

The output should resemble:

```bash theme={null}
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
myapp-deployment    3/3     3            3           10s
```

## Step 6: Validate the Pods

To inspect the pods created by the deployment, execute:

```bash theme={null}
kubectl get pods
```

Expected output:

```bash theme={null}
NAME                     READY   STATUS    RESTARTS   AGE
myapp-replicaset-pjs89   1/1     Running   0          34m
myapp-replicaset-pwv6h   1/1     Running   0          34m
myapp-replicaset-zr6c7   1/1     Running   0          23s
```

For more detailed information about your deployment, use:

```bash theme={null}
kubectl describe deployment myapp-deployment
```

This command provides comprehensive details on metadata, pod specifications, and events. You will see that the deployment uses the same selector (`app: myapp`), ensuring three desired and three available pods are running.

## Step 7: Review All Cluster Objects

Finally, run the following command to list all objects created in the cluster:

```bash theme={null}
kubectl get all
```

A sample output might look like this:

```bash theme={null}
NAME                                   READY   STATUS      RESTARTS   AGE
pod/myapp-replicaset-pjs89             1/1     Running     0          35m
pod/myapp-replicaset-pwv6h             1/1     Running     0          35m
pod/myapp-replicaset-zr6c7             1/1     Running     0          104s

NAME                                   TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
service/kubernetes                     ClusterIP   10.96.0.1     <none>        443/TCP    65m

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/myapp-deployment       3/3     3            3           105s

NAME                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/myapp-replicaset       3         3         3       35m
```

This output confirms that both the deployment and its corresponding ReplicaSet have been successfully created, with the expected pods up and running.

<Callout icon="lightbulb">
  You have now successfully deployed your application using Kubernetes Deployments. Experiment with these configurations in your practice environment for a deeper understanding of Kubernetes object management.
</Callout>

## Additional Resources

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/0919dae3-bc94-479f-b205-d52156817c98/lesson/7e954681-d6dc-4997-9c21-d7ed27daff64" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/0919dae3-bc94-479f-b205-d52156817c98/lesson/a04dde16-f00b-454b-8314-8e7357b3d7ad" />
</CardGroup>


# Demo Pods with YAML

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/Kubernetes-Concepts-Pods-ReplicaSets-Deployments/Demo-Pods-with-YAML/page

This article explains how to create a Kubernetes Pod using a YAML definition file instead of the kubectl run command.

In this article, we will walk you through the process of creating a Kubernetes Pod using a YAML definition file. Instead of using the traditional "kubectl run" command, you will learn how to define all pod specifications within a YAML file and then deploy the pod with the appropriate kubectl commands. This approach not only promotes consistency but also enhances version control.

## Step 1: Preparing the YAML File

Choose your favorite text editor to create the YAML file. On Windows, Notepad++ is a recommended option due to its syntax support, while on Linux, editors like vi or vim work well. In this example, we will use vim.

Open your terminal and create a new file named `pod.yaml`:

```bash theme={null}
vim pod.yaml
```

Inside `pod.yaml`, we define four top-level properties: `apiVersion`, `kind`, `metadata`, and `spec`. Consider the following key points:

* **apiVersion**: Use `"v1"` for a pod.
* **kind**: Set this to `"Pod"` (note the case sensitivity with a capital "P").
* **metadata**: This section acts as a dictionary where you can specify the pod’s name and labels. In our example, we assign the name `"nginx"` and labels such as `app: nginx` and `tier: frontend`.
* **spec**: Under this key, you define a list of containers. Each container has attributes like a name and an image. Here, we define a single container also named `"nginx"` using the Docker Hub image `nginx`.

Below is the complete YAML file for our pod definition:

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

<Callout icon="lightbulb">
  Ensure consistent indentation in your YAML file. Use two spaces per indent level (avoid using tabs) to guarantee that keys like `name` and `labels` are recognized as children of the `metadata` key, and similarly for entries under `spec`.
</Callout>

After editing the file, save and exit vim by pressing Escape and typing `:wq`.

## Step 2: Verifying the YAML File

To confirm that your YAML file is correctly saved and formatted, use the `cat` command:

```bash theme={null}
cat pod.yaml
```

You should see the YAML content displayed exactly as defined.

## Step 3: Creating the Pod

To deploy the pod to your Kubernetes cluster, you have the option of using either the `create` or `apply` commands. Although both function similarly when creating new objects, we will use the `apply` command:

```bash theme={null}
kubectl apply -f pod.yaml
```

The expected output should be:

```bash theme={null}
pod/nginx created
```

## Step 4: Checking Pod Status

Once created, it is important to verify that the pod is running properly. First, list all pods using:

```bash theme={null}
kubectl get pods
```

At first, the pod may be in a "ContainerCreating" state before transitioning to "Running." For detailed information about the pod, including container statuses, volumes, and events, run the following describe command:

```bash theme={null}
kubectl describe pod nginx
```

An example output of this command might look like:

```bash theme={null}
Initialized                True
Ready                      True
ContainersReady            True
PodScheduled               True
Volumes:
  default-token-f5ntk:
    Type:          Secret (a volume populated by a Secret)
    SecretName:    default-token-f5ntk
    Optional:      false
QoS Class:     BestEffort
Node-Selectors: <none>
Tolerations:
  node.kubernetes.io/not-ready:NoExecute for 300s
  node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason     Age   From               Message
  ----    -----      ----  ----               ------
  Normal  Scheduled  21s   default-scheduler  Successfully assigned default/nginx to m
  Normal  Pulling    20s   kubelet, minikube  Pulling image "nginx"
  Normal  Pulled     14s   kubelet, minikube  Successfully pulled image "nginx"
  Normal  Created    14s   kubelet, minikube  Created container nginx
  Normal  Started    14s   kubelet, minikube  Started container nginx
```

<Callout icon="lightbulb">
  For further troubleshooting or monitoring, refer to the detailed events in the `kubectl describe pod nginx` output. This information is crucial for debugging pod-related issues.
</Callout>

## Next Steps

In the following section, we will share some tips and tricks to simplify YAML development with various integrated development environments (IDEs). This will help you efficiently manage and deploy Kubernetes configurations.

***

For more detailed Kubernetes documentation, visit [Kubernetes Documentation](https://kubernetes.io/docs/).\
If you need additional resources or support, consider exploring:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Registry](https://registry.terraform.io/)
* [Docker Hub](https://hub.docker.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/0919dae3-bc94-479f-b205-d52156817c98/lesson/ce127af3-6ffe-4ff9-a547-3f7a314882bc" />
</CardGroup>
