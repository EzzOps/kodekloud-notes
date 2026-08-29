# nginx.yaml
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

Applying the configuration is as simple as running:

```bash theme={null}
kubectl apply -f nginx.yaml
```

Kubernetes will create or update the object automatically to match the state described in your YAML file. When you need to update the configuration—say, to change the image version—you modify the YAML file and apply it again with:

```bash theme={null}
kubectl apply -f nginx.yaml
```

This method ensures that your configuration files remain the single source of truth, which is especially valuable in team environments where version-controlled definitions are critical.

### Imperative vs Declarative Update Dilemma

Sometimes, you might modify a live object using the `kubectl edit` command. This command opens a YAML representation of the current state, including additional fields like status, which are absent from your original configuration file. For instance:

1. Initially, you create the object using your YAML file:

   ```bash theme={null}
   kubectl create -f nginx.yaml
   ```

2. Later, you edit the deployment:

   ```bash theme={null}
   kubectl edit deployment nginx
   ```

3. The live object now contains extra status fields. If you later apply the original `nginx.yaml` (perhaps with updates), your live edits might be overwritten.

> **lightbulb** Always update your local configuration files and use commands like `kubectl replace -f nginx.yaml` to ensure that your changes are consistently tracked and version-controlled.

A typical workflow in a team environment is as follows:

* Create the object:

  ```bash theme={null}
  kubectl create -f nginx.yaml
  ```

* Modify the local file to implement changes (e.g., update the image version).

* Update the live object with:

  ```bash theme={null}
  kubectl replace -f nginx.yaml
  ```

This practice reinforces a version-controlled process and promotes collaboration.

## Choosing the Right Approach

| Approach    | Ideal Use Case                                               | Example Commands                                                                                                                        |
| ----------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Imperative  | Quick, one-off tasks such as creating a pod or deployment.   | `kubectl run --image=nginx nginx`<br />`kubectl create deployment --image=nginx nginx`<br />`kubectl expose deployment nginx --port 80` |
| Declarative | Long-term management with version-controlled infrastructure. | `kubectl apply -f nginx.yaml`<br />`kubectl apply -f /path/to/config-files`                                                             |

* **Imperative Approach:**\
  Use this method for rapid execution when you need to quickly create or modify Kubernetes objects, particularly during certification exams.

* **Declarative Approach:**\
  This approach is recommended for complex, long-term management scenarios. It enables a systematic management of configurations via YAML files, ensuring every change is recorded and version-controlled.

## Exam Tips

When preparing for Kubernetes certification exams, consider the following strategies:

* Use imperative commands for speed when creating simple objects like pods or deployments.
* For modifications or more intricate configurations, adopt the declarative approach by updating configuration files and applying changes using `kubectl apply` or `kubectl replace`.
* Always maintain your YAML files in version control to safeguard against unintentional overwrites.

For more detailed guidance on managing a Kubernetes cluster, check the [official Kubernetes documentation](https://kubernetes.io/docs/) and experiment with both approaches in your lab exercises.

Happy learning, and see you in the next lesson!

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/c6d2ac7d-8192-4cff-aa54-e36d888c5bd9/lesson/b369ac60-39bf-449d-953d-8e05448c8d7e)


# Kube API Server

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Core-Concepts/Kube-API-Server/page

This article provides a comprehensive guide on the Kube API Servers role in managing requests and coordinating components in a Kubernetes cluster.

Welcome to this comprehensive guide on the Kube API Server in Kubernetes. In this article, we explore how the Kube API Server acts as the central management component in a Kubernetes cluster by handling requests from kubectl, validating and authenticating them, interfacing with the etcd datastore, and coordinating with other system components.

When you execute a command like:

```bash theme={null}
kubectl get nodes
```

the utility sends a request to the API Server. The server processes this request by authenticating the user, validating the request, fetching data from the etcd cluster, and replying with the desired information. For example, the output of the command might be:

```plaintext theme={null}
NAME      STATUS   ROLES    AGE   VERSION
master    Ready    master   20m   v1.11.3
node01    Ready    <none>   20m   v1.11.3
```

## API Server Request Lifecycle

When a direct API POST request is made to create a pod, the API Server:

1. Authenticates and validates the request.
2. Constructs a pod object (initially without a node assignment) and updates the etcd store.
3. Notifies the requester that the pod has been created.

For instance, using a curl command:

```bash theme={null}
curl -X POST /api/v1/namespaces/default/pods ...[other]
Pod created!
```

The scheduler continuously monitors the API Server for pods that need node assignments. Once a new pod is detected, the scheduler selects an appropriate node and informs the API Server. The API Server then updates the etcd datastore with the new assignment and passes this information to the Kubelet on the worker node. The Kubelet deploys the pod via the container runtime and later updates the pod status back to the API Server for synchronization with etcd.

> **lightbulb** At the heart of these operations is the Kube API Server, ensuring secure and validated communication between the cluster components.

![The image lists six steps related to the Kube-api Server: Authenticate User, Validate Request, Retrieve Data, Update ETCD, Scheduler, and Kubelet.](https://kodekloud.com/kk-media/image/upload/v1752869720/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Kube-API-Server/frame_130.jpg)

## Deployment and Setup

If your cluster is bootstrapped with a kube admin tool, most of these intricate details are abstracted. However, when setting up a cluster on your own hardware, you need to download the Kube API Server binary from the [Kubernetes release page](https://kubernetes.io/releases/), configure it, and run it as a service on the Kubernetes master node.

## Typical Service Configuration

The Kube API Server is launched with a variety of parameters to secure communication and manage the cluster effectively. Below is an example of a typical service configuration file:

```bash theme={null}
wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kube-apiserver
