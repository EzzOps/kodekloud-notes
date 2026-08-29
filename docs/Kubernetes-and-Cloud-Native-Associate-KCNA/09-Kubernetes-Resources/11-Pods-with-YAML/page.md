# pod-definition.yml (without namespace)
apiVersion: v1
kind: Pod
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

To ensure that a Pod is always created in a specific namespace (like dev), include the namespace in the definition file:

```yaml theme={null}
# pod-definition.yml (with namespace specified)
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  namespace: dev
  labels:
    app: myapp
    type: front-end
spec:
  containers:
    - name: nginx-container
      image: nginx
```

Then, create the Pod as usual:

```bash theme={null}
kubectl create -f pod-definition.yml
```

### Creating a New Namespace

Just like other Kubernetes objects, you can create a namespace using a definition file. For example:

```yaml theme={null}
# namespace-dev.yml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

Create the namespace with:

```bash theme={null}
kubectl create -f namespace-dev.yml
```

Output:

```text theme={null}
namespace/dev created
```

Alternatively, create a namespace directly from the command line:

```bash theme={null}
kubectl create namespace dev
```

### Switching the Active Namespace

By default, all `kubectl` commands operate in the default namespace. To permanently switch to a different namespace (e.g., dev) in your current context, run:

```bash theme={null}
kubectl config set-context $(kubectl config current-context) --namespace=dev
```

After setting the active namespace, executing:

```bash theme={null}
kubectl get pods
```

will list the Pods in the dev namespace. To view resources from other namespaces, remember to use the `--namespace` flag.

### Setting Resource Quotas

Resource quotas help limit the resources available within a namespace. The following YAML file sets quotas for the dev namespace by specifying limits on Pods, CPU, and memory:

```yaml theme={null}
# compute-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "10"
    limits.memory: 10Gi
```

Apply the resource quota using:

```bash theme={null}
kubectl create -f compute-quota.yaml
```

<Callout icon="lightbulb">
  This configuration ensures that the dev namespace does not exceed the defined resource limits.
</Callout>

## Conclusion

Namespaces in Kubernetes are a powerful tool to isolate resources, manage policies, and efficiently organize your cluster environment—whether for development, testing, or production. By leveraging namespaces, you can deploy applications securely and prevent accidental cross-environment interference.

For more information on Kubernetes concepts, visit the following resources:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)

Happy clustering!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/509501a0-727a-41b9-b9a5-e022735c098e/lesson/eb66d4ad-0202-4731-a35e-95d20772f003" />
</CardGroup>


# Pods with YAML

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Kubernetes-Resources/Pods-with-YAML/page

This tutorial teaches how to create a Kubernetes Pod using a YAML configuration file.

Hello, and welcome to this tutorial on creating a Pod using a YAML-based configuration file. In this guide, you will learn how to write and apply YAML files specifically tailored for Kubernetes. Kubernetes leverages YAML files to create various objects like Pods, ReplicaSets, Deployments, and Services. Each definition file adheres to a common structure containing four top-level fields: apiVersion, kind, metadata, and spec.

## Understanding the Key Fields

Every Kubernetes YAML definition file must include the following properties:

1. The four main properties in every file are: **apiVersion**, **kind**, \*\*metad...

<Callout icon="lightbulb">
  The four main properties in every file are: **apiVersion**, **kind**, **metadata**, and **spec**. These are essential for Kubernetes to correctly parse and create objects.
</Callout>

### 1. apiVersion

This property specifies the version of the Kubernetes API you are using to create your object. For Pods, you typically specify `"v1"`. For other objects like Deployments, you might use `"apps/v1"` or `"extensions/v1beta1"`.

### 2. kind

The `kind` field defines the type of object being created. In this lesson, we will focus on creating a Pod, so you would set `kind` as `"Pod"`. Other common values include ReplicaSet, Deployment, or Service.

### 3. metadata

The `metadata` section contains identifying information about the object, such as its name and labels. It is a dictionary rather than a string. Ensure all keys (like `name` and `labels`) have proper and consistent indentation. For example:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
```

In this snippet:

* `name` uniquely identifies the Pod.
* `labels` are key-value pairs used to categorize and manage Pods based on roles such as front-end, back-end, or database.

### 4. spec

The `spec` section provides detailed configuration for the object. For a Pod, this involves specifying one or more containers that will run within it. The key `containers` holds a list of container definitions; each item in the list is a dictionary containing that container's configuration.

Below is a complete example of defining a Pod using YAML:

```yaml theme={null}
apiVersion: v1
kind: Pod
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

In this configuration:

* The `containers` key defines a list of container specifications.
* The dash before `name` indicates the first (and only) container in the list.
* The container is named `nginx-container` and it uses the Docker image `nginx`.

## Deploying Your Pod

After creating your YAML configuration file (e.g., `pod-definition.yml`), you can deploy the Pod using the following command:

```bash theme={null}
kubectl create -f pod-definition.yml
```

Kubernetes will then create the Pod as defined in your file.

### Checking Pod Status

To verify that your Pod is running, use:

```bash theme={null}
kubectl get pods
```

The output should resemble:

```bash theme={null}
NAME        READY   STATUS    RESTARTS   AGE
myapp-pod   1/1     Running   0          20s
```

To retrieve detailed information about the Pod, execute:

```bash theme={null}
kubectl describe pod myapp-pod
```

This command displays comprehensive details including creation time, labels, container status, and events. An example output might look like:

```bash theme={null}
Name:           myapp-pod
Namespace:      default
Node:           minikube/192.168.99.100
Start Time:     Sat, 03 Mar 2018 14:26:14 +0800
Labels:         app=myapp
                name=myapp-pod
Annotations:    <none>
Status:         Running
IP:             172.17.0.24
Containers:
  nginx:
    Container ID:   docker://830bb56c8c2a86b4b70e9c1488fae1bc38663e491b6c2f5a783e7688b8c9d
    Image:          nginx
    Image ID:       docker-pullable://nginx@sha256:4771d095787c6a605299e110b3ee1e0a2529f5ea261d823e4ffe7a4cab1c5de
    Port:           <none>
    State:          Running
      Started:      Sat, 03 Mar 2018 14:26:21 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-x95w7 (ro)
Conditions:
  Type              Status
  ------            -------
  Initialized       True
  Ready             True
  PodScheduled      True
Events:
  Type     Reason                  Age                From                Message
  ----     ------                  ----               ----                -------
  Normal   Scheduled               34s                default-scheduler   Successfully assigned myapp-pod to minikube
  Normal   SuccessfulMountVolume   34s                kubelet, minikube   MountVolume.Setup succeeded for volume "default-token-x95w7"
  Normal   Pulling                 27s                kubelet, minikube   pulling image "nginx"
  Normal   Pulled                  27s                kubelet, minikube   Successfully pulled image "nginx"
  Normal   Created                 27s                kubelet, minikube   Created container
  Normal   Started                 27s                kubelet, minikube   Started container
```

## Summary

In summary, when creating a YAML file for Kubernetes, always include the four top-level properties:

* **apiVersion**: Specifies the API version.
* **kind**: Defines the type of Kubernetes object.
* **metadata**: Holds essential information such as name and labels.
* **spec**: Details the configuration specifics, such as container settings in a Pod.

This lesson demonstrated how to create a Pod using YAML. The same principles apply when defining other Kubernetes objects such as Deployments, Services, and ReplicaSets. For more information, explore the [Kubernetes Documentation](https://kubernetes.io/docs/).

<Callout icon="lightbulb">
  Consider experimenting with more complex configurations and exploring labels and selectors for robust application management in Kubernetes.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-associate-kcna/module/509501a0-727a-41b9-b9a5-e022735c098e/lesson/c8905088-2df1-4c8d-bfa4-aab04d774863" />
</CardGroup>
