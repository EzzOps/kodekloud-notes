# rc-definition.yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: myapp-rc
  labels:
    app: myapp
    type: front-end
spec:
  replicas: 3
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx
```

Once you’ve created the file, run the following command to create the replication controller:

```bash theme={null}
kubectl create -f rc-definition.yaml
```

You should see an output confirming that the replication controller “myapp-rc” has been created. To verify, use these commands:

```bash theme={null}
kubectl get replicationcontroller
kubectl get pods
```

The Pods created by the replication controller will have names starting with `myapp-rc`, indicating their management origin.

## Introducing ReplicaSets

The ReplicaSet is the modern, recommended approach for ensuring a specified number of Pod replicas. In a ReplicaSet definition:

* **apiVersion:** Use `apps/v1` (instead of `v1`).
* **kind:** Set to `ReplicaSet`.
* **metadata and template:** Similar to the replication controller, but with an additional required field.
* **selector:** The `matchLabels` selector identifies which Pods are managed by the ReplicaSet. This field is important because it allows the ReplicaSet to adopt existing Pods that match the provided labels.

Below is an example ReplicaSet definition:

```yaml theme={null}
# replicaset-definition.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-replicaset
  labels:
    app: myapp
    type: front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      type: front-end
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx
```

Create the ReplicaSet using:

```bash theme={null}
kubectl create -f replicaset-definition.yaml
```

Verify its creation with:

```bash theme={null}
kubectl get replicaset
kubectl get pods
```

## Understanding Labels and Selectors

Labels are key-value pairs assigned to Kubernetes objects that enable you to group and select resources. For example, if you deploy three instances of a front-end application as Pods, you can label them accordingly and create a ReplicaSet with a matching selector. This tells the ReplicaSet which Pods to monitor. Even if the Pods already exist, the ReplicaSet will only create new ones if an existing Pod dies, ensuring that the desired number is maintained.

Below is a snippet showing matching labels in a ReplicaSet selector and the corresponding Pod metadata:

```yaml theme={null}
# In the ReplicaSet definition
selector:
  matchLabels:
    tier: front-end
```

```yaml theme={null}
# In the Pod metadata
metadata:
  name: myapp-pod
  labels:
    tier: front-end
```

> **lightbulb** Ensure that the labels defined in the ReplicaSet's selector exactly match those in the Pod template. Mismatches can lead to unexpected behavior where the ReplicaSet fails to manage the intended Pods.

## Scaling a ReplicaSet

If you need to scale your ReplicaSet from 3 to 6 replicas, there are two common approaches:

1. **Update the Definition File:**\
   Modify the `replicas` field in your `replicaset-definition.yaml` file to 6, then apply the change using:
   ```bash theme={null}
   kubectl replace -f replicaset-definition.yaml
   ```

2. **Use the kubectl Scale Command:**\
   Scale directly from the command line with one of these commands:
   ```bash theme={null}
   kubectl scale --replicas=6 -f replicaset-definition.yaml
   ```
   Or by specifying the ReplicaSet name:
   ```bash theme={null}
   kubectl scale --replicas=6 replicaset/myapp-replicaset
   ```

> **lightbulb** Remember that when you use the scale command, the change only affects the running ReplicaSet. The original definition file will still show the previous replica count until you update it.

## Command Review

Below is a quick reference for essential Kubernetes commands used in this lesson:

| Command                               | Description                                  |
| ------------------------------------- | -------------------------------------------- |
| kubectl create -f \<definition-file>  | Create an object from a file                 |
| kubectl get replicationcontroller     | List all replication controllers             |
| kubectl get replicaset                | List all ReplicaSets                         |
| kubectl get pods                      | List all Pods                                |
| kubectl delete replicaset \<name>     | Delete a ReplicaSet by name                  |
| kubectl replace -f \<definition-file> | Update an existing object using a definition |
| kubectl scale --replicas=\<number>    | Scale an object to the specified number      |

This concludes our lesson on replication controllers and ReplicaSets. These controllers ensure that your applications remain highly available, efficiently scaled, and properly load balanced within your Kubernetes cluster.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/eae8cedf-d483-471f-8796-49f69baec6cf/lesson/4cebe7a5-b778-4505-b63b-f5578afa0efb)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/eae8cedf-d483-471f-8796-49f69baec6cf/lesson/71e14ab4-9093-4c7c-8e8e-dbaf26e03c8c)


# Solution Deployments optional

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Core-Concepts/Solution-Deployments-optional/page

This lab article introduces Kubernetes deployments and guides through the process of setting up and validating deployments in a cluster.

In this lab article, you will be introduced to Kubernetes deployments. We will walk through each step of the process while ensuring that your cluster is correctly set up and that deployments function as expected.

## Step 1: Check the Initial Cluster State

Before creating any deployments, verify that your cluster has no existing pods, ReplicaSets, or deployments.

Start by checking for pods:

```bash theme={null}
controlplane ~ ➜ kubectl get pods
No resources found in default namespace.
```

Then, check for ReplicaSets:

```bash theme={null}
controlplane ~ ➜ kubectl get rs
No resources found in default namespace.
```

Finally, check for any deployments:

```bash theme={null}
controlplane ~ ➜ kubectl get deployments
No resources found in default namespace.
```

At this point, your environment is clean with zero pods, zero ReplicaSets, and zero deployments.

## Step 2: Observe Changes After a Deployment is Created

After applying some changes, check the deployments again. You should now see that one deployment exists:

```bash theme={null}
controlplane ~ ➜ kubectl get deployments
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
frontend-deployment   0/4     4            0           10s
```

Examine the ReplicaSet created by that deployment:

```bash theme={null}
controlplane ~ ➜ kubectl get rs
NAME                                   DESIRED   CURRENT   READY   AGE
frontend-deployment-7f8dcd-b696        4         4         0       35s
```

And then inspect the pods:

```bash theme={null}
controlplane ~ ➜ kubectl get pods
NAME                                             READY   STATUS             RESTARTS   AGE
frontend-deployment-7f8dcd-b696-stmbx            0/1     ImagePullBackOff   0          59s
frontend-deployment-7f8dcd-b696-zc6x             0/1     ErrImagePull       0          59s
frontend-deployment-7f8dcd-b696-jgcbx            0/1     ErrImagePull       0          59s
frontend-deployment-7f8dcd-b696-jbr44            0/1     ErrImagePull       0          59s
```

Because none of the four pods are in a ready state, you need to identify which image they are trying to pull. Run the following command to display detailed information for one pod:

```bash theme={null}
kubectl describe pod frontend-deployment-7fd8cdb696-stmbx
```

From the output, notice that the specified image is `busybox:888`. Since this image does not exist, the pods are unable to reach a ready state.

> **lightbulb** The image name must be valid and available in your container registry. Verify the image tag before deployment to avoid issues like ImagePullBackOff.

## Step 3: Create a New Deployment Using a YAML Definition

### Verify Your Current Directory and Files

Ensure you are in the correct working directory and check the available files:

```bash theme={null}
controlplane ~ ➜ pwd
/root

controlplane ~ ➜ ls
deployment-definition-1.yaml  sample.yaml
```

### Attempt to Create the Deployment

Run the following command to create the deployment from the YAML file:

```bash theme={null}
controlplane ~ ➜ kubectl create -f deployment-definition-1.yaml
```

If you encounter an error such as:

```bash theme={null}
Error from server (BadRequest): error when creating "deployment-definition-1.yaml": deployment in version "v1" cannot be handled as a Deployment: no kind "deployment" is registered for version "apps/v1" in scheme "k8s.io/apimachinery/v1.23.3-k3s1/pkg/runtime/scheme.go:100"
```

Open the file to correct the issue:

```bash theme={null}
controlplane ~ ➜ vi deployment-definition-1.yaml
```

### Update the Deployment YAML

The error is caused by incorrect casing in the kind field. The resource kind should be capitalized. Use the corrected YAML below:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment-1
spec:
  replicas: 2
  selector:
    matchLabels:
      name: busybox-pod
  template:
    metadata:
      labels:
        name: busybox-pod
    spec:
      containers:
      - name: busybox-container
        image: busybox888
        command:
        - sh
        - "-c"
        - echo Hello Kubernetes! && sleep 3600
```

After saving the changes, create the deployment again:

```bash theme={null}
controlplane ~ ➜ kubectl create -f deployment-definition-1.yaml
```

## Step 4: Create a Deployment Using Command-Line Parameters

You can also create a deployment by specifying parameters directly in the command line. First, review the help for deployment creation:

```bash theme={null}
kubectl create deployment --help
```

For example, to create a deployment named `http-frontend` using a specified image with three replicas, run:

```bash theme={null}
kubectl create deployment http-frontend --image=<your-image> --replicas=3
```

After executing the command, verify that the deployment and pods are running as expected:

```bash theme={null}
kubectl get deployments
```

Make sure that the `http-frontend` deployment reflects the desired number of replicas in the ready state.

## Final Validation

To ensure all deployments are functioning, validate by checking that all created deployments are running and the pods are in a ready state. This confirms that your environment is correctly configured and operational.

This concludes the lab article on Kubernetes deployments. In upcoming labs, you’ll explore additional Kubernetes functionalities to further enhance your skills.

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/eae8cedf-d483-471f-8796-49f69baec6cf/lesson/55a2e4a6-a148-470e-869a-7cd2ec5e44ca)
