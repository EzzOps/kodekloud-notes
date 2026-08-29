# Solution Pods optional

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Core-Concepts/Solution-Pods-optional/page

This lab teaches working with Pods in Kubernetes using imperative commands and declarative YAML configurations, including creation, inspection, troubleshooting, and updates.

In this lab, you will learn how to work with Pods in Kubernetes using both imperative commands and declarative YAML configurations. The lab covers checking existing Pods, creating new Pods with different images, inspecting their details, troubleshooting common errors, and updating configurations to fix issues.

***

## Listing Existing Pods

Start by listing the Pods in your default namespace. This step helps you verify that no unexpected Pods are running before you begin:

```bash theme={null}
kubectl get pods
```

If no Pods are running, the output will look similar to:

```bash theme={null}
controlplane ~ ⟫ kubectl get pods
No resources found in default namespace.
controlplane ~ ⟫
```

***

## Creating a New Pod with the nginx Image

Next, create a new Pod that uses the nginx image by executing:

```bash theme={null}
kubectl run nginx --image=nginx
```

The output should confirm the creation of the Pod:

```bash theme={null}
kubectl run nginx --image=nginx
pod/nginx created
```

Verify the creation by listing the Pods again:

```bash theme={null}
kubectl get pods
```

You may see multiple Pods, especially if you have done previous exercises. For example:

```bash theme={null}
controlplane ~ ➜ kubectl get pods
NAME            READY   STATUS              RESTARTS   AGE
nginx           0/1     ContainerCreating   0          17s
newpods-llstt   0/1     ContainerCreating   0          11s
newpods-pnnx8   0/1     ContainerCreating   0          11s
newpods-k87fx   0/1     ContainerCreating   0          11s
```

<Callout icon="lightbulb">
  Some Pods might still display "ContainerCreating" as they are in the process of being set up.
</Callout>

***

## Inspecting Pod Details and Verifying the Image

To inspect the details of a specific Pod and verify which image is used, run:

```bash theme={null}
kubectl describe pod <pod-name>
```

For example, the detailed output may include:

```text theme={null}
Node:         controlplane/172.25.0.47
Start Time:   Fri, 15 Apr 2022 18:12:04 +0000
Labels:       tier=busybox
...
Containers:
  busybox:
    Container ID:   containerd://[SECRET_REDACTED]
    Image:          busybox
    Image ID:       docker.io/library/busybox@sha256:[SECRET_REDACTED]
    Command:
      sleep
      1000
    State:           Running
...
```

In this excerpt, the image used is **busybox**. You can also use the wide output option to display node information:

```bash theme={null}
kubectl get pods -o wide
```

The output might be:

```bash theme={null}
NAME              READY   STATUS    RESTARTS   AGE     IP            NODE         NOMINATED NODE   READY
newpods-pnnx8    1/1     Running   0          2m3s    10.42.0.10   controlplane  <none>           <none>
newpods-llstt    1/1     Running   0          2m3s    10.42.0.12   controlplane  <none>           <none>
newpods-k87fx    1/1     Running   0          2m3s    10.42.0.11   controlplane  <none>           <none>
nginx            1/1     Running   0          2m9s    10.42.0.9    controlplane  <none>           <none>
```

***

## Working with a Multi-Container Pod

Consider a Pod named `webapp` that contains two containers. To view the details of this multi-container Pod, run:

```bash theme={null}
kubectl describe pod webapp
```

A sample excerpt from the description might show:

```bash theme={null}
Priority: 0
Node: controlplane/172.25.0.47
Start Time: Fri, 15 Apr 2022 18:14:22 +0000
...
Containers:
  nginx:
    Container ID: containerd://[SECRET_REDACTED]
    Image: nginx
    State: Running
    Ready: True
    Restart Count: 0
    ...
  agentx:
    Container ID: agentx
    Image: agentx
    State: Waiting
    Reason: ErrImagePull
    Ready: False
    Restart Count: 0
    ...
```

In this Pod, the **nginx** container is running normally, while the **agentx** container is in a waiting state due to an image pull error (ErrImagePull). When you list the Pods, observe that the READY column indicates the number of ready containers versus the total containers:

```bash theme={null}
kubectl get pods
NAME            READY   STATUS             RESTARTS   AGE
newpods-pnnx8   1/1     Running            0          2m33s
newpods-llstt   1/1     Running            0          2m33s
newpods-k87fx   1/1     Running            0          2m33s
nginx           1/1     Running            0          2m39s
webapp          0/1     ImagePullBackOff   0          15s
```

<Callout icon="triangle-alert">
  The `ErrImagePull` error indicates that Kubernetes failed to pull the image for the **agentx** container, likely because the image name is incorrect or the image does not exist on Docker Hub.
</Callout>

***

## Deleting the Erroneous Web App Pod

Since the `webapp` Pod contains an image pull error, remove it by running:

```bash theme={null}
kubectl delete pod webapp
```

You should see a deletion confirmation:

```bash theme={null}
pod "webapp" deleted
```

***

## Creating and Correcting a Redis Pod

Now, create a new Pod named `redis` using an intentionally incorrect image name (`redis123`). This exercise demonstrates how to use declarative YAML and fix common errors.

### Step 1: Create the YAML File

Generate the Pod definition using a dry run:

```bash theme={null}
kubectl run redis --image=redis123 --dry-run=client -o yaml
```

Redirect the output to a file named `redis.yaml`. The file should resemble:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: redis
  name: redis
spec:
  containers:
  - image: redis123
    name: redis
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

### Step 2: Create the Redis Pod

Apply the YAML file to create the Pod:

```bash theme={null}
kubectl create -f redis.yaml
```

The expected output is:

```bash theme={null}
pod/redis created
```

Verify the Pod status:

```bash theme={null}
kubectl get pods
```

The output may look like:

```bash theme={null}
NAME            READY   STATUS         RESTARTS   AGE
newpods-pnnx8   1/1     Running        0          8m16s
newpods-llstt   1/1     Running        0          8m16s
newpods-k87fx   1/1     Running        0          8m16s
nginx           1/1     Running        0          8m22s
redis           0/1     ErrImagePull   0          10s
```

Since the image name `redis123` is invalid, the Pod enters an `ErrImagePull` state.

### Step 3: Update the YAML File with the Correct Image

Edit the `redis.yaml` file to update the image name from `redis123` to `redis`. The updated file should be:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: redis
  name: redis
spec:
  containers:
  - image: redis
    name: redis
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Apply the changes with:

```bash theme={null}
kubectl apply -f redis.yaml
```

You might see a warning indicating that the Pod is missing an annotation necessary for future apply operations. After updating, verify the status again:

```bash theme={null}
kubectl get pods
```

An example output is:

```bash theme={null}
NAME            READY   STATUS    RESTARTS   AGE
newpods-pnnx8   1/1     Running   0          9m38s
newpods-llstt   1/1     Running   0          9m38s
newpods-k87fx   1/1     Running   0          9m44s
nginx           1/1     Running   0          9m44s
redis           1/1     Running   0          92s
```

The `redis` Pod is now running correctly thanks to the valid Docker image.

***

## Conclusion

In this lab, you learned how to:

* List existing Pods in a Kubernetes cluster.
* Create new Pods using imperative commands with different images.
* Inspect detailed information about Pods to verify configurations.
* Troubleshoot common issues like image pull errors.
* Use declarative YAML configurations to manage and update Pods.

Happy clustering and keep exploring more Kubernetes features!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/eae8cedf-d483-471f-8796-49f69baec6cf/lesson/30117c21-15b2-4bd2-871e-a5e4f49635c6" />
</CardGroup>
